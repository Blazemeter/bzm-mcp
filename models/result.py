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
