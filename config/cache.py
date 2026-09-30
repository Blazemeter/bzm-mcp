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
import heapq
import json
import logging
import os
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import quote

import httpx

from config import cache_codec

logger = logging.getLogger(__name__)

DEFAULT_MAX_ENTRIES = 2048
DEFAULT_SWEEP_INTERVAL_SECONDS = 30.0
DEFAULT_SWEEP_BATCH_SIZE = 500
DEFAULT_HTTP_TIMEOUT_SECONDS = 2.0
# Match the storage API BZM_STORAGE_CACHE_MAX_VALUE_BYTES (request body limit).
DEFAULT_HTTP_MAX_VALUE_BYTES = 1048576

CacheObserver = Callable[[str, int], None]


class CacheScope(str, Enum):
    """
    Who may reuse a cache entry.

    USER: only the user identified in the request context. Without a user id the
    cache is bypassed, so entries can never be shared across users by accident.
    GLOBAL: any caller. Only for content that does not depend on the caller
    (help pages, static assets).
    """

    USER = "user"
    GLOBAL = "global"


def build_cache_key(
        scope: CacheScope,
        namespace: str,
        *parts: str,
        user_id: Optional[str] = None,
) -> str:
    """Build a namespaced key; USER keys require a non-empty user id."""
    if scope is CacheScope.USER:
        if not user_id or not str(user_id).strip():
            raise ValueError("USER-scoped cache keys require a user id.")
        prefix = f"{scope.value}:{str(user_id).strip()}"
    else:
        prefix = scope.value
    return ":".join([prefix, namespace, *parts])


@dataclass(frozen=True)
class CacheEntry:
    value: Any
    # Set when the value is only valid for one session binding (e.g. a task
    # snapshot or a session dataframe reference). None means shareable.
    bound_to: Optional[str] = None
    # Opaque owner marker so a writer can later delete only its own entry.
    tag: Optional[str] = None

    def accepts(self, binding: Optional[str]) -> bool:
        return self.bound_to is None or self.bound_to == binding


@dataclass(frozen=True)
class StorePlan:
    """How get_or_load stores a freshly loaded value."""

    ttl_seconds: Optional[float] = None
    bound_to: Optional[str] = None
    tag: Optional[str] = None
    # False for large read-only values (e.g. static indexes): no copy in or out,
    # so every reader must treat the value as immutable.
    copy_values: bool = True
    # Applied to a copy of the loaded value before storing (e.g. strip per-call debug).
    # Waiters sharing the load receive the transformed value as well.
    transform: Optional[Callable[[Any], Any]] = None
    after_store: Optional[Callable[[], Awaitable[None]]] = None


StorePolicy = Callable[[Any], Optional[StorePlan]]


def _store_always(_value: Any) -> StorePlan:
    return StorePlan()


def _notify(observer: Optional[CacheObserver], metric: str, value: int) -> None:
    if observer is None:
        return
    try:
        observer(metric, value)
    except Exception:
        logger.debug("cache observer failed", exc_info=True)


class CachePort(ABC):
    """
    Key/value cache with per-entry TTL.

    Adapters own storage and expiry. ``get_or_load`` adds process-local
    single-flight on top, so an adapter backed by a shared cache service only
    has to implement get/set/delete/clear.
    """

    def __init__(self) -> None:
        self._inflight: dict[str, asyncio.Future] = {}

    @abstractmethod
    async def get(self, key: str) -> Optional[CacheEntry]:
        raise NotImplementedError

    @abstractmethod
    async def set(
            self,
            key: str,
            value: Any,
            ttl_seconds: float,
            *,
            bound_to: Optional[str] = None,
            tag: Optional[str] = None,
            copy_values: bool = True,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str, *, if_tag: Optional[str] = None) -> bool:
        """Delete ``key``; with ``if_tag``, only while the entry still carries that tag."""
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        raise NotImplementedError

    async def start(self) -> None:
        """Start background maintenance, if the adapter needs it."""

    async def close(self) -> None:
        """Stop background maintenance and release resources."""

    async def get_or_load(
            self,
            key: str,
            loader: Callable[[], Awaitable[Any]],
            ttl_seconds: float,
            *,
            store_policy: Optional[StorePolicy] = None,
            binding: Optional[str] = None,
            observer: Optional[CacheObserver] = None,
    ) -> Any:
        """
        Return the cached value for ``key`` or load, store and return it.

        Concurrent misses on the same key share one ``loader`` call. The owner
        releases the key in every exit path, cancellation included, so a
        cancelled load never leaves waiters hanging. ``store_policy`` decides
        whether and how the loaded value is stored (None = do not store).
        Entries bound to another ``binding`` count as a miss.
        """
        policy = store_policy or _store_always
        loop = asyncio.get_running_loop()
        while True:
            entry = await self.get(key)
            if entry is not None and entry.accepts(binding):
                _notify(observer, "hits", 1)
                return entry.value

            future = self._inflight.get(key)
            if future is None or future.get_loop() is not loop:
                break

            wait_started = time.monotonic()
            try:
                shared_value, plan = await asyncio.shield(future)
            except asyncio.CancelledError:
                current = asyncio.current_task()
                if future.cancelled() and not (current is not None and current.cancelling()):
                    # The owner was cancelled, not us: retry and possibly become the owner.
                    continue
                raise
            _notify(observer, "shared_wait_ms", int((time.monotonic() - wait_started) * 1000))
            if plan is None or plan.bound_to is None or plan.bound_to == binding:
                if plan is not None and not plan.copy_values:
                    return shared_value
                return copy.deepcopy(shared_value)
            # The shared value belongs to another binding: load our own, uncached.
            return await loader()

        future = loop.create_future()
        self._inflight[key] = future
        _notify(observer, "misses", 1)
        try:
            value = await loader()
        except BaseException as exc:
            if self._inflight.get(key) is future:
                del self._inflight[key]
            if not future.done():
                if isinstance(exc, asyncio.CancelledError):
                    future.cancel()
                else:
                    future.set_exception(exc)
                    future.exception()  # mark retrieved; waiters still receive it
            raise

        # Caching is best effort: a failure here never fails a load that already succeeded.
        plan: Optional[StorePlan] = None
        stored = False
        shared_value = value
        try:
            plan = policy(value)
            if plan is not None:
                if plan.transform is not None:
                    shared_value = plan.transform(copy.deepcopy(value))
                ttl = plan.ttl_seconds if plan.ttl_seconds is not None else ttl_seconds
                await self.set(
                    key,
                    shared_value,
                    ttl,
                    bound_to=plan.bound_to,
                    tag=plan.tag,
                    copy_values=plan.copy_values,
                )
                stored = True
                if plan.after_store is not None:
                    await plan.after_store()
        except Exception:
            logger.warning("cache store failed for key %s; serving uncached result", key, exc_info=True)
            if plan is None:
                # Unknown binding: share only with waiters of the same binding.
                plan = StorePlan(bound_to=binding)
            if stored:
                # The entry may lack its invalidation hook (after_store failed): drop it.
                try:
                    await self.delete(key, if_tag=plan.tag)
                except Exception:
                    logger.warning("cache delete failed for key %s", key, exc_info=True)
        finally:
            if self._inflight.get(key) is future:
                del self._inflight[key]
            if not future.done():
                copy_shared = plan is None or plan.copy_values
                future.set_result((copy.deepcopy(shared_value) if copy_shared else shared_value, plan))
        return value


class NullCache(CachePort):
    """Cache disabled: every lookup misses and nothing is shared."""

    async def get(self, key: str) -> Optional[CacheEntry]:
        return None

    async def set(self, key: str, value: Any, ttl_seconds: float, *, bound_to=None, tag=None, copy_values=True) -> None:
        return None

    async def delete(self, key: str, *, if_tag: Optional[str] = None) -> bool:
        return False

    async def clear(self) -> None:
        return None

    async def get_or_load(self, key, loader, ttl_seconds, *, store_policy=None, binding=None, observer=None):
        return await loader()


@dataclass
class _Slot:
    value: Any
    expires_at: float
    bound_to: Optional[str]
    generation: int
    tag: Optional[str] = None
    copy_values: bool = True


class InMemoryTTLCache(CachePort):
    """
    Process-local cache (stdio and a single hosted worker).

    - LRU order in an OrderedDict: hits and overflow eviction are O(1).
    - Expiry heap (expires_at, generation, key): the sweeper pops only expired
      entries; stale heap items are skipped by generation.
    - Reads drop an expired entry on the spot, so correctness never waits for
      the sweeper.
    - The sweeper is an asyncio task on the running loop. All mutations happen
      on that loop between awaits, so the store needs no locks; the sweeper
      yields every ``sweep_batch_size`` entries to keep the loop responsive.
    - Values are deep-copied in and out so callers cannot mutate shared state,
      unless stored with ``copy_values=False`` (read-only values).
    """

    def __init__(
            self,
            *,
            max_entries: int = DEFAULT_MAX_ENTRIES,
            sweep_interval_seconds: float = DEFAULT_SWEEP_INTERVAL_SECONDS,
            sweep_batch_size: int = DEFAULT_SWEEP_BATCH_SIZE,
            clock: Callable[[], float] = time.monotonic,
    ) -> None:
        super().__init__()
        self._max_entries = max(1, int(max_entries))
        self._sweep_interval = float(sweep_interval_seconds)
        self._sweep_batch_size = max(1, int(sweep_batch_size))
        self._clock = clock
        self._data: OrderedDict[str, _Slot] = OrderedDict()
        self._heap: list[tuple[float, int, str]] = []
        self._generation = 0
        self._gc_task: Optional[asyncio.Task] = None
        self._gc_loop: Optional[asyncio.AbstractEventLoop] = None

    def __len__(self) -> int:
        return len(self._data)

    async def get(self, key: str) -> Optional[CacheEntry]:
        self._ensure_gc()
        slot = self._data.get(key)
        if slot is None:
            return None
        if slot.expires_at <= self._clock():
            del self._data[key]
            return None
        self._data.move_to_end(key)
        value = copy.deepcopy(slot.value) if slot.copy_values else slot.value
        return CacheEntry(value=value, bound_to=slot.bound_to, tag=slot.tag)

    async def set(
            self,
            key: str,
            value: Any,
            ttl_seconds: float,
            *,
            bound_to: Optional[str] = None,
            tag: Optional[str] = None,
            copy_values: bool = True,
    ) -> None:
        if ttl_seconds is None or ttl_seconds <= 0:
            self._data.pop(key, None)
            return
        self._ensure_gc()
        self._generation += 1
        expires_at = self._clock() + float(ttl_seconds)
        self._data[key] = _Slot(
            value=copy.deepcopy(value) if copy_values else value,
            expires_at=expires_at,
            bound_to=bound_to,
            generation=self._generation,
            tag=tag,
            copy_values=copy_values,
        )
        self._data.move_to_end(key)
        heapq.heappush(self._heap, (expires_at, self._generation, key))
        while len(self._data) > self._max_entries:
            self._data.popitem(last=False)
        self._maybe_compact_heap()

    async def delete(self, key: str, *, if_tag: Optional[str] = None) -> bool:
        slot = self._data.get(key)
        if slot is None or (if_tag is not None and slot.tag != if_tag):
            return False
        del self._data[key]
        return True

    async def clear(self) -> None:
        self._data.clear()
        self._heap.clear()

    async def sweep(self) -> int:
        """Remove expired entries in batches; returns how many were removed."""
        removed = 0
        processed = 0
        now = self._clock()
        while self._heap and self._heap[0][0] <= now:
            _, generation, key = heapq.heappop(self._heap)
            slot = self._data.get(key)
            if slot is not None and slot.generation == generation:
                del self._data[key]
                removed += 1
            processed += 1
            if processed % self._sweep_batch_size == 0:
                await asyncio.sleep(0)
                now = self._clock()
        return removed

    async def start(self) -> None:
        self._ensure_gc()

    async def close(self) -> None:
        task = self._gc_task
        self._gc_task = None
        self._gc_loop = None
        if task is None or task.done():
            return
        task.cancel()
        try:
            await task
        except (asyncio.CancelledError, RuntimeError):
            pass

    def _maybe_compact_heap(self) -> None:
        # Overwrites and LRU evictions leave stale heap items; rebuild when they dominate.
        if len(self._heap) <= max(64, 2 * len(self._data)):
            return
        self._heap = [(slot.expires_at, slot.generation, key) for key, slot in self._data.items()]
        heapq.heapify(self._heap)

    def _ensure_gc(self) -> None:
        if self._sweep_interval <= 0:
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        task = self._gc_task
        if task is not None and not task.done() and self._gc_loop is loop:
            return
        self._gc_loop = loop
        self._gc_task = loop.create_task(self._gc_run(), name="bzm-cache-sweeper")

    async def _gc_run(self) -> None:
        while True:
            await asyncio.sleep(self._sweep_interval)
            try:
                await self.sweep()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("cache sweeper failed; continuing")


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off"}


def _env_number(name: str, default: float, cast: Callable[[str], Any]) -> Any:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return cast(raw.strip())
    except ValueError:
        logger.warning("Invalid %s=%r; using default %s", name, raw, default)
        return default


class CacheValueTooLarge(ValueError):
    """The encoded value exceeds what the remote cache accepts; it is not cached."""


class HttpCache(CachePort):
    """
    Hosted: the cache lives behind the storage API (``/cache/entries``).

    What backs the API (in-memory today, a shared cache service later) can change
    without touching the MCP. Values go through ``cache_codec`` so a hit returns
    the same types as a local cache. Reads never raise (a failure is a miss);
    writes raise and ``get_or_load``'s best-effort store serves the value uncached.
    Values larger than ``max_value_bytes`` are rejected here, without a request.
    """

    def __init__(
            self,
            base_url: str,
            caller_token: str,
            *,
            timeout_seconds: float = DEFAULT_HTTP_TIMEOUT_SECONDS,
            max_value_bytes: int = DEFAULT_HTTP_MAX_VALUE_BYTES,
            transport: Optional[httpx.AsyncBaseTransport] = None,
    ) -> None:
        super().__init__()
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {caller_token}"}
        self._timeout = timeout_seconds
        self._max_value_bytes = max_value_bytes
        self._transport = transport
        self._client: Optional[httpx.AsyncClient] = None
        self._client_loop: Optional[asyncio.AbstractEventLoop] = None
        self._degraded = False

    def _http(self) -> httpx.AsyncClient:
        # One pooled client per event loop (a pool cannot be shared across loops).
        loop = asyncio.get_running_loop()
        if self._client is None or self._client_loop is not loop or self._client.is_closed:
            self._retire_client()
            if self._transport is not None:
                self._client = httpx.AsyncClient(transport=self._transport, timeout=self._timeout)
            else:
                self._client = httpx.AsyncClient(http2=True, timeout=self._timeout)
            self._client_loop = loop
        return self._client

    def _retire_client(self) -> None:
        client, loop = self._client, self._client_loop
        self._client, self._client_loop = None, None
        if client is None or client.is_closed:
            return
        # A client can only be closed on its own loop; a finished loop already
        # released its connections.
        if loop is not None and not loop.is_closed() and loop.is_running():
            asyncio.run_coroutine_threadsafe(client.aclose(), loop)

    def _url(self, key: str) -> str:
        return f"{self._base_url}/cache/entries/{quote(key, safe='')}"

    def _report_failure(self, operation: str, key: Optional[str], exc: BaseException) -> None:
        status = exc.response.status_code if isinstance(exc, httpx.HTTPStatusError) else None
        if status in (401, 403):
            if not self._degraded:
                logger.error(
                    "remote cache rejected the MCP caller (HTTP %s): check the storage caller "
                    "token. The cache is effectively disabled until this is fixed.", status,
                )
        elif not self._degraded:
            logger.warning(
                "remote cache %s failed (key %s); serving without cache until it recovers",
                operation, key, exc_info=True,
            )
        else:
            logger.debug("remote cache %s failed (key %s): %s", operation, key, exc)
        self._degraded = True

    def _report_success(self) -> None:
        if self._degraded:
            logger.info("remote cache recovered")
            self._degraded = False

    async def get(self, key: str) -> Optional[CacheEntry]:
        try:
            response = await self._http().get(self._url(key), headers=self._headers)
            if response.status_code == 404:
                self._report_success()
                return None
            response.raise_for_status()
            body = response.json()
            entry = CacheEntry(
                value=cache_codec.decode(body.get("value")),
                bound_to=body.get("bound_to"),
                tag=body.get("tag"),
            )
        except Exception as exc:
            self._report_failure("read", key, exc)
            return None
        self._report_success()
        return entry

    async def set(
            self,
            key: str,
            value: Any,
            ttl_seconds: float,
            *,
            bound_to: Optional[str] = None,
            tag: Optional[str] = None,
            copy_values: bool = True,
    ) -> None:
        # copy_values does not apply: a remote value is always a fresh copy.
        if ttl_seconds is None or ttl_seconds <= 0:
            await self.delete(key)
            return
        body = json.dumps(
            {
                "value": cache_codec.encode(value),
                "ttl_seconds": float(ttl_seconds),
                "bound_to": bound_to,
                "tag": tag,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        if len(body) > self._max_value_bytes:
            raise CacheValueTooLarge(
                f"Encoded cache value is {len(body)} bytes; the remote cache accepts {self._max_value_bytes}."
            )
        try:
            response = await self._http().put(
                self._url(key),
                headers={**self._headers, "Content-Type": "application/json"},
                content=body,
            )
            response.raise_for_status()
        except Exception as exc:
            self._report_failure("write", key, exc)
            raise
        self._report_success()

    async def delete(self, key: str, *, if_tag: Optional[str] = None) -> bool:
        params = {"if_tag": if_tag} if if_tag is not None else None
        try:
            response = await self._http().delete(self._url(key), headers=self._headers, params=params)
            response.raise_for_status()
            deleted = bool(response.json().get("deleted"))
        except Exception as exc:
            self._report_failure("delete", key, exc)
            return False
        self._report_success()
        return deleted

    async def clear(self) -> None:
        try:
            response = await self._http().delete(f"{self._base_url}/cache/entries", headers=self._headers)
            response.raise_for_status()
        except Exception as exc:
            self._report_failure("clear", None, exc)
            return
        self._report_success()

    async def close(self) -> None:
        client, self._client, self._client_loop = self._client, None, None
        if client is not None and not client.is_closed:
            await client.aclose()


def build_cache_from_env(
        transport: str = "stdio",
        storage_base_url: Optional[str] = None,
        caller_token: Optional[str] = None,
) -> CachePort:
    """
    Build the process cache from BZM_CACHE_* env vars.

    - stdio: in-memory (BZM_CACHE_MAX_ENTRIES 2048, BZM_CACHE_SWEEP_INTERVAL_SECONDS 30,
      BZM_CACHE_SWEEP_BATCH_SIZE 500).
    - streamable-http: only the storage API cache (BZM_CACHE_HTTP_TIMEOUT_SECONDS 2,
      BZM_CACHE_HTTP_MAX_VALUE_BYTES 1048576); no in-process state, so what backs
      the API can change without touching the MCP.
    - BZM_CACHE_ENABLED=false (default true): no cache in either transport.
    """
    if not _env_bool("BZM_CACHE_ENABLED", True):
        return NullCache()
    if transport == "streamable-http":
        if not storage_base_url or not caller_token:
            raise ValueError("The hosted cache needs the storage API base URL and caller token.")
        return HttpCache(
            storage_base_url,
            caller_token,
            timeout_seconds=_env_number(
                "BZM_CACHE_HTTP_TIMEOUT_SECONDS", DEFAULT_HTTP_TIMEOUT_SECONDS, float
            ),
            max_value_bytes=_env_number(
                "BZM_CACHE_HTTP_MAX_VALUE_BYTES", DEFAULT_HTTP_MAX_VALUE_BYTES, int
            ),
        )
    return _build_in_memory_cache()


def _build_in_memory_cache() -> InMemoryTTLCache:
    return InMemoryTTLCache(
        max_entries=_env_number("BZM_CACHE_MAX_ENTRIES", DEFAULT_MAX_ENTRIES, int),
        sweep_interval_seconds=_env_number(
            "BZM_CACHE_SWEEP_INTERVAL_SECONDS", DEFAULT_SWEEP_INTERVAL_SECONDS, float
        ),
        sweep_batch_size=_env_number("BZM_CACHE_SWEEP_BATCH_SIZE", DEFAULT_SWEEP_BATCH_SIZE, int),
    )


_cache: Optional[CachePort] = None


def configure_cache(cache: Optional[CachePort]) -> None:
    """Bind the process cache from AppRuntime (composition root)."""
    global _cache
    _cache = cache


def get_cache() -> CachePort:
    """Process cache; lazily built from env when AppRuntime did not configure one."""
    global _cache
    if _cache is None:
        _cache = build_cache_from_env()
    return _cache
