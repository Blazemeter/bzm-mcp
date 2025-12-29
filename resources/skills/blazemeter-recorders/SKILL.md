---
name: blazemeter-recorders
description: Comprehensive guide for BlazeMeter Recorders, including Chrome Extension and Proxy Recorder. Use when working with recorders for (1) Recording tests with Chrome Extension, (2) Creating and using Proxy Recorder, (3) Configuring browsers and devices for proxy recording, (4) Setting port ranges for proxy recorder, or any other recording tasks.
---

# BlazeMeter Recorders

Comprehensive guide for recording performance and functional tests in BlazeMeter.

## Overview

BlazeMeter provides two main recording options: Chrome Extension for browser-based recording and Proxy Recorder for mobile and web app recording. This skill covers both recording methods and their configuration.

## Quick Start

1. **Chrome Extension**: Record tests directly from Chrome browser
2. **Proxy Recorder**: Record mobile and web app traffic via proxy
3. **Configuration**: Configure browsers and devices for proxy recording

## MCP Tools Integration

While recording is primarily done through browser extensions and proxy configuration, you can use BlazeMeter MCP tools to manage tests created from recordings:

### Available MCP Tools

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details for tests created from recordings
  - `blazemeter_tests` with action `list` - List all tests in a project, including recorded tests
  - Required args: `test_id` (integer) or `project_id` (integer)
  - Returns: Test details including configuration and scripts

- **Test Execution**:
  - `blazemeter_execution` with action `read` - Read execution details for recorded tests
  - `blazemeter_execution` with action `list` - List all executions for a recorded test
  - Required args: `execution_id` (integer) or `test_id` (integer)
  - Returns: Execution details and results

### When to Use MCP Tools

- **Test Management**: Manage tests created from recordings programmatically
- **Execution Monitoring**: Monitor execution of recorded tests
- **Automation**: Integrate recorded tests into automation workflows

### Example Workflow

**Managing Recorded Tests**:
1. Record test using Chrome Extension or Proxy Recorder
2. Export recorded script to BlazeMeter
3. Use `blazemeter_tests` with action `list` to find the created test
4. Use `blazemeter_tests` with action `read` to get test details
5. Use `blazemeter_execution` to monitor test execution

## Reference Files

### Chrome Extension
- **[chrome-extension.md](skill-blazemeter-recorders://references/chrome-extension.md)**: Record, Changelog

### Proxy Recorder
- **[proxy-recorder.md](skill-blazemeter-recorders://references/proxy-recorder.md)**: Creating the Proxy Recorder, Recording Your Session, Configure Chrome for Proxy Recording, Configure Firefox for Proxy Recording, Configure Apple Devices for Proxy Recording, Configure Android Devices for Proxy Recording, Using the Other Certificate, Setting Port Range on Your Agent

## When to Use Each Reference

- **Chrome Extension**: When recording browser-based tests directly from Chrome
- **Proxy Recorder**: When recording mobile apps or web apps via proxy, or when configuring browsers/devices for proxy recording

