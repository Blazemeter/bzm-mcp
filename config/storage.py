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

import os
from pathlib import Path
from typing import List, Literal, Optional, Protocol, runtime_checkable

from config.path_mapper import PathMapperFactory, PathMappingStrategy

StorageBackend = Literal["memory", "http"]

HOSTED_FILE_ACCESS_MESSAGE = (
    "Local file lookup and upload are not supported on the hosted MCP server. "
    "Use a local stdio/Docker MCP installation for upload_assets, or wait for "
    "Phase 2 remote Storage."
)


class StorageNotSupportedError(NotImplementedError):
    """Raised when a storage backend cannot fulfill a file operation."""


@runtime_checkable
class StoragePort(Protocol):
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

    Hosted streamable-http always uses HttpStorageClient so local paths are
    rejected. Stdio uses LocalStorageClient when backend is memory (MVP default).
    """
    resolved = resolve_storage_backend(backend)
    if transport == "streamable-http" or resolved == "http":
        return HttpStorageClient()
    return LocalStorageClient()
