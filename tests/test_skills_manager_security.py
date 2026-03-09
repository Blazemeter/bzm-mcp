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

from tools import skills_utils
from tools.skills_manager import SkillsManager


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
        result = asyncio.run(SkillsManager.list_skill_resources("../safe-skill"))

        assert result.error is not None
        assert "Invalid skill name" in result.error
        assert result.result is None

    def test_list_skill_resources_returns_controlled_error_for_missing_skill(self, isolated_skills_resources):
        result = asyncio.run(SkillsManager.list_skill_resources("unknown-skill"))

        assert result.error is not None
        assert "Skill folder not found" in result.error
        assert result.result is None
