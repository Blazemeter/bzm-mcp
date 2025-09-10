import os

from mcp.server.fastmcp import FastMCP

from config.token import BzmToken, BzmTokenError
from server import register_tools

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')


def run():
    token = None

    if BLAZEMETER_API_KEY_FILE_PATH:
        try:
            token = BzmToken.from_file(BLAZEMETER_API_KEY_FILE_PATH)
        except BzmTokenError as e:
            # Token file exists but is invalid - this will be handled by individual tools
            pass
        except Exception as e:
            # Other errors (file not found, permissions, etc.) - also handled by tools
            pass

    instructions = """
    # BlazeMeter MCP Server
    A comprehensive integration tool that provides AI assistants with full programmatic access to BlazeMeter's 
    cloud-based performance testing platform.
    Enables automated management of complete load testing workflows from creation to execution and reporting.
    Transforms enterprise-grade testing capabilities into an AI-accessible service for intelligent automation 
    of complex performance testing scenarios.
    
    General rules:
        - If you have the information needed to call a tool action with its arguments, do so.
        - Read action always get more information about a particular item than the list action, list only display minimal information.
        - Read the current user information at startup to learn the username, default account, workspace and project, and other important information.
        - Dependencies:
            accounts: It doesn't depend on anyone. In user you can access which is the default account, and in the list of accounts, you can see the accounts available to the user.
            workspaces: Workspaces belong to a particular account.
            projects: Projects belong to a particular workspace.
            tests: Tests belong to a particular project.
            executions: Executions belong to a particular test.
    """
    mcp = FastMCP("blazemeter-mcp", instructions=instructions)
    register_tools(mcp, token)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
