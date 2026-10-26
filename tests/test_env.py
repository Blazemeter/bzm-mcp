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
from config.env import env_float, env_int, env_str
from config.service_auth import service_caller_token


def test_unset_or_blank_uses_default(monkeypatch):
    monkeypatch.delenv("BZM_MCP_SOME_VALUE", raising=False)
    assert env_int("SOME_VALUE", 7) == 7
    monkeypatch.setenv("BZM_MCP_SOME_VALUE", "   ")
    assert env_str("SOME_VALUE", "fallback") == "fallback"


def test_values_are_read_with_the_prefix(monkeypatch):
    monkeypatch.setenv("BZM_MCP_SOME_VALUE", "42")
    assert env_int("SOME_VALUE", 7) == 42
    assert env_float("SOME_VALUE", 1.5) == 42.0
    assert env_str("SOME_VALUE") == "42"


def test_invalid_or_below_minimum_falls_back_to_default(monkeypatch):
    monkeypatch.setenv("BZM_MCP_SOME_VALUE", "not-a-number")
    assert env_int("SOME_VALUE", 7) == 7
    assert env_float("SOME_VALUE", 1.5) == 1.5
    monkeypatch.setenv("BZM_MCP_SOME_VALUE", "0")
    assert env_int("SOME_VALUE", 7, minimum=1) == 7


def test_service_caller_token_prefers_generic_then_ticket_variable(monkeypatch):
    monkeypatch.delenv("BZM_MCP_STORAGE_CALLER_TOKEN", raising=False)
    monkeypatch.setenv("BZM_MCP_TICKET_STORAGE_CALLER_TOKEN", "ticket-token")
    assert service_caller_token() == "ticket-token"
    monkeypatch.setenv("BZM_MCP_STORAGE_CALLER_TOKEN", "storage-token")
    assert service_caller_token() == "storage-token"
