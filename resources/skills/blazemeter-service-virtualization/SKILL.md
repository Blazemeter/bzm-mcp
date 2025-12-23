---
name: blazemeter-service-virtualization
description: Comprehensive guide for BlazeMeter Service Virtualization, including virtual services, transactions, templates, and management. Use when working with Service Virtualization for (1) Creating virtual services and transactions, (2) Managing services (clone, export/import, rename/delete), (3) Using templates and environment variables, (4) Adding processing actions to transactions, (5) Using test data with virtual services, (6) Understanding transactional analytics, or any other Service Virtualization tasks.
---

# BlazeMeter Service Virtualization

Comprehensive guide for creating and managing virtual services in BlazeMeter.

## Overview

Service Virtualization enables simulating dependencies and services for testing, supporting transactions, virtual services, templates, and processing actions. This skill covers all aspects from introduction to advanced management.

## Quick Start

1. **Introduction**: Understand concepts, use cases, and terminology
2. **Transactions**: Add transactions from files or manually
3. **Virtual Services**: Create virtual services from transactions
4. **Management**: Clone, export/import, and manage services
5. **Analytics**: Monitor transaction usage and performance

## MCP Tools Integration

Service Virtualization services are managed through the BlazeMeter UI, but you can use MCP tools to manage tests that use virtual services:

### Available MCP Tools

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details including virtual service configuration
  - `blazemeter_tests` with action `list` - List all tests in a project
  - Required args: `test_id` (integer) or `project_id` (integer)
  - Returns: Test details including virtual service references

- **Test Execution**:
  - `blazemeter_execution` with action `read` - Read execution details for tests using virtual services
  - `blazemeter_execution` with action `list` - List all executions for a test
  - Required args: `execution_id` (integer) or `test_id` (integer)
  - Returns: Execution details and results

### When to Use MCP Tools

- **Test Management**: Manage tests that use virtual services programmatically
- **Execution Monitoring**: Monitor test executions that interact with virtual services
- **Automation**: Integrate virtual service testing into automation workflows
- **Reporting**: Generate reports on tests using virtual services

### Example Workflow

**Managing Tests with Virtual Services**:
1. Use `blazemeter_tests` with action `list` to find tests using virtual services
2. Use `blazemeter_tests` with action `read` to get test details and virtual service configuration
3. Use `blazemeter_execution` with action `read` to monitor test execution
4. Review execution results to verify virtual service interactions

## Reference Files

### Introduction
- **[introduction.md](skill-blazemeter-service-virtualization://references/introduction.md)**: Introduction, Use Cases and Capabilities, The Role of Services, Transaction Repository and Transaction Types

### Transactions
- **[transactions.md](skill-blazemeter-service-virtualization://references/transactions.md)**: Add Transactions, Add Processing Actions

### Virtual Services
- **[virtual-services.md](skill-blazemeter-service-virtualization://references/virtual-services.md)**: Create Your First Virtual Service, Create a Virtual Service Template, Configure Environment Variables

### Management
- **[management.md](skill-blazemeter-service-virtualization://references/management.md)**: Rename/Move, Clone Service with all Transactions, Export and Import Services with all Transactions, Rename or Delete a Service, Test Data, Upgrade Outdated

### Analytics
- **[analytics.md](skill-blazemeter-service-virtualization://references/analytics.md)**: Transactional Analytics

## When to Use Each Reference

- **Introduction**: When getting started with Service Virtualization concepts
- **Transactions**: When adding or configuring transactions and processing actions
- **Virtual Services**: When creating virtual services, templates, or configuring environment variables
- **Management**: When managing services (clone, export/import, rename/delete, upgrade)
- **Analytics**: When monitoring transaction usage and performance metrics

