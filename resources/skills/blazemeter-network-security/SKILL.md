---
name: blazemeter-network-security
description: Comprehensive guide for BlazeMeter Network & Security, including allowlisting, DNS configuration, and security best practices. Use when working with network and security for (1) Configuring allowlists for BlazeMeter engines and infrastructure, (2) Disabling DNS caching, (3) Implementing security best practices for API Monitoring, or any other network and security tasks.
---

# BlazeMeter Network & Security

Comprehensive guide for network configuration and security in BlazeMeter.

## Overview

Network & Security covers allowlisting BlazeMeter infrastructure, DNS configuration, and security best practices. This skill helps configure firewall rules and secure test execution. Network configuration is essential for ensuring BlazeMeter can communicate with your application servers and for working from behind corporate firewalls.

## Quick Start

1. **Allowlisting**: Configure firewall rules for BlazeMeter engines and infrastructure
2. **DNS**: Configure DNS caching settings for immediate DNS changes
3. **Security**: Implement security best practices for API Monitoring tests

## MCP Tools Integration

While network and security configuration is primarily done through UI and firewall settings, you can use BlazeMeter MCP tools to access workspace and location information that may be relevant for network configuration:

### Available MCP Tools

- **Workspace Information**: 
  - `blazemeter_workspaces` with action `read` - Read workspace details including location information
  - `blazemeter_workspaces` with action `read_locations` - Get location lists for a workspace (filter by purpose: load, functional, grid, mock)
  - Required args: `workspace_id` (integer)
  - Returns: Workspace details with location information that can help identify which IP ranges to allowlist

### When to Use MCP Tools

- **Location Discovery**: Use MCP tools to identify which locations your tests use, helping determine which IP ranges to allowlist
- **Automation**: Integrate location information into automation scripts for firewall configuration
- **Documentation**: Retrieve location information for network configuration documentation

### Example Workflow

**Getting Location Information for Allowlisting**:
1. Use `blazemeter_workspaces` with action `read_locations` to get location lists
2. Filter by purpose (load, functional, grid, mock) to identify test execution locations
3. Use location information to determine which IP ranges need to be allowlisted
4. Configure firewall rules based on location requirements

## Reference Files

### Allowlisting
- **[allowlisting.md](skill-blazemeter-network-security://references/allowlisting.md)**: Allowlisting BlazeMeter Engines, Allowlisting BlazeMeter Behind Firewall, API Monitoring IP Addresses Allowlisting

### DNS
- **[dns.md](skill-blazemeter-network-security://references/dns.md)**: Disable DNS Caching

### Security
- **[security.md](skill-blazemeter-network-security://references/security.md)**: API Monitoring Security

## When to Use Each Reference

- **Allowlisting**: When configuring firewall rules for BlazeMeter cloud engines, infrastructure, or Private Locations
- **DNS**: When configuring DNS caching for immediate DNS changes or failover testing
- **Security**: When implementing security best practices for API Monitoring tests

