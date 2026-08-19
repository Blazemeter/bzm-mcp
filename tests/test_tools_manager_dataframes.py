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

from config.auth import BZM_TOKEN_STATE_ATTR, BZM_USER_CONFIG_STATE_ATTR
from config.storage import InMemorySessionStorageProvider
from config.token import BzmToken
from tools.dataframe_manager import configure_dataframe_storage, register_dataframe
from tools.tools_manager import ToolsManager, resolve_session_partition


def _run(coro):
    return asyncio.run(coro)


def _ctx(token: BzmToken, session_id: str):
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


class TestResolveSessionPartition:
    def test_uses_token_id_and_ctx_session(self):
        token = BzmToken("api-key-id", "secret")
        ctx = SimpleNamespace(session_id="mcp-abc")
        assert resolve_session_partition(token, ctx) == ("api-key-id", "mcp-abc")

    def test_defaults_when_missing(self):
        assert resolve_session_partition(None, None) == ("anonymous", "default")


class TestToolsManagerDataframesAgainstStorage:
    def test_list_query_remove_clear(self):
        store = InMemorySessionStorageProvider()
        configure_dataframe_storage(store)
        token = BzmToken("user-tools", "secret")
        ctx = _ctx(token, "session-tools")
        manager = ToolsManager(ctx)

        meta = _run(
            register_dataframe(
                result=[{"id": 1, "name": "a"}, {"id": 2, "name": "b"}],
                origin_manager="tests",
                origin_action="seed",
                json_size_chars=9001,
                user_id="user-tools",
                mcp_session_id="session-tools",
            )
        )

        listed = _run(manager.dataframes_list())
        assert listed.error is None
        assert listed.total == 1

        queried = _run(
            manager.dataframes_query(
                sql=(
                    f"SELECT id FROM {meta['table_name']} "
                    f"ORDER BY id LIMIT 100 OFFSET 0"
                )
            )
        )
        assert queried.error is None
        assert queried.total == 2

        removed = _run(manager.dataframes_remove([meta["dataframe_id"]]))
        assert removed.error is None
        assert _run(manager.dataframes_list()).total == 0

        _run(
            register_dataframe(
                result=[{"id": 3}],
                origin_manager="tests",
                origin_action="seed2",
                json_size_chars=9001,
                user_id="user-tools",
                mcp_session_id="session-tools",
            )
        )
        cleared = _run(manager.dataframes_clear())
        assert cleared.result[0]["removed_count"] == 1
        assert _run(manager.dataframes_list()).total == 0
