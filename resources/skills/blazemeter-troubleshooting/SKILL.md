---
name: blazemeter-troubleshooting
description: Comprehensive troubleshooting guide for BlazeMeter, covering API Monitoring, Performance Testing, general issues, integrations, and security. Use when troubleshooting for (1) API Monitoring issues (Radar Agent auth, SSL certificates, debug tests), (2) Performance Testing issues (high response time, 500 errors, partial load, tests not starting), (3) General issues (delete non-empty project, forbidden domains, Chrome Extension export failures), (4) Integration issues (New Relic reporting), (5) Security issues (Apache Log4j2 vulnerability), (6) Support requests and tickets, or any other troubleshooting tasks.
---

# BlazeMeter Troubleshooting

Comprehensive troubleshooting guide for resolving issues in BlazeMeter.

## Overview

This skill covers troubleshooting for API Monitoring, Performance Testing, general issues, integrations, and security. It includes diagnostic steps, common solutions, and support resources. Effective troubleshooting requires systematic diagnosis and understanding of common issues and their solutions.

## Quick Start

1. **Identify the issue**: Determine if it's API Monitoring, Performance Testing, or general
2. **Check relevant reference**: Review the appropriate troubleshooting guide
3. **Apply solutions**: Follow diagnostic steps and solutions
4. **Contact support**: If issues persist, use support resources

## MCP Tools Integration

While troubleshooting is primarily done through UI and logs, you can use BlazeMeter MCP tools to access test execution information and results that may help diagnose issues:

### Available MCP Tools

- **Test Execution Information**: 
  - `blazemeter_execution` with action `read` - Read test execution details and status
  - `blazemeter_execution` with action `list` - List all executions for a test
  - Required args: `execution_id` (integer) or `test_id` (integer)
  - Returns: Execution details including status, errors, and results

- **Test Information**:
  - `blazemeter_tests` with action `read` - Read test details and configuration
  - Required args: `test_id` (integer)
  - Returns: Test details including configuration that may help identify issues

### When to Use MCP Tools

- **Execution Analysis**: Use MCP tools to programmatically retrieve execution details and errors
- **Automation**: Integrate troubleshooting information into automation scripts
- **Monitoring**: Monitor test execution status and errors programmatically

### Example Workflow

**Getting Execution Details for Troubleshooting**:
1. Use `blazemeter_execution` with action `list` to get execution IDs for a test
2. Use `blazemeter_execution` with action `read` to get detailed execution information
3. Review execution status, errors, and results to identify issues
4. Use this information to diagnose and resolve problems

## Reference Files

### API Monitoring
- **[api-monitoring.md](skill-blazemeter-troubleshooting://references/api-monitoring.md)**: Radar Agent Auth Fail, SSL Certificate, Debug Test

### Performance
- **[performance.md](skill-blazemeter-troubleshooting://references/performance.md)**: High Response Time, 500 Response, Debug Test Multiple Scenarios, Partial Load, Selenium vs JMeter Load Testing, Test Works Locally but Not in BlazeMeter, Taurus Test Works Locally but Not in BlazeMeter, Test Won't Start

### General
- **[general.md](skill-blazemeter-troubleshooting://references/general.md)**: Delete Non-Empty Project, Forbidden Domains, Chrome Extension Export JMX Failed, Support Feature Requests Submit, Support Feature Requests Track, Support Ticket Management

### Integrations
- **[integrations.md](skill-blazemeter-troubleshooting://references/integrations.md)**: Integration New Relic Reporting

### Security
- **[security.md](skill-blazemeter-troubleshooting://references/security.md)**: Apache Log4j2 Vulnerability

## When to Use Each Reference

- **API Monitoring**: When troubleshooting API Monitoring test failures, Radar Agent issues, or SSL certificate problems
- **Performance**: When troubleshooting Performance test failures, high response times, or execution issues
- **General**: When troubleshooting general issues, project deletion, or support requests
- **Integrations**: When troubleshooting integration issues
- **Security**: When addressing security vulnerabilities

