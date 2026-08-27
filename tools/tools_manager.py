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
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX
from config.runtime import AppRuntime
from config.storage import SessionScope, SessionScopeResolverPort, SessionStoragePort
from models.manager import Manager
from models.result import BaseResult
from tools.dataframe_manager import (
    INVALID_RESULT_FORMAT_ERROR,
    clear_dataframes,
    get_dataframe_metadata,
    get_sql_capabilities,
    group_dataframe_schemas,
    list_dataframes_metadata,
    normalize_result_format,
    query_dataframes,
    register_dataframe,
    remove_dataframes,
    serialize_result_to_compact_json,
    stored_as_dataframe_payload,
)
from tools.runtime_tools import run_tool_with_runtime
from tools.utils import format_sanitized_traceback


class ToolsManager(Manager):
    """Session-scoped dataframe tools backed by SessionStoragePort."""

    def __init__(
            self,
            ctx: Context,
            session_storage: SessionStoragePort,
            scope_resolver: SessionScopeResolverPort,
    ):
        super().__init__(ctx)
        self.session_storage = session_storage
        self.scope_resolver = scope_resolver

    def _scope(self) -> SessionScope:
        return self.scope_resolver.resolve(self.ctx, self.token)

    async def dataframes_list(self) -> BaseResult:
        scope = self._scope()
        metadata = await list_dataframes_metadata(
            session_storage=self.session_storage,
            scope=scope,
            include_schema=False,
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
        scope = self._scope()
        metadata = await get_dataframe_metadata(
            dataframe_id,
            session_storage=self.session_storage,
            scope=scope,
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
        scope = self._scope()
        grouped = await group_dataframe_schemas(
            session_storage=self.session_storage,
            scope=scope,
            dataframe_id_list=dataframe_id_list,
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
        scope = self._scope()
        normalized_result_format = normalize_result_format(result_format)
        if normalized_result_format == "invalid":
            return BaseResult(error=INVALID_RESULT_FORMAT_ERROR)
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
            session_storage=self.session_storage,
            scope=scope,
            output_format=effective_output_format,
        )
        if query_response.get("error"):
            return BaseResult(error=query_response["error"])

        if normalized_result_format == "dataframe":
            rows = query_response["result"] or []
            try:
                json_size_chars = len(serialize_result_to_compact_json(rows))
            except Exception as exc:
                return BaseResult(error=f"Could not serialize query result: {exc}")
            metadata = await register_dataframe(
                result=rows,
                origin_manager="blazemeter_tools",
                origin_action="dataframes_query",
                json_size_chars=json_size_chars,
                session_storage=self.session_storage,
                scope=scope,
            )
            return BaseResult(
                result=[stored_as_dataframe_payload(metadata)],
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
        empty_list_error = (
            "Missing required args for action 'dataframes_remove': "
            "dataframe_id_list must be a non-empty list of dataframe IDs."
        )
        if not dataframe_id_list or not isinstance(dataframe_id_list, list):
            return BaseResult(error=empty_list_error)
        ids = [str(df_id).strip() for df_id in dataframe_id_list if str(df_id).strip()]
        if not ids:
            return BaseResult(error=empty_list_error)

        unique_ids = list(dict.fromkeys(ids))
        outcome = await remove_dataframes(unique_ids, self.session_storage, self._scope())
        removed_ids = set(outcome["removed"])
        missing_ids = outcome["missing"]
        removed_count = len(outcome["removed"])
        removed_results = [
            {"dataframe_id": df_id, "removed": df_id in removed_ids}
            for df_id in unique_ids
        ]

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
        removed_count = await clear_dataframes(
            session_storage=self.session_storage,
            scope=self._scope(),
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
        runtime.configure_context(ctx)
        manager = ToolsManager(ctx, runtime.storage, runtime.scope_resolver)
        token = manager.token
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
            return await run_tool_with_runtime(
                runtime, f"{TOOLS_PREFIX}_tools", action, ctx, _dispatch,
                token=token,
                tool_args=args,
                dataframe_excluded_actions={
                    "dataframes_clear",
                    "dataframes_get",
                    "dataframes_list",
                    "dataframes_query",
                    "dataframes_remove",
                    "dataframes_schema_groups",
                    "dataframes_sql_help",
                },
            )
        except httpx.HTTPStatusError:
            return BaseResult(error=f"Error: {format_sanitized_traceback()}")
        except Exception:
            return BaseResult(error=f"Error: {format_sanitized_traceback()}")
