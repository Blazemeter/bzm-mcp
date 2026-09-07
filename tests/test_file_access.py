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

import pytest

from config.file_access import (
    DockerMappedFileSource,
    LocalPathFileSource,
    StorageFileSource,
    build_file_access,
)


class TestBuildFileAccess:
    def test_stdio_defaults_to_local_path_source(self, monkeypatch):
        monkeypatch.setenv("MCP_DOCKER", "false")
        source = build_file_access("stdio")
        assert isinstance(source, LocalPathFileSource)

    def test_stdio_docker_requires_source_working_directory(self, monkeypatch):
        monkeypatch.setenv("MCP_DOCKER", "true")
        monkeypatch.delenv("SOURCE_WORKING_DIRECTORY", raising=False)
        with pytest.raises(ValueError, match="Working directory must be set"):
            build_file_access("stdio")

    def test_stdio_docker_uses_mapped_source(self, monkeypatch):
        monkeypatch.setenv("MCP_DOCKER", "true")
        monkeypatch.setenv("SOURCE_WORKING_DIRECTORY", "/Users/me/work")
        source = build_file_access("stdio")
        assert isinstance(source, DockerMappedFileSource)

    def test_streamable_http_requires_storage_api_base_url(self, monkeypatch):
        monkeypatch.delenv("BZM_STORAGE_API_BASE_URL", raising=False)
        with pytest.raises(ValueError, match="BZM_STORAGE_API_BASE_URL is required"):
            build_file_access("streamable-http")

    def test_streamable_http_uses_storage_file_source(self, monkeypatch):
        monkeypatch.setenv("BZM_STORAGE_API_BASE_URL", "https://mcp-storage.internal")
        monkeypatch.setattr(StorageFileSource, "ensure_available", lambda self: None)
        source = build_file_access("streamable-http")
        assert isinstance(source, StorageFileSource)


class TestLocalPathFileSource:
    def test_exists_is_file_and_read_bytes(self, tmp_path):
        test_file = tmp_path / "demo.txt"
        test_file.write_text("hello", encoding="utf-8")

        source = LocalPathFileSource()
        assert source.map_paths([str(test_file)]) == [str(test_file)]
        assert source.exists(str(test_file)) is True
        assert source.is_file(str(test_file)) is True
        assert source.read_bytes(str(test_file)) == b"hello"


class TestDockerMappedFileSource:
    def test_map_paths_inside_source_directory(self, tmp_path):
        source_root = tmp_path / "workspace"
        source_root.mkdir()
        test_file = source_root / "suite.jmx"
        test_file.write_text("xml", encoding="utf-8")

        source = DockerMappedFileSource(
            source_working_directory=str(source_root),
            container_working_directory="/home/bzm-mcp/working_directory",
        )
        mapped = source.map_paths([str(test_file)])
        assert mapped == ["/home/bzm-mcp/working_directory/suite.jmx"]

    def test_map_paths_outside_source_directory_remains_unchanged(self, tmp_path):
        source_root = tmp_path / "workspace"
        source_root.mkdir()
        external_file = tmp_path / "external.csv"
        external_file.write_text("1,2", encoding="utf-8")

        source = DockerMappedFileSource(
            source_working_directory=str(source_root),
            container_working_directory="/home/bzm-mcp/working_directory",
        )
        mapped = source.map_paths([str(external_file)])
        assert mapped == [str(external_file)]
