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
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import WORKSPACES_ENDPOINT, TOOLS_PREFIX
from config.token import BzmToken
from formatters.workspace import format_workspaces, format_workspaces_detailed, format_workspaces_locations
from models.manager import Manager
from models.result import BaseResult
from tools import bridge
from tools.utils import api_request, format_sanitized_traceback, run_as_task, normalize_action_args, tool_result, \
    validate_required_args, ttl_cache_method


class WorkspaceManager(Manager):

    # Note: It's allowed to list all the user workspaces without AI consent
    # the format_workspaces only expose minimum information to user
    # The read operation verify permissions and don't allow to share details.

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    @ttl_cache_method(ttl_seconds=30)
    @run_as_task()
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

    @run_as_task()
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

    @run_as_task()
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
    args(dict): Dictionary with the following parameters:
        workspace_id (int, required): The id of the workspace.
- list: List all workspaces. 
    args(dict): Dictionary with the following parameters:
        account_id (int, required): The id of the account to list workspaces from.
        limit (int, optional, default=50, valid=[1 to 50 when result_format=auto/raw, 1000 when result_format=dataframe]): Max workspaces to return.
        offset (int, optional, default=0): Number of workspaces to skip.
- read_locations: get the location list for a given workspace ID.
    args(dict): Dictionary with the following parameters:
        workspace_id (int, required): The id of the workspace.
        purpose (str, optional, default="load", valid=["load", "functional", "grid", "mock"]): The purpose filter.
Hints:
- For available locations and available billing usage use the 'read' action for a particular workspace.
- Optional result formatting in args: `result_format` = `auto` (default), `dataframe` (force dataframe), `raw` (disable dataframe materialization).
- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.
"""
    )
    @tool_result()
    async def workspace(
            arguments: Dict[str, Any] = Field(
                description="Tool arguments: action, args, and any action-specific params", default=None),
            ctx: Context = Field(description="Context object providing access to MCP capabilities")
    ) -> BaseResult:
        action, args = normalize_action_args(arguments)
        if not action:
            return BaseResult(error="Missing required argument 'action' within tool arguments.")
        workspace_manager = WorkspaceManager(token, ctx)
        try:
            match action:
                case "read":
                    if validation_error := validate_required_args(action, args, ["workspace_id"]):
                        return validation_error
                    return await workspace_manager.read(args.get("workspace_id"))
                case "list":
                    if validation_error := validate_required_args(action, args, ["account_id"]):
                        return validation_error
                    return await workspace_manager.list(args.get("account_id"), args.get("limit", 50),
                                                        args.get("offset", 0))
                case "read_locations":
                    if validation_error := validate_required_args(action, args, ["workspace_id"]):
                        return validation_error
                    purpose_raw = args.get("purpose", "load")
                    purpose = (
                        purpose_raw.strip()
                        if isinstance(purpose_raw, str) and purpose_raw.strip()
                        else "load"
                    )
                    return await workspace_manager.read_locations(args.get("workspace_id"), purpose)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in workspace manager tool"
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
