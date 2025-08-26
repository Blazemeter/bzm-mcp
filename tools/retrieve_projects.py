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
    async def bzm_mcp_retrieve_projects(workspace_id: int, account_id: int) -> Dict[str, Any]:
        """
        Calls GET /projects with workspace as workspace_id and account as account_id parameters and returns the parsed JSON payload.
        This retrieves all projects in the specified workspace for user selection during test creation.
        
        Args:
            workspace_id: The ID of the workspace to retrieve projects from
            account_id: The ID of the account to retrieve projects from
        """
        return await api_request(token, "GET", f"/projects?workspaceId={workspace_id}&accountId={account_id}")
    
    @mcp.tool(
        name="bzm_mcp_get_available_projects_for_test_creation",
        description="Get all projects in a specific workspace as workspace_id and account as account_id formatted for easy selection during test creation. Use this when a user needs to select a project for test allocation."
    )
    async def bzm_mcp_get_available_projects_for_test_creation(workspace_id: int, account_id: int) -> Dict[str, Any]:
        projects_response = await api_request(token, "GET", f"/projects?workspaceId={workspace_id}&accountId={account_id}")
        
        if "error" in projects_response:
            return projects_response
        
     
        projects = projects_response.get("result", [])
        
        formatted_projects = []
        for project in projects:
            formatted_project = {
                "id": project.get("id"),
                "name": project.get("name", "Unknown"),
                "description": project.get("description", ""),
                "created": project.get("created"),
                "updated": project.get("updated"),
                "workspaceId": project.get("workspaceId"),
                "testsCount": project.get("testsCount", 0)
            }
            formatted_projects.append(formatted_project)
        
        return {
            "account_id": account_id,
            "workspace_id": workspace_id,
            "projects": formatted_projects,
            "total_projects": len(formatted_projects),
        }
