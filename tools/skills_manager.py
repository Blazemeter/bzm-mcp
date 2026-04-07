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
from tools.utils import format_sanitized_traceback
from tools.skills_utils import list_skills, read_skill_definition, read_skill_file, parse_skill_uri, \
    is_skill_uri, list_skill_resources_uri


# This it's based on the ideas behind Anthropic Skills
# More info about Skills https://github.com/anthropics/skills

class SkillsManager(Manager):
    skills = None  # Static to share between different instance of SkillsManager
    MAX_BATCH_CONCURRENCY = 100
    CONTENT_TRUST = "trusted"
    CONTENT_TRUST_NOTE = (
        "Skills content is sourced from curated repository resources and is trusted by design."
    )

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    @staticmethod
    async def list_skills() -> BaseResult:
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

    @staticmethod
    async def read_skill(skill_name: Optional[str]) -> BaseResult:
        if not isinstance(skill_name, str) or not skill_name.strip():
            return BaseResult(
                error="Missing required argument 'skill_name'. Please specify a non-empty skill name."
            )
        skill_name = skill_name.strip()
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

    @staticmethod
    async def read_skill_file_path(skill_name: str, file_path: str) -> BaseResult:
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

    @staticmethod
    async def list_skill_resources(skill_name: Optional[str]) -> BaseResult:
        if not isinstance(skill_name, str) or not skill_name.strip():
            return BaseResult(
                error="Missing required argument 'skill_name'. Please specify a non-empty skill name."
            )
        skill_name = skill_name.strip()
        try:
            skill_resources = list_skill_resources_uri(skill_name)
        except ValueError as e:
            return BaseResult(error=str(e))

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

    @staticmethod
    async def read_skill_resource_uri(skill_uri: Optional[str]) -> BaseResult:
        if not isinstance(skill_uri, str) or not skill_uri.strip():
            return BaseResult(
                error="Missing required argument 'skill_resource_uri'. Please specify a non-empty skill URI."
            )
        skill_uri = skill_uri.strip()
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

    @staticmethod
    async def read_skill_resource_uri_list(skill_uri_list: Optional[List[str]]) -> BaseResult:
        if not isinstance(skill_uri_list, list) or not skill_uri_list:
            return BaseResult(
                error="Missing required argument 'skill_resource_uri_list'. Please provide a non-empty list of skill URIs."
            )
        results = await asyncio.gather(
            *(SkillsManager.read_skill_resource_uri(skill_uri) for skill_uri in skill_uri_list)
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
        skill_name (str): The skill name.
- list_skill_resources: List all the Skills Resources available to learn.
    args(dict): Dictionary with the following required parameters:
        skill_name (str): The skill name.
- read_skill_resource_uri: Read file content based on a Skill Resource URI (blazemeter-skill-{skill_name}://{resource_path}).
    args(dict): Dictionary with the following required parameters:
        skill_resource_uri (str): The skill URI.
- read_skill_resource_uri_list: Read file content based on a Skill Resource URI list (['blazemeter-skill-{skill_name}://{resource_path}', ...]).
    args(dict): Dictionary with the following required parameters:
        skill_resource_uri_list (List[str]): The skill URI list.
- batch: Execute multiple actions in one call.
    args(dict): Dictionary with the following required parameters:
        batch_calls (List[Dict]): List of Actions dictionaries (excluding the action batch), each with 'action' (str) and 'args' (Dict).
Hints:
- Always generates the url attributes as a link in markdown format (like command_url).
- **CRITICAL**: For multiple actions, always use the 'batch' action.
- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.
"""
    )
    async def skills(
            action: str = Field(description="The action id to execute"),
            args: Dict[str, Any] = Field(description="Dictionary with parameters", default=None),
            ctx: Context = Field(description="Context object providing access to MCP capabilities")
    ) -> BaseResult:
        if args is None:
            args = {}

        skills_manager = SkillsManager(token, ctx)
        try:
            match action:
                case "list_skills":
                    return await skills_manager.list_skills()
                case "read_skill":
                    return await skills_manager.read_skill(args.get("skill_name"))
                case "list_skill_resources":
                    return await skills_manager.list_skill_resources(args.get("skill_name"))
                case "read_skill_resource_uri":
                    return await skills_manager.read_skill_resource_uri(args.get("skill_resource_uri"))
                case "read_skill_resource_uri_list":
                    return await skills_manager.read_skill_resource_uri_list(args.get("skill_resource_uri_list"))
                case "batch":
                    batch_calls = args.get("batch_calls", [])
                    if not isinstance(batch_calls, list) or not batch_calls:
                        return BaseResult(
                            error="batch_calls must be a non-empty list of dicts with 'action' and 'args'")

                    semaphore = asyncio.Semaphore(SkillsManager.MAX_BATCH_CONCURRENCY)

                    async def process_call(call: Dict[str, Any]) -> BaseResult | List[BaseResult]:
                        sub_action = call.get("action", "")
                        sub_args = call.get("args", {})
                        async with semaphore:
                            try:
                                # Recursively call the skills function itself
                                return await skills(sub_action, sub_args, ctx)
                            except httpx.HTTPStatusError:
                                return BaseResult(
                                    error=f"HTTP error in sub-action {sub_action}: {format_sanitized_traceback()}"
                                )
                            except Exception:
                                return BaseResult(
                                    error=f"Error in sub-action {sub_action}: {format_sanitized_traceback()}\n{SUPPORT_MESSAGE}")

                    # Parallel execution with asyncio.gather
                    results = await asyncio.gather(*[process_call(call) for call in batch_calls],
                                                   return_exceptions=True)
                    # Handle any exceptions returned
                    processed_results = [
                        r if not isinstance(r, Exception) else BaseResult(error=f"Unhandled exception: {str(r)}")
                        for r in results
                    ]
                    return BaseResult(result=processed_results)
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
