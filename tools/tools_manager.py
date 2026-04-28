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
import traceback
import asyncio
import time
import re
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import Context

from config.blazemeter import TOOLS_PREFIX, SUPPORT_MESSAGE
from config.token import BzmToken
from models.manager import Manager
from models.result import BaseResult
from tools.async_task_manager import (
    cancel_task,
    get_task_record,
    is_active_status,
    is_terminal_status,
    list_tasks,
    remove_task,
    task_snapshot,
)
from tools.utils import (
    normalize_action_args,
    tool_result,
    validate_non_empty_str_arg,
    validate_required_args,
)
from tools.dataframe_manager import (
    clear_dataframes,
    get_dataframe_metadata,
    get_sql_capabilities,
    group_dataframe_schemas,
    list_dataframes_metadata,
    query_dataframes,
    remove_dataframe,
)


class ToolsManager(Manager):
    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    @staticmethod
    def _should_continue_polling(status: str) -> bool:
        return status in {"parking", "working", "input_required"}

    @staticmethod
    def _to_snake_case(value: str) -> str:
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @classmethod
    def _operation_name(cls, action_payload: Dict[str, Any]) -> str:
        manager = str(action_payload.get("manager", "tool"))
        method = str(action_payload.get("method", "action"))
        tool_name = manager[:-7] if manager.endswith("Manager") else manager
        tool_name = cls._to_snake_case(tool_name)
        return f"{tool_name}.{method}"

    @staticmethod
    def _format_operation_value(value: Any) -> str:
        if isinstance(value, str):
            return repr(value)
        return repr(value)

    @classmethod
    def _operation_call_line(cls, action_payload: Dict[str, Any]) -> str:
        # Kept for backwards compatibility with tests/helpers that may still use this.
        return cls._operation_name(action_payload)

    @staticmethod
    def _batch_summary_line() -> str:
        records = list_tasks()
        counts = {
            "completed": 0,
            "working": 0,
            "parking": 0,
            "failed": 0,
            "cancelled": 0,
            "input_required": 0,
        }
        for record in records:
            status = str(record.status).lower()
            if status in counts:
                counts[status] += 1
        summary = (
            f"batch summary: total={len(records)} completed={counts['completed']} "
            f"working={counts['working']} parking={counts['parking']} failed={counts['failed']}"
        )
        if counts["cancelled"] > 0:
            summary += f" cancelled={counts['cancelled']}"
        if counts["input_required"] > 0:
            summary += f" input_required={counts['input_required']}"
        return summary

    @classmethod
    def _task_status_line(
            cls,
            task_record,
            poll_count: Optional[int],
            elapsed_seconds: int,
            next_poll_seconds: Optional[float],
            window_seconds: Optional[float] = None,
            include_polling_prefix: bool = True,
    ) -> str:
        operation = cls._operation_name(task_record.action)
        prefix = "Polling " if include_polling_prefix else ""
        line = f"{prefix}{task_record.task_id}[{operation}] ({task_record.status})"
        if poll_count is not None:
            line += f" attempt={poll_count}"
        line += f" elapsed={elapsed_seconds}s"
        if window_seconds is not None:
            line += f"/{int(window_seconds)}s"
        if next_poll_seconds is not None and cls._should_continue_polling(task_record.status):
            line += f" next={int(next_poll_seconds)}s"
        if task_record.status == "parking" and task_record.status_message:
            line += f" note={repr(task_record.status_message)}"
        return line

    @classmethod
    def _polling_message(
            cls,
            task_record,
            poll_count: int,
            elapsed_seconds: int,
            next_poll_seconds: float,
            window_seconds: float,
    ) -> str:
        line = cls._task_status_line(
            task_record=task_record,
            poll_count=poll_count,
            elapsed_seconds=elapsed_seconds,
            next_poll_seconds=next_poll_seconds,
            window_seconds=window_seconds,
            include_polling_prefix=True,
        )
        return f"{line} | {cls._batch_summary_line()}"

    @classmethod
    def _polling_finished_message(cls, task_record, elapsed_seconds: int) -> str:
        line = cls._task_status_line(
            task_record=task_record,
            poll_count=None,
            elapsed_seconds=elapsed_seconds,
            next_poll_seconds=None,
            window_seconds=None,
            include_polling_prefix=True,
        )
        return f"{line} | {cls._batch_summary_line()}"

    async def tasks_get(
            self,
            task_id: str,
            remove_on_terminal: bool = True,
            wait_for_terminal_ms: int = 0,
            poll_interval_ms: int = 1000
    ) -> BaseResult:
        if wait_for_terminal_ms < 0:
            return BaseResult(error="wait_for_terminal_ms must be greater than or equal to 0.")
        if poll_interval_ms <= 0:
            return BaseResult(error="poll_interval_ms must be greater than 0.")

        task_record = get_task_record(task_id)
        if not task_record:
            return BaseResult(error=f"Task ID {task_id} was not found.")

        polling_exhausted = False
        if wait_for_terminal_ms > 0 and not is_terminal_status(task_record.status):
            start_time = time.monotonic()
            wait_seconds = wait_for_terminal_ms / 1000.0
            poll_seconds = poll_interval_ms / 1000.0
            attempt = 0

            while True:
                task_record = get_task_record(task_id)
                if not task_record:
                    return BaseResult(error=f"Task ID {task_id} was not found.")
                if is_terminal_status(task_record.status):
                    break

                elapsed = time.monotonic() - start_time
                if elapsed >= wait_seconds:
                    polling_exhausted = True
                    break

                attempt += 1
                progress = min(100.0, (elapsed / wait_seconds) * 100.0) if wait_seconds > 0 else 100.0
                try:
                    await self.ctx.report_progress(
                        progress=progress,
                        total=100.0,
                        message=self._polling_message(
                            task_record=task_record,
                            poll_count=attempt,
                            elapsed_seconds=int(elapsed),
                            next_poll_seconds=poll_seconds,
                            window_seconds=wait_seconds,
                        )
                    )
                except Exception:
                    pass

                remaining = wait_seconds - elapsed
                await asyncio.sleep(min(poll_seconds, remaining))

            try:
                final_elapsed = min(wait_seconds, time.monotonic() - start_time)
                await self.ctx.report_progress(
                    progress=100.0,
                    total=100.0,
                    message=self._polling_finished_message(
                        task_record=task_record,
                        elapsed_seconds=int(final_elapsed),
                    )
                )
            except Exception:
                pass

        terminal = is_terminal_status(task_record.status)
        snapshot = task_snapshot(task_record, include_result=terminal)
        snapshot["should_continue_polling"] = self._should_continue_polling(task_record.status)
        snapshot["next_poll_after_ms"] = poll_interval_ms if snapshot["should_continue_polling"] else 0

        if terminal and remove_on_terminal:
            remove_task(task_id)
            return BaseResult(
                result=[snapshot],
                info=[
                    "Task result retrieved successfully and removed automatically from the task registry. "
                    "It will not be available in subsequent queries."
                ]
            )

        if terminal:
            return BaseResult(
                result=[snapshot],
                info=[
                    "Task result retrieved successfully and kept in the task registry. "
                    "Use tasks_remove to delete it when no longer needed."
                ]
            )

        return BaseResult(
            result=[snapshot],
            info=[
                (
                    "Task is still in progress after the polling window. Query tasks_status again in a few moments."
                    if polling_exhausted
                    else "Task is still in progress. Query tasks_status again in a few moments to check updated state."
                )
            ]
        )

    async def tasks_status(
            self,
            task_id: str,
            wait_for_terminal_ms: int = 0,
            poll_interval_ms: int = 1000
    ) -> BaseResult:
        if wait_for_terminal_ms < 0:
            return BaseResult(error="wait_for_terminal_ms must be greater than or equal to 0.")
        if poll_interval_ms <= 0:
            return BaseResult(error="poll_interval_ms must be greater than 0.")

        task_record = get_task_record(task_id)
        if not task_record:
            return BaseResult(error=f"Task ID {task_id} was not found.")

        polling_exhausted = False
        if wait_for_terminal_ms > 0 and not is_terminal_status(task_record.status):
            start_time = time.monotonic()
            wait_seconds = wait_for_terminal_ms / 1000.0
            poll_seconds = poll_interval_ms / 1000.0
            attempt = 0

            while True:
                task_record = get_task_record(task_id)
                if not task_record:
                    return BaseResult(error=f"Task ID {task_id} was not found.")
                if is_terminal_status(task_record.status):
                    break

                elapsed = time.monotonic() - start_time
                if elapsed >= wait_seconds:
                    polling_exhausted = True
                    break

                attempt += 1
                progress = min(100.0, (elapsed / wait_seconds) * 100.0) if wait_seconds > 0 else 100.0
                try:
                    await self.ctx.report_progress(
                        progress=progress,
                        total=100.0,
                        message=self._polling_message(
                            task_record=task_record,
                            poll_count=attempt,
                            elapsed_seconds=int(elapsed),
                            next_poll_seconds=poll_seconds,
                            window_seconds=wait_seconds,
                        )
                    )
                except Exception:
                    pass

                remaining = wait_seconds - elapsed
                await asyncio.sleep(min(poll_seconds, remaining))

            try:
                final_elapsed = min(wait_seconds, time.monotonic() - start_time)
                await self.ctx.report_progress(
                    progress=100.0,
                    total=100.0,
                    message=self._polling_finished_message(
                        task_record=task_record,
                        elapsed_seconds=int(final_elapsed),
                    )
                )
            except Exception:
                pass

        snapshot = task_snapshot(task_record, include_result=False)
        snapshot["should_continue_polling"] = self._should_continue_polling(task_record.status)
        snapshot["next_poll_after_ms"] = poll_interval_ms if snapshot["should_continue_polling"] else 0
        info_message = (
            "Task is terminal. Use tasks_get to retrieve task_result when needed."
            if is_terminal_status(task_record.status)
            else (
                "Task is still in progress after the polling window. Query tasks_status again in a few moments."
                if polling_exhausted
                else "Task is still in progress. Query tasks_status again in a few moments to check updated state."
            )
        )
        return BaseResult(result=[snapshot], info=[info_message])

    async def tasks_list(self, status: Optional[str] = None, status_list: Optional[list[str]] = None) -> BaseResult:
        filters = status_list if status_list else ([status] if status else None)
        records = list_tasks(filters)
        snapshots = []
        for record in records:
            base_snapshot = task_snapshot(record, include_result=False)
            snapshots.append(
                {
                    "task_id": record.task_id,
                    "operation": self._operation_name(record.action),
                    "status": record.status,
                    "status_message": record.status_message,
                    "created_at": record.created_at,
                    "created_at_iso": base_snapshot["created_at_iso"],
                    "last_updated_at": record.last_updated_at,
                    "last_updated_at_iso": base_snapshot["last_updated_at_iso"],
                    "started_running_at": record.started_running_at,
                    "started_running_at_iso": base_snapshot["started_running_at_iso"],
                    "finished_at": record.finished_at,
                    "finished_at_iso": base_snapshot["finished_at_iso"],
                    "time_to_live_ms": record.time_to_live_ms,
                }
            )
        return BaseResult(result=snapshots, total=len(snapshots), has_more=False)

    async def tasks_cancel(self, task_id: str) -> BaseResult:
        task_record = cancel_task(task_id)
        if not task_record:
            return BaseResult(error=f"Task ID {task_id} was not found.")
        return BaseResult(
            result=[task_snapshot(task_record, include_result=True)],
            info=["Task cancellation was requested successfully."]
        )

    async def tasks_remove(self, task_id: str) -> BaseResult:
        task_record = get_task_record(task_id)
        if not task_record:
            return BaseResult(error=f"Task ID {task_id} was not found.")

        cancel_requested = False
        if is_active_status(task_record.status):
            cancel_requested = True
            cancel_task(task_id)
            if task_record.asyncio_task:
                try:
                    await asyncio.wait_for(asyncio.shield(task_record.asyncio_task), timeout=0.2)
                except asyncio.TimeoutError:
                    pass
                except asyncio.CancelledError:
                    pass

        snapshot = task_snapshot(task_record, include_result=is_terminal_status(task_record.status))
        removed = remove_task(task_id)
        if not removed:
            return BaseResult(error=f"Task ID {task_id} could not be removed.")

        info_message = (
            "Task was active. Cancellation was requested before removal."
            if cancel_requested
            else "Task was removed from task registry."
        )
        return BaseResult(
            result=[{
                "task_id": task_id,
                "removed": True,
                "cancel_requested": cancel_requested,
                "task_snapshot": snapshot
            }],
            info=[info_message]
        )

    async def dataframes_list(self) -> BaseResult:
        metadata = await list_dataframes_metadata(include_schema=False)
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
        metadata = await get_dataframe_metadata(dataframe_id)
        if not metadata:
            return BaseResult(
                error=f"Dataframe ID {dataframe_id} was not found. Use dataframes_list to discover available dataframes."
            )
        return BaseResult(result=[metadata])

    async def dataframes_schema_groups(self, dataframe_id_list: Optional[list[str]] = None) -> BaseResult:
        grouped = await group_dataframe_schemas(dataframe_id_list)
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
                "CRITICAL: Column variations were detected. Perform mandatory detailed schema review for varying columns before the final query."
            )
            info_messages.append(
                "CRITICAL: Do not try-fast. Reason step-by-step: schema check → pattern selection → design → execute."
            )
        info_messages.append(
            "IMPORTANT: Before planning and executing the final dataframe query, call dataframes_sql_help synchronously in a separate call."
        )
        return BaseResult(
            result=[grouped],
            info=info_messages,
        )

    async def dataframes_query(
        self,
        sql: str,
        output_format: str = "matrix",
        result_format: str = "auto",
    ) -> BaseResult:
        normalized_result_format = str(result_format or "auto").strip().lower()
        effective_output_format = output_format
        info_messages = [
            "Query executed successfully against the in-memory SQL context.",
            "ORDER BY + LIMIT + OFFSET are mandatory in every dataframe query.",
            "Use a prudent default page size of up to 100 rows (for example, LIMIT 100 OFFSET 0), then continue paging as needed.",
            "ORDER BY + LIMIT + OFFSET provides deterministic pagination.",
        ]
        if normalized_result_format == "dataframe":
            # For dataframe materialization, we must preserve raw row records.
            effective_output_format = "records"
            info_messages.append(
                "When result_format=dataframe, dataframes_query uses records internally for dataframe storage and ignores output_format only for storage."
            )
        query_response = query_dataframes(sql, output_format=effective_output_format)
        if query_response.get("error"):
            return BaseResult(
                error=query_response["error"]
            )
        return BaseResult(
            result=query_response["result"],
            total=query_response["rows"],
            has_more=False,
            info=info_messages
        )

    async def dataframes_remove(self, dataframe_id_list: list[str]) -> BaseResult:
        if not dataframe_id_list or not isinstance(dataframe_id_list, list):
            return BaseResult(
                error="Missing required args for action 'dataframes_remove': dataframe_id_list must be a non-empty list of dataframe IDs."
            )
        ids = [str(df_id).strip() for df_id in dataframe_id_list if str(df_id).strip()]
        if not ids:
            return BaseResult(
                error="Missing required args for action 'dataframes_remove': dataframe_id_list must be a non-empty list of dataframe IDs."
            )

        # Preserve order while deduplicating IDs.
        unique_ids = list(dict.fromkeys(ids))
        removed_count = 0
        removed_results = []
        missing_ids = []
        for df_id in unique_ids:
            removed = await remove_dataframe(df_id)
            removed_results.append({
                "dataframe_id": df_id,
                "removed": removed,
            })
            if removed:
                removed_count += 1
            else:
                missing_ids.append(df_id)

        if len(unique_ids) == 1 and removed_count == 0:
            only_id = unique_ids[0]
            return BaseResult(
                error=f"Dataframe ID {only_id} was not found. Use dataframes_list to discover available dataframes."
            )

        info_messages = [
            f"Requested removal for {len(unique_ids)} dataframe(s). Removed: {removed_count}. Missing: {len(missing_ids)}."
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
            info=info_messages
        )

    async def dataframes_clear(self) -> BaseResult:
        removed_count = await clear_dataframes()
        return BaseResult(
            result=[{
                "removed_count": removed_count,
                "remaining": 0
            }],
            info=[
                "All in-memory dataframes were removed and unregistered from SQL context."
            ]
        )

    async def dataframes_sql_help(self) -> BaseResult:
        return BaseResult(
            result=[get_sql_capabilities()],
            info=[
                "Only read-only SQL is allowed in dataframe queries."
            ]
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_tools",
        description="""
Operations for asynchronous task lifecycle management.
Actions:
- tasks_get: Get task metadata by task ID and return task_result when task is terminal.
    args(dict): Dictionary with required/optional parameters:
        task_id (str, required, non-empty): The task id to query.
        remove_on_terminal (bool, default=True): Removes task automatically if status is terminal.
        wait_for_terminal_ms (int, default=0): Internal polling window in milliseconds.
        poll_interval_ms (int, default=1000): Delay between polling attempts in milliseconds.
- tasks_status: Get lightweight task status by task ID (without task_result payload).
    args(dict): Dictionary with required/optional parameters:
        task_id (str, required, non-empty): The task id to query.
        wait_for_terminal_ms (int, default=0): Internal polling window in milliseconds.
        poll_interval_ms (int, default=1000): Delay between polling attempts in milliseconds.
- tasks_list: List tasks currently stored in the task registry.
    args(dict): Dictionary with optional parameters:
        status (str): Optional single status filter.
        status_list (list[str]): Optional list of statuses to filter.
- tasks_cancel: Cancel a running/queued task.
    args(dict): Dictionary with required parameters:
        task_id (str, required, non-empty): The task id to cancel.
- tasks_remove: Remove a task from registry.
    args(dict): Dictionary with required parameters:
        task_id (str, required, non-empty): The task id to remove.
- dataframes_list: List all in-memory dataframes and their metadata.
- dataframes_get: Get dataframe metadata and schema by dataframe ID. Use this for detailed inspection of a specific dataframe after schema groups indicates differences or ambiguity.
    args(dict): Dictionary with required parameters:
        dataframe_id (str, required, non-empty): The dataframe id to query.
- dataframes_schema_groups: Group dataframe schemas hierarchically by top-level contract and per-column schema variants. This is the default first step for schema validation when a query involves 2 or more dataframes.
    args(dict): Dictionary with optional parameters:
        dataframe_id_list (list[str], optional): Specific dataframe IDs to analyze. If omitted, all dataframes are included.
- dataframes_query: Execute read-only SQL against all in-memory dataframe tables.
    args(dict): Dictionary with required parameters:
        sql (str, required, non-empty): SQL query string. Supports SELECT and WITH queries.
        output_format (str, default="matrix", valid=["matrix", "columnar", "records"]): Query result shape.
        result_format (str, optional): If set to "dataframe", query data is stored internally from records format; output_format is ignored only for storage.
    precondition: Before planning any dataframe SQL query, call dataframes_sql_help first.
    requirement: ORDER BY + LIMIT + OFFSET are mandatory in every query.
    recommendation: Use a prudent default page size of up to 100 rows (for example, LIMIT 100 OFFSET 0), then continue paging as needed.
- dataframes_remove: Remove one or more dataframes from memory and SQL context.
    args(dict): Dictionary with required parameters:
        dataframe_id_list (list[str], required): List of dataframe IDs to remove. Must be non-empty.
- dataframes_clear: Remove all dataframes from memory and SQL context.
- dataframes_sql_help: Describe supported SQL usage and blocked operations.
Hints:
- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.
- **CRITICAL**: Before writing any dataframe SQL query, call `dataframes_sql_help` first.
- **CRITICAL**: If the query involves 2 or more dataframes, call `dataframes_schema_groups` before any broad `dataframes_get` usage.
- **CRITICAL**: Use `dataframes_get` selectively for outliers or ambiguous fields detected by schema groups; do not scan all dataframes by default.
- **CRITICAL**: If the query touches nested/list fields, use the robust UNNEST -> aggregate -> join-back pattern in CTEs. No exception for single dataframe. Do not try direct nested access first.
- **CRITICAL**: Before SQL that touches nested/list: explicitly confirm "there are nested/list fields; I use the robust pattern."
- **CRITICAL**: For dataframe SQL: reason step-by-step before executing. Design your approach (schema check, nested check, pattern choice), verify against rules, then execute. Do not try-fast.
- Use dataframes_schema_groups to compare schema similarities/differences across multiple dataframes without repeating schema payload.
- Single dataframe (scalar-only): dataframes_sql_help -> dataframes_get -> dataframes_query.
- Single dataframe (nested/list): dataframes_sql_help -> dataframes_get -> staged CTE (UNNEST -> aggregate -> join-back) -> dataframes_query. Same robust pattern as multi-dataframe.
- Multi-dataframe query flow: dataframes_sql_help -> dataframes_schema_groups -> targeted dataframes_get -> dataframes_query.
- Multi-dataframe nested flow: dataframes_sql_help -> dataframes_schema_groups -> targeted dataframes_get -> staged CTE (UNNEST -> aggregate -> join-back) -> final query.
- Large tool results may be automatically materialized as in-memory dataframes and returned as references.
- Optional result formatting in args: `result_format` = `auto` (default), `dataframe` (force dataframe), `raw` (disable dataframe materialization).
- If you plan joins, filtering, sorting, grouping, or multi-step analysis, prefer `result_format=dataframe` and use `dataframes_query` instead of merging large inline results in AI context.
- ORDER BY + LIMIT + OFFSET are mandatory in every dataframe query.
- Use a prudent default page size of up to 100 rows (for example, LIMIT 100 OFFSET 0), then continue paging as needed.
- Use ORDER BY + LIMIT + OFFSET for deterministic pagination when reading dataframes.
- All registered dataframe tables are available in the same SQL context, including JOIN and UNION scenarios.
- When a dataframe is no longer needed, release memory using dataframes_remove or dataframes_clear.
- When a task is no longer needed (especially terminal tasks), release it from registry using tasks_remove.
"""
    )
    @tool_result(excluded_actions={
        "tasks_list",
        "tasks_status",
        "dataframes_list",
        "dataframes_get",
        "dataframes_schema_groups",
        "dataframes_query",
        "dataframes_remove",
        "dataframes_clear",
        "dataframes_sql_help",
    })
    async def tools(arguments: Dict[str, Any] = None, ctx: Context = None) -> BaseResult:
        action, args = normalize_action_args(arguments)
        if not action:
            return BaseResult(error="Missing required argument 'action' within tool arguments.")
        tools_manager = ToolsManager(token, ctx)
        try:
            match action:
                case "tasks_get":
                    if validation_error := validate_required_args(action, args, ["task_id"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "task_id"):
                        return err
                    return await tools_manager.tasks_get(
                        args.get("task_id"),
                        args.get("remove_on_terminal", True),
                        args.get("wait_for_terminal_ms", 0),
                        args.get("poll_interval_ms", 1000)
                    )
                case "tasks_list":
                    return await tools_manager.tasks_list(args.get("status"), args.get("status_list"))
                case "tasks_status":
                    if validation_error := validate_required_args(action, args, ["task_id"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "task_id"):
                        return err
                    return await tools_manager.tasks_status(
                        args.get("task_id"),
                        args.get("wait_for_terminal_ms", 0),
                        args.get("poll_interval_ms", 1000)
                    )
                case "tasks_cancel":
                    if validation_error := validate_required_args(action, args, ["task_id"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "task_id"):
                        return err
                    return await tools_manager.tasks_cancel(args.get("task_id"))
                case "tasks_remove":
                    if validation_error := validate_required_args(action, args, ["task_id"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "task_id"):
                        return err
                    return await tools_manager.tasks_remove(args.get("task_id"))
                case "dataframes_list":
                    return await tools_manager.dataframes_list()
                case "dataframes_get":
                    if validation_error := validate_required_args(action, args, ["dataframe_id"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "dataframe_id"):
                        return err
                    return await tools_manager.dataframes_get(args.get("dataframe_id"))
                case "dataframes_schema_groups":
                    return await tools_manager.dataframes_schema_groups(args.get("dataframe_id_list"))
                case "dataframes_query":
                    if validation_error := validate_required_args(action, args, ["sql"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "sql"):
                        return err
                    return await tools_manager.dataframes_query(
                        args.get("sql"),
                        args.get("output_format", "matrix"),
                        args.get("result_format", "auto"),
                    )
                case "dataframes_remove":
                    if validation_error := validate_required_args(action, args, ["dataframe_id_list"]):
                        return validation_error
                    dataframe_id_list = args.get("dataframe_id_list")
                    if not isinstance(dataframe_id_list, list) or not dataframe_id_list:
                        return BaseResult(
                            error="Missing required args for action 'dataframes_remove': dataframe_id_list must be a non-empty list of dataframe IDs within 'args'. "
                                  "Required args: dataframe_id_list (list[str], non-empty)."
                        )
                    return await tools_manager.dataframes_remove(dataframe_id_list)
                case "dataframes_clear":
                    return await tools_manager.dataframes_clear()
                case "dataframes_sql_help":
                    return await tools_manager.dataframes_sql_help()
                case _:
                    return BaseResult(error=f"Action {action} not found in tools manager tool")
        except httpx.HTTPStatusError:
            return BaseResult(error=f"Error: {traceback.format_exc()}")
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}\n{SUPPORT_MESSAGE}"
            )
