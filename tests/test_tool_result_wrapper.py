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
