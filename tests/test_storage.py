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

from config.file_access import LocalPathFileSource, StorageFileSource
from config.runtime import build_runtime
from config.storage import (
    DefaultSessionScopeResolver,
    HOSTED_FILE_ACCESS_MESSAGE,
    HttpSessionStorageProvider,
    HttpStorageClient,
    InMemorySessionStorageProvider,
    LocalStorageClient,
    StorageNotSupportedError,
    build_storage,
    resolve_storage_backend,
)
from tools.test_manager import TestManager


class TestResolveStorageBackend:
    def test_default_memory(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_STRATEGY", raising=False)
        assert resolve_storage_backend() == "memory"

    def test_env_http(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_STRATEGY", "http")
        assert resolve_storage_backend() == "http"

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="BZM_STORAGE_STRATEGY"):
            resolve_storage_backend("s3")


class TestBuildStorage:
    def test_stdio_memory_uses_local(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_STRATEGY", raising=False)
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        storage = build_storage("stdio")
        assert isinstance(storage, LocalStorageClient)

    def test_streamable_http_uses_http_client(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_STRATEGY", "memory")
        storage = build_storage("streamable-http")
        assert isinstance(storage, HttpStorageClient)

    def test_explicit_http_backend_on_stdio(self):
        storage = build_storage("stdio", backend="http")
        assert isinstance(storage, HttpStorageClient)


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
        client = HttpStorageClient()
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
    def test_http_runtime_gets_http_storage(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_API_BASE_URL", "https://mcp-storage.internal")
        monkeypatch.setattr(HttpSessionStorageProvider, "ensure_available", lambda self: None)
        runtime = build_runtime("streamable-http")
        assert isinstance(runtime.storage, HttpSessionStorageProvider)
        assert isinstance(runtime.file_access, StorageFileSource)

    def test_stdio_runtime_gets_local_storage(self, monkeypatch):
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        runtime = build_runtime("stdio")
        assert isinstance(runtime.storage, InMemorySessionStorageProvider)
        assert isinstance(runtime.file_access, LocalPathFileSource)


class TestUploadAssetsHostedRejection:
    def test_upload_assets_returns_clear_error_on_http_storage(self):
        manager = TestManager(
            ctx=None,
            file_access=StorageFileSource("https://mcp-storage.internal"),
            scope_resolver=DefaultSessionScopeResolver(),
        )

        async def _fake_read(_test_id):
            from models.result import BaseResult
            return BaseResult(result=[{"id": 1}])

        manager.read = _fake_read  # type: ignore[method-assign]
        result = asyncio.run(
            manager.upload_assets(1, ["/tmp/demo.jmx"], main_script=None)
        )
        assert "error" in result
        assert "No valid files found to upload" in result["error"]

    def test_upload_assets_without_file_ports_returns_hosted_message(self):
        manager = TestManager(ctx=None)
        result = asyncio.run(
            manager.upload_assets(1, ["/tmp/demo.jmx"], main_script=None)
        )
        assert result["error"] == HOSTED_FILE_ACCESS_MESSAGE
