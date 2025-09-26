import traceback
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX, USER_ENDPOINT
from config.token import BzmToken
from formatters.user import format_users
from models.result import BaseResult
from tools.utils import api_request


class UserManager:

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx

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
                          If you think this is a bug, please contact blazemeter support or report issue at https://github.com/BlazeMeter/bzm-mcp/issues"""
            )
