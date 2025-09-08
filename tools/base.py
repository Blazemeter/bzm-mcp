"""
Simple utilities for BlazeMeter MCP tools.
"""
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from config.blazemeter import BZM_API_BASE_URL
from config.token import BzmToken

TOOLS_PREFIX = "blazemeter"

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

def get_date_time_iso(timestamp: int) -> Optional[str]:
    if timestamp is None:
        return None
    else:
        return datetime.fromtimestamp(timestamp).isoformat()
