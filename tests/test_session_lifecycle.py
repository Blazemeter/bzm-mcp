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
"""stdio session lifecycle, storage outages, shared clients and schema guard."""
import asyncio
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from mcp.server.fastmcp import FastMCP

from config.http_clients import SharedAsyncClient, aclose_http_clients
from config.identity import BlazeMeterIdentityVerifier, Identity, InvalidCredentials
from config.ids import SIMPLE_ID_ALPHABET
from config.runtime import build_runtime
from config.session import (
    SESSION_ID_PREFIX,
    HttpSessionProvider,
    InMemorySessionProvider,
    SessionError,
    SessionErrorCode,
    SessionState,
    generate_session_id,
    is_valid_session_id,
)
from config.session_context import bind_session_context, current_identity, current_session
from config.storage import SessionPartitionPayload, SessionScope
from config.token import BzmToken
from tests.conftest import make_ctx
from tools.mcp_entrypoint import _declare_session_id_required
from tools.session_manager import SessionManager

pytestmark = pytest.mark.no_session_context

CREDENTIAL = "Basic alice"


class _Clock:
    def __init__(self):
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += timedelta(seconds=seconds)


def _provider(clock, purged=None, idle=100, grace=10):
    return InMemorySessionProvider(
        idle_timeout_seconds=idle,
        purge_grace_seconds=grace,
        sweep_interval_seconds=1,
        on_purge=(lambda owner, sid: purged.append((owner, sid))) if purged is not None else None,
        clock=clock,
    )


# --- stdio lifecycle -------------------------------------------------------

def test_stdio_keep_alive_postpones_idle_expiry():
    clock = _Clock()
    provider = _provider(clock)

    async def scenario():
        session = await provider.open("alice", CREDENTIAL)
        clock.advance(90)
        await provider.touch(session.session_id, "alice", CREDENTIAL)
        clock.advance(90)  # 180s since open, 90s since the keep-alive
        touched = await provider.touch(session.session_id, "alice", CREDENTIAL)
        assert touched.state is SessionState.ACTIVE

    asyncio.run(scenario())


def test_stdio_idle_session_expires_then_purges_after_the_grace_with_its_partition():
    clock = _Clock()
    purged = []
    provider = _provider(clock, purged)

    async def scenario():
        session = await provider.open("alice", CREDENTIAL)
        clock.advance(100)
        await provider.open("bob", "Basic bob")  # sweep: alice's session expires now
        clock.advance(8)
        with pytest.raises(SessionError) as expired:
            await provider.touch(session.session_id, "alice", CREDENTIAL)
        assert expired.value.code is SessionErrorCode.EXPIRED

        clock.advance(5)  # 13s since expiry, 5s since the first answer: kept
        with pytest.raises(SessionError) as again:
            await provider.touch(session.session_id, "alice", CREDENTIAL)
        assert again.value.code is SessionErrorCode.EXPIRED
        assert purged == []

        clock.advance(6)  # grace counted from the first "expired" answer
        with pytest.raises(SessionError) as gone:
            await provider.touch(session.session_id, "alice", CREDENTIAL)
        assert gone.value.code is SessionErrorCode.INVALID
        assert purged == [("alice", session.session_id)]

    asyncio.run(scenario())


def test_stdio_expired_session_nobody_asked_about_is_purged_by_a_later_sweep():
    clock = _Clock()
    purged = []
    provider = _provider(clock, purged)

    async def scenario():
        stale = await provider.open("alice", CREDENTIAL)
        clock.advance(100)
        await provider.open("bob", "Basic bob")  # sweep: stale expires (never notified)
        clock.advance(10)
        await provider.open("bob", "Basic bob")  # sweep: grace since expiry passed
        assert purged == [("alice", stale.session_id)]

    asyncio.run(scenario())


def test_stdio_runtime_releases_the_partition_of_a_purged_session():
    runtime = build_runtime("stdio", startup_token=BzmToken("k", "s"))
    scope = SessionScope(user_id="alice", mcp_session_id="bzs_" + "a" * 32)

    async def scenario():
        await runtime.storage.put_partition(scope, SessionPartitionPayload(metadata={"x": 1}))
        runtime.sessions._on_purge("alice", scope.mcp_session_id)
        assert await runtime.storage.get_partition(scope) is None

    asyncio.run(scenario())


# --- storage outages are coded, never tracebacks ---------------------------

def _http_provider(handler):
    return HttpSessionProvider(
        "https://storage.internal", "caller", transport=httpx.MockTransport(handler)
    )


def _down(request):
    raise httpx.ConnectError("down")


@pytest.mark.parametrize("handler", [_down, lambda r: httpx.Response(503), lambda r: httpx.Response(200, text="nope")])
def test_http_session_open_and_touch_failures_are_unavailable(handler):
    provider = _http_provider(handler)
    for call in (
        lambda: provider.open("alice", CREDENTIAL),
        lambda: provider.touch("bzs_" + "a" * 32, "alice", CREDENTIAL),
    ):
        with pytest.raises(SessionError) as failed:
            asyncio.run(call())
        assert failed.value.code is SessionErrorCode.UNAVAILABLE


@pytest.mark.parametrize("status,code", [(404, SessionErrorCode.INVALID), (410, SessionErrorCode.EXPIRED)])
def test_http_session_touch_keeps_invalid_and_expired(status, code):
    provider = _http_provider(lambda request: httpx.Response(status))
    with pytest.raises(SessionError) as failed:
        asyncio.run(provider.touch("bzs_" + "a" * 32, "alice", CREDENTIAL))
    assert failed.value.code is code


@pytest.mark.parametrize(
    "status,code",
    [
        (429, SessionErrorCode.UNAVAILABLE),
        (408, SessionErrorCode.UNAVAILABLE),
        (502, SessionErrorCode.UNAVAILABLE),
        (401, SessionErrorCode.SERVICE_ERROR),  # wrong caller token: retrying will not help
        (403, SessionErrorCode.SERVICE_ERROR),
        (422, SessionErrorCode.SERVICE_ERROR),
    ],
)
def test_http_session_errors_separate_transient_from_configuration(status, code):
    provider = _http_provider(lambda request: httpx.Response(status))
    for call in (
        lambda: provider.open("alice", CREDENTIAL),
        lambda: provider.touch("bzs_" + "a" * 32, "alice", CREDENTIAL),
    ):
        with pytest.raises(SessionError) as failed:
            asyncio.run(call())
        assert failed.value.code is code


class _BrokenSessions:
    def __init__(self, error):
        self.error = error

    async def open(self, owner_id, credential):
        raise self.error

    async def touch(self, session_id, owner_id, credential):
        raise self.error


@pytest.mark.parametrize("error", [SessionError(SessionErrorCode.UNAVAILABLE), RuntimeError("boom")])
def test_session_tool_reports_an_outage_as_session_unavailable(error):
    async def scenario():
        with bind_session_context(Identity(user_id="alice"), None, CREDENTIAL):
            return await SessionManager(_BrokenSessions(error)).get()

    result = asyncio.run(scenario())
    assert result.error_code == SessionErrorCode.UNAVAILABLE.value
    assert "Traceback" not in result.error and "boom" not in result.error


# --- identity -------------------------------------------------------------

@pytest.mark.parametrize(
    "body",
    [{"error": {"message": "API key is disabled"}}, {"message": "API key is disabled"}],
)
def test_rejected_credentials_carry_blazemeter_reason(body):
    verifier = BlazeMeterIdentityVerifier(
        transport=httpx.MockTransport(lambda request: httpx.Response(401, json=body))
    )
    with pytest.raises(InvalidCredentials) as failed:
        asyncio.run(verifier.verify(BzmToken("k", "s")))
    assert "API key is disabled" in failed.value.detail


def test_rejected_credentials_without_a_reason_keep_the_generic_detail():
    verifier = BlazeMeterIdentityVerifier(
        transport=httpx.MockTransport(lambda request: httpx.Response(403, text="<html>"))
    )
    with pytest.raises(InvalidCredentials) as failed:
        asyncio.run(verifier.verify(BzmToken("k", "s")))
    assert failed.value.detail == InvalidCredentials.public_detail


def test_identity_uses_its_own_short_timeout():
    verifier = BlazeMeterIdentityVerifier(timeout_seconds=3.0)

    async def scenario():
        return verifier._http.get().timeout

    assert asyncio.run(scenario()).read == 3.0


# --- shared clients -------------------------------------------------------

def test_shared_client_is_reused_closed_on_shutdown_and_rebuilt():
    created = []

    def factory():
        created.append(httpx.AsyncClient())
        return created[-1]

    shared = SharedAsyncClient(factory)
    first = shared.get()
    assert shared.get() is first
    asyncio.run(aclose_http_clients())
    assert first.is_closed
    assert shared.get() is not first  # a closed client is replaced
    assert len(created) == 2


def test_http_session_provider_reuses_one_client_for_open_and_touch():
    clients = []

    def handler(request):
        return httpx.Response(410)

    provider = _http_provider(handler)
    original = provider._http.get

    def tracking_get():
        client = original()
        if not any(client is seen for seen in clients):
            clients.append(client)
        return client

    provider._http.get = tracking_get

    async def scenario():
        for _ in range(3):
            with pytest.raises(SessionError):
                await provider.touch("bzs_" + "a" * 32, "alice", CREDENTIAL)

    asyncio.run(scenario())
    assert len(clients) == 1


# --- schema guard and ids -------------------------------------------------

def test_declaring_session_id_on_a_missing_fastmcp_tool_fails_loudly():
    with pytest.raises(RuntimeError, match="session_id"):
        _declare_session_id_required(FastMCP("t"), "not_registered")


def test_session_ids_use_the_shared_alphabet():
    session_id = generate_session_id()
    assert session_id.startswith(SESSION_ID_PREFIX)
    assert set(session_id[len(SESSION_ID_PREFIX):]) <= set(SIMPLE_ID_ALPHABET)
    assert is_valid_session_id(session_id)
    for ambiguous in "ilou":
        assert not is_valid_session_id(SESSION_ID_PREFIX + ambiguous * 32)


# --- make_ctx bindings do not leak between tests ---------------------------
# (consecutive tests: pytest runs a module in file order)

def test_make_ctx_binds_a_session_without_the_default_context():
    make_ctx(BzmToken("leaky", "s"), "bzs_" + "l" * 32)
    assert current_identity() == Identity(user_id="leaky")


def test_make_ctx_binding_was_undone_after_the_previous_test():
    assert current_identity() is None
    assert current_session() is None
