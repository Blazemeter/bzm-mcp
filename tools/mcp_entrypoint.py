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
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Optional, Set

import httpx
from mcp.server.fastmcp import Context

from config.blazemeter import SUPPORT_MESSAGE
from config.runtime import AppRuntime
from config.token import BzmToken
from models.result import BaseResult
from tools.runtime_tools import run_tool_with_runtime
from tools.utils import (
    format_sanitized_traceback,
    normalize_action_args,
    tool_result,
)

ToolDispatch = Callable[
    [str, Dict[str, Any], Optional[BzmToken], Context],
    Awaitable[BaseResult],
]


def register_managed_tool(
        mcp: Any,
        runtime: AppRuntime,
        *,
        name: str,
        description: str,
        dispatch: ToolDispatch,
        excluded_actions: Optional[Set[str]] = None,
        disable_materialization: bool = False,
        support_message: Optional[str] = SUPPORT_MESSAGE,
) -> Callable[..., Awaitable[BaseResult]]:
    """
    Shared MCP tool entrypoint: arguments= normalize → configure_context →
    run_tool_with_runtime → @tool_result wrap.

    ``dispatch(action, args, token, ctx)`` owns action routing and validation.
    Materialization stays inside ``run_tool_with_runtime`` so tracing includes persist.
    Returns the registered tool coroutine (needed for help/skills batch re-entry).
    """

    @mcp.tool(name=name, description=description)
    @tool_result(
        excluded_actions=excluded_actions,
        disable_materialization=True,
    )
    async def _tool(
            arguments: Dict[str, Any] = None,
            ctx: Context = None,
    ) -> BaseResult:
        action, args = normalize_action_args(arguments)
        if not action:
            return BaseResult(error="Missing required argument 'action' within tool arguments.")
        runtime.configure_context(ctx)
        token = runtime.auth.get_token(ctx)

        async def _run() -> BaseResult:
            return await dispatch(action, args, token, ctx)

        try:
            return await run_tool_with_runtime(
                runtime,
                name,
                action,
                ctx,
                _run,
                token=token,
                tool_args=args,
                dataframe_excluded_actions=excluded_actions,
                disable_dataframe_materialization=disable_materialization,
            )
        except httpx.HTTPStatusError:
            return BaseResult(error=f"Error: {format_sanitized_traceback()}")
        except Exception:
            detail = format_sanitized_traceback()
            if support_message:
                return BaseResult(error=f"Error: {detail}\n{support_message}")
            return BaseResult(error=f"Error: {detail}")

    return _tool
