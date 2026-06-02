#!/usr/bin/env bash
set -euo pipefail

MCP_BIN="/Users/wguerrero/blazemeterMCP/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp"

if ! pgrep -f "$MCP_BIN" >/dev/null 2>&1; then
  echo "BlazeMeter MCP server is not running."
  exit 0
fi

echo "Stopping BlazeMeter MCP server..."
pkill -f "$MCP_BIN" || true

# Wait up to 5 seconds for processes to exit
for i in $(seq 1 5); do
  if ! pgrep -f "$MCP_BIN" >/dev/null 2>&1; then
    echo "BlazeMeter MCP server stopped."
    exit 0
  fi
  sleep 1
done

# Force-kill if still running
echo "Server did not exit cleanly, force-killing..."
pkill -9 -f "$MCP_BIN" || true
echo "BlazeMeter MCP server force-stopped."
