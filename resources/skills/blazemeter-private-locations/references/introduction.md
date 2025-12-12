# Introduction

## Overview

Private locations are the on-premise solution when you need to test applications or create virtual services behind a firewall. To learn more about the off-premise architecture, see [Cloud vs Private Location](https://help.blazemeter.com/docs/guide/private-locations-vs-cloud.html).

**Use when**: Understanding what Private Locations are, how they work, or when deciding if Private Locations are the right solution for your testing needs.

## How Private Locations Work

With this service, you do not need to make incoming requests. You only install our agent on your on-premise servers. The agent gives your servers a "heartbeat" by sending outgoing requests to BlazeMeter to check if any tests started for the Private location. If any test started, BlazeMeter responds with instructions for these servers. Your load generators then send traffic to your application while sending data back to BlazeMeter, so you have full access to our real-time reporting.

### Key Concepts

- **Private Location** is your on-premise environment, formerly known as a 'harbor'.
- **Agent** - any server on which you install our agent is an agent within a Private location. These are your load generators. Formerly known as a 'ship'.

### Important Considerations

Private locations are self-service machines and require you to maintain and upkeep them on a regular basis.

## Permission Error Message

Depending on what type of BlazeMeter plan you are subscribed to, when you create a new Private Location, you may encounter the error "You don't have the permission to create a private location in this workspace. Please contact your account admin to enable this feature".

### If you are not the account administrator or workspace manager:

- Contact your account administrator or workspace manager to get permission to create a Private location.

### If you are the account administrator or workspace manager:

- This message means that your current subscription plan does not include the Private Locations feature that is limited to enterprise customers.
- To enable the feature, contact [BlazeMeter Support](mailto:support-blazemeter@perforce.com?subject=Enable Private Locations) or your account manager.

## Getting Started

Once you have the Private Location feature available, you can begin the installation of your first Private location. For more information, see [Private Location System Requirements](https://help.blazemeter.com/docs/guide/private-locations-system-requirements.html).

**Note**: Private Locations use an agent-based architecture where the agent sends outgoing requests to BlazeMeter (heartbeat) to check for test instructions. This eliminates the need for incoming firewall rules, making it easier to deploy in secure environments.

## Documentation References

For detailed information about Private Locations introduction, use the BlazeMeter MCP help tools:

**Introduction**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `private-locations-intro`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["private-locations-intro"]}`

