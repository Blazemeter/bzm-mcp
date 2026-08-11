# Hosted MCP MVP runbook

For platform operators running BlazeMeter MCP behind TLS at
`https://mcp.blazemeter.com/mcp`.

MVP: single Cloud Run instance, in-memory storage, no external Storage Service.
Stdio / local Docker clients (IDE `docker run …:latest`) are unchanged.

## Deploy matrix

| Mode | Transport | Auth | Storage | File access |
|------|-----------|------|---------|-------------|
| Hosted prod (MVP) | streamable-http | Bearer | memory | Local paths rejected |

## Container configuration

| Variable | Hosted value |
|----------|--------------|
| `BZM_MCP_TRANSPORT` | `http` (or `CMD ["--mcp", "http"]`) |
| `FASTMCP_HOST` | `0.0.0.0` |
| `FASTMCP_PORT` | `8000` (Cloud Run may inject `PORT`; app falls back to `PORT`) |
| `FASTMCP_STREAMABLE_HTTP_PATH` | `/mcp` |
| `BZM_STORAGE_BACKEND` | `memory` (default; no external Storage) |

Do **not** set `MCP_DOCKER=true` on the hosted image (that flag is for local
stdio Docker + volume mounts).

## Images (do not mix tags)

| Image | Tag | Dockerfile | Audience |
|-------|-----|------------|----------|
| Stdio | `latest`, semver | `Dockerfile` (PyInstaller binary) | Existing IDE Docker clients |
| Hosted HTTP | `hosted`, `hosted-<version>` | `Dockerfile.hosted` (Python source) | Cloud Run only |

**Never** retag or overwrite `:latest` with the hosted image.

Artifact Registry (prod project `esd-blazemeter-slc-prd`):

```text
us-central1-docker.pkg.dev/esd-blazemeter-slc-prd/bzm-mcp/bzm-mcp:hosted
```

GHCR (when CI publishes): `ghcr.io/blazemeter/bzm-mcp:hosted`

## Endpoints

| Path | Auth | Purpose |
|------|------|---------|
| `GET /health`, `GET /healthz` | None | Orchestrator / LB probes |
| `POST /mcp` (streamable HTTP) | `Authorization: Bearer` | MCP clients |

Production base URL: `https://mcp.blazemeter.com`

## CI/CD path (build → deploy)

### 1. Build & push image (`bzm-mcp` repo)

1. Merge/release on the branch that contains hosted HTTP support.
2. Prefer building **`Dockerfile.hosted` from source** (not an old
   `dist/bzm-mcp-linux-*` binary — that caused Cloud Run “failed to listen on PORT”).
3. CI: `.github/workflows/docker-multiplatform.yaml` publishes stdio tags from
   `Dockerfile` and hosted tags from `Dockerfile.hosted`.
4. For GCP, also push/mirror to Artifact Registry `:hosted` (keep `:latest` intact).

Manual build example:

```bash
export PROJECT_ID=esd-blazemeter-slc-prd
export AR_HOSTED="us-central1-docker.pkg.dev/${PROJECT_ID}/bzm-mcp/bzm-mcp:hosted"

gcloud auth configure-docker us-central1-docker.pkg.dev
docker buildx build --platform linux/amd64 \
  -f Dockerfile.hosted \
  -t "$AR_HOSTED" \
  --push .
```

### 2. Deploy (`mcp-services` / Cloud Run)

Target project: `esd-blazemeter-slc-prd`, region `us-central1`, service
`bzm-mcp-hosted`, **min=max instances = 1**.

Deploy manifests and CI live in the
[mcp-services](https://github.com/Blazemeter/mcp-services) repository
(`cloudrun/service.yaml`, `.github/workflows/deploy-hosted-mcp.yaml`).

```bash
export PROJECT_ID=esd-blazemeter-slc-prd
export REGION=us-central1
export SERVICE=bzm-mcp-hosted
export AR_HOSTED="us-central1-docker.pkg.dev/${PROJECT_ID}/bzm-mcp/bzm-mcp:hosted"

gcloud run deploy "$SERVICE" \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --image="$AR_HOSTED" \
  --port=8000 \
  --allow-unauthenticated \
  --min-instances=1 \
  --max-instances=1 \
  --cpu=1 \
  --memory=512Mi \
  --set-env-vars="BZM_MCP_TRANSPORT=http,FASTMCP_HOST=0.0.0.0,BZM_STORAGE_BACKEND=memory"
```

`--allow-unauthenticated` opens the edge only; `/mcp` still requires Bearer.
Probes use `/health`.

### 3. DNS + TLS (`mcp.blazemeter.com`)

1. Cloud DNS zone `mcp` (`mcp.blazemeter.com.`) in `esd-blazemeter-slc-prd`,
   **NS-delegated from apex** `blazemeter.com` (same pattern as `bem` /
   `shiftleft`).
2. Cloud Run domain mapping → service `bzm-mcp-hosted`.
3. Publish the records from `gcloud beta run domain-mappings describe` into
   zone `mcp`.
4. Wait for Google-managed certificate.

```bash
gcloud beta run domain-mappings create \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --service="$SERVICE" \
  --domain=mcp.blazemeter.com

gcloud beta run domain-mappings describe \
  --domain=mcp.blazemeter.com \
  --region="$REGION" \
  --project="$PROJECT_ID"
```

### 4. Smoke

```bash
curl -sf https://mcp.blazemeter.com/health
# {"status":"ok"}

# MCP client (Cursor / VS Code):
# url: https://mcp.blazemeter.com/mcp
# headers.Authorization: Bearer <apiKeyId>:<apiKeySecret>
# → list tools → blazemeter_user action read
```

Local image smoke (Apple Silicon needs `--platform linux/amd64` if the image is amd64-only):

```bash
docker run --rm --platform linux/amd64 -p 8000:8000 -e PORT=8000 "$AR_HOSTED"
curl -sf http://127.0.0.1:8000/health
```

## Storage contract (app)

- `StoragePort` — `config/storage.py` (session get/put/delete + file access)
- `SessionPartition` — `{metadata, dataframes, tasks, uploaded_files}` under
  `{user_id}/{mcp_session_id}`
- `MemoryStorageProvider` — stdio / local Docker: in-memory session partitions +
  local disk files (`BZM_STORAGE_BACKEND=memory`)
- `HTTPStorageClient` — hosted streamable-http: HTTP client to Storage Service
  (`BZM_STORAGE_SERVICE_URL`); file map/read/upload still raise
  `StorageNotSupportedError` until remote `uploaded_files` lands

Storage Service API (external `bzm-mcp-storage-api`):

| Method | Path | Notes |
|--------|------|-------|
| `GET` | `/internal/v1/sessions/{user_id}/{mcp_session_id}` | `404` if missing |
| `PUT` | `/internal/v1/sessions/{user_id}/{mcp_session_id}` | full partition JSON body |
| `DELETE` | `/internal/v1/sessions/{user_id}/{mcp_session_id}` | idempotent |

Partition body: `metadata`, `dataframes`, `tasks` (objects) and `uploaded_files`
(list of `{file_id, name?, content_type?, size_bytes?, metadata?}`).
Dataframe rows are stored under `dataframes.<id>` with metadata plus a `data`
array of records. Polars/SQL stays in the MCP worker; only the backing store
is remote in hosted mode.

## MVP limitations

1. **Dataframes** are Storage-backed (Memory for stdio, HTTP for hosted). Async
   tasks (when enabled) still need the same partition treatment.
2. **File upload** (`upload_assets`) requires local disk — rejected on hosted.
   Use local stdio or stdio Docker MCP for uploads.
3. **Per-session elicitation** is still a process-wide CLI / `--confirm` flag,
   not per Bearer session.
4. **Multi-instance hosted** requires `BZM_STORAGE_SERVICE_URL` pointing at
   `bzm-mcp-storage-api` (dev/prod Cloud Run).

## Client configuration

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

Credentials: plaintext `id:secret` or base64(`id:secret`). Invalid/missing Bearer
→ `401` before tools run.
