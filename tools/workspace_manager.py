import traceback
from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import WORKSPACES_ENDPOINT, TOOLS_PREFIX
from config.token import BzmToken
from formatters.workspace import format_workspaces, format_workspaces_detailed
from models.result import BaseResult
from tools.utils import api_request


class WorkspaceManager:

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx

    async def read(self, workspace_id: int) -> BaseResult:
        return await api_request(
            self.token,
            "GET",
            f"{WORKSPACES_ENDPOINT}/{workspace_id}",
            result_formatter=format_workspaces_detailed
        )

    async def list(self, account_id: int, limit: int = 50, offset: int = 0) -> BaseResult:
        parameters = {
            "accountId": account_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        return await api_request(
            self.token,
            "GET",
            f"{WORKSPACES_ENDPOINT}",
            result_formatter=format_workspaces,
            params=parameters
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_workspaces",
        description="""
                Operations on workspaces.
                Actions: 
                - read: Read a workspace. Get the detailed information of a workspace.
                    args(dict): Dictionary with the following required parameters:
                        workspace_id (int): The id of the workspace.
                - list: List all workspaces. 
                    args(dict): Dictionary with the following required parameters:
                        account_id (int): The id of the account to list the workspaces from
                        limit (int, default=50): The number of workspaces to list.
                        offset (int, default=0): Number of workspaces to skip.
                Hints:
                - For available locations and available billing usage use the 'read' action for a particular workspace.
                """
    )
    async def workspace(
            action: str = Field(description="The action id to execute"),
            args: Dict[str, Any] = Field(description="Dictionary with parameters"),
            ctx: Context = Field(description="Context object providing access to MCP capabilities")
    ) -> BaseResult:

        workspace_manager = WorkspaceManager(token, ctx)
        try:
            match action:
                case "read":
                    return await workspace_manager.read(args["workspace_id"])
                case "list":
                    return await workspace_manager.list(args["account_id"], args.get("limit", 50),
                                                        args.get("offset", 0))
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in tests manager tool"
                    )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
