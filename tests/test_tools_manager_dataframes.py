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
from types import SimpleNamespace

import pytest

from config.session_context import SessionContextMissing
from config.storage import DefaultSessionScopeResolver, SessionScope
from config.token import BzmToken
from tests.conftest import make_ctx, run_async, use_session
from tools.dataframe_manager import register_dataframe, resolve_session_scope
from tools.tools_manager import ToolsManager


class TestResolveSessionScope:
    @pytest.mark.no_session_context
    def test_uses_only_the_validated_session_not_token_or_transport(self):
        token = BzmToken("api-key-id", "secret")
        ctx = SimpleNamespace(
            session_id="mcp-abc",
            request_context=SimpleNamespace(
                request=SimpleNamespace(headers={"mcp-session-id": "mcp-abc"})
            ),
        )
        with use_session(user_id="bzm-user-7", session_id="bzs_" + "a" * 32):
            assert resolve_session_scope(ctx, token) == SessionScope("bzm-user-7", "bzs_" + "a" * 32)

    @pytest.mark.no_session_context
    def test_fails_closed_without_a_validated_session(self):
        # No more "anonymous"/"default" shared partition.
        with pytest.raises(SessionContextMissing):
            resolve_session_scope(None, None)


class TestToolsManagerDataframesAgainstStorage:
    def test_list_query_remove_clear(self, in_memory_session_storage):
        token = BzmToken("user-tools", "secret")
        ctx = make_ctx(token, "session-tools")
        manager = ToolsManager(ctx, in_memory_session_storage, DefaultSessionScopeResolver())
        scope = SessionScope("user-tools", "session-tools")

        meta = run_async(
            register_dataframe(
                result=[{"id": 1, "name": "a"}, {"id": 2, "name": "b"}],
                origin_manager="tests",
                origin_action="seed",
                json_size_chars=9001,
                session_storage=in_memory_session_storage,
                scope=scope,
            )
        )

        listed = run_async(manager.dataframes_list())
        assert listed.error is None
        assert listed.total == 1

        queried = run_async(
            manager.dataframes_query(
                sql=(
                    f"SELECT id FROM {meta['table_name']} "
                    f"ORDER BY id LIMIT 100 OFFSET 0"
                )
            )
        )
        assert queried.error is None
        assert queried.total == 2

        removed = run_async(manager.dataframes_remove([meta["dataframe_id"]]))
        assert removed.error is None
        assert run_async(manager.dataframes_list()).total == 0

        run_async(
            register_dataframe(
                result=[{"id": 3}],
                origin_manager="tests",
                origin_action="seed2",
                json_size_chars=9001,
                session_storage=in_memory_session_storage,
                scope=scope,
            )
        )
        cleared = run_async(manager.dataframes_clear())
        assert cleared.result[0]["removed_count"] == 1
        assert run_async(manager.dataframes_list()).total == 0
