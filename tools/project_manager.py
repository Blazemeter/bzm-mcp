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
from typing import Optional, Dict, Any

import httpx
from mcp.server.fastmcp import Context

from config.blazemeter import TOOLS_PREFIX, PROJECTS_ENDPOINT
from config.token import BzmToken
from formatters.project import format_projects
from models.manager import Manager
from models.result import BaseResult
from tools import bridge
from tools.utils import api_request, format_sanitized_traceback, ttl_cache_method, run_as_task, normalize_action_args, \
    tool_result, validate_required_args


class ProjectManager(Manager):

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    @ttl_cache_method(ttl_seconds=30)
    @run_as_task()
    async def read(self, project_id: int, include_tests_count: bool = True) -> BaseResult:
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

        if include_tests_count:
            # Optional enrichment; can be disabled for fast hierarchy validation paths.
            project_element.tests_count = await bridge.count_project_tests(self.token, self.ctx, project_id)
        return project_result

    @run_as_task()
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
    args(dict): Dictionary with the following parameters:
        project_id (int, required): The id of the project to get information.
- list: List all projects. 
    args(dict): Dictionary with the following parameters:
        workspace_id (int, required): The id of the workspace to list projects from.
        limit (int, optional, default=50, valid=[1 to 50 when result_format=auto/raw, 1000 when result_format=dataframe]): Max projects to return.
        offset (int, optional, default=0): Number of projects to skip.
Hints:
- For a particular project, go directly to the read action (you don't need account or workspace information).
- Reading also allows you to obtain the number of tests the project has without having to use a list to count.
- Optional result formatting in args: `result_format` = `auto` (default), `dataframe` (force dataframe), `raw` (disable dataframe materialization).
- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.
"""
    )
    @tool_result()
    async def project(arguments: Dict[str, Any] = None, ctx: Context = None) -> BaseResult:
        action, args = normalize_action_args(arguments)
        if not action:
            return BaseResult(error="Missing required argument 'action' within tool arguments.")
        project_manager = ProjectManager(token, ctx)
        try:
            match action:
                case "read":
                    if validation_error := validate_required_args(action, args, ["project_id"]):
                        return validation_error
                    return await project_manager.read(args.get("project_id"))
                case "list":
                    if validation_error := validate_required_args(action, args, ["workspace_id"]):
                        return validation_error
                    limit = args.get("limit", 50)
                    offset = args.get("offset", 0)
                    return await project_manager.list(args.get("workspace_id"), limit, offset)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in project manager tool"
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
