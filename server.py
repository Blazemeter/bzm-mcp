"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Optional

from config.token import BzmToken
from tools.account_manager import register as register_account_manager
from tools.billing_manager import register as register_billing_manager
from tools.execution_manager import register as register_execution_manager
from tools.help_manager import register as register_help_manager
from tools.project_manager import register as register_project_manager
from tools.skills_manager import register as register_skills_manager
from tools.test_manager import register as register_test_manager
from tools.user_manager import register as register_user_manager
from tools.workspace_manager import register as register_workspace_manager


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
    register_execution_manager(mcp, token)
    register_account_manager(mcp, token)
    register_billing_manager(mcp, token)
    register_help_manager(mcp, token)
    register_skills_manager(mcp, token)
