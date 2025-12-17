# Workspaces and Projects Management

## Manage Workspaces and Projects

Manage Workspaces and Projects in BlazeMeter, including adding members, assigning roles, creating projects, and organizing tests and reports.

**Use when**: Managing Workspaces and Projects in BlazeMeter or when adding members, assigning roles, creating projects, and organizing tests and reports.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Workspaces and Projects**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-workspaces-and-projects`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-workspaces-and-projects"]}`

**Related Help IDs**:
- `administration-manage-group.htm` - See [Manage Groups](#administration-manage-groups) section below
- `administration-manage-environment.htm` - See [Manage Environments](#administration-manage-environments) section below

### Workspace Management

Workspaces are containers for projects, tests, and reports. Workspaces divide your account into separate sub-accounts, each with its own distinct set of assets and access controls.

**Workspace Characteristics:**
- Each workspace includes its own tests, reports, projects, shared folders, APM credentials, private locations, and dedicated IPs
- Members can navigate between workspaces but will only see the contents of one workspace at a time, similar to using a badge to enter a room
- A member can be assigned different roles (Manager, Tester, or Viewer) in each workspace they have access to

**Should You Use Multiple Workspaces or Just One?**
- Use multiple workspaces if you want clear boundaries between different asset sets and the ability to assign members different roles across asset sets (for example, Tester in their workspace and Viewer in others)
- Use a single workspace if you want to share all assets across all users
- Usage is tracked at both the workspace and project levels, so either organizational method supports usage tracking goals

Use MCP tools to programmatically manage workspaces:

- **List workspaces**: Use `blazemeter_workspaces` with action `list` to retrieve all workspaces for an account
- **Read workspace**: Use `blazemeter_workspaces` with action `read` to get detailed workspace information including available locations and billing usage
- **Read locations**: Use `blazemeter_workspaces` with action `read_locations` to get location lists for a workspace

### Project Management

Projects organize tests and reports within a workspace. **Projects** are designed to organize tests and reports and track usage within a workspace.

**Project Characteristics:**
- Each test and all of its reports belong to a project
- If a workspace is like a room you enter with a badge, a project is like a rack or whiteboard in that room
- The "All Tests" and "All Reports" lists show tests from all projects within the current workspace
- Selecting a project from the Project drop-down displays a list of tests within that project
- Tests can be moved from one Project to another by choosing "Move this test to..." on its Test Configuration screen

Use MCP tools to manage projects:

- **List projects**: Use `blazemeter_project` with action `list` to retrieve all projects in a workspace
- **Read project**: Use `blazemeter_project` with action `read` to get detailed project information

### Add Members to a Workspace

New members can only be added from within the account that the workspace belongs to; members from outside the account cannot be added. For instructions on adding new users to your account, refer to [How to Invite Additional Users to a BlazeMeter Account](skill-blazemeter-administration://references/workspaces-projects.md).

To add members:

1. Log in to your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings** > **Workspace** > **Members** and select the users to add to the workspace
4. Click the '**Plus**' button
5. Select the user you wish to add and click the **Add** button to confirm

### Assign Workspace Roles

Workspace owners can assign the following roles to members of their workspaces:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. To assign roles, go to **Settings > Workspace > Users**, and edit the user you want
2. Choose the role that you want from the dropdown menu:
   - **Viewer**: Can only view reports, cannot run or edit tests
   - **Tester**: Can create/edit/delete/run tests and reports, projects, APM credentials and view Private Locations, Dedicated IPs and Usage Reports
   - **Manager**: Same access as a Tester, but can also add or remove members from the Workspace, can create or delete alerts, and can create, edit, or delete Private Locations

### Remove Members from a Workspace

As a workspace owner, you can also disable or enable a member's access to a workspace, this is BlazeMeter's equivalent of deleting a user. Once you disable a user, they are removed from the workspace members list. Use the '**Show Disabled**' ON/OFF button to view disabled members.

### Add a New Project

1. Verify that you're in the desired workspace where you'd like to add the project. To switch workspaces, use the dropdown menu in the top-right corner of the screen
2. Click the **Projects** dropdown button, then select **Create New Project**
3. Enter a name for your project and click **Create Project**

### Create a Test in a Project

To create a new test in an existing project, either click **Create Test**, or select the relevant project from the **Projects** dropdown menu in the top-left corner of the screen.

In this example, the project selected is *Guy's Awesome Project*, located within the Second Workspace. This means the new test will be added to *Guy's Awesome Project*, and members of the Second Workspace with the necessary permissions can view, edit, share, or delete the test.

For more information about how to migrate a test between projects within the same workspace, see [Duplicate, Delete, or Move a Performance Test](skill-blazemeter-performance-testing://references/management.md) and [GUI Functional Testing - Overview](skill-blazemeter-functional-testing://references/gui-tests.md).

### Workspace Operations

- **Adding members to workspaces**: See [Add Members to a Workspace](#add-members-to-a-workspace) above
- **Assigning roles**: See [Assign Workspace Roles](#assign-workspace-roles) above
- **Removing members**: See [Remove Members from a Workspace](#remove-members-from-a-workspace) above
- **Creating new projects**: See [Add a New Project](#add-a-new-project) above
- **Organizing tests and reports**: Organize tests and reports within projects
- **Managing workspace settings**: Manage workspace-level settings

### Project Operations

- **Creating projects**: Create new projects within a workspace
- **Creating tests in projects**: To create a new test in an existing project, either click **Create Test**, or select the relevant project from the **Projects** dropdown menu in the top-left corner of the screen
- **Organizing tests by project**: Organize tests by project for better management
- **Moving tests between projects**: Tests can be moved from one Project to another by choosing "Move this test to..." on its Test Configuration screen
- **Managing project-level settings**: Manage project-level settings
- **Viewing project-level reports**: View reports organized by project

---

## Administration How to Change Default Test Location

When you first log in to BlazeMeter, you see the list of tests in your default project, in your default workspace, in your default account. There can be any number of reasons why you may want your initial view after logging in to default to somewhere else. For example, if you have a personal account but have also joined an organization's account (after having been invited to the account), you may want to change your default so that you always see the organization's account when you first login instead of your own account.

**Use when**: Changing the default test location upon login or when configuring default account/workspace/project settings.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration How to Change Default Test Location**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-how-to-change-the-default-test-location`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-how-to-change-the-default-test-location"]}`

### Steps

To change your default view so you always see a specific account upon logging in, follow these steps:

**First, find the Project ID** of what you want to become the new default project, in your new default workspace, in your new default account:

1. Navigate to the Projects menu in the navigation bar
2. Open the project that is to become your new default project
3. Copy the Project ID from the URL shown in your browser navbar: `https://a.blazemeter.com/app/?#/accounts/xxxxxx/workspaces/xxxxxx/projects/xxxxxx/tests`

**Note**: You can also find Project IDs via the API.

**Now you can change your default settings:**

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Navigate to **Personal** > **Personal Settings**. Your view may or may not include the other categories pictured above, depending on your user's permissions level
3. Review the **Default Test Location** configuration
4. Click the pencil icon beside "Default project" to edit it, then enter the Project ID of the project that you want as the default instead
5. Click the checkmark button to confirm the change

**Wondering why you need the Project ID to change the Account ID?** This is because, when you log in, your default view is of your default project. Each workspace has its own default project, and each account has different workspaces. Specifying the Project ID therefore by extension also selects that project's parent workspace (and the account to which it belongs) as the default workspace and account.

### Using MCP Tools

To programmatically identify workspace and project IDs, use BlazeMeter MCP tools:

**List workspaces**:
- Tool: `blazemeter_workspaces`
- Action: `list`
- Required args: `account_id` (integer)
- Optional args: `limit` (1-50, default 10), `offset` (default 0)
- Returns: List of workspaces with workspace IDs

**List projects**:
- Tool: `blazemeter_project`
- Action: `list`
- Required args: `workspace_id` (integer)
- Optional args: `limit` (1-50, default 10), `offset` (default 0)
- Returns: List of projects with project IDs

**Read workspace details**:
- Tool: `blazemeter_workspaces`
- Action: `read`
- Required args: `workspace_id` (integer)
- Returns: Workspace details including available locations and billing usage

**Read project details**:
- Tool: `blazemeter_project`
- Action: `read`
- Required args: `project_id` (integer)
- Returns: Project details including test count

---

## Administration Time Zone Override

Do you collaborate across time zones? Discussing graphs can be challenging (and error prone!) if you have to convert time zones in your head. Let the app do the work!

**Use when**: Configuring time zone override for UI display or when enabling collaboration across time zones with consistent time representation.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Time Zone Override**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-time-zone-override`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-time-zone-override"]}`

### Set the Time Zone Override

Follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Toggle the Time Zone Override feature on
3. Choose the time zone offset from the menu

This Setting will change the Time Zone display only for the current user.

To return to your local time zone, simply toggle the feature back off.

### Benefits

- Consistent time display for all team members
- Easier coordination across time zones
- Standardized reporting timestamps
- Avoid time zone conversion errors when discussing graphs

---

## Administration Managing an Account

Manage BlazeMeter accounts, including inviting users, changing account roles, removing users, adding workspaces, customizing account name and logo, and deleting accounts.

**Use when**: Managing BlazeMeter accounts or when inviting users, changing account roles, removing users, adding workspaces, customizing account name and logo, and deleting accounts.

### Account Management Operations

- **Inviting users**: Add new users to the account. When inviting, you can assign Account roles (Standard, Admin, Billing, User Manager) and initial Workspace Roles (Viewer, Tester, Manager). Invalid email addresses will be rejected. If there is only one Workspace in this Account, the user will be automatically added to that Workspace
- **Changing account roles**: The Account admin/owner can assign the following roles to an Account's user: **Standard** (has no permissions in the Account's managerial levels, the typical end-user), **Billing** (can view/change Billing related settings, for example, credits and servers hours allocations), **Admin** (same as Billing but can also manage users and workspaces), **Owner** (single, same as admin but can also delete the Account). The Owner role is unique - only BlazeMeter Support can change who holds the Owner role
- **Removing users**: Users cannot be deleted; however, disabling a user's access to the Account, for all intents and purposes, has the same effect, as a disabled user will no longer have access, nor will they be visible anymore. When you disable users, they will be removed from the Account's Users list. Use the 'Show Disabled' ON/OFF button to view disabled users
- **Adding workspaces**: Adding new Workspaces is possible only if your plan allows multiple workspaces. Different Workspaces are used to divide teams that work on different independent applications. If you want to share *all* assets across *all* users, use just *one* workspace
- **Customizing account**: As an account owner or manager, you can customize your account name and logo. Setting a custom account logo will also display the logo in all your account's executive summary reports. If undefined, the default BlazeMeter logo will display
- **Deleting accounts**: To delete an account, [open a Support ticket](https://help.blazemeter.com/docs/answers/support-ticket.html)

### Using MCP Tools

Use BlazeMeter MCP tools to programmatically access account information:

**Read account**:
- Tool: `blazemeter_account`
- Action: `read`
- Required args: `account_id` (integer)
- Returns: Account details including AI Consent information

**List accounts**:
- Tool: `blazemeter_account`
- Action: `list`
- Optional args: `limit` (1-50, default 10), `offset` (default 0)
- Returns: List of accounts with account IDs

**Get default account**:
- If you have a project ID, use `blazemeter_project` with action `read` to get project details
- The project response includes workspace information
- Use `blazemeter_workspaces` with action `read` to get workspace details
- The workspace response includes account information

### Account Settings

- Account name and logo customization
- User management and role assignment
- Workspace creation and management
- Account-level security settings

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Managing an Account**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-managing-an-account` (managing an account)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-managing-an-account"]}`

**Workspaces and Projects Management**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `administration-workspaces-and-projects` (workspaces and projects)
  - `administration-workspace-manage-profiles.htm` (manage APM profiles)
  - `administration-manage-group.htm` (manage groups)
  - `administration-manage-environment.htm` (manage environments)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-workspaces-and-projects", "administration-workspace-manage-profiles.htm", "administration-manage-group.htm", "administration-manage-environment.htm"]}`

---

## Administration Manage Environments

As an account owner, you can configure various advanced features and parameters in the **Environment** section of your **Account Settings**. When the options are available, you can use the toggle keys to enable options.

**Use when**: Configuring advanced account-level features and parameters in the Environment section of Account Settings.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Manage Environments**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-manage-environment.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-manage-environment.htm"]}`

### Available Environment Options

The following options are available in the Environment section:

- [JMeter Plugin Manager](#jmeter-plugin-manager)
- [Resource Consumption Alert](#resource-consumption-alert)
- [JMeter Version Auto-Detect](#jmeter-version-auto-detect)
- [Display Response Body in Errors](#display-response-body-in-errors)
- [Account AI Consent](#account-ai-consent)
- [Anomaly Detection](#anomaly-detection)
- [In-App Messaging](#in-app-messaging)

### JMeter Plugin Manager

Enter your local JMeter Plugin Manager address or leave the field empty to use BlazeMeter's default setting. For more information, see [JMeter Plugin Manager](https://www.blazemeter.com/blog/jmeter-plugins-manager).

### Resource Consumption Alert

Set a threshold for the number of engines per test. If a test runs with more engines than defined, an alert is triggered and sent to the specified email address.

### JMeter Version Auto-Detect

As an account admin, you can enable BlazeMeter to detect the JMeter version used by a Taurus YAML JMeter or JMeter file. If the detected version is not available in BlazeMeter's image, Taurus will attempt to download the specified JMeter version. This includes legacy JMeter versions.

**To enable the JMeter Version Auto-Detect functionality:**

1. Go to **Settings** > **Account Settings** > **Environment**
2. Turn on the **JMeter Version Auto-Detect** toggle (deactivated by default)

**Behavior:**
- If Auto-Detect is **disabled**: Only the Latest (5.6.3) and Stable (5.5) JMeter versions are available in the test configuration dropdown
- If Auto-Detect is **enabled**: The dropdown will also include an Auto-Detect option, allowing for automatic selection of the appropriate JMeter version

### Display Response Body in Errors

To display the response body of transactions that fail on the Errors tab in the test report, switch on this option. For more information, see [View the Response Body](skill-blazemeter-performance-testing://references/reporting.md).

### Account AI Consent

The Account AI Consent toggle key lets account owners control AI-related features at the account level. For more information, see [AI Consent](skill-blazemeter-administration://references/ai-consent.md).

**Options:**
- **User-defined**: Allows users to choose whether to enable AI features
- **Agree**: Determines that all users have AI features enabled by default
- **Disagree**: Determines that all users have AI features disabled by default

### Anomaly Detection

This feature identifies and displays performance anomalies across all test runs in the Timeline Report. For more information, see [View Anomalies](skill-blazemeter-performance-testing://references/reporting.md).

### In-App Messaging

Create in-app messages that display at a frequency that you set. Click **+ Add Message** to create your message. When you are finished, click **Save**. You can edit or delete the message by clicking the Edit or Delete icons.

**Display Frequency Options:**
- **Only once**: The in-app message displays only one time. When the user logs in again, the in-app message does not display
- **Every login**: The in-app message displays every time a user logs in
- **Every number of days**: The in-app message displays after the set number of days when the user logs in

---

## Administration Manage Groups

As an account administrator, you can create and manage groups, as well as view users associated with each group.

Groups let you manage user access and permissions on the account level and across workspaces. By leveraging Single Sign-On (SSO) with Active Directory (AD) groups, you can automatically assign roles and workspace permissions to users based on their group memberships.

**Use when**: Managing user groups, configuring SSO-based access control, or when you need to automatically assign roles and workspace permissions based on group memberships.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Manage Groups**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-manage-group.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-manage-group.htm"]}`

### Overview

BlazeMeter offers Role-Based Access Control (RBAC) through SSO groups (groups). This feature allows organizations to define user roles and workspace permissions directly within their own identity provider (IdP) systems. By mapping these internal groups to corresponding roles and workspaces in BlazeMeter, user access is automatically configured upon login, eliminating the need for manual intervention.

**Example**: If a user belongs to the AD group *retail-team-managers*, which is configured to provide access to three workspaces, they automatically receive manager permissions for the provided workspaces.

### Benefits

- **Centralized user management**: Administrators can manage user roles and permissions entirely within their existing IdP, which can help to reduce the need to navigate multiple platforms
- **Automated access provisioning**: New users gain immediate access to the appropriate BlazeMeter resources based on their group memberships, which can help to enhance onboarding efficiency
- **Security compliance**: By leveraging the organization's existing security policies, including multi-factor authentication and audit trails, the integration which can help to ensure consistent enforcement of access controls
- **Simplified role transitions**: Changes in a user's role—such as promotions or department transfers—can be managed by updating group memberships in the IdP, with corresponding permissions in BlazeMeter adjusting automatically

### Workflow

Aligning BlazeMeter groups with IdP groups can help to ensure that user roles and workspace permissions are consistently applied upon login. The following steps are required to enable this integration:

1. **Integration request**: Organizations initiate the process by contacting BlazeMeter support ([support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com)) to set up SSO integration
2. **Group configuration**: Within the organization's IdP, administrators create groups corresponding to required roles and workspace permissions in BlazeMeter
3. **Mapping in BlazeMeter**: These IdP groups are mapped to specific roles and workspaces within BlazeMeter, establishing the required access controls
4. **User assignment**: Users are added to the appropriate groups in the IdP. Upon logging into BlazeMeter, they receive permissions based on their group memberships, with no additional configuration required within BlazeMeter

SSO groups can help organizations to manage both authentication and authorization through their existing identity management systems, thereby promoting efficiency, security, and user experience.

### Prerequisites

- **SSO configuration**: Ensure that SSO is configured between your IdP and BlazeMeter. This step involves setting up the necessary SAML attributes and establishing trust between the two systems. For more information, see [SAML SSO Integration](https://help.blazemeter.com/docs/guide/integrations-saml-sso-integration.html)
- **Group attribute mapping**: Configure your IdP to send group information to BlazeMeter
- **Groups must exist in both BlazeMeter and the IdP** for users to log in. If a group is missing in BlazeMeter, affected users will lose access
- **If no groups match during login**, the user will be removed from all workspaces and permissions
- **Deleting a group in the IdP** does not automatically remove it from BlazeMeter
- **When a user logs in to BlazeMeter via SSO**, BlazeMeter receives the user's group memberships from the IdP. Based on these groups, BlazeMeter assigns the user the predefined account and workspace roles
- **If a user belongs to multiple groups**, BlazeMeter aggregates the permissions, providing the highest level of access assigned

### Create Group

When you add a group, you can assign account roles and workspace permissions.

**Steps:**

1. In **Settings**, navigate to **Account** and click **Groups**
2. Click **Add Group**. The **Add Group** page appears
3. Fill in the following fields:
   - **Group Name**: Enter a name for the group
   - **Account Roles**: Select account-level roles (Standard, Admin, Billing, User Manager)
4. In the **Workspace** section, select one or more workspaces
5. Click **Assign Roles**. You can define the following roles for the selected workspaces:
   - **Viewer**: Can only view reports, cannot run or edit tests. This role is typically assigned to users on the executive level, for example, managers or directors
   - **Tester**: Can create, edit, delete, and run tests and reports, manage projects, and handle APM credentials. Additionally, can view private locations, dedicated IPs, and usage reports. This is the typical role for end users such as testers or developers
   - **Manager**: Same access as a tester but can also add or remove members from the Workspace, can create or delete alerts, and can create, edit, or delete Private Locations. This role is typically assigned to a scrum lead or manager that is responsible for everything that falls under that workspace, including the handling of private locations
6. You can select other workspaces and define different sets of roles. You can assign multiple roles to a group for the same account or workspace
7. Click **Add**

The new group is added to the **Groups** list.

### Filter Groups

To filter your groups, you can select what you would like to filter by:
- **Group Name**
- **Account Roles**
- **Workspace Permissions**

### View Users

To open the list of group users:

1. In the **Groups** list, select the view users icon for the required group
2. The users list opens, showing all users associated with that group

### Edit Group

1. In the **Groups** list, select the edit icon for the required group
2. The **Edit Group** screen opens
3. You can change any of the settings. For more information, see [Create Group](#create-group)
4. When you have finished making changes, click **Save**

### Delete Group

1. In the **Groups** list, select the delete icon for the required group
2. Confirm the deletion

**Note**: Deleting a group in BlazeMeter does not automatically remove it from the IdP. Ensure proper coordination between systems.

### Manage User Access

#### Add Users

To grant a user access to BlazeMeter with specific permissions, add the user to the appropriate group(s) in your IdP. Upon their next login, BlazeMeter will automatically assign the corresponding roles and workspace access.

#### Remove Users

To revoke a user's access, remove the user from the relevant group(s) in your IdP. The next time the user attempts to log in, they will no longer have the associated permissions or access in BlazeMeter.

### Transition Period for Existing Users

Upon enabling SSO-based permissions, there is a transition period during which:

- **Existing users**: Users who previously had access through BlazeMeter's legacy permissions system will retain their current roles until they log in through SSO. You can continue to change their roles in the BlazeMeter user interface
- **New users**: Users logging in for the first time through SSO will receive permissions based solely on their IdP group memberships. You cannot change their roles through the BlazeMeter user interface

### View SSO-Related Roles

#### Account Users

To view account users SSO-related roles:

1. In **Settings**, navigate to **Account** and click **Users**
2. The user list opens. There are two columns that show SSO-related roles:
   - **Group-Based Roles**: Displays the account role assigned through group-based (RBAC) SSO permissions
   - **Basic SSO Roles**: Displays the account role assigned through basic (legacy) SSO settings

#### Workspace Members

To view workspace members SSO-related roles:

1. In **Settings**, navigate to **Workspace** and click **Members**
2. The user list opens. There are two columns that show SSO-related roles:
   - **Group-Based Roles**: Displays the workspace role assigned through group-based (RBAC) SSO permissions
   - **Basic SSO Roles**: Displays the workspace role assigned through basic (legacy) SSO settings

