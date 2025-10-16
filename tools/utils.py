"""
Simple utilities for BlazeMeter MCP tools.
"""
import os
import platform
from datetime import datetime

from typing import Optional, Callable

import httpx

from config.blazemeter import BZM_API_BASE_URL
from config.token import BzmToken
from config.version import __version__
from models.result import BaseResult

so = platform.system()       # "Windows", "Linux", "Darwin"
version = platform.version() # kernel / build version
release = platform.release() # ex. "10", "5.15.0-76-generic"
machine = platform.machine() # ex. "x86_64", "AMD64", "arm64"

ua_part = f"{so} {release}; {machine}"

async def api_request(token: Optional[BzmToken], method: str, endpoint: str,
                      result_formatter: Callable = None,
                      result_formatter_params: Optional[dict] = None,
                      **kwargs) -> BaseResult:
    """
    Make an authenticated request to the BlazeMeter API.
    Handles authentication errors gracefully.
    """
    if not token:
        return BaseResult(
            error="No API token. Set BLAZEMETER_API_KEY env var with file path or API_KEY_ID and API_KEY_SECRET secrets in docker catalog configuration."
        )

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = token.as_basic_auth()
    headers["User-Agent"] = f"bzm-mcp/{__version__} ({ua_part})"

    timeout = httpx.Timeout(
        connect=15.0,
        read=60.0,
        write=15.0,
        pool=60.0
    )

    # Read SSL_CERT_FILE environment variable for custom CA certificates
    # This is needed in Docker environments with self-signed certificates or custom CAs
    # verify = os.environ.get("SSL_CERT_FILE", True)
    
    async with (httpx.AsyncClient(base_url=BZM_API_BASE_URL, http2=True, timeout=timeout) as client):
        try:
            resp = await client.request(method, endpoint, headers=headers, **kwargs)
            resp.raise_for_status()
            response_dict = resp.json()
            result = response_dict.get("result", [])
            default_total = 0
            if not isinstance(result, list):  # Generalize result always as a list
                result = [result]
                default_total = 1
            final_result = result_formatter(result, result_formatter_params) if result_formatter else result
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
