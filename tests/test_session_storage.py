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
from typing import Any, Dict, Optional

import httpx
import pytest

from config.runtime import build_runtime
from config.storage import (
    HOSTED_FILE_ACCESS_MESSAGE,
    HTTPStorageClient,
    MemoryStorageProvider,
    SessionPartition,
    StorageNotSupportedError,
    build_storage,
)


class TestSessionPartition:
    def test_roundtrip_dict(self):
        partition = SessionPartition(
            metadata={"version": 1},
            dataframes={"abc": {"dataframe_id": "abc", "data": [{"x": 1}]}},
            tasks={"t1": {"status": "queued"}},
            uploaded_files={},
        )
        restored = SessionPartition.from_dict(partition.to_dict())
        assert restored.metadata == {"version": 1}
        assert restored.dataframes["abc"]["dataframe_id"] == "abc"
        assert restored.tasks["t1"]["status"] == "queued"
        assert restored.uploaded_files == {}

    def test_from_dict_defaults_missing_sections(self):
        restored = SessionPartition.from_dict({})
        assert restored.metadata == {}
        assert restored.dataframes == {}
        assert restored.tasks == {}
        assert restored.uploaded_files == {}


class TestMemoryStorageProvider:
    def test_get_missing_returns_none(self):
        store = MemoryStorageProvider()
        assert asyncio.run(store.get("user-a", "session-1")) is None

    def test_put_get_delete_roundtrip(self):
        store = MemoryStorageProvider()
        partition = SessionPartition(
            dataframes={"df1": {"dataframe_id": "df1", "data": [{"n": 1}]}},
        )
        asyncio.run(store.put("user-a", "session-1", partition))

        loaded = asyncio.run(store.get("user-a", "session-1"))
        assert loaded is not None
        assert loaded.dataframes["df1"]["dataframe_id"] == "df1"

        # Partitions are isolated by user_id and mcp_session_id.
        assert asyncio.run(store.get("user-a", "session-2")) is None
        assert asyncio.run(store.get("user-b", "session-1")) is None

        asyncio.run(store.delete("user-a", "session-1"))
        assert asyncio.run(store.get("user-a", "session-1")) is None

    def test_put_replaces_entire_partition(self):
        store = MemoryStorageProvider()
        asyncio.run(
            store.put(
                "u",
                "s",
                SessionPartition(dataframes={"a": {"dataframe_id": "a"}}, tasks={"t": {}}),
            )
        )
        asyncio.run(
            store.put(
                "u",
                "s",
                SessionPartition(dataframes={"b": {"dataframe_id": "b"}}),
            )
        )
        loaded = asyncio.run(store.get("u", "s"))
        assert loaded is not None
        assert list(loaded.dataframes.keys()) == ["b"]
        assert loaded.tasks == {}

    def test_file_access_still_works(self, tmp_path, monkeypatch):
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        path = tmp_path / "asset.jmx"
        path.write_bytes(b"<jmx/>")
        store = MemoryStorageProvider()
        assert store.map_paths([str(path)]) == [str(path)]
        assert store.exists(str(path))
        assert store.is_file(str(path))
        assert store.read_bytes(str(path)) == b"<jmx/>"
        assert store.basename(str(path)) == "asset.jmx"


class _FakeTransport(httpx.AsyncBaseTransport):
    """In-memory HTTP transport simulating the Storage Service API."""

    def __init__(self):
        self.partitions: Dict[str, Dict[str, Any]] = {}

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        prefix = "/v1/sessions/"
        if not path.startswith(prefix):
            return httpx.Response(404, json={"error": "not found"})
        key = path[len(prefix) :]
        if request.method == "GET":
            if key not in self.partitions:
                return httpx.Response(404, json={"error": "not found"})
            return httpx.Response(200, json=self.partitions[key])
        if request.method == "PUT":
            import json

            self.partitions[key] = json.loads(request.content.decode("utf-8"))
            return httpx.Response(200, json=self.partitions[key])
        if request.method == "DELETE":
            self.partitions.pop(key, None)
            return httpx.Response(204)
        return httpx.Response(405)


class TestHTTPStorageClient:
    def test_file_methods_still_fail_closed(self):
        client = HTTPStorageClient(base_url="http://storage.test")
        with pytest.raises(StorageNotSupportedError, match="hosted MCP"):
            client.map_paths(["/tmp/a.jmx"])
        with pytest.raises(StorageNotSupportedError):
            client.read_bytes("/tmp/a.jmx")
        assert HOSTED_FILE_ACCESS_MESSAGE

    def test_get_put_delete_via_http(self):
        transport = _FakeTransport()
        http = httpx.AsyncClient(
            transport=transport,
            base_url="http://storage.test",
        )
        client = HTTPStorageClient(base_url="http://storage.test", http_client=http)

        async def _run():
            assert await client.get("user-1", "sess-a") is None
            partition = SessionPartition(
                metadata={"source": "test"},
                dataframes={"df1": {"dataframe_id": "df1", "data": [{"v": 9}]}},
            )
            await client.put("user-1", "sess-a", partition)
            loaded = await client.get("user-1", "sess-a")
            assert loaded is not None
            assert loaded.metadata["source"] == "test"
            assert loaded.dataframes["df1"]["data"][0]["v"] == 9
            # Same Mcp-Session-Id key space is shared across gets.
            again = await client.get("user-1", "sess-a")
            assert again is not None
            assert again.dataframes == loaded.dataframes
            await client.delete("user-1", "sess-a")
            assert await client.get("user-1", "sess-a") is None
            await http.aclose()

        asyncio.run(_run())

    def test_requires_base_url(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_SERVICE_URL", raising=False)
        client = HTTPStorageClient(base_url="")
        with pytest.raises(ValueError, match="BZM_STORAGE_SERVICE_URL"):
            asyncio.run(client.get("u", "s"))


class TestBuildStorageSessionBackends:
    def test_stdio_uses_memory_storage_provider(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_BACKEND", raising=False)
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        storage = build_storage("stdio")
        assert isinstance(storage, MemoryStorageProvider)

    def test_streamable_http_uses_http_storage_client(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_BACKEND", "memory")
        monkeypatch.setenv("BZM_STORAGE_SERVICE_URL", "http://storage.test")
        storage = build_storage("streamable-http")
        assert isinstance(storage, HTTPStorageClient)

    def test_runtime_wires_session_storage(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_BACKEND", raising=False)
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        stdio = build_runtime("stdio")
        assert isinstance(stdio.storage, MemoryStorageProvider)
        http = build_runtime("streamable-http")
        assert isinstance(http.storage, HTTPStorageClient)


class TestSharedSessionVisibility:
    """Integration-style: two logical requests with same session share data."""

    def test_memory_two_requests_same_session_see_shared_data(self):
        store = MemoryStorageProvider()

        async def request_one():
            await store.put(
                "user-42",
                "mcp-session-xyz",
                SessionPartition(dataframes={"shared": {"dataframe_id": "shared", "rows": 2}}),
            )

        async def request_two() -> Optional[SessionPartition]:
            return await store.get("user-42", "mcp-session-xyz")

        asyncio.run(request_one())
        loaded = asyncio.run(request_two())
        assert loaded is not None
        assert "shared" in loaded.dataframes

    def test_http_two_requests_same_session_see_shared_data(self):
        transport = _FakeTransport()
        http = httpx.AsyncClient(transport=transport, base_url="http://storage.test")
        client = HTTPStorageClient(base_url="http://storage.test", http_client=http)

        async def _run():
            await client.put(
                "user-42",
                "mcp-session-xyz",
                SessionPartition(dataframes={"shared": {"dataframe_id": "shared", "rows": 2}}),
            )
            # Simulate a second MCP request on another worker using the same client/API.
            other = HTTPStorageClient(base_url="http://storage.test", http_client=http)
            loaded = await other.get("user-42", "mcp-session-xyz")
            assert loaded is not None
            assert loaded.dataframes["shared"]["rows"] == 2
            await http.aclose()

        asyncio.run(_run())
