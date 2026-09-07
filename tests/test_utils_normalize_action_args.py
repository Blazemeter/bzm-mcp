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
from tools.utils import normalize_action_args


def test_normalize_action_args_standard_format():
    """Standard format: action + args nested."""
    action, args = normalize_action_args({
        "action": "list",
        "args": {"limit": 5, "project_id": 158903, "result_format": "dataframe"},
    })
    assert action == "list"
    assert args == {"limit": 5, "project_id": 158903, "result_format": "dataframe"}


def test_normalize_action_args_flat_format():
    """Flat format: action + params at top level merged into args."""
    action, args = normalize_action_args({
        "action": "read",
        "test_id": 123,
    })
    assert action == "read"
    assert args == {"test_id": 123}


def test_normalize_action_args_double_wrapped():
    """Double-wrapped format: {"arguments": {"action": "x", "args": {...}}}."""
    action, args = normalize_action_args({
        "arguments": {
            "action": "list",
            "args": {
                "limit": 5,
                "project_id": 158903,
                "result_format": "dataframe",
            },
        },
    })
    assert action == "list"
    assert args == {"limit": 5, "project_id": 158903, "result_format": "dataframe"}


def test_normalize_action_args_double_wrapped_with_action_only():
    """Double-wrapped with only action (no args) still unwraps."""
    action, args = normalize_action_args({
        "arguments": {"action": "list_help_categories"},
    })
    assert action == "list_help_categories"
    assert args == {}


def test_normalize_action_args_does_not_unwrap_when_extra_keys():
    """When top-level has other keys besides 'arguments', do not unwrap."""
    action, args = normalize_action_args({
        "arguments": {"action": "x", "args": {}},
        "other_key": "value",
    })
    assert action == ""
    assert "arguments" in args
    assert args["other_key"] == "value"
