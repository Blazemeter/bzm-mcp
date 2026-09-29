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

import pytest

from config.cache import (
    CacheScope,
    InMemoryTTLCache,
    NullCache,
    StorePlan,
    build_cache_from_env,
    build_cache_key,
)


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def _cache(**kwargs):
    kwargs.setdefault("sweep_interval_seconds", 0)
    return InMemoryTTLCache(**kwargs)


def test_get_returns_copies_so_callers_cannot_mutate_the_entry():
    async def scenario():
        cache = _cache()
        await cache.set("k", {"items": [1]}, 30)
        first = await cache.get("k")
        first.value["items"].append(2)
        second = await cache.get("k")
        assert second.value == {"items": [1]}

    asyncio.run(scenario())


def test_expired_entry_is_a_miss_and_is_dropped_on_read():
    async def scenario():
        clock = FakeClock()
        cache = _cache(clock=clock)
        await cache.set("k", "v", 30)
        clock.advance(30)
        assert await cache.get("k") is None
        assert len(cache) == 0

    asyncio.run(scenario())


def test_sweep_removes_only_expired_entries_in_batches():
    async def scenario():
        clock = FakeClock()
        cache = _cache(clock=clock, sweep_batch_size=2)
        for index in range(5):
            await cache.set(f"old-{index}", index, 10)
        await cache.set("fresh", "v", 100)
        clock.advance(11)
        removed = await cache.sweep()
        assert removed == 5
        assert len(cache) == 1
        assert (await cache.get("fresh")).value == "v"

    asyncio.run(scenario())


def test_overwrite_keeps_new_value_when_old_heap_item_expires():
    async def scenario():
        clock = FakeClock()
        cache = _cache(clock=clock)
        await cache.set("k", "old", 10)
        await cache.set("k", "new", 100)
        clock.advance(11)
        assert await cache.sweep() == 0
        assert (await cache.get("k")).value == "new"

    asyncio.run(scenario())


def test_lru_eviction_drops_least_recently_used_entry():
    async def scenario():
        cache = _cache(max_entries=2)
        await cache.set("a", 1, 30)
        await cache.set("b", 2, 30)
        await cache.get("a")  # "b" becomes least recently used
        await cache.set("c", 3, 30)
        assert await cache.get("b") is None
        assert (await cache.get("a")).value == 1
        assert (await cache.get("c")).value == 3

    asyncio.run(scenario())


def test_non_positive_ttl_does_not_store():
    async def scenario():
        cache = _cache()
        await cache.set("k", "v", 0)
        assert await cache.get("k") is None

    asyncio.run(scenario())


def test_get_or_load_single_flight_for_concurrent_misses():
    async def scenario():
        cache = _cache()
        calls = {"count": 0}

        async def loader():
            calls["count"] += 1
            await asyncio.sleep(0.02)
            return {"value": 1}

        results = await asyncio.gather(*(cache.get_or_load("k", loader, 30) for _ in range(5)))
        assert calls["count"] == 1
        assert all(result == {"value": 1} for result in results)
        # Each caller got its own copy.
        results[0]["value"] = 99
        assert results[1] == {"value": 1}

    asyncio.run(scenario())


def test_get_or_load_does_not_store_failures():
    async def scenario():
        cache = _cache()
        calls = {"count": 0}

        async def loader():
            calls["count"] += 1
            raise RuntimeError("boom")

        for _ in range(2):
            with pytest.raises(RuntimeError):
                await cache.get_or_load("k", loader, 30)
        assert calls["count"] == 2
        assert await cache.get("k") is None

    asyncio.run(scenario())


def test_store_policy_none_skips_storing():
    async def scenario():
        cache = _cache()
        calls = {"count": 0}

        async def loader():
            calls["count"] += 1
            return "v"

        for _ in range(2):
            await cache.get_or_load("k", loader, 30, store_policy=lambda _value: None)
        assert calls["count"] == 2

    asyncio.run(scenario())


def test_cancelled_owner_does_not_leave_waiters_hanging():
    async def scenario():
        cache = _cache()
        started = asyncio.Event()
        calls = {"count": 0}

        async def slow_loader():
            calls["count"] += 1
            started.set()
            await asyncio.sleep(10)
            return "never"

        async def fast_loader():
            calls["count"] += 1
            return "ok"

        owner = asyncio.create_task(cache.get_or_load("k", slow_loader, 30))
        await started.wait()
        waiter = asyncio.create_task(cache.get_or_load("k", fast_loader, 30))
        await asyncio.sleep(0)
        owner.cancel()
        with pytest.raises(asyncio.CancelledError):
            await owner
        assert await asyncio.wait_for(waiter, timeout=1) == "ok"
        # The key is free again and holds the waiter's value.
        assert (await cache.get("k")).value == "ok"

    asyncio.run(scenario())


def test_bound_entry_is_a_miss_for_another_binding():
    async def scenario():
        cache = _cache()
        calls = {"count": 0}

        async def loader():
            calls["count"] += 1
            return f"value-{calls['count']}"

        bound = lambda _value: StorePlan(bound_to="session-a")
        first = await cache.get_or_load("k", loader, 30, store_policy=bound, binding="session-a")
        again = await cache.get_or_load("k", loader, 30, store_policy=bound, binding="session-a")
        other = await cache.get_or_load("k", loader, 30, store_policy=lambda _v: None, binding="session-b")
        assert first == again == "value-1"
        assert other == "value-2"

    asyncio.run(scenario())


def test_shared_value_bound_to_another_binding_is_not_handed_to_waiter():
    async def scenario():
        cache = _cache()
        release = asyncio.Event()

        async def owner_loader():
            await release.wait()
            return "session-a-value"

        async def waiter_loader():
            return "session-b-value"

        owner = asyncio.create_task(
            cache.get_or_load(
                "k", owner_loader, 30,
                store_policy=lambda _v: StorePlan(bound_to="session-a"),
                binding="session-a",
            )
        )
        await asyncio.sleep(0)
        waiter = asyncio.create_task(cache.get_or_load("k", waiter_loader, 30, binding="session-b"))
        await asyncio.sleep(0)
        release.set()
        assert await owner == "session-a-value"
        assert await waiter == "session-b-value"

    asyncio.run(scenario())


def test_after_store_runs_once_the_value_is_stored():
    async def scenario():
        cache = _cache()
        seen = []

        async def after_store():
            seen.append((await cache.get("k")).value)

        await cache.get_or_load(
            "k", lambda: asyncio.sleep(0, result="v"), 30,
            store_policy=lambda _v: StorePlan(after_store=after_store),
        )
        assert seen == ["v"]

    asyncio.run(scenario())


def test_background_sweeper_removes_expired_entries_and_stops_on_close():
    async def scenario():
        cache = InMemoryTTLCache(sweep_interval_seconds=0.01)
        await cache.set("k", "v", 0.02)
        await asyncio.sleep(0.1)
        assert len(cache) == 0
        await cache.close()
        assert cache._gc_task is None

    asyncio.run(scenario())


def test_null_cache_never_stores_or_shares():
    async def scenario():
        cache = NullCache()
        calls = {"count": 0}

        async def loader():
            calls["count"] += 1
            await asyncio.sleep(0.01)
            return "v"

        await asyncio.gather(cache.get_or_load("k", loader, 30), cache.get_or_load("k", loader, 30))
        assert calls["count"] == 2
        assert await cache.get("k") is None

    asyncio.run(scenario())


def test_user_keys_require_a_user_id_and_are_namespaced():
    assert build_cache_key(CacheScope.USER, "m", "a", user_id="u1") == "user:u1:m:a"
    assert build_cache_key(CacheScope.GLOBAL, "help", "index") == "global:help:index"
    with pytest.raises(ValueError):
        build_cache_key(CacheScope.USER, "m", user_id="")
    with pytest.raises(ValueError):
        build_cache_key(CacheScope.USER, "m", user_id=None)


def test_build_cache_from_env(monkeypatch):
    monkeypatch.setenv("BZM_CACHE_ENABLED", "false")
    assert isinstance(build_cache_from_env(), NullCache)

    monkeypatch.setenv("BZM_CACHE_ENABLED", "true")
    monkeypatch.setenv("BZM_CACHE_MAX_ENTRIES", "7")
    monkeypatch.setenv("BZM_CACHE_SWEEP_INTERVAL_SECONDS", "not-a-number")
    cache = build_cache_from_env()
    assert isinstance(cache, InMemoryTTLCache)
    assert cache._max_entries == 7
    assert cache._sweep_interval == 30.0


def test_store_failure_serves_the_value_and_keeps_the_key_free():
    async def scenario():
        cache = _cache()

        async def failing_after_store():
            raise RuntimeError("hook failed")

        value = await cache.get_or_load(
            "k", lambda: asyncio.sleep(0, result="v"), 30,
            store_policy=lambda _v: StorePlan(after_store=failing_after_store),
        )
        assert value == "v"
        assert await cache.get("k") is None
        assert cache._inflight == {}

    asyncio.run(scenario())


def test_delete_if_tag_only_removes_the_matching_entry():
    async def scenario():
        cache = _cache()
        await cache.set("k", "snapshot", 30, tag="task-a")
        await cache.set("k", "newer", 30, tag="task-b")
        assert await cache.delete("k", if_tag="task-a") is False
        assert (await cache.get("k")).value == "newer"
        assert await cache.delete("k", if_tag="task-b") is True
        assert await cache.get("k") is None

    asyncio.run(scenario())


def test_read_only_entries_are_not_copied():
    async def scenario():
        cache = _cache()
        index = {"tree": {"a": [1]}}
        loaded = await cache.get_or_load(
            "k", lambda: asyncio.sleep(0, result=index), 30,
            store_policy=lambda _v: StorePlan(copy_values=False),
        )
        hit = await cache.get_or_load("k", lambda: asyncio.sleep(0, result=None), 30)
        assert loaded is index
        assert hit is index

    asyncio.run(scenario())


def test_transform_applies_to_the_stored_value_only():
    async def scenario():
        cache = _cache()

        def strip(value):
            value.pop("debug")
            return value

        owner = await cache.get_or_load(
            "k", lambda: asyncio.sleep(0, result={"data": 1, "debug": {"ms": 5}}), 30,
            store_policy=lambda _v: StorePlan(transform=strip),
        )
        assert owner == {"data": 1, "debug": {"ms": 5}}
        assert (await cache.get("k")).value == {"data": 1}

    asyncio.run(scenario())
