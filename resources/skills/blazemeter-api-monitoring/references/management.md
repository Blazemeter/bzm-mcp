# API Monitoring Management

## Teams

Your account is organized into Teams. You can belong to more than one team.

**Use when**: Managing API Monitoring teams, configuring team settings, or managing team members, roles, and permissions.

### View Your Teams

Follow these steps:

1. Log in to BlazeMeter and navigate to the **API Monitoring** tab
2. Click the **Profile and Account Settings** icon in the top right corner
3. Click **Teams & Usage**. The **Teams & Usage** page opens

You can see all the teams within the account. These are all the teams that you are a part of. For each team, you can see more details, such as:
- Plan type
- Number of team members
- Number of buckets
- Usage data

### Manage Your Team Settings

For each Team, there is a menu on the left side. Follow these steps:

1. Click **Setting & Usage** to view your plan usage, change your plan name, and more
2. Click **Team Members** to change the team owner, view and invite team members or add new team groups
3. Click **Roles and Permissions** to manage user roles
4. Click **Connected Services** to connect to 3rd party services to trigger and respond to API test runs
5. Click **Script Library** to upload a library available for use within the Environment
6. Click **File Library** to upload files

### Overview

Teams in API Monitoring provide organizational structure for managing tests, members, and resources. Teams enable:
- Member management and collaboration
- Role-based access control
- Shared resources (libraries, secrets, files)
- Team-level settings and configuration
- Connected services integration

### Best Practices

- Organize teams by project or functional area
- Use appropriate roles and permissions
- Regularly review team membership
- Document team structure and purpose

---

## Manage AI Consent in API Monitoring

AI-assisted features in API Monitoring require explicit consent from the team owner before they can be used. By default, AI features are **disabled** and administrators must opt in to enable them.

**Use when**: Enabling or disabling AI features in API Monitoring, managing team-level AI consent settings, or understanding AI consent requirements.

### Enabling or Disabling AI Features

To enable or disable AI features:

1. Go to **Account Settings > Teams & Usage > Settings & Usage > Team AI Consent**
2. Enable or disable AI features by choosing **Agree** or **Disagree**
3. Click **Save Changes** to apply the update

### Who Can Manage AI Consent?

AI Consent can be managed by users with the 'Change Team Settings' permission. By default, only Team Owners and Administrators (protected roles) can modify AI Consent settings.

### Important Considerations

- When AI features are disabled, team members will not be able to access AI-assisted script generation
- Consent settings apply at the team level and affect all users within the team
- Changes to AI Consent take effect immediately upon saving

For more details on AI policies, refer to the Perforce [Generative AI Policy](https://www.perforce.com/generative-ai-policy).

### Documentation References

For detailed information about managing AI consent in API Monitoring, use the BlazeMeter MCP help tools:

**Manage AI Consent in API Monitoring**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-ai-consent`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-ai-consent"]}`

---

## Making Use of Your API Monitoring Trial Plan

When you sign up for a BlazeMeter account, you will be given a 14-day free trial to discover all functions that the BlazeMeter platform has to offer.

**Use when**: Understanding trial plan features, comparing trial vs free plan, or planning for post-trial period.

### Trial Plan Features

Specifically for API Monitoring, the Trial plan comes with a number of paid and/or Enterprise-grade features. Note that a number of these features will be disabled at the end of your trial period.

### Trial vs Free Plan Comparison

| Feature | Trial plan | Free plan | What happens after trial period |
|---------|------------|-----------|--------------------------------|
| Number of requests | 100,000 | 25,000 | Reduction in request limit per billing period |
| Number of team members | 6 | 1 | Team members (except team owner) can no longer create tests |
| Number of buckets | 10 | 5 | While existing buckets will still be available, you cannot add or create more buckets |
| Scheduled tests | Available | Not available | Scheduled tests will not run after reaching the maximum request limit (25,000) |
| Trigger URLs | Available | Not available | Needs a qualifying plan |
| Test revisions | Available | Not available | Needs a qualifying plan |
| Client certificates | Available | Not available | Needs a qualifying plan |
| On-premises Radar Agent | Available (19 locations) | Limited (8 locations) | For more information on available locations, see [Global Locations](skill-blazemeter-api-monitoring://references/configuration.md) |
| Detailed request/response timings | Available | Not available | Needs a qualifying plan |
| Custom script libraries and snippets | Available | Not available | File library, scripts and snippets options will no longer be available |

### Documentation References

For detailed information about API Monitoring trial plans, use the BlazeMeter MCP help tools:

**Making Use of Your API Monitoring Trial Plan**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-making-use-of-your-api-monitoring-trial-plan`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-making-use-of-your-api-monitoring-trial-plan"]}`

---

## Buckets

Your account is organized into Teams and Buckets. Buckets are a way of organizing your tests into logical groupings. Each bucket can contain multiple tests.

**Use when**: Creating, managing, or organizing buckets in API Monitoring or configuring concurrent test limits and bucket-level notifications.

### Create a New Bucket in Your Team

Follow these steps:

1. Log in to BlazeMeter and navigate to the **API Monitoring** tab
2. Click **Tests**. You are taken to your dashboard
3. Click the Bucket drop-down menu on the left side next to **Tests**. The list shows all your Teams and Buckets within the Teams. You can also filter by Bucket name or a Key
4. Click **Create Bucket** at the bottom of the list to create a new bucket. You will be taken to a **Create Bucket** page
5. Select the Team to add the bucket to
6. Name the Bucket
7. *Optional*: Enable the **Create as Private Bucket** option to restrict view and access to assigned users only
8. *Optional*: Enable the **Bucket name must be unique** option to prevent duplicate bucket names
9. Click **Create Bucket**

### Manage Concurrent Tests in a Bucket

As you start creating more tests in your buckets, there are certain limits that are good to keep in mind when creating and organizing your buckets and tests.

Currently, our buckets have certain limits when running a high number of tests, which is based on whether your team is using cloud locations and/or On-premise Radar Agents:

- **200 tests can be simultaneously running per cloud location** (example: US Virginia) per bucket
- **200 tests can be simultaneously running amongst all on-premise Radar Agents** (example: multiple tests running from 10 different agents) in a bucket

This is true for tests which are running or being executed concurrently. If you go over these limits, any additional test runs will be added to a queue, and will be executed as soon as the number of concurrent tests is less than 200. This does increase the chances of tests failing for taking more than 10 minutes to execute, which is the system limit for the execution time of a test.

**Example Scenarios:**

- **Scenario 1**: If you have 1 bucket with 250 tests in it, only one cloud location enabled (US Virginia), and every test is scheduled to run every minute, 200 of those tests will start running. The remaining 50 tests will be added to a queue, and as soon as the initial 200 tests finish running the remaining tests will start being executed. If your tests are long-running tests for any reason, this can lead to the queues in the system getting bigger, and that could lead to tests expiring because of timeout issues.

- **Scenario 2**: If you have 1 bucket with 200 tests in it, each test has two cloud locations enabled (US Virginia and US Illinois), and every test is scheduled to run every minute, since each test has two cloud locations, every minute you'll have 400 tests running concurrently. But since each cloud location will only have a maximum of 200 tests running concurrently, as long as your tests finish running in under a minute, you shouldn't see any issues.

- **Scenario 3**: If you have 1 bucket with 100 tests in it, and each test has three Radar Agent locations, and every test is scheduled to run every minute, since there are 3 locations, every minute 200 tests will start running among the 3 different agents, while 100 tests will be added to the queue and wait for the initial tests to be completed before they can start running. On-premise agents work differently than our public locations. Even though in this scenario there are 3 separate agents representing 3 locations in your environment, they can still only run a maximum of 200 tests at the same time.

To avoid potential issues with your tests such as delays or expiration, we recommend:

- Keeping the number of tests in a bucket to less than 150
- Running your tests from [multiple cloud locations](https://help.blazemeter.com/docs/guide/api-monitoring-global-locations.html)
- Splitting up tests into multiple buckets. For more information on how to move one or more tests to a different bucket, see [Move a Test to a Different Bucket](https://help.blazemeter.com/docs/guide/api-monitoring-manage-your-buckets.html#h_01FK4SC198EDKP27QZY81SV5K6)
- Running your tests from multiple cloud locations. Set a different location for one or more tests. For more information, see **Select Test Locations** in [Global Locations](https://help.blazemeter.com/docs/guide/api-monitoring-global-locations.html)
- Adjusting the [schedule](https://help.blazemeter.com/docs/guide/api-monitoring-scheduling-test-runs.html) of your tests to minimize the number of tests running concurrently

For each bucket with locations that are running greater than 85% of the maximum limit for concurrent tests per location per bucket, a warning message indicating the location name and the percentage of utilization of test concurrency is displayed on the dashboard for that bucket.

### Manage Bucket-Level Tests and Notifications

You can run bucket-level tests through the UI or via the Bucket Trigger URL:

- **Run All Tests in Dashboard**: Use the **Run All Tests** button in your bucket's dashboard to execute all tests grouped under that bucket. This option is best for on-demand, manual testing initiated through the web interface
- **Bucket Trigger URL (API)**: Each bucket is assigned a unique Trigger URL, which allows you to initiate a bucket-level test programmatically. This is ideal for integrating test execution into CI/CD pipelines, external monitoring tools, or custom automation scripts. You can initiate the call using tools like curl or as part of a webhook from another service. For more information on Trigger URLs, see Build/Deployment Integration

You can also set up email and third-party app notifications for bucket-level tests within your Bucket Settings.

To configure bucket-level email and integrations settings:

1. Navigate to **Bucket Settings**
2. Under *Email Notifications*, choose whether to notify all members of the team, or select individual members
3. Under *Integrations Notifications*, use the toggle to enable or disable integrations with third-party services. Currently supported apps are Microsoft Teams and Slack

### Move a Test to a Different Bucket

Follow these steps:

1. Log in to BlazeMeter and navigate to the **API Monitoring** tab
2. Click **Tests**. You are taken to your dashboard
3. Click **More...** to expand the menu on the left side and click **Settings**
4. Scroll down to the **Move Test** section
5. Select a Bucket that you want to move the test to and click **Move Test**

### Bucket Utilization API

We have enhanced the [Bucket Detail API](https://help.blazemeter.com/apidocs/api-monitoring/buckets_detail.htm) to also list the percentage of concurrent tests running in each location compared to the limit of 200 tests per location per bucket. The API can be called with the **list_utilizations_gt** parameter that accepts a number (integer value) from 1 to 100 as follows:

```
v1/buckets/<bucket_key>?list_utilizations_gt=<value>
```

Example: `api.runscope.com/v1/buckets/<bucket_key>?list_utilizations_gt=80`

The API output will show locations that exceeded the threshold value with their utilization percentages. The API output for threshold-percentage=80 with utilization will look like the following example:

```json
{
  "data": {
    "auth_token": null,
    "default": false,
    "key": "ov2f2tq1floq",
    "name": "Mobile Apps",
    "team": {
      "name": "Mobile Team",
      "uuid": "7a7a0917-91d7-43ef-b8f4-fe31762167e0"
    },
    "verify_ssl": true,
    "locations_utilization_%": {
      "remote": 82,
      "us california": 86,
      "us iowa": 90
    }
  },
  "meta": {
    "status": "success"
  }
}
```

You can see that three locations exceeded the threshold value of 80%: All Radar agents 82%, US California: 86% and US Iowa: 90%.

### Best Practices

- Organize buckets logically (by project, environment, etc.)
- Keep number of tests per bucket under 150
- Use multiple cloud locations to distribute load
- Set appropriate concurrent test limits
- Use bucket-level notifications for relevant alerts
- Regularly review and clean up unused buckets
- Monitor bucket utilization to avoid queuing issues

---

## Role-Based Access Control (RBAC)

Configure role-based access control for API Monitoring teams, managing permissions and access levels for team members.

**Use when**: Configuring permissions and access levels for API Monitoring team members or implementing security policies for team collaboration.

### Overview

RBAC in API Monitoring allows you to control what team members can do, providing:
- Granular permission control
- Role-based access levels
- Security and compliance
- Team collaboration management

### Roles and Permissions

- **Admin**: Full access to team and bucket settings
- **Member**: Standard access to create and manage tests
- **Viewer**: Read-only access to tests and results
- **Custom Roles**: Create custom roles with specific permissions

### Configuration

1. **Define Roles**: Create roles with appropriate permissions
2. **Assign Members**: Assign roles to team members
3. **Review Permissions**: Regularly review and update permissions
4. **Audit Access**: Monitor and audit access levels

### Best Practices

- Use principle of least privilege
- Regularly review role assignments
- Document role definitions and permissions
- Implement role-based security policies

---

## Diagnostics

Enable and use advanced diagnostics tools in API Monitoring, including ping, netcat, dig, and traceroute for network troubleshooting.

**Use when**: Troubleshooting network connectivity issues in API Monitoring tests or diagnosing network problems during test execution.

### Overview

Diagnostics tools in API Monitoring help troubleshoot network and connectivity issues. Available tools include:
- **Ping**: Test network connectivity
- **Netcat**: Test TCP/UDP connections
- **Dig**: DNS lookup and troubleshooting
- **Traceroute**: Network path analysis

### Using Diagnostics

1. **Enable Diagnostics**: Enable diagnostics in test configuration
2. **Select Tools**: Choose diagnostic tools to use
3. **Run Tests**: Execute tests with diagnostics enabled
4. **Review Results**: Analyze diagnostic output for issues

### Common Use Cases

- **Network Connectivity**: Test connectivity to API endpoints
- **DNS Resolution**: Troubleshoot DNS issues
- **Network Path**: Analyze network routing
- **Connection Testing**: Test TCP/UDP connections

### Best Practices

- Use diagnostics when troubleshooting network issues
- Enable diagnostics only when needed (performance impact)
- Review diagnostic output carefully
- Document diagnostic findings

---

## Secrets Management

Use Secrets Management to manage values that are encrypted and hidden from users, but can still be read and used by API Monitoring test scripts. The Secrets Management feature for API Monitoring Tests requires a qualifying plan; check your plan or contact Sales to get started.

**Use when**: Managing encrypted secrets in API Monitoring or creating, editing, deleting, and using secrets in test scripts at team and bucket levels.

### How Secret Management Works

The Secrets feature allows API Monitoring **team owners** and administrators to create and manage variables with a key/value pair, where the value is encrypted and **hidden**, and allows all team members to use the variables in their tests with the new built-in function `{{get_secret(key)}}`.

In the same way you might have a `.env` or `config` file in your app that includes sensitive variables you don't want to be checked in to your project's version control repository. The Secrets feature can help you keep sensitive information secure.

### Examples

Some common cases where secrets can be used:

- You might have an API key or access token that you do not wish to be visible in your tests for security reasons
- You are working with an API that requires authentication credentials that you don't want exposed
- You don't want to send certain information to third-party integrations

### Manage Secrets

As a team owner or admin, you can manage secrets at the team level and at the bucket level. Secrets created at the team level can be used by all tests in all buckets. Secrets created at the bucket level can be used only by tests within that bucket.

Secrets have a 4096-character limit.

### Create Secrets at the Team Level

As an API Monitoring team owner or admin, you can create secrets at the team level.

Follow these steps:

1. Go to the **API Monitoring** tab
2. Click your profile on the top-right and select **Secrets** from the dropdown list
3. On the **Secrets** page, click **Add Secret**. A new secret key/value pair is created
4. Enter the name that will be used to access the secret throughout your tests
5. Enter the value
6. Click **Save Changes**

### Edit and Delete Secrets at the Team Level

To edit an existing secret, go to the **Secrets** page and click **Edit** next to the secret you wish to change the value for. Enter the new value and click **Save Changes**.

To delete a secret, go to the **Secrets** page and click the **x** next to the secret that you wish to delete.

### Create Secrets at the Bucket Level

You can create secrets at the bucket level if you have appropriate RBAC privileges. If you don't have permission to create secrets, contact your team owner or administrator.

Follow these steps:

1. In **API Monitoring**, click **Bucket Settings** in the top right corner. The **Bucket Settings** page opens
2. Scroll down to the **Bucket Secrets** section
3. Click **Add Secret**

**Note**: Secrets on a bucket level can't have the same name as secrets on the team level.

4. Enter the **Name** and **Value**. **Description** is optional
5. Click **Save Changes**

### Edit and Delete Secrets at the Bucket Level

To edit an existing secret, go to the **Bucket Settings** page and scroll down to the **Bucket Secrets** section. Click **Edit** next to the secret that you wish to change the value for. Enter the new value, and click **Save Changes**.

To delete a secret, click the **x** next to the secret that you wish to delete.

Team owners and admins can create roles with various permissions, for example, the View or Manage Bucket Permissions, and assign the roles to team members. For more information, see Role-Based Access Control.

### Use Secrets in Tests

To use secrets in your tests, you'll have to use a built-in function:

| Variable/Function | Description |
|-------------------|-------------|
| `{{get_secret(key)}}` | Retrieves the secret value for the `key` name. |

To see what team level secrets are available in your BlazeMeter API Monitoring account, you'll need to check with your team owner which can be found in the Team Members page. To see what secrets are available at the bucket level, go to the Bucket Settings page.

This built-in function can be used just like any other BlazeMeter API Monitoring built-in functions, which means you can add it to your environment settings, initial variables, pre-request/post-response scripts, etc. To use it in scripts, make sure you're calling the function as `get_secret(key)` without the parenthesis:

```javascript
// Example pre-request / post-response script
request.params.push({name:"api_key", value: get_secret("secret_key")});
```

**Important**: Whenever you have a step in your API tests that's using the `get_secret` function or is referencing a variable that was set using this function, **the results for that step will omit any information that might contain the value for that secret**, including the headers and body for both request and response. This also applies to any step that has a pre-request script or post-response script as it might reveal the value of the secret value.

### Best Practices

- Store all sensitive data as secrets
- Use descriptive secret names
- Rotate secrets regularly
- Never hardcode secrets in scripts
- Use team-level secrets for shared credentials
- Use bucket-level secrets for specific test data
- Remember that secret values are hidden from logs and UI

---

## AI Consent

Manage AI consent settings for API Monitoring teams, enabling or disabling AI-assisted features like script generation based on team policies.

**Use when**: Managing AI consent settings for API Monitoring teams or enabling or disabling AI-assisted features like script generation based on team policies.

### Overview

AI Consent controls whether AI-assisted features are available for a team. These features include:
- AI Script Assistant for script generation
- AI-powered test suggestions
- Automated script refinement

### Consent Management

- **Team-Level Control**: Configure consent at team level
- **Enable/Disable**: Turn AI features on or off
- **Policy Compliance**: Ensure compliance with organizational policies
- **Member Notification**: Inform team members of consent status

### Configuration

1. **Review Policies**: Understand organizational AI policies
2. **Configure Consent**: Set consent level for team
3. **Notify Members**: Inform team members of settings
4. **Monitor Usage**: Track AI feature usage

### Best Practices

- Align with organizational AI policies
- Document consent decisions
- Regularly review consent settings
- Ensure team members understand implications

---

## Bucket Metrics

You can access detailed usage metrics for your Buckets and Teams across multiple views. This function provides visibility into test activity, including number of tests, usage and execution trends, along with convenient CSV export options.

**Use when**: Viewing and exporting team and bucket usage metrics, analyzing test activity and execution trends, or exporting usage data to CSV.

### View Team and Bucket Usage

Follow these steps:

1. Log in to BlazeMeter and navigate to the **API Monitoring** tab.
2. Click the**Profile and Account Settings** icon in the top right corner.
3. Select **Teams & Usage**.
4. In the left-hand panel, find the relevant Bucket.
5. Click its **Settings & Usage**.

You will see the following metrics overview:

- **Plan Usage:** Usage summary for the current billing period.
- **Team Usage Data:** A graph of request usage over the last 90 days (grouped daily) and last year (grouped monthly).
- **Bucket Usage:** A list of all Buckets, with the number of tests and total requests for each.

### View Test-level Metrics within a Bucket

Follow these steps:

1. In the *Bucket Usage* section, click on a Bucket name.
2. A detailed sub-page opens, showing a list of tests with:
   - Test name
   - Test UUID
   - Requests made in the current billing period
   - Requests made in the last 90 days
   - Step count
   - Last start date

### Export Usage Metrics into CSV

**To export team usage data (last year):**

1. In the *Team Usage Data* section, use the drop-down menu to choose grouping: **Monthly**, **Weekly** or **Daily**.
2. Click **Download Usage (1 Year, CSV)** to download a CSV file with request and run data for the past year.

**To export bucket usage data (last 90 days):**

1. In the *Bucket Usage* section, click **Download Monthly Usage (CSV, Last 90 Days)**.
2. A CSV file will download, containing usage metrics for each Bucket.

---

## Role-Based Access Control

Role-based access control (RBAC) is a feature for teams that want to manage user's access to managing, editing, and viewing specific tests, buckets, and account features.

With RBAC you can:
- Allow users to have admin access to team's features such as RBAC itself, File Uploads, or billing details.
- Create a group that only has access to Bucket A and B, but not Bucket C.
- Create separate roles with different levels of access for developers, managers, Q&A, contractors, etc.

**Use when**: Managing user access to tests, buckets, and account features, creating groups and roles with different permission levels, or implementing role-based access control for team members.

### How RBAC Works

RBAC in BlazeMeter API Monitoring has three important elements: **groups**, **roles**, and **permissions**.

#### Groups

**Groups** are a way for team administrators to control team members access to **private buckets**. For example:
- You can have a group named "Internal", where team members that are part of that group only have access to BlazeMeter API Monitoring buckets that are related to internal APIs.
- You can have another group named "Contractors", where team members only have access to a select number of buckets that they're currently working on.

Buckets are set to public by default after they are created, and can be set to private by accessing the bucket's settings.

Users have a one-to-many relationship, so users can be a part of multiple groups at the same time. If a user is a part of multiple groups, they will have access to all of the buckets that are included in all of the groups they are a part of.

#### Roles and Permissions

**Roles** and **permissions** are a way to organize the level of access each team member can have. For example:
- A user can have a role of "Developer". That user will have a set of permissions that are related to development tasks, such as creating new tests, viewing tests, editing/modifying tests, deleting tests, etc.
- Another user can have a role of "Management". That user will have a set of permissions that allows them to view tests, but doesn't allow them to create or edit new tests. They can view the status and health of any API monitors, but won't be able to make changes to current test configurations.

### List of Permissions

| Permission | Description |
|---|---|
| View Tests | View all tests within a bucket |
| Execute Tests | Run or cancel tests within a bucket |
| Modify Tests | Create and edit tests within a bucket |
| Delete Tests | Delete tests within a bucket |
| Share Test Results | Share the results of a test |
| Manage Test Schedules | Add, modify, and delete test schedules within a bucket |
| Export Tests | Export tests within a bucket |
| Modify Shared Environments | Add, modify, and delete shared environments within a bucket |
| Add Buckets | Add new buckets |
| Modify Buckets | Modify bucket settings (change name, delete, etc.) |
| Manage Private Buckets | Manage all private buckets |
| Add Connected Service | Add a connected service |
| Delete Connected Service | Delete a connected service |
| Modify Script Libraries | Modify script libraries |
| Delete Script Libraries | Delete script libraries |
| Gateway Agent Authentication | Authorize to sign in via the Gateway Agent |
| Radar Agent Authentication | Authorize to sign in via the Radar Agent |
| View Team Members | View all members of a team |
| Manage Team Members | Add or delete team members |
| Invite Team Members | Invite members to a team |
| Change Team Settings | Change team settings |
| View Team Usage | View team usage |
| View Team Groups | View group permissions and membership |
| Modify Team Groups | Modify group permissions and membership |
| View Team Secrets | View the list of all sensitive variables |
| Manage Team Secrets | Create, edit, and delete sensitive variables |
| Manage File Uploads | Upload and delete files |
| View Billing | View billing information for a team |
| Manage Billing | Change billing information for a team |
| View Bucket Secrets | View the list of all sensitive variables at the bucket level |
| Manage Bucket Secrets | Create, edit, and delete sensitive variables at the bucket level |

### Create and Manage Groups

Follow these steps:

1. After logging in to your BlazeMeter API Monitoring account, click on your profile on the top-right and select **Teams & Usage**.
2. On the left-hand side, click on **Team Members** under the team that you want to manage.
3. Under the *Team Groups* section, click **Add New***.*
4. Name your group and click **Create Group**.
5. Click the new group name.
6. Under the **Private Buckets** section, use the search box to search for private buckets under your account. Click **Add Bucket** to add a bucket to the list. Use the checkbox next to each bucket if you want to remove it from the list.
7. Under the **Members** section, enter your team member's email address that you want to give access to the buckets in the selected user group and click **Add Member**.
8. Click **Save**.

### Create and Manage Roles and Permissions

#### Create a New Role

Follow these steps:

1. In **API Monitoring**, click your profile on the top-right and select **Teams & Usage**.
2. From the menu on the left, select **Roles and Permissions**. **Note:** By default, BlazeMeter API Monitoring creates three roles for every team with the RBAC feature enabled. These are protected roles and can't be edited: *Administrators*, *Read-only Members*, and *User Group.*
3. To create a new role, click **Add Role**.
4. Name the role. **Example:** If you want to create a new role with permissions to manage secrets at the bucket level, you can name the role **Manage_Buckets**.
5. Click **Create Role**. The role shows in the list of roles.
6. Click the new role and from the list of permissions, check the boxes for any permissions that you want the new role to have access to. **Example:** If you want to assign permissions to manage secrets at a bucket level, check **Manage Bucket Secrets**. Team members with this role will have permissions to create, edit and delete secrets at the bucket level.
7. Click **Save**.

#### Edit a Role

Follow these steps:

1. In **API Monitoring**, click your profile on the top-right and select **Teams & Usage**.
2. From the menu on the left, select **Roles and Permissions**.
3. Select an existing role that you wish to edit.
4. In the list of permissions, check or uncheck the boxes for various permissions, as needed.
5. Click **Save**.

#### Assign a Role to a Team Member

Follow these steps:

1. In **API Monitoring**, click your profile on the top-right and select **Teams & Usage**.
2. From the menu on the left, click **Team Members**.
3. Scroll down to the **Team Members** section and select the team member that you want to assign the role to.
4. From the drop-down list next to the name, select the role. **Example:** Earlier you created a new role called **Manage_Buckets**with permissions to **Manage Bucket Secrets**. When you assign the role, the team member will have permissions to create, edit and delete secrets at the bucket level.

For more information on managing teams, see [API Monitoring Teams](skill-blazemeter-administration://references/api-monitoring-teams.md).

---

## Security

**Security is our top priority. If you think you've found a vulnerability in any BlazeMeter API Monitoring service, please contact us.**

**Use when**: Understanding API Monitoring security practices, implementing secure testing practices, or reporting security vulnerabilities.

### How We Keep You Safe

BlazeMeter uses best practices for Internet security. This helps ensure that your data is safe, secure, and available only to authorized users. Your data will be completely inaccessible to anyone else, unless you explicitly choose to share that data with the public.

BlazeMeter API Monitoring enforces secure HTTPS for our entire website, including the public (unauthenticated) parts of the site. All communications with the API Monitoring API are also protected with SSL. We also use HTTP Strict Transport Security to ensure your web browser never interacts with BlazeMeter over insecure HTTP.

BlazeMeter API Monitoring provides each user in your organization with a unique user name and password. These credentials must be entered to access your organization's data.

### How To Keep Yourself Safe

BlazeMeter can be used to inspect traffic to APIs that communicate via plain-text HTTP or encrypted HTTPS. When you use API Monitoring with a plain-text HTTP API, all network traffic between your server and BlazeMeter will be sent in plain text, as will all network traffic between BlazeMeter and your API provider.

**For this reason, we recommend that you use HTTPS whenever possible.** If an API gives you the choice, you should always use HTTPS.

API Monitoring buckets are writable given that you know the randomly generated bucket key; however, data can only be viewed by the bucket owner. You may optionally enable secondary authentication for a bucket. Authenticated buckets require an additional secret token to be supplied in either an HTTP header or query string parameter to write to a bucket. If you would like to enable authentication tokens for your buckets, you may do so by enabling them in the Bucket Settings page on your dashboard.

### Contacting BlazeMeter Support

If you have found a security vulnerability in a BlazeMeter web site or service, or if you have further questions about your data's security, send an email to [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com?subject=security vulnerability in BlazeMeter API Monitoring) or contact the Account Team.

Your email will be reviewed promptly. We request that you not publicly disclose the issue until it has been addressed by BlazeMeter.

---

## View and Export Team and Bucket Metrics

Access detailed usage metrics for your Buckets and Teams across multiple views. This function provides visibility into test activity, including number of tests, usage and execution trends, along with convenient CSV export options.

**Use when**: Viewing team and bucket usage metrics, exporting usage data, or analyzing test activity and execution trends.

### View Team and Bucket Usage

Follow these steps:

1. Log in to BlazeMeter and navigate to the **API Monitoring** tab
2. Click the **Profile and Account Settings** icon in the top right corner
3. Select **Teams & Usage**
4. In the left-hand panel, find the relevant Bucket
5. Click its **Settings & Usage**

You will see the following metrics overview:

- **Plan Usage**: Usage summary for the current billing period
- **Team Usage Data**: A graph of request usage over the last 90 days (grouped daily) and last year (grouped monthly)
- **Bucket Usage**: A list of all Buckets, with the number of tests and total requests for each

### View Test-level Metrics within a Bucket

Follow these steps:

1. In the *Bucket Usage* section, click on a Bucket name
2. A detailed sub-page opens, showing a list of tests with:
   - Test name
   - Test UUID
   - Requests made in the current billing period
   - Requests made in the last 90 days
   - Step count
   - Last start date

### Export Usage Metrics into CSV

**To export team usage data (last year):**

1. In the *Team Usage Data* section, use the drop-down menu to choose grouping: **Monthly**, **Weekly** or **Daily**
2. Click **Download Usage (1 Year, CSV)** to download a CSV file with request and run data for the past year

**To export bucket usage data (last 90 days):**

1. In the *Bucket Usage* section, click **Download Monthly Usage (CSV, Last 90 Days)**
2. A CSV file will download, containing usage metrics for each Bucket

### Documentation References

For detailed information about viewing and exporting team and bucket metrics, use the BlazeMeter MCP help tools:

**View and Export Team and Bucket Metrics**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-bucket-metrics`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-bucket-metrics"]}`

---

## Documentation References

For detailed information about API Monitoring management, use the BlazeMeter MCP help tools:

**Teams and Buckets**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-manage-your-teams` (for teams) y `api-monitoring-manage-your-buckets` (for buckets)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-manage-your-teams", "api-monitoring-manage-your-buckets"]}`

**Secrets Management**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-secrets-management`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-secrets-management"]}`

**Role-Based Access Control**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-role-based-access-control`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-role-based-access-control"]}`

**Bucket Metrics**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-bucket-metrics`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-bucket-metrics"]}`

**Security**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-security`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-security"]}`

