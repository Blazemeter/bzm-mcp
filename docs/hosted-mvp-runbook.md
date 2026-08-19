# Hosted MCP — session storage + dataframes

Ops deploy (Cloud Run, DNS, CI) lives in
[`hosted-bzm-mcp`](https://github.com/Blazemeter/hosted-bzm-mcp).
This file documents how **bzm-mcp** uses the Storage Service introduced on
`STREAMABLE_HTTP`.

## Runtime wiring

| Mode | Transport | Session store | File access |
|------|-----------|---------------|-------------|
| Stdio / local Docker | `stdio` | `InMemorySessionStorageProvider` | `LocalPathFileSource` / Docker mapped paths |
| Hosted HTTP | `streamable-http` | `HttpSessionStorageProvider` | `StorageFileSource` |

Composition root: `build_runtime` → `AppRuntime.storage` (`SessionStoragePort`)
→ `configure_dataframe_storage(runtime.storage)` in `server.register_tools`.

Partition key: `{user_id}/{mcp_session_id}` via `DefaultSessionScopeResolver`
(`Mcp-Session-Id` header, then FastMCP `ctx.session_id`).

## Session Storage Service

Env: `BZM_STORAGE_API_BASE_URL` (required for streamable-http).

| Method | Path |
|--------|------|
| `GET` / `PUT` / `DELETE` | `/session-partitions/{user_id}/{mcp_session_id}` |

`put_partition` accepts a partial `SessionPartitionPayload`. Dataframe tools
send only `dataframes`, so tasks/metadata/uploaded_files are preserved by the
storage merge.

MCP workers keep Polars/SQL in-process; only the partition document is remote.

## Dataframe tools

`dataframes_list`, `dataframes_query`, `dataframes_remove`, and
`dataframes_clear` hydrate/persist through `SessionStoragePort`. Stdio uses
in-memory partitions; hosted uses the HTTP Storage Service client.
