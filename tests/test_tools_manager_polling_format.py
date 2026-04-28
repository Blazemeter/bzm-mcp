import tools.async_task_manager as task_manager
from tools.tools_manager import ToolsManager
import asyncio
from models.result import BaseResult


def _clear_tasks():
    task_manager._tasks.clear()


def test_operation_call_line_uses_all_named_params():
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

    line = ToolsManager._operation_call_line(action_payload)
    assert line == "execution.list"


def test_polling_message_includes_operation_task_and_batch_summary():
    _clear_tasks()
    record = task_manager.TaskRecord(
        task_id="7k2p9m4q",
        action={
            "manager": "ExecutionManager",
            "method": "list",
            "params": {"test_id": 15332595, "limit": 1, "offset": 0},
        },
        created_at=0.0,
        last_updated_at=0.0,
        time_to_live_ms=None,
        status=task_manager.STATUS_WORKING,
        status_message="Task is currently running.",
        status_info="",
    )
    task_manager._tasks[record.task_id] = record

    message = ToolsManager._polling_message(
        task_record=record,
        poll_count=3,
        elapsed_seconds=12,
        next_poll_seconds=1.0,
        window_seconds=30.0,
    )

    assert "Polling 7k2p9m4q[execution.list] (working) attempt=3 elapsed=12s/30s next=1s" in message
    assert "batch summary: total=1 completed=0 working=1 parking=0 failed=0" in message


def test_tasks_list_returns_minimal_snapshot_without_action_payload():
    _clear_tasks()
    record = task_manager.TaskRecord(
        task_id="abc123xy",
        action={
            "manager": "TestManager",
            "method": "upload_assets",
            "params": {"test_id": 1, "file_paths": ["/very/long/path"]},
        },
        created_at=0.0,
        last_updated_at=0.0,
        time_to_live_ms=None,
        status=task_manager.STATUS_WORKING,
        status_message="Task is currently running.",
        status_info="",
    )
    task_manager._tasks[record.task_id] = record

    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(manager.tasks_list())
    assert response.result is not None
    item = response.result[0]
    assert item["task_id"] == "abc123xy"
    assert item["operation"] == "test.upload_assets"
    assert "action" not in item


def test_tasks_status_terminal_omits_task_result_payload():
    _clear_tasks()
    record = task_manager.TaskRecord(
        task_id="done1234",
        action={"manager": "ExecutionManager", "method": "list", "params": {"limit": 1, "offset": 0}},
        created_at=0.0,
        last_updated_at=0.0,
        time_to_live_ms=None,
        status=task_manager.STATUS_COMPLETED,
        status_message="Task completed.",
        status_info="",
        result=BaseResult(result=[{"id": 1, "name": "result"}]),
    )
    task_manager._tasks[record.task_id] = record

    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(manager.tasks_status("done1234"))
    assert response.result is not None
    item = response.result[0]
    assert item["task_id"] == "done1234"
    assert "task_result" not in item
    assert response.info is not None
    assert "Use tasks_get to retrieve task_result" in response.info[0]


def test_tasks_get_terminal_includes_task_result_payload():
    _clear_tasks()
    record = task_manager.TaskRecord(
        task_id="done5678",
        action={"manager": "ExecutionManager", "method": "list", "params": {"limit": 1, "offset": 0}},
        created_at=0.0,
        last_updated_at=0.0,
        time_to_live_ms=None,
        status=task_manager.STATUS_COMPLETED,
        status_message="Task completed.",
        status_info="",
        result=BaseResult(result=[{"id": 2, "name": "final"}]),
    )
    task_manager._tasks[record.task_id] = record

    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(manager.tasks_get("done5678", remove_on_terminal=False))
    assert response.result is not None
    item = response.result[0]
    assert item["task_id"] == "done5678"
    assert "task_result" in item
