---
name: blazemeter-functional-testing
description: Comprehensive guide for BlazeMeter Functional Testing, including GUI Functional Tests, API Tests (deprecated), Action Library, and debugging. Use when working with Functional Testing for (1) Creating GUI Functional Tests (YAML, Java IDE, Python IDE), (2) Managing Functional Tests (duplicate, delete, move, rename), (3) Using test data in Functional Tests, (4) Working with Action Library, (5) Debugging Functional Tests, (6) Understanding browser support, or any other Functional Testing tasks. Note - API Functional Tests are deprecated in favor of API Monitoring.
---

# BlazeMeter Functional Testing

Comprehensive guide for creating and managing Functional Tests in BlazeMeter.

## Overview

Functional Testing in BlazeMeter supports GUI Functional Tests with scriptless creation, YAML upload, and IDE-based development. This skill covers test creation, management, debugging, and browser support.

## Quick Start

1. **GUI Tests**: Create tests using scriptless UI, YAML files, or IDEs
2. **Test Data**: Use test data in Functional Tests
3. **Action Library**: Manage shared Objects and Group Actions
4. **Debugging**: Debug tests using best practices
5. **Browsers**: Understand browser support and selection

## MCP Tools Integration

Functional Tests are managed through the BlazeMeter UI, but you can use MCP tools to manage tests and executions:

### Available MCP Tools

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details including functional test configuration
  - `blazemeter_tests` with action `list` - List all tests in a project
  - Required args: `test_id` (integer) or `project_id` (integer)
  - Returns: Test details including functional test configuration

- **Test Execution**:
  - `blazemeter_execution` with action `read` - Read execution details for functional tests
  - `blazemeter_execution` with action `list` - List all executions for a test
  - Required args: `execution_id` (integer) or `test_id` (integer)
  - Returns: Execution details and results

### When to Use MCP Tools

- **Test Management**: Manage functional tests programmatically
- **Execution Monitoring**: Monitor functional test executions
- **Automation**: Integrate functional testing into automation workflows
- **Reporting**: Generate reports on functional test results

### Example Workflow

**Managing Functional Tests**:
1. Use `blazemeter_tests` with action `list` to find functional tests
2. Use `blazemeter_tests` with action `read` to get test details
3. Use `blazemeter_execution` with action `read` to monitor test execution
4. Review execution results for functional test outcomes

## Reference Files

### GUI Tests
- **[gui-tests.md](skill-blazemeter-functional-testing://references/gui-tests.md)**: Overview, Create YAML File, Create from Java IDE, Create from Python IDE, Report, Duplicate/Delete/Move/Rename Test, Test Data, Parameterize Taurus YAML Scripts, Desired Capabilities Options, Custom JavaScript Actions, Taurus Actions Scriptless

### API Tests (Deprecated)
- **[api-tests.md](skill-blazemeter-functional-testing://references/api-tests.md)**: Create, Report, Scripting in UI, Create from Existing Script. **Note: This feature is deprecated. Use API Monitoring instead.**

### Action Library
- **[action-library.md](skill-blazemeter-functional-testing://references/action-library.md)**: Test Action Library, Management

### Debugging
- **[debugging.md](skill-blazemeter-functional-testing://references/debugging.md)**: Debug Best Practices

### Browsers
- **[browsers.md](skill-blazemeter-functional-testing://references/browsers.md)**: Supported Browsers

## When to Use Each Reference

- **GUI Tests**: When creating, managing, or reporting on GUI Functional Tests
- **API Tests**: When working with deprecated API Functional Tests (use API Monitoring instead)
- **Action Library**: When managing shared test components
- **Debugging**: When debugging Functional Tests
- **Browsers**: When understanding browser support and selection

