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

import pytest

from config.auth import StdioAuthProvider
from config.blazemeter import TOOLS_PREFIX
from config.file_access import build_file_access
from config.runtime import AppRuntime
from config.storage import DefaultSessionScopeResolver, SessionScope
from config.token import BzmToken
from tests.conftest import make_ctx, run_async
from tools import skills_utils
from tools.dataframe_manager import list_dataframes_metadata
from tools.skills_manager import SkillsManager, register as register_skills_tool


@pytest.fixture
def isolated_skills_resources(tmp_path, monkeypatch):
    resources_path = tmp_path / "resources"
    skill_dir = resources_path / "skills" / "safe-skill"
    refs_dir = skill_dir / "references"
    refs_dir.mkdir(parents=True)

    (skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: safe-skill\n"
        "description: Security test skill\n"
        "---\n",
        encoding="utf-8",
    )
    (refs_dir / "guide.md").write_text("# Guide\n", encoding="utf-8")

    monkeypatch.setattr(skills_utils, "get_resources_path", lambda: resources_path)
    return resources_path


class TestSkillsManagerListResourcesErrors:
    def test_list_skill_resources_returns_controlled_error_for_invalid_skill_name(self, isolated_skills_resources):
        manager = SkillsManager(ctx=None)
        result = asyncio.run(manager.list_skill_resources("../safe-skill"))

        assert result.error is not None
        assert "Invalid skill name" in result.error
        assert result.result is None

    def test_list_skill_resources_returns_controlled_error_for_missing_skill(self, isolated_skills_resources):
        manager = SkillsManager(ctx=None)
        result = asyncio.run(manager.list_skill_resources("unknown-skill"))

        assert result.error is not None
        assert "Skill folder not found" in result.error
        assert result.result is None


class FakeMcp:
    def __init__(self):
        self.tools = {}

    def tool(self, name, description):
        def decorator(func):
            self.tools[name] = func
            return func

        return decorator


class TestSkillsSkipDataframeMaterialization:
    def test_read_skill_keeps_large_document_inline(self, isolated_skills_resources, in_memory_session_storage):
        large_body = "x" * 12000
        skill_dir = isolated_skills_resources / "skills" / "safe-skill"
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: safe-skill\n"
            "description: Security test skill\n"
            "---\n"
            f"{large_body}\n",
            encoding="utf-8",
        )
        SkillsManager.skills = None
        token = BzmToken("user-skills", "secret")
        runtime = AppRuntime(
            transport="stdio",
            auth=StdioAuthProvider(token),
            storage=in_memory_session_storage,
            file_access=build_file_access("stdio"),
            scope_resolver=DefaultSessionScopeResolver(),
            user_config={"token": token},
        )
        mcp = FakeMcp()
        register_skills_tool(mcp, runtime)
        tool = mcp.tools[f"{TOOLS_PREFIX}_skills"]
        ctx = make_ctx(token, "sess-skills")

        result = asyncio.run(
            tool({"action": "read_skill", "args": {"skill_name": "safe-skill"}}, ctx=ctx)
        )

        assert result.error is None
        assert result.result[0].get("stored_as_dataframe") is not True
        assert large_body in result.result[0]["content"]
        listed = run_async(
            list_dataframes_metadata(
                in_memory_session_storage, SessionScope("user-skills", "sess-skills")
            )
        )
        assert listed == []
