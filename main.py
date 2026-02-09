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
import argparse
import json
import logging
import os
import sys
from typing import Literal, cast

from mcp.server.fastmcp import FastMCP

from config.token import BzmToken, BzmTokenError
from config.version import __version__, __executable__, __bundle__
from server import register_tools
from tools.utils import ConfirmMode, register_confirm_mode

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')

LOG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def init_logging(level_name: str) -> None:
    level = getattr(logging, level_name.upper(), logging.CRITICAL)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
        force=True,
    )


def get_token():
    global BLAZEMETER_API_KEY_FILE_PATH

    # Verify if running inside Docker container
    is_docker = os.getenv('MCP_DOCKER', 'false').lower() == 'true'
    token = None

    if sys.platform == "darwin" and __bundle__.endswith(".app"):
        local_api_key_file = os.path.join(os.path.dirname(__bundle__), "api-key.json")
    else:
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


def run(log_level: str = "CRITICAL", confirm_mode: ConfirmMode = ConfirmMode.DELETE):
    token = get_token()
    instructions = """
# BlazeMeter MCP Server
A comprehensive integration tool that provides AI assistants with full programmatic access to BlazeMeter's cloud-based performance testing platform. Enables automated management of complete load testing workflows from creation to execution and reporting. Transforms enterprise-grade testing capabilities into an AI-accessible service for intelligent automation of complex performance testing scenarios.

## General Rules

- **If you have the information needed to call a tool action with its arguments, do so.**
- **Read action always gets more information** about a particular item than the list action. List only displays minimal information.
- **Read the current user information at startup** to learn the username, default account, workspace and project, and other important information.
- **Links anchors**: Never invent or add anchors to links if they do not originally have them.

## Hierarchy and Dependencies

- **Always respect the hierarchy**: Account → Workspace → Project → Test → Execution. Validate each level before operating on the next.
- **Dependencies**:
    - **accounts**: It doesn't depend on anyone. In user you can access which is the default account, and in the list of accounts, you can see the accounts available to the user.
    - **workspaces**: Workspaces belong to a particular account.
    - **projects**: Projects belong to a particular workspace.
    - **tests**: Tests belong to a particular project.
    - **executions**: Executions belong to a particular test.

## Workspace and Project Context

- **Always identify and confirm workspace/project** before performing any actions that depend on them. Start with the default project (from user information) but always confirm with the user which workspace and project to use.
- **Be transparent**: Always inform the user about which workspace/project you're working with.

## User Confirmation Required

- **ALWAYS ask for explicit user confirmation** before performing any action that creates, modifies, or alters anything in the user's BlazeMeter configurations, accounts, workspaces, projects or tests.
- **Actions requiring confirmation**: Creating tests, configuring load/locations, uploading assets, starting executions, or any other write/modify operations.
- **How to request**: Clearly state what action you're about to perform and on which workspace/project. Wait for user approval before proceeding.

## Proactive Knowledge Consultation

- **ALWAYS consult BlazeMeter Skills and Help tools first** before answering questions, configuring tests, interpreting results, troubleshooting, or providing recommendations.
- **Use `blazemeter_skills`**: Access specialized knowledge about performance testing, best practices, troubleshooting, and official guides.
- **Use `blazemeter_help`**: Consult documentation, help categories, and specific guides.
- **Golden rule**: If you're not 100% certain about something related to BlazeMeter, consult Skills or Help first, and if you can't find it and need to search online, always prioritize the domain site blazemeter.com .

## Capability Discovery

- **Explore available tools** to understand their full capabilities and parameters. Don't assume limitations.
- **Discover what's possible**: Consult tool descriptions and parameters to discover supported formats, options, and features.
- **Adapt to new capabilities**: Tools may have new capabilities; explore and use them.

## Important Guidelines
- **Batch Operations**: When making multiple calls to the same tool, check if that tool supports a `batch` action and use it instead of separate calls.
- **Don't assume**: If you don't know a parameter, capability, or best practice, consult available tools (especially Skills or Help).
- **Don't invent**: If something is unclear, consult Skills/Help before responding.
- **Provides resources**: Always include markdown-formatted links to authoritative websites or BlazeMeter help documentation for further learning.
- **Never modify without confirmation**: Always ask before creating, modifying, or altering anything in BlazeMeter.
- **Always confirm context**: Always identify and confirm workspace/project before operations.
- **Proactive Troubleshooting**: Use the skills for troubleshooting any detected issues.
    """
    mcp = FastMCP("blazemeter-mcp", instructions=instructions, log_level=cast(LOG_LEVELS, log_level))
    register_confirm_mode(confirm_mode)
    register_tools(mcp, token)
    mcp.run(transport="stdio")


def main():
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

    parser.add_argument(
        "--confirm",
        type=ConfirmMode,
        choices=list(ConfirmMode),
        default=ConfirmMode.DELETE,
        help=(
            "Confirmation mode:\n"
            "  DELETE  - Confirm delete operations only (default)\n"
            "  CUD     - Confirm create, update and delete operations\n"
            "  DISABLE - Disable confirmation"
        )
    )

    args = parser.parse_args()

    if args.mcp:
        init_logging(args.log_level)
        run(log_level=args.log_level.upper(), confirm_mode=args.confirm)
    else:

        logo_ascii = (
            "  ____  _                __  __      _            \n"
            " | __ )| | __ _ _______ |  \/  | ___| |_ ___ _ __ \n"
            " |  _ \| |/ _` |_  / _ \| .  . |/ _ \ __/ _ \ '__|\n"
            " | |_) | | (_| |/ /  __/| |\/| |  __/ ||  __/ |   \n"
            " |____/|_|\__,_/___\___||_|  |_|\___|\__\___|_|   \n"
            "                                                    \n"
            f" BlazeMeter MCP Server v{__version__} \n"
            " Copyright © 2025, Perforce Software, Inc. All rights reserved.\n"
            " Licensed under the Apache License, Version 2.0.\n"
        )
        print(logo_ascii)
        if sys.platform == "darwin" and __bundle__.endswith(".app"):
            command_path = os.path.join(__bundle__, "Contents", "MacOS", "bzm-mcp")
        else:
            command_path = __executable__
        config_dict = {
            "BlazeMeter MCP": {
                "command": command_path,
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


if __name__ == "__main__":
    main()
