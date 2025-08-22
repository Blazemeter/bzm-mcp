from typing import Any, Dict, Optional
from config.token import BzmToken
from .base import api_request


def register(mcp, token: Optional[BzmToken]):
    """
    Registers project selection tools on the given MCP server.
    """

    @mcp.tool(
        name="bzm_mcp_get_available_projects_for_test_creation",
        description="Get all projects in a specific workspace formatted for easy selection during test creation. Use this when a user needs to select a project for test allocation. This tool provides a user-friendly list of projects with clear selection instructions."
    )
    async def bzm_mcp_get_available_projects_for_test_creation(workspace_id: str, account_id: str) -> Dict[str, Any]:
        """
        Retrieves all projects in the specified workspace and formats them for easy project selection during test creation.
        Returns a structured response with project details for user selection.
        
        Args:
            workspace_id: The ID of the workspace to retrieve projects from
            account_id: The ID of the account to retrieve projects from
        """
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
            "selection_instructions": f"Found {len(formatted_projects)} project(s) in workspace {workspace_id}. To select a project for test creation, use the project ID from the list above.",
            "usage_context": "Use this data when a user wants to create a test and needs to select which project to allocate it to."
        }

    @mcp.tool(
        name="bzm_mcp_select_project_for_test",
        description="Select a specific project for test creation by providing the project ID. Use this after retrieving available projects to confirm the user's project selection for test allocation."
    )
    async def bzm_mcp_select_project_for_test(project_id: str, workspace_id: str, account_id: str) -> Dict[str, Any]:
        """
        Validates and confirms a project selection for test creation.
        
        Args:
            project_id: The ID of the project selected for test creation
            workspace_id: The ID of the workspace containing the project
            account_id: The ID of the account containing the workspace
        """
        projects_response = await api_request(token, "GET", f"/projects?workspaceId={workspace_id}&accountId={account_id}")
        
        if "error" in projects_response:
            return projects_response
        
        projects = projects_response.get("result", [])
        
        selected_project = None
        for project in projects:
            if str(project.get("id")) == str(project_id):
                selected_project = project
                break
        
        if not selected_project:
            return {
                "error": f"Project with ID {project_id} not found in workspace {workspace_id}",
                "available_project_ids": [str(p.get("id")) for p in projects]
            }
        
        return {
            "selected_project": {
                "id": selected_project.get("id"),
                "name": selected_project.get("name"),
                "description": selected_project.get("description"),
                "workspaceId": selected_project.get("workspaceId"),
                "testsCount": selected_project.get("testsCount", 0)
            },
            "confirmation": f"Project '{selected_project.get('name')}' (ID: {project_id}) has been selected for test creation.",
            "next_steps": "You can now proceed with creating your test in this project."
        }
