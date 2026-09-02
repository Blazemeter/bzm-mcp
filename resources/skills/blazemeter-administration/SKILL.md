---
name: blazemeter-administration
description: "Comprehensive guide for BlazeMeter Administration, including workspaces, projects, security, alerts, and team management. Use when working with administration for (1) Managing workspaces and projects, (2) Configuring security settings (SAML SSO, 2FA, API keys), (3) Creating workspace alerts, (4) Managing private locations across workspaces, (5) Creating APM credentials, (6) Managing API Monitoring teams, (7) Configuring AI consent, or any other administration tasks."
---

# BlazeMeter Administration

Comprehensive guide for administering BlazeMeter accounts, workspaces, and teams.

## Quick Start

1. **Workspaces & Projects**: Manage workspaces, projects, and default settings
2. **Security**: Configure SAML SSO, 2FA, and API keys
3. **Alerts**: Create workspace alerts for notifications
4. **Teams**: Manage API Monitoring teams and permissions

## MCP Tools Integration

### Available MCP Tools

| Tool | Action | Required Args | Purpose |
|------|--------|---------------|---------|
| `blazemeter_user` | `read` | — | Read current user info (default account, workspace, project) |
| `blazemeter_account` | `read` | `account_id` (int) | Read account details including AI consent |
| `blazemeter_account` | `list` | `limit` (int), `offset` (int) | List all accounts |
| `blazemeter_workspaces` | `read` | `workspace_id` (int) | Read workspace details, locations, and billing |
| `blazemeter_workspaces` | `list` | `account_id` (int) | List workspaces for an account |
| `blazemeter_workspaces` | `read_locations` | `workspace_id` (int), `purpose` (str) | Get locations filtered by purpose: load, functional, grid, mock |
| `blazemeter_project` | `read` | `project_id` (int) | Read project info and test count |
| `blazemeter_project` | `list` | `workspace_id` (int) | List projects in a workspace |

### Example Workflows

**Getting Workspace and Project Information**:
1. Call `blazemeter_user` with action `read` to get the current user's default account ID
2. Verify the response contains a valid account ID before proceeding
3. Call `blazemeter_workspaces` with action `list`, args `{"account_id": 12345}` to list workspaces
4. Call `blazemeter_project` with action `list`, args `{"workspace_id": 67890}` to list projects
5. Verify each response has no `error` field before using the returned IDs

**Checking AI Consent**:
1. Call `blazemeter_account` with action `read`, args `{"account_id": 12345}`
2. If the response returns an error about AI consent not being enabled, the account cannot be used for AI operations — advise the user to contact their account manager

**Listing Available Test Locations**:
1. Call `blazemeter_workspaces` with action `read_locations`, args `{"workspace_id": 67890, "purpose": "load"}`
2. The response includes both public cloud locations and any private locations configured for the workspace
3. Use a returned location ID when configuring test execution targets

## Reference Files

- **[workspaces-projects.md](skill-blazemeter-administration://references/workspaces-projects.md)**: Workspaces and Projects, How to Change Default Test Location, Time Zone Override, Managing an Account
- **[security.md](skill-blazemeter-administration://references/security.md)**: Security, Two-Factor Authentication, SAML SSO setup
- **[alerts.md](skill-blazemeter-administration://references/alerts.md)**: Creating Workspace Alerts for test and usage notifications
- **[private-locations.md](skill-blazemeter-administration://references/private-locations.md)**: Manage Private Locations across workspaces
- **[apm-credentials.md](skill-blazemeter-administration://references/apm-credentials.md)**: Creating APM Credentials for monitoring integrations
- **[api-monitoring-teams.md](skill-blazemeter-administration://references/api-monitoring-teams.md)**: API Monitoring Teams, RBAC, and bucket management
- **[ai-consent.md](skill-blazemeter-administration://references/ai-consent.md)**: AI Consent Management at the account level

