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
from typing import Any, Optional
from urllib.parse import quote

import httpx
from mcp.server.fastmcp import Context

from config.token import BzmToken


class StorageNotConfiguredError(RuntimeError):
    """Raised when session storage is used before AppRuntime wiring."""


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
    def resolve(self, ctx: Optional[Context], token: Optional[BzmToken]) -> SessionScope:
        raise NotImplementedError


class DefaultSessionScopeResolver(SessionScopeResolverPort):
    """
    Resolve scope from request/ctx metadata.

    Hosted HTTP receives `Mcp-Session-Id` via header.
    Local stdio/docker falls back to FastMCP context session_id when available.
    """

    @staticmethod
    def _resolve_session_id(ctx: Optional[Context]) -> str:
        if ctx is None:
            return "default"
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

    def resolve(self, ctx: Optional[Context], token: Optional[BzmToken]) -> SessionScope:
        return SessionScope(
            user_id=self._resolve_user_id(token),
            mcp_session_id=self._resolve_session_id(ctx),
        )


def resolve_session_scope(
        ctx: Any,
        token: Optional[BzmToken] = None,
        scope_resolver: Optional[SessionScopeResolverPort] = None,
) -> SessionScope:
    """Resolve partition keys from auth token + MCP session context."""
    resolver = scope_resolver or DefaultSessionScopeResolver()
    resolved_token = token
    if resolved_token is None:
        from config.context_resolution import resolve_ctx_token
        resolved_token = resolve_ctx_token(ctx)
    return resolver.resolve(ctx, resolved_token)


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
        with httpx.Client(http2=True, timeout=min(self._timeout, 5.0)) as client:
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


