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
from types import SimpleNamespace

from models.result import BaseResult
from tools import account_manager, project_manager
from tools.account_manager import AccountManager
from tools.project_manager import ProjectManager


class TestHierarchy:
    def test_account_read_returns_result(self, monkeypatch):
        async def fake_api_request(*args, **kwargs):
            return BaseResult(result=[SimpleNamespace(account_id=123, account_name="Test")])

        monkeypatch.setattr(account_manager, "api_request", fake_api_request)
        manager = AccountManager(token=None, ctx=None)

        result = asyncio.run(manager.read(123))

        assert result.error is None
        assert result.result[0].account_id == 123

    def test_project_read_sets_tests_count(self, monkeypatch):
        async def fake_api_request(*args, **kwargs):
            return BaseResult(result=[SimpleNamespace(workspace_id=11, tests_count=None)])

        async def fake_count_project_tests(*args, **kwargs):
            return 7

        monkeypatch.setattr(project_manager, "api_request", fake_api_request)
        monkeypatch.setattr(project_manager.bridge, "count_project_tests", fake_count_project_tests)
        manager = ProjectManager(token=None, ctx=None)

        result = asyncio.run(manager.read(200))

        assert result.error is None
        assert result.result[0].tests_count == 7
