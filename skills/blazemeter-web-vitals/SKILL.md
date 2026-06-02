---
name: blazemeter-web-vitals
description: "Use when working with BlazeMeter Web Vitals tests for this workspace. Collects account, workspace, project, test case, and test master IDs at execution time. Invoke via Copilot agent (interactive prompts) or CLI with --account-id, --workspace-id, --project-id, --test-case-id, --test-master-id parameters."
---

# BlazeMeter Web Vitals

## Purpose

This skill collects the BlazeMeter context IDs required for Web Vitals testing from the user at execution time and uses them to run, manage, or report on Web Vitals test executions.

## Knowledge Reference

Before interpreting results, configuring failure criteria, or answering questions about metric thresholds, consult the reference document included with this skill:

- **File:** `.github/skills/blazemeter-web-vitals/reference/webvitals.md`
- **Contents:** Definitions and Good/Needs Improvement/Poor thresholds for all 13 tracked metrics: LCP, INP, CLS (Core Web Vitals) plus TTFB, FCP, TTI, TBT, Document Complete Time, Page Load Time, Request Count, Total Page Size, DNS Lookup Time, and FPS.
- **Usage:** Load this file when the agent needs to evaluate metric values, explain what a score means, or recommend failure criteria thresholds.

## Use This Skill When

- You want to run or schedule a Web Vitals test in BlazeMeter.
- You need to look up the status or results of a Web Vitals test execution.
- You are configuring failure criteria, load settings, or locations for a Web Vitals test.
- You need to reference the canonical project/test IDs for this workspace in any BlazeMeter MCP tool call.

## Inputs

When this skill is invoked, **prompt the user to provide each of the following values** before proceeding. Do not assume or infer any ID — ask explicitly and wait for the answer.

| # | Field          | Prompt to show the user                                                              |
|---|----------------|--------------------------------------------------------------------------------------|
| 1 | Account ID     | "Please provide your BlazeMeter **Account ID**."                                    |
| 2 | Workspace ID   | "Please provide your BlazeMeter **Workspace ID**."                                  |
| 3 | Project ID     | "Please provide your BlazeMeter **Project ID**."                                    |
| 4 | Test Case ID   | "Please provide the **Test Case ID** (the test you want to run or inspect)."        |
| 5 | Test Master ID | "Please provide the **Test Master ID** (execution ID) to retrieve artifacts.zip from each load generator." |
| 6 | Action         | "Please choose the **action**: `run`, `status`, `results`, or `configure`."         |
| 7 | Report Type    | "Please choose the **report type**: `basic`, `detailed`, or `executive`."           |

All seven values are required for results/reporting workflows. If any are missing, ask again before continuing.

### Input Options

- **Action:**
  - `run`: Start or execute a Web Vitals test flow.
  - `status`: Check execution state or progress for an existing test master ID.
  - `results`: Retrieve and process outputs, including sessions, artifacts, metadata, and report generation.
  - `configure`: Update test settings such as failure criteria, load, or locations, with explicit confirmation.
- **Report Type:**
  - `basic`: Generate the default basic summary report from the HTML template.
  - `detailed`: Generate the full detailed HTML report with summary, location, step, and raw data sections.
  - `executive`: Generate an executive-style summary report intended for concise stakeholder review.

## Workflow

1. Confirm the BlazeMeter MCP server is running (use the `start-blazemeter-mcp` skill if needed).
2. Prompt the user for all required values listed in the **Inputs** section above. Collect them one by one if not provided together.
3. Echo the collected values, including `action` and `report type`, back to the user in a summary table and ask for confirmation before proceeding.
4. Validate the account → workspace → project → test hierarchy using the provided IDs.
5. Execute the requested operation using the confirmed IDs as parameters for any BlazeMeter MCP tool call.
6. Route report generation behavior according to the selected `report type`.
7. Always ask for explicit user confirmation before starting a test execution or modifying test configuration.

## Results Processing

### Phase 1: Extract Sessions from Master

**Endpoint:** `GET https://a.blazemeter.com/api/v4/masters/{masterId}`

**Extract:** The `sessions` array from the response.

**Example:**
```json
{
  "response": {
    "master": {
      "sessions": [
        "r-v4-6a0dd6850e1d3853079977",
        "r-v4-6a0dd6850e9cb576969641",
        "r-v4-6a0dd6850ef8c329482363",
        "r-v4-6a0dd6850f6a8929026722"
      ]
    }
  }
}
```

Each session ID represents a **load generator** that participated in the test execution.

### Phase 2: Extract Location from Each Session

**Endpoint:** `GET https://a.blazemeter.com/api/v4/sessions/{sessionId}`

**Extract:** The `location` field from the `configuration` object in each session response.

**Example:**
```json
{
  "response": {
    "session": {
      "configuration": {
        "location": "us-east-1"
      }
    }
  }
}
```

**Repeat for each session ID** to map sessions to their geographic locations.

### Phase 3: Download Files from Each Load Generator Session

**Endpoint:** `GET https://a.blazemeter.com/api/v4/sessions/{sessionId}/files`

**Purpose:** Retrieve the list of available files (including `artifacts.zip`) from each session.

**Example Response:**
```json
{
  "response": {
    "files": [
      {
        "id": "file-1",
        "name": "artifacts.zip",
        "size": 2048576
      },
      {
        "id": "file-2",
        "name": "report.html",
        "size": 512000
      }
    ]
  }
}
```

**Download and Rename Process:**
1. For each session ID from Phase 1, call the files endpoint to list available files.
2. Locate the `artifacts.zip` file in the response.
3. Download `artifacts.zip` from the session.
4. **Rename using the pattern:** `artifacts-{sessionId}-{location}.zip`
   - Example: `artifacts-r-v4-6a0dd6850e1d3853079977-us-east-1.zip`
5. Create an execution-specific directory with the prefix pattern: `blz_masterid_{testMasterId}_{DateTime}`
   - Example: `blz_masterid_82173056_20260527_143022`
   - Timestamp format: `YYYYMMDD_HHMMSS` (UTC)
6. Store the renamed files in the workspace directory structure:
   ```
   ${workspaceFolder}/web_vitals_process/
   ├── blz_masterid_82173056_20260527_143022/
   │   ├── us-east-1/
   │   │   ├── artifacts-r-v4-6a0dd6850e1d3853079977-us-east-1.zip
   │   │   ├── artifacts-r-v4-6a0dd6850e9cb576969641-us-east-1.zip
   │   │   └── ...
   │   ├── us-west-2/
   │   │   ├── artifacts-r-v4-6a0dd6850ef8c329482363-us-west-2.zip
   │   │   └── ...
   │   └── execution-metadata.json
   ├── blz_masterid_82173056_20260527_150515/
   │   ├── us-east-1/
   │   └── ...
   ```
7. Extract each renamed `artifacts.zip` within its execution directory to expose `web-vitals-report.csv`.
8. **Preserve naming separation:** Rename each extracted `web-vitals-report.csv` to prevent collisions:
   - Pattern: `web-vitals-report-{sessionId}-{location}.csv`
   - Example: `web-vitals-report-r-v4-6a0dd6850e1d3853079977-us-east-1.csv`
   - Storage: Keep in location subdirectory alongside the zipfile
9. Store execution metadata (test IDs, timestamps, session mappings) in `execution-metadata.json` for tracking and audit purposes.

## Phase 4: Generate HTML Report from Aggregated Metrics

**Purpose:** Parse all extracted `web-vitals-report-*.csv` files and generate a comprehensive HTML report.

**CSV Field Structure** (from `web-vitals-report.csv`):
```
timestamp, testName, stepName, url,
LCP_ms, INP_ms, CLS, TTFB_ms, FCP_ms,
TTI_ms, TBT_ms, documentCompleteTime_ms,
pageLoadTime_ms, requestCount, totalPageSizeMB,
dnsLookupTime_ms, FPS
```

**Report Hierarchy:**
1. **Account Level** → Account ID & Name
2. **Workspace Level** → Workspace ID & Name  
3. **Project Level** → Project ID & Name
4. **Test Level** → Test ID & Test Case Name
5. **Execution Level** → Test Master ID with timestamp
6. **Load Generator Sessions** → Aggregated metrics from each session/location

**Report Sections:**
- Executive Summary: Overall test performance metrics
- Per-Location Breakdown: Metrics aggregated by geographic location
- Per-Session Details: Individual session performance traces
- Step-Level Analysis: Performance metrics for each test step
- Charts & Visualizations:
  - Web Vitals trends (LCP, INP, CLS)
  - Response time distribution (TTFB, FCP, TTI)
  - Resource metrics (requestCount, totalPageSizeMB, dnsLookupTime)
  - Frame rate (FPS) stability

**HTML Report Output:**
- File: `web-vitals-{reportType}-report-{masterNameSlug}-{masterId}-{DateTime}.html`
- Location: `blz_masterid_{masterId}_{DateTime}/web-vitals-{reportType}-report-{masterNameSlug}-{masterId}-{DateTime}.html`
- Format: Self-contained HTML with embedded charts (Chart.js or similar)
- Includes: CSS styling, JavaScript interactivity, sortable tables

## Output

- Test execution status and results for the Web Vitals test case.
- Links to the BlazeMeter report for the executed test.
- **HTML Report:** A comprehensive, self-contained HTML report generated from aggregated Web Vitals metrics.

## Report Generation

After all CSV files have been extracted and organized, generate the HTML report using the provided Python script:

**Script Location:** `.github/skills/blazemeter-web-vitals/scripts/generate_web_vitals_report.py`

**Default HTML Template:** `.github/skills/blazemeter-web-vitals/html_report_templates/basic-web-vitals-report.html`

Use `basic-web-vitals-report.html` as the default baseline template for any future basic summary report logic. Additional report templates can be added under `html_report_templates/` as the skill evolves.

**Usage:**
```bash
cd ${workspaceFolder}
python .github/skills/blazemeter-web-vitals/scripts/generate_web_vitals_report.py web_vitals_process/blz_masterid_${MasterID}_${DateTime}
```

To generate the default basic summary report from the template:
```bash
cd ${workspaceFolder}
python .github/skills/blazemeter-web-vitals/scripts/generate_web_vitals_report.py web_vitals_process/blz_masterid_${MasterID}_${DateTime} --report-style basic
```

Alternatively, run from workspace root:
```bash
python -m .github.skills.blazemeter-web-vitals.scripts.generate_web_vitals_report web_vitals_process/blz_masterid_${MasterID}_${DateTime}
```

**Report Output:**
- Filename: `web-vitals-{reportType}-report-{masterNameSlug}-{masterId}-{timestamp}.html`
- Location: Inside the execution directory
- Format: Self-contained HTML with embedded styling and interactive tables
- Contents: Executive summary, location breakdown, step analysis, and raw data

**Execution Metadata Structure** (`execution-metadata.json`):
Populate this file during execution with:
```json
{
  "accountId": "account-id",
  "accountName": "Account Name",
  "workspaceId": "workspace-id",
  "workspaceName": "Workspace Name",
  "projectId": "project-id",
  "projectName": "Project Name",
  "testCaseId": "test-case-id",
  "testCaseName": "Test Case Name",
  "testMasterId": "82173056",
  "executionTime": "2026-05-27T14:30:22Z",
  "sessions": {
    "r-v4-6a0dd6850e1d3853079977": {
      "location": "us-east-1",
      "fileCount": 1
    }
  }
}
```

## Guardrails

- Always confirm the correct account/workspace/project before any create, update, or delete operation.
- Never start a test execution without explicit user approval.
- Do not modify test configuration without confirming the target test case ID matches what the user provided.
- Consult `blazemeter_skills` or `blazemeter_help` MCP tools for best practices before configuring tests.

## Example Prompts

- "Run the Web Vitals test"
- "Show me the latest Web Vitals test results"
- "What is the status of the last Web Vitals execution?"
- "Configure failure criteria for the Web Vitals test"

## How to Invoke This Skill

### Via Copilot Agent (Interactive)

Simply ask the agent to use the `blazemeter-web-vitals` skill. The agent will automatically prompt you for each required ID:

```
"Use the blazemeter-web-vitals skill to run a test"
```

The agent will then ask you to provide:
1. Account ID
2. Workspace ID
3. Project ID
4. Test Case ID
5. Test Master ID

### Via CLI (Automated / Programmatic)

Pass all five IDs as command-line parameters to avoid interactive prompts:

```bash
bzm-vitals-mcp --skill blazemeter-web-vitals \
  --account-id <ACCOUNT_ID> \
  --workspace-id <WORKSPACE_ID> \
  --project-id <PROJECT_ID> \
  --test-case-id <TEST_CASE_ID> \
  --test-master-id <TEST_MASTER_ID> \
  --action <ACTION> \
  --report-type <REPORT_TYPE>
```

Replace `<ACTION>` with one of the following operation selectors:

- `run`: Start or execute a Web Vitals test flow.
- `status`: Check execution state or progress for an existing test master ID.
- `results`: Retrieve and process outputs (sessions, artifacts, and report generation).
- `configure`: Update test settings such as failure criteria, load, or locations (with explicit confirmation).

Replace `<REPORT_TYPE>` with one of the following report selectors:

- `basic`: Use the default basic summary template.
- `detailed`: Generate the full detailed report.
- `executive`: Generate an executive summary style report.

These values define the intent of the CLI call and route the skill to the corresponding workflow path.

**Example:**
```bash
bzm-vitals-mcp --skill blazemeter-web-vitals \
  --account-id 12345 \
  --workspace-id 67890 \
  --project-id 11111 \
  --test-case-id 22222 \
  --test-master-id 33333 \
  --action results \
  --report-type basic
```

## Notes

- **Test Master ID** is the execution-level identifier returned by BlazeMeter when a test is started (also visible in the test report URL as the `masterId` parameter). Use this ID to fetch `artifacts.zip` from each load generator via the BlazeMeter API:
  ```
  GET /api/latest/data/masters/{masterId}/reports/{sessionId}/reports/artifacts.zip
  ```
- Workspace root: `${workspaceFolder}`
- API keys file: `${workspaceFolder}/api-key.json`
- MCP binary: `${workspaceFolder}/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp`
- Related skill: `start-blazemeter-mcp` — use to ensure the MCP server is running before any tool calls.
- Web Vitals metric reference: `.github/skills/blazemeter-web-vitals/reference/webvitals.md` — consult for metric definitions and Good/Needs Improvement/Poor thresholds.
- BlazeMeter API Keys guide: https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html
- BlazeMeter MCP Server docs: https://help.blazemeter.com/docs/guide/integrations-blazemeter-mcp-server.html
