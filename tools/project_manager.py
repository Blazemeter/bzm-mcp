import traceback
from typing import Optional, Dict, Any, List

from mcp.server.fastmcp import Context

from config.token import BzmToken
from models.result import BaseResult
from .base import api_request, get_date_time_iso, TOOLS_PREFIX


class ProjectManager:

    def __init__(self, token: Optional[BzmToken]):
        self.token = token

    async def read(self, project_id: int) -> BaseResult:
        project_response = await api_request(self.token, "GET", f"/projects/{project_id}")

        if "error" in project_response and project_response["error"]:
            return BaseResult(
                error=project_response.get("error")
            )

        projects = [project_response.get("result", None)]
        return BaseResult(
            result=self.normalize_projects(projects),
            has_more=False
        )

    async def list(self, account_id: int, workspace_id: int, limit: int = 50, offset: int = 0) -> BaseResult:
        parameters = {
            "workspaceId": workspace_id,
            "accountId": account_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        projects_response = await api_request(self.token, "GET", f"/projects", params=parameters)

        if "error" in projects_response and projects_response["error"]:
            return BaseResult(
                error=projects_response.get("error")
            )

        projects = projects_response.get("result", [])
        has_more = projects_response.get("total", 0) - (offset + limit) > 0

        return BaseResult(
            result=self.normalize_projects(projects),
            has_more=has_more
        )

    @staticmethod
    def normalize_projects(projects: List[Any]) -> List[Any]:
        formatted_projects = []
        for project in projects:
            formatted_project = {
                "project_id": project.get("id"),
                "project_name": project.get("name", "Unknown"),
                "description": project.get("description", ""),
                "created": get_date_time_iso(project.get("created")),
                "updated": get_date_time_iso(project.get("updated")),
                "tests_count": project.get("testsCount", 0)
            }
            formatted_projects.append(formatted_project)
        return formatted_projects


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_project",
        description="""
        Operations on projects in a specific workspace as workspace_id and account as account_id. 
        Use this when a user needs to select a project for test allocation.
        Actions:
        - read: Read a Project. Get the information of a project.
            args(dict): Dictionary with the following required parameters:
                project_id (int): The id of the project to get information.
        - list: List all tests. 
            args(dict): Dictionary with the following required parameters:
                account_id (int): The id of the account to list the tests from
                workspace_id (int): The id of the workspace to list tests from.
                limit (int, default=50): The number of tests to list.
                offset (int, default=0): Number of tests to skip.
        """
    )
    async def project(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        project_manager = ProjectManager(token)
        try:
            match action:
                case "read":
                    return await project_manager.read(args["project_id"])
                case "list":
                    limit = args.get("limit", 10)
                    offset = args.get("offset", 0)
                    return await project_manager.list(args["account_id"], args["workspace_id"], limit, offset)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in project manager tool"
                    )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
