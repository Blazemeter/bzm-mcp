from typing import Any, Dict, Optional
from config.token import BzmToken
from .base import api_request


def register(mcp, token: Optional[BzmToken]):
    """
    Registers the `bzm_mcp_retrieve_user` tool on the given MCP server,
    using the provided BzmToken for authentication.
    """

    @mcp.tool(
        name="bzm_mcp_retrieve_user",
        description="Fetch current user information from BlazeMeter API"
    )
    async def bzm_mcp_retrieve_user() -> Dict[str, Any]:
        """
        Calls GET /user and returns the parsed JSON payload.
        """
        return await api_request(token, "GET", "/user")

