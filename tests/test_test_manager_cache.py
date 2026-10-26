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

import pytest

from config.auth import BZM_USER_CONFIG_STATE_ATTR
from config.token import BzmToken
from models.performance_test import PerformanceTestObject
from models.result import BaseResult
from tests.conftest import make_ctx
from tools import test_manager as test_manager_module
from tools.test_manager import TestManager


class FakeTestsApi:
    """BlazeMeter /tests/{id} stand-in: GET returns the stored test, PATCH replaces the fields sent."""

    def __init__(self):
        self.exists = True
        self.tests_in_project = 1
        self.override_executions = []
        self.configuration = {}
        self.gets = 0

    async def api_request(self, token, method, endpoint, result_formatter=None, json=None, **kwargs):
        if method == "GET":
            self.gets += 1
            if not self.exists:
                return BaseResult(error="Test not found")
            return BaseResult(result=[SimpleNamespace(
                project_id=1,
                override_executions=[dict(override) for override in self.override_executions],
                configuration=dict(self.configuration),
            )])
        if method == "PATCH":
            if "overrideExecutions" in json:
                self.override_executions = json["overrideExecutions"] or []
            if "configuration" in json:
                self.configuration = json["configuration"]
            return BaseResult(result=[{"ok": True}])
        if method == "POST":
            self.tests_in_project += 1
            return BaseResult(result=[{"ok": True}])
        if method == "DELETE":
            self.exists = False
            self.tests_in_project -= 1
            return BaseResult(result=[{"ok": True}])
        raise AssertionError(f"unexpected {method}")


@pytest.fixture
def tests_api(monkeypatch):
    api = FakeTestsApi()
    monkeypatch.setattr(test_manager_module, "api_request", api.api_request)

    async def read_project(token, ctx, project_id):
        return BaseResult(result=[{"id": project_id}])

    monkeypatch.setattr(test_manager_module.bridge, "read_project", read_project)
    return api


def _manager():
    ctx = make_ctx(BzmToken("user-1", "secret"), "sess-a")
    # The fake ctx cannot elicit: run writes without the delete confirmation prompt.
    getattr(ctx.request_context.request.state, BZM_USER_CONFIG_STATE_ATTR)["confirmation_mode"] = "NONE"
    return TestManager(ctx)


def test_second_configure_keeps_the_first_change(tests_api):
    async def scenario():
        manager = _manager()
        await manager.configure(PerformanceTestObject({"test_id": 42, "concurrency": 50}))
        await manager.configure(PerformanceTestObject({"test_id": 42, "ramp-up": "5m"}))

    asyncio.run(scenario())
    assert tests_api.override_executions == [{"concurrency": 50, "rampUp": "5m"}]


def test_second_failure_criteria_update_keeps_the_first_change(tests_api):
    async def scenario():
        manager = _manager()
        await manager.configure_failure_criteria(
            {"test_id": 42, "enabled": True, "rules": [], "ignore_rampup": True}
        )
        await manager.configure_failure_criteria({"test_id": 42, "enabled": True, "rules": []})

    asyncio.run(scenario())
    assert tests_api.configuration["plugins"]["thresholds"]["ignoreRampup"] is True


def test_read_after_configure_sees_the_change(tests_api):
    async def scenario():
        manager = _manager()
        await manager.read(42)
        await manager.configure(PerformanceTestObject({"test_id": 42, "concurrency": 50}))
        return await manager.read(42)

    after = asyncio.run(scenario())
    assert after.result[0].override_executions == [{"concurrency": 50}]


def test_read_after_delete_does_not_return_the_deleted_test(tests_api):
    async def scenario():
        manager = _manager()
        await manager.read(42)
        await manager.delete(42)
        return await manager.read(42)

    after = asyncio.run(scenario())
    assert after.error == "Test not found"


def test_reads_without_writes_are_still_cached(tests_api):
    async def scenario():
        manager = _manager()
        await manager.read(42)
        await manager.read(42)

    asyncio.run(scenario())
    assert tests_api.gets == 1


@pytest.fixture
def project_reads(monkeypatch, tests_api):
    """Real (cached) ProjectManager.read over a fake API whose tests_count follows tests_api."""
    from tools import project_manager as project_manager_module

    calls = {"count": 0}

    async def api_request(token, method, endpoint, result_formatter=None, **kwargs):
        calls["count"] += 1
        return BaseResult(result=[SimpleNamespace(project_id=1, workspace_id=1, tests_count=0)])

    async def read_workspace(token, ctx, workspace_id):
        return BaseResult(result=[{"id": workspace_id}])

    async def count_project_tests(token, ctx, project_id):
        return tests_api.tests_in_project

    monkeypatch.setattr(project_manager_module, "api_request", api_request)
    monkeypatch.setattr(project_manager_module.bridge, "read_workspace", read_workspace)
    monkeypatch.setattr(project_manager_module.bridge, "count_project_tests", count_project_tests)
    return calls


def _project_manager():
    from tools.project_manager import ProjectManager

    return ProjectManager(make_ctx(BzmToken("user-1", "secret"), "sess-a"))


def test_project_tests_count_follows_a_created_test(tests_api, project_reads):
    async def scenario():
        before = await _project_manager().read(1)
        await _manager().create("new test", 1)
        after = await _project_manager().read(1)
        return before.result[0].tests_count, after.result[0].tests_count

    assert asyncio.run(scenario()) == (1, 2)


def test_project_tests_count_follows_a_deleted_test(tests_api, project_reads):
    async def scenario():
        before = await _project_manager().read(1)
        await _manager().delete(42)
        after = await _project_manager().read(1)
        return before.result[0].tests_count, after.result[0].tests_count

    assert asyncio.run(scenario()) == (1, 0)


def test_project_reads_without_test_changes_are_still_cached(tests_api, project_reads):
    async def scenario():
        await _project_manager().read(1)
        await _project_manager().read(1)

    asyncio.run(scenario())
    assert project_reads["count"] == 1


def test_read_after_upload_sees_the_new_main_script(monkeypatch, tests_api):
    class FakeUploader:
        """Stands in for the disk upload: sets the main script like the real PATCH does."""

        def __init__(self, file_access, scope_resolver):
            pass

        async def upload(self, token, ctx, test_id, file_paths, main_script, read_test):
            tests_api.configuration = {"filename": main_script, "scriptType": "jmeter"}
            return BaseResult(result=[{"uploaded": file_paths}])

    monkeypatch.setattr(test_manager_module, "StdioAssetUploader", FakeUploader)

    async def scenario():
        manager = _manager()
        await manager.read(42)
        await manager.upload_assets(42, ["plan.jmx"], "plan.jmx")
        return await manager.read(42)

    after = asyncio.run(scenario())
    assert after.result[0].configuration["filename"] == "plan.jmx"
