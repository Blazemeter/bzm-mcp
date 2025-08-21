
# BlazeMeter MCP Server

MCP server for BlazeMeter API integration. Provides authentication handling and API tools.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) package manager
- BlazeMeter API credentials

## Setup

### 1. **Clone and install dependencies:**
   ```bash
   git clone <repo>
   cd bzm-mcp
   uv sync
   ```

### 2. **Create API key file in BlazeMeter:**
   
   Should look like:
   ```json
   {
     "id": "your_api_key_id",
     "secret": "your_api_secret"
   }
   ```
   > `/path/to/your/api-key.json`

 ### 3.**Configure MCP client:**
   
   **3.1. Cursor**
   ```json
   {
     "mcpServers": {
       "Blazmeter MCP": {
         "command": "uv",
         "args": ["run", "/path/to/bzm-mcp/main.py"],
         "env": {
           "BLAZEMETER_API_KEY": "/path/to/your/api-key.json"
         }
       }
     }
   }
   ```
   > Location in MacOs: `~/.cursor/mcp.json`

   **3.2. Claude**
   ```json
   Configuration not defined
   ```
   > Location in MacOs: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

## Development

### Adding new tools
1. Create tool file in `tools/`
2. Use `api_request(token, method, endpoint)` for API calls
3. Register tool in `server.py`

Example:
```python
# tools/my_tool.py
from .base import api_request

def register(mcp, token):
    @mcp.tool(name="bzm_mcp_my_tool", description="My tool")
    async def bzm_mcp_my_tool():
        return await api_request(token, "GET", "/endpoint")
        # Above response must be manipulated for LLM better understanding
```

### Build binary
```bash
uv run build.py
```

## Debugging

### Cursor
```bash
# Find latest log folder
ls -la ~/Library/Application\ Support/Cursor/logs/

# Tail logs
tail -f ~/Library/Application\ Support/Cursor/logs/YYYYMMDDTHHMMSS/window1/exthost/anysphere.cursor-retrieval/MCP\ user-Blazmeter\ MCP.log
```

### Claude
```bash
tail -f ~/Library/Logs/Claude/mcp-server-Blazmeter\ MCP.log
```

## Authentication

The server handles two error scenarios:
- **No token**: Returns `{"error": "No API token. Set BLAZEMETER_API_KEY env var."}`
- **Invalid token**: Returns `{"error": "Invalid credentials"}` on 401/403

No additional error handling needed in tools - just use `api_request()`.
