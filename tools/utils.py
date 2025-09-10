"""
Simple utilities for BlazeMeter MCP tools.
"""
from datetime import datetime
from typing import Optional, Callable

import httpx

from config.blazemeter import BZM_API_BASE_URL
from config.token import BzmToken
from models.result import BaseResult


async def api_request(token: Optional[BzmToken], method: str, endpoint: str, result_formatter: Callable = None,
                      **kwargs) -> BaseResult:
    """
    Make an authenticated request to the BlazeMeter API.
    Handles authentication errors gracefully.
    """
    if not token:
        return BaseResult(
            error="No API token. Set BLAZEMETER_API_KEY env var."
        )

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = token.as_basic_auth()

    async with (httpx.AsyncClient(base_url=BZM_API_BASE_URL) as client):
        try:
            resp = await client.request(method, endpoint, headers=headers, **kwargs)
            resp.raise_for_status()
            response_dict = resp.json()
            result = response_dict.get("result", [])
            default_total = 0
            if not isinstance(result, list):  # Generalize result always as a list
                result = [result]
                default_total = 1
            final_result = result_formatter(result) if result_formatter else result
            return BaseResult(
                result=final_result,
                error=response_dict.get("error", None),
                total=response_dict.get("total", default_total),
                has_more=response_dict.get("total", 0) - (
                        response_dict.get("skip", 0) + response_dict.get("limit", 0)) > 0
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [401, 403]:
                return BaseResult(
                    error="Invalid credentials"
                )
            raise


def get_date_time_iso(timestamp: int) -> Optional[str]:
    if timestamp is None:
        return None
    else:
        return datetime.fromtimestamp(timestamp).isoformat()
