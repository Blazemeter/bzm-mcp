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

from config.auth import HttpAuthProvider
from config.blazemeter import TOOLS_PREFIX
from config.runtime import AppRuntime
from config.storage import DefaultSessionScopeResolver, InMemorySessionStorageProvider
from config.tickets import MintedTicket, TicketPort
from config.token import BzmToken
from models.result import BaseResult
from tests.conftest import make_ctx
from tools.test_manager import TestManager, register as register_tests_tool

SHA256 = "a" * 64
CAPABILITY = "capability-secret-token"
BASIC_PREFIX = "Basic "


class FakeTicketClient(TicketPort):
    def __init__(self, public_base_url="http://127.0.0.1:8090"):
        self.public_base_url = public_base_url
        self.credentials = []
        self.mints = []

    async def put_credential(self, user_id, mcp_session_id, api_token):
        self.credentials.append(
            {
                "user_id": user_id,
                "mcp_session_id": mcp_session_id,
                "api_token": api_token,
            }
        )

    async def mint(
        self,
        user_id,
        mcp_session_id,
        test_id,
        filename,
        declared_size,
        encoding,
        sha256,
    ):
        self.mints.append(
            {
                "user_id": user_id,
                "mcp_session_id": mcp_session_id,
                "test_id": test_id,
                "filename": filename,
                "declared_size": declared_size,
                "encoding": encoding,
                "sha256": sha256,
            }
        )
        return MintedTicket(
            id="ticket-1",
            token=CAPABILITY,
            redeem_deadline="2026-09-15T00:00:00Z",
            upload_deadline="2026-09-15T00:05:00Z",
            size_ceiling=104857600,
        )


class FakeMcp:
    def __init__(self):
        self.tools = {}

    def tool(self, name, description):
        def decorator(func):
            self.tools[name] = func
            return func

        return decorator


def _mint_args(**overrides):
    args = {
        "test_id": 42,
        "filename": "Retail-Demo.jmx",
        "declared_size": 128,
        "encoding": "identity",
        "sha256": SHA256,
    }
    args.update(overrides)
    return args


def _http_runtime(tickets):
    return AppRuntime(
        transport="streamable-http",
        auth=HttpAuthProvider(),
        storage=InMemorySessionStorageProvider(),
        file_access=None,
        scope_resolver=DefaultSessionScopeResolver(),
        user_config={},
        tickets=tickets,
    )


def _manager(token, tickets):
    ctx = make_ctx(token, "sess-a")
    return TestManager(
        ctx,
        scope_resolver=DefaultSessionScopeResolver(),
        tickets=tickets,
    )


def _first_payload(result):
    if getattr(result, "structuredContent", None):
        rows = result.structuredContent.get("result") or []
        return rows[0] if rows else None
    rows = getattr(result, "result", None) or []
    return rows[0] if rows else None


def _error_text(result):
    if getattr(result, "error", None):
        return result.error
    payload = _first_payload(result)
    if isinstance(payload, dict):
        return payload.get("error")
    return None


class TestUploadAssetsRemote:
    def test_mints_url_after_authorize_and_credential_put(self, caplog):
        token = BzmToken("key-id", "key-secret")
        tickets = FakeTicketClient()
        manager = _manager(token, tickets)

        async def _fake_read(_test_id):
            return BaseResult(result=[{"id": 42}])

        manager.read = _fake_read  # type: ignore[method-assign]
        with caplog.at_level("DEBUG"):
            result = asyncio.run(manager.upload_assets_remote(_mint_args()))

        payload = _first_payload(result)
        assert result.error is None
        assert payload["method"] == "POST"
        assert payload["url"] == "http://127.0.0.1:8090/services/uploads/ticket-1"
        assert payload["authorization"] == f"Bearer {CAPABILITY}"
        assert payload["headers"]["X-Upload-Filename"] == "Retail-Demo.jmx"
        assert payload["headers"]["X-Content-SHA256"] == SHA256
        assert payload["headers"]["Content-Encoding"] == "identity"
        assert payload["one_file_per_url"] is True
        assert payload["success_status"] == 201
        assert tickets.credentials == [
            {
                "user_id": "key-id",
                "mcp_session_id": "sess-a",
                "api_token": token.as_basic_auth(),
            }
        ]
        assert tickets.mints[0]["test_id"] == 42
        assert tickets.mints[0]["sha256"] == SHA256
        combined = "\n".join(record.getMessage() for record in caplog.records)
        assert CAPABILITY not in combined
        assert token.as_basic_auth() not in combined
        assert BASIC_PREFIX not in combined

    def test_failed_read_does_not_put_or_mint(self):
        token = BzmToken("key-id", "key-secret")
        tickets = FakeTicketClient()
        manager = _manager(token, tickets)

        async def _fail_read(_test_id):
            return BaseResult(error="Test not found")

        manager.read = _fail_read  # type: ignore[method-assign]
        result = asyncio.run(manager.upload_assets_remote(_mint_args()))
        assert _error_text(result) == "Test not found"
        assert tickets.credentials == []
        assert tickets.mints == []

    def test_rejects_bytes_and_paths(self):
        token = BzmToken("key-id", "key-secret")
        tickets = FakeTicketClient()
        manager = _manager(token, tickets)
        result = asyncio.run(
            manager.upload_assets_remote(
                _mint_args(file_paths=["/tmp/demo.jmx"], content="abc", main_script="x.jmx")
            )
        )
        error = _error_text(result)
        assert "does not accept file bytes" in error
        assert "file_paths" in error
        assert "content" in error
        assert "main_script" in error
        assert tickets.credentials == []
        assert tickets.mints == []


class TestUploadAssetsHttpDispatch:
    def test_http_file_paths_only_is_validation_error(self):
        mcp = FakeMcp()
        register_tests_tool(mcp, _http_runtime(FakeTicketClient()))
        tool = mcp.tools[f"{TOOLS_PREFIX}_tests"]
        token = BzmToken("key-id", "key-secret")
        result = asyncio.run(
            tool(
                {
                    "action": "upload_assets",
                    "args": {"test_id": 123, "file_paths": ["/tmp/demo.jmx"]},
                },
                ctx=make_ctx(token, "sess-a"),
            )
        )
        assert result.error is not None
        assert "filename" in result.error
        assert "declared_size" in result.error
        assert "sha256" in result.error

    def test_http_tool_returns_mint_contract(self, monkeypatch):
        tickets = FakeTicketClient()
        mcp = FakeMcp()
        register_tests_tool(mcp, _http_runtime(tickets))
        tool = mcp.tools[f"{TOOLS_PREFIX}_tests"]

        async def _fake_read(self, test_id):
            return BaseResult(result=[{"id": test_id}])

        monkeypatch.setattr(TestManager, "read", _fake_read)
        token = BzmToken("key-id", "key-secret")
        result = asyncio.run(
            tool(
                {"action": "upload_assets", "args": _mint_args()},
                ctx=make_ctx(token, "sess-a"),
            )
        )
        assert result.error is None
        payload = _first_payload(result)
        assert payload["url"] == "http://127.0.0.1:8090/services/uploads/ticket-1"
        assert payload["success_status"] == 201
        assert len(tickets.mints) == 1
        assert len(tickets.credentials) == 1
