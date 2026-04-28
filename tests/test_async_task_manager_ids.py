import asyncio

import pytest

import tools.async_task_manager as task_manager
from models.result import BaseResult


def _clear_tasks():
    task_manager._tasks.clear()


def test_submit_task_uses_crockford_base32_id():
    _clear_tasks()

    async def scenario():
        async def action():
            return BaseResult(result=[{"ok": True}])

        task_id = task_manager.submit_task(
            action={"manager": "TestManager", "method": "read"},
            coro_factory=action,
        )
        record = task_manager.get_task_record(task_id)
        assert record is not None
        assert len(task_id) == 8
        assert all(ch in task_manager.TASK_ID_ALPHABET for ch in task_id)

        while True:
            record = task_manager.get_task_record(task_id)
            if record and record.status in {"completed", "failed", "cancelled"}:
                break
            await asyncio.sleep(0.01)

        assert task_manager.remove_task(task_id) is True

    asyncio.run(scenario())


def test_collision_policy_fails_after_ten_attempts(monkeypatch):
    _clear_tasks()
    task_manager._tasks["deadbeef"] = task_manager.TaskRecord(
        task_id="deadbeef",
        action={"manager": "TestManager", "method": "read"},
        created_at=0.0,
        last_updated_at=0.0,
        time_to_live_ms=None,
        status=task_manager.STATUS_PARKING,
        status_message="seed",
        status_info="seed",
    )

    monkeypatch.setattr(task_manager, "_generate_task_id", lambda: "deadbeef")

    with pytest.raises(RuntimeError, match="Unable to allocate unique 8-char task id after 10 attempts."):
        task_manager._allocate_task_id()


def test_task_lookup_is_case_insensitive():
    _clear_tasks()
    now = 0.0
    task_manager._tasks["7k2p9m4q"] = task_manager.TaskRecord(
        task_id="7k2p9m4q",
        action={"manager": "ExecutionManager", "method": "list"},
        created_at=now,
        last_updated_at=now,
        time_to_live_ms=None,
        status=task_manager.STATUS_WORKING,
        status_message="running",
        status_info="running",
    )

    assert task_manager.get_task_record("7K2P9M4Q") is not None
    assert task_manager.remove_task("7K2P9M4Q") is True
    assert task_manager.get_task_record("7k2p9m4q") is None
