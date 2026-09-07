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
from __future__ import annotations

import ast
import asyncio
import importlib
from pathlib import Path

import pytest

from config.blazemeter import SUPPORT_MESSAGE
from config.runtime import build_runtime
from tools.mcp_entrypoint import register_managed_tool

TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
HARDCODED_SUPPORT_SNIPPET = "If you think this is a bug, please contact BlazeMeter support"

MANAGER_MODULES = (
    "tools.account_manager",
    "tools.billing_manager",
    "tools.execution_manager",
    "tools.help_manager",
    "tools.project_manager",
    "tools.skills_manager",
    "tools.test_manager",
    "tools.tools_manager",
    "tools.user_manager",
    "tools.workspace_manager",
)

# tools_manager wraps other tools; it opts out so callers do not see the message twice.
OPT_OUT_MODULES = frozenset({"tools.tools_manager"})


class FakeMcp:
    def __init__(self):
        self.tools = {}

    def tool(self, name, description):
        def decorator(func):
            self.tools[name] = func
            return func

        return decorator


def _literal_strings(tree: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            found.append(node.value)
        elif isinstance(node, ast.JoinedStr):
            parts: list[str] = []
            for value in node.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    parts.append(value.value)
            if parts:
                found.append("".join(parts))
    return found


def test_support_message_is_defined_once_in_config():
    assert "https://github.com/Blazemeter/bzm-mcp/issues" in SUPPORT_MESSAGE
    assert HARDCODED_SUPPORT_SNIPPET in SUPPORT_MESSAGE


def test_tool_modules_do_not_hardcode_the_support_message():
    offenders: list[str] = []
    for path in sorted(TOOLS_DIR.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        if any(HARDCODED_SUPPORT_SNIPPET in value for value in _literal_strings(tree)):
            offenders.append(path.name)
    assert offenders == [], (
        f"Hardcoded support text in {offenders}; import SUPPORT_MESSAGE from config.blazemeter"
    )


@pytest.mark.parametrize("module_name", MANAGER_MODULES)
def test_managers_pass_central_support_message(module_name, monkeypatch):
    captured: dict = {}

    def fake_register(*args, **kwargs):
        captured.update(kwargs)

        async def _tool(*_args, **_kwargs):
            return None

        return _tool

    module = importlib.import_module(module_name)
    monkeypatch.setattr(module, "register_managed_tool", fake_register)
    module.register(FakeMcp(), build_runtime("stdio"))

    if module_name in OPT_OUT_MODULES:
        assert captured.get("support_message") is None
        return

    assert captured.get("support_message", SUPPORT_MESSAGE) is SUPPORT_MESSAGE


def test_unexpected_error_appends_support_message_by_default(monkeypatch):
    async def boom(*_args, **_kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("tools.mcp_entrypoint.run_tool_with_runtime", boom)
    mcp = FakeMcp()
    register_managed_tool(
        mcp,
        build_runtime("stdio"),
        name="demo",
        description="demo",
        dispatch=_unused_dispatch,
    )

    result = asyncio.run(mcp.tools["demo"]({"action": "read"}, ctx=None))
    assert result.error is not None
    assert SUPPORT_MESSAGE in result.error


def test_opt_out_omits_support_message(monkeypatch):
    async def boom(*_args, **_kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("tools.mcp_entrypoint.run_tool_with_runtime", boom)
    mcp = FakeMcp()
    register_managed_tool(
        mcp,
        build_runtime("stdio"),
        name="demo",
        description="demo",
        dispatch=_unused_dispatch,
        support_message=None,
    )

    result = asyncio.run(mcp.tools["demo"]({"action": "read"}, ctx=None))
    assert result.error is not None
    assert SUPPORT_MESSAGE not in result.error


async def _unused_dispatch(action, args, token, ctx):
    raise AssertionError("dispatch should not run when run_tool_with_runtime is stubbed")
