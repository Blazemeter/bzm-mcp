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
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Optional

from models.result import BaseResult
from tools.dataframe_manager import materialize_large_result_if_needed
from tools.utils import generate_simple_id, SIMPLE_ID_ALPHABET, SIMPLE_ID_LENGTH, normalize_simple_id

# Crockford-like base32 alphabet used by generate_simple_id / task ids (tests assert against this).
TASK_ID_ALPHABET = SIMPLE_ID_ALPHABET

STATUS_WORKING = "working"
STATUS_PARKING = "parking"
STATUS_INPUT_REQUIRED = "input_required"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_CANCELLED = "cancelled"

TERMINAL_STATES = {STATUS_COMPLETED, STATUS_FAILED, STATUS_CANCELLED}
ACTIVE_STATES = {STATUS_PARKING, STATUS_WORKING, STATUS_INPUT_REQUIRED}
MAX_PARALLEL_TASKS = 10

TASK_ID_MAX_ATTEMPTS = 10

logger = logging.getLogger(__name__)

STATUS_INFO = {
    STATUS_WORKING: (
        "The request is currently being processed."
    ),
    STATUS_PARKING: (
        "The request is queued and waiting for an execution slot."
    ),
    STATUS_INPUT_REQUIRED: (
        "The receiver needs input from the requestor. "
        "Use tasks_status for lightweight tracking and tasks_get to receive input requests."
    ),
    STATUS_COMPLETED: (
        "The request completed successfully and results are available."
    ),
    STATUS_FAILED: (
        "The associated request did not complete successfully."
    ),
    STATUS_CANCELLED: (
        "The request was cancelled before completion."
    ),
}

_semaphore = asyncio.Semaphore(MAX_PARALLEL_TASKS)


@dataclass
class TaskRecord:
    task_id: str
    action: Dict[str, Any]
    created_at: float
    last_updated_at: float
    time_to_live_ms: Optional[int]
    status: str
    status_message: str
    status_info: str
    result: Optional[BaseResult] = None
    asyncio_task: Optional[asyncio.Task] = None
    started_running_at: Optional[float] = None
    finished_at: Optional[float] = None

    def set_status(self, status: str, status_message: str):
        self.status = status
        self.status_message = status_message
        self.status_info = STATUS_INFO.get(status, "")
        self.last_updated_at = time.time()
        if status == STATUS_WORKING and self.started_running_at is None:
            self.started_running_at = self.last_updated_at
        if status in TERMINAL_STATES:
            self.finished_at = self.last_updated_at


_tasks: Dict[str, TaskRecord] = {}

def _to_iso(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()


def _normalize_result(result: Any) -> BaseResult:
    if isinstance(result, BaseResult):
        return result
    return BaseResult(result=[result])


def _generate_task_id() -> str:
    return generate_simple_id()


def _allocate_task_id() -> str:
    for _ in range(TASK_ID_MAX_ATTEMPTS):
        candidate = _generate_task_id()
        if candidate not in _tasks:
            return candidate

    logger.error(
        "Unable to allocate task id. attempts=%s id_length=%s alphabet=crockford32 active_pool_size=%s",
        TASK_ID_MAX_ATTEMPTS,
        SIMPLE_ID_LENGTH,
        len(_tasks),
    )
    raise RuntimeError(
        f"Unable to allocate unique {SIMPLE_ID_LENGTH}-char task id after {TASK_ID_MAX_ATTEMPTS} attempts."
    )


async def _task_runner(task_record: TaskRecord, coro_factory: Callable[[], Awaitable[Any]]):
    task_record.set_status(STATUS_PARKING, "Task is waiting for an available execution slot.")
    try:
        async with _semaphore:
            task_record.set_status(STATUS_WORKING, "Task is currently running.")
            if task_record.time_to_live_ms is None:
                action_result = await coro_factory()
            else:
                action_result = await asyncio.wait_for(coro_factory(), timeout=task_record.time_to_live_ms / 1000)
            normalized = _normalize_result(action_result)
            result_format = str(task_record.action.get("result_format", "auto")).strip().lower()
            if result_format != "raw":
                normalized = await materialize_large_result_if_needed(
                    base_result=normalized,
                    origin_manager=task_record.action.get("manager", "unknown"),
                    origin_action=task_record.action.get("method", "unknown"),
                    force=(result_format == "dataframe"),
                )
            task_record.result = normalized
            if normalized.error:
                task_record.set_status(STATUS_FAILED, f"Task finished with error: {normalized.error}")
            else:
                task_record.set_status(STATUS_COMPLETED, "Task finished successfully.")
    except asyncio.TimeoutError:
        timeout_message = (
            f"Task timed out after {task_record.time_to_live_ms} ms."
            if task_record.time_to_live_ms is not None
            else "Task timed out."
        )
        task_record.result = BaseResult(error=timeout_message)
        task_record.set_status(STATUS_CANCELLED, timeout_message)
    except asyncio.CancelledError:
        cancel_message = "Task was cancelled."
        task_record.result = BaseResult(error=cancel_message)
        task_record.set_status(STATUS_CANCELLED, cancel_message)
    except Exception as exc:
        error_message = f"Task failed with exception: {str(exc)}"
        task_record.result = BaseResult(error=error_message)
        task_record.set_status(STATUS_FAILED, error_message)


def submit_task(
        action: Dict[str, Any],
        coro_factory: Callable[[], Awaitable[Any]],
        time_to_live_ms: Optional[int] = None
) -> str:
    now = time.time()
    task_id = _allocate_task_id()
    task_record = TaskRecord(
        task_id=task_id,
        action=action,
        created_at=now,
        last_updated_at=now,
        time_to_live_ms=time_to_live_ms,
        status=STATUS_PARKING,
        status_message="Task accepted and pending scheduling.",
        status_info=STATUS_INFO[STATUS_PARKING],
    )
    async_task = asyncio.create_task(_task_runner(task_record, coro_factory))
    task_record.asyncio_task = async_task
    _tasks[task_id] = task_record
    return task_id


def get_task_record(task_id: str) -> Optional[TaskRecord]:
    return _tasks.get(normalize_simple_id(task_id))


def remove_task(task_id: str) -> bool:
    return _tasks.pop(normalize_simple_id(task_id), None) is not None


def task_snapshot(task_record: TaskRecord, include_result: bool = False) -> Dict[str, Any]:
    snapshot = {
        "task_id": task_record.task_id,
        "action": task_record.action,
        "created_at": task_record.created_at,
        "created_at_iso": _to_iso(task_record.created_at),
        "last_updated_at": task_record.last_updated_at,
        "last_updated_at_iso": _to_iso(task_record.last_updated_at),
        "time_to_live_ms": task_record.time_to_live_ms,
        "status": task_record.status,
        "status_message": task_record.status_message,
        "status_info": task_record.status_info,
        "started_running_at": task_record.started_running_at,
        "started_running_at_iso": _to_iso(task_record.started_running_at) if task_record.started_running_at else None,
        "finished_at": task_record.finished_at,
        "finished_at_iso": _to_iso(task_record.finished_at) if task_record.finished_at else None,
    }
    if include_result and task_record.result is not None:
        snapshot["task_result"] = task_record.result.model_dump()
    return snapshot


def list_tasks(status_list: Optional[list[str]] = None) -> list[TaskRecord]:
    if not status_list:
        return list(_tasks.values())
    expected = {status.lower() for status in status_list}
    return [task for task in _tasks.values() if task.status.lower() in expected]


def is_terminal_status(status: str) -> bool:
    return status in TERMINAL_STATES


def is_active_status(status: str) -> bool:
    return status in ACTIVE_STATES


def cancel_task(task_id: str) -> Optional[TaskRecord]:
    normalized_task_id = normalize_simple_id(task_id)
    task_record = _tasks.get(normalized_task_id)
    if not task_record:
        return None
    if task_record.asyncio_task and not task_record.asyncio_task.done():
        task_record.asyncio_task.cancel()
    else:
        task_record.set_status(STATUS_CANCELLED, "Task was already finished and marked as cancelled.")
        if task_record.result is None:
            task_record.result = BaseResult(error="Task was cancelled.")
    return task_record
