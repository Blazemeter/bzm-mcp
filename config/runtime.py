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
from dataclasses import dataclass
from typing import Literal, Optional
import os

from config.auth import AuthPort, HttpAuthProvider, StdioAuthProvider
from config.storage import (
    DefaultSessionScopeResolver,
    FileStoragePort,
    HttpSessionStorageProvider,
    InMemorySessionStorageProvider,
    SessionScopeResolverPort,
    SessionStoragePort,
    build_storage,
)
from config.token import BzmToken

Transport = Literal["stdio", "streamable-http"]


@dataclass(frozen=True)
class AppRuntime:
    """Process-level collaborators shared by tool registrations."""

    transport: Transport
    auth: AuthPort
    storage: FileStoragePort
    session_storage: SessionStoragePort
    scope_resolver: SessionScopeResolverPort


def build_runtime(
        transport: Transport,
        startup_token: Optional[BzmToken] = None,
        storage_backend: Optional[str] = None,
) -> AppRuntime:
    """
    Compose auth and storage for the selected transport.

    - stdio: process-lifetime ``startup_token`` + local/memory file storage.
    - streamable-http: request-scoped auth + hosted-safe file storage, and
      external session-partition persistence when BZM_STORAGE_API_BASE_URL is set.
    """
    file_storage = build_storage(transport, backend=storage_backend)

    if transport == "stdio":
        return AppRuntime(
            transport=transport,
            auth=StdioAuthProvider(startup_token),
            storage=file_storage,
            session_storage=InMemorySessionStorageProvider(),
            scope_resolver=DefaultSessionScopeResolver(),
        )

    if transport == "streamable-http":
        storage_base_url = os.getenv("BZM_STORAGE_API_BASE_URL", "").strip()
        if storage_base_url:
            session_storage: SessionStoragePort = HttpSessionStorageProvider(
                base_url=storage_base_url,
            )
            session_storage.ensure_available()
        else:
            session_storage = InMemorySessionStorageProvider()

        return AppRuntime(
            transport=transport,
            auth=HttpAuthProvider(),
            storage=file_storage,
            session_storage=session_storage,
            scope_resolver=DefaultSessionScopeResolver(),
        )

    raise ValueError(f"Unknown transport: {transport}")
