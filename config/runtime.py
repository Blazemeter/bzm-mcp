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

from config.auth import AuthPort, HttpAuthProvider, StdioAuthProvider
from config.token import BzmToken

Transport = Literal["stdio", "streamable-http"]


@dataclass(frozen=True)
class AppRuntime:
    """Process-level collaborators shared by tool registrations."""

    transport: Transport
    auth: AuthPort


def build_runtime(
        transport: Transport,
        startup_token: Optional[BzmToken] = None,
) -> AppRuntime:
    """
    Compose auth for the selected transport.

    - stdio: use process-lifetime ``startup_token`` (from env / api-key.json / Docker).
    - streamable-http: resolve credentials per request via Bearer middleware + HttpAuthProvider.
    """
    if transport == "stdio":
        return AppRuntime(transport=transport, auth=StdioAuthProvider(startup_token))
    if transport == "streamable-http":
        return AppRuntime(transport=transport, auth=HttpAuthProvider())
    raise ValueError(f"Unknown transport: {transport}")
