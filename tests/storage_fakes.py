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
from __future__ import annotations

import json
from typing import Any, Dict

import httpx

from config.storage import SESSION_PARTITION_PATH_PREFIX


class FakeStorageTransport(httpx.AsyncBaseTransport):
    """In-memory HTTP transport simulating the Storage Service session API."""

    def __init__(self):
        self.partitions: Dict[str, Dict[str, Any]] = {}

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        prefix = f"{SESSION_PARTITION_PATH_PREFIX}/"
        if not path.startswith(prefix):
            return httpx.Response(404, json={"error": "not found"})
        key = path[len(prefix):]
        if request.method == "GET":
            if key not in self.partitions:
                return httpx.Response(404, json={"error": "not found"})
            return httpx.Response(200, json=self.partitions[key])
        if request.method == "PUT":
            self.partitions[key] = json.loads(request.content.decode("utf-8"))
            return httpx.Response(200, json=self.partitions[key])
        if request.method == "DELETE":
            self.partitions.pop(key, None)
            return httpx.Response(204)
        return httpx.Response(405)
