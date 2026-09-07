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
from typing import Any, Awaitable, Callable, Optional

from config.runtime import AppRuntime
from telemetry import run_tool


async def run_tool_with_runtime(
        runtime: AppRuntime,
        tool_name: str,
        action: str,
        ctx: Any,
        dispatch: Callable[[], Awaitable[Any]],
        *,
        token: Any = None,
        tool_args: Any = None,
        dataframe_excluded_actions: Optional[set[str]] = None,
        disable_dataframe_materialization: bool = False,
) -> Any:
    """
    Run a tool action inside telemetry, then materialize large results via SessionStoragePort.

    Managers pass ``runtime`` once; tracing stays unaware of dataframe types.
    Materialization runs inside the tool span so duration includes the commit.
    """
    resolved_token = token if token is not None else runtime.auth.get_token(ctx)

    async def _dispatch_and_finalize() -> Any:
        result = await dispatch()
        if disable_dataframe_materialization or result is None:
            return result
        from tools.dataframe_manager import finalize_tool_result

        # Idempotent if the async task runner already materialized the payload.
        return await finalize_tool_result(
            result,
            action=action,
            args=tool_args,
            origin_manager=tool_name,
            session_storage=runtime.storage,
            scope_resolver=runtime.scope_resolver,
            token=resolved_token,
            ctx=ctx,
            excluded_actions=dataframe_excluded_actions,
        )

    return await run_tool(tool_name, action, ctx, _dispatch_and_finalize)
