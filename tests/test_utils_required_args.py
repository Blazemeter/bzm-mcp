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
from models.result import BaseResult
from tools.utils import validate_required_args, validate_non_empty_str_arg


def test_validate_required_args_missing():
    err = validate_required_args("read", {}, ["account_id"])
    assert err is not None
    assert "account_id" in err.error


def test_validate_required_args_present():
    assert validate_required_args("read", {"account_id": 1}, ["account_id"]) is None


def test_validate_non_empty_str_arg():
    assert validate_non_empty_str_arg("x", {"task_id": "  "}, "task_id") is not None
    assert validate_non_empty_str_arg("x", {"task_id": "abc"}, "task_id") is None
