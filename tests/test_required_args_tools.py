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

from config.blazemeter import TOOLS_PREFIX
from tools.account_manager import register as register_account_tool
from tools.execution_manager import register as register_execution_tool
from tools.help_manager import register as register_help_tool
from tools.project_manager import register as register_project_tool
from tools.skills_manager import register as register_skills_tool
from tools.test_manager import register as register_tests_tool
from tools.workspace_manager import register as register_workspaces_tool


class FakeMcp:
    def __init__(self):
        self.tools = {}

    def tool(self, name, description):
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

    def resource(self, pattern):
        def decorator(func):
            return func
        return decorator


class TestRequiredArgumentsForTools:
    def test_account_read_requires_account_id(self):
        mcp = FakeMcp()
        register_account_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_account"]

        result = asyncio.run(tool("read", {}, ctx=None))
        assert result.error is not None
        assert "account_id" in result.error

    def test_workspace_list_requires_account_id(self):
        mcp = FakeMcp()
        register_workspaces_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_workspaces"]

        result = asyncio.run(tool("list", {}, ctx=None))
        assert result.error is not None
        assert "account_id" in result.error

    def test_project_read_requires_project_id(self):
        mcp = FakeMcp()
        register_project_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_project"]

        result = asyncio.run(tool("read", {}, ctx=None))
        assert result.error is not None
        assert "project_id" in result.error

    def test_tests_create_requires_test_name(self):
        mcp = FakeMcp()
        register_tests_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_tests"]

        result = asyncio.run(tool("create", {"project_id": 123}, ctx=None))
        assert result.error is not None
        assert "test_name" in result.error

    def test_tests_upload_assets_requires_file_paths(self):
        mcp = FakeMcp()
        register_tests_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_tests"]

        result = asyncio.run(tool("upload_assets", {"test_id": 123}, ctx=None))
        assert result.error is not None
        assert "file_paths" in result.error

    def test_execution_read_requires_execution_id(self):
        mcp = FakeMcp()
        register_execution_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_execution"]

        result = asyncio.run(tool("read", {}, ctx=None))
        assert result.error is not None
        assert "execution_id" in result.error

    def test_execution_read_summary_requires_execution_id(self):
        mcp = FakeMcp()
        register_execution_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_execution"]

        result = asyncio.run(tool("read_summary", {}, ctx=None))
        assert result.error is not None
        assert "execution_id" in result.error

    def test_skills_read_skill_requires_skill_name(self):
        mcp = FakeMcp()
        register_skills_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_skills"]

        result = asyncio.run(tool("read_skill", {}, ctx=None))
        assert result.error is not None
        assert "skill_name" in result.error

    def test_skills_read_skill_resource_uri_requires_uri(self):
        mcp = FakeMcp()
        register_skills_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_skills"]

        result = asyncio.run(tool("read_skill_resource_uri", {}, ctx=None))
        assert result.error is not None
        assert "skill_resource_uri" in result.error

    def test_skills_read_skill_resource_uri_list_requires_non_empty_list(self):
        mcp = FakeMcp()
        register_skills_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_skills"]

        result = asyncio.run(tool("read_skill_resource_uri_list", {}, ctx=None))
        assert result.error is not None
        assert "skill_resource_uri_list" in result.error

    def test_help_read_help_info_requires_help_id_list(self):
        mcp = FakeMcp()
        register_help_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_help"]

        result = asyncio.run(tool("read_help_info", {}, ctx=None))
        assert result.error is not None
        assert "help_id_list" in result.error

    def test_help_list_help_category_content_requires_subcategory_list(self):
        mcp = FakeMcp()
        register_help_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_help"]

        result = asyncio.run(tool("list_help_category_content", {}, ctx=None))
        assert result.error is not None
        assert "subcategory_id_list" in result.error
