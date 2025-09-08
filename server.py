from tools.user_manager import register as register_user_manager
from tools.project_manager import register as register_project_manager
from tools.workspace_manager import register as register_workspace_manager
from tools.test_manager import register as register_test_manager
from tools.test_execution_manager import register as register_test_execution_manager
from tools.account_manager import register as register_account_manager
from config.token import BzmToken
from typing import Optional

def register_tools(mcp, token: Optional[BzmToken]):
    """
    Register all available tools with the MCP server.
    
    Args:
        mcp: The MCP server instance
        token: Optional BlazeMeter token (can be None if not configured)
    """
    register_user_manager(mcp, token)
    register_project_manager(mcp, token)
    register_workspace_manager(mcp, token)
    register_test_manager(mcp, token)
    register_test_execution_manager(mcp, token)
    register_account_manager(mcp, token)
