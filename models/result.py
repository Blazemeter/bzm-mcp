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
from typing import Any, Optional, List

from mcp.types import CallToolResult, TextContent
from pydantic import BaseModel, Field

class BaseResult(BaseModel):
    result: Optional[List[Any]] = Field(description="Result List", default=None)
    total: Optional[int] = Field(description="Total available records", default=None)
    has_more: Optional[bool] = Field(description="More records per page to list", default=None)
    error: Optional[str] = Field(description="Error message", default=None)
    info: Optional[List[str]] = Field(description="Info messages", default=None)
    warning: Optional[List[str]] = Field(description="Warning messages", default=None)
    tool_call_started_at: Optional[str] = Field(description="ISO timestamp when tool action started", default=None)
    tool_call_finished_at: Optional[str] = Field(description="ISO timestamp when tool action finished", default=None)
    tool_call_duration_ms: Optional[int] = Field(description="Tool action duration in milliseconds", default=None)
    debug: Optional[dict[str, Any]] = Field(description="Optional debug metrics for tool calls", default=None)

    def append_warnings(self, messages: List[str]):
        if not self.warning:
            self.warning = []
        self.warning.extend(messages)

    def append_info(self, info: List[str]):
        if not self.info:
            self.info = []
        self.info.extend(info)

    def model_dump(self, **kwargs):
        return super().model_dump(exclude_none=True, **kwargs)

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(exclude_none=True, **kwargs)


class HttpBaseResult(BaseResult):
    result: Optional[Any] = Field(description="Result", default=None)


class ToolResult(CallToolResult):
    @classmethod
    def from_base_result(cls, base_result: BaseResult) -> "ToolResult":
        compact_text = base_result.model_dump_json(indent=2)
        structured = base_result.model_dump(mode="json")
        return cls(
            content=[TextContent(type="text", text=compact_text)],
            structuredContent=structured,
            isError=bool(base_result.error),
        )

    @property
    def result(self) -> Optional[List[Any]]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("result")

    @property
    def total(self) -> Optional[int]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("total")

    @property
    def has_more(self) -> Optional[bool]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("has_more")

    @property
    def error(self) -> Optional[str]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("error")

    @property
    def info(self) -> Optional[List[str]]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("info")

    @property
    def warning(self) -> Optional[List[str]]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("warning")

    @property
    def tool_call_started_at(self) -> Optional[str]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("tool_call_started_at")

    @property
    def tool_call_finished_at(self) -> Optional[str]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("tool_call_finished_at")

    @property
    def tool_call_duration_ms(self) -> Optional[int]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("tool_call_duration_ms")

    @property
    def debug(self) -> Optional[dict[str, Any]]:
        if not isinstance(self.structuredContent, dict):
            return None
        return self.structuredContent.get("debug")
