---
name: start-blazemeter-mcp
description: "Use when launching, validating, or troubleshooting the local BlazeMeter MCP server for this workspace. Uses direct stdio MCP binary startup with API_KEYS_FILE configured in MCP settings."
---

# Start BlazeMeter MCP (Local stdio Configuration)

## Use This Skill When

- You want to run BlazeMeter MCP in local stdio mode.
- You want MCP config to use `servers.BlazeMeter MCP` with `type: stdio`.
- You want `sv-server` disabled for now and may re-enable it later.
- You want startup scripts aligned to the local app-bundle binary and API keys file.

## Target Configuration

`.vscode/mcp.json` should include:

```json
"servers": {
  "BlazeMeter MCP": {
    "type": "stdio",
    "command": "/Users/wguerrero/bzm-vitals-mcp/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp",
    "args": ["--mcp"],
    "env": {
      "API_KEYS_FILE": "/Users/wguerrero/bzm-vitals-mcp/api-key.json"
    }
  }
}
```

`mcp.json` should match `.vscode/mcp.json` for `BlazeMeter MCP` and keep `sv-server` disabled/omitted.

## Workspace Assumptions

- Workspace root: /Users/wguerrero/bzm-vitals-mcp
- VS Code MCP config: /Users/wguerrero/bzm-vitals-mcp/.vscode/mcp.json
- Root MCP config: /Users/wguerrero/bzm-vitals-mcp/mcp.json
- MCP binary: /Users/wguerrero/bzm-vitals-mcp/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp
- API keys file: /Users/wguerrero/bzm-vitals-mcp/api-key.json
- Helper script: /Users/wguerrero/bzm-vitals-mcp/.github/skills/start-blazemeter-mcp/scripts/check-and-start-mcp.sh
- Watchdog script: /Users/wguerrero/bzm-vitals-mcp/.github/skills/start-blazemeter-mcp/scripts/run-mcp-with-restart.sh

## Preferred Commands

### Start once

```bash
bash /Users/wguerrero/bzm-vitals-mcp/.github/skills/start-blazemeter-mcp/scripts/check-and-start-mcp.sh
```

### Start with auto-restart

```bash
bash /Users/wguerrero/bzm-vitals-mcp/.github/skills/start-blazemeter-mcp/scripts/run-mcp-with-restart.sh
```

## Validation Checklist

1. Confirm both config files are valid JSON.
2. Confirm MCP binary exists and is executable.
3. Confirm API key file exists.
4. Confirm MCP process is running with `--mcp`.

## Troubleshooting

- If startup fails, verify executable permissions:

```bash
ls -l /Users/wguerrero/bzm-vitals-mcp/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp
```

- Validate JSON configs:

```bash
jq . /Users/wguerrero/bzm-vitals-mcp/.vscode/mcp.json
jq . /Users/wguerrero/bzm-vitals-mcp/mcp.json
```

- If API key loading fails, verify file exists and is readable:

```bash
ls -l /Users/wguerrero/bzm-vitals-mcp/api-key.json
```

- If `sv-server` is needed in the future, re-add it to `mcp.json` and then validate the target URL/port.
