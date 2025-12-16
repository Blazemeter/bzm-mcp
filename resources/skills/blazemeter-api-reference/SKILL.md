---
name: blazemeter-api-reference
description: Comprehensive reference for BlazeMeter REST APIs, including authentication, identifiers, and API endpoints. Use when working with BlazeMeter APIs for (1) Understanding BlazeMeter REST API structure, (2) Authenticating API requests, (3) Obtaining identifiers (Workspace ID, Project ID, Test ID, etc.), (4) Using Test Data API, (5) Using Cloning API, (6) Using Export API, (7) Using Service Virtualization Bulk Operations APIs, or any other API tasks.
---

# BlazeMeter API Reference

Comprehensive reference for BlazeMeter REST APIs.

## Overview

BlazeMeter provides REST APIs for automating test execution, managing resources, and integrating with external systems. This skill covers API authentication, identifiers, and all available API endpoints.

## Quick Start

1. **Overview**: Understand BlazeMeter REST API structure
2. **Authentication**: Configure API key authentication
3. **Identifiers**: Obtain Workspace ID, Project ID, Test ID, and other identifiers
4. **APIs**: Use Test Data API, Cloning API, Export API, and Bulk Operations APIs

## MCP Tools Integration

BlazeMeter MCP tools provide programmatic access to BlazeMeter, complementing the REST APIs. The MCP tools offer a higher-level interface for common operations:

### Available MCP Tools

- **User Management**: 
  - `blazemeter_user` with action `read_user` - Read current user information
  - Returns: User details including default account, workspace, and project

- **Account Management**: 
  - `blazemeter_account` with action `read` - Read account information
  - `blazemeter_account` with action `list` - List all accounts
  - Required args: `account_id` (integer) for read action

- **Workspace Management**: 
  - `blazemeter_workspaces` with action `read` - Read workspace details
  - `blazemeter_workspaces` with action `list` - List all workspaces
  - `blazemeter_workspaces` with action `read_locations` - Get location lists
  - Required args: `workspace_id` (integer) for read action, `account_id` (integer) for list action

- **Project Management**: 
  - `blazemeter_project` with action `read` - Read project information
  - `blazemeter_project` with action `list` - List all projects
  - Required args: `project_id` (integer) for read action, `workspace_id` (integer) for list action

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details
  - `blazemeter_tests` with action `list` - List all tests
  - `blazemeter_tests` with action `create` - Create new tests
  - `blazemeter_tests` with action `configure_load` - Configure load settings
  - `blazemeter_tests` with action `configure_locations` - Configure location distribution
  - `blazemeter_tests` with action `upload_assets` - Upload test assets
  - Required args: `test_id` (integer) or `project_id` (integer)

- **Execution Management**: 
  - `blazemeter_execution` with action `start` - Start test execution
  - `blazemeter_execution` with action `read` - Read execution details
  - `blazemeter_execution` with action `list` - List all executions
  - `blazemeter_execution` with action `read_summary` - Get summary report
  - `blazemeter_execution` with action `read_errors` - Get error report
  - `blazemeter_execution` with action `read_request_stats` - Get request statistics
  - `blazemeter_execution` with action `read_all_reports` - Get all reports
  - Required args: `test_id` (integer) or `execution_id` (integer)

- **Help System**: 
  - `blazemeter_help` with action `list_help_categories` - List help categories
  - `blazemeter_help` with action `list_help_category_content` - List help content
  - `blazemeter_help` with action `read_help_info` - Read help information
  - Required args: Varies by action

### When to Use MCP Tools vs REST APIs

- **MCP Tools**: Use for high-level operations, automation workflows, and AI agent interactions
- **REST APIs**: Use for direct API access, custom integrations, and fine-grained control

### Example Workflow

**Using MCP Tools for API-like Operations**:
1. Use `blazemeter_user` with action `read_user` to get default workspace and project IDs
2. Use `blazemeter_tests` with action `list` to find tests (equivalent to GET /tests API)
3. Use `blazemeter_execution` with action `start` to execute tests (equivalent to POST /tests/{testId}/start API)
4. Use `blazemeter_execution` with action `read_summary` to get results (equivalent to GET /executions/{executionId}/summary API)

## Reference Files

### Overview
- **[overview.md](skill-blazemeter-api-reference://references/overview.md)**: BlazeMeter REST APIs, API Overview

### Authentication
- **[authentication.md](skill-blazemeter-api-reference://references/authentication.md)**: Authorization, API Keys

### Identifiers
- **[identifiers.md](skill-blazemeter-api-reference://references/identifiers.md)**: Get Your Workspace ID, Get the Project ID, Get the Test or Collection ID, Get the Scenario ID, Get the Master ID, Get the Session ID, Get the Location Name

### Test Data API
- **[test-data-api.md](skill-blazemeter-api-reference://references/test-data-api.md)**: Test Data API

### Cloning API
- **[cloning-api.md](skill-blazemeter-api-reference://references/cloning-api.md)**: Cloning API

### Export API
- **[export-api.md](skill-blazemeter-api-reference://references/export-api.md)**: Export API

### Bulk Operations
- **[bulk-operations.md](skill-blazemeter-api-reference://references/bulk-operations.md)**: Service Virtualization Bulk Operations APIs

## When to Use Each Reference

- **Overview**: When understanding BlazeMeter REST API structure and endpoints
- **Authentication**: When configuring API key authentication or authorization
- **Identifiers**: When obtaining Workspace ID, Project ID, Test ID, or other identifiers for API calls
- **Test Data API**: When using Test Data API for generating and managing test data
- **Cloning API**: When cloning services using the Cloning API
- **Export API**: When exporting services using the Export API
- **Bulk Operations**: When performing bulk operations on Service Virtualization

