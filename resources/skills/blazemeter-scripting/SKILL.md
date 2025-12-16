---
name: blazemeter-scripting
description: Comprehensive guide for BlazeMeter Scripting, including Groovy/Beanshell, JMeter plugins, JMeter DSL, and API Monitoring scripting. Use when working with scripting for (1) Writing files in Groovy/Beanshell scripts, (2) Using non-standard JMeter plugins, (3) Creating JMeter tests with JMeter DSL, (4) Writing custom scripts for API Monitoring (custom libraries, included libraries, initial script, reusable snippets), or any other scripting tasks.
---

# BlazeMeter Scripting

Comprehensive guide for scripting in BlazeMeter tests.

## Overview

Scripting in BlazeMeter supports Groovy/Beanshell for Performance tests, JMeter DSL for code-based test creation, and JavaScript for API Monitoring. This skill covers all scripting capabilities.

## Quick Start

1. **Groovy/Beanshell**: Write files and custom logic in Performance tests
2. **JMeter Plugins**: Use non-standard JMeter plugins
3. **JMeter DSL**: Create JMeter tests as code
4. **API Monitoring Scripting**: Write custom JavaScript for API Monitoring

## MCP Tools Integration

While scripting is primarily done through test configuration and code, you can use BlazeMeter MCP tools to manage tests that use custom scripts:

### Available MCP Tools

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details including script configuration
  - `blazemeter_tests` with action `list` - List all tests in a project
  - Required args: `test_id` (integer) or `project_id` (integer)
  - Returns: Test details including script files and configuration

- **Test Execution**:
  - `blazemeter_execution` with action `read` - Read execution details for scripted tests
  - `blazemeter_execution` with action `list` - List all executions for a test
  - Required args: `execution_id` (integer) or `test_id` (integer)
  - Returns: Execution details and results

### When to Use MCP Tools

- **Test Management**: Manage tests with custom scripts programmatically
- **Script Validation**: Verify test scripts are configured correctly
- **Execution Monitoring**: Monitor execution of scripted tests
- **Automation**: Integrate scripted tests into automation workflows

### Example Workflow

**Managing Scripted Tests**:
1. Use `blazemeter_tests` with action `list` to find tests with custom scripts
2. Use `blazemeter_tests` with action `read` to get test details and script configuration
3. Use `blazemeter_execution` with action `read` to monitor test execution
4. Review execution results for script-related issues

## Reference Files

### Groovy/Beanshell
- **[groovy-beanshell.md](skill-blazemeter-scripting://references/groovy-beanshell.md)**: File Writing

### JMeter Plugins
- **[jmeter-plugins.md](skill-blazemeter-scripting://references/jmeter-plugins.md)**: Random CSV Data Set Config Plugin

### JMeter DSL
- **[jmeter-dsl.md](skill-blazemeter-scripting://references/jmeter-dsl.md)**: JMeter DSL

### API Monitoring Scripting
- **[api-monitoring-scripting.md](skill-blazemeter-scripting://references/api-monitoring-scripting.md)**: Custom Libraries, Included Libraries, Initial Script, Script Engine Overview, Reusable Snippets

## When to Use Each Reference

- **Groovy/Beanshell**: When writing files or custom logic in Performance tests
- **JMeter Plugins**: When using non-standard JMeter plugins
- **JMeter DSL**: When creating JMeter tests as code in Java
- **API Monitoring Scripting**: When writing custom JavaScript for API Monitoring tests

