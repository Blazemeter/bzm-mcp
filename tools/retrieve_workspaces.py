from typing import Any, Dict, Optional
from config.token import BzmToken
from .base import api_request


def register(mcp, token: Optional[BzmToken]):
    """
    Registers the `bzm_mcp_retrieve_workspaces` tool on the given MCP server,
    using the provided BzmToken for authentication.
    """

    @mcp.tool(
        name="bzm_mcp_retrieve_workspaces",
        description="Fetch current user workspaces from BlazeMeter API. Requires an account_id to specify the account."
    )
    async def bzm_mcp_retrieve_workspaces(account_id: int) -> Dict[str, Any]:
        """
        Calls GET /workspace and returns the parsed JSON payload.
        """
        return await api_request(token, "GET", "/workspaces", params={"accountId": account_id})

