# Hosted MCP — session storage + dataframes

Hosted MCP ops deploy lives in
[`hosted-bzm-mcp`](https://github.com/Blazemeter/hosted-bzm-mcp).
This file documents how **bzm-mcp** uses the Storage Service introduced on
`STREAMABLE_HTTP`.

## Naming (do not rename STREAMABLE_HTTP types)

Dataframe tools depend on `AppRuntime.storage: SessionStoragePort`. Story names
map to the types already landed on `STREAMABLE_HTTP`:

| Story / plan name | STREAMABLE_HTTP type | Used for dataframes |
|-------------------|----------------------|---------------------|
| StoragePort | `SessionStoragePort` | Yes |
| MemoryStorageProvider | `InMemorySessionStorageProvider` | Yes (stdio) |
| HttpStorageProvider | `HttpSessionStorageProvider` | Yes (hosted) |
| HTTPStorageClient (story) | `HttpSessionStorageProvider` | Yes |

## Runtime wiring

| Mode | Transport | Session store | File access |
|------|-----------|---------------|-------------|
| Stdio / local Docker | `stdio` | `InMemorySessionStorageProvider` | `LocalPathFileSource` / Docker mapped paths |
| Hosted HTTP | `streamable-http` | `HttpSessionStorageProvider` | `None` (mint via `TicketPort`) |

Composition root: `build_runtime` → `AppRuntime.storage` / `scope_resolver`.
`server.register_tools` also calls `configure_task_storage(runtime.storage)` so
async tasks share the same session partitions as dataframes.
Tool registrations call `run_tool_with_runtime(runtime, ...)` so tracing stays
unaware of dataframe types. There is no process-global dataframe store.

Partition key: `{user_id}/{mcp_session_id}` via `DefaultSessionScopeResolver`,
taken only from the validated chat session of the current tool call:

1. Every tool call verifies the token with BlazeMeter `GET /user`
   (`AppRuntime.identity`); `user_id` is the verified BlazeMeter user id.
2. Every tool except `blazemeter_session` requires `session_id` (from
   `blazemeter_session` action `get`, once per conversation). The entrypoint checks it
   is ACTIVE and owned by that user (`AppRuntime.sessions`: in memory on stdio,
   storage-api `/sessions` on streamable-http) and records the keep-alive.
3. Only then are identity and session bound in request-scoped ContextVars; outside a
   validated call the resolver fails closed (no shared `anonymous`/`default` partition).

Sessions are bound to the credential they were opened with (opaque; today the
BlazeMeter `Authorization` value). The storage-api keeps only its HMAC and every
storage call (touch, partitions, mint, credentials) sends it in `X-Bzm-Credential`;
a different credential, even a rotated key of the same user, is `SESSION_INVALID`.

Hosted session lifecycle (owned by the storage-api): 7 days without a keep-alive →
`SESSION_EXPIRED` ("get a new session"); one hour after that first answer the session
and its partitions are purged, and the id then answers `SESSION_INVALID`, which asks
for a new session as well. stdio sessions last as long as the process.

`blazemeter_help` and `blazemeter_skills` are public: no API key needed and
`session_id` optional. With a valid token + session they run in that session;
otherwise they run inline without a session (no task, no partition) and add a warning.

`Mcp-Session-Id` / FastMCP `ctx.session_id` are transport sessions and are not used.
Errors: `SESSION_REQUIRED`, `SESSION_INVALID` (unknown or someone else's),
`SESSION_EXPIRED`, `AUTH_INVALID`, `AUTH_UNAVAILABLE`.

## Session Storage Service

Env: `BZM_STORAGE_API_BASE_URL` (required for streamable-http).

| Method | Path |
|--------|------|
| `GET` / `PUT` / `DELETE` | `/session-partitions/{user_id}/{mcp_session_id}` |

`put_partition` accepts a partial `SessionPartitionPayload`. Dataframe tools
send only `dataframes`; the async task runner sends only `tasks`. Other
sections are preserved by the storage merge.

MCP workers keep Polars/SQL and asyncio task handles in-process; only the
partition document is remote.

### Task map concurrency

`put_partition(tasks=...)` replaces the **entire** tasks map for that
partition. In-process locks serialize mutations on one worker. Across hosted MCP
workers, commit re-reads `SessionStoragePort` and unions keys added by other
writers (and drops ids this operation removed). Live local `asyncio.Task`
handles win on overlapping keys. Same-key concurrent writes and the GET/PUT
race can still last-write-win. Closing that window needs Storage CAS/etag.

## Task execution affinity (hosted)

- **Status / list / get** are Storage-backed and work across workers for a session.
- **In-flight execution** (`asyncio.Task`, semaphore, cancel of a live handle) is
  **process-local**. Only the worker that started the coroutine can cancel it via
  the local handle.
- Calling `tasks_cancel` on a different worker marks cancel in Storage when there
  is no local handle, but the owning worker may still finish and overwrite status
  to `completed` / `failed`. Do not assume multi-worker cancel stops execution.
- Prefer sticky routing / single-writer affinity for a session while tasks are
  active if cancel must be reliable.

### Dataframe map concurrency

`put_partition(dataframes=...)` replaces the **entire** dataframes map for that
partition. In-process locks serialize mutations on one worker. Across hosted MCP
workers, commit re-reads `SessionStoragePort` and unions keys added by other
writers (and drops ids this operation removed). Same-key concurrent writes and
the GET/PUT race can still last-write-win. Closing that window needs Storage
CAS/etag, which this service does not expose yet.

## Dataframe tools

`dataframes_list`, `dataframes_query`, `dataframes_remove`, and
`dataframes_clear` hydrate/commit through `SessionStoragePort`. Stdio uses
`InMemorySessionStorageProvider`; hosted uses `HttpSessionStorageProvider`.
Missing session storage on a path that would persist fails closed (error, not raw payload).

