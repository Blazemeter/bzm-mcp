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

import httpx
import pytest

from config.tickets import (
    DEFAULT_UPLOAD_PUBLIC_BASE_URL,
    HttpTicketClient,
    TicketClientError,
    build_ticket_client,
)


class _FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


class _FakeAsyncClient:
    def __init__(self, response):
        self.response = response
        self.calls = []

    async def request(self, method, url, headers=None, json=None):
        self.calls.append(
            {"method": method, "url": url, "headers": headers, "json": json}
        )
        return self.response

    async def aclose(self):
        return None


def test_build_ticket_client_none_on_stdio():
    assert build_ticket_client("stdio") is None


def test_build_ticket_client_requires_storage_url(monkeypatch):
    monkeypatch.delenv("BZM_STORAGE_API_BASE_URL", raising=False)
    with pytest.raises(ValueError, match="BZM_STORAGE_API_BASE_URL"):
        build_ticket_client("streamable-http")


def test_build_ticket_client_requires_caller_token(monkeypatch):
    monkeypatch.setenv("BZM_STORAGE_API_BASE_URL", "https://storage.internal")
    monkeypatch.delenv("BZM_MCP_TICKET_STORAGE_CALLER_TOKEN", raising=False)
    with pytest.raises(ValueError, match="BZM_MCP_TICKET_STORAGE_CALLER_TOKEN"):
        build_ticket_client("streamable-http")


def test_build_ticket_client_requires_public_base_url(monkeypatch):
    monkeypatch.setenv("BZM_STORAGE_API_BASE_URL", "https://storage.internal")
    monkeypatch.setenv("BZM_MCP_TICKET_STORAGE_CALLER_TOKEN", "caller-secret")
    monkeypatch.delenv("BZM_MCP_UPLOAD_PUBLIC_BASE_URL", raising=False)
    with pytest.raises(ValueError, match="BZM_MCP_UPLOAD_PUBLIC_BASE_URL"):
        build_ticket_client("streamable-http")


def test_build_ticket_client_http_success(monkeypatch):
    monkeypatch.setenv("BZM_STORAGE_API_BASE_URL", "https://storage.internal")
    monkeypatch.setenv("BZM_MCP_TICKET_STORAGE_CALLER_TOKEN", "caller-secret")
    monkeypatch.setenv("BZM_MCP_UPLOAD_PUBLIC_BASE_URL", DEFAULT_UPLOAD_PUBLIC_BASE_URL)
    client = build_ticket_client("streamable-http")
    assert isinstance(client, HttpTicketClient)
    assert client.public_base_url == DEFAULT_UPLOAD_PUBLIC_BASE_URL
    assert client.public_upload_url("abc") == (
        f"{DEFAULT_UPLOAD_PUBLIC_BASE_URL}/services/uploads/abc"
    )


def test_mint_maps_success_and_does_not_log_secret(caplog, monkeypatch):
    response = _FakeResponse(
        201,
        {
            "id": "ticket-9",
            "token": "capability-must-not-log",
            "redeem_deadline": "2026-09-15T00:00:00Z",
            "upload_deadline": "2026-09-15T00:05:00Z",
            "size_ceiling": 10,
        },
    )
    http = _FakeAsyncClient(response)
    client = HttpTicketClient(
        "https://storage.internal",
        caller_token="caller-secret",
        http=http,
    )
    with caplog.at_level("DEBUG"):
        minted = asyncio.run(
            client.mint(
                "user-1",
                "sess-a",
                7,
                "Retail-Demo.jmx",
                12,
                "identity",
                "a" * 64,
            )
        )
    assert minted.id == "ticket-9"
    assert minted.token == "capability-must-not-log"
    assert http.calls[0]["headers"]["Authorization"] == "Bearer caller-secret"
    combined = "\n".join(record.getMessage() for record in caplog.records)
    assert "capability-must-not-log" not in combined
    assert "caller-secret" not in combined


def test_put_credential_maps_422():
    http = _FakeAsyncClient(_FakeResponse(422))
    client = HttpTicketClient("https://storage.internal", "caller", http=http)
    with pytest.raises(TicketClientError, match="rejected"):
        asyncio.run(client.put_credential("u", "s", "Basic abc"))


def test_mint_maps_429():
    http = _FakeAsyncClient(_FakeResponse(429))
    client = HttpTicketClient("https://storage.internal", "caller", http=http)
    with pytest.raises(TicketClientError, match="quota"):
        asyncio.run(
            client.mint("u", "s", 1, "a.jmx", 1, "identity", "a" * 64)
        )


def test_mint_maps_401():
    http = _FakeAsyncClient(_FakeResponse(401))
    client = HttpTicketClient("https://storage.internal", "caller", http=http)
    with pytest.raises(TicketClientError, match="caller identity"):
        asyncio.run(
            client.mint("u", "s", 1, "a.jmx", 1, "identity", "a" * 64)
        )


def test_mint_maps_malformed_json():
    http = _FakeAsyncClient(_FakeResponse(201, {"id": "only-id"}))
    client = HttpTicketClient("https://storage.internal", "caller", http=http)
    with pytest.raises(TicketClientError, match="invalid response"):
        asyncio.run(
            client.mint("u", "s", 1, "a.jmx", 1, "identity", "a" * 64)
        )


def test_request_maps_network_error():
    class _BrokenClient:
        async def request(self, *args, **kwargs):
            raise httpx.ConnectError("boom")

        async def aclose(self):
            return None

    client = HttpTicketClient(
        "https://storage.internal", "caller", http=_BrokenClient()
    )
    with pytest.raises(TicketClientError, match="unreachable"):
        asyncio.run(client.put_credential("u", "s", "Basic abc"))


def test_owned_client_is_reused(monkeypatch):
    created = []

    class _TrackingClient(_FakeAsyncClient):
        def __init__(self, response):
            super().__init__(response)
            created.append(self)

    monkeypatch.setattr(
        "config.tickets.httpx.AsyncClient",
        lambda timeout: _TrackingClient(_FakeResponse(204)),
    )
    client = HttpTicketClient("https://storage.internal", "caller")
    asyncio.run(client.put_credential("u", "s", "Basic abc"))
    asyncio.run(client.put_credential("u", "s", "Basic abc"))
    assert len(created) == 1
