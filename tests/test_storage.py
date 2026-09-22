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

from config.file_access import HOSTED_FILE_ACCESS_MESSAGE, LocalPathFileSource
from config.runtime import build_runtime
from config.storage import (
    HttpSessionStorageProvider,
    InMemorySessionStorageProvider,
)
from tools.test_manager import TestManager


class TestRuntimeStorageWiring:
    def test_http_runtime_gets_session_storage_and_tickets(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_API_BASE_URL", "https://mcp-storage.internal")
        monkeypatch.setenv("BZM_MCP_TICKET_STORAGE_CALLER_TOKEN", "caller-secret")
        monkeypatch.setenv("BZM_MCP_UPLOAD_PUBLIC_BASE_URL", "http://127.0.0.1:8090")
        monkeypatch.setattr(HttpSessionStorageProvider, "ensure_available", lambda self: None)
        runtime = build_runtime("streamable-http")
        assert isinstance(runtime.storage, HttpSessionStorageProvider)
        assert runtime.file_access is None
        assert runtime.tickets is not None

    def test_stdio_runtime_gets_local_storage(self, monkeypatch):
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        runtime = build_runtime("stdio")
        assert isinstance(runtime.storage, InMemorySessionStorageProvider)
        assert isinstance(runtime.file_access, LocalPathFileSource)
        assert runtime.tickets is None


class TestUploadAssetsHostedRejection:
    def test_local_upload_assets_without_file_ports_returns_hosted_message(self):
        manager = TestManager(ctx=None)
        result = asyncio.run(
            manager.upload_assets(1, ["/tmp/demo.jmx"], main_script=None)
        )
        if hasattr(result, "error"):
            inner = result.result[0] if result.result else {}
            error_text = result.error or (inner.get("error") if isinstance(inner, dict) else None)
        else:
            error_text = result.get("error") if isinstance(result, dict) else None
        assert error_text == HOSTED_FILE_ACCESS_MESSAGE
