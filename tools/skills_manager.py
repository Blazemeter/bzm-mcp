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
import asyncio
from typing import Optional, Dict, Any, List
from urllib.parse import unquote

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX, SUPPORT_MESSAGE
from config.token import BzmToken
from models.manager import Manager
from models.result import BaseResult
from tools.utils import (
    format_sanitized_traceback,
    run_as_task,
    execute_batch_calls,
    tool_result,
    normalize_action_args,
    validate_non_empty_str_arg,
    validate_required_args,
)
from tools.skills_utils import list_skills, read_skill_definition, read_skill_file, parse_skill_uri, \
    is_skill_uri, list_skill_resources_uri


# This it's based on the ideas behind Anthropic Skills
# More info about Skills https://github.com/anthropics/skills

class SkillsManager(Manager):
    skills = None  # Static to share between different instance of SkillsManager
    CONTENT_TRUST = "trusted"
    CONTENT_TRUST_NOTE = (
        "Skills content is sourced from curated repository resources and is trusted by design."
    )

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    @run_as_task()
    async def list_skills(self) -> BaseResult:
        errors = []
        if SkillsManager.skills is None:
            skills, errors = list_skills()
            SkillsManager.skills = skills

        return BaseResult(
            result=SkillsManager.skills,
            total=len(SkillsManager.skills),
            has_more=False,
            error=errors[0] if errors and len(errors) > 0 else None  # Only the first error
        )

    @run_as_task()
    async def read_skill(self, skill_name: str) -> BaseResult:
        skill_content, error = read_skill_definition(skill_name)
        # Trust policy note for future audits:
        # Skills and their resources are curated project artifacts and considered trusted by design.
        return BaseResult(
            result=[{
                "skill_name": skill_name,
                "path": "SKILL.md",
                "content": skill_content,
                "content_trust": SkillsManager.CONTENT_TRUST,
                "content_trust_note": SkillsManager.CONTENT_TRUST_NOTE,
            }],
            error=error
        )

    async def read_skill_file_path(self, skill_name: str, file_path: str) -> BaseResult:
        skill_content, error = read_skill_file(skill_name, file_path)
        return BaseResult(
            result=[{
                "skill_name": skill_name,
                "path": file_path,
                "content": skill_content,
                "content_trust": SkillsManager.CONTENT_TRUST,
                "content_trust_note": SkillsManager.CONTENT_TRUST_NOTE,
            }],
            error=error
        )

    @run_as_task()
    async def list_skill_resources(self, skill_name: str) -> BaseResult:
        skill_resources = list_skill_resources_uri(skill_name)
        return BaseResult(
            result=[{
                "skill_name": skill_name,
                "resources": skill_resources,
                "content_trust": SkillsManager.CONTENT_TRUST,
                "content_trust_note": SkillsManager.CONTENT_TRUST_NOTE,
            }],
            total=len(skill_resources),
            has_more=False,
        )

    @run_as_task()
    async def read_skill_resource_uri(self, skill_uri: str) -> BaseResult:
        if is_skill_uri(skill_uri):
            skill_name, file_path = parse_skill_uri(skill_uri)
            skill_content, error = read_skill_file(skill_name, file_path)
            return BaseResult(
                result=[{
                    "skill_name": skill_name,
                    "path": file_path,
                    "content": skill_content,
                    "content_trust": SkillsManager.CONTENT_TRUST,
                    "content_trust_note": SkillsManager.CONTENT_TRUST_NOTE,
                }],
                error=error
            )
        else:
            return BaseResult(
                error=f"Invalid Skill URI: {skill_uri}"
            )

    @run_as_task()
    async def read_skill_resource_uri_list(self, skill_uri_list: List[str]) -> BaseResult:
        results = await asyncio.gather(
            *(self.read_skill_resource_uri(skill_uri) for skill_uri in skill_uri_list)
        )
        return BaseResult(
            result=results,
            total=len(results),
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.resource("blazemeter-skill-{skill_name}://{path}")
    def universal_skills_handler(skill_name: str, path: str) -> str:
        path = unquote(path)
        content, error = read_skill_file(skill_name, path)
        if error:
            return error
        return content

    async def _dispatch_batch_skills(batch_calls: Any, ctx: Context):
        async def _process_skills_batch_call(call: Dict[str, Any]) -> BaseResult:
            if not isinstance(call, dict):
                return BaseResult(error="Each batch call must be a dict with 'action' and optional 'args'.")
            sub_action = call.get("action", "")
            raw_sub_args = call.get("args", {})
            sub_args = dict(raw_sub_args) if isinstance(raw_sub_args, dict) else {}
            try:
                return await skills({"action": sub_action, "args": sub_args}, ctx)
            except httpx.HTTPStatusError:
                return BaseResult(error=f"HTTP error in sub-action {sub_action}: {format_sanitized_traceback()}")
            except Exception:
                return BaseResult(error=f"Error in sub-action {sub_action}: {format_sanitized_traceback()}")

        return await execute_batch_calls(
            batch_calls,
            _process_skills_batch_call,
        )

    @mcp.tool(
        name=f"{TOOLS_PREFIX}_skills",
        description="""
Operations to obtain Skills around BlazeMeter.
**Note**: If you need to call this action multiple times (even with different parameters), 
use the `batch` action instead of making separate calls.
Actions:
- list_skills: List all the Skills available to learn.
- read_skill: Read detailed information about a specific skill_name.
    args(dict): Dictionary with the following required parameters:
        skill_name (str, required, non-empty): The skill name.
- list_skill_resources: List all the Skills Resources available to learn.
    args(dict): Dictionary with the following required parameters:
        skill_name (str, required, non-empty): The skill name.
- read_skill_resource_uri: Read file content based on a Skill Resource URI (blazemeter-skill-{skill_name}://{resource_path}).
    args(dict): Dictionary with the following required parameters:
        skill_resource_uri (str, required, non-empty): The skill URI.
- read_skill_resource_uri_list: Read file content based on a Skill Resource URI list (['blazemeter-skill-{skill_name}://{resource_path}', ...]).
    args(dict): Dictionary with the following required parameters:
        skill_resource_uri_list (List[str], required, non-empty): The skill URI list.
- batch: Execute multiple actions in one call.
    args(dict): Dictionary with the following required parameters:
        batch_calls (List[Dict]): List of Actions dictionaries (excluding the action batch), each with 'action' (str) and 'args' (Dict).
Hints:
- Always generates the url attributes as a link in markdown format (like command_url).
- **CRITICAL**: For multiple actions, always use the 'batch' action.
- **IMPORTANT**: `batch` sub-actions execute directly (no forced task mode); responses are returned inline in this same call.
- Optional result formatting in args: `result_format` = `auto` (default), `dataframe` (force dataframe), `raw` (disable dataframe materialization).
- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.
"""
    )
    @tool_result(excluded_actions={"batch"})
    async def skills(
            arguments: Dict[str, Any] = Field(description="Tool arguments: action, args, and any action-specific params", default=None),
            ctx: Context = Field(description="Context object providing access to MCP capabilities")
    ) -> BaseResult:
        action, args = normalize_action_args(arguments)
        if not action:
            return BaseResult(error="Missing required argument 'action' within tool arguments.")
        skills_manager = SkillsManager(token, ctx)
        try:
            match action:
                case "list_skills":
                    return await skills_manager.list_skills()
                case "read_skill":
                    if validation_error := validate_required_args(action, args, ["skill_name"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "skill_name"):
                        return err
                    return await skills_manager.read_skill(str(args.get("skill_name")).strip())
                case "list_skill_resources":
                    if validation_error := validate_required_args(action, args, ["skill_name"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "skill_name"):
                        return err
                    return await skills_manager.list_skill_resources(str(args.get("skill_name")).strip())
                case "read_skill_resource_uri":
                    if validation_error := validate_required_args(action, args, ["skill_resource_uri"]):
                        return validation_error
                    if err := validate_non_empty_str_arg(action, args, "skill_resource_uri"):
                        return err
                    return await skills_manager.read_skill_resource_uri(
                        str(args.get("skill_resource_uri")).strip()
                    )
                case "read_skill_resource_uri_list":
                    if validation_error := validate_required_args(action, args, ["skill_resource_uri_list"]):
                        return validation_error
                    skill_resource_uri_list = args.get("skill_resource_uri_list", [])
                    if (
                        not isinstance(skill_resource_uri_list, list)
                        or len(skill_resource_uri_list) == 0
                    ):
                        return BaseResult(
                            error=(
                                f"Missing required args for action '{action}': skill_resource_uri_list must be a "
                                f"non-empty list within 'args'. Required args: skill_resource_uri_list (list[str], "
                                f"non-empty)."
                            )
                        )
                    return await skills_manager.read_skill_resource_uri_list(skill_resource_uri_list)
                case "batch":
                    return await _dispatch_batch_skills(args.get("batch_calls", []), ctx)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in skills manager tool"
                    )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {format_sanitized_traceback()}"
            )
        except Exception:
            return BaseResult(
                error=f"Error: {format_sanitized_traceback()}\n{SUPPORT_MESSAGE}"
            )
