"""
Simple utilities for BlazeMeter MCP tools.
"""

from typing import Any, Dict, Optional, List

import httpx
from pydantic import BaseModel, Field

from config.blazemeter import BZM_API_BASE_URL
from config.token import BzmToken


async def api_request(token: Optional[BzmToken], method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """
    Make an authenticated request to the BlazeMeter API.
    Handles authentication errors gracefully.
    """
    if not token:
        return {"error": "No API token. Set BLAZEMETER_API_KEY env var."}

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = token.as_basic_auth()

    async with httpx.AsyncClient(base_url=BZM_API_BASE_URL) as client:
        try:
            resp = await client.request(method, endpoint, headers=headers, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [401, 403]:
                return {"error": "Invalid credentials"}
            raise


class BaseResult(BaseModel):
    result: Optional[List[Any]] = Field(description="Result List", default=None)
    has_more: Optional[bool] = Field(description="More records per page to list", default=None)
    error: Optional[str] = Field(description="Error message", default=None)

    def model_dump(self, **kwargs):
        return super().model_dump(exclude_none=True, **kwargs)

    def model_dump_json(self, **kwargs):
        return super().model_dump_json(exclude_none=True, **kwargs)
