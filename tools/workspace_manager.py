import traceback
from datetime import datetime
from typing import Any, Dict, Optional, List, Union

from pydantic import BaseModel, Field

from config.token import BzmToken
from .base import api_request, BaseResult


class Workspace(BaseModel):
    """Workspace basic information structure."""
    workspace_id: int = Field(description="The unique identifier for the workspace. Also known as a workspaceId")
    name: str = Field(description="The name of this workspace")
    created: datetime = Field(description="The datetime for when the workspace was created")
    updated: datetime = Field(description="The datetime for when the workspace was updated")
    enabled: bool = Field(description="Denotes if the workspace is enabled or not")


class WorkspaceDetailed(Workspace):
    """Workspace detailed information structure."""
    owner: Dict[str, Any] = Field(description="The details of the owner of the workspace")
    allowance: Dict[str, Any] = Field(description="The available billing usage details")
    users_count: int = Field(description="The number of users in the workspace")
    locations: List[Dict[str, Any]] = Field(description="The location details available to the workspace")


class WorkspaceResult(BaseResult):
    result: Optional[List[Union[WorkspaceDetailed, Workspace]]] = Field(description="Workspaces List", default=None)


class WorkspaceManager:

    def __init__(self, token: Optional[BzmToken]):
        self.token = token

    async def read(self, workspace_id: int) -> WorkspaceResult:
        workspace_response = await api_request(self.token, "GET", f"/workspaces/{workspace_id}")
        workspaces = [workspace_response.get("result", None)]
        return WorkspaceResult(
            result=self.normalize_workspaces(workspaces, detailed=True),
            has_more=False
        )

    async def list(self, account_id: int, limit: int = 50, offset: int = 0) -> WorkspaceResult:
        parameters = {
            "accountId": account_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        workspaces_response = await api_request(self.token, "GET", "/workspaces", params=parameters)
        workspaces = workspaces_response.get("result", [])
        has_more = workspaces_response.get("total", 0) - (offset + limit) > 0

        return WorkspaceResult(
            result=self.normalize_workspaces(workspaces),
            has_more=has_more
        )

    @staticmethod
    def normalize_workspaces(workspaces: List[Any], detailed: bool = False) -> List[
        Union[WorkspaceDetailed, Workspace]]:
        normalized_workspaces = []
        for workspace in workspaces:

            workspace_element = {
                "workspace_id": workspace["id"],
                "name": workspace["name"],
                "created": datetime.fromtimestamp(workspace["created"]),
                "updated": datetime.fromtimestamp(workspace["updated"]),
                "enabled": workspace["enabled"],
            }
            if detailed:
                workspace_element.update({
                    "owner": workspace["owner"],
                    "allowance": workspace["allowance"],
                    "users_count": workspace["membersCount"],
                    "locations": workspace["locations"],
                })
            workspace_object = WorkspaceDetailed(**workspace_element) if detailed else Workspace(**workspace_element)
            normalized_workspaces.append(workspace_object)
        return normalized_workspaces


def register(mcp, token: Optional[BzmToken]):
    """
    Registers the `bzm_mcp_retrieve_workspaces` tool on the given MCP server,
    using the provided BzmToken for authentication.
    """

    @mcp.tool(
        name="bzm_mcp_workspaces",
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
                """
    )
    async def bzm_mcp_tests_tool(action: str, args: Dict[str, Any]) -> WorkspaceResult:
        workspace_manager = WorkspaceManager(token)
        try:
            match action:
                case "read":
                    return await workspace_manager.read(args["workspace_id"])
                case "list":
                    return await workspace_manager.list(args["account_id"], args.get("limit", 50), args.get("offset", 0))
                case _:
                    return WorkspaceResult(
                        error=f"Action {action} not found in tests manager tool"
                    )
        except Exception:
            return WorkspaceResult(
                error=f"Error: {traceback.format_exc()}"
            )
