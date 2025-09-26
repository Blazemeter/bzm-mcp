import traceback
from typing import Optional, Dict, Any

import httpx
from mcp.server.fastmcp import Context

from config.blazemeter import TOOLS_PREFIX, PROJECTS_ENDPOINT
from config.token import BzmToken
from formatters.project import format_projects
from models.result import BaseResult
from tools import bridge
from tools.utils import api_request


class ProjectManager:

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx

    async def read(self, project_id: int) -> BaseResult:
        project_result = await api_request(
            self.token,
            "GET",
            f"{PROJECTS_ENDPOINT}/{project_id}",
            result_formatter=format_projects
        )

        if project_result.error:
            return project_result
        project_element = project_result.result[0]

        # Check if it's valid or allowed
        workspace_result = await bridge.read_workspace(self.token, self.ctx, project_element.workspace_id)
        if workspace_result.error:
            return workspace_result

        # Get the amount of test
        project_element.tests_count = await bridge.count_project_tests(self.token, self.ctx, project_id)
        return project_result

    async def list(self, workspace_id: int, limit: int = 50, offset: int = 0) -> BaseResult:

        # Check if it's valid or allowed
        workspace_result = await bridge.read_workspace(self.token, self.ctx, workspace_id)
        if workspace_result.error:
            return workspace_result

        parameters = {
            "workspaceId": workspace_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        return await api_request(
            self.token,
            "GET",
            f"{PROJECTS_ENDPOINT}",
            result_formatter=format_projects,
            params=parameters
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_project",
        description="""
        Operations on projects. 
        Use this when a user needs to select a project for test allocation.
        Actions:
        - read: Read a Project. Obtain information about a particular project.
            args(dict): Dictionary with the following required parameters:
                project_id (int): The id of the project to get information.
        - list: List all projects. 
            args(dict): Dictionary with the following required parameters:
                workspace_id (int): The id of the workspace to list projects from.
                limit (int, default=10, valid=[1 to 50]): The number of projects to list.
                offset (int, default=0): Number of projects to skip.
        Hints:
        - For a particular project, go directly to the read action (you don't need account or workspace information).
        - Reading also allows you to obtain the number of tests the project has without having to use a list to count.
        """
    )
    async def project(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        project_manager = ProjectManager(token, ctx)
        try:
            match action:
                case "read":
                    return await project_manager.read(args["project_id"])
                case "list":
                    limit = args.get("limit", 10)
                    offset = args.get("offset", 0)
                    return await project_manager.list(args["workspace_id"], limit, offset)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in project manager tool"
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
