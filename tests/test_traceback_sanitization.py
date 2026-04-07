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

import os
import re

import pytest

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

    @pytest.mark.skipif(os.name != "nt", reason="Only supported on Windows")
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

    def test_sanitized_traceback_hides_mnt_paths(self):
        try:
            _raise_with_custom_filename("/mnt/secrets/private_script.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/mnt/secrets/private_script.py" not in sanitized
        assert "private_script.py" in sanitized

    def test_sanitized_traceback_hides_run_secrets_paths(self):
        try:
            _raise_with_custom_filename("/run/secrets/api_key.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/run/secrets/api_key.py" not in sanitized
        assert "api_key.py" in sanitized

    def test_sanitized_traceback_hides_root_paths(self):
        try:
            _raise_with_custom_filename("/root/.config/credentials.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/root/.config/credentials.py" not in sanitized
        assert "credentials.py" in sanitized

    def test_sanitized_traceback_hides_app_paths(self):
        try:
            _raise_with_custom_filename("/app/config/settings.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/app/config/settings.py" not in sanitized
        assert "settings.py" in sanitized

    def test_sanitized_traceback_hides_var_paths(self):
        try:
            _raise_with_custom_filename("/var/lib/secrets/token.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/var/lib/secrets/token.py" not in sanitized
        assert "token.py" in sanitized

    def test_sanitized_traceback_hides_etc_paths(self):
        try:
            _raise_with_custom_filename("/etc/credentials/config.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/etc/credentials/config.py" not in sanitized
        assert "config.py" in sanitized

    def test_sanitized_traceback_hides_data_paths(self):
        try:
            _raise_with_custom_filename("/data/secrets/private.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/data/secrets/private.py" not in sanitized
        assert "private.py" in sanitized

    @pytest.mark.skipif(os.name == "nt", reason="macOS paths not relevant on Windows")
    def test_sanitized_traceback_hides_macos_users_paths(self):
        try:
            _raise_with_custom_filename("/Users/david/secrets/private.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/Users/david/secrets/private.py" not in sanitized
        assert "private.py" in sanitized

    @pytest.mark.skipif(os.name == "nt", reason="macOS paths not relevant on Windows")
    def test_sanitized_traceback_hides_macos_library_paths(self):
        try:
            _raise_with_custom_filename("/Library/Application Support/config.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/Library/Application Support/config.py" not in sanitized

    @pytest.mark.skipif(os.name == "nt", reason="macOS paths not relevant on Windows")
    def test_sanitized_traceback_hides_macos_private_paths(self):
        try:
            _raise_with_custom_filename("/private/tmp/secret_script.py")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/private/tmp/secret_script.py" not in sanitized
        assert "secret_script.py" in sanitized

    def test_sanitized_traceback_does_not_redact_url_paths(self):
        # URL path segments like /api/v4/tests should not be mangled
        try:
            raise RuntimeError("Request failed for url 'https://a.blazemeter.com/api/v4/tests'")
        except RuntimeError as exc:
            sanitized = format_sanitized_traceback(exc)

        assert "/api/v4/tests" in sanitized
