---
name: blazemeter-private-locations
description: Comprehensive guide for BlazeMeter Private Locations, including Radar Agent, installation (Docker, Kubernetes, Helm), configuration, management, and troubleshooting. Use when working with Private Locations for (1) Installing agents (Docker, Kubernetes, Helm Chart), (2) Configuring Radar Agent for API Monitoring, (3) Setting up environment variables and certificates, (4) Managing private locations and agents, (5) Troubleshooting installation and connectivity issues, or any other Private Location tasks.
---

# BlazeMeter Private Locations

Comprehensive guide for installing, configuring, and managing Private Locations in BlazeMeter.

## Overview

Private Locations enable running BlazeMeter tests from your own infrastructure, providing control over test execution environment and network access. This skill covers Radar Agent, installation methods, configuration, and troubleshooting.

## Quick Start

1. **Installation**: Choose Docker, Kubernetes, or Helm Chart installation
2. **Radar Agent**: Configure for API Monitoring private API access
3. **Configuration**: Set environment variables, certificates, and proxy settings
4. **Management**: Create, use, and manage private locations and agents
5. **Troubleshooting**: Resolve installation, connectivity, and resource issues

## MCP Tools Integration

Private Locations are managed through the BlazeMeter UI, but you can use MCP tools to manage tests that use private locations:

### Available MCP Tools

- **Test Management**: 
  - `blazemeter_tests` with action `read` - Read test details including private location configuration
  - `blazemeter_tests` with action `list` - List all tests in a project
  - Required args: `test_id` (integer) or `project_id` (integer)
  - Returns: Test details including private location selection

- **Test Execution**:
  - `blazemeter_execution` with action `read` - Read execution details for tests using private locations
  - `blazemeter_execution` with action `list` - List all executions for a test
  - Required args: `execution_id` (integer) or `test_id` (integer)
  - Returns: Execution details and results

### When to Use MCP Tools

- **Test Management**: Manage tests that use private locations programmatically
- **Execution Monitoring**: Monitor test executions on private locations
- **Automation**: Integrate private location testing into automation workflows
- **Reporting**: Generate reports on tests using private locations

### Example Workflow

**Managing Tests with Private Locations**:
1. Use `blazemeter_tests` with action `list` to find tests using private locations
2. Use `blazemeter_tests` with action `read` to get test details and private location configuration
3. Use `blazemeter_execution` with action `read` to monitor test execution
4. Review execution results to verify private location usage

## Reference Files

### Introduction
- **[introduction.md](skill-blazemeter-private-locations://references/introduction.md)**: Overview of Private Locations, How Private Locations Work, Key Concepts (Private Location, Agent), Important Considerations, Permission Error Messages, Getting Started

### Radar Agent
- **[radar-agent.md](skill-blazemeter-private-locations://references/radar-agent.md)**: Overview, Changelog, Connection Errors, SSO Login Error, HTTP/HTTPS Proxy Setup, High Availability/Failover, Availability Issues, Remote Agent Expired, Auto-Restart on Linux, HTTPS Common Name in X509 Certificates, Run as Container, Run as Service/Daemon, Harbor ID and Ship ID, Manual Update of Images, RSS Subscription for Image Updates

### Installation
- **[installation.md](skill-blazemeter-private-locations://references/installation.md)**: Install Agent for Docker, Install Agent for Kubernetes, Install Agent for Kubernetes for Mock Services, Install Agent Helm Chart, System Requirements, Manual Kubernetes Agent Installation, Upgrade from Legacy Supervisor Ship

### Configuration
- **[configuration.md](skill-blazemeter-private-locations://references/configuration.md)**: Environment Variables, Enable Auto-Update for Running Containers, Configure Agents to Use Corporate Proxy, Configure Docker Installation to Use CA Bundle, Configure Kubernetes Agent to Use CA Bundle, Bring Your Own Certificate Mock Services, OpenShift Support, Supported SSL CA Certificates, Internal Repository, Configure Crane Agent to Ensure Mock Service Deployed is Reachable

### Management
- **[management.md](skill-blazemeter-private-locations://references/management.md)**: VS Cloud, Create, Use, Install Agent, Regenerate Agent, Remove Agent, Enable Download Agent Log

### Troubleshooting
- **[troubleshooting.md](skill-blazemeter-private-locations://references/troubleshooting.md)**: Handle Network Issues on OPL Machines Docker Installation, Check for Connectivity from Container to BlazeMeter API Server, Where to Find Agent Logs, Overcome Container Storage Limitation, Image Scan Requirements, Resolve Missing Image Tag Docker Location, Resolve Forbidden Not Enough Resources Error

## When to Use Each Reference

- **Introduction**: When understanding what Private Locations are, how they work, or when deciding if Private Locations are the right solution for your testing needs
- **Radar Agent**: When configuring API Monitoring agents for private API access
- **Installation**: When installing or upgrading private location agents
- **Configuration**: When setting up environment variables, certificates, proxies, or auto-updates
- **Management**: When creating, using, or managing private locations and agents
- **Troubleshooting**: When diagnosing installation, connectivity, or resource issues

