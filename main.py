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
import base64
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Literal, cast

from mcp.server.fastmcp import FastMCP

from config.token import BzmToken, BzmTokenError
from config.version import __version__, __executable__, __bundle__
from server import register_tools
from tools.utils import ConfirmMode, register_confirm_mode

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')

LOG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Canonical server label for printed JSON and clients that accept arbitrary string ids.
MCP_SERVER_DISPLAY_NAME = "BlazeMeter MCP"

# Claude Code: `add-json` defaults to local (current project); use user scope for all projects.
CLAUDE_CODE_MCP_INSTALL_SCOPE = "user"

# URLs for adding this MCP server in each client (install redirects or docs)
CURSOR_INSTALL_BASE = "cursor://anysphere.cursor-deeplink/mcp/install"
VSCODE_INSTALL_BASE = "https://insiders.vscode.dev/redirect/mcp/install"


def _mcp_server_name_for_cursor_and_vscode(canonical_name: str) -> str:
    """
    Cursor / VS Code: the `name` query parameter and JSON `mcpServers` keys are
    arbitrary strings (URL-encoded or JSON-quoted). No published character
    restriction on the server id; Cursor applies a separate ~60-character limit
    to MCP *tool* names, not to the server configuration key.
    """
    label = canonical_name.strip()
    return label or MCP_SERVER_DISPLAY_NAME


def _mcp_server_name_for_claude_code(canonical_name: str) -> str:
    """
    Claude Code: `claude mcp add-json` rejects names outside [A-Za-z0-9_-]
    (spaces and most punctuation are invalid). Official examples use ids like
    `my-server` and `weather-api`.
    """
    s = re.sub(r"\s+", "_", canonical_name.strip())
    s = re.sub(r"[^A-Za-z0-9_-]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "BlazeMeter_MCP"


def _cursor_install_url(server_config: dict, canonical_name: str = MCP_SERVER_DISPLAY_NAME) -> str:
    """Build a Cursor one-click install URL from a server config (command, args, env)."""
    name = _mcp_server_name_for_cursor_and_vscode(canonical_name)
    raw = json.dumps(server_config, separators=(",", ":"))
    b64 = base64.b64encode(raw.encode()).decode()
    return (
        f"{CURSOR_INSTALL_BASE}"
        f"?name={urllib.parse.quote(name)}"
        f"&config={urllib.parse.quote(b64, safe='')}"
    )


def _vscode_install_url(server_config: dict, canonical_name: str = MCP_SERVER_DISPLAY_NAME) -> str:
    """Build a VS Code one-click install URL; config is URL-encoded JSON (not base64)."""
    name = _mcp_server_name_for_cursor_and_vscode(canonical_name)
    raw = json.dumps(server_config, separators=(",", ":"))
    config_param = urllib.parse.quote(raw, safe="")
    return f"{VSCODE_INSTALL_BASE}?name={urllib.parse.quote(name)}&config={config_param}"


def _hyperlink(url: str, label: str) -> str:
    """
    Return an OSC 8 hyperlink for terminals that support it (e.g. Cursor, iTerm2).

    Kept for a possible future CLI path that prints clickable links; the install
    wizard uses URL handlers or Claude Code instead.
    """
    return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"


def _open_win_url_silent(url):
    escape_url = url.replace("%", "%%")
    bat_content = f"@echo off\nexplorer \"{escape_url}\" >nul 2>&1"
    bat_path = os.path.join(tempfile.gettempdir(), "silent_open.bat")

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    subprocess.Popen(
        [bat_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def _open_url_in_default_browser(url: str) -> bool:
    """
    Open a URL with the OS default handler (browser), same pattern as desktop
    file/URL associations: Windows explorer, macOS open, Linux xdg-open.

    Returns False on failure; callers should print the install address for manual use.
    """
    try:
        argument = url
        if sys.platform.startswith("win"):
            _open_win_url_silent(url)
            return True
        elif sys.platform.startswith("darwin"):
            open_command = "open"
        else:
            open_command = "xdg-open"
        subprocess.run(
            [open_command, argument],
            check=True,
            timeout=60,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return False


def _prompt_input(prompt: str) -> str:
    """Blank line before and after each interactive input for clearer console layout."""
    print()
    try:
        value = input(prompt)
    except EOFError:
        print()
        raise
    print()
    return value


def _claude_code_user_config_path() -> str:
    """
    Absolute path to Claude Code's user-wide settings file where MCP servers
    installed with ``--scope user`` are stored. There is no CLI to change MCP
    entries; users edit this JSON file directly.
    """
    return str(Path.home() / ".claude.json")


def _claude_mcp_add_json_payload(server_entry: dict) -> dict:
    """
    JSON shape for `claude mcp add-json` (stdio). Cursor/VS Code accept bare
    {command, args, env}; Claude Code requires a ``type`` field set to ``stdio``.
    See: https://docs.claude.com/en/docs/claude-code/mcp#claude-mcp-add-json
    """
    payload: dict = {
        "type": "stdio",
        "command": server_entry["command"],
        "args": list(server_entry.get("args", [])),
    }
    if "env" in server_entry:
        payload["env"] = server_entry["env"]
    return payload


def _try_claude_mcp_add_json(
        server_entry: dict, canonical_name: str = MCP_SERVER_DISPLAY_NAME
) -> tuple[bool, str | None]:
    """
    Register this server via Claude Code (`claude mcp add-json --scope user`).

    Uses user scope so the server is stored in user-wide config (all projects),
    not only the current directory's local config.

    The CLI server id is derived from ``canonical_name`` via
    :func:`_mcp_server_name_for_claude_code`. The JSON payload includes the
    required ``type: "stdio"`` wrapper for local servers.

    Returns (True, None) on success, or (False, error_message) on failure.
    """
    install_name = _mcp_server_name_for_claude_code(canonical_name)
    json_str = json.dumps(_claude_mcp_add_json_payload(server_entry), separators=(",", ":"))
    try:
        subprocess.run(
            [
                "claude",
                "mcp",
                "add-json",
                "--scope",
                CLAUDE_CODE_MCP_INSTALL_SCOPE,
                install_name,
                json_str,
            ],
            check=True,
            timeout=120,
            capture_output=True,
            text=True,
        )
        return True, None
    except FileNotFoundError:
        return (
            False,
            "The `claude` command was not found. Install Claude Code and ensure it is on your PATH.",
        )
    except subprocess.TimeoutExpired:
        return False, "The `claude` command timed out."
    except subprocess.CalledProcessError as e:
        detail = (e.stderr or e.stdout or "").strip()
        if not detail:
            detail = str(e)
        return False, detail


def _prompt_install_wizard(server_entry: dict) -> None:
    """
    Interactive install flow: Y/N to proceed; any other response exits the program.
    If Y, numbered menu to pick a client. Cursor/VS Code use compact install URLs
    opened via the OS default handler; Claude Code uses `claude mcp add-json --scope user`.
    The user confirms with Enter before each install action. Choosing 1–3 runs
    once then exits the menu; 0 skips install.
    """
    print(
        " Do you want to install this MCP in a supported client "
        "(Cursor, Visual Studio Code, Claude Code)?"
    )
    try:
        choice = _prompt_input(" [Y/N]: ")
    except EOFError:
        sys.exit(0)
    key = choice.strip()[:1].upper()
    if key not in ("Y", "N"):
        sys.exit(0)
    if key == "N":
        return

    # "MCP-compatible editor" matches how VS Code / Cursor document MCP integration.
    print(" Select your MCP-compatible client:")
    print("   1 — Cursor")
    print("   2 — Visual Studio Code (VS Code)")
    print("   3 — Claude Code (CLI)")
    print("   0 — Done")

    while True:
        try:
            line = _prompt_input(" Choice [0-3]: ")
        except EOFError:
            break
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.isdigit():
            print(" Invalid choice. Enter 0, 1, 2, or 3.")
            continue
        n = int(stripped)
        if n == 0:
            break
        if n == 1:
            url = _cursor_install_url(server_entry)
            client_label = "Cursor"
        elif n == 2:
            url = _vscode_install_url(server_entry)
            client_label = "Visual Studio Code"
        elif n != 3:
            print(" Invalid choice. Enter 0, 1, 2, or 3.")
            continue

        if n in (1, 2):
            print(
                f" The next step will open {client_label} directly to install this MCP server."
            )
        else:
            print(
                " The next step runs Claude Code to register this MCP server in your "
                "user-wide config (`claude mcp add-json --scope user`, available in all projects), "
                "not only the current folder."
            )
        try:
            _prompt_input(" Press Enter to proceed with installation: ")
        except EOFError:
            break

        if n in (1, 2):
            if _open_url_in_default_browser(url):
                print(" Done")
            else:
                print(
                    " Could not start the default application for this install request.\n"
                    " Complete setup manually using this address:\n"
                    f" {url}"
                )
        else:
            ok, err_detail = _try_claude_mcp_add_json(server_entry)
            if ok:
                print(" Done")
                print(
                    " Claude Code has no CLI to adjust MCP server settings after install.\n"
                    " To configure this server (for example env vars or paths), edit your user config:\n"
                    f" {_claude_code_user_config_path()}"
                )
            else:
                json_str = json.dumps(
                    _claude_mcp_add_json_payload(server_entry), separators=(",", ":")
                )
                claude_name = _mcp_server_name_for_claude_code(MCP_SERVER_DISPLAY_NAME)
                print(
                    " Could not register the MCP server using Claude Code.\n"
                    f" {err_detail}\n\n"
                    " Retry manually with the server name and compact JSON below, e.g.:\n\n"
                    f'   claude mcp add-json --scope user "{claude_name}" \'<single-line-json>\'\n\n'
                    f"   Name: {claude_name}\n"
                    f"   JSON: {json_str}\n"
                )
        break


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
- **Actions requiring confirmation**: Creating tests, configuring load/locations/failure criteria, uploading assets, starting executions, or any other write/modify operations.
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
- **Failure criteria**: The same field names appear when you read a test and when you configure failure criteria (`failure_criteria` on the test); the server handles BlazeMeter’s REST format internally. Use `failure_criteria_meta` for field definitions and KPI/condition catalogs. When describing criteria to the user, use `meta.general_labels`, `meta.rule_field_labels`, `meta.kpi_labels`, and `meta.condition_labels`; use raw metric and operator ids only inside tool calls. Use `configure_failure_criteria` only after user confirmation; it replaces all rules unless you merge from a prior read.
    """
    mcp = FastMCP("blazemeter-mcp", instructions=instructions, log_level=cast(LOG_LEVELS, log_level))
    register_confirm_mode(confirm_mode)
    register_tools(mcp, token)
    mcp.run(transport="stdio")


def main():
    parser = argparse.ArgumentParser(
        prog="bzm-mcp",
        formatter_class=argparse.RawTextHelpFormatter,
    )

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
        type=lambda s: s.strip().upper(),
        choices=tuple(ConfirmMode.__members__),
        default=ConfirmMode.DELETE.name,
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
        run(log_level=args.log_level.upper(), confirm_mode=ConfirmMode[args.confirm])
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
        server_entry = {
            "command": command_path,
            "args": ["--mcp"],
        }
        if BLAZEMETER_API_KEY_FILE_PATH:
            server_entry["env"] = {"BLAZEMETER_API_KEY": BLAZEMETER_API_KEY_FILE_PATH}
        config_dict = {MCP_SERVER_DISPLAY_NAME: server_entry}

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
        _prompt_install_wizard(server_entry)
        print(" ")
        print(" There are configuration alternatives, if you want to know more:")
        print(" https://github.com/Blazemeter/bzm-mcp/")
        _prompt_input("Press Enter to exit...")


if __name__ == "__main__":
    main()
