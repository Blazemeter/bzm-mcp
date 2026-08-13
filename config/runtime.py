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
import os
from typing import Any, Literal, Optional

from config.auth import AuthPort, HttpAuthProvider, StdioAuthProvider
from config.file_access import FileAccessPort, build_file_access
from config.storage import (
    DefaultSessionScopeResolver,
    HttpSessionStorageProvider,
    InMemorySessionStorageProvider,
    SessionScopeResolverPort,
    SessionStoragePort,
)
from config.token import BzmToken
from tools.utils import ConfirmMode

Transport = Literal["stdio", "streamable-http"]


@dataclass(frozen=True)
class AppRuntime:
    """Process-level collaborators shared by tool registrations."""

    transport: Transport
    auth: AuthPort
    storage: SessionStoragePort
    file_access: FileAccessPort
    scope_resolver: SessionScopeResolverPort
    user_config: dict[str, Any]


def build_user_config(runtime: AppRuntime, ctx) -> dict[str, Any]:
    user_config = dict(runtime.user_config)
    token = runtime.auth.get_token(ctx)
    if token is not None:
        user_config["token"] = token
    return user_config


def build_runtime(
        transport: Transport,
        startup_token: Optional[BzmToken] = None,
        startup_confirmation_mode: ConfirmMode = ConfirmMode.DELETE,
) -> AppRuntime:
    """
    Compose auth, file access, and session storage for the selected transport.

    - stdio: process-lifetime ``startup_token`` and in-memory session storage.
    - streamable-http: request-scoped auth and storage API-backed partitions.
    """
    if transport == "stdio":
        stdio_user_config = {
            "startup_token": startup_token,
            "token": startup_token,
            "confirmation_mode": startup_confirmation_mode.name,
        }
        return AppRuntime(
            transport=transport,
            auth=StdioAuthProvider(startup_token),
            storage=InMemorySessionStorageProvider(),
            file_access=build_file_access(transport),
            scope_resolver=DefaultSessionScopeResolver(),
            user_config=stdio_user_config,
        )

    if transport == "streamable-http":
        storage_base_url = os.getenv("BZM_STORAGE_API_BASE_URL", "").strip()
        if not storage_base_url:
            raise ValueError(
                "BZM_STORAGE_API_BASE_URL is required for streamable-http transport."
            )
        storage: SessionStoragePort = HttpSessionStorageProvider(
            base_url=storage_base_url,
        )
        storage.ensure_available()
        return AppRuntime(
            transport=transport,
            auth=HttpAuthProvider(),
            storage=storage,
            file_access=build_file_access(transport),
            scope_resolver=DefaultSessionScopeResolver(),
            user_config={},
        )

    raise ValueError(f"Unknown transport: {transport}")
