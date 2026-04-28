import asyncio

from models.result import BaseResult
from tools import utils


class _Token:
    def __init__(self, token_id: str):
        self.id = token_id


class _DummyManager:
    def __init__(self):
        self.token = _Token("token-a")
        self.calls = 0

    @utils.ttl_cache_method(ttl_seconds=30)
    async def read_ok(self, entity_id: int) -> BaseResult:
        self.calls += 1
        await asyncio.sleep(0.01)
        return BaseResult(result=[{"entity_id": entity_id, "call": self.calls}])

    @utils.ttl_cache_method(ttl_seconds=30)
    async def read_error(self) -> BaseResult:
        self.calls += 1
        await asyncio.sleep(0.01)
        return BaseResult(error="boom")


class _DummyTaskManager:
    def __init__(self):
        self.token = _Token("token-b")

    @utils.run_as_task(fast_response_threshold_seconds=0.2)
    async def read_ok(self) -> BaseResult:
        await asyncio.sleep(0.01)
        return BaseResult(result=[{"ok": True}])



def _clear_method_cache():
    utils._method_cache.clear()
    utils._method_cache_inflight.clear()


def test_ttl_cache_reuses_successful_read_result():
    _clear_method_cache()
    manager = _DummyManager()

    async def scenario():
        first = await manager.read_ok(10)
        second = await manager.read_ok(10)
        return first, second

    first, second = asyncio.run(scenario())
    assert manager.calls == 1
    assert first.result == second.result


def test_ttl_cache_does_not_cache_errors():
    _clear_method_cache()
    manager = _DummyManager()

    async def scenario():
        first = await manager.read_error()
        second = await manager.read_error()
        return first, second

    first, second = asyncio.run(scenario())
    assert first.error == "boom"
    assert second.error == "boom"
    assert manager.calls == 2


def test_ttl_cache_single_flight_for_concurrent_calls():
    _clear_method_cache()
    manager = _DummyManager()

    async def scenario():
        results = await asyncio.gather(
            manager.read_ok(99),
            manager.read_ok(99),
            manager.read_ok(99),
        )
        return results

    results = asyncio.run(scenario())
    assert manager.calls == 1
    assert all(result.result == results[0].result for result in results)


def test_tool_result_adds_tool_call_timing_fields():
    @utils.tool_result()
    async def tool_handler(action: str) -> BaseResult:
        await asyncio.sleep(0.01)
        return BaseResult(result=[{"ok": True}])

    previous = utils.is_result_debug_enabled()
    utils.set_result_debug_enabled(True)
    try:
        response = asyncio.run(tool_handler("read"))
        assert response.tool_call_started_at is not None
        assert response.tool_call_finished_at is not None
        assert isinstance(response.tool_call_duration_ms, int)
        assert response.tool_call_duration_ms >= 0
        assert response.debug is not None
        assert response.debug.get("network", {}).get("http_calls") == 0
        assert response.debug.get("network", {}).get("http_total_ms") == 0
    finally:
        utils.set_result_debug_enabled(previous)


def test_tool_result_adds_network_debug_metrics():
    @utils.tool_result()
    async def tool_handler(action: str) -> BaseResult:
        utils._accumulate_network_debug(120)
        utils._accumulate_network_debug(80)
        return BaseResult(result=[{"ok": True}])

    previous = utils.is_result_debug_enabled()
    utils.set_result_debug_enabled(True)
    try:
        response = asyncio.run(tool_handler("read"))
        assert response.debug is not None
        network = response.debug.get("network", {})
        assert network.get("http_calls") == 2
        assert network.get("http_total_ms") == 200
    finally:
        utils.set_result_debug_enabled(previous)


def test_tool_result_debug_disabled_by_default():
    @utils.tool_result()
    async def tool_handler(action: str) -> BaseResult:
        return BaseResult(result=[{"ok": True}])

    previous = utils.is_result_debug_enabled()
    utils.set_result_debug_enabled(False)
    try:
        response = asyncio.run(tool_handler("read"))
        assert response.tool_call_started_at is not None
        assert response.tool_call_finished_at is not None
        assert isinstance(response.tool_call_duration_ms, int)
        assert response.tool_call_duration_ms >= 0
        assert response.debug is None
    finally:
        utils.set_result_debug_enabled(previous)


def test_tool_result_timing_always_present_with_run_as_task_when_debug_disabled():
    @utils.tool_result()
    async def tool_handler(action: str, args: dict) -> BaseResult:
        manager = _DummyTaskManager()
        return await manager.read_ok()

    previous = utils.is_result_debug_enabled()
    utils.set_result_debug_enabled(False)
    try:
        response = asyncio.run(tool_handler("read", {"result_format": "raw"}))
        assert response.error is None
        assert response.tool_call_started_at is not None
        assert response.tool_call_finished_at is not None
        assert isinstance(response.tool_call_duration_ms, int)
        assert response.tool_call_duration_ms >= 0
        assert response.debug is None
    finally:
        utils.set_result_debug_enabled(previous)
