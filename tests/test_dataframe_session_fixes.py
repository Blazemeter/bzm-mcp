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
from unittest.mock import MagicMock

from config.runtime import AppRuntime
from config.storage import DefaultSessionScopeResolver, SessionScope
from config.token import BzmToken
from models.result import BaseResult
from tests.conftest import make_ctx, run_async
from tools.dataframe_manager import (
    MISSING_STORAGE_ERROR,
    finalize_tool_result,
    list_dataframes_metadata,
    materialize_large_result_if_needed,
    register_dataframe,
)
from tools.runtime_tools import run_tool_with_runtime
from tools.tools_manager import ToolsManager


class TestConcurrentSessionIsolation:
    def test_concurrent_registers_do_not_cross_write(self, session_store):
        async def _register(user_id: str, session_id: str, value: int):
            return await register_dataframe(
                result=[{"v": value}],
                origin_manager="tests",
                origin_action="seed",
                json_size_chars=9001,
                storage=session_store,
                scope=SessionScope(user_id, session_id),
            )

        async def _exercise():
            await asyncio.gather(
                _register("u1", "s1", 1),
                _register("u1", "s2", 2),
                _register("u2", "s1", 3),
                _register("u1", "s1", 11),
            )
            listed = await asyncio.gather(
                list_dataframes_metadata(session_store, SessionScope("u1", "s1")),
                list_dataframes_metadata(session_store, SessionScope("u1", "s2")),
                list_dataframes_metadata(session_store, SessionScope("u2", "s1")),
            )
            return listed

        s1, s2, s3 = run_async(_exercise())
        assert len(s1) == 2
        assert len(s2) == 1
        assert len(s3) == 1
        assert {row["rows"] for row in s1} == {1}
        assert s2[0]["origin_action"] == "seed"
        for partition in (s1, s2, s3):
            assert all(item["origin_manager"] == "tests" for item in partition)


class TestMaterializeWiring:
    def test_finalize_materializes_large_auto_result(self, session_store):
        token = BzmToken("user-mat", "secret")
        ctx = make_ctx(token, "sess-mat")
        payload = [{"id": i, "name": f"row-{i}", "note": "x" * 40} for i in range(300)]
        base = BaseResult(result=payload)

        finalized = run_async(
            finalize_tool_result(
                base,
                action="list",
                args={},
                origin_manager="blazemeter_tests",
                storage=session_store,
                scope_resolver=DefaultSessionScopeResolver(),
                token=token,
                ctx=ctx,
            )
        )
        assert finalized.error is None
        assert finalized.result[0]["stored_as_dataframe"] is True
        listed = run_async(
            list_dataframes_metadata(session_store, SessionScope("user-mat", "sess-mat"))
        )
        assert len(listed) == 1

    def test_force_dataframe_even_when_small(self, session_store):
        base = BaseResult(result=[{"id": 1}])
        finalized = run_async(
            materialize_large_result_if_needed(
                base,
                origin_manager="tests",
                origin_action="list",
                storage=session_store,
                scope=SessionScope("user-force", "sess-force"),
                force=True,
            )
        )
        assert finalized.result[0]["stored_as_dataframe"] is True

    def test_finalize_without_storage_fails_closed(self):
        payload = [{"id": i, "note": "x" * 40} for i in range(300)]
        finalized = run_async(
            finalize_tool_result(
                BaseResult(result=payload),
                action="list",
                args={},
                origin_manager="blazemeter_tests",
            )
        )
        assert finalized.error == MISSING_STORAGE_ERROR

    def test_excluded_action_skips_without_storage(self):
        payload = [{"id": i, "note": "x" * 40} for i in range(300)]
        finalized = run_async(
            finalize_tool_result(
                BaseResult(result=payload),
                action="dataframes_list",
                args={},
                origin_manager="blazemeter_tools",
                excluded_actions={"dataframes_list"},
            )
        )
        assert len(finalized.result) == 300

    def test_excluded_action_skips_auto_materialize(self, session_store):
        token = BzmToken("user-ex", "secret")
        ctx = make_ctx(token, "sess-ex")
        payload = [{"id": i, "note": "x" * 40} for i in range(300)]
        finalized = run_async(
            finalize_tool_result(
                BaseResult(result=payload),
                action="dataframes_list",
                args={},
                origin_manager="blazemeter_tools",
                storage=session_store,
                token=token,
                ctx=ctx,
                excluded_actions={"dataframes_list"},
            )
        )
        assert len(finalized.result) == 300


class TestRunToolWithRuntime:
    def test_materializes_large_result_via_runtime_storage(self, session_store):
        token = BzmToken("user-rt", "secret")
        ctx = make_ctx(token, "sess-rt")
        runtime = AppRuntime(
            transport="stdio",
            auth=MagicMock(get_token=MagicMock(return_value=token)),
            storage=session_store,
            file_access=MagicMock(),
            scope_resolver=DefaultSessionScopeResolver(),
            user_config={},
        )
        payload = [{"id": i, "name": f"row-{i}", "note": "x" * 40} for i in range(300)]

        async def _dispatch():
            return BaseResult(result=payload)

        finalized = run_async(
            run_tool_with_runtime(
                runtime, "blazemeter_tests", "list", ctx, _dispatch,
            )
        )
        assert finalized.error is None
        assert finalized.result[0]["stored_as_dataframe"] is True
        listed = run_async(
            list_dataframes_metadata(session_store, SessionScope("user-rt", "sess-rt"))
        )
        assert len(listed) == 1


class TestDataframesQueryResultFormatStore:
    def test_result_format_dataframe_registers_new_dataframe(self, session_store):
        token = BzmToken("user-q", "secret")
        ctx = make_ctx(token, "sess-q")
        manager = ToolsManager(ctx, session_store, DefaultSessionScopeResolver())
        scope = SessionScope("user-q", "sess-q")

        meta = run_async(
            register_dataframe(
                result=[{"id": 1, "name": "a"}, {"id": 2, "name": "b"}],
                origin_manager="tests",
                origin_action="seed",
                json_size_chars=9001,
                storage=session_store,
                scope=scope,
            )
        )
        queried = run_async(
            manager.dataframes_query(
                sql=(
                    f"SELECT id, name FROM {meta['table_name']} "
                    f"ORDER BY id LIMIT 100 OFFSET 0"
                ),
                result_format="dataframe",
            )
        )
        assert queried.error is None
        assert queried.result[0]["stored_as_dataframe"] is True
        listed = run_async(list_dataframes_metadata(session_store, scope))
        assert len(listed) == 2
