---
name: blazemeter-getting-started
description: Getting started guides for BlazeMeter, including onboarding, migration guides, continuous testing journey, glossary, and mobile testing. Use when getting started with BlazeMeter for (1) Navigating BlazeMeter University onboarding, (2) Migrating from Runscope or JMeter, (3) Understanding the continuous testing journey, (4) Referencing BlazeMeter terminology, (5) Testing mobile sites and apps, or any other getting started tasks.
---

# BlazeMeter Getting Started

Getting started guides and resources for new BlazeMeter users.

## Overview

Getting Started covers onboarding, migration guides, terminology, and mobile testing. This skill helps new users understand BlazeMeter and transition from other tools.

## Quick Start

1. **Onboarding**: Navigate BlazeMeter University
2. **Migration**: Transition from Runscope or JMeter
3. **Journey**: Understand the continuous testing journey
4. **Glossary**: Reference BlazeMeter terminology
5. **Mobile**: Test mobile sites and apps

## MCP Tools Integration

Getting started with BlazeMeter involves understanding the platform structure. You can use BlazeMeter MCP tools to explore your account, workspaces, and projects:

### Available MCP Tools

- **User Information**: 
  - `blazemeter_user` with action `read_user` - Read current user information
  - Returns: User details including default account, workspace, and project

- **Account Exploration**: 
  - `blazemeter_account` with action `read` - Read account information
  - `blazemeter_account` with action `list` - List all accessible accounts
  - Required args: `account_id` (integer) for read action

- **Workspace Exploration**: 
  - `blazemeter_workspaces` with action `read` - Read workspace details
  - `blazemeter_workspaces` with action `list` - List all workspaces in an account
  - Required args: `workspace_id` (integer) for read action, `account_id` (integer) for list action

- **Project Exploration**: 
  - `blazemeter_project` with action `read` - Read project information
  - `blazemeter_project` with action `list` - List all projects in a workspace
  - Required args: `project_id` (integer) for read action, `workspace_id` (integer) for list action

### When to Use MCP Tools

- **Account Setup**: Explore your account structure when getting started
- **Workspace Navigation**: Understand workspace organization
- **Project Discovery**: Discover existing projects and tests
- **Learning**: Use tools to learn about BlazeMeter structure

### Example Workflow

**Exploring Your BlazeMeter Account**:
1. Use `blazemeter_user` with action `read_user` to get your default account, workspace, and project
2. Use `blazemeter_workspaces` with action `list` to see all workspaces in your account
3. Use `blazemeter_project` with action `list` to see all projects in a workspace
4. Use `blazemeter_tests` with action `list` to see all tests in a project

## Reference Files

### Getting Started
- **[getting-started.md](skill-blazemeter-getting-started://references/getting-started.md)**: Getting Started with BlazeMeter - Creating Your Account, The Welcome Screen, Drop-Down Menus, Navigation Bar, Creating Your First Test

### Onboarding
- **[onboarding.md](skill-blazemeter-getting-started://references/onboarding.md)**: BlazeMeter University Onboarding FAQ

### Migration
- **[migration.md](skill-blazemeter-getting-started://references/migration.md)**: BlazeMeter for Runscope Users, BlazeMeter for People Who Know JMeter, BlazeMeter Updates for BlazeMeter Users

### Journey
- **[journey.md](skill-blazemeter-getting-started://references/journey.md)**: Continuous Testing Journey

### Glossary
- **[glossary.md](skill-blazemeter-getting-started://references/glossary.md)**: Glossary

### Mobile
- **[mobile.md](skill-blazemeter-getting-started://references/mobile.md)**: Testing Mobile Sites and Apps

## When to Use Each Reference

- **Getting Started**: When getting started with BlazeMeter, creating your account, navigating the interface, or creating your first test
- **Onboarding**: When navigating BlazeMeter University onboarding process
- **Migration**: When transitioning from Runscope, JMeter, or understanding BlazeMeter updates
- **Journey**: When understanding the continuous testing journey
- **Glossary**: When referencing BlazeMeter terminology
- **Mobile**: When testing mobile sites and apps

