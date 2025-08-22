from typing import Any, Dict, Optional
from config.token import BzmToken
from .base import api_request


def register(mcp, token: Optional[BzmToken]):
    """
    Registers the `bzm_mcp_retrieve_projects` tool on the given MCP server,
    using the provided BzmToken for authentication.
    """

    @mcp.tool(
        name="bzm_mcp_retrieve_projects",
        description="Fetch projects from BlazeMeter API for a specific workspace and account. Use this to get available projects for test creation and selection."
    )
    async def bzm_mcp_retrieve_projects(workspace_id: str, account_id: str) -> Dict[str, Any]:
        """
        Calls GET /projects with workspace and account parameters and returns the parsed JSON payload.
        This retrieves all projects in the specified workspace for user selection during test creation.
        
        Args:
            workspace_id: The ID of the workspace to retrieve projects from
            account_id: The ID of the account to retrieve projects from
        """
        return await api_request(token, "GET", f"/projects?workspaceId={workspace_id}&accountId={account_id}")
