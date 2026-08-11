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
from typing import Optional

import httpx
import pytest

import tools.dataframe_manager as dataframe_manager
from config.storage import (
    HTTPStorageClient,
    MemoryStorageProvider,
    SessionPartition,
    StorageNotConfiguredError,
)
from tests.storage_fakes import FakeStorageTransport
from tools.dataframe_manager import (
    clear_dataframes,
    configure_dataframe_storage,
    list_dataframes_metadata,
    query_dataframes,
    register_dataframe,
    remove_dataframe,
)


def _run(coro):
    return asyncio.run(coro)


@pytest.fixture
def memory_store():
    store = MemoryStorageProvider()
    configure_dataframe_storage(store)
    return store


@pytest.fixture
def http_store():
    transport = FakeStorageTransport()
    http = httpx.AsyncClient(transport=transport, base_url="http://storage.test")
    client = HTTPStorageClient(base_url="http://storage.test", http_client=http)
    configure_dataframe_storage(client)
    yield client, http
    _run(http.aclose())


class TestDataframeStorageWiring:
    def test_requires_configure_before_use(self):
        dataframe_manager._storage = None
        with pytest.raises(StorageNotConfiguredError, match="not configured"):
            _run(list_dataframes_metadata(user_id="u", mcp_session_id="s"))


class TestDataframeManagerMemoryStorage:
    def test_register_list_query_remove_clear(self, memory_store):
        meta = _run(
            register_dataframe(
                result=[{"id": 1, "name": "alpha"}, {"id": 2, "name": "beta"}],
                origin_manager="tests",
                origin_action="seed",
                json_size_chars=9001,
                user_id="user-1",
                mcp_session_id="sess-a",
            )
        )
        assert meta["rows"] == 2

        listed = _run(
            list_dataframes_metadata(user_id="user-1", mcp_session_id="sess-a")
        )
        assert len(listed) == 1
        assert listed[0]["dataframe_id"] == meta["dataframe_id"]

        sql = (
            f"SELECT id, name FROM {meta['table_name']} "
            f"ORDER BY id LIMIT 100 OFFSET 0"
        )
        queried = _run(
            query_dataframes(sql, user_id="user-1", mcp_session_id="sess-a")
        )
        assert "error" not in queried
        assert queried["rows"] == 2

        assert _run(
            remove_dataframe(meta["dataframe_id"], user_id="user-1", mcp_session_id="sess-a")
        )
        assert _run(list_dataframes_metadata(user_id="user-1", mcp_session_id="sess-a")) == []

        # Clear on empty session is a no-op.
        assert _run(clear_dataframes(user_id="user-1", mcp_session_id="sess-a")) == 0

    def test_sessions_are_isolated(self, memory_store):
        _run(
            register_dataframe(
                result=[{"id": 1}],
                origin_manager="tests",
                origin_action="a",
                json_size_chars=9001,
                user_id="user-1",
                mcp_session_id="sess-a",
            )
        )
        _run(
            register_dataframe(
                result=[{"id": 2}],
                origin_manager="tests",
                origin_action="b",
                json_size_chars=9001,
                user_id="user-1",
                mcp_session_id="sess-b",
            )
        )
        a = _run(list_dataframes_metadata(user_id="user-1", mcp_session_id="sess-a"))
        b = _run(list_dataframes_metadata(user_id="user-1", mcp_session_id="sess-b"))
        assert len(a) == 1
        assert len(b) == 1
        assert a[0]["dataframe_id"] != b[0]["dataframe_id"]

    def test_two_requests_same_session_share_data(self, memory_store):
        """Simulates two MCP requests with the same Mcp-Session-Id."""
        meta = _run(
            register_dataframe(
                result=[{"n": 1}, {"n": 2}],
                origin_manager="tests",
                origin_action="req1",
                json_size_chars=9001,
                user_id="user-42",
                mcp_session_id="mcp-session-shared",
            )
        )
        # Force a cold hydrate as if a new request handler ran.
        configure_dataframe_storage(memory_store)
        listed = _run(
            list_dataframes_metadata(
                user_id="user-42",
                mcp_session_id="mcp-session-shared",
            )
        )
        assert len(listed) == 1
        assert listed[0]["dataframe_id"] == meta["dataframe_id"]
        assert listed[0]["rows"] == 2


class TestDataframeManagerHttpStorage:
    def test_register_and_query_via_http_storage(self, http_store):
        client, _http = http_store
        meta = _run(
            register_dataframe(
                result=[{"id": 10, "label": "x"}],
                origin_manager="tests",
                origin_action="http",
                json_size_chars=9001,
                user_id="user-9",
                mcp_session_id="sess-http",
            )
        )
        # New manager instance / cold cache using the same HTTP backend.
        configure_dataframe_storage(client)
        listed = _run(
            list_dataframes_metadata(user_id="user-9", mcp_session_id="sess-http")
        )
        assert len(listed) == 1
        sql = (
            f"SELECT id, label FROM {meta['table_name']} "
            f"ORDER BY id LIMIT 10 OFFSET 0"
        )
        queried = _run(
            query_dataframes(sql, user_id="user-9", mcp_session_id="sess-http")
        )
        assert "error" not in queried
        assert queried["rows"] == 1

        partition: Optional[SessionPartition] = _run(client.get("user-9", "sess-http"))
        assert partition is not None
        assert meta["dataframe_id"] in partition.dataframes

    def test_register_preserves_existing_tasks(self, http_store):
        client, _http = http_store
        _run(
            client.put(
                "user-9",
                "sess-tasks",
                SessionPartition(tasks={"t1": {"status": "running"}}),
            )
        )
        meta = _run(
            register_dataframe(
                result=[{"id": 1}],
                origin_manager="tests",
                origin_action="http",
                json_size_chars=9001,
                user_id="user-9",
                mcp_session_id="sess-tasks",
            )
        )
        partition = _run(client.get("user-9", "sess-tasks"))
        assert partition is not None
        assert partition.tasks == {"t1": {"status": "running"}}
        assert meta["dataframe_id"] in partition.dataframes
