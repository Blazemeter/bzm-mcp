---
name: blazemeter-administration
description: Comprehensive guide for BlazeMeter Administration, including workspaces, projects, security, alerts, and team management. Use when working with administration for (1) Managing workspaces and projects, (2) Configuring security settings (SAML SSO, 2FA, API keys), (3) Creating workspace alerts, (4) Managing private locations across workspaces, (5) Creating APM credentials, (6) Managing API Monitoring teams, (7) Configuring AI consent, or any other administration tasks.
---

# BlazeMeter Administration

Comprehensive guide for administering BlazeMeter accounts, workspaces, and teams.

## Overview

Administration in BlazeMeter covers account management, workspace and project configuration, security settings, alerts, and team management. This skill covers all administrative tasks and integrates with BlazeMeter MCP tools for programmatic administration.

## Quick Start

1. **Workspaces & Projects**: Manage workspaces, projects, and default settings
2. **Security**: Configure SAML SSO, 2FA, and API keys
3. **Alerts**: Create workspace alerts for notifications
4. **Teams**: Manage API Monitoring teams and permissions

## MCP Tools Integration

This skill leverages BlazeMeter MCP tools for programmatic administration. Use these tools to automate administrative tasks:

### Available MCP Tools

- **User Management**: 
  - `blazemeter_user` with action `read_user` - Read current user information from BlazeMeter

- **Account Management**: 
  - `blazemeter_account` with action `read` - Read account information including AI consent settings
  - `blazemeter_account` with action `list` - List all accounts

- **Workspace Management**: 
  - `blazemeter_workspaces` with action `read` - Read workspace details including available locations and billing usage
  - `blazemeter_workspaces` with action `list` - List all workspaces for an account
  - `blazemeter_workspaces` with action `read_locations` - Get location lists for a workspace (filter by purpose: load, functional, grid, mock)

- **Project Management**: 
  - `blazemeter_project` with action `read` - Read project information
  - `blazemeter_project` with action `list` - List all projects in a workspace

### When to Use MCP Tools

- **Programmatic Operations**: Use MCP tools for automation, scripting, and integration
- **Data Retrieval**: Use MCP tools to read account, workspace, and project information
- **Configuration Tasks**: Use UI for visual configuration tasks (security settings, alerts, team management)

### Example Workflows

**Getting Workspace and Project Information**:
1. Use `blazemeter_account` to list accounts and get account ID
2. Use `blazemeter_workspaces` to list workspaces and get workspace ID
3. Use `blazemeter_project` to list projects and get project ID
4. Use these IDs for subsequent operations or API calls

**Checking AI Consent**:
1. Use `blazemeter_account` with action `read` to get account details
2. Check AI consent information in the account response

## Reference Files

### Workspaces & Projects
- **[workspaces-projects.md](skill-blazemeter-administration://references/workspaces-projects.md)**: Workspaces and Projects, How to Change Default Test Location, Time Zone Override, Managing an Account

### Security
- **[security.md](skill-blazemeter-administration://references/security.md)**: Security, Two-Factor Authentication

### Alerts
- **[alerts.md](skill-blazemeter-administration://references/alerts.md)**: Creating Workspace Alerts

### Private Locations
- **[private-locations.md](skill-blazemeter-administration://references/private-locations.md)**: Manage Private Locations

### APM Credentials
- **[apm-credentials.md](skill-blazemeter-administration://references/apm-credentials.md)**: Creating APM Credentials

### API Monitoring Teams
- **[api-monitoring-teams.md](skill-blazemeter-administration://references/api-monitoring-teams.md)**: API Monitoring Teams

### AI Consent
- **[ai-consent.md](skill-blazemeter-administration://references/ai-consent.md)**: AI Consent Management

## When to Use Each Reference

- **Workspaces & Projects**: When managing workspaces, projects, or account settings
- **Security**: When configuring security settings, SSO, or 2FA
- **Alerts**: When creating workspace alerts
- **Private Locations**: When managing private locations across workspaces
- **APM Credentials**: When creating APM integration credentials
- **API Monitoring Teams**: When managing API Monitoring teams
- **AI Consent**: When configuring AI consent settings

