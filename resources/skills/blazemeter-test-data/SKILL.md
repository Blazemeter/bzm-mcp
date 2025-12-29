---
name: blazemeter-test-data
description: Comprehensive guide for BlazeMeter Test Data Management, including data entities, parameters, generation, orchestration, and management operations. Use when working with test data for (1) Creating and managing data entities and parameters, (2) Generating synthetic test data with seed lists and functions, (3) Using test data in tests (CSV, Data Entities), (4) Managing test data (backup, import/export, sharing), (5) Using Test Data Orchestration and Profiler, (6) Working with Test Data Pro, or any other Test Data Management tasks.
---

# BlazeMeter Test Data Management

Comprehensive guide for creating, managing, and using test data in BlazeMeter tests.

## Overview

Test Data Management in BlazeMeter enables data-driven testing with CSV files, Data Entities, synthetic data generation, and orchestration. This skill covers all aspects of test data from basic concepts to advanced management operations.

## Quick Start

1. **Core Concepts**: Understand Data Entities and Data Parameters
2. **Generation**: Create synthetic test data with seed lists and functions
3. **Management**: Manage entities, spreadsheets, and parameters
4. **Orchestration**: Prepare test environments with Test Data Orchestration
5. **Pro**: Use Test Data Pro for AI-driven data generation

## MCP Tools Integration

Test Data entities are managed through the BlazeMeter UI, but you can use MCP tools to manage tests that use test data:

### Available MCP Tools

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details including test data configuration
  - `blazemeter_tests` with action `list` - List all tests in a project
  - Required args: `test_id` (integer) or `project_id` (integer)
  - Returns: Test details including test data entity references

- **Test Execution**:
  - `blazemeter_execution` with action `read` - Read execution details for tests using test data
  - `blazemeter_execution` with action `list` - List all executions for a test
  - Required args: `execution_id` (integer) or `test_id` (integer)
  - Returns: Execution details and results

### When to Use MCP Tools

- **Test Management**: Manage tests that use test data programmatically
- **Execution Monitoring**: Monitor test executions using test data
- **Automation**: Integrate test data testing into automation workflows
- **Reporting**: Generate reports on tests using test data

### Example Workflow

**Managing Tests with Test Data**:
1. Use `blazemeter_tests` with action `list` to find tests using test data
2. Use `blazemeter_tests` with action `read` to get test details and test data configuration
3. Use `blazemeter_execution` with action `read` to monitor test execution
4. Review execution results to verify test data usage

## Reference Files

### Core Concepts
- **[core-concepts.md](skill-blazemeter-test-data://references/core-concepts.md)**: What are Data Entities and Data Parameters, How to Use, Share, How to Parameterize, How to Use Parameters in Tests, Load from Spreadsheets

### Management
- **[management.md](skill-blazemeter-test-data://references/management.md)**: How to Find Usages, How to Back Up, How to Manage Spreadsheets, How to Manage Data Parameters, How to Manage Entities, How to Configure CSV, How to Troubleshoot, How to Preview, Settings, Share Entities Within Workspace, Share Spreadsheets Within Workspace, Unshare, Import Export, How to Add Entity

### Generation
- **[generation.md](skill-blazemeter-test-data://references/generation.md)**: Generator Functions Seed Lists, How to Randomize, Variants, Negative Chaos Testing

### Orchestration
- **[orchestration.md](skill-blazemeter-test-data://references/orchestration.md)**: Test Data Orchestration, Profiler

### Pro
- **[pro.md](skill-blazemeter-test-data://references/pro.md)**: Test Data Pro, Test Data Pro FAQ

## When to Use Each Reference

- **Core Concepts**: When learning about data entities, parameters, and basic usage
- **Management**: When managing, backing up, sharing, or troubleshooting test data
- **Generation**: When creating synthetic test data with functions and seed lists
- **Orchestration**: When preparing test environments or profiling scripts
- **Pro**: When using Test Data Pro for AI-driven data generation

