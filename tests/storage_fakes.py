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
)


class RecordingSessionStorageProvider(InMemorySessionStorageProvider):
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


def http_session_storage_provider(monkeypatch, transport: MergingSessionTransport) -> HttpSessionStorageProvider:
    class _Client(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("config.storage.httpx.AsyncClient", _Client)
    return HttpSessionStorageProvider(base_url="http://storage.test")
