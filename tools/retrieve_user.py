import httpx
from typing import Any, Dict
from config.token import BzmToken
from config.blazemeter import BZM_API_BASE_URL  


def register(mcp, token: BzmToken):
    """
    Registers the `retrieve_user` tool on the given MCP server,
    using the provided BzmToken for authentication.
    """

    @mcp.tool(
        name="retrieve_user",
        description="Fetch current user information from BlazeMeter API"
    )
    async def retrieve_user() -> Dict[str, Any]:
        """
        Calls GET /user and returns the parsed JSON payload.
        """
        headers = {
            "Authorization": token.as_basic_auth()
        }

        async with httpx.AsyncClient(base_url=BZM_API_BASE_URL) as client:
            resp = await client.get("/user", headers=headers)
            resp.raise_for_status()
            return resp.json()

