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

from config.storage import DefaultSessionScopeResolver, InMemorySessionStorageProvider, SessionScope
from config.token import BzmToken
from models.result import BaseResult
from tests.conftest import make_ctx
from tools.async_task_manager import (
    STATUS_COMPLETED,
    STATUS_WORKING,
    TaskRecord,
    configure_task_storage,
    submit_task,
)
from tools.tools_manager import ToolsManager
import tools.async_task_manager as task_manager

_TOKEN = BzmToken("local", "secret")
_SESSION_ID = "stdio"
_STDIO_SCOPE = SessionScope(user_id="local", mcp_session_id="stdio")


def _configure():
    store = InMemorySessionStorageProvider()
    configure_task_storage(store)
    return store


def _manager(store=None):
    store = store or _configure()
    ctx = make_ctx(_TOKEN, _SESSION_ID)
    return ToolsManager(ctx, store, DefaultSessionScopeResolver())


def test_operation_name_from_manager_method():
    action_payload = {
        "manager": "ExecutionManager",
        "method": "list",
        "params": {
            "test_id": 15332595,
            "limit": 1,
            "offset": 0,
            "purpose": "diagnostics",
        },
    }

    line = ToolsManager._operation_name(action_payload)
    assert line == "execution.list"


def test_polling_message_includes_operation_task_and_batch_summary():
    store = _configure()

    async def scenario():
        record = TaskRecord(
            task_id="7k2p9m4q",
            action={
                "manager": "ExecutionManager",
                "method": "list",
                "params": {"test_id": 15332595, "limit": 1, "offset": 0},
            },
            created_at=0.0,
            last_updated_at=0.0,
            time_to_live_ms=None,
            status=STATUS_WORKING,
            status_message="Task is currently running.",
            status_info="",
            user_id="local",
            mcp_session_id="stdio",
        )
        cache = await task_manager._get_or_create_cache(_STDIO_SCOPE)
        async with cache.lock:
            cache.hydrated = True
            cache.tasks[record.task_id] = record
            await task_manager._commit_cache(cache, _STDIO_SCOPE)

        manager = _manager(store)
        message = await manager._polling_message(
            task_record=record,
            poll_count=3,
            elapsed_seconds=12,
            next_poll_seconds=1.0,
            window_seconds=30.0,
        )

        assert "Polling 7k2p9m4q[execution.list] (working) attempt=3 elapsed=12s/30s next=1s" in message
        assert "batch summary: total=1 completed=0 working=1 parking=0 failed=0" in message

    asyncio.run(scenario())


def test_tasks_list_returns_minimal_snapshot_without_action_payload():
    store = _configure()

    async def scenario():
        record = TaskRecord(
            task_id="abc123xy",
            action={
                "manager": "TestManager",
                "method": "upload_assets",
                "params": {"test_id": 1, "file_paths": ["/very/long/path"]},
            },
            created_at=0.0,
            last_updated_at=0.0,
            time_to_live_ms=None,
            status=STATUS_WORKING,
            status_message="Task is currently running.",
            status_info="",
            user_id="local",
            mcp_session_id="stdio",
        )
        cache = await task_manager._get_or_create_cache(_STDIO_SCOPE)
        async with cache.lock:
            cache.hydrated = True
            cache.tasks[record.task_id] = record
            await task_manager._commit_cache(cache, _STDIO_SCOPE)

        manager = _manager(store)
        response = await manager.tasks_list()
        assert response.result is not None
        item = response.result[0]
        assert item["task_id"] == "abc123xy"
        assert item["operation"] == "test.upload_assets"
        assert "action" not in item

    asyncio.run(scenario())


def test_tasks_status_terminal_omits_task_result_payload():
    store = _configure()

    async def scenario():
        record = TaskRecord(
            task_id="done1234",
            action={"manager": "ExecutionManager", "method": "list", "params": {"limit": 1, "offset": 0}},
            created_at=0.0,
            last_updated_at=0.0,
            time_to_live_ms=None,
            status=STATUS_COMPLETED,
            status_message="Task completed.",
            status_info="",
            result=BaseResult(result=[{"id": 1, "name": "result"}]),
            user_id="local",
            mcp_session_id="stdio",
        )
        cache = await task_manager._get_or_create_cache(_STDIO_SCOPE)
        async with cache.lock:
            cache.hydrated = True
            cache.tasks[record.task_id] = record
            await task_manager._commit_cache(cache, _STDIO_SCOPE)

        manager = _manager(store)
        response = await manager.tasks_status("done1234")
        assert response.result is not None
        item = response.result[0]
        assert item["task_id"] == "done1234"
        assert "task_result" not in item
        assert response.info is not None
        assert "Use tasks_get to retrieve task_result" in response.info[0]

    asyncio.run(scenario())


def test_tasks_get_terminal_includes_task_result_payload():
    store = _configure()

    async def scenario():
        record = TaskRecord(
            task_id="done5678",
            action={"manager": "ExecutionManager", "method": "list", "params": {"limit": 1, "offset": 0}},
            created_at=0.0,
            last_updated_at=0.0,
            time_to_live_ms=None,
            status=STATUS_COMPLETED,
            status_message="Task completed.",
            status_info="",
            result=BaseResult(result=[{"id": 2, "name": "final"}]),
            user_id="local",
            mcp_session_id="stdio",
        )
        cache = await task_manager._get_or_create_cache(_STDIO_SCOPE)
        async with cache.lock:
            cache.hydrated = True
            cache.tasks[record.task_id] = record
            await task_manager._commit_cache(cache, _STDIO_SCOPE)

        manager = _manager(store)
        response = await manager.tasks_get("done5678", remove_on_terminal=False)
        assert response.result is not None
        item = response.result[0]
        assert item["task_id"] == "done5678"
        assert item["task_result"]["result"] == [{"id": 2, "name": "final"}]

    asyncio.run(scenario())


def test_execute_with_task_management_fast_path():
    from tools.utils import execute_with_task_management

    _configure()

    async def scenario():
        async def action():
            return BaseResult(result=[{"fast": True}])

        result = await execute_with_task_management(
            action_payload={"manager": "TestManager", "method": "read"},
            coro_factory=action,
            fast_response_threshold_seconds=2.0,
            scope=_STDIO_SCOPE,
        )
        assert result.error is None
        assert result.result == [{"fast": True}]

    asyncio.run(scenario())


def test_execute_with_task_management_async_handoff():
    from tools.utils import execute_with_task_management

    store = _configure()

    async def scenario():
        async def action():
            await asyncio.sleep(0.3)
            return BaseResult(result=[{"slow": True}])

        result = await execute_with_task_management(
            action_payload={"manager": "TestManager", "method": "read"},
            coro_factory=action,
            fast_response_threshold_seconds=0.05,
            scope=_STDIO_SCOPE,
        )
        assert result.result is not None
        assert "task_id" in result.result[0]
        assert result.result[0]["status"] in {"parking", "working", "completed"}
        assert result.info is not None
        assert "tasks_status" in result.info[0]

        task_id = result.result[0]["task_id"]
        manager = _manager(store)
        for _ in range(50):
            status = await manager.tasks_status(task_id)
            if status.result and status.result[0]["status"] == STATUS_COMPLETED:
                break
            await asyncio.sleep(0.02)
        got = await manager.tasks_get(task_id, remove_on_terminal=True)
        assert got.result[0]["task_result"]["result"] == [{"slow": True}]

    asyncio.run(scenario())
