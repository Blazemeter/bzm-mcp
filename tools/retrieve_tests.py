from typing import Any, Dict, Optional
from config.token import BzmToken
from .base import api_request


def register(mcp, token: Optional[BzmToken]):
    """
    Registers test selection and retrieval tools on the given MCP server.
    """

    @mcp.tool(
        name="bzm_mcp_get_retrieve_all_tests",
        description="Get all tests in a specific project as project_id, workspace as workspace_id and account as account_id formatted for easy selection during test updates. Use this when a user needs to select a test for updating."
    )
    async def bzm_mcp_get_retrieve_all_tests(project_id: id, workspace_id: id, account_id: id) -> Dict[str, Any]:
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
            "total_tests": len(formatted_tests)
        }

