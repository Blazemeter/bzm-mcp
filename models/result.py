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

from pydantic import BaseModel, Field

class BaseResult(BaseModel):
    result: Optional[List[Any]] = Field(description="Result List", default=None)
    total: Optional[int] = Field(description="Total available records", default=None)
    has_more: Optional[bool] = Field(description="More records per page to list", default=None)
    error: Optional[str] = Field(description="Error message", default=None)
    info: Optional[List[str]] = Field(description="Info messages", default=None)
    warning: Optional[List[str]] = Field(description="Warning messages", default=None)

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
