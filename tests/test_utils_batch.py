import asyncio

from models.result import BaseResult
from tools.dataframe_manager import clear_dataframes, list_dataframes_metadata
from tools.utils import execute_batch_calls, process_batch_sub_action
from tools import utils


def test_execute_batch_calls_requires_non_empty_list():
    async def process_call(call):
        return BaseResult(result=[call])

    response = asyncio.run(execute_batch_calls({}, process_call))
    assert response.error == "batch_calls must be a non-empty list of dicts with 'action' and 'args'"


def test_execute_batch_calls_collects_results_and_exceptions():
    async def process_call(call):
        if call.get("action") == "boom":
            raise RuntimeError("failure")
        return BaseResult(result=[call.get("action")])

    response = asyncio.run(
        execute_batch_calls(
            [{"action": "ok"}, {"action": "boom"}],
            process_call,
        )
    )

    assert response.result is not None
    assert isinstance(response.result[0], BaseResult)
    assert response.result[0].result == ["ok"]
    assert isinstance(response.result[1], BaseResult)
    assert response.result[1].error == "Unhandled exception: failure"


def test_execute_batch_calls_respects_max_concurrency_kwarg():
    active = {"current": 0, "max": 0}

    async def process_call(call):
        active["current"] += 1
        active["max"] = max(active["max"], active["current"])
        try:
            await asyncio.sleep(0.02)
            return BaseResult(result=[call])
        finally:
            active["current"] -= 1

    response = asyncio.run(
        execute_batch_calls(
            [{"action": str(i)} for i in range(6)],
            process_call,
            max_concurrency=2,
        )
    )
    assert response.error is None
    assert active["max"] <= 2


def test_process_batch_sub_action_wraps_sub_action_exception():
    async def dispatch_sub_action(sub_action, sub_args):
        raise RuntimeError("boom")

    response = asyncio.run(
        process_batch_sub_action(
            {"action": "read_skill", "args": {"skill_name": "x"}},
            dispatch_sub_action,
            "support msg",
        )
    )
    assert isinstance(response, BaseResult)
    assert response.error is not None
    assert "Error in sub-action read_skill:" in response.error


def test_process_batch_sub_action_forces_task_mode_for_sub_actions():
    class _Dummy:
        @utils.run_as_task()
        async def read(self) -> BaseResult:
            await asyncio.sleep(0.01)
            return BaseResult(result=[{"ok": True}])

    async def dispatch_sub_action(sub_action, sub_args):
        manager = _Dummy()
        return await manager.read()

    response = asyncio.run(
        process_batch_sub_action(
            {"action": "read", "args": {}},
            dispatch_sub_action,
        )
    )

    assert isinstance(response, BaseResult)
    assert response.result is not None
    assert isinstance(response.result[0], dict)
    assert "task_id" in response.result[0]
    assert response.info is not None
    assert "Long-running operation accepted" in response.info[0]


def test_tool_result_batch_never_materializes_dataframe_even_when_requested():
    async def _run():
        await clear_dataframes()

        @utils.tool_result(excluded_actions={"batch"})
        async def handler(action: str, args: dict) -> BaseResult:
            return BaseResult(result=[{"payload": "x" * 9000}])

        response = await handler("batch", {"result_format": "dataframe"})
        metadata = await list_dataframes_metadata()
        return response, metadata

    response, metadata = asyncio.run(_run())
    assert response.error is None
    assert response.result is not None
    assert response.result[0].get("stored_as_dataframe") is not True
    assert metadata == []
