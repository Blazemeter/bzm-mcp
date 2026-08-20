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
import json

import httpx

from config.storage import (
    HttpSessionStorageProvider,
    InMemorySessionStorageProvider,
    SessionPartitionPayload,
    SessionScope,
    SessionStoragePort,
)
from tests.conftest import run_async
from tools import dataframe_manager as dataframe_manager_module
from tools.dataframe_manager import (
    clear_dataframes,
    list_dataframes_metadata,
    query_dataframes,
    register_dataframe,
    remove_dataframes,
    remove_dataframe,
)


def _seed(storage, scope, rows, action="seed"):
    return run_async(
        register_dataframe(
            result=rows,
            origin_manager="tests",
            origin_action=action,
            json_size_chars=9001,
            storage=storage,
            scope=scope,
        )
    )


class RecordingSessionStorage(InMemorySessionStorageProvider):
    def __init__(self) -> None:
        super().__init__()
        self.put_payloads: list[SessionPartitionPayload] = []

    async def put_partition(self, scope: SessionScope, payload: SessionPartitionPayload) -> None:
        self.put_payloads.append(payload)
        await super().put_partition(scope, payload)


class MergingSessionTransport(httpx.AsyncBaseTransport):
    """Simulates Storage API merge-on-PUT for /session-partitions/{user}/{session}."""

    def __init__(self) -> None:
        self.partitions: dict[str, dict] = {}

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        prefix = "/session-partitions/"
        if not path.startswith(prefix):
            return httpx.Response(404, json={"error": "not found"})
        key = path[len(prefix):]
        if request.method == "GET":
            if key not in self.partitions:
                return httpx.Response(404, json={"error": "not found"})
            return httpx.Response(200, json=self.partitions[key])
        if request.method == "PUT":
            incoming = json.loads(request.content.decode("utf-8"))
            existing = dict(self.partitions.get(key) or {})
            for section in ("metadata", "dataframes", "tasks", "uploaded_files"):
                if section in incoming:
                    existing[section] = incoming[section]
            user_id, _, session_id = key.partition("/")
            existing["user_id"] = user_id
            existing["mcp_session_id"] = session_id
            self.partitions[key] = existing
            return httpx.Response(200, json=existing)
        if request.method == "DELETE":
            deleted = key in self.partitions
            self.partitions.pop(key, None)
            return httpx.Response(200, json={"deleted": deleted})
        return httpx.Response(405)


def _http_storage(monkeypatch, transport: MergingSessionTransport) -> HttpSessionStorageProvider:
    class _Client(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("config.storage.httpx.AsyncClient", _Client)
    return HttpSessionStorageProvider(base_url="http://storage.test")


class TestDataframeManagerMemoryStorage:
    def test_register_list_query_remove_clear(self, session_store, session_scope):
        meta = _seed(
            session_store,
            session_scope,
            [{"id": 1, "name": "alpha"}, {"id": 2, "name": "beta"}],
        )
        assert meta["rows"] == 2

        listed = run_async(list_dataframes_metadata(session_store, session_scope))
        assert len(listed) == 1
        assert listed[0]["dataframe_id"] == meta["dataframe_id"]

        sql = (
            f"SELECT id, name FROM {meta['table_name']} "
            f"ORDER BY id LIMIT 100 OFFSET 0"
        )
        queried = run_async(query_dataframes(sql, session_store, session_scope))
        assert "error" not in queried
        assert queried["rows"] == 2

        assert run_async(remove_dataframe(meta["dataframe_id"], session_store, session_scope))
        assert run_async(list_dataframes_metadata(session_store, session_scope)) == []
        assert run_async(clear_dataframes(session_store, session_scope)) == 0

    def test_sessions_are_isolated(self, session_store):
        scope_a = SessionScope("user-1", "sess-a")
        scope_b = SessionScope("user-1", "sess-b")
        _seed(session_store, scope_a, [{"id": 1}], action="a")
        _seed(session_store, scope_b, [{"id": 2}], action="b")
        a = run_async(list_dataframes_metadata(session_store, scope_a))
        b = run_async(list_dataframes_metadata(session_store, scope_b))
        assert len(a) == 1
        assert len(b) == 1
        assert a[0]["dataframe_id"] != b[0]["dataframe_id"]

    def test_second_call_sees_storage_without_cache_reset(self, session_store):
        scope = SessionScope("user-42", "mcp-session-shared")
        meta = _seed(
            session_store,
            scope,
            [{"n": 1}, {"n": 2}],
            action="req1",
        )
        listed = run_async(list_dataframes_metadata(session_store, scope))
        assert len(listed) == 1
        assert listed[0]["dataframe_id"] == meta["dataframe_id"]
        assert listed[0]["rows"] == 2

    def test_external_put_is_visible_on_next_read(self, monkeypatch):
        transport = MergingSessionTransport()
        client_a = _http_storage(monkeypatch, transport)
        client_b = HttpSessionStorageProvider(base_url="http://storage.test")
        scope = SessionScope("user-1", "sess-a")
        first = _seed(client_a, scope, [{"id": 1}])
        injected = _seed(client_b, scope, [{"id": 99}], action="external")
        listed_again = run_async(list_dataframes_metadata(client_a, scope))
        ids = {row["dataframe_id"] for row in listed_again}
        assert first["dataframe_id"] in ids
        assert injected["dataframe_id"] in ids


class TestDataframeManagerSessionPort:
    def test_register_writes_through_put_partition(self):
        store = RecordingSessionStorage()
        scope = SessionScope("user-9", "sess-http")
        meta = _seed(store, scope, [{"id": 10, "label": "x"}], action="http")
        assert store.put_payloads
        assert meta["dataframe_id"] in store.put_payloads[-1].dataframes

        listed = run_async(list_dataframes_metadata(store, scope))
        assert len(listed) == 1
        sql = (
            f"SELECT id, label FROM {meta['table_name']} "
            f"ORDER BY id LIMIT 10 OFFSET 0"
        )
        queried = run_async(query_dataframes(sql, store, scope))
        assert "error" not in queried
        assert queried["rows"] == 1

        partition = run_async(store.get_partition(scope))
        assert partition is not None
        assert meta["dataframe_id"] in partition.dataframes

    def test_register_preserves_existing_tasks(self, session_store):
        scope = SessionScope("user-9", "sess-tasks")
        run_async(
            session_store.put_partition(
                scope,
                SessionPartitionPayload(tasks={"t1": {"status": "running"}}),
            )
        )
        meta = _seed(session_store, scope, [{"id": 1}], action="http")
        partition = run_async(session_store.get_partition(scope))
        assert partition is not None
        assert partition.tasks == {"t1": {"status": "running"}}
        assert meta["dataframe_id"] in partition.dataframes

    def test_remove_batch_persists_once(self):
        store = RecordingSessionStorage()
        scope = SessionScope("user-9", "sess-batch")
        a = _seed(store, scope, [{"id": 1}], action="a")
        b = _seed(store, scope, [{"id": 2}], action="b")
        puts_before = len(store.put_payloads)
        outcome = run_async(
            remove_dataframes(
                [a["dataframe_id"], b["dataframe_id"]],
                store,
                scope,
            )
        )
        assert outcome["removed"] == [a["dataframe_id"], b["dataframe_id"]]
        assert len(store.put_payloads) == puts_before + 1


class InterveningGetStorage(InMemorySessionStorageProvider):
    """Injects extra dataframes on a chosen GET to simulate another worker."""

    def __init__(self, extra_dataframes: dict) -> None:
        super().__init__()
        self.get_count = 0
        self.inject_on_get: int | None = None
        self.extra_dataframes = extra_dataframes

    async def get_partition(self, scope: SessionScope):
        self.get_count += 1
        if self.get_count == self.inject_on_get:
            existing = await super().get_partition(scope)
            dataframes = dict(existing.dataframes) if existing else {}
            dataframes.update(self.extra_dataframes)
            await super().put_partition(
                scope, SessionPartitionPayload(dataframes=dataframes)
            )
        return await super().get_partition(scope)


class TestDataframeMapMerge:
    def test_persist_keeps_keys_added_since_hydrate(self, session_scope):
        side = InMemorySessionStorageProvider()
        extra_meta = _seed(side, session_scope, [{"id": 99}], action="external")
        extra_partition = run_async(side.get_partition(session_scope))
        extra_dataframes = {
            extra_meta["dataframe_id"]: extra_partition.dataframes[extra_meta["dataframe_id"]]
        }
        store = InterveningGetStorage(extra_dataframes)
        first = _seed(store, session_scope, [{"id": 1}])
        store.get_count = 0
        store.inject_on_get = 2
        second = _seed(store, session_scope, [{"id": 2}], action="local")
        listed = run_async(list_dataframes_metadata(store, session_scope))
        ids = {row["dataframe_id"] for row in listed}
        assert first["dataframe_id"] in ids
        assert second["dataframe_id"] in ids
        assert extra_meta["dataframe_id"] in ids


class TestHttpSessionStorageProviderDataframes:
    def test_http_client_roundtrip_and_task_merge(self, monkeypatch):
        transport = MergingSessionTransport()
        client = _http_storage(monkeypatch, transport)
        scope = SessionScope("user-9", "sess-http")

        run_async(
            client.put_partition(
                scope,
                SessionPartitionPayload(tasks={"t1": {"status": "running"}}),
            )
        )
        meta = _seed(client, scope, [{"id": 10, "label": "x"}], action="http")
        listed = run_async(list_dataframes_metadata(client, scope))
        assert len(listed) == 1
        sql = (
            f"SELECT id, label FROM {meta['table_name']} "
            f"ORDER BY id LIMIT 10 OFFSET 0"
        )
        queried = run_async(query_dataframes(sql, client, scope))
        assert "error" not in queried
        partition = run_async(client.get_partition(scope))
        assert partition is not None
        assert partition.tasks == {"t1": {"status": "running"}}
        assert meta["dataframe_id"] in partition.dataframes
        assert isinstance(client, SessionStoragePort)


class TestSqlReadOnlyGate:
    def test_requires_select_order_limit_offset(self, session_store, session_scope):
        missing_clauses = run_async(
            query_dataframes("SELECT * FROM df_x", session_store, session_scope)
        )
        assert "error" in missing_clauses
        assert "ORDER BY" in missing_clauses["error"]

        delete_stmt = run_async(
            query_dataframes("DELETE FROM df_x", session_store, session_scope)
        )
        assert "error" in delete_stmt
        assert "read-only" in delete_stmt["error"].lower()

        meta = _seed(session_store, session_scope, [{"id": 1, "name": "a"}])
        valid = run_async(
            query_dataframes(
                f"SELECT * FROM {meta['table_name']} ORDER BY id LIMIT 10 OFFSET 0",
                session_store,
                session_scope,
            )
        )
        assert "error" not in valid
        assert valid["rows"] == 1


class TestSessionLockBound:
    def test_unlocked_locks_are_evicted(self, session_store, monkeypatch):
        monkeypatch.setattr(dataframe_manager_module, "_MAX_SESSION_LOCKS", 4)

        async def _exercise():
            for index in range(10):
                await list_dataframes_metadata(
                    session_store, SessionScope("user-1", f"sess-{index}")
                )
            return len(dataframe_manager_module._session_locks)

        assert run_async(_exercise()) <= 4
