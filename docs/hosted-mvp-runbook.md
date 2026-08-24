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

Composition root: `build_runtime` → `AppRuntime.storage` / `scope_resolver`.
Tool registrations call `run_tool_with_runtime(runtime, ...)` so tracing stays
unaware of dataframe types. There is no process-global dataframe store.

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

### Dataframe map concurrency

`put_partition(dataframes=...)` replaces the **entire** dataframes map for that
partition. In-process locks serialize mutations on one worker. Across Cloud Run
instances, persist re-reads Storage and unions keys added by other writers
(and drops ids this operation removed). Same-key concurrent writes and the
GET/PUT race can still last-write-win. Closing that window needs Storage
CAS/etag, which this service does not expose yet.

## Dataframe tools

`dataframes_list`, `dataframes_query`, `dataframes_remove`, and
`dataframes_clear` hydrate/persist through `SessionStoragePort`. Stdio uses
in-memory partitions; hosted uses the HTTP Storage Service client.
Missing storage on a path that would persist fails closed (error, not raw payload).

## Load-testing concurrency (JMeter)

Unit tests cannot open the Cloud Run GET/PUT window. Use
[`tests/jmeter/hosted-dataframe-storage.jmx`](../tests/jmeter/hosted-dataframe-storage.jmx)
(see [`tests/jmeter/README.md`](../tests/jmeter/README.md)) against hosted HTTP MCP.

That plan uses the JMeter MCP plugin (`STREAMABLE_HTTP` + `Authorization` headers).
One Client Config is one MCP session: concurrent threads share `{user_id, mcp_session_id}`.
A second Client Config is a second session (isolation).
`blazemeter_tests` `list` needs an integer `project_id`: pass `-Jmcp.projectId=…` or let step 05 copy `default_project_id` from user read.

Interpretation of `dataframes_list.total` vs successful `result_format=dataframe` stores:

- Equal, with MCP `max-instances=1`: in-process session locks serialized the writes.
- Equal, with `max-instances>1`: merge-on-persist kept distinct ids for that run.
- Listed &lt; stored: last-write-wins on the whole map (GET/PUT race). Raise threads
  and Cloud Run instances to make that more likely. Set `-Jmcp.failOnLostUpdates=true`
  if the run should fail when keys are dropped.

