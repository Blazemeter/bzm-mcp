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

from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, List, Literal, Optional, Protocol, runtime_checkable
from urllib.parse import quote

import httpx
from mcp.server.fastmcp import Context

from config.path_mapper import PathMapperFactory, PathMappingStrategy
from config.token import BzmToken

StorageBackend = Literal["memory", "http"]

HOSTED_FILE_ACCESS_MESSAGE = (
    "Local file lookup and upload are not supported on the hosted MCP server. "
    "Use a local stdio/Docker MCP installation for upload_assets, or wait for "
    "Phase 2 remote Storage."
)


class StorageNotSupportedError(NotImplementedError):
    """Raised when a storage backend cannot fulfill a file operation."""


@runtime_checkable
class FileStoragePort(Protocol):
    """
    Contract for resolving and reading files used by MCP tools (e.g. upload_assets).

    MVP backends:
    - memory/local: process-local disk via path mapping (stdio / local Docker)
    - http: fail-closed stub for hosted streamable-http (no local disk)
    """

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


# Backward-compat name used in current managers/tests.
StoragePort = FileStoragePort


class LocalStorageClient:
    """
    Process-local file access (BZM_STORAGE_BACKEND=memory for MVP).

    Uses the existing path mapper so Docker volume mounts keep working.
    No external Storage Service — suitable for single-instance / stdio MVP.
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


class HttpStorageClient:
    """
    Fail-closed file storage for hosted HTTP (and future remote Storage Service).

    Every file lookup/upload path raises so local client paths cannot be used
    against a shared hosted instance. Phase 2 can replace these stubs with
    real remote Storage API calls.
    """

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


def resolve_storage_backend(raw: Optional[str] = None) -> StorageBackend:
    """Resolve BZM_STORAGE_BACKEND (default: memory)."""
    candidate = (
        raw if raw is not None else os.getenv("BZM_STORAGE_BACKEND", "memory")
    ).strip().lower()
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
) -> FileStoragePort:
    """
    Select file storage for the process.

    Hosted streamable-http always uses HttpStorageClient so local paths are
    rejected. Stdio uses LocalStorageClient when backend is memory (MVP default).
    """
    resolved = resolve_storage_backend(backend)
    if transport == "streamable-http" or resolved == "http":
        return HttpStorageClient()
    return LocalStorageClient()


@dataclass(frozen=True)
class SessionScope:
    user_id: str
    mcp_session_id: str


@dataclass(frozen=True)
class SessionPartitionPayload:
    metadata: dict[str, Any] | None = None
    dataframes: dict[str, Any] | None = None
    tasks: dict[str, Any] | None = None
    uploaded_files: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if self.metadata is not None:
            body["metadata"] = self.metadata
        if self.dataframes is not None:
            body["dataframes"] = self.dataframes
        if self.tasks is not None:
            body["tasks"] = self.tasks
        if self.uploaded_files is not None:
            body["uploaded_files"] = self.uploaded_files
        return body


@dataclass(frozen=True)
class SessionPartition:
    user_id: str
    mcp_session_id: str
    metadata: dict[str, Any]
    dataframes: dict[str, Any]
    tasks: dict[str, Any]
    uploaded_files: list[dict[str, Any]]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionPartition":
        return cls(
            user_id=str(data.get("user_id", "")),
            mcp_session_id=str(data.get("mcp_session_id", "")),
            metadata=data.get("metadata", {}) or {},
            dataframes=data.get("dataframes", {}) or {},
            tasks=data.get("tasks", {}) or {},
            uploaded_files=data.get("uploaded_files", []) or [],
        )


class SessionStoragePort(ABC):
    @abstractmethod
    async def put_partition(self, scope: SessionScope, payload: SessionPartitionPayload) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_partition(self, scope: SessionScope) -> SessionPartition | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_partition(self, scope: SessionScope) -> bool:
        raise NotImplementedError


class SessionScopeResolverPort(ABC):
    @abstractmethod
    def resolve(self, ctx: Context, token: Optional[BzmToken]) -> SessionScope:
        raise NotImplementedError


class DefaultSessionScopeResolver(SessionScopeResolverPort):
    """
    Resolve scope from request/ctx metadata.

    Hosted HTTP receives `Mcp-Session-Id` via header.
    Local stdio/docker falls back to FastMCP context session_id when available.
    """

    @staticmethod
    def _resolve_session_id(ctx: Context) -> str:
        request = getattr(getattr(ctx, "request_context", None), "request", None)
        if request is not None:
            session_id = request.headers.get("mcp-session-id")
            if session_id and session_id.strip():
                return session_id.strip()
        session_id = getattr(ctx, "session_id", None)
        if session_id is not None and str(session_id).strip():
            return str(session_id).strip()
        return "default"

    @staticmethod
    def _resolve_user_id(token: Optional[BzmToken]) -> str:
        if token is not None and token.id.strip():
            return token.id.strip()
        return "anonymous"

    def resolve(self, ctx: Context, token: Optional[BzmToken]) -> SessionScope:
        return SessionScope(
            user_id=self._resolve_user_id(token),
            mcp_session_id=self._resolve_session_id(ctx),
        )


class InMemorySessionStorageProvider(SessionStoragePort):
    def __init__(self) -> None:
        self._partitions: dict[tuple[str, str], SessionPartition] = {}

    async def put_partition(self, scope: SessionScope, payload: SessionPartitionPayload) -> None:
        existing = self._partitions.get((scope.user_id, scope.mcp_session_id))
        metadata = existing.metadata if existing else {}
        dataframes = existing.dataframes if existing else {}
        tasks = existing.tasks if existing else {}
        uploaded_files = existing.uploaded_files if existing else []

        if payload.metadata is not None:
            metadata = payload.metadata
        if payload.dataframes is not None:
            dataframes = payload.dataframes
        if payload.tasks is not None:
            tasks = payload.tasks
        if payload.uploaded_files is not None:
            uploaded_files = payload.uploaded_files

        self._partitions[(scope.user_id, scope.mcp_session_id)] = SessionPartition(
            user_id=scope.user_id,
            mcp_session_id=scope.mcp_session_id,
            metadata=metadata,
            dataframes=dataframes,
            tasks=tasks,
            uploaded_files=uploaded_files,
        )

    async def get_partition(self, scope: SessionScope) -> SessionPartition | None:
        return self._partitions.get((scope.user_id, scope.mcp_session_id))

    async def delete_partition(self, scope: SessionScope) -> bool:
        return self._partitions.pop((scope.user_id, scope.mcp_session_id), None) is not None


class HttpSessionStorageProvider(SessionStoragePort):
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 15.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout_seconds

    def _url_for_scope(self, scope: SessionScope) -> str:
        user_id = quote(scope.user_id, safe="")
        mcp_session_id = quote(scope.mcp_session_id, safe="")
        return f"{self._base_url}/session-partitions/{user_id}/{mcp_session_id}"

    def _health_url(self) -> str:
        return f"{self._base_url}/health"

    def ensure_available(self) -> None:
        """Fail fast if the storage API is unreachable."""
        with httpx.Client(timeout=min(self._timeout, 5.0)) as client:
            response = client.get(self._health_url())
            response.raise_for_status()

    async def put_partition(self, scope: SessionScope, payload: SessionPartitionPayload) -> None:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.put(
                self._url_for_scope(scope),
                json=payload.to_dict(),
            )
            response.raise_for_status()

    async def get_partition(self, scope: SessionScope) -> SessionPartition | None:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                self._url_for_scope(scope),
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return SessionPartition.from_dict(response.json())

    async def delete_partition(self, scope: SessionScope) -> bool:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.delete(
                self._url_for_scope(scope),
            )
            response.raise_for_status()
            payload = response.json()
            return bool(payload.get("deleted"))


# Backward-compat aliases for the feature branch naming.
InMemoryStorageProvider = InMemorySessionStorageProvider
HttpStorageProvider = HttpSessionStorageProvider
