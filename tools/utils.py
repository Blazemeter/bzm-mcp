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
import secrets

"""
Simple utilities for BlazeMeter MCP tools.
"""
import asyncio
import contextvars
import copy
import functools
import inspect
import os
import platform
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Optional, Callable, Awaitable, Any, Dict

import httpx
from mcp.types import CallToolResult
from pydantic import BaseModel

from config.blazemeter import BZM_API_BASE_URL
from config.security import validate_http_request_endpoint
from config.token import BzmToken
from config.version import __version__
from models.result import BaseResult, HttpBaseResult, ToolResult

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
project_root = Path(__file__).resolve().parent.parent
# Match Windows absolute paths (backslash or forward slash; latter may appear on POSIX).
# Negative lookbehind ensures we don't match URL protocols like https:// (where the
# letter before ':' is preceded by more letters, e.g. 'http' in 'https://').
windows_abs_path_pattern = re.compile(
    r"(?<![A-Za-z])[A-Za-z]:[\\/](?:[^\\\n\r\t\"']+[\\/])*[^\\\n\r\t\"']*"
)
unix_abs_path_pattern = re.compile(
    r"/(?:"
    r"Users|home|root"  # User home directories (macOS, Linux)
    r"|var|tmp|etc|opt|srv"  # Standard Linux directories
    r"|mnt|run|media"  # Mount points and runtime (Linux)
    r"|app|data"  # Common Docker container directories
    r"|System|Library|Applications|private|Volumes"  # macOS directories
    r")/[^\n\r\t\"']+"
)

SIMPLE_ID_ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
SIMPLE_ID_LENGTH = 8

def generate_simple_id() -> str:
    return "".join(secrets.choice(SIMPLE_ID_ALPHABET) for _ in range(SIMPLE_ID_LENGTH))

def normalize_simple_id(simple_id: str) -> str:
    return str(simple_id).strip().lower()

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


_confirm_mode = ConfirmMode.DELETE
_task_management_enabled = contextvars.ContextVar("task_management_enabled", default=False)
_method_cache: Dict[str, tuple[float, Any]] = {}
_method_cache_inflight: Dict[str, asyncio.Future] = {}
_method_cache_lock = asyncio.Lock()
_method_cache_max_entries = 2048
_http_clients_lock = asyncio.Lock()
_bzm_http_client: Optional[httpx.AsyncClient] = None
_generic_http_client: Optional[httpx.AsyncClient] = None
_network_debug_context = contextvars.ContextVar("network_debug_context", default=None)
_cache_debug_context = contextvars.ContextVar("cache_debug_context", default=None)
_result_debug_enabled = False
_result_format_context = contextvars.ContextVar("result_format_context", default="auto")
_force_task_response_context = contextvars.ContextVar("force_task_response_context", default=False)


class Operations(Enum):
    CREATE = "C"  # Create
    READ = "R"  # Read
    UPDATE = "U"  # Update
    DELETE = "D"  # Delete


def set_result_debug_enabled(enabled: bool):
    global _result_debug_enabled
    _result_debug_enabled = bool(enabled)


def is_result_debug_enabled() -> bool:
    return _result_debug_enabled


async def _get_bzm_http_client() -> httpx.AsyncClient:
    global _bzm_http_client
    if _bzm_http_client is not None:
        return _bzm_http_client
    async with _http_clients_lock:
        if _bzm_http_client is None:
            _bzm_http_client = httpx.AsyncClient(base_url=BZM_API_BASE_URL, http2=True, timeout=timeout)
    return _bzm_http_client


async def _get_generic_http_client() -> httpx.AsyncClient:
    global _generic_http_client
    if _generic_http_client is not None:
        return _generic_http_client
    async with _http_clients_lock:
        if _generic_http_client is None:
            _generic_http_client = httpx.AsyncClient(base_url="", http2=True, timeout=timeout)
    return _generic_http_client


def _start_network_debug_scope() -> contextvars.Token:
    if not _result_debug_enabled:
        return _network_debug_context.set(None)
    return _network_debug_context.set({"http_calls": 0, "http_total_ms": 0})


def _get_network_debug_snapshot() -> Dict[str, int]:
    current = _network_debug_context.get()
    if not isinstance(current, dict):
        return {"http_calls": 0, "http_total_ms": 0}
    return {
        "http_calls": int(current.get("http_calls", 0)),
        "http_total_ms": int(current.get("http_total_ms", 0)),
    }


def _accumulate_network_debug(elapsed_ms: int):
    current = _network_debug_context.get()
    if not isinstance(current, dict):
        return
    current["http_calls"] = int(current.get("http_calls", 0)) + 1
    current["http_total_ms"] = int(current.get("http_total_ms", 0)) + max(0, int(elapsed_ms))


def _start_cache_debug_scope() -> contextvars.Token:
    if not _result_debug_enabled:
        return _cache_debug_context.set(None)
    return _cache_debug_context.set(
        {
            "hits": 0,
            "misses": 0,
            "shared_wait_ms": 0,
            "lock_wait_ms": 0,
            "deepcopy_ms": 0,
        }
    )


def _accumulate_cache_debug(metric: str, value: int = 1):
    current = _cache_debug_context.get()
    if not isinstance(current, dict):
        return
    current[metric] = int(current.get(metric, 0)) + int(value)


def _get_cache_debug_snapshot() -> Dict[str, int]:
    current = _cache_debug_context.get()
    if not isinstance(current, dict):
        return {
            "hits": 0,
            "misses": 0,
            "shared_wait_ms": 0,
            "lock_wait_ms": 0,
            "deepcopy_ms": 0,
        }
    return {
        "hits": int(current.get("hits", 0)),
        "misses": int(current.get("misses", 0)),
        "shared_wait_ms": int(current.get("shared_wait_ms", 0)),
        "lock_wait_ms": int(current.get("lock_wait_ms", 0)),
        "deepcopy_ms": int(current.get("deepcopy_ms", 0)),
    }


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

    client = await _get_bzm_http_client()
    request_started = time.monotonic()
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
        if e.response.status_code in [401, 403]:
            return BaseResult(
                error="Invalid credentials"
            )
        raise
    finally:
        _accumulate_network_debug(int((time.monotonic() - request_started) * 1000))


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

    client = await _get_generic_http_client()
    request_started = time.monotonic()
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
    finally:
        _accumulate_network_debug(int((time.monotonic() - request_started) * 1000))


def get_date_time_iso(timestamp: int) -> Optional[str]:
    if timestamp is None:
        return None
    else:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def _set_tool_call_timing(
        result: BaseResult,
        started_monotonic: float,
        started_wall_clock: float,
        extra_timing: Optional[Dict[str, int]] = None
):
    finished_wall_clock = time.time()
    duration_ms = int((time.monotonic() - started_monotonic) * 1000)
    result.tool_call_started_at = datetime.fromtimestamp(started_wall_clock).isoformat()
    result.tool_call_finished_at = datetime.fromtimestamp(finished_wall_clock).isoformat()
    result.tool_call_duration_ms = duration_ms
    if not _result_debug_enabled:
        return
    debug = result.debug if isinstance(result.debug, dict) else {}
    network = _get_network_debug_snapshot()
    debug["network"] = network
    debug["cache"] = _get_cache_debug_snapshot()
    timing = {
        "total_ms": duration_ms,
        "network_ms": int(network.get("http_total_ms", 0)),
        "non_network_ms": max(0, duration_ms - int(network.get("http_total_ms", 0))),
    }
    if extra_timing:
        timing.update({k: int(v) for k, v in extra_timing.items()})
    debug["timing"] = timing
    result.debug = debug


def _attach_task_debug(result: BaseResult, task_record: Any):
    if not _result_debug_enabled:
        return
    if not isinstance(result, BaseResult) or task_record is None:
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


def _extract_result_format(action: Any, args_dict: Any) -> str:
    # result_format is only supported in tool entrypoints with dict args.
    if not isinstance(args_dict, dict):
        return "auto"
    result_format = str(args_dict.get("result_format", "auto")).strip().lower()
    if result_format not in {"auto", "dataframe", "raw"}:
        return "invalid"
    return result_format


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


# Max concurrent sub-calls when executing tool "batch" (help, skills, etc.); additional calls wait on the semaphore.
MAX_BATCH_CONCURRENCY = 100


async def _execute_batch_item_with_limit(
        semaphore: asyncio.Semaphore,
        call: Any,
        process_call: Callable[[Any], Awaitable[BaseResult | list[BaseResult]]],
) -> BaseResult | list[BaseResult]:
    async with semaphore:
        return await process_call(call)


async def execute_batch_calls(
        batch_calls: Any,
        process_call: Callable[[Any], Awaitable[BaseResult | list[BaseResult]]],
        *,
        max_concurrency: Optional[int] = None,
) -> BaseResult:
    """Run batch sub-calls with asyncio.gather; at most ``max_concurrency`` run at once (default MAX_BATCH_CONCURRENCY).

    When the number of batch items exceeds the limit, extra work waits until a slot is free.
    """
    if not isinstance(batch_calls, list) or not batch_calls:
        return BaseResult(
            error="batch_calls must be a non-empty list of dicts with 'action' and 'args'"
        )
    limit = MAX_BATCH_CONCURRENCY if max_concurrency is None else max_concurrency
    if limit < 1:
        limit = 1
    semaphore = asyncio.Semaphore(limit)
    results = await asyncio.gather(
        *(
            _execute_batch_item_with_limit(semaphore, call, process_call)
            for call in batch_calls
        ),
        return_exceptions=True,
    )
    processed_results = [
        r if not isinstance(r, Exception) else BaseResult(error=f"Unhandled exception: {str(r)}")
        for r in results
    ]
    return BaseResult(result=processed_results)


async def process_batch_sub_action(
        call: Dict[str, Any],
        dispatch_sub_action: Callable[[str, Dict[str, Any]], Awaitable[BaseResult | list[BaseResult]]],
        support_message: Optional[str] = None,
) -> BaseResult | list[BaseResult]:
    sub_action = call.get("action", "")
    raw_sub_args = call.get("args", {})
    sub_args = dict(raw_sub_args) if isinstance(raw_sub_args, dict) else {}
    force_task_token = _force_task_response_context.set(True)
    try:
        return await dispatch_sub_action(sub_action, sub_args)
    except httpx.HTTPStatusError:
        return BaseResult(error=f"HTTP error in sub-action {sub_action}: {traceback.format_exc()}")
    except Exception:
        suffix = f"\n{support_message}" if support_message else ""
        return BaseResult(error=f"Error in sub-action {sub_action}: {traceback.format_exc()}{suffix}")
    finally:
        _force_task_response_context.reset(force_task_token)


def get_resources_path():
    try:
        resources_path = resources.files("resources")
    except ModuleNotFoundError:
        # Fallback for development or if not installed as package
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        resources_path = Path(base_path) / 'resources'
    return resources_path


class Confirmation(BaseModel):
    pass  # Empty model with no fields for simple accept/cancel without UI elements


def register_confirm_mode(confirm_mode_value: ConfirmMode):
    global _confirm_mode
    _confirm_mode = confirm_mode_value


def get_confirm_mode() -> ConfirmMode:
    global _confirm_mode
    return _confirm_mode


def operation_need_confirmation(operation: Operations) -> bool:
    confirm_mode = get_confirm_mode()
    if confirm_mode == ConfirmMode.DELETE and operation in [Operations.DELETE]:
        return True
    elif confirm_mode == ConfirmMode.CUD and operation in [Operations.CREATE, Operations.UPDATE, Operations.DELETE]:
        return True
    else:
        return False


def _cache_scope_from_instance(instance: Any) -> str:
    token = getattr(instance, "token", None)
    token_id = getattr(token, "id", "anonymous")
    return f"{instance.__class__.__name__}:{token_id}"


def _cache_compact_value(value: Any) -> str:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return repr(value)
    if isinstance(value, dict):
        keys = sorted(value.keys(), key=lambda x: str(x))
        return "{" + ",".join(f"{k}:{_cache_compact_value(value[k])}" for k in keys) + "}"
    if isinstance(value, (list, tuple, set)):
        return "[" + ",".join(_cache_compact_value(v) for v in value) + "]"
    return repr(value)


def _cleanup_expired_cache_entries(now: Optional[float] = None):
    current = now if now is not None else time.monotonic()
    expired_keys = [key for key, (expires_at, _) in _method_cache.items() if expires_at <= current]
    for key in expired_keys:
        _method_cache.pop(key, None)


def _trim_cache_size_if_needed():
    if len(_method_cache) <= _method_cache_max_entries:
        return
    # Keep entries with the longest remaining TTL.
    sorted_entries = sorted(_method_cache.items(), key=lambda item: item[1][0], reverse=True)
    _method_cache.clear()
    for key, value in sorted_entries[:_method_cache_max_entries]:
        _method_cache[key] = value


def ttl_cache_method(ttl_seconds: int = 30):
    """
    Async TTL cache decorator for manager instance methods.
    Caches successful results only and prevents duplicate concurrent fetches.
    """

    def decorator(func: Callable[..., Awaitable[Any]]):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            scope = _cache_scope_from_instance(self)
            cache_key = (
                f"{scope}:{func.__module__}.{func.__qualname__}:"
                f"args={_cache_compact_value(args)}:kwargs={_cache_compact_value(kwargs)}"
            )
            now = time.monotonic()
            cache_hit = False
            cached_value = None
            shared_future: Optional[asyncio.Future] = None
            is_owner = False

            lock_wait_started = time.monotonic()
            async with _method_cache_lock:
                _accumulate_cache_debug("lock_wait_ms", int((time.monotonic() - lock_wait_started) * 1000))
                _cleanup_expired_cache_entries(now)
                cached_entry = _method_cache.get(cache_key)
                if cached_entry and cached_entry[0] > now:
                    cache_hit = True
                    cached_value = cached_entry[1]
                else:
                    shared_future = _method_cache_inflight.get(cache_key)
                    if shared_future is None:
                        shared_future = asyncio.get_running_loop().create_future()
                        _method_cache_inflight[cache_key] = shared_future
                        is_owner = True
                        _accumulate_cache_debug("misses", 1)
                    else:
                        is_owner = False

            if cache_hit:
                _accumulate_cache_debug("hits", 1)
                dc_started = time.monotonic()
                copied = copy.deepcopy(cached_value)
                _accumulate_cache_debug("deepcopy_ms", int((time.monotonic() - dc_started) * 1000))
                return copied

            if not is_owner and shared_future is not None:
                shared_wait_started = time.monotonic()
                shared_result = await shared_future
                _accumulate_cache_debug("shared_wait_ms", int((time.monotonic() - shared_wait_started) * 1000))
                dc_started = time.monotonic()
                copied = copy.deepcopy(shared_result)
                _accumulate_cache_debug("deepcopy_ms", int((time.monotonic() - dc_started) * 1000))
                return copied

            try:
                result = await func(self, *args, **kwargs)
                should_cache = not (isinstance(result, BaseResult) and result.error)
                dc_started = time.monotonic()
                cached_copy = copy.deepcopy(result) if should_cache else None
                shared_copy = copy.deepcopy(result)
                _accumulate_cache_debug("deepcopy_ms", int((time.monotonic() - dc_started) * 1000))

                async with _method_cache_lock:
                    if should_cache:
                        _method_cache[cache_key] = (time.monotonic() + ttl_seconds, cached_copy)
                        _trim_cache_size_if_needed()

                    current_future = _method_cache_inflight.pop(cache_key, None)
                    if current_future is not None and not current_future.done():
                        current_future.set_result(shared_copy)
                return result
            except Exception as exc:
                async with _method_cache_lock:
                    current_future = _method_cache_inflight.pop(cache_key, None)
                    if current_future is not None and not current_future.done():
                        current_future.set_exception(exc)
                raise

        return wrapper

    return decorator


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
            need_confirmation = operation_need_confirmation(operation)
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


async def execute_with_task_management(
        action_payload: Dict[str, Any],
        coro_factory: Callable[[], Awaitable[Any]],
        time_to_live_ms: Optional[int] = None,
        fast_response_threshold_seconds: float = 5.0
) -> BaseResult:
    # Deferred import avoids circular dependency: utils → async_task_manager → dataframe_manager → utils.
    from tools.async_task_manager import submit_task, get_task_record, remove_task, task_snapshot

    wait_started = time.monotonic()
    try:
        task_id = submit_task(action_payload, coro_factory, time_to_live_ms=time_to_live_ms)
    except RuntimeError as exc:
        return BaseResult(error=str(exc))
    task_record = get_task_record(task_id)
    if not task_record or not task_record.asyncio_task:
        return BaseResult(error="Task could not be scheduled.")

    try:
        await asyncio.wait_for(asyncio.shield(task_record.asyncio_task), timeout=fast_response_threshold_seconds)
        latest_record = get_task_record(task_id)
        if not latest_record or latest_record.result is None:
            remove_task(task_id)
            return BaseResult(error="Task finished without result.")
        final_result = latest_record.result
        _attach_task_debug(final_result, latest_record)
        if isinstance(final_result.debug, dict):
            final_result.debug.setdefault("task", {})
            final_result.debug["task"]["sync_wait_ms"] = int((time.monotonic() - wait_started) * 1000)
        remove_task(task_id)
        return final_result
    except asyncio.TimeoutError:
        latest_record = get_task_record(task_id)
        if not latest_record:
            return BaseResult(error="Task was not found after scheduling.")
        snapshot = task_snapshot(latest_record, include_result=False)
        timeout_result = BaseResult(
            result=[snapshot],
            info=[
                "Long-running operation accepted. Use blazemeter_tools with action 'tasks_status' to monitor status."
            ]
        )
        _attach_task_debug(timeout_result, latest_record)
        if isinstance(timeout_result.debug, dict):
            timeout_result.debug.setdefault("task", {})
            timeout_result.debug["task"]["sync_wait_ms"] = int((time.monotonic() - wait_started) * 1000)
        return timeout_result


def _serialize_action_value(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _serialize_action_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize_action_value(v) for v in value]
    return repr(value)


def run_as_task(
        time_to_live_ms: Optional[int] = None,
        fast_response_threshold_seconds: float = 5.0
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
                # Keep all user-provided parameters with names for richer task context.
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
            }

            token = _task_management_enabled.set(True)
            try:
                effective_fast_response_threshold = (
                    0.0 if _force_task_response_context.get() else fast_response_threshold_seconds
                )
                coro_factory = lambda: func(self, *args, **kwargs)
                return await execute_with_task_management(
                    action_payload=action_payload,
                    coro_factory=coro_factory,
                    time_to_live_ms=time_to_live_ms,
                    fast_response_threshold_seconds=effective_fast_response_threshold
                )
            finally:
                _task_management_enabled.reset(token)

        return wrapper

    return decorator


def tool_result(excluded_actions: Optional[set[str]] = None):
    excluded = excluded_actions or set()

    def decorator(func: Callable[..., Awaitable[BaseResult]]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> ToolResult | CallToolResult:
            def _to_tool_result(value: Any) -> ToolResult | CallToolResult:
                if isinstance(value, ToolResult):
                    return value
                if isinstance(value, CallToolResult):
                    return value
                if isinstance(value, BaseResult):
                    return ToolResult.from_base_result(value)
                return ToolResult.from_base_result(BaseResult(result=[value]))

            started_monotonic = time.monotonic()
            started_wall_clock = time.time()
            network_token = _start_network_debug_scope()
            cache_token = _start_cache_debug_scope()
            result_format_token = _result_format_context.set("auto")
            try:
                result = await func(*args, **kwargs)
                after_func_monotonic = time.monotonic()
                if not isinstance(result, BaseResult) or result.error or result.result is None:
                    if isinstance(result, BaseResult):
                        _set_tool_call_timing(
                            result,
                            started_monotonic,
                            started_wall_clock,
                            extra_timing={
                                "manager_logic_ms": int((after_func_monotonic - started_monotonic) * 1000),
                                "postprocess_ms": 0,
                            },
                        )
                    return _to_tool_result(result)

                action = kwargs.get("action")
                if action is None and len(args) > 0:
                    action = args[0]
                tool_args = kwargs.get("args")
                if tool_args is None and len(args) > 1:
                    tool_args = args[1]

                result_format = _extract_result_format(action, tool_args)
                if result_format == "invalid":
                    invalid = BaseResult(
                        error="Invalid result_format value. Allowed values: auto, dataframe, raw."
                    )
                    _set_tool_call_timing(
                        invalid,
                        started_monotonic,
                        started_wall_clock,
                        extra_timing={
                            "manager_logic_ms": int((after_func_monotonic - started_monotonic) * 1000),
                            "postprocess_ms": 0,
                        },
                    )
                    return _to_tool_result(invalid)
                if isinstance(action, str) and action == "batch":
                    # Batch envelopes must remain inline results; do not materialize as dataframe.
                    result_format = "raw"
                _result_format_context.reset(result_format_token)
                result_format_token = _result_format_context.set(result_format)

                if result_format == "auto" and isinstance(action, str) and action in excluded:
                    _set_tool_call_timing(
                        result,
                        started_monotonic,
                        started_wall_clock,
                        extra_timing={
                            "manager_logic_ms": int((after_func_monotonic - started_monotonic) * 1000),
                            "postprocess_ms": 0,
                        },
                    )
                    return _to_tool_result(result)

                try:
                    postprocess_started = time.monotonic()
                    if result_format == "raw":
                        final_result = result
                    else:
                        from tools.dataframe_manager import materialize_large_result_if_needed

                        final_result = await materialize_large_result_if_needed(
                            base_result=result,
                            origin_manager=func.__name__,
                            origin_action=str(action) if action is not None else "unknown",
                            force=(result_format == "dataframe"),
                        )
                    _set_tool_call_timing(
                        final_result,
                        started_monotonic,
                        started_wall_clock,
                        extra_timing={
                            "manager_logic_ms": int((after_func_monotonic - started_monotonic) * 1000),
                            "postprocess_ms": int((time.monotonic() - postprocess_started) * 1000),
                        },
                    )
                    return _to_tool_result(final_result)
                except Exception as exc:
                    failure_result = BaseResult(
                        error=(
                            f"Large result materialization failed: {exc}. "
                            "Try reducing the scope or filters and retry."
                        )
                    )
                    _set_tool_call_timing(
                        failure_result,
                        started_monotonic,
                        started_wall_clock,
                        extra_timing={
                            "manager_logic_ms": int((after_func_monotonic - started_monotonic) * 1000),
                            "postprocess_ms": 0,
                        },
                    )
                    return _to_tool_result(failure_result)
            finally:
                _network_debug_context.reset(network_token)
                _cache_debug_context.reset(cache_token)
                _result_format_context.reset(result_format_token)

        return wrapper

    return decorator


# Backward-compatible alias. Prefer using tool_result in new code.
dataframe_result = tool_result
