"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    10|Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import pytest

from config.blazemeter import TOOLS_PREFIX
from config.runtime import build_runtime
from config.storage import HttpSessionStorageProvider
from tools.action_spec import ALL, HTTP, STDIO, ActionSpec, filter_actions, render_description
from tools.test_actions import TEST_ACTIONS, TEST_HINTS, TEST_TOOL_HEADER
from tools.test_manager import TEST_DISPATCH_ACTIONS, register as register_tests_tool


class RecordingMcp:
    def __init__(self):
        self.tools = {}
        self.descriptions = {}

    def tool(self, name, description):
        def decorator(func):
            self.tools[name] = func
            self.descriptions[name] = description
            return func

        return decorator


def _http_runtime(monkeypatch):
    monkeypatch.setenv("BZM_STORAGE_API_BASE_URL", "https://mcp-storage.internal")
    monkeypatch.setattr(HttpSessionStorageProvider, "ensure_available", lambda self: None)
    return build_runtime("streamable-http")


class TestFilterActions:
    def test_keeps_matching_transport_and_drops_the_other(self):
        specs = (
            ActionSpec("shared", ALL, "- shared: ok"),
            ActionSpec("upload_assets", frozenset({STDIO}), "- upload_assets: files"),
            ActionSpec("upload_assets", frozenset({HTTP}), "- upload_assets: mint"),
        )
        stdio = filter_actions(STDIO, specs)
        http = filter_actions(HTTP, specs)
        assert [spec.body for spec in stdio if spec.name == "upload_assets"] == [
            "- upload_assets: files"
        ]
        assert [spec.body for spec in http if spec.name == "upload_assets"] == [
            "- upload_assets: mint"
        ]
        assert {spec.name for spec in stdio} == {"shared", "upload_assets"}
        assert {spec.name for spec in http} == {"shared", "upload_assets"}

    def test_duplicate_name_after_filter_raises(self):
        specs = (
            ActionSpec("read", ALL, "- read: a"),
            ActionSpec("read", frozenset({STDIO}), "- read: b"),
        )
        with pytest.raises(ValueError, match="Duplicate action names for stdio"):
            filter_actions(STDIO, specs)


class TestRenderDescription:
    def test_joins_header_actions_and_hints(self):
        rendered = render_description(
            "Operations on tests.",
            (ActionSpec("read", ALL, "- read: Read a test."),),
            ("- Follow the schema.",),
        )
        assert rendered.startswith("Operations on tests.\nActions:\n- read: Read a test.")
        assert "Hints:\n- Follow the schema.\n" in rendered


class TestTestActionsCatalog:
    def test_unique_catalog_names_match_dispatch_arms(self):
        assert {spec.name for spec in TEST_ACTIONS} == TEST_DISPATCH_ACTIONS

    def test_http_description_uses_local_path_schema(self, monkeypatch):
        mcp = RecordingMcp()
        register_tests_tool(mcp, _http_runtime(monkeypatch))
        description = mcp.descriptions[f"{TOOLS_PREFIX}_tests"]
        assert "file_paths" in description
        assert "X-Content-SHA256" not in description

    def test_stdio_description_is_local_paths(self):
        mcp = RecordingMcp()
        register_tests_tool(mcp, build_runtime("stdio"))
        description = mcp.descriptions[f"{TOOLS_PREFIX}_tests"]
        assert "file_paths" in description
        assert "X-Content-SHA256" not in description
        assert TEST_TOOL_HEADER in description
        assert TEST_HINTS[0] in description
