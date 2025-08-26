from .base import api_request
from typing import Optional, Dict, Any
from config.token import BzmToken

ACCOUNTS_ENDPOINT = "/accounts"

def register(mcp, token: Optional[BzmToken]) -> None:
    """Register the retrieve account tool with the MCP server."""
    
    @mcp.tool(
        name="bzm_mcp_retrieve_account", 
        description="Retrieve all accounts for the given user. Account is required for test creation.")
    async def bzm_mcp_retrieve_account() -> str:

        api_response = await api_request(token, "GET", ACCOUNTS_ENDPOINT)
        
        if "error" in api_response and api_response["error"]:
            return f"Error retrieving accounts: {api_response['error']}"
        
        accounts = api_response.get("result", [])
        
        if not accounts:
            return "No accounts found for the current user."
        
        minimized_accounts = "\n".join([
            f"{account['name']} ({account['id']})" 
            for account in accounts
        ])
        
        formatted_response = f"""
        Current user has the following accounts to choose from:
        {minimized_accounts}
        If you need to create a test, you need to choose an account.
        Account id is essential in order to store the test in the correct account.
        """
        
        return formatted_response