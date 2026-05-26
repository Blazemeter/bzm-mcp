#!/bin/bash
set -e

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN="$BIN_DIR/bzm-mcp"

if [ -t 1 ]; then
  exec "$BIN" "$@"
else
  open -a Terminal "$BIN"
fi
