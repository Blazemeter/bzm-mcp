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

from config.storage import MemoryStorageProvider
from config.token import BzmToken
from models.result import BaseResult
from tools.dataframe_manager import (
    configure_dataframe_storage,
    finalize_tool_result,
    list_dataframes_metadata,
    materialize_large_result_if_needed,
    register_dataframe,
)
from tools.tools_manager import ToolsManager


def _run(coro):
    return asyncio.run(coro)


class TestConcurrentSessionIsolation:
    def test_concurrent_registers_do_not_cross_write(self):
        store = MemoryStorageProvider()
        configure_dataframe_storage(store)

        async def _register(user_id: str, session_id: str, value: int):
            return await register_dataframe(
                result=[{"v": value}],
                origin_manager="tests",
                origin_action="seed",
                json_size_chars=9001,
                user_id=user_id,
                mcp_session_id=session_id,
            )

        async def _exercise():
            await asyncio.gather(
                _register("u1", "s1", 1),
                _register("u1", "s2", 2),
                _register("u2", "s1", 3),
                _register("u1", "s1", 11),
            )
            listed = await asyncio.gather(
                list_dataframes_metadata(user_id="u1", mcp_session_id="s1"),
                list_dataframes_metadata(user_id="u1", mcp_session_id="s2"),
                list_dataframes_metadata(user_id="u2", mcp_session_id="s1"),
            )
            return listed

        s1, s2, s3 = _run(_exercise())
        assert len(s1) == 2
        assert len(s2) == 1
        assert len(s3) == 1
        assert {row["rows"] for row in s1} == {1}
        assert s2[0]["origin_action"] == "seed"
        values = []
        for partition in (s1, s2, s3):
            assert all(item["origin_manager"] == "tests" for item in partition)


class TestMaterializeWiring:
    def test_finalize_materializes_large_auto_result(self):
        store = MemoryStorageProvider()
        configure_dataframe_storage(store)
        token = BzmToken("user-mat", "secret")
        ctx = SimpleNamespace(session_id="sess-mat")
        payload = [{"id": i, "name": f"row-{i}", "note": "x" * 40} for i in range(300)]
        base = BaseResult(result=payload)

        finalized = _run(
            finalize_tool_result(
                base,
                action="list",
                args={},
                origin_manager="blazemeter_tests",
                token=token,
                ctx=ctx,
            )
        )
        assert finalized.error is None
        assert finalized.result[0]["stored_as_dataframe"] is True
        listed = _run(
            list_dataframes_metadata(user_id="user-mat", mcp_session_id="sess-mat")
        )
        assert len(listed) == 1

    def test_force_dataframe_even_when_small(self):
        configure_dataframe_storage(MemoryStorageProvider())
        token = BzmToken("user-force", "secret")
        ctx = SimpleNamespace(session_id="sess-force")
        base = BaseResult(result=[{"id": 1}])
        finalized = _run(
            materialize_large_result_if_needed(
                base,
                origin_manager="tests",
                origin_action="list",
                force=True,
                user_id="user-force",
                mcp_session_id="sess-force",
            )
        )
        assert finalized.result[0]["stored_as_dataframe"] is True

    def test_excluded_action_skips_auto_materialize(self):
        configure_dataframe_storage(MemoryStorageProvider())
        token = BzmToken("user-ex", "secret")
        ctx = SimpleNamespace(session_id="sess-ex")
        payload = [{"id": i, "note": "x" * 40} for i in range(300)]
        finalized = _run(
            finalize_tool_result(
                BaseResult(result=payload),
                action="dataframes_list",
                args={},
                origin_manager="blazemeter_tools",
                token=token,
                ctx=ctx,
                excluded_actions={"dataframes_list"},
            )
        )
        assert len(finalized.result) == 300


class TestDataframesQueryResultFormatStore:
    def test_result_format_dataframe_registers_new_dataframe(self):
        configure_dataframe_storage(MemoryStorageProvider())
        token = BzmToken("user-q", "secret")
        ctx = SimpleNamespace(session_id="sess-q")
        manager = ToolsManager(token, ctx)

        meta = _run(
            register_dataframe(
                result=[{"id": 1, "name": "a"}, {"id": 2, "name": "b"}],
                origin_manager="tests",
                origin_action="seed",
                json_size_chars=9001,
                user_id="user-q",
                mcp_session_id="sess-q",
            )
        )
        queried = _run(
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
        listed = _run(
            list_dataframes_metadata(user_id="user-q", mcp_session_id="sess-q")
        )
        assert len(listed) == 2
