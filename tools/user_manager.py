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
from typing import Any, Dict

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX, USER_ENDPOINT
from config.runtime import AppRuntime
from formatters.user import format_users
from models.manager import Manager
from models.result import BaseResult
from tools.runtime_tools import run_tool_with_runtime
from tools.utils import api_request, format_sanitized_traceback


class UserManager(Manager):

    def __init__(
        self,
        ctx: Context,
    ):
        super().__init__(ctx)

    async def read(self) -> BaseResult:
        return await api_request(
            self.token,
            "GET",
            f"{USER_ENDPOINT}",
            result_formatter=format_users
        )


def register(mcp, runtime: AppRuntime):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_user",
        description="""
Operations on user information.
Actions:
- read: Read a current user information from BlazeMeter.
Hints:
- For default account, workspace and project, use the 'read' action. 
- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.
"""
    )
    async def user(
            action: str = Field(description="The action id to execute"),
            args: Dict[str, Any] = Field(description="Dictionary with parameters"),
            ctx: Context = Field(description="Context object providing access to MCP capabilities")
    ) -> BaseResult:

        runtime.configure_context(ctx)
        user_manager = UserManager(ctx)

        async def _dispatch():
            match action:
                case "read":
                    return await user_manager.read()
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in user manager tool"
                    )

        try:
            return await run_tool_with_runtime(
                runtime, f"{TOOLS_PREFIX}_user", action, ctx, _dispatch,
                tool_args=args,
            )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {format_sanitized_traceback()}"
            )
        except Exception:
            return BaseResult(
                error=f"""Error: {format_sanitized_traceback()}
                          If you think this is a bug, please contact BlazeMeter support or report issue at https://github.com/BlazeMeter/bzm-mcp/issues"""
            )
