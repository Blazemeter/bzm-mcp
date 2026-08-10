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

import asyncio
import copy
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Protocol, runtime_checkable
from urllib.parse import quote

import httpx

from config.path_mapper import PathMapperFactory, PathMappingStrategy

StorageBackend = Literal["memory", "http"]

HOSTED_FILE_ACCESS_MESSAGE = (
    "Local file lookup and upload are not supported on the hosted MCP server. "
    "Use a local stdio/Docker MCP installation for upload_assets, or wait for "
    "Phase 2 remote Storage."
)

DEFAULT_STORAGE_SERVICE_URL_ENV = "BZM_STORAGE_SERVICE_URL"


class StorageNotSupportedError(NotImplementedError):
    """Raised when a storage backend cannot fulfill a file operation."""


@dataclass
class SessionPartition:
    """
    Session document stored under ``{user_id}/{mcp_session_id}``.

    Schema placeholders match the external Storage Service contract so MCP
    workers and the storage API stay aligned.
    """

    metadata: Dict[str, Any] = field(default_factory=dict)
    dataframes: Dict[str, Any] = field(default_factory=dict)
    tasks: Dict[str, Any] = field(default_factory=dict)
    uploaded_files: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": copy.deepcopy(self.metadata),
            "dataframes": copy.deepcopy(self.dataframes),
            "tasks": copy.deepcopy(self.tasks),
            "uploaded_files": copy.deepcopy(self.uploaded_files),
        }

    @classmethod
    def from_dict(cls, payload: Optional[Dict[str, Any]]) -> "SessionPartition":
        data = payload or {}
        return cls(
            metadata=dict(data.get("metadata") or {}),
            dataframes=dict(data.get("dataframes") or {}),
            tasks=dict(data.get("tasks") or {}),
            uploaded_files=dict(data.get("uploaded_files") or {}),
        )


@runtime_checkable
class StoragePort(Protocol):
    """
    Contract for session-partitioned state and file access used by MCP tools.

    Session methods are keyed by ``{user_id}/{mcp_session_id}`` so hosted
    workers can share dataframes/tasks across HTTP requests and instances.

    File methods support ``upload_assets`` on stdio; hosted backends fail closed.
    """

    async def get(self, user_id: str, mcp_session_id: str) -> Optional[SessionPartition]:
        ...

    async def put(
            self,
            user_id: str,
            mcp_session_id: str,
            partition: SessionPartition,
    ) -> None:
        ...

    async def delete(self, user_id: str, mcp_session_id: str) -> None:
        ...

    def map_paths(self, file_paths: List[str]) -> List[str]:
        ...

    def exists(self, path: str) -> bool:
        ...

    def is_file(self, path: str) -> bool:
        ...

    def read_bytes(self, path: str) -> bytes:
        ...

    def basename(self, path: str) -> str:
        ...


class LocalStorageClient:
    """
    Process-local file access helper used by ``MemoryStorageProvider``.

    Kept as a named type so existing upload/security tests can target file I/O
    without depending on session-partition behaviour.
    """

    def __init__(self, path_mapper: Optional[PathMappingStrategy] = None):
        self._path_mapper = path_mapper or PathMapperFactory.create_strategy()

    def map_paths(self, file_paths: List[str]) -> List[str]:
        return self._path_mapper.map_paths(file_paths)

    def exists(self, path: str) -> bool:
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def read_bytes(self, path: str) -> bytes:
        with open(path, "rb") as handle:
            return handle.read()

    def basename(self, path: str) -> str:
        return Path(path).name


class MemoryStorageProvider:
    """
    Stdio / single-process session store (in-memory partitions) + local files.

    Replaces the process-global ``_dataframes`` dict as the backing store while
    preserving local disk access for ``upload_assets``.
    """

    def __init__(
            self,
            path_mapper: Optional[PathMappingStrategy] = None,
            files: Optional[LocalStorageClient] = None,
    ):
        self._files = files or LocalStorageClient(path_mapper=path_mapper)
        self._partitions: Dict[tuple[str, str], SessionPartition] = {}
        self._lock = asyncio.Lock()

    @staticmethod
    def _key(user_id: str, mcp_session_id: str) -> tuple[str, str]:
        return (str(user_id), str(mcp_session_id))

    async def get(self, user_id: str, mcp_session_id: str) -> Optional[SessionPartition]:
        async with self._lock:
            partition = self._partitions.get(self._key(user_id, mcp_session_id))
            if partition is None:
                return None
            return SessionPartition.from_dict(partition.to_dict())

    async def put(
            self,
            user_id: str,
            mcp_session_id: str,
            partition: SessionPartition,
    ) -> None:
        async with self._lock:
            self._partitions[self._key(user_id, mcp_session_id)] = SessionPartition.from_dict(
                partition.to_dict()
            )

    async def delete(self, user_id: str, mcp_session_id: str) -> None:
        async with self._lock:
            self._partitions.pop(self._key(user_id, mcp_session_id), None)

    def map_paths(self, file_paths: List[str]) -> List[str]:
        return self._files.map_paths(file_paths)

    def exists(self, path: str) -> bool:
        return self._files.exists(path)

    def is_file(self, path: str) -> bool:
        return self._files.is_file(path)

    def read_bytes(self, path: str) -> bytes:
        return self._files.read_bytes(path)

    def basename(self, path: str) -> str:
        return self._files.basename(path)


class HTTPStorageClient:
    """
    Hosted Storage Service client: session get/put/delete over HTTP.

    File lookup/upload paths remain fail-closed until remote ``uploaded_files``
    support lands. Base URL: ``BZM_STORAGE_SERVICE_URL``.
    """

    def __init__(
            self,
            base_url: Optional[str] = None,
            http_client: Optional[httpx.AsyncClient] = None,
            timeout: Optional[httpx.Timeout] = None,
    ):
        env_url = os.getenv(DEFAULT_STORAGE_SERVICE_URL_ENV, "")
        self._base_url = (base_url if base_url is not None else env_url).rstrip("/")
        self._http_client = http_client
        self._owns_client = http_client is None
        self._timeout = timeout or httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=5.0)
        self._client_lock = asyncio.Lock()

    def _require_base_url(self) -> str:
        if not self._base_url:
            raise ValueError(
                f"{DEFAULT_STORAGE_SERVICE_URL_ENV} is required for HTTP storage "
                "(session get/put/delete)."
            )
        return self._base_url

    def _partition_path(self, user_id: str, mcp_session_id: str) -> str:
        user = quote(str(user_id), safe="")
        session = quote(str(mcp_session_id), safe="")
        return f"/v1/sessions/{user}/{session}"

    async def _client(self) -> httpx.AsyncClient:
        if self._http_client is not None:
            return self._http_client
        async with self._client_lock:
            if self._http_client is None:
                self._http_client = httpx.AsyncClient(
                    base_url=self._require_base_url(),
                    timeout=self._timeout,
                )
            return self._http_client

    async def get(self, user_id: str, mcp_session_id: str) -> Optional[SessionPartition]:
        self._require_base_url()
        client = await self._client()
        response = await client.get(self._partition_path(user_id, mcp_session_id))
        if response.status_code == 404:
            return None
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Storage Service get returned a non-object JSON payload")
        return SessionPartition.from_dict(payload)

    async def put(
            self,
            user_id: str,
            mcp_session_id: str,
            partition: SessionPartition,
    ) -> None:
        self._require_base_url()
        client = await self._client()
        response = await client.put(
            self._partition_path(user_id, mcp_session_id),
            json=partition.to_dict(),
        )
        response.raise_for_status()

    async def delete(self, user_id: str, mcp_session_id: str) -> None:
        self._require_base_url()
        client = await self._client()
        response = await client.delete(self._partition_path(user_id, mcp_session_id))
        if response.status_code == 404:
            return
        response.raise_for_status()

    def map_paths(self, file_paths: List[str]) -> List[str]:
        raise StorageNotSupportedError(HOSTED_FILE_ACCESS_MESSAGE)

    def exists(self, path: str) -> bool:
        raise StorageNotSupportedError(HOSTED_FILE_ACCESS_MESSAGE)

    def is_file(self, path: str) -> bool:
        raise StorageNotSupportedError(HOSTED_FILE_ACCESS_MESSAGE)

    def read_bytes(self, path: str) -> bytes:
        raise StorageNotSupportedError(HOSTED_FILE_ACCESS_MESSAGE)

    def basename(self, path: str) -> str:
        raise StorageNotSupportedError(HOSTED_FILE_ACCESS_MESSAGE)


# Backward-compatible alias used by older tests / docs.
HttpStorageClient = HTTPStorageClient


def resolve_storage_backend(raw: Optional[str] = None) -> StorageBackend:
    """Resolve BZM_STORAGE_BACKEND (default: memory)."""
    candidate = (raw if raw is not None else os.getenv("BZM_STORAGE_BACKEND", "memory")).strip().lower()
    if not candidate:
        return "memory"
    if candidate not in ("memory", "http"):
        raise ValueError(
            f"Invalid BZM_STORAGE_BACKEND '{candidate}'. Valid values: memory, http."
        )
    return candidate  # type: ignore[return-value]


def build_storage(
        transport: Literal["stdio", "streamable-http"],
        backend: Optional[str] = None,
) -> StoragePort:
    """
    Select storage for the process.

    - stdio + memory → ``MemoryStorageProvider`` (in-memory sessions + local files)
    - streamable-http or backend=http → ``HTTPStorageClient`` (remote sessions;
      local file paths rejected)
    """
    resolved = resolve_storage_backend(backend)
    if transport == "streamable-http" or resolved == "http":
        return HTTPStorageClient()
    return MemoryStorageProvider()
