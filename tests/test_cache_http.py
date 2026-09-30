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
import json
from datetime import datetime, timezone
from urllib.parse import unquote

import httpx
import pytest
from pydantic import BaseModel

from config import cache_codec
from config.cache import (
    CacheValueTooLarge,
    HttpCache,
    InMemoryTTLCache,
    NullCache,
    StorePlan,
    build_cache_from_env,
    configure_cache,
)
from config.token import BzmToken
from models.account import Account
from models.manager import Manager
from models.result import BaseResult
from tests.conftest import make_ctx
from tools.utils import ttl_cache_method

KEY = "user:u-1:tools.account_manager.AccountManager.read:args=(42,):kwargs={}:format='auto':a/b"


class FakeStorageCache:
    """In-memory stand-in for the storage API /cache/entries contract."""

    def __init__(self):
        self.entries = {}
        self.requests = []
        self.fail_with = None

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self.fail_with:
            return httpx.Response(self.fail_with)
        if request.headers.get("authorization") != "Bearer mcp-caller":
            return httpx.Response(401)
        prefix = "/cache/entries/"
        path = request.url.raw_path.decode().split("?")[0]
        if request.method == "DELETE" and path == "/cache/entries":
            cleared = len(self.entries)
            self.entries.clear()
            return httpx.Response(200, json={"cleared": cleared})
        key = unquote(path[len(prefix):])
        if request.method == "GET":
            if key not in self.entries:
                return httpx.Response(404, json={"detail": "Cache entry not found."})
            entry = self.entries[key]
            return httpx.Response(200, json={"key": key, "expires_at": "2026-09-01T00:00:00Z", **entry})
        if request.method == "PUT":
            body = json.loads(request.content)
            self.entries[key] = {"value": body["value"], "bound_to": body["bound_to"], "tag": body["tag"]}
            return httpx.Response(200, json={"key": key, "expires_at": "2026-09-01T00:00:00Z", **self.entries[key]})
        if request.method == "DELETE":
            if_tag = request.url.params.get("if_tag")
            entry = self.entries.get(key)
            deleted = entry is not None and (if_tag is None or entry["tag"] == if_tag)
            if deleted:
                del self.entries[key]
            return httpx.Response(200, json={"key": key, "deleted": deleted})
        return httpx.Response(405)


@pytest.fixture
def remote():
    return FakeStorageCache()


@pytest.fixture
def http_cache(remote):
    return HttpCache("http://storage", "mcp-caller", transport=httpx.MockTransport(remote.handler))


def _account(account_id=42):
    return Account(account_id=account_id, account_name="Acme", description="", ai_consent=True,
                   created="2026-09-01T00:00:00+00:00", updated="2026-09-02T00:00:00+00:00")


# --- codec ----------------------------------------------------------------------


def test_codec_restores_typed_results_and_container_shapes():
    original = BaseResult(
        result=[
            _account(),
            {1: {"category": "guide"}, "__model__": "plain data, not a marker"},
            (1, "a"),
            {"x", "y"},
            datetime(2026, 9, 1, tzinfo=timezone.utc),
        ],
        total=1,
        info=["ok"],
    )
    wire = json.loads(json.dumps(cache_codec.encode(original)))  # must survive real JSON
    restored = cache_codec.decode(wire)

    assert isinstance(restored, BaseResult)
    assert isinstance(restored.result[0], Account)
    assert restored.result[0].account_id == 42  # attribute access, as bridge callers do
    assert restored.result[1] == {1: {"category": "guide"}, "__model__": "plain data, not a marker"}
    assert restored.result[2] == (1, "a")
    assert restored.result[3] == {"x", "y"}
    assert restored.result[4] == datetime(2026, 9, 1, tzinfo=timezone.utc)
    assert restored.model_dump() == original.model_dump()
    assert restored.model_fields_set == original.model_fields_set


def test_codec_only_rebuilds_allowed_models():
    class Outside(BaseModel):
        x: int = 1

    with pytest.raises(cache_codec.CacheCodecError):
        cache_codec.encode(Outside())
    with pytest.raises(cache_codec.CacheCodecError):
        cache_codec.decode({"__model__": "os:system", "fields": {}})
    with pytest.raises(cache_codec.CacheCodecError):
        cache_codec.encode(object())


# --- HttpCache adapter ----------------------------------------------------------


def test_http_cache_roundtrip_keeps_types_binding_and_tag(http_cache, remote):
    async def scenario():
        await http_cache.set(KEY, BaseResult(result=[_account()]), 30, bound_to="u-1/s-1", tag="t-1")
        assert list(remote.entries) == [KEY]  # the key with "/" and quotes arrives intact
        entry = await http_cache.get(KEY)
        assert isinstance(entry.value.result[0], Account)
        assert (entry.bound_to, entry.tag) == ("u-1/s-1", "t-1")
        assert await http_cache.delete(KEY, if_tag="other") is False
        assert await http_cache.delete(KEY, if_tag="t-1") is True
        assert await http_cache.get(KEY) is None

    asyncio.run(scenario())
    assert all(r.headers["authorization"] == "Bearer mcp-caller" for r in remote.requests)


def test_http_cache_read_failures_are_misses_not_errors(http_cache, remote):
    remote.fail_with = 503
    assert asyncio.run(http_cache.get(KEY)) is None
    assert asyncio.run(http_cache.delete(KEY)) is False


def test_get_or_load_over_http_single_flight_and_best_effort_store(http_cache, remote):
    calls = {"count": 0}

    async def loader():
        calls["count"] += 1
        await asyncio.sleep(0.01)
        return BaseResult(result=[_account()])

    async def scenario():
        results = await asyncio.gather(*(http_cache.get_or_load(KEY, loader, 30) for _ in range(3)))
        assert calls["count"] == 1
        assert all(isinstance(r.result[0], Account) for r in results)
        hit = await http_cache.get_or_load(KEY, loader, 30)
        assert calls["count"] == 1 and isinstance(hit.result[0], Account)

        remote.fail_with = 500  # storage down: still served, just not cached
        value = await http_cache.get_or_load(KEY + "-2", loader, 30)
        assert isinstance(value.result[0], Account)

    asyncio.run(scenario())


def test_uncacheable_value_is_served_but_not_stored(http_cache, remote):
    async def scenario():
        value = await http_cache.get_or_load(KEY, lambda: asyncio.sleep(0, result=object()), 30)
        assert value is not None
        assert remote.entries == {}

    asyncio.run(scenario())


def test_ttl_cache_method_hits_return_typed_models_through_the_api(http_cache, remote):
    class AccountReader(Manager):
        calls = 0

        @ttl_cache_method(ttl_seconds=30)
        async def read(self, account_id: int) -> BaseResult:
            AccountReader.calls += 1
            return BaseResult(result=[_account(account_id)])

    configure_cache(http_cache)
    try:
        manager = AccountReader(make_ctx(BzmToken("u-1", "secret"), "sess-a"))
        asyncio.run(manager.read(7))
        hit = asyncio.run(manager.read(7))
    finally:
        configure_cache(None)
    assert AccountReader.calls == 1
    assert isinstance(hit.result[0], Account) and hit.result[0].account_id == 7
    assert len(remote.entries) == 1


# --- wiring ---------------------------------------------------------------------


def test_build_cache_picks_the_backend_per_transport(monkeypatch):
    monkeypatch.delenv("BZM_CACHE_ENABLED", raising=False)
    assert isinstance(build_cache_from_env(), InMemoryTTLCache)
    hosted = build_cache_from_env("streamable-http", storage_base_url="http://storage", caller_token="t")
    # Hosted keeps no in-process cache state: everything lives behind the API.
    assert isinstance(hosted, HttpCache)
    with pytest.raises(ValueError):
        build_cache_from_env("streamable-http", storage_base_url="http://storage", caller_token="")
    monkeypatch.setenv("BZM_CACHE_ENABLED", "false")
    assert isinstance(build_cache_from_env("streamable-http"), NullCache)


# --- limits, error reporting ----------------------------------------------------


def test_oversized_value_is_rejected_without_a_request(remote):
    cache = HttpCache("http://storage", "mcp-caller", max_value_bytes=1024,
                      transport=httpx.MockTransport(remote.handler))
    with pytest.raises(CacheValueTooLarge):
        asyncio.run(cache.set(KEY, {"blob": "x" * 2048}, 30))
    assert remote.requests == []


def test_auth_failure_is_reported_once_and_recovery_is_logged(http_cache, remote, caplog):
    import logging

    caplog.set_level(logging.DEBUG, logger="config.cache")
    remote.fail_with = 401
    for _ in range(3):
        assert asyncio.run(http_cache.get(KEY)) is None
    errors = [r for r in caplog.records if r.levelno == logging.ERROR]
    assert len(errors) == 1 and "caller token" in errors[0].getMessage()
    remote.fail_with = None
    asyncio.run(http_cache.get(KEY))
    assert any(r.getMessage() == "remote cache recovered" for r in caplog.records)


def test_clear_is_best_effort(http_cache, remote):
    remote.fail_with = 503
    asyncio.run(http_cache.clear())  # does not raise


# --- help index on the hosted cache ---------------------------------------------


def test_large_help_index_lives_behind_the_api_as_small_pieces(remote, monkeypatch):
    from tools.help_manager import HelpManager

    calls = {"n": 0}
    sections = {f"sub{i}": [{"title": "t" * 300, "help_id": f"p{i}-{j}", "help_tree_id": i * 100 + j}
                            for j in range(20)] for i in range(40)}

    async def fake_build():
        calls["n"] += 1
        return {"tree": {"guide": sections}, "items_index": {}, "index_nodes": {}}

    limit = 16 * 1024  # far below the whole index (~300 KB), above any single piece
    assert len(json.dumps(sections)) > 10 * limit
    monkeypatch.setattr(HelpManager, "_build_help_index", staticmethod(fake_build))
    configure_cache(HttpCache("http://storage", "mcp-caller", max_value_bytes=limit,
                              transport=httpx.MockTransport(remote.handler)))
    try:
        async def scenario():
            await HelpManager(None).list_help_categories()
            for i in (0, 7, 39):
                content = await HelpManager(None).list_help_category_content("guide", [f"sub{i}"])
                assert content.result[0][0]["help_id"] == f"p{i}-0"

        asyncio.run(scenario())
    finally:
        configure_cache(None)
    assert calls["n"] == 1  # every piece fit, so later reads never rebuilt
    assert "global:help:categories" in remote.entries
    assert sum(key.startswith("global:help:section:guide:") for key in remote.entries) == 40
