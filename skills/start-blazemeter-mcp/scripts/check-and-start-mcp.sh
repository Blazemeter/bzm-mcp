#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="/Users/wguerrero/blazemeterMCP"
VSCODE_MCP_JSON="$WORKSPACE_ROOT/.vscode/mcp.json"
ROOT_MCP_JSON="$WORKSPACE_ROOT/mcp.json"
MCP_BIN="$WORKSPACE_ROOT/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp"
MCP_ARGS=("--mcp")
API_KEYS_FILE="$WORKSPACE_ROOT/api-key.json"

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "ERROR: Missing file: $path" >&2
    exit 1
  fi
}

require_executable() {
  local path="$1"
  if [[ ! -x "$path" ]]; then
    echo "ERROR: Missing executable or no execute permission: $path" >&2
    exit 1
  fi
}

validate_json() {
  local path="$1"
  if command -v jq >/dev/null 2>&1; then
    jq . "$path" >/dev/null
  else
    # Fallback parser if jq is not available on the host.
    python3 -m json.tool "$path" >/dev/null
  fi
}

print_mcp_processes() {
  pgrep -fl "$MCP_BIN" || true
}

require_file "$VSCODE_MCP_JSON"
require_file "$ROOT_MCP_JSON"
require_file "$API_KEYS_FILE"
require_executable "$MCP_BIN"

validate_json "$VSCODE_MCP_JSON"
validate_json "$ROOT_MCP_JSON"

if pgrep -f "$MCP_BIN" >/dev/null 2>&1; then
  echo "✓ BlazeMeter MCP already running in stdio mode"
  print_mcp_processes
  exit 0
fi

echo "Starting BlazeMeter MCP (stdio mode)..."

export API_KEYS_FILE="$API_KEYS_FILE"

"$MCP_BIN" "${MCP_ARGS[@]}" >/dev/null 2>&1 &
disown || true

sleep 3

if pgrep -f "$MCP_BIN" >/dev/null 2>&1; then
  echo "✓ BlazeMeter MCP started successfully (stdio mode)"
  print_mcp_processes
  exit 0
fi

echo "ERROR: BlazeMeter MCP did not start." >&2
exit 1
