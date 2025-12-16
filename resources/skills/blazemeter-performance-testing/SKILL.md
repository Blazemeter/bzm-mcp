---
name: blazemeter-performance-testing
description: Comprehensive guide for BlazeMeter Performance Testing, including load configuration, reporting, JMeter configuration, Taurus, scenarios, and advanced features. Use when working with Performance tests for (1) Configuring load settings and distribution, (2) Creating and running tests (JMeter, Browser, URL/API, Multi-Test), (3) Analyzing reports and filtering data, (4) Configuring JMeter properties and scenarios, (5) Using Taurus for test configuration, (6) Advanced features (AI Log Analysis, APM Integration, Network Emulation, Mainframe Testing), (7) Troubleshooting test issues, or any other Performance Testing tasks.
---

# BlazeMeter Performance Testing

Comprehensive guide for creating, configuring, and analyzing Performance tests in BlazeMeter.

## Overview

Performance Testing in BlazeMeter supports JMeter, Browser-based, URL/API, and Multi-Test scenarios with comprehensive reporting and analysis capabilities. This skill covers load configuration, test creation, reporting, and advanced features.

## Quick Start

1. **Load Configuration**: Set users, duration, ramp-up, and distribution
2. **Test Creation**: Create JMeter, Browser, URL/API, or Multi-Tests
3. **Reporting**: Analyze results with filtering, comparison, and advanced search
4. **JMeter Configuration**: Configure properties, user properties, and live remote control
5. **Taurus**: Use Taurus YAML for test configuration
6. **Advanced Features**: Leverage AI Log Analysis, APM Integration, Network Emulation
7. **Troubleshooting**: Resolve test failures and performance issues

## MCP Tools Integration

Performance tests are managed through the BlazeMeter UI, but you can use MCP tools to manage tests, executions, and results:

### Available MCP Tools

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details including performance test configuration
  - `blazemeter_tests` with action `list` - List all tests in a project
  - `blazemeter_tests` with action `create` - Create new performance tests
  - `blazemeter_tests` with action `configure_load` - Configure load settings (users, duration, ramp-up)
  - `blazemeter_tests` with action `configure_locations` - Configure location distribution
  - Required args: `test_id` (integer) or `project_id` (integer)
  - Returns: Test details including configuration

- **Test Execution**:
  - `blazemeter_execution` with action `start` - Start performance test execution
  - `blazemeter_execution` with action `read` - Read execution details and results
  - `blazemeter_execution` with action `list` - List all executions for a test
  - `blazemeter_execution` with action `read_summary` - Get execution summary report
  - `blazemeter_execution` with action `read_errors` - Get error report
  - `blazemeter_execution` with action `read_request_stats` - Get request statistics report
  - Required args: `test_id` (integer) or `execution_id` (integer)
  - Returns: Execution details, results, and reports

### When to Use MCP Tools

- **Test Management**: Manage performance tests programmatically
- **Load Configuration**: Configure load settings via API
- **Execution Control**: Start and monitor test executions
- **Results Analysis**: Retrieve and analyze test results
- **Automation**: Integrate performance testing into automation workflows
- **CI/CD Integration**: Integrate tests into CI/CD pipelines

### Example Workflows

**Creating and Running a Performance Test**:
1. Use `blazemeter_tests` with action `create` to create a new test
2. Use `blazemeter_tests` with action `configure_load` to set load parameters
3. Use `blazemeter_tests` with action `configure_locations` to set location distribution
4. Use `blazemeter_execution` with action `start` to start test execution
5. Use `blazemeter_execution` with action `read_summary` to get results

**Analyzing Test Results**:
1. Use `blazemeter_execution` with action `list` to find executions
2. Use `blazemeter_execution` with action `read_summary` to get summary
3. Use `blazemeter_execution` with action `read_errors` to analyze errors
4. Use `blazemeter_execution` with action `read_request_stats` to get detailed statistics

## Reference Files

### Load Configuration
- **[load-configuration.md](skill-blazemeter-performance-testing://references/load-configuration.md)**: Load Configuration, Load Distribution

### Reporting
- **[reporting.md](skill-blazemeter-performance-testing://references/reporting.md)**: Filter Report Data, Compare Reports, Manage Tags, Restore Archived Report, Share Reports, Advanced Search, Intro to Reporting, Monitoring and Post-Test Analysis, KPIs Purpose

### Scenarios
- **[scenarios.md](skill-blazemeter-performance-testing://references/scenarios.md)**: Scenario Definition, Run Test, Stop Test, Configure Ultimate Thread Group Scenario, CSV Split Distribute Engines, Schedule Test

### JMeter Configuration
- **[jmeter-configuration.md](skill-blazemeter-performance-testing://references/jmeter-configuration.md)**: JMeter Properties, JMeter User Properties, Live Remote Control for JMeter Properties, JMeter Auto Correlation Rules

### Taurus
- **[taurus.md](skill-blazemeter-performance-testing://references/taurus.md)**: Taurus Calibration, Configure Engines, Shared Folders with Taurus, Create Taurus Dedicated IP, Test Data with Taurus Scripts

### Advanced Features
- **[advanced-features.md](skill-blazemeter-performance-testing://references/advanced-features.md)**: AI Log Analysis Report, Add Users Dynamically, APM Integration, Create Browser Test, Create JMeter Test, Create Multi Test, Create URL/API Test, Dedicated IPs, DNS Override, EUX Monitoring, Mainframe Testing (RTE), Network Emulation, Shared Folders, Use Test Data in Testing, More About Performance Testing, Checklist, Testing Process

### Troubleshooting
- **[troubleshooting.md](skill-blazemeter-performance-testing://references/troubleshooting.md)**: Test Won't Start Troubleshooting, High Response Time, 500 Response, Partial Load, Selenium vs JMeter Load Testing, Test Works Locally but Not in BlazeMeter, Taurus Test Works Locally but Not in BlazeMeter, Debug Test Multiple Scenarios

## When to Use Each Reference

- **Load Configuration**: When setting up users, duration, ramp-up, or geographic distribution
- **Reporting**: When analyzing test results, comparing reports, or managing tags
- **Scenarios**: When configuring test scenarios, running tests, or scheduling executions
- **JMeter Configuration**: When configuring JMeter properties, user properties, or correlation rules
- **Taurus**: When using Taurus YAML for test configuration and calibration
- **Advanced Features**: When working with browser tests, multi-tests, APM integration, or specialized testing scenarios
- **Troubleshooting**: When diagnosing test failures or performance issues

