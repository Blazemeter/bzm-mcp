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
"""api_request / http_request / Log Analyzer reuse one client instead of one per call."""
import asyncio

import httpx
import pytest

from config.token import BzmToken
from tools.utils import common


def _counting(monkeypatch, shared, handler):
    created = []

    def factory():
        created.append(httpx.AsyncClient(
            base_url="https://a.blazemeter.com", transport=httpx.MockTransport(handler)
        ))
        return created[-1]

    monkeypatch.setattr(shared, "_factory", factory)
    shared.discard()
    return created


def test_api_request_reuses_one_client(monkeypatch):
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"result": {"id": 1}})

    created = _counting(monkeypatch, common.bzm_http_client, handler)

    async def calls():
        for _ in range(3):
            result = await common.api_request(BzmToken("k", "s"), "GET", "/user")
            assert result.result == [{"id": 1}]

    asyncio.run(calls())
    assert len(created) == 1
    assert len(seen) == 3
    assert all(r.headers["authorization"].startswith("Basic ") for r in seen)


def test_http_request_reuses_one_client(monkeypatch):
    created = _counting(monkeypatch, common.web_http_client, lambda request: httpx.Response(200, text="ok"))
    monkeypatch.setattr(common, "validate_http_request_endpoint", lambda endpoint: None)

    async def calls():
        for _ in range(2):
            result = await common.http_request("GET", "https://example.com/page")
            assert result.result == "ok"

    asyncio.run(calls())
    assert len(created) == 1


def test_log_analyzer_uses_the_shared_web_client(monkeypatch):
    from tools.execution_manager import ExecutionManager

    urls = []

    def handler(request):
        urls.append(str(request.url))
        return httpx.Response(200, json={"data": {"ok": True}})

    created = _counting(monkeypatch, common.web_http_client, handler)
    manager = ExecutionManager.__new__(ExecutionManager)
    manager.token = BzmToken("k", "s")

    async def calls():
        for _ in range(2):
            result = await manager._request_log_analyzer_api("GET", 42)
            assert result.result == [{"ok": True}]

    asyncio.run(calls())
    assert len(created) == 1
    assert urls == ["https://log-analyzer.blazemeter.com/analyzer/42"] * 2


@pytest.mark.parametrize("shared", [common.bzm_http_client, common.web_http_client])
def test_request_clients_are_closed_on_shutdown(monkeypatch, shared):
    from config.http_clients import aclose_http_clients

    _counting(monkeypatch, shared, lambda request: httpx.Response(200))
    client = shared.get()
    asyncio.run(aclose_http_clients())
    assert client.is_closed


def test_shared_clients_never_keep_cookies_between_callers(monkeypatch):
    cookies_sent = []

    def handler(request):
        cookies_sent.append(request.headers.get("cookie"))
        return httpx.Response(
            200, json={"result": {"id": 1}}, headers={"set-cookie": "bzm_sess=alice-session; Path=/"}
        )

    _counting(monkeypatch, common.bzm_http_client, handler)

    async def calls():
        await common.api_request(BzmToken("alice", "s"), "GET", "/user")
        await common.api_request(BzmToken("bob", "s"), "GET", "/user")

    asyncio.run(calls())
    assert cookies_sent == [None, None]
    assert not common.bzm_http_client.get().cookies


def test_identity_verifier_does_not_carry_cookies_between_users():
    from config.identity import BlazeMeterIdentityVerifier

    cookies_sent = []

    def handler(request):
        cookies_sent.append(request.headers.get("cookie"))
        return httpx.Response(200, json={"result": {"id": 7}}, headers={"set-cookie": "bzm_sess=a; Path=/"})

    verifier = BlazeMeterIdentityVerifier(transport=httpx.MockTransport(handler))

    async def calls():
        await verifier.verify(BzmToken("alice", "s"))
        await verifier.verify(BzmToken("bob", "s"))

    asyncio.run(calls())
    assert cookies_sent == [None, None]


@pytest.mark.parametrize("status", [401, 403])
def test_api_request_rejection_with_html_body_is_invalid_credentials(monkeypatch, status):
    _counting(monkeypatch, common.bzm_http_client, lambda request: httpx.Response(status, text="<html>WAF</html>"))
    result = asyncio.run(common.api_request(BzmToken("k", "s"), "GET", "/user"))
    assert result.error == "Invalid credentials"


def test_log_analyzer_without_token_uses_the_shared_message():
    from config.blazemeter import NO_API_TOKEN_MESSAGE
    from tools.execution_manager import ExecutionManager

    manager = ExecutionManager.__new__(ExecutionManager)
    manager.token = None
    result = asyncio.run(manager._request_log_analyzer_api("GET", 42))
    assert result.error == NO_API_TOKEN_MESSAGE


def test_ticket_client_with_injected_http_builds_no_owned_client():
    from config.tickets import HttpTicketClient

    injected = httpx.AsyncClient()
    client = HttpTicketClient("https://storage.internal", "caller", http=injected)
    assert client._client() is injected
    assert client._owned_http is None
