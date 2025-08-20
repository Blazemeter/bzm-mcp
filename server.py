from tools.retrieve_user import register as register_retrieve_user
from config.token import BzmToken
from typing import Optional

def register_tools(mcp, token: Optional[BzmToken]):
    """
    Register all available tools with the MCP server.
    
    Args:
        mcp: The MCP server instance
        token: Optional BlazeMeter token (can be None if not configured)
    """
    register_retrieve_user(mcp, token)
