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
    def resolve(self) -> SessionScope:
        raise NotImplementedError


class DefaultSessionScopeResolver(SessionScopeResolverPort):
    """
    Resolve the partition from the validated chat session of the current tool call.

    The tool entrypoint binds the verified BlazeMeter user and the ACTIVE session
    it owns; nothing else (transport Mcp-Session-Id, FastMCP ctx.session_id, the raw
    token id) is trusted. Outside a validated call this fails closed instead of
    falling back to a shared partition.
    """

    def resolve(self) -> SessionScope:
        from config.session_context import SessionContextMissing, current_identity, current_session

        identity = current_identity()
        session = current_session()
        if identity is None or session is None:
            raise SessionContextMissing(
                "No validated session in this call; session-scoped data needs a session_id."
            )
        return SessionScope(user_id=identity.user_id, mcp_session_id=session.session_id)


def resolve_session_scope(
        scope_resolver: Optional[SessionScopeResolverPort] = None,
) -> SessionScope:
    """Resolve partition keys for the current validated chat session."""
    resolver = scope_resolver or DefaultSessionScopeResolver()
    return resolver.resolve()


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

    def discard_session(self, user_id: str, mcp_session_id: str) -> None:
        """Drop a purged session's partition (stdio session provider ``on_purge``)."""
        self._partitions.pop((user_id, mcp_session_id), None)


class HttpSessionStorageProvider(SessionStoragePort):
    def __init__(
        self,
        base_url: str,
        timeout_seconds: Optional[float] = None,
        caller_token: Optional[str] = None,
    ) -> None:
        from config.http_clients import SharedAsyncClient
        from config.session import SESSION_STORAGE_TIMEOUT_SECONDS

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout_seconds if timeout_seconds is not None else SESSION_STORAGE_TIMEOUT_SECONDS
        # Shared: partitions are read and written on most tool calls.
        self._http = SharedAsyncClient(lambda: httpx.AsyncClient(http2=True, timeout=self._timeout))
        # The storage-api only serves partitions to the MCP caller identity.
        self._caller_token = caller_token

    def _request_headers(self) -> dict[str, str]:
        """Caller identity plus the end-user credential of the current validated call."""
        from config.session_context import current_credential
        from config.service_auth import service_headers

        return service_headers(self._caller_token, current_credential())

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
        response = await self._http.get().put(
            self._url_for_scope(scope),
            headers=self._request_headers(),
            json=payload.to_dict(),
        )
        response.raise_for_status()

    async def get_partition(self, scope: SessionScope) -> SessionPartition | None:
        response = await self._http.get().get(
            self._url_for_scope(scope),
            headers=self._request_headers(),
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return SessionPartition.from_dict(response.json())

    async def delete_partition(self, scope: SessionScope) -> bool:
        response = await self._http.get().delete(
            self._url_for_scope(scope),
            headers=self._request_headers(),
        )
        response.raise_for_status()
        payload = response.json()
        return bool(payload.get("deleted"))


