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
from tools import account_manager, project_manager, workspace_manager, test_manager, execution_manager
from tools.account_manager import AccountManager
from tools.execution_manager import ExecutionManager
from tools.project_manager import ProjectManager
from tools.test_manager import TestManager
from tools.utils import register_confirm_mode, ConfirmMode
from tools.workspace_manager import WorkspaceManager


class TestHierarchyAndConsent:
    def test_account_read_blocks_when_ai_consent_is_false(self, monkeypatch):
        async def fake_api_request(*args, **kwargs):
            return BaseResult(result=[SimpleNamespace(ai_consent=False)])

        monkeypatch.setattr(account_manager, "api_request", fake_api_request)
        manager = AccountManager(token=None, ctx=None)

        result = asyncio.run(manager.read(123))

        assert result.error is not None
        assert "does not have AI consent" in result.error

    def test_workspace_read_propagates_account_validation_error(self, monkeypatch):
        async def fake_api_request(*args, **kwargs):
            return BaseResult(result=[SimpleNamespace(account_id=99)])

        async def fake_read_account(*args, **kwargs):
            return BaseResult(error="Account validation failed")

        monkeypatch.setattr(workspace_manager, "api_request", fake_api_request)
        monkeypatch.setattr(workspace_manager.bridge, "read_account", fake_read_account)
        manager = WorkspaceManager(token=None, ctx=None)

        result = asyncio.run(manager.read(55))

        assert result.error == "Account validation failed"

    def test_project_read_sets_tests_count_after_hierarchy_validation(self, monkeypatch):
        async def fake_api_request(*args, **kwargs):
            return BaseResult(result=[SimpleNamespace(workspace_id=11, tests_count=None)])

        async def fake_read_workspace(*args, **kwargs):
            return BaseResult(result=["ok"])

        async def fake_count_project_tests(*args, **kwargs):
            return 7

        monkeypatch.setattr(project_manager, "api_request", fake_api_request)
        monkeypatch.setattr(project_manager.bridge, "read_workspace", fake_read_workspace)
        monkeypatch.setattr(project_manager.bridge, "count_project_tests", fake_count_project_tests)
        manager = ProjectManager(token=None, ctx=None)

        result = asyncio.run(manager.read(200))

        assert result.error is None
        assert result.result[0].tests_count == 7

    def test_test_read_propagates_project_validation_error(self, monkeypatch):
        async def fake_api_request(*args, **kwargs):
            return BaseResult(result=[SimpleNamespace(project_id=777)])

        async def fake_read_project(*args, **kwargs):
            return BaseResult(error="Project validation failed")

        monkeypatch.setattr(test_manager, "api_request", fake_api_request)
        monkeypatch.setattr(test_manager.bridge, "read_project", fake_read_project)
        manager = TestManager(token=None, ctx=None)

        result = asyncio.run(manager.read(50))

        assert result.error == "Project validation failed"

    def test_execution_start_stops_when_test_validation_fails(self, monkeypatch):
        register_confirm_mode(ConfirmMode.DISABLE)
        called = {"api_request": False}

        async def fake_read_test(*args, **kwargs):
            return BaseResult(error="Test validation failed")

        async def fake_api_request(*args, **kwargs):
            called["api_request"] = True
            return BaseResult(result=["should not run"])

        monkeypatch.setattr(execution_manager.bridge, "read_test", fake_read_test)
        monkeypatch.setattr(execution_manager, "api_request", fake_api_request)
        manager = ExecutionManager(token=None, ctx=None)

        result = asyncio.run(manager.start(42))

        assert result.error == "Test validation failed"
        assert called["api_request"] is False

    def test_execution_read_propagates_project_validation_error_and_skips_status(self, monkeypatch):
        async def fake_api_request(*args, **kwargs):
            return BaseResult(result=[SimpleNamespace(project_id=456, execution_status_detailed=None)])

        async def fake_read_project(*args, **kwargs):
            return BaseResult(error="Project blocked")

        async def fake_fetch_execution_status(*args, **kwargs):  # pragma: no cover
            return BaseResult(result=["status should not be called"])

        monkeypatch.setattr(execution_manager, "api_request", fake_api_request)
        monkeypatch.setattr(execution_manager.bridge, "read_project", fake_read_project)
        monkeypatch.setattr(ExecutionManager, "_fetch_execution_status", fake_fetch_execution_status)
        manager = ExecutionManager(token=None, ctx=None)

        result = asyncio.run(manager.read(909))

        assert result.error == "Project blocked"
