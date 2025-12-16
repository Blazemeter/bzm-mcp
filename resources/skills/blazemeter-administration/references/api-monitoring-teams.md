# API Monitoring Teams

## Administration API Monitoring Teams

BlazeMeter API Monitoring teams allow you to share your buckets and request data across a group of people. When signing up for BlazeMeter, everyone is given a personal account. You may join an unlimited number of teams which will all be available to you under a single sign in.

**Note**: Currently, API Monitoring team membership is controlled separately from BlazeMeter account and workspace membership. This will become more integrated and streamlined in future releases.

**Use when**: Creating and managing API Monitoring teams or when sharing buckets and request data across groups, inviting members, and managing team ownership.

### API Monitoring Teams Overview

API Monitoring teams are separate from BlazeMeter workspaces and are specific to API Monitoring functionality. Teams enable sharing of buckets, request data, and test configurations across team members.

### Create a Team

To create your first team you can either [create one from scratch](https://www.runscope.com/teams/create) or [upgrade your personal account](https://www.runscope.com/teams/upgrade) to a team account.

**Note**: All team accounts require a paid subscription plan.

**Important**: When you create a team, you become the team owner by default. Team ownership can be transferred to another member at any time, but this action cannot be undone by yourself.

### Invite Team Members

After creating your team you are a team owner by default and can invite people to join it.

Follow these steps:

1. In API Monitoring, click the **Profile and Account Settings** icon in the top right corner
2. Click **Teams & Usage**
3. Select the team you'd like to invite members to from the [Teams list](https://www.runscope.com/teams) and click **Team Members**
4. In the **Invite Team Members** section, enter the email addresses for the people you would like to invite. If they don't already have a BlazeMeter account, they will be able to create one while accepting the invite
5. Click **Send Invites**

### Team Owners vs Members

Every team has one member designated as owner, initially set to the person who created the team. Team owners have a few extra capabilities over regular team members:

- Change the team's subscription plan and update billing information
- View billing transaction history
- Invite/remove team members

All other capabilities (viewing data, making requests, creating buckets) are available to all team members.

As team owner you can transfer ownership of a team to another member at any time. From the team detail page, select the new owner and click 'Change Owner'. **Careful, you won't be able to undo this yourself.**

**Note**: Regular users can also delete and manage team members, provided they have the ["Manage Team Members" and "Modify Team Groups"](https://help.blazemeter.com/docs/guide/api-monitoring-role-based-access-control.html#how-rbac-works) permissions enabled. See [Role-Based Access Control](https://help.blazemeter.com/docs/guide/api-monitoring-role-based-access-control.html) for details.

### Manage Team Members

As an admin or team owner, you can delete and manage the roles and permissions of your team members. See [Role-Based Access Control](skill-blazemeter-api-monitoring://references/management.md) for details.

Regular users can also delete and manage team members, provided they have the ["Manage Team Members" and "Modify Team Groups"](skill-blazemeter-api-monitoring://references/management.md) permissions enabled.

### Bucket Sharing

Teams enable sharing of:
- **Buckets**: Test containers and configurations
- **Request Data**: API request history and data
- **Script Libraries**: Shared JavaScript libraries
- **Test Configurations**: Reusable test setups

### Team Ownership

- **Transfer Ownership**: Current owner can transfer to another member
- **Owner Responsibilities**: Manage team settings and membership
- **Ownership Requirements**: At least one owner required

### Best Practices

- Use descriptive team names
- Assign appropriate roles based on responsibilities
- Regularly review team membership
- Document team purposes and usage
- Clean up unused teams

### Integration with Workspaces

- API Monitoring teams are separate from BlazeMeter workspaces
- Team members can belong to multiple teams
- Teams can span multiple workspaces
- Bucket sharing is team-scoped

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration API Monitoring Teams**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-api-monitoring-teams`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-api-monitoring-teams"]}`

**Related Topics**:
- **API Monitoring Buckets**: `api-monitoring-manage-your-buckets` (Category: `root_category`, Subcategory: `guide`)
- **API Monitoring RBAC**: `api-monitoring-role-based-access-control` (Category: `root_category`, Subcategory: `guide`)
- **API Monitoring Sharing**: `api-monitoring-sharing-test-results` (Category: `root_category`, Subcategory: `guide`)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-manage-your-buckets", "api-monitoring-role-based-access-control", "api-monitoring-sharing-test-results"]}`

