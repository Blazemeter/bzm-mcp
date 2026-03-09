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

from pathlib import Path

import pytest

from tools import skills_utils


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
        "---\n"
        "\n"
        "# Skill\n",
        encoding="utf-8",
    )
    (refs_dir / "guide.md").write_text("# Guide\n", encoding="utf-8")

    monkeypatch.setattr(skills_utils, "get_resources_path", lambda: resources_path)
    return resources_path


class TestSkillsUtilsPathTraversalProtection:
    def test_read_skill_file_rejects_parent_directory_traversal(self, isolated_skills_resources):
        content, error = skills_utils.read_skill_file("safe-skill", "../../etc/passwd")

        assert content is None
        assert error == "Invalid file path: parent directory traversal is not allowed"

    def test_read_skill_file_rejects_unix_absolute_path(self, isolated_skills_resources):
        content, error = skills_utils.read_skill_file("safe-skill", "/etc/passwd")

        assert content is None
        assert error == "Invalid file path: absolute paths are not allowed"

    def test_read_skill_file_rejects_windows_absolute_path(self, isolated_skills_resources):
        content, error = skills_utils.read_skill_file("safe-skill", "C:/Windows/win.ini")

        assert content is None
        assert error == "Invalid file path: absolute paths are not allowed"

    def test_read_skill_file_rejects_invalid_skill_name(self, isolated_skills_resources):
        content, error = skills_utils.read_skill_file("../safe-skill", "SKILL.md")

        assert content is None
        assert error == "Invalid skill name: ../safe-skill"

    def test_read_skill_file_allows_valid_relative_path(self, isolated_skills_resources):
        content, error = skills_utils.read_skill_file("safe-skill", "references/guide.md")

        assert error is None
        assert content == "# Guide\n"


class TestSkillUriValidation:
    def test_is_skill_uri_rejects_path_traversal_segments(self):
        assert not skills_utils.is_skill_uri(
            "blazemeter-skill-safe-skill://references/../../etc/passwd"
        )

    def test_parse_skill_uri_accepts_valid_uri(self):
        skill_name, file_path = skills_utils.parse_skill_uri(
            "blazemeter-skill-safe-skill://references/guide.md"
        )

        assert skill_name == "safe-skill"
        assert file_path == "references/guide.md"

    def test_parse_skill_uri_rejects_invalid_uri(self):
        with pytest.raises(ValueError, match="Invalid Skill URI"):
            skills_utils.parse_skill_uri("blazemeter-skill-safe-skill://../../etc/passwd")


class TestSkillResourcesListingSecurity:
    def test_list_skill_resources_uri_rejects_invalid_skill_name(self, isolated_skills_resources):
        with pytest.raises(ValueError, match="Invalid skill name"):
            skills_utils.list_skill_resources_uri("../safe-skill")

    def test_list_skill_resources_uri_rejects_missing_skill_folder(self, isolated_skills_resources):
        with pytest.raises(ValueError, match="Skill folder not found"):
            skills_utils.list_skill_resources_uri("unknown-skill")

    def test_list_skill_resources_uri_returns_only_paths_inside_skill(self, isolated_skills_resources):
        resources = skills_utils.list_skill_resources_uri("safe-skill")

        assert "blazemeter-skill-safe-skill://SKILL.md" in resources
        assert "blazemeter-skill-safe-skill://references/guide.md" in resources
