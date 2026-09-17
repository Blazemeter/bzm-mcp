"""
File access abstractions for upload-oriented tools.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path

from config.storage import SessionScope


class FileAccessPort(ABC):
    """Abstraction for file path mapping and file content reads."""

    @abstractmethod
    def map_paths(self, file_paths: list[str], scope: SessionScope | None = None) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, file_path: str, scope: SessionScope | None = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_file(self, file_path: str, scope: SessionScope | None = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def read_bytes(self, file_path: str, scope: SessionScope | None = None) -> bytes:
        raise NotImplementedError


class LocalPathFileSource(FileAccessPort):
    """Use filesystem paths as provided by the caller."""

    def map_paths(self, file_paths: list[str], scope: SessionScope | None = None) -> list[str]:
        return file_paths

    def exists(self, file_path: str, scope: SessionScope | None = None) -> bool:
        return os.path.exists(file_path)

    def is_file(self, file_path: str, scope: SessionScope | None = None) -> bool:
        return os.path.isfile(file_path)

    def read_bytes(self, file_path: str, scope: SessionScope | None = None) -> bytes:
        return Path(file_path).read_bytes()


class DockerMappedFileSource(LocalPathFileSource):
    """
    Map host paths into the mounted container path and then read locally.

    This mirrors the old path mapper behavior for Docker stdio mode.
    """

    def __init__(
        self,
        source_working_directory: str,
        container_working_directory: str = "/home/bzm-mcp/working_directory",
    ) -> None:
        self._source_working_directory = Path(source_working_directory).resolve()
        self._container_working_directory = container_working_directory.rstrip("/\\")

    def map_paths(self, file_paths: list[str], scope: SessionScope | None = None) -> list[str]:
        mapped_paths: list[str] = []
        for file_path in file_paths:
            abs_file_path = Path(file_path).resolve()
            try:
                relative_path = abs_file_path.relative_to(self._source_working_directory)
                mapped_path = (
                    f"{self._container_working_directory}/{relative_path.as_posix()}"
                )
                mapped_paths.append(mapped_path)
            except ValueError:
                mapped_paths.append(file_path)
        return mapped_paths


def build_file_access(transport: str) -> FileAccessPort | None:
    """
    Build disk access for stdio / Docker stdio. Streamable-http has no disk:
    return None; HTTP upload_assets mints a URL via TicketPort instead.
    """
    if transport == "streamable-http":
        return None

    is_docker = os.getenv("MCP_DOCKER", "false").lower() == "true"
    if transport == "stdio" and is_docker:
        source_dir = os.getenv("SOURCE_WORKING_DIRECTORY")
        if not source_dir:
            raise ValueError(
                "Working directory must be set in the Docker catalog configuration."
                "Without volume mount, actions like upload assets will not work."
                "Lack of volume mount results in missing SOURCE_WORKING_DIRECTORY environment variable"
            )
        return DockerMappedFileSource(source_working_directory=source_dir)
    return LocalPathFileSource()
