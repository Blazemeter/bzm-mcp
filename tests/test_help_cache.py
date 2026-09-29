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

from config.cache import InMemoryTTLCache, configure_cache
from models.result import HttpBaseResult
from tools import help_manager as help_manager_module
from tools.help_manager import HelpManager

TWELVE_HOURS = 12 * 60 * 60


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def _fake_index():
    return {
        "tree": {"guide": {"self": [{"title": "Intro", "help_id": "intro", "help_tree_id": 1}]}},
        "items_index": {"guide:self:intro": 1},
        "index_nodes": {1: {"category": "guide", "subcategory": "self", "help_id": "intro", "sub_nodes": []}},
    }


def test_help_ttl_is_twelve_hours():
    assert HelpManager.HELP_CACHE_TTL_SECONDS == TWELVE_HOURS


def test_help_index_is_global_and_refreshed_after_twelve_hours(monkeypatch):
    clock = FakeClock()
    configure_cache(InMemoryTTLCache(sweep_interval_seconds=0, clock=clock))
    calls = {"count": 0}

    async def fake_build():
        calls["count"] += 1
        return _fake_index()

    monkeypatch.setattr(HelpManager, "_build_help_index", staticmethod(fake_build))

    async def scenario():
        await asyncio.gather(*(HelpManager.get_help_index() for _ in range(3)))
        assert calls["count"] == 1
        clock.now += TWELVE_HOURS - 1
        await HelpManager.get_help_index()
        assert calls["count"] == 1
        clock.now += 2
        await HelpManager.get_help_index()
        assert calls["count"] == 2

    asyncio.run(scenario())


def test_help_page_is_cached_and_marked_as_cached(monkeypatch):
    calls = {"count": 0}

    async def fake_http_request(method, endpoint, result_formatter=None, result_formatter_params=None, **kwargs):
        calls["count"] += 1
        return HttpBaseResult(result={"help_content": "Intro page"})

    monkeypatch.setattr(help_manager_module, "http_request", fake_http_request)

    async def scenario():
        first = await HelpManager.get_help_object("guide", "self", "intro")
        second = await HelpManager.get_help_object("guide", "self", "intro")
        assert first["help_cached"] is False
        assert second["help_cached"] is True
        assert second["help_result"] == {"help_content": "Intro page"}
        assert second["help_id"] == "intro"
        assert calls["count"] == 1

    asyncio.run(scenario())


def test_help_page_errors_are_not_cached(monkeypatch):
    calls = {"count": 0}

    async def fake_http_request(method, endpoint, result_formatter=None, result_formatter_params=None, **kwargs):
        calls["count"] += 1
        return HttpBaseResult(error="Invalid credentials")

    monkeypatch.setattr(help_manager_module, "http_request", fake_http_request)

    async def scenario():
        first = await HelpManager.get_help_object("guide", "self", "missing")
        second = await HelpManager.get_help_object("guide", "self", "missing")
        assert "Error:Invalid credentials" in first["help_result"]
        assert second["help_cached"] is False
        assert calls["count"] == 2

    asyncio.run(scenario())


def test_section_pages_expand_sub_nodes_from_the_cached_index(monkeypatch):
    async def fake_build():
        index = _fake_index()
        index["index_nodes"][1]["sub_nodes"] = [2]
        index["index_nodes"][2] = {"category": "guide", "subcategory": "self", "help_id": "child", "sub_nodes": []}
        return index

    async def fake_http_request(method, endpoint, result_formatter=None, result_formatter_params=None, **kwargs):
        return HttpBaseResult(result={"help_content": "Overview. In this section:"})

    monkeypatch.setattr(HelpManager, "_build_help_index", staticmethod(fake_build))
    monkeypatch.setattr(help_manager_module, "http_request", fake_http_request)

    help_object = asyncio.run(HelpManager.get_help_object("guide", "self", "intro"))
    assert help_object["sub_nodes"] == [
        {"category": "guide", "subcategory": "self", "help_id": "child", "sub_nodes": []}
    ]


def test_help_index_is_shared_read_only_and_listings_return_copies(monkeypatch):
    async def fake_build():
        return _fake_index()

    monkeypatch.setattr(HelpManager, "_build_help_index", staticmethod(fake_build))

    async def scenario():
        first = await HelpManager.get_help_index()
        second = await HelpManager.get_help_index()
        assert first is second  # no deep copy of the whole index per call

        listing = await HelpManager(None).list_help_category_content("guide", ["self"])
        listing.result[0][0]["title"] = "mutated by caller"
        assert (await HelpManager.get_help_index())["tree"]["guide"]["self"][0]["title"] == "Intro"

    asyncio.run(scenario())
