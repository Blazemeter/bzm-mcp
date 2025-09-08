import traceback
from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context

from config.token import BzmToken
from models.result import BaseResult
from .base import api_request, TOOLS_PREFIX


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_user",
        description="""
            Operations on tests executions and results reports.
            Actions:
            - read: Read a current user information from BlazeMeter.
        """
    )
    async def user(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        try:
            match action:
                case "read":
                    return BaseResult(
                        result=[await api_request(token, "GET", "/user")]
                    )
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in user manager tool"
                    )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
