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
from unittest.mock import MagicMock

import pytest

from config.auth import HttpAuthProvider
from config.blazemeter import TOOLS_PREFIX
from config.runtime import AppRuntime, build_runtime
from config.storage import DefaultSessionScopeResolver, InMemorySessionStorageProvider
from tools.actions import ALL, HTTP, STDIO, ActionSpec, filter_actions, render_description
from tools.actions.tests import ACTIONS, HEADER, HINTS
from tools.test_manager import build_test_handlers, register as register_tests_tool


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


def _http_runtime():
    return AppRuntime(
        transport="streamable-http",
        auth=HttpAuthProvider(),
        storage=InMemorySessionStorageProvider(),
        file_access=None,
        scope_resolver=DefaultSessionScopeResolver(),
        user_config={},
        tickets=object(),
    )


class TestFilterActions:
    def test_keeps_matching_transport_and_drops_the_other(self):
        specs = (
            ActionSpec("shared", ALL, "ok"),
            ActionSpec("upload_assets", frozenset({STDIO}), "files"),
            ActionSpec("upload_assets", frozenset({HTTP}), "mint"),
        )
        stdio = filter_actions(STDIO, specs)
        http = filter_actions(HTTP, specs)
        assert [spec.body for spec in stdio if spec.name == "upload_assets"] == ["files"]
        assert [spec.body for spec in http if spec.name == "upload_assets"] == ["mint"]
        assert {spec.name for spec in stdio} == {"shared", "upload_assets"}
        assert {spec.name for spec in http} == {"shared", "upload_assets"}

    def test_duplicate_name_after_filter_raises(self):
        specs = (
            ActionSpec("read", ALL, "a"),
            ActionSpec("read", frozenset({STDIO}), "b"),
        )
        with pytest.raises(ValueError, match="Duplicate action names for stdio"):
            filter_actions(STDIO, specs)


class TestRenderDescription:
    def test_joins_header_actions_and_hints(self):
        rendered = render_description(
            "Operations on tests.",
            (ActionSpec("read", ALL, "Read a test."),),
            ("- Follow the schema.",),
        )
        assert rendered.startswith("Operations on tests.\nActions:\n- read: Read a test.")
        assert "Hints:\n- Follow the schema.\n" in rendered


class TestTestActionsCatalog:
    def test_unique_catalog_names_match_dispatch_arms(self):
        handler_names = set(build_test_handlers(MagicMock(), STDIO))
        assert {spec.name for spec in ACTIONS} == handler_names

    def test_required_args_appear_in_body(self):
        for spec in ACTIONS:
            for arg_name in spec.required_args:
                assert arg_name in spec.body, f"{spec.name} missing {arg_name} in body"

    def test_bodies_do_not_repeat_name_prefix(self):
        for spec in ACTIONS:
            assert not spec.body.lstrip().startswith(f"- {spec.name}:")

    def test_http_description_is_mint_contract(self):
        mcp = RecordingMcp()
        register_tests_tool(mcp, _http_runtime())
        description = mcp.descriptions[f"{TOOLS_PREFIX}_tests"]
        assert "sha256" in description
        assert "does not accept file bytes" in description
        assert "file_paths" not in description

    def test_stdio_description_is_local_paths(self):
        mcp = RecordingMcp()
        register_tests_tool(mcp, build_runtime("stdio"))
        description = mcp.descriptions[f"{TOOLS_PREFIX}_tests"]
        assert "file_paths" in description
        assert "X-Content-SHA256" not in description
        assert HEADER in description
        assert HINTS[0] in description
