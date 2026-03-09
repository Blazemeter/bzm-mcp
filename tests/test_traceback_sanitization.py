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

import re

from tools.utils import format_sanitized_traceback


def _raise_with_custom_filename(filename: str):
    compiled = compile("def boom():\n    raise RuntimeError('boom')\nboom()", filename, "exec")
    exec(compiled, {})  # noqa: S102 - used for controlled traceback generation in tests


def _raise_cause_chain_with_custom_filename(filename: str):
    source = (
        "def inner():\n"
        "    raise ValueError('inner')\n"
        "def outer():\n"
        "    try:\n"
        "        inner()\n"
        "    except ValueError as exc:\n"
        "        raise RuntimeError('outer') from exc\n"
        "outer()"
    )
    compiled = compile(source, filename, "exec")
    exec(compiled, {})  # noqa: S102 - controlled traceback generation for testing


def _raise_context_chain_with_custom_filename(filename: str):
    source = (
        "def inner():\n"
        "    raise ValueError('inner')\n"
        "def outer():\n"
        "    try:\n"
        "        inner()\n"
        "    except ValueError:\n"
        "        raise RuntimeError('outer')\n"
        "outer()"
    )
    compiled = compile(source, filename, "exec")
    exec(compiled, {})  # noqa: S102 - controlled traceback generation for testing


class TestTracebackSanitization:
    def test_sanitized_traceback_hides_unix_absolute_paths(self):
        try:
            _raise_with_custom_filename("/tmp/secret/runtime/private_script.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "RuntimeError: boom" in sanitized
        assert "private_script.py" in sanitized
        assert "/tmp/secret/runtime/private_script.py" not in sanitized

    def test_sanitized_traceback_hides_windows_absolute_paths(self):
        try:
            _raise_with_custom_filename(r"C:\secret\runtime\private_script.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "RuntimeError: boom" in sanitized
        assert "private_script.py" in sanitized
        assert r"C:\secret\runtime\private_script.py" not in sanitized

    def test_sanitized_traceback_keeps_project_relative_path(self):
        try:
            raise ValueError("relative check")
        except ValueError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "ValueError: relative check" in sanitized
        assert "tests/test_traceback_sanitization.py" in sanitized
        assert not re.search(r"[A-Za-z]:\\", sanitized)

    def test_sanitized_traceback_hides_paths_for_cause_chain(self):
        try:
            _raise_cause_chain_with_custom_filename("/tmp/secret/runtime/chain.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "RuntimeError: outer" in sanitized
        assert "ValueError: inner" in sanitized
        assert "/tmp/secret/runtime/chain.py" not in sanitized
        assert "chain.py" in sanitized

    def test_sanitized_traceback_hides_paths_for_context_chain(self):
        try:
            _raise_context_chain_with_custom_filename(r"C:\secret\runtime\chain.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "RuntimeError: outer" in sanitized
        assert "ValueError: inner" in sanitized
        assert r"C:\secret\runtime\chain.py" not in sanitized
        assert "chain.py" in sanitized
