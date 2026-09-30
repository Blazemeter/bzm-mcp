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
import json
from dataclasses import replace
from typing import Optional

import httpx
import pytest

from config.identity import (
    BlazeMeterIdentityVerifier,
    Identity,
    IdentityPort,
    IdentityUnavailable,
    InvalidCredentials,
)
from config.runtime import build_runtime
from config.session import (
    SESSION_TOOL_NAME,
    HttpSessionProvider,
    InMemorySessionProvider,
    SessionError,
    SessionErrorCode,
    SessionState,
    is_valid_session_id,
)
from config.session_context import current_identity, current_session
from config.storage import InMemorySessionStorageProvider, resolve_session_scope
from config.token import BzmToken
from models.result import BaseResult
from tools.dataframe_manager import list_dataframes_metadata, register_dataframe
from tools.mcp_entrypoint import SESSION_HINT, register_managed_tool
from tools.session_manager import register as register_session_tool

pytestmark = pytest.mark.no_session_context

ALICE = BzmToken("alice-key", "alice-secret")
BOB = BzmToken("bob-key", "bob-secret")
FORGED_ALICE = BzmToken("alice-key", "guessed-secret")
ALICE_OTHER_KEY = BzmToken("alice-key-2", "alice-secret-2")


class FakeIdentity(IdentityPort):
    """BlazeMeter stand-in: only the exact id:secret pairs below are valid."""

    USERS = {
        ("alice-key", "alice-secret"): "bzm-alice",
        ("alice-key-2", "alice-secret-2"): "bzm-alice",  # a second key of the same user
        ("bob-key", "bob-secret"): "bzm-bob",
    }

    def __init__(self):
        self.calls = 0
        self.unavailable = False

    async def verify(self, token: Optional[BzmToken]) -> Identity:
        self.calls += 1
        if self.unavailable:
            raise IdentityUnavailable()
        user_id = self.USERS.get((token.id, token.secret)) if token else None
        if user_id is None:
            raise InvalidCredentials("Invalid credentials")
        return Identity(user_id=user_id)


class FakeMcp:
    def __init__(self):
        self.tools = {}
        self.descriptions = {}

    def tool(self, name, description):
        def decorator(func):
            self.tools[name] = func
            self.descriptions[name] = description
            return func
        return decorator


class TokenAuth:
    """Per-call token, like the HTTP Bearer middleware."""

    def __init__(self):
        self.token = None

    def get_token(self, ctx):
        return self.token


@pytest.fixture
def harness():
    auth = TokenAuth()
    identity = FakeIdentity()
    sessions = InMemorySessionProvider()
    storage = InMemorySessionStorageProvider()
    runtime = replace(
        build_runtime("stdio"), auth=auth, identity=identity, sessions=sessions, storage=storage
    )
    mcp = FakeMcp()
    register_session_tool(mcp, runtime)
    seen = []

    async def dispatch(action, args, token, ctx):
        match action:
            case "whoami":
                seen.append((current_identity(), current_session()))
                return BaseResult(result=[{"ok": True}])
            case "store":
                scope = resolve_session_scope(ctx)
                await register_dataframe(
                    result=[{"row": 1}], origin_manager="t", origin_action="store",
                    json_size_chars=10, session_storage=storage, scope=scope,
                )
                return BaseResult(result=[{"stored": True}])
            case "count":
                listed = await list_dataframes_metadata(storage, resolve_session_scope(ctx))
                return BaseResult(result=[{"dataframes": len(listed)}])
            case "batch":
                return await mcp.tools["probe"]({"action": "whoami", "args": args.get("sub_args", {})}, None)
        return BaseResult(error="unknown")

    register_managed_tool(
        mcp, runtime, name="probe", description="Probe tool.", dispatch=dispatch,
        disable_materialization=True,
    )
    register_managed_tool(
        mcp, runtime, name="public_probe", description="Static content.", dispatch=dispatch,
        disable_materialization=True, public=True,
    )

    def call(tool, action, token, **args):
        auth.token = token
        result = asyncio.run(mcp.tools[tool]({"action": action, "args": args}, None))
        return result.structuredContent

    def open_session(token=ALICE):
        return call(SESSION_TOOL_NAME, "get", token)["session_id"]

    return {
        "call": call, "open_session": open_session, "sessions": sessions,
        "identity": identity, "seen": seen, "mcp": mcp,
    }


def test_session_tool_returns_a_new_session_for_the_verified_user(harness):
    body = harness["call"](SESSION_TOOL_NAME, "get", ALICE)
    assert body.get("error") is None
    assert is_valid_session_id(body["session_id"])
    assert body["result"][0]["session_id"] == body["session_id"]
    assert harness["open_session"]() != body["session_id"]


def test_session_tool_rejects_invalid_credentials(harness):
    body = harness["call"](SESSION_TOOL_NAME, "get", FORGED_ALICE)
    assert body["error_code"] == "AUTH_INVALID"
    assert "session_id" not in body


def test_missing_session_id_is_required_and_points_to_the_session_tool(harness):
    body = harness["call"]("probe", "whoami", ALICE)
    assert body["error_code"] == SessionErrorCode.REQUIRED.value
    assert SESSION_TOOL_NAME in body["error"]
    assert harness["seen"] == []


@pytest.mark.parametrize("bad", ["abc", "bzs_short", "BZS_" + "a" * 32, 123])
def test_malformed_session_id_is_invalid(harness, bad):
    body = harness["call"]("probe", "whoami", ALICE, session_id=bad)
    assert body["error_code"] == SessionErrorCode.INVALID.value


def test_unknown_and_foreign_sessions_are_indistinguishable(harness):
    alice_session = harness["open_session"](ALICE)
    foreign = harness["call"]("probe", "whoami", BOB, session_id=alice_session)
    unknown = harness["call"]("probe", "whoami", BOB, session_id="bzs_" + "0" * 32)
    assert foreign["error_code"] == unknown["error_code"] == SessionErrorCode.INVALID.value
    assert foreign["error"] == unknown["error"]
    assert harness["seen"] == []


def test_forged_token_cannot_use_the_owner_session(harness):
    alice_session = harness["open_session"](ALICE)
    body = harness["call"]("probe", "whoami", FORGED_ALICE, session_id=alice_session)
    assert body["error_code"] == "AUTH_INVALID"
    assert harness["seen"] == []


def test_valid_session_binds_context_echoes_session_and_records_keep_alive(harness):
    session_id = harness["open_session"]()
    before = harness["sessions"]._sessions[session_id].last_seen_at
    body = harness["call"]("probe", "whoami", ALICE, session_id=session_id)
    assert body.get("error") is None
    assert body["session_id"] == session_id
    identity, session = harness["seen"][0]
    assert identity.user_id == "bzm-alice"
    assert session.session_id == session_id
    assert harness["sessions"]._sessions[session_id].last_seen_at >= before
    # Nothing leaks out of the call.
    assert current_identity() is None and current_session() is None


def test_session_id_is_accepted_at_top_level_of_arguments(harness):
    session_id = harness["open_session"]()  # leaves ALICE as the current token
    result = asyncio.run(
        harness["mcp"].tools["probe"]({"action": "whoami", "session_id": session_id}, None)
    )
    assert result.structuredContent.get("error") is None
    assert harness["seen"][-1][1].session_id == session_id


def test_expired_session_asks_for_a_new_one(harness):
    session_id = harness["open_session"]()
    sessions = harness["sessions"]._sessions
    sessions[session_id] = replace(sessions[session_id], state=SessionState.EXPIRED)
    body = harness["call"]("probe", "whoami", ALICE, session_id=session_id)
    assert body["error_code"] == SessionErrorCode.EXPIRED.value
    assert SESSION_TOOL_NAME in body["error"]


def test_identity_is_verified_on_every_call_and_outage_fails_closed(harness):
    session_id = harness["open_session"]()
    calls_before = harness["identity"].calls
    harness["call"]("probe", "whoami", ALICE, session_id=session_id)
    assert harness["identity"].calls == calls_before + 1

    harness["identity"].unavailable = True
    body = harness["call"]("probe", "whoami", ALICE, session_id=session_id)
    assert body["error_code"] == "AUTH_UNAVAILABLE"
    assert len(harness["seen"]) == 1


def test_sessions_of_the_same_user_do_not_share_dataframes(harness):
    first = harness["open_session"]()
    second = harness["open_session"]()
    harness["call"]("probe", "store", ALICE, session_id=first)
    assert harness["call"]("probe", "count", ALICE, session_id=first)["result"][0]["dataframes"] == 1
    assert harness["call"]("probe", "count", ALICE, session_id=second)["result"][0]["dataframes"] == 0


def test_nested_calls_inherit_the_session_and_reject_another_one(harness):
    session_id = harness["open_session"]()
    inherited = harness["call"]("probe", "batch", ALICE, session_id=session_id)
    assert inherited.get("error") is None
    assert harness["seen"][-1][1].session_id == session_id

    other = harness["open_session"]()
    body = harness["call"]("probe", "batch", ALICE, session_id=session_id, sub_args={"session_id": other})
    # The probe's batch returns the nested call's result as its own.
    assert body["error_code"] == SessionErrorCode.INVALID.value


def test_descriptions_teach_the_session_requirement(harness):
    descriptions = harness["mcp"].descriptions
    assert SESSION_HINT in descriptions["probe"]
    assert SESSION_HINT not in descriptions[SESSION_TOOL_NAME]
    assert "ONCE" in descriptions[SESSION_TOOL_NAME]


# --- adapters -------------------------------------------------------------------


def test_in_memory_provider_scopes_sessions_to_the_owner():
    async def scenario():
        provider = InMemorySessionProvider()
        session = await provider.open("bzm-alice", "cred-a")
        assert session.state is SessionState.ACTIVE
        touched = await provider.touch(session.session_id, "bzm-alice", "cred-a")
        assert touched.last_seen_at >= session.last_seen_at
        for owner, credential in (("bzm-bob", "cred-a"), ("bzm-alice", "other-cred")):
            with pytest.raises(SessionError) as denied:
                await provider.touch(session.session_id, owner, credential)
            assert denied.value.code is SessionErrorCode.INVALID
        assert "cred-a" not in repr(provider.__dict__)

    asyncio.run(scenario())


def test_http_provider_maps_storage_api_contract():
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        body = json.loads(request.content)
        record = {
            "id": "bzs_" + "b" * 32, "owner_id": body["owner_id"], "state": "ACTIVE",
            "created_at": "2026-09-01T00:00:00+00:00", "last_seen_at": "2026-09-01T00:00:00+00:00",
            "expired_at": None,
        }
        if request.url.path == "/sessions":
            return httpx.Response(201, json=record)
        if "unknown" in body["owner_id"]:
            return httpx.Response(404, json={"detail": "Session not found."})
        if "expired" in body["owner_id"]:
            return httpx.Response(410, json={"detail": "Session expired."})
        return httpx.Response(200, json=record)

    provider = HttpSessionProvider("http://storage", "mcp-caller", transport=httpx.MockTransport(handler))

    async def scenario():
        opened = await provider.open("bzm-alice", "Basic cred")
        assert opened.session_id == "bzs_" + "b" * 32
        assert (await provider.touch(opened.session_id, "bzm-alice", "Basic cred")).owner_id == "bzm-alice"
        for owner, code in (("unknown-user", SessionErrorCode.INVALID), ("expired-user", SessionErrorCode.EXPIRED)):
            with pytest.raises(SessionError) as failed:
                await provider.touch(opened.session_id, owner, "Basic cred")
            assert failed.value.code is code

    asyncio.run(scenario())
    assert all(r.headers["authorization"] == "Bearer mcp-caller" for r in requests)
    assert all(r.headers["x-bzm-credential"] == "Basic cred" for r in requests)
    assert requests[1].url.path == f"/sessions/{'bzs_' + 'b' * 32}/touch"


def test_blazemeter_verifier_maps_user_endpoint(monkeypatch):
    import tools.utils as tools_utils

    responses = {
        "ok": BaseResult(result=[{"id": 12345, "email": "a@b.c"}]),
        "denied": BaseResult(error="Invalid credentials"),
    }

    async def fake_api_request(token, method, endpoint, **kwargs):
        assert (method, endpoint) == ("GET", "/user")
        if token.secret == "boom":
            raise httpx.ConnectError("down")
        return responses[token.secret]

    monkeypatch.setattr(tools_utils, "api_request", fake_api_request)
    verifier = BlazeMeterIdentityVerifier()

    async def scenario():
        assert await verifier.verify(BzmToken("k", "ok")) == Identity(user_id="12345")
        with pytest.raises(InvalidCredentials):
            await verifier.verify(BzmToken("k", "denied"))
        with pytest.raises(InvalidCredentials):
            await verifier.verify(None)
        with pytest.raises(IdentityUnavailable):
            await verifier.verify(BzmToken("k", "boom"))

    asyncio.run(scenario())


def test_session_is_bound_to_the_credential_that_created_it(harness):
    # Same BlazeMeter user, another API key: the session does not follow the key.
    session_id = harness["open_session"](ALICE)
    body = harness["call"]("probe", "whoami", ALICE_OTHER_KEY, session_id=session_id)
    assert body["error_code"] == SessionErrorCode.INVALID.value
    assert harness["seen"] == []


def test_public_tools_work_without_api_key_or_session(harness):
    body = harness["call"]("public_probe", "whoami", None)
    assert body.get("error") is None
    identity, session = harness["seen"][-1]
    assert identity is None and session is None
    assert harness["identity"].calls == 0  # no BlazeMeter round trip needed


def test_public_tools_use_a_valid_session_when_given(harness):
    session_id = harness["open_session"]()
    body = harness["call"]("public_probe", "whoami", ALICE, session_id=session_id)
    assert body.get("error") is None
    assert body["session_id"] == session_id
    assert harness["seen"][-1][1].session_id == session_id


def test_public_tools_never_block_on_a_bad_session_or_token(harness):
    for token, session_id in ((ALICE, "bzs_" + "0" * 32), (FORGED_ALICE, "bzs_" + "0" * 32)):
        body = harness["call"]("public_probe", "whoami", token, session_id=session_id)
        assert body.get("error") is None
        assert any("Running without a session" in w for w in body["warning"])
        assert harness["seen"][-1] == (None, None)


def test_public_tool_descriptions_do_not_demand_a_session(harness):
    descriptions = harness["mcp"].descriptions
    assert SESSION_HINT not in descriptions["public_probe"]
    assert "without an API key" in descriptions["public_probe"]


def test_ticket_client_accepts_the_generic_storage_caller_token(monkeypatch):
    from config.tickets import build_ticket_client

    monkeypatch.delenv("BZM_MCP_TICKET_STORAGE_CALLER_TOKEN", raising=False)
    monkeypatch.setenv("BZM_MCP_STORAGE_CALLER_TOKEN", "storage-token")
    monkeypatch.setenv("BZM_MCP_UPLOAD_PUBLIC_BASE_URL", "https://mcp.example")
    client = build_ticket_client("streamable-http", "http://storage")
    assert client._headers()["Authorization"] == "Bearer storage-token"


def test_storage_clients_send_the_session_credential_of_the_call():
    from config.identity import Identity
    from config.session_context import bind_session_context
    from config.storage import HttpSessionStorageProvider
    from config.tickets import HttpTicketClient
    from tests.conftest import make_chat_session

    partitions = HttpSessionStorageProvider("http://storage", caller_token="mcp-caller")
    tickets = HttpTicketClient(
        base_url="http://storage", caller_token="mcp-caller", public_base_url="https://mcp.example",
    )
    assert "X-Bzm-Credential" not in partitions._request_headers()
    with bind_session_context(Identity("bzm-alice"), make_chat_session(), "Basic cred"):
        assert partitions._request_headers()["X-Bzm-Credential"] == "Basic cred"
        assert tickets._headers()["X-Bzm-Credential"] == "Basic cred"


def test_real_skills_tool_works_without_api_key_or_session():
    from dataclasses import replace as dc_replace

    from tools.skills_manager import register as register_skills

    runtime = dc_replace(build_runtime("stdio"), auth=TokenAuth(), identity=FakeIdentity())
    mcp = FakeMcp()
    mcp.resource = lambda pattern: (lambda func: func)
    register_skills(mcp, runtime)
    result = asyncio.run(mcp.tools["blazemeter_skills"]({"action": "list_skills", "args": {}}, None))
    body = result.structuredContent
    assert body.get("error") is None
    assert body.get("error_code") is None
    assert body["result"]


# --- published input schema -----------------------------------------------------


def _published_schemas():
    from mcp.server.fastmcp import FastMCP

    from server import register_tools

    mcp = FastMCP("schema-check")
    register_tools(mcp, build_runtime("stdio"))
    return mcp, {tool.name: tool.inputSchema for tool in asyncio.run(mcp.list_tools())}


def test_session_id_is_a_required_parameter_in_the_published_schema():
    _, schemas = _published_schemas()
    for name, schema in schemas.items():
        if name in {SESSION_TOOL_NAME, "blazemeter_help", "blazemeter_skills"}:
            continue
        assert "session_id" in schema.get("required", []), name
        prop = schema["properties"]["session_id"]
        assert prop["type"] == "string"
        assert SESSION_TOOL_NAME in prop["description"]


def test_public_tools_declare_session_id_as_optional_and_the_session_tool_does_not_have_it():
    _, schemas = _published_schemas()
    for name in ("blazemeter_help", "blazemeter_skills"):
        assert "session_id" in schemas[name]["properties"]
        assert "session_id" not in schemas[name].get("required", [])
    assert "session_id" not in schemas[SESSION_TOOL_NAME]["properties"]


def test_missing_session_id_reaches_the_gate_instead_of_a_bare_validation_error():
    mcp, _ = _published_schemas()
    arg_model = mcp._tool_manager.get_tool("blazemeter_tests").fn_metadata.arg_model
    # FastMCP validates with this model: it must accept the call so the gate answers SESSION_REQUIRED.
    arg_model.model_validate({"arguments": {"action": "read", "args": {"test_id": 1}}})


def test_declared_session_id_parameter_is_used_and_wins_over_a_nested_one(harness):
    session_id = harness["open_session"]()  # leaves ALICE as the current token
    other = harness["open_session"]()
    probe = harness["mcp"].tools["probe"]
    result = asyncio.run(
        probe({"action": "whoami", "args": {"session_id": other}}, None, session_id=session_id)
    )
    assert result.structuredContent.get("error") is None
    assert harness["seen"][-1][1].session_id == session_id
