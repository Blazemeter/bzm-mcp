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
"""
Simple utilities for BlazeMeter MCP tools.
"""
import asyncio
import contextvars
import functools
import inspect
import os
import platform
import re
import secrets
import sys
import time
import traceback
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional, Callable, Awaitable, Tuple
from importlib import resources
from pathlib import Path

import httpx
from mcp.types import CallToolResult
from pydantic import BaseModel

from config.blazemeter import BZM_API_BASE_URL
from config.cache import CacheScope, StorePlan, build_cache_key, get_cache
from config.context_resolution import resolve_ctx_token, resolve_ctx_user_config
from config.security import validate_http_request_endpoint
from config.token import BzmToken
from config.version import __version__
from models.result import BaseResult, HttpBaseResult, ToolResult

SIMPLE_ID_ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
SIMPLE_ID_LENGTH = 8


def generate_simple_id() -> str:
    return "".join(secrets.choice(SIMPLE_ID_ALPHABET) for _ in range(SIMPLE_ID_LENGTH))


def normalize_simple_id(simple_id: str) -> str:
    return str(simple_id).strip().lower()


so = platform.system()  # "Windows", "Linux", "Darwin"
version = platform.version()  # kernel / build version
release = platform.release()  # ex. "10", "5.15.0-76-generic"
machine = platform.machine()  # ex. "x86_64", "AMD64", "arm64"

ua_part = f"{so} {release}; {machine}"
user_agent = f"bzm-mcp/{__version__} ({ua_part})"
timeout = httpx.Timeout(
    connect=15.0,
    read=60.0,
    write=15.0,
    pool=60.0
)
project_root = Path(__file__).resolve().parents[2]
# Match Windows absolute paths (backslash or forward slash; latter may appear on POSIX).
# Negative lookbehind ensures we don't match URL protocols like https:// (where the
# letter before ':' is preceded by more letters, e.g. 'http' in 'https://').
windows_abs_path_pattern = re.compile(
    r"(?<![A-Za-z])[A-Za-z]:[\\/](?:[^\\\n\r\t\"']+[\\/])*[^\\\n\r\t\"']*"
)
unix_abs_path_pattern = re.compile(
    r"/(?:"
    r"Users|home|root"           # User home directories (macOS, Linux)
    r"|var|tmp|etc|opt|srv"      # Standard Linux directories
    r"|mnt|run|media"            # Mount points and runtime (Linux)
    r"|app|data"                 # Common Docker container directories
    r"|System|Library|Applications|private|Volumes"  # macOS directories
    r")/[^\n\r\t\"']+"
)


def sanitize_path(path_value: str) -> str:
    if not path_value:
        return path_value

    # On POSIX, Windows-style paths (e.g. from compile() or cross-platform code)
    # resolve to cwd+path, so relative_to() would incorrectly return the raw path.
    # Redact them immediately. On Windows, the normal flow handles them correctly.
    if so != "Windows" and re.match(r"^[A-Za-z]:[\\/]", path_value):
        return Path(path_value.replace("\\", "/")).name or "<root hidden>"

    try:
        absolute_path = Path(path_value).resolve()
        relative_path = absolute_path.relative_to(project_root)
        return relative_path.as_posix()
    except Exception:
        pass

    if re.match(r"^[A-Za-z]:[\\/]", path_value) or path_value.startswith("/"):
        return Path(path_value.replace("\\", "/")).name or "<root hidden>"

    return path_value


def redact_system_paths(text: str) -> str:
    def replace_match(match: re.Match) -> str:
        return sanitize_path(match.group(0))

    text = windows_abs_path_pattern.sub(replace_match, text)
    text = unix_abs_path_pattern.sub(replace_match, text)
    return text


def _sanitize_traceback_exception(tb_exception: traceback.TracebackException):
    for frame in tb_exception.stack:
        frame.filename = sanitize_path(frame.filename)

    if tb_exception.__cause__:
        _sanitize_traceback_exception(tb_exception.__cause__)
    if tb_exception.__context__ and not tb_exception.__suppress_context__:
        _sanitize_traceback_exception(tb_exception.__context__)


def format_sanitized_traceback(exc: Optional[BaseException] = None) -> str:
    if exc is None:
        exc = sys.exc_info()[1]

    if exc is None:
        return "No traceback available."

    tb_exception = traceback.TracebackException.from_exception(exc, capture_locals=False)
    _sanitize_traceback_exception(tb_exception)
    formatted_traceback = "".join(tb_exception.format()).strip()
    return redact_system_paths(formatted_traceback)


class ConfirmMode(Enum):
    DELETE = "DELETE"  # Delete only
    CUD = "CUD"  # Create, Update, Delete
    DISABLE = "NONE"  # No confirmation


_task_management_enabled = contextvars.ContextVar("task_management_enabled", default=False)
_result_format_context = contextvars.ContextVar("result_format_context", default="auto")
_disable_dataframe_materialization = contextvars.ContextVar(
    "disable_dataframe_materialization", default=False
)
_tool_result_depth = contextvars.ContextVar("tool_result_depth", default=0)
_cache_debug_context = contextvars.ContextVar("cache_debug_context", default=None)
_result_debug_enabled = False


class Operations(Enum):
    CREATE = "C"  # Create
    READ = "R"  # Read
    UPDATE = "U"  # Update
    DELETE = "D"  # Delete


# MCP tool actions that must stay inline under result_format=auto (no auto-dataframe).
# Shared by @tool_result(excluded_actions=...) and the async task runner so exclusions
# are honored even when @run_as_task materializes before the entrypoint finalize.
TOOLS_ACTIONS_SKIP_AUTO_DATAFRAME = frozenset({
    "tasks_get",
    "tasks_list",
    "tasks_status",
    "tasks_cancel",
    "tasks_remove",
    "dataframes_list",
    "dataframes_get",
    "dataframes_schema_groups",
    "dataframes_query",
    "dataframes_remove",
    "dataframes_clear",
    "dataframes_sql_help",
})


def set_result_debug_enabled(enabled: bool):
    global _result_debug_enabled
    _result_debug_enabled = bool(enabled)


def is_result_debug_enabled() -> bool:
    return _result_debug_enabled


def set_disable_dataframe_materialization(disabled: bool) -> contextvars.Token:
    return _disable_dataframe_materialization.set(bool(disabled))


def reset_disable_dataframe_materialization(token: contextvars.Token) -> None:
    _disable_dataframe_materialization.reset(token)


def normalize_action_args(arguments: Optional[Dict[str, Any]] = None) -> tuple[str, Dict[str, Any]]:
    """
    Normalize tool arguments to (action, args) format.
    Supports:
      - {"action": "x", "args": {"key": "value"}}
      - {"action": "x", "key": "value"}  (params at top level, merged into args)
      - {"arguments": {"action": "x", "args": {...}}}  (double-wrapped by client)
    Top-level keys other than 'action' and 'args' are merged into args.
    Use a single 'arguments' param so the full MCP tool call payload is received
    (avoids Pydantic dropping extra fields when using action/args separately).
    """
    arguments = arguments or {}
    # Unwrap double-nested format: {"arguments": {"action": "x", "args": {...}}}
    inner = arguments.get("arguments")
    if (
            isinstance(inner, dict)
            and len(arguments) == 1
            and ("action" in inner or "args" in inner)
    ):
        arguments = inner
    action = str(arguments.get("action") or "").strip() or ""
    args = dict(arguments.get("args") or {})
    for key, value in arguments.items():
        if key not in ("action", "args"):
            args[key] = value
    return action, args


def validate_required_args(action: str, args: Optional[Dict[str, Any]], required: list[str]) -> Optional[BaseResult]:
    args = args or {}
    missing = [key for key in required if key not in args or args[key] is None]
    if not missing:
        return None
    missing_str = ", ".join(missing)
    required_str = ", ".join(required)
    return BaseResult(
        error=(
            f"Missing required args for action '{action}': {missing_str} not found within 'args'. "
            f"Required args: {required_str}. Ensure parameters are passed inside the 'args' argument."
        )
    )


def validate_non_empty_str_arg(
        action: str, args: Optional[Dict[str, Any]], key: str
) -> Optional[BaseResult]:
    """Return BaseResult error if args[key] is missing, not a str, or only whitespace."""
    args = args or {}
    value = args.get(key)
    if not isinstance(value, str) or not value.strip():
        return BaseResult(
            error=(
                f"Missing required args for action '{action}': {key} must be a non-empty string "
                f"within 'args'. Required args: {key}."
            )
        )
    return None


def _resolve_tool_token(ctx: Any) -> Optional[BzmToken]:
    if ctx is None:
        return None
    return resolve_ctx_token(ctx)


def _resolve_invocation(
        args: tuple[Any, ...],
        kwargs: Dict[str, Any],
) -> Tuple[str, Dict[str, Any], Any]:
    """Resolve (action, tool_args, ctx) from arguments= or legacy action/args shapes."""
    ctx = kwargs.get("ctx")
    arguments = kwargs.get("arguments")

    if arguments is None and args:
        if isinstance(args[0], dict):
            arguments = args[0]
            if ctx is None and len(args) >= 2:
                ctx = args[1]
        elif isinstance(args[0], str):
            action = args[0]
            tool_args = args[1] if len(args) > 1 else (kwargs.get("args") or {})
            if ctx is None and len(args) >= 3:
                ctx = args[2]
            if not isinstance(tool_args, dict):
                tool_args = {}
            return action, tool_args, ctx

    if isinstance(arguments, dict):
        action, tool_args = normalize_action_args(arguments)
        return action, tool_args, ctx

    action = kwargs.get("action") or ""
    tool_args = kwargs.get("args") or {}
    if not isinstance(tool_args, dict):
        tool_args = {}
    return str(action), tool_args, ctx


def _set_tool_call_timing(
        result: BaseResult,
        started_monotonic: float,
        started_wall_clock: float,
        extra_timing: Optional[Dict[str, int]] = None,
):
    finished_wall_clock = time.time()
    duration_ms = int((time.monotonic() - started_monotonic) * 1000)
    result.tool_call_started_at = datetime.fromtimestamp(started_wall_clock, tz=timezone.utc).isoformat()
    result.tool_call_finished_at = datetime.fromtimestamp(finished_wall_clock, tz=timezone.utc).isoformat()
    result.tool_call_duration_ms = duration_ms
    if not _result_debug_enabled:
        return
    debug = result.debug if isinstance(result.debug, dict) else {}
    timing = {"total_ms": duration_ms}
    if extra_timing:
        timing.update({k: int(v) for k, v in extra_timing.items()})
    debug["timing"] = timing
    cache_debug = _cache_debug_context.get()
    if isinstance(cache_debug, dict) and any(cache_debug.values()):
        debug["cache"] = dict(cache_debug)
    result.debug = debug


def _start_cache_debug_scope() -> contextvars.Token:
    if not _result_debug_enabled:
        return _cache_debug_context.set(None)
    return _cache_debug_context.set({"hits": 0, "misses": 0, "shared_wait_ms": 0})


def _accumulate_cache_debug(metric: str, value: int = 1) -> None:
    current = _cache_debug_context.get()
    if isinstance(current, dict):
        current[metric] = int(current.get(metric, 0)) + int(value)


def tool_result(
        excluded_actions: Optional[set[str]] = None,
        *,
        disable_materialization: bool = False,
):
    """
    MCP entrypoint wrapper: set result_format context, attach timing, and return ToolResult.

    Nested calls (e.g. help/skills batch sub-actions) return BaseResult to avoid wrapping.
    Materialization is owned by run_tool_with_runtime / the async task runner unless
    ``disable_materialization`` is False (legacy/direct finalize path).
    """
    excluded = excluded_actions or set()

    def decorator(func: Callable[..., Awaitable[Any]]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> ToolResult | CallToolResult | BaseResult:
            depth = _tool_result_depth.get()
            depth_token = _tool_result_depth.set(depth + 1)
            cache_debug_token = _start_cache_debug_scope() if depth == 0 else None
            action, tool_args, ctx = _resolve_invocation(args, kwargs)

            result_format = "auto"
            if isinstance(tool_args, dict) and "result_format" in tool_args:
                raw_format = str(tool_args.get("result_format", "auto")).strip().lower()
                if raw_format in {"auto", "dataframe", "raw"}:
                    result_format = raw_format
                else:
                    result_format = "invalid"
            if isinstance(action, str) and action == "batch":
                result_format = "raw"

            format_token = _result_format_context.set(
                result_format if result_format != "invalid" else "auto"
            )
            started_monotonic = time.monotonic()
            started_wall_clock = time.time()
            try:
                if result_format == "invalid":
                    result: Any = BaseResult(
                        error="Invalid result_format value. Allowed values: auto, dataframe, raw."
                    )
                    after_func_monotonic = started_monotonic
                else:
                    result = await func(*args, **kwargs)
                    after_func_monotonic = time.monotonic()

                postprocess_ms = 0
                if (
                        not disable_materialization
                        and isinstance(result, BaseResult)
                        and not result.error
                        and result.result is not None
                ):
                    from tools.dataframe_manager import finalize_tool_result

                    post_started = time.monotonic()
                    result = await finalize_tool_result(
                        result,
                        action=action,
                        args=tool_args,
                        origin_manager=func.__name__,
                        token=_resolve_tool_token(ctx),
                        ctx=ctx,
                        excluded_actions=excluded,
                    )
                    postprocess_ms = int((time.monotonic() - post_started) * 1000)

                if isinstance(result, BaseResult):
                    _set_tool_call_timing(
                        result,
                        started_monotonic,
                        started_wall_clock,
                        extra_timing={
                            "manager_logic_ms": int((after_func_monotonic - started_monotonic) * 1000),
                            "postprocess_ms": postprocess_ms,
                        },
                    )

                if depth > 0:
                    return result
                if isinstance(result, (ToolResult, CallToolResult)):
                    return result
                if isinstance(result, BaseResult):
                    return ToolResult.from_base_result(result)
                return ToolResult.from_base_result(BaseResult(result=[result]))
            finally:
                _result_format_context.reset(format_token)
                if cache_debug_token is not None:
                    _cache_debug_context.reset(cache_debug_token)
                _tool_result_depth.reset(depth_token)

        return wrapper

    return decorator


def _attach_task_debug(result: BaseResult, task_record: Any):
    if not _result_debug_enabled:
        return
    if not isinstance(result, BaseResult) or task_record is None:
        return
    if not hasattr(result, "debug"):
        return
    debug = result.debug if isinstance(result.debug, dict) else {}
    task_debug: Dict[str, int] = {}
    if task_record.started_running_at is not None:
        task_debug["queue_wait_ms"] = int((task_record.started_running_at - task_record.created_at) * 1000)
        end_ts = task_record.finished_at if task_record.finished_at is not None else task_record.last_updated_at
        task_debug["run_ms"] = int((end_ts - task_record.started_running_at) * 1000)
    task_debug["lifecycle_ms"] = int((task_record.last_updated_at - task_record.created_at) * 1000)
    debug["task"] = task_debug
    result.debug = debug


def _serialize_action_value(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _serialize_action_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize_action_value(v) for v in value]
    return repr(value)


async def execute_with_task_management(
        action_payload: Dict[str, Any],
        coro_factory: Callable[[], Awaitable[Any]],
        time_to_live_ms: Optional[int] = None,
        fast_response_threshold_seconds: float = 5.0,
        scope: Optional[Any] = None,
) -> BaseResult:
    # Deferred import avoids circular dependency: utils → async_task_manager → dataframe_manager → utils.
    from config.storage import SessionScope
    from tools.async_task_manager import (
        DEFAULT_SCOPE,
        submit_task,
        get_task_record,
        remove_task,
        task_snapshot,
    )

    resolved_scope = scope if isinstance(scope, SessionScope) else DEFAULT_SCOPE
    wait_started = time.monotonic()
    try:
        task_id = await submit_task(
            action_payload,
            coro_factory,
            time_to_live_ms=time_to_live_ms,
            scope=resolved_scope,
        )
    except RuntimeError as exc:
        return BaseResult(error=str(exc))
    task_record = await get_task_record(task_id, scope=resolved_scope)
    if not task_record or not task_record.asyncio_task:
        return BaseResult(error="Task could not be scheduled.")

    try:
        await asyncio.wait_for(
            asyncio.shield(task_record.asyncio_task),
            timeout=fast_response_threshold_seconds,
        )
        latest_record = await get_task_record(task_id, scope=resolved_scope)
        if not latest_record or latest_record.result is None:
            await remove_task(task_id, scope=resolved_scope)
            return BaseResult(error="Task finished without result.")
        final_result = latest_record.result
        _attach_task_debug(final_result, latest_record)
        debug = getattr(final_result, "debug", None)
        if isinstance(debug, dict):
            debug.setdefault("task", {})
            debug["task"]["sync_wait_ms"] = int((time.monotonic() - wait_started) * 1000)
        await remove_task(task_id, scope=resolved_scope)
        return final_result
    except asyncio.TimeoutError:
        latest_record = await get_task_record(task_id, scope=resolved_scope)
        if not latest_record:
            return BaseResult(error="Task was not found after scheduling.")
        snapshot = task_snapshot(latest_record, include_result=False)
        timeout_result = BaseResult(
            result=[snapshot],
            info=[
                "Long-running operation accepted. Use blazemeter_tools with action 'tasks_status' to monitor status."
            ],
        )
        _attach_task_debug(timeout_result, latest_record)
        debug = getattr(timeout_result, "debug", None)
        if isinstance(debug, dict):
            debug.setdefault("task", {})
            debug["task"]["sync_wait_ms"] = int((time.monotonic() - wait_started) * 1000)
        timeout_result.mark_pending_task(task_id, resolved_scope)
        return timeout_result


def run_as_task(
        time_to_live_ms: Optional[int] = None,
        fast_response_threshold_seconds: float = 5.0,
):
    def decorator(func: Callable[..., Awaitable[Any]]):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            if _task_management_enabled.get():
                return await func(self, *args, **kwargs)

            try:
                signature = inspect.signature(func)
                bound = signature.bind(self, *args, **kwargs)
                bound.apply_defaults()
                named_params = {
                    key: _serialize_action_value(value)
                    for key, value in bound.arguments.items()
                    if key != "self"
                }
            except Exception:
                named_params = {}

            action_payload = {
                "manager": self.__class__.__name__,
                "method": func.__name__,
                "args": _serialize_action_value(args),
                "kwargs": _serialize_action_value(kwargs),
                "params": named_params,
                "result_format": _result_format_context.get(),
                "disable_dataframe_materialization": bool(
                    _disable_dataframe_materialization.get()
                ),
            }

            from tools.async_task_manager import session_scope_from_manager

            scope = session_scope_from_manager(self)
            token = _task_management_enabled.set(True)
            try:
                coro_factory = lambda: func(self, *args, **kwargs)
                return await execute_with_task_management(
                    action_payload=action_payload,
                    coro_factory=coro_factory,
                    time_to_live_ms=time_to_live_ms,
                    fast_response_threshold_seconds=fast_response_threshold_seconds,
                    scope=scope,
                )
            finally:
                _task_management_enabled.reset(token)

        return wrapper

    return decorator


def resolve_cache_user_id(manager: Any) -> Optional[str]:
    """
    User id that scopes USER cache entries, read from the request context.

    Single seam for the verified identity: the session work replaces this lookup
    with the verified user id; callers stay unchanged.
    """
    token = getattr(manager, "token", None)
    user_id = getattr(token, "id", None)
    if user_id is None or not str(user_id).strip():
        return None
    return str(user_id).strip()


def _cache_compact_value(value: Any) -> str:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return repr(value)
    if isinstance(value, dict):
        keys = sorted(value.keys(), key=lambda x: str(x))
        return "{" + ",".join(f"{k}:{_cache_compact_value(value[k])}" for k in keys) + "}"
    if isinstance(value, (list, tuple, set)):
        items = sorted(value, key=repr) if isinstance(value, set) else value
        return "[" + ",".join(_cache_compact_value(v) for v in items) + "]"
    return repr(value)


def _strip_per_call_fields(value: Any) -> Any:
    """Drop timing/debug that describe one call, so cache hits do not replay them."""
    if isinstance(value, BaseResult):
        value.debug = None
        value.tool_call_started_at = None
        value.tool_call_finished_at = None
        value.tool_call_duration_ms = None
    return value


def ttl_cache_method(ttl_seconds: float = 30, scope: CacheScope = CacheScope.USER):
    """
    Async TTL cache for manager instance methods (bursts and internal re-reads).

    - USER scope keys on the user id from the request context; without one the
      cache is bypassed, so entries are never shared across users.
    - GLOBAL scope is for results that do not depend on the caller.
    - Errors are never cached. Concurrent misses share one call.
    - Place it above @run_as_task: a hit skips the task entirely. When the call
      returns a snapshot of a task that is still running, the snapshot is cached
      for this session only and dropped as soon as the task finishes; session
      dataframe references are likewise cached for their session only.
    """

    def decorator(func: Callable[..., Awaitable[Any]]):
        qualified_name = f"{func.__module__}.{func.__qualname__}"

        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            if scope is CacheScope.USER:
                user_id = resolve_cache_user_id(self)
                if user_id is None:
                    return await func(self, *args, **kwargs)
            else:
                user_id = None

            cache = get_cache()
            # Inline calls (nested inside a running tool/task, e.g. bridge validations) always
            # get the domain result; top-level calls may get a task snapshot or a dataframe
            # reference. Separate keys keep one from ever being served to the other.
            key = build_cache_key(
                scope,
                qualified_name,
                f"args={_cache_compact_value(args)}",
                f"kwargs={_cache_compact_value(kwargs)}",
                f"format={_result_format_context.get()}",
                f"materialize={int(not _disable_dataframe_materialization.get())}",
                f"inline={int(_task_management_enabled.get())}",
                user_id=user_id,
            )

            from tools.async_task_manager import add_task_terminal_callback, session_scope_from_manager
            from tools.dataframe_manager import is_dataframe_reference

            session_scope = session_scope_from_manager(self)
            binding = f"{session_scope.user_id}/{session_scope.mcp_session_id}"

            def _store_policy(value: Any) -> Optional[StorePlan]:
                if not isinstance(value, BaseResult):
                    return StorePlan()
                if value.error:
                    return None
                if value.pending_task is not None:
                    task_id, task_scope = value.pending_task

                    async def _invalidate() -> None:
                        # Only our snapshot: another session may have stored a newer value since.
                        await cache.delete(key, if_tag=task_id)

                    async def _drop_when_task_finishes() -> None:
                        await add_task_terminal_callback(task_id, task_scope, _invalidate)

                    return StorePlan(
                        bound_to=binding,
                        tag=task_id,
                        transform=_strip_per_call_fields,
                        after_store=_drop_when_task_finishes,
                    )
                if is_dataframe_reference(value):
                    return StorePlan(bound_to=binding, transform=_strip_per_call_fields)
                return StorePlan(transform=_strip_per_call_fields)

            return await cache.get_or_load(
                key,
                lambda: func(self, *args, **kwargs),
                ttl_seconds,
                store_policy=_store_policy,
                binding=binding,
                observer=_accumulate_cache_debug,
            )

        return wrapper

    return decorator


async def api_request(token: Optional[BzmToken], method: str, endpoint: str,
                      result_formatter: Callable = None,
                      result_formatter_params: Optional[dict] = None,
                      **kwargs) -> BaseResult:
    """
    Make an authenticated request to the BlazeMeter API.
    Handles authentication errors gracefully.
    """
    if not token:
        return BaseResult(
            error="No API token. Set BLAZEMETER_API_KEY env var with file path or API_KEY_ID and API_KEY_SECRET secrets in docker catalog configuration."
        )

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = token.as_basic_auth()
    headers["User-Agent"] = user_agent

    async with (httpx.AsyncClient(base_url=BZM_API_BASE_URL, http2=True, timeout=timeout) as client):
        try:
            resp = await client.request(method, endpoint, headers=headers, **kwargs)
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            if "application/json" in content_type.lower():
                response_dict = resp.json()
                result = response_dict.get("result", [])
            else:
                response_dict = {}
                result = resp.text
            default_total = 0
            if not isinstance(result, list):  # Generalize result always as a list
                result = [result]
                default_total = 1
            final_result = result_formatter(result, result_formatter_params) if result_formatter else result
            return BaseResult(
                result=final_result,
                error=response_dict.get("error", None),
                total=response_dict.get("total", default_total),
                has_more=response_dict.get("total", 0) - (
                        response_dict.get("skip", 0) + response_dict.get("limit", 0)) > 0
            )
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_msg = None
            if status_code in [401, 403]:
                # Try to extract detailed error message from response body
                error_msg = "Invalid credentials"

                error_body = e.response.json()
                if isinstance(error_body, dict):
                    api_error = error_body.get("error")
                    if api_error:
                        if isinstance(api_error, dict):
                            error_msg = api_error.get("message", error_msg)
                        else:
                            error_msg = str(api_error)
                    elif "message" in error_body:
                        error_msg = error_body.get("message", error_msg)

                    # Check for data retention related keywords
                    error_text = str(error_body).lower()
                    if any(keyword in error_text for keyword in ["retention", "expired", "no longer available"]):
                        error_msg = "Data retention period expired: Report data is no longer available due to data retention policy"

            elif status_code in [404]:
                error_msg = "Not Found. Please ask the user to verify if the request is valid."

            if error_msg:
                return BaseResult(
                    error=error_msg
                )
            raise


async def http_request(method: str, endpoint: str,
                       result_formatter: Callable = None,
                       result_formatter_params: Optional[dict] = None,
                       **kwargs) -> HttpBaseResult:
    """
    Make an http request to Webpage.
    """

    endpoint_error = validate_http_request_endpoint(endpoint)
    if endpoint_error:
        return HttpBaseResult(error=endpoint_error)

    headers = kwargs.pop("headers", {})
    headers["User-Agent"] = user_agent

    async with (httpx.AsyncClient(base_url="", http2=True, timeout=timeout) as client):
        try:
            resp = await client.request(method, endpoint, headers=headers, **kwargs)
            resp.raise_for_status()
            result = resp.text
            error = None
            final_result = result_formatter(result, result_formatter_params) if result_formatter else result
            return HttpBaseResult(
                result=final_result,
                error=error,
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [401, 403]:
                return HttpBaseResult(
                    error="Invalid credentials"
                )
            raise


def get_date_time_iso(timestamp: int) -> Optional[str]:
    if timestamp is None:
        return None
    else:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def get_resources_path():
    try:
        resources_path = resources.files("resources")
    except ModuleNotFoundError:
        # Fallback for development or if not installed as package
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = Path(__file__).resolve().parents[2]
        resources_path = Path(base_path) / 'resources'
    return resources_path


class Confirmation(BaseModel):
    pass  # Empty model with no fields for simple accept/cancel without UI elements


def _to_confirm_mode(value: Any) -> ConfirmMode:
    if isinstance(value, ConfirmMode):
        return value
    if isinstance(value, str):
        normalized = value.strip().upper()
        if normalized in ConfirmMode.__members__:
            return ConfirmMode[normalized]
        for mode in ConfirmMode:
            if normalized == mode.value:
                return mode
    return ConfirmMode.DELETE


def _get_ctx_user_config(ctx: Any) -> dict[str, Any] | None:
    user_config = resolve_ctx_user_config(ctx)
    if user_config:
        return user_config
    return None


def resolve_confirmation_mode(ctx: Any, manager_user_config: Any = None) -> ConfirmMode:
    """
    Resolve confirmation mode from runtime/user session context.

    Precedence:
    1) per-request/per-session context user config
    2) manager-level user config (stdio startup config)
    3) DELETE default
    """
    ctx_user_config = _get_ctx_user_config(ctx)
    if isinstance(ctx_user_config, dict):
        return _to_confirm_mode(ctx_user_config.get("confirmation_mode"))
    if isinstance(manager_user_config, dict):
        return _to_confirm_mode(manager_user_config.get("confirmation_mode"))
    return ConfirmMode.DELETE


def operation_need_confirmation(operation: Operations, confirm_mode: ConfirmMode) -> bool:
    if confirm_mode == ConfirmMode.DELETE and operation in [Operations.DELETE]:
        return True
    elif confirm_mode == ConfirmMode.CUD and operation in [Operations.CREATE, Operations.UPDATE, Operations.DELETE]:
        return True
    else:
        return False


def require_confirmation(operation: Operations = Operations.READ,
                         message="This action requires manual confirmation to continue"):
    confirmation_schema = Confirmation
    confirmation_unsupported_error = (
        "Action not allowed: confirmation is required, but this MCP client "
        "does not support elicitation for confirmation prompts."
    )

    def decorator(func: Callable[..., Awaitable]):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            confirm_mode = resolve_confirmation_mode(
                getattr(self, "ctx", None),
                getattr(self, "user_config", None),
            )
            need_confirmation = operation_need_confirmation(operation, confirm_mode)
            confirmed = True  # Run operation by default
            if need_confirmation:
                try:
                    result = await self.ctx.elicit(message=message, schema=confirmation_schema)
                    confirmed = (result.action == "accept" and result.data)
                except Exception:
                    return BaseResult(error=confirmation_unsupported_error)
            if confirmed:
                return await func(self, *args, **kwargs)
            else:
                return BaseResult(result=["Action manually cancelled by the user."])

        return wrapper

    return decorator
