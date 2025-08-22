from tools.retrieve_user import register as register_retrieve_user
from tools.retrieve_projects import register as register_retrieve_projects
from tools.select_project import register as register_select_project
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
    register_retrieve_projects(mcp, token)
    register_select_project(mcp, token)
