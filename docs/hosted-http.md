# Hosted HTTP (streamable-http)

Operator and advanced client guide for running BlazeMeter MCP over HTTP. For the standard local install (binary, uvx, Docker stdio), see the [README](../README.md).

## Hosted endpoint (clients)

Production URL:

`https://mcp.blazemeter.com/mcp`

Configure the MCP client with that URL and your BlazeMeter API key as Bearer credentials (`id:secret` or base64 of `id:secret`):

```json
{
  "mcpServers": {
    "BlazeMeter MCP": {
      "url": "https://mcp.blazemeter.com/mcp",
      "headers": {
        "Authorization": "Bearer <apiKeyId>:<apiKeySecret>"
      }
    }
  }
}
```

For a locally run server, use `"url": "http://localhost:8000/mcp"` instead.

### Auth behavior

- Over HTTP, credentials are resolved **per request** from the `Authorization` header.
- Invalid or missing Bearer credentials return `401` before any tool runs.
- Well-formed but wrong API keys fail later inside BlazeMeter API calls (same as stdio).
- Stdio / local Docker transport uses `api-key.json` / env / Docker secrets instead of Bearer auth.

## Local / operator run

Transport resolution precedence: **CLI `--mcp` > `BZM_MCP_TRANSPORT` > stdio**.

```bash
# From source
uv run python main.py --mcp http
# or
BZM_MCP_TRANSPORT=http FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=8000 uv run python main.py --mcp

# Container image (:latest is stdio by default; pass hosted HTTP env vars)
docker run --rm -p 8000:8000 \
  -e BZM_MCP_TRANSPORT=http \
  -e FASTMCP_HOST=0.0.0.0 \
  -e FASTMCP_PORT=8000 \
  -e FASTMCP_STREAMABLE_HTTP_PATH=/mcp \
  -e BZM_STORAGE_STRATEGY=memory \
  ghcr.io/blazemeter/bzm-mcp:latest
```

### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BZM_MCP_TRANSPORT` | Logical transport: `stdio`, `http`, or `docker` | `stdio` |
| `FASTMCP_HOST` | Bind address (HTTP only) | `127.0.0.1` |
| `FASTMCP_PORT` | Listen port (HTTP only). Also accepts `PORT` (e.g. Cloud Run) | `8000` |
| `FASTMCP_STREAMABLE_HTTP_PATH` | HTTP path for the MCP endpoint | `/mcp` |
| `BZM_STORAGE_STRATEGY` | `memory` or `http` | `memory` |

On streamable-http, local file paths are always rejected regardless of `BZM_STORAGE_STRATEGY` (hosted fail-closed storage).

## Hosted MVP limitations

- In-memory / fail-closed storage: no local disk access on the shared hosted server.
- `upload_assets` and other local file lookup/upload paths are rejected. Use a local stdio or Docker MCP installation for those workflows, or wait for remote Storage (Phase 2).
