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
from models.result import BaseResult
from tools.help_manager import HelpManager, register as register_help_tool
from tools.skills_manager import SkillsManager, register as register_skills_tool


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


class TestBatchControls:
    def test_help_batch_respects_concurrency_limit(self, monkeypatch):
        mcp = FakeMcp()
        register_help_tool(mcp, token=None)
        help_tool = mcp.tools[f"{TOOLS_PREFIX}_help"]
        HelpManager.help_tree = {}
        monkeypatch.setattr(HelpManager, "MAX_BATCH_CONCURRENCY", 2)

        active_calls = {"current": 0, "max": 0}

        async def slow_list_help_categories(self):
            active_calls["current"] += 1
            active_calls["max"] = max(active_calls["max"], active_calls["current"])
            try:
                await asyncio.sleep(0.02)
                return BaseResult(result=[])
            finally:
                active_calls["current"] -= 1

        monkeypatch.setattr(HelpManager, "list_help_categories", slow_list_help_categories)

        batch_calls = [{"action": "list_help_categories", "args": {}} for _ in range(6)]
        result = asyncio.run(help_tool("batch", {"batch_calls": batch_calls}, ctx=None))

        assert result.error is None
        assert active_calls["max"] <= 2

    def test_skills_batch_respects_concurrency_limit(self, monkeypatch):
        mcp = FakeMcp()
        register_skills_tool(mcp, token=None)
        skills_tool = mcp.tools[f"{TOOLS_PREFIX}_skills"]
        monkeypatch.setattr(SkillsManager, "MAX_BATCH_CONCURRENCY", 2)

        active_calls = {"current": 0, "max": 0}

        async def slow_list_skills():
            active_calls["current"] += 1
            active_calls["max"] = max(active_calls["max"], active_calls["current"])
            try:
                await asyncio.sleep(0.02)
                return BaseResult(result=[])
            finally:
                active_calls["current"] -= 1

        monkeypatch.setattr(SkillsManager, "list_skills", staticmethod(slow_list_skills))

        batch_calls = [{"action": "list_skills", "args": {}} for _ in range(6)]
        result = asyncio.run(skills_tool("batch", {"batch_calls": batch_calls}, ctx=None))

        assert result.error is None
        assert active_calls["max"] <= 2
