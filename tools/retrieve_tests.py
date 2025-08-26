from typing import Any, Dict, Optional
from config.token import BzmToken
from .base import api_request


def register(mcp, token: Optional[BzmToken]):
    """
    Registers test selection and retrieval tools on the given MCP server.
    """

    @mcp.tool(
        name="bzm_mcp_retrieve_tests_by_project",
        description="Fetch all tests for a specific project from BlazeMeter API. Use this to get tests filtered by project."
    )
    async def bzm_mcp_retrieve_tests_by_project(project_id: str, workspace_id: str, account_id: str) -> Dict[str, Any]:
        """
        Calls GET /tests with project filter and returns the parsed JSON payload.
        
        Args:
            project_id: The ID of the project to retrieve tests from
            workspace_id: The ID of the workspace containing the project
            account_id: The ID of the account containing the workspace
        """
        return await api_request(token, "GET", f"/tests?projectId={project_id}&workspaceId={workspace_id}&accountId={account_id}")

    @mcp.tool(
        name="bzm_mcp_get_available_tests_for_project",
        description="Get all tests in a specific project formatted for easy selection during test updates. Use this when a user needs to select a test for updating. This tool provides a user-friendly list of tests with clear selection instructions."
    )
    async def bzm_mcp_get_available_tests_for_project(project_id: str, workspace_id: str, account_id: str) -> Dict[str, Any]:
        """
        Retrieves all tests in the specified project and formats them for easy test selection during updates.
        Returns a structured response with test details for user selection.
        
        Args:
            project_id: The ID of the project to retrieve tests from
            workspace_id: The ID of the workspace containing the project
            account_id: The ID of the account containing the workspace
        """
        tests_response = await api_request(token, "GET", f"/tests?projectId={project_id}&workspaceId={workspace_id}&accountId={account_id}")
        
        if "error" in tests_response:
            return tests_response
        
        tests = tests_response.get("result", [])
        
        formatted_tests = []
        for test in tests:
            formatted_test = {
                "id": test.get("id"),
                "name": test.get("name", "Unknown"),
                "description": test.get("description", ""),
                "created": test.get("created"),
                "updated": test.get("updated"),
                "projectId": test.get("projectId"),
                "status": test.get("status", "Unknown"),
                "type": test.get("type", "Unknown"),
                "configuration": test.get("configuration", {})
            }
            formatted_tests.append(formatted_test)
        
        return {
            "account_id": account_id,
            "workspace_id": workspace_id,
            "project_id": project_id,
            "tests": formatted_tests,
            "total_tests": len(formatted_tests),
            "selection_instructions": f"Found {len(formatted_tests)} test(s) in project {project_id}. To select a test for updating, use the test ID from the list above.",
            "usage_context": "Use this data when a user wants to update a test and needs to select which test to modify."
        }

    @mcp.tool(
        name="bzm_mcp_select_test_for_update",
        description="Select a specific test for updating by providing the test ID. Use this after retrieving available tests to confirm the user's test selection for updates."
    )
    async def bzm_mcp_select_test_for_update(test_id: str, project_id: str, workspace_id: str, account_id: str) -> Dict[str, Any]:
        """
        Validates and confirms a test selection for updating.
        
        Args:
            test_id: The ID of the test selected for updating
            project_id: The ID of the project containing the test
            workspace_id: The ID of the workspace containing the project
            account_id: The ID of the account containing the workspace
        """
        tests_response = await api_request(token, "GET", f"/tests?projectId={project_id}&workspaceId={workspace_id}&accountId={account_id}")
        
        if "error" in tests_response:
            return tests_response
        
        tests = tests_response.get("result", [])
        
        selected_test = None
        for test in tests:
            if str(test.get("id")) == str(test_id):
                selected_test = test
                break
        
        if not selected_test:
            return {
                "error": f"Test with ID {test_id} not found in project {project_id}",
                "available_test_ids": [str(t.get("id")) for t in tests]
            }
        
        return {
            "selected_test": {
                "id": selected_test.get("id"),
                "name": selected_test.get("name"),
                "description": selected_test.get("description"),
                "projectId": selected_test.get("projectId"),
                "status": selected_test.get("status"),
                "type": selected_test.get("type"),
                "configuration": selected_test.get("configuration", {})
            },
            "confirmation": f"Test '{selected_test.get('name')}' (ID: {test_id}) has been selected for updating.",
            "next_steps": "You can now proceed with updating this test."
        }
