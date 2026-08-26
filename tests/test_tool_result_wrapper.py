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
from models.result import BaseResult, ToolResult


def test_tool_result_from_base_result_builds_pretty_text_and_structured_content():
    base = BaseResult(result=[{"ok": True}], info=["done"])
    wrapped = ToolResult.from_base_result(base)

    assert wrapped.isError is False
    assert wrapped.structuredContent == base.model_dump(mode="json")
    assert wrapped.content[0].type == "text"
    assert wrapped.content[0].text == base.model_dump_json(indent=2)
    assert "\n" in wrapped.content[0].text


def test_tool_result_from_base_result_marks_error():
    base = BaseResult(error="boom")
    wrapped = ToolResult.from_base_result(base)

    assert wrapped.isError is True
    assert wrapped.error == "boom"
