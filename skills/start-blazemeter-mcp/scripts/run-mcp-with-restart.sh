#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="/Users/wguerrero/blazemeterMCP"
MCP_BIN="$WORKSPACE_ROOT/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp"
API_KEYS_FILE="$WORKSPACE_ROOT/api-key.json"
LOG_DIR="$WORKSPACE_ROOT/.github/skills/start-blazemeter-mcp/logs"
LOG_FILE="$LOG_DIR/mcp-watchdog.log"

# Restart policy (small backoff with cap)
INITIAL_BACKOFF=1
MAX_BACKOFF=10

mkdir -p "$LOG_DIR"

if [[ ! -x "$MCP_BIN" ]]; then
  echo "ERROR: MCP binary is not executable: $MCP_BIN" >&2
  exit 1
fi

if [[ ! -f "$API_KEYS_FILE" ]]; then
  echo "ERROR: API key file is missing: $API_KEYS_FILE" >&2
  exit 1
fi

export API_KEYS_FILE

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

echo "[$(timestamp)] Watchdog starting for BlazeMeter MCP (stdio mode)" | tee -a "$LOG_FILE"

backoff=$INITIAL_BACKOFF

while true; do
  echo "[$(timestamp)] Launching: $MCP_BIN --mcp" | tee -a "$LOG_FILE"
  "$MCP_BIN" --mcp >>"$LOG_FILE" 2>&1 || true

  echo "[$(timestamp)] MCP exited; restarting in ${backoff}s" | tee -a "$LOG_FILE"
  sleep "$backoff"

  if (( backoff < MAX_BACKOFF )); then
    backoff=$((backoff * 2))
    if (( backoff > MAX_BACKOFF )); then
      backoff=$MAX_BACKOFF
    fi
  fi
done
