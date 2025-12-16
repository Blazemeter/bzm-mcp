---
name: blazemeter-usage-billing
description: Guide for BlazeMeter Usage & Billing, including credit types and charging. Use when working with usage and billing for (1) Understanding BlazeMeter credit types (VU, VUH, Tests), (2) Calculating credit consumption for different test types, or any other usage and billing tasks.
---

# BlazeMeter Usage & Billing

Guide for understanding BlazeMeter usage and billing.

## Overview

Usage & Billing covers credit types, charging models, and credit consumption calculation for different test types in BlazeMeter. This skill helps you understand how credits are consumed, optimize credit usage, and access billing information through BlazeMeter MCP tools.

## Quick Start

1. **Understand Credit Types**: Learn about VU, VUH, and Tests credits
2. **Calculate Consumption**: Understand how credits are charged for each test type
3. **Optimize Usage**: Learn strategies to optimize credit consumption
4. **Access Billing Info**: Use MCP tools to access workspace billing information

## MCP Tools Integration

While there are no dedicated MCP tools for credit management, you can access billing information through workspace tools:

### Available MCP Tools

- **Workspace Billing Information**: 
  - `blazemeter_workspaces` with action `read` - Read workspace details including billing usage information
  - Required args: `workspace_id` (integer)
  - Returns: Workspace details with billing usage data

### When to Use MCP Tools

- **Programmatic Access**: Use MCP tools to programmatically retrieve billing information
- **Automation**: Integrate billing information into automation scripts
- **Monitoring**: Monitor credit consumption patterns through API access

### Example Workflow

**Getting Workspace Billing Information**:
1. Use `blazemeter_workspaces` with action `read` to get workspace details
2. Extract billing usage information from the workspace response
3. Use this information for reporting or monitoring

## Reference Files

### Credits
- **[credits.md](skill-blazemeter-usage-billing://references/credits.md)**: Credit Types and Charging

## When to Use This Reference

- **Credits**: When understanding BlazeMeter credit types, how credits are charged, or calculating credit consumption for performance, functional, API monitoring, and service virtualization tests

