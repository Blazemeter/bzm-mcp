import traceback
from typing import Optional, Dict, Any

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX, SUPPORT_MESSAGE
from config.token import BzmToken
from models.manager import Manager
from models.result import BaseResult
from tools.skills_utils import list_skills, read_skill_definition, read_skill_file, parse_skill_uri, \
    is_skill_uri, list_skill_resources_uri


# This it's based on the ideas behind Anthropic Skills
# More info about Skills https://github.com/anthropics/skills

class SkillsManager(Manager):
    skills = None  # Static to share between different instance of SkillsManager

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
            error=errors[0] if errors and len(errors) > 0 else None  # Only the first error
        )

    @staticmethod
    async def read_skill(skill_name: str) -> BaseResult:
        skill_content, error = read_skill_definition(skill_name)
        return BaseResult(
            result=[{
                "skill_name": skill_name,
                "path": "SKILL.md",
                "content": skill_content,
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
            }],
            error=error
        )

    @staticmethod
    async def list_skill_resources(skill_name: str) -> BaseResult:
        skill_resources = list_skill_resources_uri(skill_name)
        return BaseResult(
            result=[{
                "skill_name": skill_name,
                "resources": skill_resources,
            }]
        )

    @staticmethod
    async def read_skill_resource_uri(skill_uri: str) -> BaseResult:
        if is_skill_uri(skill_uri):
            skill_name, file_path = parse_skill_uri(skill_uri)
            skill_content, error = read_skill_file(skill_name, file_path)
            return BaseResult(
                result=[{
                    "skill_name": skill_name,
                    "path": file_path,
                    "content": skill_content,
                }],
                error=error
            )
        else:
            return BaseResult(
                error=f"Invalid Skill URI: {skill_uri}"
            )


def register(mcp, token: Optional[BzmToken]):
    @mcp.resource("skills-{skill_name}://{path}")
    def universal_skills_handler(skill_name: str, path: str) -> BaseResult:
        content, error = read_skill_file(skill_name, path)
        return BaseResult(
            result=[{
                "skill_name": skill_name,
                "path": path,
                "content": content,
            }],
            error=error
        )

    @mcp.tool(
        name=f"{TOOLS_PREFIX}_skills",
        description="""
Operations to obtain Skills around BlazeMeter.
Actions:
- list_skills: List all the Skills available to learn.
- read_skill: Read detailed information about a specific skill_name.
    args(dict): Dictionary with the following required parameters:
        skill_name (str): The skill name.
- list_skill_resources: List all the Skills Resources available to learn.
    args(dict): Dictionary with the following required parameters:
        skill_name (str): The skill name.
- read_skill_resource_uri: Read file content based on a Skill Resource URI (skill-{skill_name}://{resource_path}).
    args(dict): Dictionary with the following required parameters:
        skill_resource_uri (str): The skill URI.

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
                    return await skills_manager.read_skill(args.get("skill_name", ""))
                case "list_skill_resources":
                    return await skills_manager.list_skill_resources(args.get("skill_name", ""))
                case "read_skill_resource_uri":
                    return await skills_manager.read_skill_resource_uri(args.get("skill_resource_uri", ""))
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in skills manager tool"
                    )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}\n{SUPPORT_MESSAGE}"
            )
