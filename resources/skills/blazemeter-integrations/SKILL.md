---
name: blazemeter-integrations
description: Comprehensive guide for BlazeMeter Integrations, including APM tools, CI/CD pipelines, and development tools. Use when working with integrations for (1) Integrating APM tools (AppDynamics, Datadog, New Relic, CloudWatch, DX APM, Dynatrace, Delphix), (2) Integrating CI/CD tools (Jenkins, GitHub Actions, GitLab CI/CD, Azure DevOps, AWS CodePipeline, Bamboo, TeamCity, CircleCI, Codeship), (3) Using development tools (Visual Studio Code Plugin, MCP Server), or any other integration tasks.
---

# BlazeMeter Integrations

Comprehensive guide for integrating BlazeMeter with APM tools, CI/CD pipelines, and development tools.

## Overview

BlazeMeter integrates with various third-party tools for APM monitoring, CI/CD automation, and development workflows. This skill covers APM integrations, CI/CD plugins, and development tools.

## Quick Start

1. **APM Tools**: Integrate with Application Performance Monitoring tools
2. **CI/CD**: Integrate with continuous integration and deployment pipelines
3. **Development Tools**: Use Visual Studio Code plugin and MCP Server

## MCP Tools Integration

BlazeMeter MCP tools are themselves part of the integration ecosystem. The MCP Server provides programmatic access to BlazeMeter, and the tools can be used to automate integration workflows.

### Available MCP Tools

- **User Management**: 
  - `blazemeter_user` with action `read_user` - Read current user information

- **Account Management**: 
  - `blazemeter_account` with action `read` - Read account information
  - `blazemeter_account` with action `list` - List all accounts

- **Workspace Management**: 
  - `blazemeter_workspaces` with action `read` - Read workspace details
  - `blazemeter_workspaces` with action `list` - List all workspaces
  - `blazemeter_workspaces` with action `read_locations` - Get location lists

- **Project Management**: 
  - `blazemeter_project` with action `read` - Read project information
  - `blazemeter_project` with action `list` - List all projects

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details
  - `blazemeter_tests` with action `list` - List all tests
  - `blazemeter_tests` with action `create` - Create new tests

- **Execution Management**: 
  - `blazemeter_execution` with action `read` - Read execution details
  - `blazemeter_execution` with action `list` - List all executions
  - `blazemeter_execution` with action `start` - Start test execution
  - `blazemeter_execution` with action `read_summary` - Get summary report
  - `blazemeter_execution` with action `read_errors` - Get error report

### When to Use MCP Tools

- **Automation**: Automate integration workflows and test management
- **CI/CD Integration**: Use MCP tools in CI/CD pipelines for test execution
- **Programmatic Access**: Access BlazeMeter programmatically for custom integrations
- **Workflow Automation**: Build custom workflows using MCP tools

### Example Workflows

**Automating CI/CD Integration**:
1. Use `blazemeter_tests` with action `list` to find tests
2. Use `blazemeter_execution` with action `start` to execute tests
3. Use `blazemeter_execution` with action `read_summary` to get results
4. Use results to set CI/CD pipeline status

**Managing APM Integrations**:
1. Use `blazemeter_workspaces` with action `read` to get workspace details
2. Access APM credential information
3. Use workspace information for APM integration setup

## Reference Files

### APM
- **[apm.md](skill-blazemeter-integrations://references/apm.md)**: Integrate with AppDynamics, Integrate with Datadog, Integrate with Delphix, New Relic APM, Set Up AWS IAM for CloudWatch

### CI/CD
- **[cicd.md](skill-blazemeter-integrations://references/cicd.md)**: Jenkins Plugin Guide, Bamboo Plugin, TeamCity Plugin, ShiftLeft Converter for LoadRunner, Testing via AWS CodePipeline, Testing via Azure DevOps Pipeline

### Development Tools
- **[development-tools.md](skill-blazemeter-integrations://references/development-tools.md)**: BlazeMeter Visual Studio Code Plugin, BlazeMeter MCP Server, BlazeMeter MCP Server Tools

## When to Use Each Reference

- **APM**: When integrating with Application Performance Monitoring tools
- **CI/CD**: When integrating with continuous integration and deployment pipelines
- **Development Tools**: When using Visual Studio Code plugin or MCP Server for local development

