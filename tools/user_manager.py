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
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX, USER_ENDPOINT
from config.token import BzmToken
from formatters.user import format_users
from models.manager import Manager
from models.result import BaseResult
from tools.utils import api_request


class UserManager(Manager):

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    async def read(self) -> BaseResult:
        return await api_request(
            self.token,
            "GET",
            f"{USER_ENDPOINT}",
            result_formatter=format_users
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_user",
        description="""
            Operations on user information.
            Actions:
            - read: Read a current user information from BlazeMeter.
            Hints:
            - For default account, workspace and project, use the 'read' action. 
        """
    )
    async def user(
            action: str = Field(description="The action id to execute"),
            args: Dict[str, Any] = Field(description="Dictionary with parameters"),
            ctx: Context = Field(description="Context object providing access to MCP capabilities")
    ) -> BaseResult:

        user_manager = UserManager(token, ctx)
        try:
            match action:
                case "read":
                    return await user_manager.read()
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in user manager tool"
                    )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
        except Exception:
            return BaseResult(
                error=f"""Error: {traceback.format_exc()}
                          If you think this is a bug, please contact BlazeMeter support or report issue at https://github.com/BlazeMeter/bzm-mcp/issues"""
            )
