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
from typing import Any, Dict, Optional, Tuple

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX
from config.runtime import AppRuntime
from config.token import BzmToken
from models.manager import Manager
from models.result import BaseResult
from telemetry import run_tool
from tools.dataframe_manager import (
    clear_dataframes,
    get_dataframe_metadata,
    get_sql_capabilities,
    group_dataframe_schemas,
    list_dataframes_metadata,
    query_dataframes,
    register_dataframe,
    remove_dataframe,
    resolve_partition_ids,
    serialize_result_to_compact_json,
)
from tools.utils import format_sanitized_traceback


def resolve_session_partition(
        token: Optional[BzmToken],
        ctx: Optional[Context],
) -> Tuple[str, str]:
    """Map the current MCP invocation to a Storage partition key."""
    return resolve_partition_ids(token, ctx)


class ToolsManager(Manager):
    """Session-scoped dataframe tools backed by SessionStoragePort."""

    def _session(self) -> Tuple[str, str]:
        return resolve_session_partition(self.token, self.ctx)

    async def dataframes_list(self) -> BaseResult:
        user_id, mcp_session_id = self._session()
        metadata = await list_dataframes_metadata(
            include_schema=False,
            user_id=user_id,
            mcp_session_id=mcp_session_id,
        )
        return BaseResult(
            result=metadata,
            total=len(metadata),
            has_more=False,
            info=[
                "Schema is omitted in dataframes_list to reduce payload size.",
                "Use dataframes_schema_groups to compare shared/different schemas across dataframes.",
                "Use dataframes_get for full metadata and schema of a specific dataframe.",
            ],
        )

    async def dataframes_get(self, dataframe_id: str) -> BaseResult:
        user_id, mcp_session_id = self._session()
        metadata = await get_dataframe_metadata(
            dataframe_id,
            user_id=user_id,
            mcp_session_id=mcp_session_id,
        )
        if not metadata:
            return BaseResult(
                error=(
                    f"Dataframe ID {dataframe_id} was not found. "
                    "Use dataframes_list to discover available dataframes."
                )
            )
        return BaseResult(result=[metadata])

    async def dataframes_schema_groups(
            self,
            dataframe_id_list: Optional[list[str]] = None,
    ) -> BaseResult:
        user_id, mcp_session_id = self._session()
        grouped = await group_dataframe_schemas(
            dataframe_id_list,
            user_id=user_id,
            mcp_session_id=mcp_session_id,
        )
        mandatory_review_groups = [
            grp for grp in grouped.get("groups", [])
            if isinstance(grp, dict) and str(grp.get("varying_columns", "")).strip()
        ]
        info_messages = [
            "Grouped dataframe schemas by top-level contract and per-column schema variations.",
            "Dataframe ID lists are deduplicated in 'df_sets'; groups and variations reference them via 'df_ref'.",
            "If dataframe_id_list is omitted, all current dataframes are included.",
        ]
        if mandatory_review_groups:
            info_messages.append(
                "CRITICAL: Column variations were detected. Perform mandatory detailed schema "
                "review for varying columns before the final query."
            )
        info_messages.append(
            "IMPORTANT: Before planning and executing the final dataframe query, "
            "call dataframes_sql_help synchronously in a separate call."
        )
        return BaseResult(result=[grouped], info=info_messages)

    async def dataframes_query(
            self,
            sql: str,
            output_format: str = "matrix",
            result_format: str = "auto",
    ) -> BaseResult:
        user_id, mcp_session_id = self._session()
        normalized_result_format = str(result_format or "auto").strip().lower()
        if normalized_result_format not in {"auto", "dataframe", "raw"}:
            return BaseResult(
                error="Invalid result_format value. Allowed values: auto, dataframe, raw."
            )
        # Store path always queries as records so register_dataframe can rebuild rows.
        effective_output_format = (
            "records" if normalized_result_format == "dataframe" else output_format
        )
        info_messages = [
            "Query executed successfully against the session SQL context.",
            "ORDER BY + LIMIT + OFFSET are mandatory in every dataframe query.",
            "Use a prudent default page size of up to 100 rows (for example, LIMIT 100 OFFSET 0), "
            "then continue paging as needed.",
        ]
        query_response = await query_dataframes(
            sql,
            output_format=effective_output_format,
            user_id=user_id,
            mcp_session_id=mcp_session_id,
        )
        if query_response.get("error"):
            return BaseResult(error=query_response["error"])

        if normalized_result_format == "dataframe":
            rows = query_response["result"] or []
            try:
                json_size_chars = len(serialize_result_to_compact_json(rows))
            except Exception:
                json_size_chars = 0
            metadata = await register_dataframe(
                result=rows,
                origin_manager="blazemeter_tools",
                origin_action="dataframes_query",
                json_size_chars=json_size_chars,
                user_id=user_id,
                mcp_session_id=mcp_session_id,
            )
            return BaseResult(
                result=[{
                    "stored_as_dataframe": True,
                    "dataframe_id": metadata["dataframe_id"],
                    "table_name": metadata["table_name"],
                    "rows": metadata["rows"],
                    "columns": metadata["columns"],
                    "schema_hash": metadata["schema_hash"],
                    "json_size_chars": metadata["json_size_chars"],
                }],
                info=info_messages + [
                    "result_format=dataframe stored the query output as a new session dataframe."
                ],
            )

        return BaseResult(
            result=query_response["result"],
            total=query_response["rows"],
            has_more=False,
            info=info_messages,
        )

    async def dataframes_remove(self, dataframe_id_list: list[str]) -> BaseResult:
        if not dataframe_id_list or not isinstance(dataframe_id_list, list):
            return BaseResult(
                error=(
                    "Missing required args for action 'dataframes_remove': "
                    "dataframe_id_list must be a non-empty list of dataframe IDs."
                )
            )
        ids = [str(df_id).strip() for df_id in dataframe_id_list if str(df_id).strip()]
        if not ids:
            return BaseResult(
                error=(
                    "Missing required args for action 'dataframes_remove': "
                    "dataframe_id_list must be a non-empty list of dataframe IDs."
                )
            )

        user_id, mcp_session_id = self._session()
        unique_ids = list(dict.fromkeys(ids))
        removed_count = 0
        removed_results = []
        missing_ids = []
        for df_id in unique_ids:
            removed = await remove_dataframe(
                df_id,
                user_id=user_id,
                mcp_session_id=mcp_session_id,
            )
            removed_results.append({"dataframe_id": df_id, "removed": removed})
            if removed:
                removed_count += 1
            else:
                missing_ids.append(df_id)

        if len(unique_ids) == 1 and removed_count == 0:
            only_id = unique_ids[0]
            return BaseResult(
                error=(
                    f"Dataframe ID {only_id} was not found. "
                    "Use dataframes_list to discover available dataframes."
                )
            )

        info_messages = [
            f"Requested removal for {len(unique_ids)} dataframe(s). "
            f"Removed: {removed_count}. Missing: {len(missing_ids)}."
        ]
        if removed_count > 0:
            info_messages.append("Removed dataframes were unregistered from SQL context.")
        if missing_ids:
            info_messages.append(
                "Some dataframe IDs were not found: " + ", ".join(missing_ids) + "."
            )
        return BaseResult(
            result=removed_results,
            total=len(removed_results),
            has_more=False,
            info=info_messages,
        )

    async def dataframes_clear(self) -> BaseResult:
        user_id, mcp_session_id = self._session()
        removed_count = await clear_dataframes(
            user_id=user_id,
            mcp_session_id=mcp_session_id,
        )
        return BaseResult(
            result=[{"removed_count": removed_count, "remaining": 0}],
            info=[
                "All session dataframes were removed and unregistered from SQL context."
            ],
        )

    async def dataframes_sql_help(self) -> BaseResult:
        return BaseResult(
            result=[get_sql_capabilities()],
            info=["Only read-only SQL is allowed in dataframe queries."],
        )


def register(mcp, runtime: AppRuntime):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_tools",
        description="""
Operations for session dataframe management (Storage-backed).
Actions:
- dataframes_list: List dataframes and metadata for the current MCP session.
- dataframes_get: Get dataframe metadata and schema by dataframe ID.
    args(dict): dataframe_id (str, required)
- dataframes_schema_groups: Group dataframe schemas for multi-dataframe queries.
    args(dict): dataframe_id_list (list[str], optional)
- dataframes_query: Execute read-only SQL against session dataframe tables.
    args(dict): sql (str, required); output_format (matrix|columnar|records);
                result_format (auto|dataframe|raw, optional)
    requirement: ORDER BY + LIMIT + OFFSET are mandatory in every query.
- dataframes_remove: Remove one or more dataframes from the session store.
    args(dict): dataframe_id_list (list[str], required)
- dataframes_clear: Remove all dataframes for the current session.
- dataframes_sql_help: Describe supported SQL usage and blocked operations.
Hints:
- **CRITICAL**: Always follow the action schema exactly.
- **CRITICAL**: Before writing any dataframe SQL query, call `dataframes_sql_help` first.
- ORDER BY + LIMIT + OFFSET are mandatory in every dataframe query.
"""
    )
    async def tools(
            action: str = Field(description="The action id to execute"),
            args: Dict[str, Any] = Field(description="Dictionary with parameters"),
            ctx: Context = Field(description="Context object providing access to MCP capabilities"),
    ) -> BaseResult:
        token = runtime.auth.get_token(ctx)
        manager = ToolsManager(token, ctx)
        args = args or {}

        async def _dispatch():
            match action:
                case "dataframes_list":
                    return await manager.dataframes_list()
                case "dataframes_get":
                    dataframe_id = str(args.get("dataframe_id", "")).strip()
                    if not dataframe_id:
                        return BaseResult(
                            error="Missing required args for action 'dataframes_get': dataframe_id"
                        )
                    return await manager.dataframes_get(dataframe_id)
                case "dataframes_schema_groups":
                    return await manager.dataframes_schema_groups(args.get("dataframe_id_list"))
                case "dataframes_query":
                    sql = str(args.get("sql", "")).strip()
                    if not sql:
                        return BaseResult(
                            error="Missing required args for action 'dataframes_query': sql"
                        )
                    return await manager.dataframes_query(
                        sql=sql,
                        output_format=str(args.get("output_format", "matrix")),
                        result_format=str(args.get("result_format", "auto")),
                    )
                case "dataframes_remove":
                    return await manager.dataframes_remove(args.get("dataframe_id_list"))
                case "dataframes_clear":
                    return await manager.dataframes_clear()
                case "dataframes_sql_help":
                    return await manager.dataframes_sql_help()
                case _:
                    return BaseResult(error=f"Action {action} not found in tools manager tool")

        try:
            return await run_tool(f"{TOOLS_PREFIX}_tools", action, ctx, _dispatch,
                token=token,
                tool_args=args,
                dataframe_excluded_actions={"dataframes_clear", "dataframes_get", "dataframes_list", "dataframes_query", "dataframes_remove", "dataframes_schema_groups", "dataframes_sql_help"}
            )
        except httpx.HTTPStatusError:
            return BaseResult(error=f"Error: {format_sanitized_traceback()}")
        except Exception:
            return BaseResult(error=f"Error: {format_sanitized_traceback()}")
