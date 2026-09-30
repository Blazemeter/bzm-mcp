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

from config.cache import CacheScope
from config.token import BzmToken
from models.manager import Manager
from models.result import BaseResult
from tests.conftest import make_ctx
from tools.utils import run_as_task, set_result_debug_enabled, tool_result, ttl_cache_method


def _manager(cls, user_id="user-1", session_id="sess-a"):
    token = BzmToken(user_id, "secret") if user_id else None
    ctx = make_ctx(token, session_id) if token else None
    return cls(ctx)


class CountingManager(Manager):
    calls = 0

    @ttl_cache_method(ttl_seconds=30)
    async def read(self, item_id: int) -> BaseResult:
        CountingManager.calls += 1
        return BaseResult(result=[{"item_id": item_id, "call": CountingManager.calls}])

    @ttl_cache_method(ttl_seconds=30)
    async def failing(self) -> BaseResult:
        CountingManager.calls += 1
        return BaseResult(error="upstream failed")

    @ttl_cache_method(ttl_seconds=30, scope=CacheScope.GLOBAL)
    async def static_content(self) -> BaseResult:
        CountingManager.calls += 1
        return BaseResult(result=["static"])

    @ttl_cache_method(ttl_seconds=30)
    async def slow_read(self) -> BaseResult:
        CountingManager.calls += 1
        await asyncio.sleep(0.02)
        return BaseResult(result=["slow"])

    @ttl_cache_method(ttl_seconds=30)
    async def dataframe_reference(self) -> BaseResult:
        CountingManager.calls += 1
        return BaseResult(result=[{"stored_as_dataframe": True, "dataframe_id": "df1"}])


class TaskManager(Manager):
    calls = 0

    @ttl_cache_method(ttl_seconds=30)
    @run_as_task(fast_response_threshold_seconds=0.01)
    async def long_read(self) -> BaseResult:
        TaskManager.calls += 1
        await asyncio.sleep(0.1)
        return BaseResult(result=["done"])

    @ttl_cache_method(ttl_seconds=30)
    @run_as_task()
    async def fast_read(self) -> BaseResult:
        TaskManager.calls += 1
        return BaseResult(result=["fast"])


def setup_function():
    CountingManager.calls = 0
    TaskManager.calls = 0


def test_reuses_successful_result_for_the_same_user():
    async def scenario():
        manager = _manager(CountingManager)
        first = await manager.read(1)
        second = await manager.read(1)
        other_args = await manager.read(2)
        assert first.result == second.result
        assert other_args.result[0]["item_id"] == 2
        assert CountingManager.calls == 2

    asyncio.run(scenario())


def test_entries_are_never_shared_across_users():
    async def scenario():
        await _manager(CountingManager, user_id="user-1").read(1)
        result = await _manager(CountingManager, user_id="user-2").read(1)
        assert CountingManager.calls == 2
        assert result.result[0]["call"] == 2

    asyncio.run(scenario())


def test_user_scope_is_bypassed_without_a_user_in_context():
    async def scenario():
        manager = _manager(CountingManager, user_id=None)
        await manager.read(1)
        await manager.read(1)
        assert CountingManager.calls == 2

    asyncio.run(scenario())


def test_same_user_shares_plain_results_across_sessions():
    async def scenario():
        await _manager(CountingManager, session_id="sess-a").read(1)
        await _manager(CountingManager, session_id="sess-b").read(1)
        assert CountingManager.calls == 1

    asyncio.run(scenario())


def test_errors_are_not_cached():
    async def scenario():
        manager = _manager(CountingManager)
        await manager.failing()
        await manager.failing()
        assert CountingManager.calls == 2

    asyncio.run(scenario())


def test_global_scope_is_shared_across_users():
    async def scenario():
        await _manager(CountingManager, user_id="user-1").static_content()
        await _manager(CountingManager, user_id="user-2").static_content()
        await _manager(CountingManager, user_id=None).static_content()
        assert CountingManager.calls == 1

    asyncio.run(scenario())


def test_concurrent_calls_share_one_upstream_call():
    async def scenario():
        manager = _manager(CountingManager)
        results = await asyncio.gather(*(manager.slow_read() for _ in range(5)))
        assert CountingManager.calls == 1
        assert all(result.result == ["slow"] for result in results)

    asyncio.run(scenario())


def test_session_dataframe_reference_is_not_served_to_another_session():
    async def scenario():
        await _manager(CountingManager, session_id="sess-a").dataframe_reference()
        await _manager(CountingManager, session_id="sess-a").dataframe_reference()
        assert CountingManager.calls == 1
        await _manager(CountingManager, session_id="sess-b").dataframe_reference()
        assert CountingManager.calls == 2

    asyncio.run(scenario())


def test_hit_skips_the_task_for_fast_results(isolated_cache):
    async def scenario():
        manager = _manager(TaskManager)
        first = await manager.fast_read()
        second = await manager.fast_read()
        assert first.result == second.result == ["fast"]
        assert TaskManager.calls == 1

    asyncio.run(scenario())


def test_running_task_snapshot_is_cached_and_dropped_when_the_task_finishes(isolated_cache):
    async def scenario():
        manager = _manager(TaskManager)
        first = await manager.long_read()
        snapshot = first.result[0]
        assert snapshot["status"] in {"parking", "working"}

        # Burst while the task runs: same snapshot, no new upstream call or task.
        second = await manager.long_read()
        assert second.result[0]["task_id"] == snapshot["task_id"]
        assert len(isolated_cache) == 1

        await asyncio.sleep(0.25)  # the task finishes and invalidates the snapshot
        assert len(isolated_cache) == 0
        assert TaskManager.calls == 1

    asyncio.run(scenario())


def test_running_task_snapshot_is_not_served_to_another_session(isolated_cache):
    async def scenario():
        first = await _manager(TaskManager, session_id="sess-a").long_read()
        other = await _manager(TaskManager, session_id="sess-b").long_read()
        assert other.result[0]["task_id"] != first.result[0]["task_id"]
        await asyncio.sleep(0.25)
        assert TaskManager.calls == 2

    asyncio.run(scenario())


def test_debug_reports_cache_hits_and_misses():
    @tool_result(disable_materialization=True)
    async def handler(arguments=None, ctx=None):
        manager = _manager(CountingManager)
        await manager.read(1)
        return await manager.read(1)

    set_result_debug_enabled(True)
    try:
        result = asyncio.run(handler({"action": "read", "args": {}}, ctx=None))
    finally:
        set_result_debug_enabled(False)
    assert result.structuredContent["debug"]["cache"] == {"hits": 1, "misses": 1, "shared_wait_ms": 0}


async def _inline(call):
    """Run ``call`` the way a nested bridge validation runs inside a tool/task."""
    from tools.utils.common import _task_management_enabled

    token = _task_management_enabled.set(True)
    try:
        return await call()
    finally:
        _task_management_enabled.reset(token)


def test_inline_call_never_receives_a_top_level_task_snapshot(isolated_cache):
    async def scenario():
        manager = _manager(TaskManager)
        snapshot = await manager.long_read()
        assert "task_id" in snapshot.result[0]

        nested = await _inline(manager.long_read)
        assert nested.result == ["done"]
        await asyncio.sleep(0.25)
        assert TaskManager.calls == 2

    asyncio.run(scenario())


def test_inline_call_never_receives_a_dataframe_reference_from_the_same_session():
    class DataframeThenModel(Manager):
        @ttl_cache_method(ttl_seconds=30)
        async def read(self) -> BaseResult:
            from tools.utils.common import _task_management_enabled

            CountingManager.calls += 1
            if _task_management_enabled.get():
                return BaseResult(result=[{"project_id": 7}])
            return BaseResult(result=[{"stored_as_dataframe": True, "dataframe_id": "df1"}])

    async def scenario():
        manager = _manager(DataframeThenModel)
        await manager.read()
        nested = await _inline(manager.read)
        assert nested.result == [{"project_id": 7}]
        assert CountingManager.calls == 2

    asyncio.run(scenario())


def test_cache_store_failure_does_not_fail_a_successful_call(monkeypatch, isolated_cache):
    import tools.async_task_manager as async_task_manager

    async def storage_down(task_id, scope, callback):
        raise RuntimeError("storage unavailable")

    monkeypatch.setattr(async_task_manager, "add_task_terminal_callback", storage_down)

    async def scenario():
        result = await _manager(TaskManager).long_read()
        assert result.error is None
        assert "task_id" in result.result[0]
        # Without its invalidation hook the snapshot must not stay cached.
        assert len(isolated_cache) == 0
        await asyncio.sleep(0.25)

    asyncio.run(scenario())


def test_cache_hits_do_not_replay_per_call_debug_or_timing():
    class DebugManager(Manager):
        @ttl_cache_method(ttl_seconds=30)
        async def read(self) -> BaseResult:
            CountingManager.calls += 1
            return BaseResult(
                result=["data"],
                debug={"task": {"run_ms": 790}},
                tool_call_duration_ms=800,
            )

    async def scenario():
        manager = _manager(DebugManager)
        first = await manager.read()
        hit = await manager.read()
        assert first.debug == {"task": {"run_ms": 790}}
        assert hit.result == ["data"]
        assert hit.debug is None
        assert hit.tool_call_duration_ms is None
        assert CountingManager.calls == 1

    asyncio.run(scenario())


def test_finished_task_does_not_evict_a_newer_value_for_the_same_key(isolated_cache):
    async def scenario():
        await _manager(TaskManager).long_read()
        [key] = list(isolated_cache._data)
        # Another session stored a fresher value for the same key meanwhile.
        await isolated_cache.set(key, BaseResult(result=["newer"]), 30)
        await asyncio.sleep(0.25)  # the first task finishes and runs its invalidation
        assert (await isolated_cache.get(key)).value.result == ["newer"]

    asyncio.run(scenario())


def test_register_tools_wires_the_runtime_cache():
    from config.cache import InMemoryTTLCache, get_cache
    from config.runtime import build_runtime
    from dataclasses import replace
    from server import register_tools

    class FakeMcp:
        def tool(self, name, description):
            return lambda func: func

        def resource(self, pattern):
            return lambda func: func

    runtime_cache = InMemoryTTLCache(sweep_interval_seconds=0)
    runtime = replace(build_runtime("stdio"), cache=runtime_cache)
    register_tools(FakeMcp(), runtime)
    assert get_cache() is runtime_cache
