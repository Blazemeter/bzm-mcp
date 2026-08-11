# Hosted MCP — app storage contract

Ops deploy (Cloud Run, DNS, CI) lives in
[`hosted-bzm-mcp`](https://github.com/Blazemeter/hosted-bzm-mcp)
(`docs/hosted-mvp-runbook.md`). This file documents only what the **bzm-mcp**
process needs for Storage-backed sessions.

## Runtime wiring

| Mode | Transport | Session store | File access |
|------|-----------|---------------|-------------|
| Stdio / local Docker | `stdio` | `MemoryStorageProvider` | local disk |
| Hosted HTTP | `streamable-http` | `HTTPStorageClient` | fail-closed |

Composition root: `build_runtime` → `AppRuntime.storage` →
`configure_dataframe_storage(runtime.storage)` in `server.register_tools`.

## Ports (`config/storage.py`)

- `FileStoragePort` — path map / read for `upload_assets`
- `SessionStoragePort` — partition get/put/delete + `put_dataframes`
- `StoragePort` — combined (what `AppRuntime` holds)
- `MemoryStorageProvider` / `HTTPStorageClient` — implementations

## Session Storage Service

Env: `BZM_STORAGE_SERVICE_URL` (required for HTTP session ops).

| Method | Path |
|--------|------|
| `GET` / `PUT` / `DELETE` | `/internal/v1/sessions/{user_id}/{mcp_session_id}` |

Partition body: `metadata`, `dataframes`, `tasks` (objects); `uploaded_files`
(list of `{file_id, name?, content_type?, size_bytes?, metadata?}`).

MCP workers keep Polars/SQL in-process; only the partition document is remote.
`put_dataframes` updates the dataframes map without clearing tasks/metadata.

## Related env (hosted)

| Variable | Typical value |
|----------|----------------|
| `BZM_MCP_TRANSPORT` | `http` |
| `FASTMCP_HOST` | `0.0.0.0` |
| `FASTMCP_PORT` / `PORT` | `8000` |
| `FASTMCP_STREAMABLE_HTTP_PATH` | `/mcp` |
| `BZM_STORAGE_BACKEND` | `http` when using Storage Service |
| `BZM_STORAGE_SERVICE_URL` | Storage API base URL |

Do not set `MCP_DOCKER=true` on hosted (stdio Docker volume mounts only).
