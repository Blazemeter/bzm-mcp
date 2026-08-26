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


def run_async(coro):
    return asyncio.run(coro)


def make_ctx(token: BzmToken, session_id: str):
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
    from tools.dataframe_manager import _session_locks

    _session_locks.clear()
    yield
    _session_locks.clear()


@pytest.fixture(autouse=True)
def _configure_session_task_storage(session_store):
    """Ensure @run_as_task can persist when manager methods are called in unit tests."""
    from tools.async_task_manager import configure_task_storage

    configure_task_storage(session_store)
    yield session_store


@pytest.fixture
def session_store():
    return InMemorySessionStorageProvider()


@pytest.fixture
def session_scope():
    return SessionScope(user_id="user-1", mcp_session_id="sess-a")
