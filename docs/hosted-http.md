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
        "Authorization": "Bearer <apiKeyId>:<apiKeySecret>",
        "confirmation-mode": "DELETE"
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

### Confirmation mode header

- Optional header: `confirmation-mode`
- Allowed values: `DELETE`, `CUD`, `DISABLE`
- If omitted, empty, or invalid, the session falls back to `DELETE`.

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
  -e BZM_STORAGE_API_BASE_URL=https://mcp-storage.internal \
  -e BZM_MCP_TICKET_STORAGE_CALLER_TOKEN=dev-mcp-caller \
  -e BZM_MCP_UPLOAD_PUBLIC_BASE_URL=http://127.0.0.1:8090 \
  ghcr.io/blazemeter/bzm-mcp:latest
```

### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BZM_MCP_TRANSPORT` | Logical transport: `stdio`, `http`, or `docker` | `stdio` |
| `FASTMCP_HOST` | Bind address (HTTP only) | `127.0.0.1` |
| `FASTMCP_PORT` | Listen port (HTTP only). Also accepts `PORT` | `8000` |
| `FASTMCP_STREAMABLE_HTTP_PATH` | HTTP path for the MCP endpoint | `/mcp` |
| `BZM_STORAGE_API_BASE_URL` | Storage Service base URL (required for streamable-http). Session partitions and upload-ticket mint use this origin. | — |
| `BZM_MCP_TICKET_STORAGE_CALLER_TOKEN` | Bearer token MCP uses when calling storage-api mint/credential endpoints. Must match storage-api `BZM_STORAGE_MCP_CALLER_TOKEN`. Required for streamable-http. | — |
| `BZM_MCP_UPLOAD_PUBLIC_BASE_URL` | Public origin returned in mint results (`{base}/services/uploads/{id}`). Required for streamable-http. Production is `https://mcp.blazemeter.com`. | — |
| `BZM_MCP_TICKET_STORAGE_TIMEOUT_SECONDS` | Timeout for storage-api mint and credential writes | `2` |
| `BZM_CACHE_ENABLED` | Method cache on/off (both transports) | `true` |
| `BZM_CACHE_HTTP_TIMEOUT_SECONDS` | Timeout for storage-api cache calls (streamable-http) | `2` |
| `BZM_CACHE_HTTP_MAX_VALUE_BYTES` | Largest encoded value sent to the storage-api cache; larger values are not cached (not even sent). Keep in line with storage-api `BZM_STORAGE_CACHE_MAX_VALUE_BYTES` | `1048576` |
| `BZM_MCP_STORAGE_CALLER_TOKEN` | MCP caller token for the storage-api (tickets and cache); falls back to `BZM_MCP_TICKET_STORAGE_CALLER_TOKEN` | — |
| `BZM_CACHE_MAX_ENTRIES` / `BZM_CACHE_SWEEP_INTERVAL_SECONDS` / `BZM_CACHE_SWEEP_BATCH_SIZE` | In-memory cache tuning (stdio) | `2048` / `30` / `500` |

On streamable-http, session partitions use `HttpSessionStorageProvider`. There is no disk adapter (`file_access` is `None`). Upload is `TicketPort` mint, not a file read.

The method cache (`@ttl_cache_method`, help pages) is in-memory on stdio and lives only behind the storage-api `/cache/entries` API on streamable-http (`HttpCache`, same caller token as tickets): the two are independent and hosted keeps no in-process cache state. The help index (several MB in full) is cached as small pieces (categories, one entry per subcategory, child pages per category), each read on its own and each within the API size limit. Typed results round-trip through `config/cache_codec.py`; only pydantic models from `models.*` are rebuilt. A failed cache read is a miss and a failed write only skips caching: the cache never fails a tool call. What backs the API can change without touching the MCP.

## Hosted file upload

`blazemeter_tests` / `upload_assets` is the same action name as stdio, with a different schema on HTTP:

- Required args: `test_id`, `filename`, `declared_size`, `encoding`, `sha256`.
- MCP authorizes the test, writes the session credential, mints a one-shot URL, and returns immediately.
- MCP does not accept file bytes, paths, or `main_script` on HTTP. The client POSTs the raw file to the returned URL (`201` means the file landed).
- After real bytes the URL is spent; call `upload_assets` again. If the POST returns `503` after bytes were sent, list test files before retrying.

## Hosted MVP limitations

- Session dataframes/tasks live in the Storage Service keyed by `{user_id}/{mcp_session_id}`.
- HTTP `upload_assets` mints a URL; it does not read local disk or set the test main script. Use stdio/Docker MCP when you want MCP to upload paths and optionally PATCH the entrypoint.
