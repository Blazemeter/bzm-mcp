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

import tools.async_task_manager as task_manager
from config.storage import (
    InMemorySessionStorageProvider,
    SessionPartitionPayload,
    SessionScope,
    StorageNotConfiguredError,
)
from models.result import BaseResult
from tools.async_task_manager import (
    STATUS_CANCELLED,
    STATUS_COMPLETED,
    STATUS_WORKING,
    configure_task_storage,
    cancel_task,
    get_task_record,
    list_tasks,
    remove_task,
    submit_task,
    task_snapshot,
)


def _run(coro):
    return asyncio.run(coro)


async def _wait_terminal(task_id: str, user_id: str, mcp_session_id: str, timeout: float = 2.0):
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        record = await get_task_record(task_id, user_id=user_id, mcp_session_id=mcp_session_id)
        if record and record.status in {"completed", "failed", "cancelled"}:
            return record
        await asyncio.sleep(0.01)
    raise AssertionError(f"Task {task_id} did not reach a terminal state")


@pytest.fixture
def memory_store():
    store = InMemorySessionStorageProvider()
    configure_task_storage(store)
    return store


class TestTaskStorageWiring:
    def test_requires_configure_before_use(self):
        task_manager._storage = None
        with pytest.raises(StorageNotConfiguredError, match="not configured"):
            _run(list_tasks(user_id="u", mcp_session_id="s"))


class TestAsyncTaskManagerMemoryStorage:
    def test_submit_lifecycle_and_persist(self, memory_store):
        async def scenario():
            async def action():
                await asyncio.sleep(0.05)
                return BaseResult(result=[{"ok": True}])

            task_id = await submit_task(
                action={"manager": "TestManager", "method": "read"},
                coro_factory=action,
                user_id="user-1",
                mcp_session_id="sess-a",
            )
            assert len(task_id) == 8
            assert all(ch in task_manager.TASK_ID_ALPHABET for ch in task_id)

            record = await _wait_terminal(task_id, "user-1", "sess-a")
            assert record.status == STATUS_COMPLETED
            assert record.result is not None
            assert record.result.result == [{"ok": True}]

            scope = SessionScope(user_id="user-1", mcp_session_id="sess-a")
            partition = await memory_store.get_partition(scope)
            assert partition is not None
            assert task_id in partition.tasks
            assert partition.tasks[task_id]["status"] == STATUS_COMPLETED

            assert await remove_task(task_id, user_id="user-1", mcp_session_id="sess-a") is True
            partition = await memory_store.get_partition(scope)
            assert partition is not None
            assert task_id not in partition.tasks

        _run(scenario())

    def test_session_isolation(self, memory_store):
        async def scenario():
            async def action():
                return BaseResult(result=[{"v": 1}])

            task_a = await submit_task(
                {"manager": "A", "method": "list"},
                action,
                user_id="user-1",
                mcp_session_id="sess-a",
            )
            task_b = await submit_task(
                {"manager": "B", "method": "list"},
                action,
                user_id="user-1",
                mcp_session_id="sess-b",
            )
            await _wait_terminal(task_a, "user-1", "sess-a")
            await _wait_terminal(task_b, "user-1", "sess-b")

            listed_a = await list_tasks(user_id="user-1", mcp_session_id="sess-a")
            listed_b = await list_tasks(user_id="user-1", mcp_session_id="sess-b")
            assert [t.task_id for t in listed_a] == [task_a]
            assert [t.task_id for t in listed_b] == [task_b]

        _run(scenario())

    def test_collision_policy_fails_after_ten_attempts(self, memory_store, monkeypatch):
        async def scenario():
            cache = await task_manager._get_or_create_cache("user-1", "sess-a")
            async with cache.lock:
                cache.hydrated = True
                cache.tasks["deadbeef"] = task_manager.TaskRecord(
                    task_id="deadbeef",
                    action={"manager": "TestManager", "method": "read"},
                    created_at=0.0,
                    last_updated_at=0.0,
                    time_to_live_ms=None,
                    status=task_manager.STATUS_PARKING,
                    status_message="seed",
                    status_info="seed",
                    user_id="user-1",
                    mcp_session_id="sess-a",
                )
                monkeypatch.setattr(task_manager, "_generate_task_id", lambda: "deadbeef")
                with pytest.raises(
                    RuntimeError,
                    match="Unable to allocate unique 8-char task id after 10 attempts.",
                ):
                    await task_manager._allocate_task_id(cache)

        _run(scenario())

    def test_task_lookup_is_case_insensitive(self, memory_store):
        async def scenario():
            now = 0.0
            cache = await task_manager._get_or_create_cache("user-1", "sess-a")
            async with cache.lock:
                cache.hydrated = True
                cache.tasks["7k2p9m4q"] = task_manager.TaskRecord(
                    task_id="7k2p9m4q",
                    action={"manager": "ExecutionManager", "method": "list"},
                    created_at=now,
                    last_updated_at=now,
                    time_to_live_ms=None,
                    status=STATUS_WORKING,
                    status_message="running",
                    status_info="running",
                    user_id="user-1",
                    mcp_session_id="sess-a",
                )
                await task_manager._persist_cache(cache, "user-1", "sess-a")

            assert await get_task_record("7K2P9M4Q", user_id="user-1", mcp_session_id="sess-a") is not None
            assert await remove_task("7K2P9M4Q", user_id="user-1", mcp_session_id="sess-a") is True
            assert await get_task_record("7k2p9m4q", user_id="user-1", mcp_session_id="sess-a") is None

        _run(scenario())

    def test_status_visible_after_cache_drop(self, memory_store):
        """Simulate another worker by dropping the in-process cache and hydrating from Storage."""
        async def scenario():
            async def action():
                await asyncio.sleep(0.05)
                return BaseResult(result=[{"ok": True}])

            task_id = await submit_task(
                {"manager": "TestManager", "method": "read"},
                action,
                user_id="user-9",
                mcp_session_id="sess-tasks",
            )
            await _wait_terminal(task_id, "user-9", "sess-tasks")

            task_manager._session_caches.clear()
            record = await get_task_record(task_id, user_id="user-9", mcp_session_id="sess-tasks")
            assert record is not None
            assert record.status == STATUS_COMPLETED
            snap = task_snapshot(record, include_result=True)
            assert snap["task_result"]["result"] == [{"ok": True}]

        _run(scenario())

    def test_submit_preserves_existing_dataframes(self, memory_store):
        async def scenario():
            scope = SessionScope(user_id="user-9", mcp_session_id="sess-tasks")
            await memory_store.put_partition(
                scope,
                SessionPartitionPayload(dataframes={"df1": {"dataframe_id": "df1", "data": []}}),
            )

            async def action():
                return BaseResult(result=[{"ok": True}])

            task_id = await submit_task(
                {"manager": "TestManager", "method": "read"},
                action,
                user_id="user-9",
                mcp_session_id="sess-tasks",
            )
            await _wait_terminal(task_id, "user-9", "sess-tasks")
            partition = await memory_store.get_partition(scope)
            assert partition is not None
            assert "df1" in partition.dataframes
            assert task_id in partition.tasks

        _run(scenario())


class TestCancelTaskSemantics:
    def test_cancel_leaves_completed_task_unchanged(self, memory_store):
        async def scenario():
            async def action():
                return BaseResult(result=[{"ok": True}])

            task_id = await submit_task(
                {"manager": "TestManager", "method": "read"},
                action,
                user_id="user-cancel",
                mcp_session_id="sess-cancel",
            )
            completed = await _wait_terminal(task_id, "user-cancel", "sess-cancel")
            assert completed.status == STATUS_COMPLETED

            after = await cancel_task(
                task_id, user_id="user-cancel", mcp_session_id="sess-cancel"
            )
            assert after is not None
            assert after.status == STATUS_COMPLETED
            assert after.result is not None
            assert after.result.result == [{"ok": True}]

            partition = await memory_store.get_partition(
                SessionScope(user_id="user-cancel", mcp_session_id="sess-cancel")
            )
            assert partition.tasks[task_id]["status"] == STATUS_COMPLETED

        _run(scenario())

    def test_cancel_without_local_handle_marks_storage_cancelled(self, memory_store):
        async def scenario():
            async def action():
                await asyncio.sleep(60)
                return BaseResult(result=[{"ok": True}])

            task_id = await submit_task(
                {"manager": "TestManager", "method": "read"},
                action,
                user_id="user-affinity",
                mcp_session_id="sess-affinity",
            )
            # Wait until working, then drop local handle (simulate other worker hydrate).
            for _ in range(100):
                record = await get_task_record(
                    task_id, user_id="user-affinity", mcp_session_id="sess-affinity"
                )
                if record and record.status == STATUS_WORKING:
                    break
                await asyncio.sleep(0.01)
            else:
                raise AssertionError("task did not start working")

            record.asyncio_task = None
            cancelled = await cancel_task(
                task_id, user_id="user-affinity", mcp_session_id="sess-affinity"
            )
            assert cancelled is not None
            assert cancelled.status == STATUS_CANCELLED
            assert "no local" in (cancelled.status_message or "").lower()

        _run(scenario())

    def test_cancel_local_running_task(self, memory_store):
        async def scenario():
            started = asyncio.Event()

            async def action():
                started.set()
                await asyncio.sleep(60)
                return BaseResult(result=[{"ok": True}])

            task_id = await submit_task(
                {"manager": "TestManager", "method": "read"},
                action,
                user_id="user-local-cancel",
                mcp_session_id="sess-local-cancel",
            )
            await asyncio.wait_for(started.wait(), timeout=2.0)
            record = await get_task_record(
                task_id, user_id="user-local-cancel", mcp_session_id="sess-local-cancel"
            )
            assert record is not None
            assert record.asyncio_task is not None
            assert not record.asyncio_task.done()

            await cancel_task(
                task_id,
                user_id="user-local-cancel",
                mcp_session_id="sess-local-cancel",
            )
            terminal = await _wait_terminal(
                task_id, "user-local-cancel", "sess-local-cancel", timeout=2.0
            )
            assert terminal.status == STATUS_CANCELLED

        _run(scenario())
