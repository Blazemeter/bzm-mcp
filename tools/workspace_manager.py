import traceback
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import WORKSPACES_ENDPOINT, TOOLS_PREFIX
from config.token import BzmToken
from formatters.workspace import format_workspaces, format_workspaces_detailed, format_workspaces_locations
from models.result import BaseResult
from tools import bridge
from tools.utils import api_request


class WorkspaceManager:

    # Note: It's allowed to list all the user workspaces without AI consent
    # the format_workspaces only expose minimum information to user
    # The read operation verify permissions and don't allow to share details.

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx

    async def read(self, workspace_id: int) -> BaseResult:

        workspace_result = await api_request(
            self.token,
            "GET",
            f"{WORKSPACES_ENDPOINT}/{workspace_id}",
            result_formatter=format_workspaces_detailed
        )
        if workspace_result.error:
            return workspace_result
        else:
            # Check if it's valid or allowed
            account_result = await bridge.read_account(self.token, self.ctx,
                                                       workspace_result.result[0].account_id)
            if account_result.error:
                return account_result
            else:
                return workspace_result

    async def list(self, account_id: int, limit: int = 50, offset: int = 0) -> BaseResult:

        # Check if it's valid or allowed
        account_data = await bridge.read_account(self.token, self.ctx, account_id)
        if account_data.error:
            return account_data

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

    async def read_locations(self, workspace_id: int, purpose: str = "load") -> BaseResult:

        locations_result = await api_request(
            self.token,
            "GET",
            f"{WORKSPACES_ENDPOINT}/{workspace_id}",
            result_formatter=format_workspaces_locations,
            result_formatter_params={"purpose": purpose}
        )
        if locations_result.error:
            return locations_result
        else:
            # Check if it's valid or allowed
            account_result = await bridge.read_account(self.token, self.ctx,
                                                       locations_result.result[0]["account_id"])
            if account_result.error:
                return account_result
            else:
                return locations_result


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
                        limit (int, default=10, valid=[1 to 50]): The number of workspaces to list.
                        offset (int, default=0): Number of workspaces to skip.
                - read_locations: get the location list for a given workspace ID.
                    args(dict): Dictionary with the following required parameters:
                        workspace_id (int): The id of the workspace.
                        purpose (str, default="load", valid=["load", "functional", "grid", "mock"]): The purpose filter.
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
                case "read_locations":
                    return await workspace_manager.read_locations(args["workspace_id"], args.get("purpose", "load"))
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in workspace manager tool"
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
