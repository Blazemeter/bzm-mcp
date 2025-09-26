import argparse
import json
import logging
import os
import sys
from typing import Literal, cast

from mcp.server.fastmcp import FastMCP

from config.token import BzmToken, BzmTokenError
from config.version import __version__, __executable__
from server import register_tools

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')

LOG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def init_logging(level_name: str) -> None:
    level = getattr(logging, level_name.upper(), logging.CRITICAL)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
        force=True,
    )


def get_token():
    global BLAZEMETER_API_KEY_FILE_PATH

    # Verify if running inside Docker container
    is_docker = os.getenv('MCP_DOCKER', 'false').lower() == 'true'
    token = None

    local_api_key_file = os.path.join(os.path.dirname(__executable__), "api-key.json")
    if not BLAZEMETER_API_KEY_FILE_PATH and os.path.exists(local_api_key_file):
        BLAZEMETER_API_KEY_FILE_PATH = local_api_key_file

    if BLAZEMETER_API_KEY_FILE_PATH:
        try:
            token = BzmToken.from_file(BLAZEMETER_API_KEY_FILE_PATH)
        except BzmTokenError:
            # Token file exists but is invalid - this will be handled by individual tools
            pass
        except Exception:
            # Other errors (file not found, permissions, etc.) - also handled by tools
            pass
    elif is_docker:
        token = BzmToken(os.getenv('API_KEY_ID'), os.getenv('API_KEY_SECRET'))
    return token


def run(log_level: str = "CRITICAL"):
    token = get_token()
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
    mcp = FastMCP("blazemeter-mcp", instructions=instructions, log_level=cast(LOG_LEVELS, log_level))
    register_tools(mcp, token)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="bzm-mcp")

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--mcp",
        action="store_true",
        help="Execute MCP Server"
    )

    parser.add_argument(
        "--log-level",
        default="CRITICAL",  # By default, only critical errors
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: CRITICAL = critical errors only)"
    )

    args = parser.parse_args()
    init_logging(args.log_level)

    if args.mcp:
        run(log_level=args.log_level.upper())
    else:

        logo_ascii = (
            "  ____  _                __  __      _            \n"
            " | __ )| | __ _ _______ |  \/  | ___| |_ ___ _ __ \n"
            " |  _ \| |/ _` |_  / _ \| .  . |/ _ \ __/ _ \ '__|\n"
            " | |_) | | (_| |/ /  __/| |\/| |  __/ ||  __/ |   \n"
            " |____/|_|\__,_/___\___||_|  |_|\___|\__\___|_|   \n"
            "                                                    \n"
            f" BlazeMeter MCP Server v{__version__} \n"
        )
        print(logo_ascii)

        config_dict = {
            "BlazeMeter MCP": {
                "command": f"{__executable__}",
                "args": ["--mcp"],
            }
        }

        print(" MCP Server Configuration:\n")
        print(" In your tool with MCP server support, locate the MCP server configuration file")
        print(" and add the following server to the server list.\n")

        json_str = json.dumps(config_dict, ensure_ascii=False, indent=4)
        print("\n".join(json_str.split("\n")[1:-1]) + "\n")

        if not get_token():
            print(" [X] BlazeMeter API Key not configured.")
            print(" ")
            print(" Copy the BlazeMeter API Key file (api-key.json) to the same location of this executable.")
            print(" ")
            print(" How to obtain the api-key.json file:")
            print(" https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html")
        else:
            print(" [OK] BlazeMeter API Key configured correctly.")
        print(" ")
        print(" There are configuration alternatives, if you want to know more:")
        print(" https://github.com/Blazemeter/bzm-mcp/")
        print(" ")
        input("Press Enter to exit...")
