"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import asyncio
import hashlib
import json
import logging
import re
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional

import polars as pl

from models.result import BaseResult
from tools.utils import generate_simple_id, SIMPLE_ID_LENGTH

logger = logging.getLogger(__name__)

DATAFRAME_JSON_SIZE_THRESHOLD = 8000

DATAFRAME_ID_MAX_ATTEMPTS = 10

_dataframes: Dict[str, "DataFrameRecord"] = {}
_write_lock = asyncio.Lock()
_sql_context = pl.SQLContext()

_DISALLOWED_SQL_PATTERN = re.compile(
    r"\b(insert|update|delete|create|drop|alter|truncate|replace|merge|call|copy|grant|revoke)\b",
    re.IGNORECASE,
)
_LEADING_SQL_COMMENTS_PATTERN = re.compile(
    r"^(?:\s*(?:--[^\n]*\n|/\*.*?\*/))*\s*",
    re.DOTALL,
)
_SQL_LINE_COMMENT_PATTERN = re.compile(r"--[^\n]*")
_SQL_BLOCK_COMMENT_PATTERN = re.compile(r"/\*.*?\*/", re.DOTALL)
_ORDER_BY_PATTERN = re.compile(r"\border\s+by\b", re.IGNORECASE)
_LIMIT_PATTERN = re.compile(r"\blimit\b", re.IGNORECASE)
_OFFSET_PATTERN = re.compile(r"\boffset\b", re.IGNORECASE)


@dataclass
class DataFrameRecord:
    dataframe_id: str
    table_name: str
    created_at: str
    origin_manager: str
    origin_action: str
    rows: int
    columns: int
    schema: List[Dict[str, str]]
    schema_hash: str
    json_size_chars: int
    dataframe: pl.DataFrame

    def to_metadata(self, include_schema: bool = True) -> Dict[str, Any]:
        metadata = asdict(self)
        metadata.pop("dataframe", None)
        if not include_schema:
            metadata.pop("schema", None)
        return metadata


def _json_default_serializer(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def serialize_result_to_compact_json(result: List[Any]) -> str:
    return json.dumps(result, separators=(",", ":"), ensure_ascii=False, default=_json_default_serializer)


def build_dataframe_from_result(result: List[Any]) -> pl.DataFrame:
    normalized = json.loads(serialize_result_to_compact_json(result))

    # matrix envelope: [{"columns":[...], "rows":[...]}]
    if (
            isinstance(normalized, list)
            and len(normalized) == 1
            and isinstance(normalized[0], dict)
            and set(normalized[0].keys()) == {"columns", "rows"}
            and isinstance(normalized[0]["columns"], list)
            and isinstance(normalized[0]["rows"], list)
    ):
        matrix = normalized[0]
        return pl.DataFrame(matrix["rows"], schema=[str(c) for c in matrix["columns"]], orient="row")

    # columnar envelope: [{"colA":[...], "colB":[...]}]
    if (
            isinstance(normalized, list)
            and len(normalized) == 1
            and isinstance(normalized[0], dict)
            and normalized[0]
            and all(isinstance(v, list) for v in normalized[0].values())
    ):
        col_lengths = {len(v) for v in normalized[0].values()}
        if len(col_lengths) == 1:
            return pl.DataFrame(normalized[0])

    if isinstance(normalized, list):
        if not normalized:
            return pl.DataFrame()
        if all(isinstance(item, dict) for item in normalized):
            return pl.DataFrame(normalized)
        return pl.DataFrame({"value": normalized})
    if isinstance(normalized, dict):
        return pl.DataFrame([normalized])
    return pl.DataFrame({"value": [normalized]})


def auto_flatten_wide(
        df: pl.DataFrame,
        max_passes: int = 30,
        sep: str = "__",
) -> pl.DataFrame:
    """
    Flatten nested structures in a DataFrame for SQL queryability.

    - Nested structs: expanded into flat columns with path-style names
      (e.g. configuration__threads, config__inner__b). Only flattens down to leaf scalars.
    - List columns: flattened to scalar (first element). List of structs becomes
      the struct fields of the first element with path prefix; list of scalars
      becomes the first scalar.
    - Preserves original row count.
    - Safe for schemas with configuration, override_executions, and similar nested structures.
    """
    for _ in range(max_passes):
        struct_cols = [c for c, dt in df.schema.items() if isinstance(dt, pl.Struct)]
        list_cols = [c for c, dt in df.schema.items() if isinstance(dt, pl.List)]

        if not struct_cols and not list_cols:
            break

        # Flatten list columns: take first element, then unnest if struct
        for col in list_cols:
            inner = getattr(df.schema[col], "inner", None)
            is_struct_inner = inner is not None and isinstance(inner, pl.Struct)

            temp = f"{col}{sep}temp"
            expr = pl.col(col).fill_null([]).list.first()
            df = df.with_columns(expr.alias(temp))

            if is_struct_inner:
                df = df.unnest(temp).drop(col)
                # Rename to path format: col__field_name
                fields = getattr(inner, "fields", [])
                rename_map = {f.name: f"{col}{sep}{f.name}" for f in fields}
                df = df.rename(rename_map)
            else:
                df = df.drop(col).rename({temp: col})

        # Unnest struct columns one at a time, renaming to path format
        struct_cols = [c for c, dt in df.schema.items() if isinstance(dt, pl.Struct)]
        for col in struct_cols:
            struct_dtype = df.schema[col]
            fields = getattr(struct_dtype, "fields", [])
            rename_map = {f.name: f"{col}{sep}{f.name}" for f in fields}
            df = df.unnest(col)
            df = df.rename(rename_map)

    return df


def _to_schema_rows(dataframe: pl.DataFrame) -> List[Dict[str, str]]:
    schema = dataframe.schema
    return [{"name": name, "dtype": str(dtype)} for name, dtype in schema.items()]


def _schema_hash(schema_rows: List[Dict[str, str]]) -> str:
    payload = json.dumps(schema_rows, separators=(",", ":"), ensure_ascii=False)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()


def _stable_hash(payload: str) -> str:
    return hashlib.md5(payload.encode("utf-8")).hexdigest()


def _normalize_root_dtype(dtype: str) -> str:
    dtype_str = str(dtype or "").strip()
    if dtype_str.startswith("Struct("):
        return "Struct"
    if dtype_str.startswith("List("):
        inner = dtype_str[5:-1].strip() if dtype_str.endswith(")") else ""
        if inner.startswith("Struct("):
            return "List(Struct)"
        return "List"
    if dtype_str.startswith("Array("):
        inner = dtype_str[6:-1].strip() if dtype_str.endswith(")") else ""
        if inner.startswith("Struct("):
            return "Array(Struct)"
        return "Array"
    return dtype_str


def _canonicalize_top_schema(schema_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    top_level = [
        {"name": str(row.get("name", "")), "dtype": _normalize_root_dtype(str(row.get("dtype", "")))}
        for row in schema_rows
    ]
    return sorted(top_level, key=lambda col: col["name"])


async def register_dataframe(
        result: List[Any],
        origin_manager: str,
        origin_action: str,
        json_size_chars: int,
        flatten: bool = True,
) -> Dict[str, Any]:
    dataframe = build_dataframe_from_result(result)
    return await _register_dataframe_instance(
        dataframe, origin_manager, origin_action, json_size_chars, flatten=flatten
    )


def _allocate_dataframe_id() -> str:
    for _ in range(DATAFRAME_ID_MAX_ATTEMPTS):
        candidate = generate_simple_id()
        if candidate not in _dataframes:
            return candidate

    logger.error(
        "Unable to allocate dataframe id. attempts=%s id_length=%s active_pool_size=%s",
        DATAFRAME_ID_MAX_ATTEMPTS,
        SIMPLE_ID_LENGTH,
        len(_dataframes),
    )
    raise RuntimeError(f"Unable to allocate dataframe id after {DATAFRAME_ID_MAX_ATTEMPTS} attempts.")


async def _register_dataframe_instance(
        dataframe: pl.DataFrame,
        origin_manager: str,
        origin_action: str,
        json_size_chars: int,
        flatten: bool = True,
) -> Dict[str, Any]:
    if flatten:
        try:
            dataframe = auto_flatten_wide(dataframe)
        except Exception:
            pass  # Keep original dataframe if flattening fails
    dataframe_id = _allocate_dataframe_id()
    table_name = f"df_{dataframe_id}"
    record = DataFrameRecord(
        dataframe_id=dataframe_id,
        table_name=table_name,
        created_at=datetime.now(UTC).isoformat(),
        origin_manager=origin_manager,
        origin_action=origin_action,
        rows=dataframe.height,
        columns=dataframe.width,
        schema=(schema_rows := _to_schema_rows(dataframe)),
        schema_hash=_schema_hash(schema_rows),
        json_size_chars=json_size_chars,
        dataframe=dataframe,
    )
    async with _write_lock:
        _sql_context.register(table_name, dataframe)
        _dataframes[dataframe_id] = record
    return record.to_metadata()


async def materialize_large_result_if_needed(
        base_result: BaseResult,
        origin_manager: str,
        origin_action: str,
        force: bool = False
) -> BaseResult:
    if not isinstance(base_result, BaseResult) or base_result.error or base_result.result is None:
        return base_result
    if (
            isinstance(base_result.result, list)
            and len(base_result.result) == 1
            and isinstance(base_result.result[0], dict)
            and base_result.result[0].get("stored_as_dataframe") is True
            and base_result.result[0].get("dataframe_id")
    ):
        # Avoid rematerializing a payload that is already a dataframe reference.
        return base_result
    try:
        compact_json = serialize_result_to_compact_json(base_result.result)
        json_size_chars = len(compact_json)
    except Exception as exc:
        base_result.append_warnings(
            [f"Result size check failed, skipping dataframe materialization: {exc}"]
        )
        return base_result

    if not force and json_size_chars <= DATAFRAME_JSON_SIZE_THRESHOLD:
        return base_result

    try:
        dataframe_preview = build_dataframe_from_result(base_result.result)
    except Exception as exc:
        base_result.append_warnings(
            [f"Result dataframe preview failed, skipping dataframe materialization: {exc}"]
        )
        return base_result

    if dataframe_preview.height == 0:
        base_result.append_info([
            "Result contains no rows; dataframe was not created."
        ])
        return base_result

    metadata = await _register_dataframe_instance(
        dataframe=dataframe_preview,
        origin_manager=origin_manager,
        origin_action=origin_action,
        json_size_chars=json_size_chars,
    )
    base_result.result = [{
        "stored_as_dataframe": True,
        "dataframe_id": metadata["dataframe_id"],
        "table_name": metadata["table_name"],
        "rows": metadata["rows"],
        "columns": metadata["columns"],
        "schema_hash": metadata["schema_hash"],
        "json_size_chars": metadata["json_size_chars"],
    }]
    base_result.append_info([
        "Large result was stored as an in-memory dataframe. Use blazemeter_tools with action "
        "'dataframes_list'/'dataframes_get' to inspect metadata and 'dataframes_query' to read data with SQL.",
        "ORDER BY + LIMIT + OFFSET are mandatory in every dataframe query.",
        "Use a prudent default page size of up to 100 rows (for example, LIMIT 100 OFFSET 0), then continue paging as needed.",
        "When the dataframe is no longer needed, free resources with 'dataframes_remove' or 'dataframes_clear'.",
    ])
    return base_result


async def list_dataframes_metadata(include_schema: bool = False) -> List[Dict[str, Any]]:
    async with _write_lock:
        return [record.to_metadata(include_schema=include_schema) for record in _dataframes.values()]


async def get_dataframe_metadata(dataframe_id: str, include_schema: bool = True) -> Optional[Dict[str, Any]]:
    async with _write_lock:
        record = _dataframes.get(dataframe_id)
        if not record:
            return None
        return record.to_metadata(include_schema=include_schema)


async def group_dataframe_schemas(dataframe_id_list: Optional[List[str]] = None) -> Dict[str, Any]:
    async with _write_lock:
        if dataframe_id_list:
            requested = [str(df_id) for df_id in dataframe_id_list]
            selected = [record for df_id in requested if (record := _dataframes.get(df_id))]
            missing = [df_id for df_id in requested if df_id not in _dataframes]
        else:
            selected = list(_dataframes.values())
            missing = []
        top_groups: Dict[str, Dict[str, Any]] = {}
        for record in selected:
            top_schema = _canonicalize_top_schema(record.schema)
            top_signature = json.dumps(top_schema, separators=(",", ":"), ensure_ascii=False)
            top_hash = _stable_hash(top_signature)
            group = top_groups.setdefault(
                top_hash,
                {
                    "dataframes": [],
                    "_columns": {},
                },
            )
            group["dataframes"].append(
                record.dataframe_id
            )

            schema_by_name = {str(col.get("name", "")): str(col.get("dtype", "")) for col in record.schema}
            for top_col in top_schema:
                column_name = top_col["name"]
                full_dtype = schema_by_name.get(column_name, "__MISSING__")
                schema_preview = full_dtype
                version_signature = json.dumps({"dtype": full_dtype}, separators=(",", ":"), ensure_ascii=False)
                column_hash = _stable_hash(version_signature)

                column_group = group["_columns"].setdefault(
                    column_name,
                    {
                        "name": column_name,
                        "_versions": {},
                    },
                )
                version_group = column_group["_versions"].setdefault(
                    column_hash,
                    {
                        "hash": column_hash,
                        "column_schema": schema_preview,
                        "dataframes": [],
                    },
                )
                version_group["dataframes"].append(
                    record.dataframe_id
                )

        top_level_groups = []
        df_sets: Dict[str, str] = {}
        dataframe_set_index: Dict[tuple[str, ...], str] = {}
        next_df_set_id = 1

        def _register_dataframe_set(ids: List[str]) -> str:
            nonlocal next_df_set_id
            normalized = tuple(sorted(set(ids)))
            if normalized in dataframe_set_index:
                return dataframe_set_index[normalized]
            set_id = str(next_df_set_id)
            next_df_set_id += 1
            dataframe_set_index[normalized] = set_id
            df_sets[set_id] = ",".join(normalized)
            return set_id

        for top_hash in sorted(top_groups.keys()):
            group = top_groups[top_hash]
            columns = []
            varying_columns: List[str] = []
            for column_name in sorted(group["_columns"].keys()):
                column_group = group["_columns"][column_name]
                variations = []
                for column_hash in sorted(column_group["_versions"].keys()):
                    version = dict(column_group["_versions"][column_hash])
                    version["df_ref"] = _register_dataframe_set(version.pop("dataframes"))
                    version.pop("hash", None)
                    variations.append(version)
                if len(variations) > 1:
                    varying_columns.append(column_group["name"])
                columns.append(
                    {
                        "name": column_group["name"],
                        "variations": variations,
                    }
                )
            top_level_groups.append(
                {
                    "df_ref": _register_dataframe_set(group["dataframes"]),
                    "varying_columns": ",".join(varying_columns),
                    "columns": columns,
                }
            )

        return {
            "groups": top_level_groups,
            "df_sets": df_sets,
            "missing_df_ids": ",".join(missing),
        }


def _sanitize_sql_for_keyword_scan(sql: str) -> str:
    without_comments = _SQL_BLOCK_COMMENT_PATTERN.sub(" ", _SQL_LINE_COMMENT_PATTERN.sub(" ", sql))
    # Remove string and quoted identifier contents to avoid false positives, e.g. SELECT 'delete'
    sanitized = re.sub(r"'(?:''|[^'])*'", "''", without_comments)
    sanitized = re.sub(r'"(?:""|[^"])*"', '""', sanitized)
    sanitized = re.sub(r"`(?:``|[^`])*`", "``", sanitized)
    return sanitized


def _validate_sql_read_only(sql: str) -> Optional[str]:
    without_comments = _LEADING_SQL_COMMENTS_PATTERN.sub("", sql or "")
    lowered = without_comments.strip().lower()
    if not lowered:
        return "SQL query is empty. Provide a SELECT query."
    if not (lowered.startswith("select") or lowered.startswith("with")):
        return (
            "Only read-only SQL is allowed. Start queries with SELECT or WITH (CTE + SELECT). "
            "ORDER BY + LIMIT + OFFSET are mandatory for all dataframe queries."
        )
    sanitized = _sanitize_sql_for_keyword_scan(lowered)
    if not _ORDER_BY_PATTERN.search(sanitized):
        return (
            "Deterministic pagination required. ORDER BY is mandatory for dataframe queries. "
            "Use ORDER BY + LIMIT + OFFSET in every query, for example: "
            "SELECT * FROM df_x ORDER BY created_at DESC LIMIT 100 OFFSET 0."
        )
    if not _LIMIT_PATTERN.search(sanitized):
        return (
            "Deterministic pagination required. LIMIT is mandatory for dataframe queries. "
            "Use ORDER BY + LIMIT + OFFSET in every query, for example: "
            "SELECT * FROM df_x ORDER BY created_at DESC LIMIT 100 OFFSET 0."
        )
    if not _OFFSET_PATTERN.search(sanitized):
        return (
            "Deterministic pagination required. OFFSET is mandatory for dataframe queries. "
            "Use ORDER BY + LIMIT + OFFSET in every query, for example: "
            "SELECT * FROM df_x ORDER BY created_at DESC LIMIT 100 OFFSET 0."
        )
    disallowed = _DISALLOWED_SQL_PATTERN.search(sanitized)
    if disallowed:
        return (
            f"SQL statement '{disallowed.group(1).upper()}' is not allowed in dataframe queries. "
            "Allowed entry points are SELECT and WITH."
        )
    return None


def query_dataframes(sql: str, output_format: str = "matrix") -> Dict[str, Any]:
    sql_error = _validate_sql_read_only(sql)
    if sql_error:
        return {"error": sql_error}
    normalized_output_format = str(output_format or "matrix").strip().lower()
    if normalized_output_format not in {"matrix", "columnar", "records"}:
        return {"error": "Invalid output_format. Allowed values: matrix, columnar, records."}
    try:
        query_result = _sql_context.execute(sql)
        if hasattr(query_result, "collect"):
            query_result = query_result.collect()
        if not isinstance(query_result, pl.DataFrame):
            query_result = pl.DataFrame(query_result)
        if normalized_output_format == "columnar":
            result_payload = [query_result.to_dict(as_series=False)]
        elif normalized_output_format == "records":
            result_payload = query_result.to_dicts()
        else:
            result_payload = [{
                "columns": query_result.columns,
                "rows": [list(row) for row in query_result.rows()],
            }]
        return {
            "result": result_payload,
            "rows": query_result.height,
            "columns": query_result.width,
            "schema": _to_schema_rows(query_result),
            "output_format": normalized_output_format,
        }
    except Exception as exc:
        error_text = str(exc)
        lowered = error_text.lower()
        if "not found" in lowered and ("table" in lowered or "relation" in lowered):
            guidance = (
                "Table not found in SQL context. Use dataframes_list to discover available table_name values, "
                "then retry your query."
            )
        elif "column" in lowered and "not found" in lowered:
            guidance = (
                "Column not found. Use dataframes_get to inspect schema and exact column names before querying."
            )
        elif "syntax" in lowered or "parse" in lowered:
            guidance = (
                "SQL syntax error. Use dataframes_sql_help for allowed SQL operations and examples."
            )
        else:
            guidance = (
                "Use dataframes_sql_help first for supported SQL semantics. "
                "For multi-dataframe queries, run dataframes_schema_groups before broad schema inspection. "
                "Use dataframes_get selectively for outliers or ambiguous fields."
            )
        return {
            "error": (
                f"SQL query failed: {exc}. {guidance}"
            )
        }


async def remove_dataframe(dataframe_id: str) -> bool:
    async with _write_lock:
        record = _dataframes.pop(dataframe_id, None)
        if not record:
            return False
        try:
            _sql_context.unregister(record.table_name)
        except Exception:
            pass
        return True


async def clear_dataframes() -> int:
    async with _write_lock:
        ids = list(_dataframes.keys())
        for dataframe_id in ids:
            record = _dataframes.pop(dataframe_id, None)
            if not record:
                continue
            try:
                _sql_context.unregister(record.table_name)
            except Exception:
                pass
        return len(ids)


def get_sql_capabilities() -> Dict[str, Any]:
    return {
        "engine_scope": {
            "query_entrypoints": ["SELECT", "WITH"],
            "mode": "read-only",
            "description": "SQL support is available for SELECT/WITH queries with BlazeMeter MCP query constraints.",
        },
        "allowed_entrypoints": ["SELECT", "WITH"],
        "disallowed_statements": [
            "INSERT",
            "UPDATE",
            "DELETE",
            "CREATE",
            "DROP",
            "ALTER",
            "TRUNCATE",
            "REPLACE",
            "MERGE",
            "CALL",
            "COPY",
            "GRANT",
            "REVOKE",
        ],
        "allowed_features": [
            "JOIN",
            "UNION",
            "UNION ALL",
            "CTE (WITH)",
            "GROUP BY",
            "HAVING",
            "ORDER BY",
            "LIMIT",
            "OFFSET",
            "aggregations",
            "UNNEST",
        ],
        "supported_functions": [
            "ABS", "ACOS", "ACOSD", "ARRAY_CONTAINS", "ARRAY_GET", "ARRAY_LENGTH", "ARRAY_LOWER", "ARRAY_MEAN",
            "ARRAY_REVERSE", "ARRAY_SUM", "ARRAY_TO_STRING", "ARRAY_UNIQUE", "ARRAY_UPPER", "ASIN", "ASIND",
            "ATAN", "ATAN2", "ATAN2D", "ATAND", "AVG", "BIT_LENGTH", "CBRT", "CEIL", "COALESCE", "CONCAT",
            "CONCAT_WS", "COS", "COSD", "COT", "COTD", "COUNT", "DATE", "DATE_PART", "DEGREES", "ENDS_WITH",
            "EXP", "EXTRACT", "FIRST", "FLOOR", "GREATEST", "IF", "IFNULL", "INITCAP", "LAST", "LEAST", "LEFT",
            "LENGTH", "LN", "LOG", "LOG1P", "LOG10", "LOG2", "LOWER", "LTRIM", "MAX", "MEDIAN", "MIN", "MOD",
            "NULLIF", "OCTET_LENGTH", "PI", "POW", "RADIANS", "REGEXP_LIKE", "REPLACE", "REVERSE", "RIGHT",
            "ROUND", "RTRIM", "SIGN", "SIN", "SIND", "SQRT", "STARTS_WITH", "STDDEV", "STRPOS", "SUBSTRING",
            "SUM", "TAN", "TAND", "UNNEST", "UPPER", "VARIANCE"
        ],
        "unsupported_functions": [
            {"name": "STRUCT_EXTRACT", "reason": "Not recognized in this SQL context."},
            {"name": "TO_JSON", "reason": "Not recognized in this SQL context."},
            {"name": "TYPEOF", "reason": "Not recognized in this SQL context."},
        ],
        "unsupported_or_unstable_patterns": [
            "Complex chained nested access with mixed subscript and dot notation in a single expression",
            "Casting LIST/STRUCT directly to STRING for inspection",
            "Nested extraction without staged CTE when list expansion is required",
            "Unqualified join keys that create ambiguous column references",
        ],
        "ai_common_mistakes": [
            "Assuming generic warehouse helper functions are available",
            "Building one very large query instead of staged CTEs",
            "Skipping aliases in JOIN/CTE steps",
            "Trying direct list aggregations (for example list_max on nested overrides) instead of UNNEST + staged CTE",
            "Trying unsupported helper functions before checking supported_functions",
            "Assuming nested/scalar fields are homogeneous across dataframes without checking schemas first",
            "Inspecting every dataframe with dataframes_get before checking grouped schema differences",
            "Using direct nested extraction in the first multi-dataframe query after schema groups reports column variations",
            "Assuming single dataframe justifies bypassing the robust UNNEST/CTE pattern for nested/list fields",
            "Trying the 'fast' direct nested access first when the query touches nested/list fields",
            "Try-fast: attempting the simplest path first and retrying on failure instead of reasoning through the design before executing",
            "Not considering all values in a nested list when searching for max/min, which can miss important extreme values",
            "Using only the first element of a nested list instead of aggregating over all its values",
        ],
        "query_rules": [
            "CRITICAL: Before writing queries that combine 2 or more dataframes, run dataframes_schema_groups first to validate schema compatibility across all involved dataframes.",
            "CRITICAL: Use dataframes_get only for targeted drill-down on dataframes flagged by schema groups as different or ambiguous for required fields.",
            "CRITICAL: Hard gate: if schema groups reports column variations, direct nested extraction is forbidden in the first query.",
            "CRITICAL: If the query touches nested/list fields, direct nested access is forbidden. Always use the robust pattern: UNNEST -> aggregate -> join-back in CTEs. No exception for single dataframe.",
            "IMPORTANT: Validate schema compatibility before using nested fields.",
            "ORDER BY + LIMIT + OFFSET are mandatory in every dataframe query.",
            "Use deterministic pagination: ORDER BY + LIMIT + OFFSET.",
            "Recommended default page size: LIMIT 100 OFFSET 0, then continue paging.",
            "If loading data with result_format=dataframe, prefer one initial fetch with the maximum allowed tool limit, then paginate/filter in dataframes_query.",
            "CRITICAL: When a query includes UNNEST + CTE + JOIN, always enforce explicit join-key renaming and qualification. Rename the base key in the UNNEST CTE (e.g. test_id AS base_test_id) and use only that renamed key downstream.",
            "For CTE-heavy joins, rename join keys in intermediate CTEs (for example test_id AS t_id or base_test_id).",
            "Single dataframe query flow (scalar-only): dataframes_sql_help -> dataframes_get -> dataframes_query.",
            "Single dataframe query flow (nested/list fields): dataframes_sql_help -> dataframes_get -> staged CTE (UNNEST -> aggregate -> join-back) -> dataframes_query. Same robust pattern as multi-dataframe.",
            "Multi-dataframe nested flow: dataframes_sql_help -> dataframes_schema_groups -> targeted dataframes_get -> staged CTE (UNNEST -> aggregate -> join-back) -> final query.",
            "If schema groups returns a CRITICAL variation warning, call dataframes_sql_help again immediately before writing the final query.",
            "Direct nested access is allowed only when each required nested column has exactly one variation across all relevant dataframes in schema groups.",
        ],
        "nested_unnest_intro": (
            "To query and aggregate data from a list of structs (e.g., override_executions), use UNNEST in a CTE to flatten the list, "
            "then aggregate and compare with scalar fields using GREATEST/LEAST. See query_examples.good for the compact pattern."
        ),
        "nested_list_pre_sql_checklist": [
            "Step 1: Identify if the query touches nested/list (List, Struct, Array in schema). Step 2: If yes, confirm robust pattern. Step 3: Design the CTE structure. Step 4: Execute. Do not skip to Step 4.",
            "Before launching SQL that touches nested/list fields, explicitly confirm: 'There are nested/list fields; I use the robust UNNEST -> aggregate -> join-back pattern.'",
            "Do not attempt the 'fast' direct nested extraction first. Start with the robust CTE pattern.",
            "Single dataframe is NOT an exception: use the same robust pattern when querying nested/list columns.",
            "Anti-ambiguity checklist (UNNEST+CTE+JOIN): No unqualified key columns in SELECT, JOIN, GROUP BY, or ORDER BY; UNNEST CTE key is renamed (base_* or src_*); join-back uses different left/right key names; final projection is scalar-only; query ends with ORDER BY ... LIMIT ... OFFSET.",
        ],
        "pre_execution_reasoning": [
            "Before dataframes_query: reason step-by-step. (1) Schema check: what columns and types? (2) Nested/list? If List, Struct, Array → robust pattern. (3) Pattern selection: scalar-only vs UNNEST/CTE. (4) Design the query structure. (5) Confirm, then execute.",
            "Do not try-fast. Design before do.",
        ],
        "recommended_patterns": [
            "Prefer one final aggregation query over multiple partial queries when feasible",
            "Build queries incrementally: base SELECT -> UNNEST CTE -> aggregate -> join -> final sort/page",
            "Use a dedicated CTE for UNNEST operations on nested arrays/lists",
            "If a nested field fails, use the robust pattern: UNNEST -> aggregate -> join-back.",
            "First nested-field query must use the robust UNNEST/CTE pattern. Never try direct nested access first. No exception for single dataframe.",
            "Alias every table and CTE explicitly",
            "Rename join keys in CTEs (for example: t_id, base_test_id, src_test_id) before joins to avoid ambiguous references",
            "Join-key hygiene for UNNEST+CTE+JOIN: (1) In UNNEST CTE rename base key immediately (test_id AS base_test_id). (2) In downstream CTEs use only the renamed key (GROUP BY base_test_id). (3) In join-back use fully-qualified names (ON b.test_id = a.base_test_id). (4) In final SELECT prefix columns with table alias. (5) Never reuse generic key names across CTE boundaries.",
            "Use COALESCE/CASE for fallback values after joins",
            "UNION ALL only scalar projections; avoid UNION over nested struct/list columns",
            "Validate each CTE with a small LIMIT before composing final query",
            "For multi-dataframe analysis, use schema groups first, then perform targeted per-dataframe inspection only when needed.",
            "To get the maximum value between a scalar field and all values in a nested list per record, use UNNEST on the list, then GROUP BY and GREATEST(MAX(list.field), MAX(scalar)).",
            "Before UNION ALL, normalize each branch to the same concrete type your next step expects (e.g. INTEGER year, not “string then parse after union”).",
        ],
        "known_engine_pitfalls": [
            "CTE + JOIN resolution may treat same-name keys as ambiguous even when aliases are present; rename join keys in the UNNEST stage (base_*/src_*) to guarantee deterministic resolution",
            "Alias/join-key resolution may fail in some CTE + JOIN combinations",
            "Ambiguous join keys are common if columns are not fully qualified",
            "Nested schema drift across tables can break field resolution",
            "UNION over nested struct/list columns is fragile; normalize to scalar output first",
            "Direct list aggregation over nested overrides is brittle; UNNEST + MAX + join-back is more reliable",
        ],
        "nested_query_recipe": [
            "Base table CTE",
            "UNNEST CTE",
            "Aggregate CTE (for example MAX over nested field)",
            "Join aggregate back to base",
            "Apply null-safe metric expression (for example GREATEST(COALESCE(default1,0), COALESCE(default2,0), COALESCE(override_max,0)))",
            "Emit scalar projection only",
            "UNION ALL scalar projections only",
            "Final ORDER BY + LIMIT + OFFSET",
        ],
        "debug_ladder": [
            "A) Run schema groups for all candidate dataframes and identify only the outliers to inspect with dataframes_get.",
            "B) base SELECT LIMIT 10",
            "C) UNNEST stage LIMIT 10",
            "D) aggregate stage LIMIT 10",
            "E) join result LIMIT 10",
            "F) add ranking and pagination",
            "G) add next table to UNION ALL and repeat",
        ],
        "query_examples": {
            "good": [
                "SELECT * FROM df_tests ORDER BY test_id LIMIT 100 OFFSET 0",
                "WITH expanded AS (SELECT t.test_id, UNNEST(t.override_executions) AS ov FROM df_tests t), "
                "agg AS (SELECT e.test_id, MAX(e.ov.concurrency) AS max_concurrency FROM expanded e GROUP BY e.test_id) "
                "SELECT t.test_id, t.test_name, "
                "GREATEST(COALESCE(t.configuration.threads, 0), COALESCE(a.max_concurrency, 0)) AS max_concurrency_used "
                "FROM df_tests t LEFT JOIN agg a ON t.test_id = a.test_id "
                "ORDER BY max_concurrency_used DESC, t.test_id ASC LIMIT 10 OFFSET 0",
                "WITH a AS (SELECT test_id, test_name FROM df_a), b AS (SELECT test_id, test_name FROM df_b) "
                "SELECT * FROM a UNION ALL SELECT * FROM b ORDER BY test_id LIMIT 100 OFFSET 0",
                "WITH s1_exp AS (SELECT t.test_id AS t_id, UNNEST(t.override_executions) AS ov FROM df_a t), "
                "s1_agg AS (SELECT e.t_id, MAX(e.ov.concurrency) AS ov_max FROM s1_exp e GROUP BY e.t_id), "
                "s1 AS (SELECT t.test_id, t.test_name, GREATEST(COALESCE(t.configuration.threads,0), COALESCE(a.ov_max,0)) "
                "AS max_concurrency_used FROM df_a t LEFT JOIN s1_agg a ON t.test_id = a.t_id), "
                "s2_exp AS (SELECT t.test_id AS t_id, UNNEST(t.override_executions) AS ov FROM df_b t), "
                "s2_agg AS (SELECT e.t_id, MAX(e.ov.concurrency) AS ov_max FROM s2_exp e GROUP BY e.t_id), "
                "s2 AS (SELECT t.test_id, t.test_name, GREATEST(COALESCE(t.configuration.threads,0), COALESCE(a.ov_max,0)) "
                "AS max_concurrency_used FROM df_b t LEFT JOIN s2_agg a ON t.test_id = a.t_id), "
                "all_rows AS (SELECT test_id, test_name, max_concurrency_used FROM s1 UNION ALL "
                "SELECT test_id, test_name, max_concurrency_used FROM s2) "
                "SELECT test_name, test_id, max_concurrency_used FROM all_rows "
                "ORDER BY max_concurrency_used DESC, test_id ASC LIMIT 10 OFFSET 0",
                "WITH expanded AS (SELECT t.test_id, t.test_name, t.configuration.threads AS threads, UNNEST(t.override_executions) AS ov FROM df_tests t), "
                "agg AS (SELECT test_id, test_name, GREATEST(COALESCE(MAX(ov.concurrency), 0), COALESCE(MAX(threads), 0)) AS max_concurrency FROM expanded GROUP BY test_id, test_name) "
                "SELECT test_id, test_name, max_concurrency FROM agg ORDER BY max_concurrency DESC, test_id ASC LIMIT 10 OFFSET 0",
            ],
            "bad": [
                "SELECT * FROM df_tests",
                "SELECT * FROM df_tests WHERE status = 'ERROR'",
                "SELECT test_id, MAX(UNNEST(override_executions).concurrency) FROM df_tests GROUP BY test_id",
                "SELECT * FROM df_a JOIN df_b ON test_id = test_id ORDER BY test_id LIMIT 100 OFFSET 0",
                "SELECT * FROM df_a UNION ALL SELECT * FROM df_b ORDER BY test_id LIMIT 100 OFFSET 0",
                "SELECT TO_JSON(configuration) FROM df_tests ORDER BY test_id LIMIT 10 OFFSET 0",
            ],
        },
        "troubleshooting_hints": [
            "If you get ambiguous column errors, alias every table/CTE and qualify join keys.",
            "If nested field access fails, move expansion into a dedicated CTE using UNNEST.",
            "If a query is too complex, split it into 2-4 CTE stages and validate each stage independently.",
            "If an inferred function fails, verify against supported_functions and unsupported_functions.",
            "If aggregation results over nested lists do not reflect expected values, check that you are using UNNEST and aggregation (MAX, MIN, etc.) correctly, and that you compare against the scalar field with GREATEST/LEAST.",
        ],
        "notes": [
            "All in-memory dataframe tables are queryable in the same SQL context.",
            "Function name typo seen in some sources: STRPOST; use STRPOS.",
            "This help defines practical usage constraints for BlazeMeter MCP SQL queries.",
        ],
        "references": [
            "https://docs.pola.rs/py-polars/html/reference/sql/index.html",
            "https://docs.pola.rs/py-polars/html/reference/sql/functions/index.html",
            "https://docs.pola.rs/py-polars/html/reference/sql/clauses.html",
            "https://docs.pola.rs/py-polars/html/reference/sql/table_operations.html",
            "https://docs.pola.rs/py-polars/html/reference/sql/set_operations.html"
        ],
    }
