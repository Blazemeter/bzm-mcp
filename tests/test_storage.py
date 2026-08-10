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

from config.runtime import build_runtime
from config.storage import (
    HOSTED_FILE_ACCESS_MESSAGE,
    HTTPStorageClient,
    HttpStorageClient,
    LocalStorageClient,
    MemoryStorageProvider,
    StorageNotSupportedError,
    build_storage,
    resolve_storage_backend,
)
from tools.test_manager import TestManager


class TestResolveStorageBackend:
    def test_default_memory(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_BACKEND", raising=False)
        assert resolve_storage_backend() == "memory"

    def test_env_http(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_BACKEND", "http")
        assert resolve_storage_backend() == "http"

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="BZM_STORAGE_BACKEND"):
            resolve_storage_backend("s3")


class TestBuildStorage:
    def test_stdio_memory_uses_memory_provider(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_BACKEND", raising=False)
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        storage = build_storage("stdio")
        assert isinstance(storage, MemoryStorageProvider)

    def test_streamable_http_uses_http_client(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_BACKEND", "memory")
        storage = build_storage("streamable-http")
        assert isinstance(storage, HTTPStorageClient)
        assert isinstance(storage, HttpStorageClient)

    def test_explicit_http_backend_on_stdio(self):
        storage = build_storage("stdio", backend="http")
        assert isinstance(storage, HTTPStorageClient)


class TestLocalStorageClient:
    def test_read_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        path = tmp_path / "asset.jmx"
        path.write_bytes(b"<jmx/>")
        client = LocalStorageClient()
        mapped = client.map_paths([str(path)])
        assert mapped == [str(path)]
        assert client.exists(str(path))
        assert client.is_file(str(path))
        assert client.read_bytes(str(path)) == b"<jmx/>"
        assert client.basename(str(path)) == "asset.jmx"


class TestHttpStorageClient:
    def test_all_file_methods_raise(self):
        client = HTTPStorageClient(base_url="http://storage.test")
        with pytest.raises(StorageNotSupportedError, match="hosted MCP") as exc_info:
            client.map_paths(["/tmp/a.jmx"])
        assert HOSTED_FILE_ACCESS_MESSAGE in str(exc_info.value)
        with pytest.raises(StorageNotSupportedError):
            client.exists("/tmp/a.jmx")
        with pytest.raises(StorageNotSupportedError):
            client.is_file("/tmp/a.jmx")
        with pytest.raises(StorageNotSupportedError):
            client.read_bytes("/tmp/a.jmx")
        with pytest.raises(StorageNotSupportedError):
            client.basename("/tmp/a.jmx")


class TestRuntimeStorageWiring:
    def test_http_runtime_gets_http_storage(self):
        runtime = build_runtime("streamable-http")
        assert isinstance(runtime.storage, HTTPStorageClient)

    def test_stdio_runtime_gets_memory_storage(self, monkeypatch):
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        monkeypatch.delenv("BZM_STORAGE_BACKEND", raising=False)
        runtime = build_runtime("stdio")
        assert isinstance(runtime.storage, MemoryStorageProvider)


class TestUploadAssetsHostedRejection:
    def test_upload_assets_returns_clear_error_on_http_storage(self):
        manager = TestManager(token=None, ctx=None, storage=HTTPStorageClient(base_url="http://x"))

        async def _fake_read(_test_id):
            from models.result import BaseResult
            return BaseResult(result=[{"id": 1}])

        manager.read = _fake_read  # type: ignore[method-assign]
        result = asyncio.run(
            manager.upload_assets(1, ["/tmp/demo.jmx"], main_script=None)
        )
        assert "error" in result
        assert "not supported on the hosted MCP" in result["error"]
