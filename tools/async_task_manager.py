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

from __future__ import annotations

import asyncio
import copy
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set

from config.storage import (
    SessionPartitionPayload,
    SessionScope,
    SessionStoragePort,
    StorageNotConfiguredError,
    resolve_session_scope,
)
from models.result import BaseResult
from tools.dataframe_manager import finalize_tool_result
from tools.utils import (
    SIMPLE_ID_ALPHABET,
    SIMPLE_ID_LENGTH,
    TOOLS_ACTIONS_SKIP_AUTO_DATAFRAME,
    generate_simple_id,
    normalize_simple_id,
)

# Match DefaultSessionScopeResolver fallbacks when token/ctx are absent.
DEFAULT_USER_ID = "anonymous"
DEFAULT_SESSION_ID = "default"
DEFAULT_SCOPE = SessionScope(user_id=DEFAULT_USER_ID, mcp_session_id=DEFAULT_SESSION_ID)

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
_MAX_SESSION_CACHES = 256

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

_storage: Optional[SessionStoragePort] = None
_registry_lock = asyncio.Lock()
_session_caches: OrderedDict[tuple[str, str], "_SessionTaskCache"] = OrderedDict()


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
    user_id: str = DEFAULT_USER_ID
    mcp_session_id: str = DEFAULT_SESSION_ID

    def set_status(self, status: str, status_message: str):
        self.status = status
        self.status_message = status_message
        self.status_info = STATUS_INFO.get(status, "")
        self.last_updated_at = time.time()
        if status == STATUS_WORKING and self.started_running_at is None:
            self.started_running_at = self.last_updated_at
        if status in TERMINAL_STATES:
            self.finished_at = self.last_updated_at

    def scope(self) -> SessionScope:
        return SessionScope(user_id=self.user_id, mcp_session_id=self.mcp_session_id)


@dataclass
class _SessionTaskCache:
    """In-process task handles + hydrated records for one session partition."""

    tasks: Dict[str, TaskRecord] = field(default_factory=dict)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    hydrated: bool = False


def configure_task_storage(storage: SessionStoragePort) -> None:
    """Bind session storage from AppRuntime (composition root)."""
    global _storage, _session_caches
    _storage = storage
    _session_caches = OrderedDict()


def _get_storage() -> SessionStoragePort:
    if _storage is None:
        raise StorageNotConfiguredError(
            "Session storage is not configured. "
            "Wire AppRuntime via configure_task_storage() before using tasks."
        )
    return _storage


def _session_key(scope: SessionScope) -> tuple[str, str]:
    return (str(scope.user_id), str(scope.mcp_session_id))


def _task_key(task_id: str) -> str:
    return normalize_simple_id(task_id)


def _cache_is_idle(cache: _SessionTaskCache) -> bool:
    if cache.lock.locked():
        return False
    for record in cache.tasks.values():
        handle = record.asyncio_task
        if handle is not None and not handle.done():
            return False
    return True


def _evict_idle_session_caches() -> None:
    """Drop least-recent idle caches so the map cannot grow without bound."""
    while len(_session_caches) >= _MAX_SESSION_CACHES:
        evicted = False
        for key, cache in list(_session_caches.items()):
            if _cache_is_idle(cache):
                del _session_caches[key]
                evicted = True
                break
        if not evicted:
            return


async def _get_or_create_cache(scope: SessionScope) -> _SessionTaskCache:
    key = _session_key(scope)
    async with _registry_lock:
        cache = _session_caches.get(key)
        if cache is not None:
            _session_caches.move_to_end(key)
            return cache
        _evict_idle_session_caches()
        cache = _SessionTaskCache()
        _session_caches[key] = cache
        return cache


def _to_iso(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()


def _normalize_result(result: Any) -> BaseResult:
    if isinstance(result, BaseResult):
        return result
    return BaseResult(result=[result])


def _generate_task_id() -> str:
    return generate_simple_id()


def _json_default(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _result_to_storage_dict(result: Optional[BaseResult]) -> Optional[Dict[str, Any]]:
    """Serialize a BaseResult to a JSON-compatible dict for Storage."""
    if result is None:
        return None
    try:
        dumped = result.model_dump(mode="json")
    except (TypeError, ValueError):
        dumped = result.model_dump(mode="python")
    return json.loads(json.dumps(dumped, default=_json_default))


def _serialize_record(record: TaskRecord) -> Dict[str, Any]:
    payload = {
        "task_id": record.task_id,
        "action": copy.deepcopy(record.action),
        "created_at": record.created_at,
        "last_updated_at": record.last_updated_at,
        "time_to_live_ms": record.time_to_live_ms,
        "status": record.status,
        "status_message": record.status_message,
        "status_info": record.status_info,
        "started_running_at": record.started_running_at,
        "finished_at": record.finished_at,
        "user_id": record.user_id,
        "mcp_session_id": record.mcp_session_id,
    }
    if record.result is not None:
        payload["result"] = _result_to_storage_dict(record.result)
    return payload


def _deserialize_record(payload: Dict[str, Any]) -> TaskRecord:
    raw_result = payload.get("result")
    result: Optional[BaseResult] = None
    if isinstance(raw_result, dict):
        result = BaseResult.model_validate(raw_result)
    return TaskRecord(
        task_id=str(payload["task_id"]),
        action=dict(payload.get("action") or {}),
        created_at=float(payload.get("created_at") or 0.0),
        last_updated_at=float(payload.get("last_updated_at") or 0.0),
        time_to_live_ms=payload.get("time_to_live_ms"),
        status=str(payload.get("status") or STATUS_PARKING),
        status_message=str(payload.get("status_message") or ""),
        status_info=str(payload.get("status_info") or ""),
        result=result,
        asyncio_task=None,
        started_running_at=(
            float(payload["started_running_at"])
            if payload.get("started_running_at") is not None
            else None
        ),
        finished_at=(
            float(payload["finished_at"])
            if payload.get("finished_at") is not None
            else None
        ),
        user_id=str(payload.get("user_id") or DEFAULT_USER_ID),
        mcp_session_id=str(payload.get("mcp_session_id") or DEFAULT_SESSION_ID),
    )


def _merge_remote_into_cache(cache: _SessionTaskCache, remote_tasks: Dict[str, Any]) -> None:
    """
    Merge Storage tasks into the in-process cache.

    Prefer live local records that still own an asyncio.Task handle (running or
    finished on this worker) so cancel/wait/result identity stay intact. Purely
    hydrated records (no local handle) refresh from Storage for cross-request
    polling.
    """
    merged: Dict[str, TaskRecord] = {}
    for raw in remote_tasks.values():
        if not isinstance(raw, dict) or "task_id" not in raw:
            continue
        remote = _deserialize_record(raw)
        key = _task_key(remote.task_id)
        local = cache.tasks.get(key)
        if local is not None and local.asyncio_task is not None:
            merged[key] = local
        else:
            merged[key] = remote
    for task_id, local in cache.tasks.items():
        key = _task_key(task_id)
        if key not in merged:
            merged[key] = local
    cache.tasks = merged


async def _hydrate_cache(cache: _SessionTaskCache, scope: SessionScope) -> None:
    """Load partition tasks into the session cache (caller holds cache.lock)."""
    partition = await _get_storage().get_partition(scope)
    remote = partition.tasks if partition else {}
    _merge_remote_into_cache(cache, remote)
    cache.hydrated = True


async def _commit_cache(
        cache: _SessionTaskCache,
        scope: SessionScope,
        snapshot_ids: Optional[Set[str]] = None,
) -> None:
    """
    Persist the tasks map for this SessionScope.

    Atomicity: one put_partition of the full tasks map.
    Consistency: partial payload (tasks only) so dataframes/metadata/files stay.
    Isolation: caller holds the in-process session lock. Before PUT, re-read
    and union keys added by other workers; drop ids this operation removed.
    Live local asyncio handles win on overlapping keys via cache.tasks overlay.
    Durability: delegated to SessionStoragePort.

    Same-key concurrent writes and the GET/PUT race can still last-write-win;
    closing that window requires Storage CAS/etag (not implemented here).
    """
    current_ids = set(cache.tasks.keys())
    removed_ids = (
        {_task_key(task_id) for task_id in snapshot_ids} - current_ids
        if snapshot_ids is not None
        else set()
    )
    partition = await _get_storage().get_partition(scope)
    remote = partition.tasks if partition else {}

    merged: Dict[str, TaskRecord] = {}
    for raw in remote.values():
        if not isinstance(raw, dict) or "task_id" not in raw:
            continue
        record = _deserialize_record(raw)
        merged[_task_key(record.task_id)] = record

    for removed_id in removed_ids:
        merged.pop(removed_id, None)

    merged.update(cache.tasks)
    for removed_id in removed_ids:
        merged.pop(removed_id, None)

    cache.tasks = merged
    tasks = {
        task_id: _serialize_record(record)
        for task_id, record in merged.items()
    }
    await _get_storage().put_partition(
        scope,
        SessionPartitionPayload(tasks=tasks),
    )


async def _allocate_task_id(cache: _SessionTaskCache) -> str:
    for _ in range(TASK_ID_MAX_ATTEMPTS):
        candidate = _generate_task_id()
        if candidate not in cache.tasks:
            return candidate

    logger.error(
        "Unable to allocate task id. attempts=%s id_length=%s alphabet=crockford32 active_pool_size=%s",
        TASK_ID_MAX_ATTEMPTS,
        SIMPLE_ID_LENGTH,
        len(cache.tasks),
    )
    raise RuntimeError(
        f"Unable to allocate unique {SIMPLE_ID_LENGTH}-char task id after {TASK_ID_MAX_ATTEMPTS} attempts."
    )


async def _set_status_and_persist(
        record: TaskRecord,
        status: str,
        status_message: str,
) -> None:
    record.set_status(status, status_message)
    scope = record.scope()
    cache = await _get_or_create_cache(scope)
    async with cache.lock:
        cache.tasks[_task_key(record.task_id)] = record
        await _commit_cache(cache, scope)


async def _task_runner(task_record: TaskRecord, coro_factory: Callable[[], Awaitable[Any]]):
    await _set_status_and_persist(
        task_record,
        STATUS_PARKING,
        "Task is waiting for an available execution slot.",
    )
    try:
        async with _semaphore:
            await _set_status_and_persist(
                task_record,
                STATUS_WORKING,
                "Task is currently running.",
            )
            if task_record.time_to_live_ms is None:
                action_result = await coro_factory()
            else:
                action_result = await asyncio.wait_for(
                    coro_factory(),
                    timeout=task_record.time_to_live_ms / 1000,
                )
            normalized = _normalize_result(action_result)
            result_format = str(task_record.action.get("result_format", "auto")).strip().lower()
            origin_action = str(task_record.action.get("method", "unknown")).strip() or "unknown"
            # Task runner owns materialization for parked work (pollers read Storage).
            # run_tool_with_runtime may finalize again on the fast path; that path is
            # idempotent for already-stored dataframe payloads.
            normalized = await finalize_tool_result(
                normalized,
                action=origin_action,
                args={"result_format": result_format},
                origin_manager=str(task_record.action.get("manager", "unknown")),
                session_storage=_get_storage(),
                scope=task_record.scope(),
                excluded_actions=TOOLS_ACTIONS_SKIP_AUTO_DATAFRAME,
            )
            task_record.result = normalized
            if normalized.error:
                await _set_status_and_persist(
                    task_record,
                    STATUS_FAILED,
                    f"Task finished with error: {normalized.error}",
                )
            else:
                await _set_status_and_persist(
                    task_record,
                    STATUS_COMPLETED,
                    "Task finished successfully.",
                )
    except asyncio.TimeoutError:
        timeout_message = (
            f"Task timed out after {task_record.time_to_live_ms} ms."
            if task_record.time_to_live_ms is not None
            else "Task timed out."
        )
        task_record.result = BaseResult(error=timeout_message)
        await _set_status_and_persist(task_record, STATUS_CANCELLED, timeout_message)
    except asyncio.CancelledError:
        cancel_message = "Task was cancelled."
        task_record.result = BaseResult(error=cancel_message)
        await _set_status_and_persist(task_record, STATUS_CANCELLED, cancel_message)
    except Exception as exc:
        error_message = f"Task failed with exception: {str(exc)}"
        task_record.result = BaseResult(error=error_message)
        await _set_status_and_persist(task_record, STATUS_FAILED, error_message)


async def submit_task(
        action: Dict[str, Any],
        coro_factory: Callable[[], Awaitable[Any]],
        time_to_live_ms: Optional[int] = None,
        scope: SessionScope = DEFAULT_SCOPE,
) -> str:
    cache = await _get_or_create_cache(scope)
    async with cache.lock:
        await _hydrate_cache(cache, scope)
        now = time.time()
        task_id = await _allocate_task_id(cache)
        task_record = TaskRecord(
            task_id=task_id,
            action=action,
            created_at=now,
            last_updated_at=now,
            time_to_live_ms=time_to_live_ms,
            status=STATUS_PARKING,
            status_message="Task accepted and pending scheduling.",
            status_info=STATUS_INFO[STATUS_PARKING],
            user_id=scope.user_id,
            mcp_session_id=scope.mcp_session_id,
        )
        cache.tasks[task_id] = task_record
        await _commit_cache(cache, scope)
        # Assign the handle before releasing the lock so concurrent get/cancel
        # cannot hydrate a deserialized copy that drops asyncio.Task identity.
        async_task = asyncio.create_task(_task_runner(task_record, coro_factory))
        task_record.asyncio_task = async_task
    return task_id


async def get_task_record(
        task_id: str,
        scope: SessionScope = DEFAULT_SCOPE,
) -> Optional[TaskRecord]:
    normalized = _task_key(task_id)
    cache = await _get_or_create_cache(scope)
    async with cache.lock:
        await _hydrate_cache(cache, scope)
        return cache.tasks.get(normalized)


async def remove_task(
        task_id: str,
        scope: SessionScope = DEFAULT_SCOPE,
) -> bool:
    normalized = _task_key(task_id)
    cache = await _get_or_create_cache(scope)
    async with cache.lock:
        await _hydrate_cache(cache, scope)
        snapshot_ids = set(cache.tasks.keys())
        removed = cache.tasks.pop(normalized, None) is not None
        if removed:
            await _commit_cache(cache, scope, snapshot_ids=snapshot_ids)
        return removed


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


async def list_tasks(
        status_list: Optional[List[str]] = None,
        scope: SessionScope = DEFAULT_SCOPE,
) -> List[TaskRecord]:
    cache = await _get_or_create_cache(scope)
    async with cache.lock:
        await _hydrate_cache(cache, scope)
        records = list(cache.tasks.values())
    if not status_list:
        return records
    expected = {status.lower() for status in status_list}
    return [task for task in records if task.status.lower() in expected]


def is_terminal_status(status: str) -> bool:
    return status in TERMINAL_STATES


def is_active_status(status: str) -> bool:
    return status in ACTIVE_STATES


async def cancel_task(
        task_id: str,
        scope: SessionScope = DEFAULT_SCOPE,
) -> Optional[TaskRecord]:
    """
    Request cancellation for a task in this session partition.

    Terminal tasks (completed/failed/cancelled) are left unchanged.
    Live local asyncio handles are cancelled on this worker only.
    Active tasks without a local handle (typical hosted multi-worker case) are
    marked cancelled in Storage for status visibility, but the owning worker's
    coroutine may still finish and overwrite status — see hosted runbook.
    """
    normalized_task_id = _task_key(task_id)
    cache = await _get_or_create_cache(scope)
    async with cache.lock:
        await _hydrate_cache(cache, scope)
        task_record = cache.tasks.get(normalized_task_id)
        if not task_record:
            return None
        if is_terminal_status(task_record.status):
            return task_record
        if task_record.asyncio_task and not task_record.asyncio_task.done():
            task_record.asyncio_task.cancel()
            # CancelledError path in _task_runner persists terminal state.
            return task_record
        # Active in Storage but no cancelable handle on this process.
        task_record.set_status(
            STATUS_CANCELLED,
            (
                "Cancel recorded in session Storage, but this worker has no local "
                "asyncio handle. If another worker owns the coroutine, it may still "
                "run to completion and overwrite status."
            ),
        )
        if task_record.result is None:
            task_record.result = BaseResult(
                error=(
                    "Task cancel was recorded without a local execution handle. "
                    "Execution affinity is process-local in hosted MCP."
                )
            )
        await _commit_cache(cache, scope)
        return task_record


def session_scope_from_manager(manager: Any) -> SessionScope:
    """Resolve Storage partition keys from a Manager instance (token + ctx)."""
    return resolve_session_scope(
        getattr(manager, "ctx", None),
        token=getattr(manager, "token", None),
        scope_resolver=getattr(manager, "scope_resolver", None),
    )
