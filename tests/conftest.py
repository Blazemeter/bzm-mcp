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
from types import SimpleNamespace

import pytest

from config.auth import BZM_TOKEN_STATE_ATTR, BZM_USER_CONFIG_STATE_ATTR
from config.storage import InMemorySessionStorageProvider, SessionScope
from config.token import BzmToken


TEST_USER_ID = "user-1"
TEST_SESSION_ID = "bzs_" + "t" * 32


def run_async(coro):
    return asyncio.run(coro)


def make_chat_session(session_id: str = TEST_SESSION_ID, owner_id: str = TEST_USER_ID):
    from datetime import datetime, timezone

    from config.session import ChatSession, SessionState

    now = datetime.now(timezone.utc)
    return ChatSession(
        session_id=session_id,
        owner_id=owner_id,
        state=SessionState.ACTIVE,
        created_at=now,
        last_seen_at=now,
    )


def use_session(user_id: str = TEST_USER_ID, session_id: str = TEST_SESSION_ID):
    """Bind a validated identity + session, as the tool entrypoint does after its checks."""
    from config.identity import Identity
    from config.session_context import bind_session_context

    return bind_session_context(Identity(user_id=user_id), make_chat_session(session_id, user_id))


@pytest.fixture(autouse=True)
def default_session_context(request):
    """
    Most tests exercise managers/tools, not the session gate: run them inside a
    validated session. Tests of the gate itself opt out with
    ``@pytest.mark.no_session_context``.
    """
    if request.node.get_closest_marker("no_session_context"):
        yield None
        return
    with use_session():
        yield SessionScope(user_id=TEST_USER_ID, mcp_session_id=TEST_SESSION_ID)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "no_session_context: run without the default validated session context"
    )


def make_ctx(token: BzmToken, session_id: str, *, bind_session: bool = True):
    """
    Fake FastMCP ctx carrying ``token``.

    The ctx itself no longer decides the partition (only the validated session
    does), so by default this also binds ``token.id`` + ``session_id`` as the
    validated session of the running test, like the tool entrypoint would. The
    autouse ``default_session_context`` fixture restores the previous binding on
    teardown.
    """
    if bind_session and token is not None:
        from config.identity import Identity
        from config.session_context import _current_identity, _current_session

        _current_identity.set(Identity(user_id=token.id))
        _current_session.set(make_chat_session(session_id, token.id))
    request_state = SimpleNamespace(
        **{
            BZM_TOKEN_STATE_ATTR: token,
            BZM_USER_CONFIG_STATE_ATTR: {"token": token},
        }
    )
    request = SimpleNamespace(
        state=request_state,
        headers={"mcp-session-id": session_id},
    )
    return SimpleNamespace(
        session_id=session_id,
        request_context=SimpleNamespace(request=request),
    )


@pytest.fixture(autouse=True)
def reset_dataframe_session_locks():
    from tools import dataframe_manager as dataframe_manager_module

    dataframe_manager_module._session_locks.clear()
    dataframe_manager_module._overflow_lock = None
    yield
    dataframe_manager_module._session_locks.clear()
    dataframe_manager_module._overflow_lock = None


@pytest.fixture(autouse=True)
def _configure_session_task_storage(in_memory_session_storage):
    """Ensure @run_as_task can persist when manager methods are called in unit tests."""
    from tools.async_task_manager import configure_task_storage

    configure_task_storage(in_memory_session_storage)
    yield in_memory_session_storage


@pytest.fixture
def in_memory_session_storage():
    """Stdio-equivalent SessionStoragePort (InMemorySessionStorageProvider)."""
    return InMemorySessionStorageProvider()


@pytest.fixture
def session_scope():
    # Same partition the default validated session context resolves to.
    return SessionScope(user_id=TEST_USER_ID, mcp_session_id=TEST_SESSION_ID)
