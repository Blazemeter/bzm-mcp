# API Monitoring Notifications

## Custom Emails

You can configure email notifications to send test results to custom email addresses which includes non-member emails, external emails, or distribution list emails.

**Use when**: Configuring custom email notifications for API Monitoring tests or sending notifications to non-member emails or distribution lists.

### Configuration Methods

To configure custom emails:

- **Via the BlazeMeter app**: See **Email Notifications** in Managing Configuration with Environments
- **Via the API Monitoring API**: 
  - Manage email domains using the [Team Email Domains API](https://help.blazemeter.com/apidocs/api-monitoring/teams_email_domains.htm)
  - Manage custom email addresses using the [Bucket Custom Emails API](https://help.blazemeter.com/apidocs/api-monitoring/buckets_custom_emails_add.htm)

### Overview

Custom email notifications allow you to send test result notifications to:
- Team members
- Non-member email addresses
- External distribution lists
- Custom email groups

### Best Practices

- Use distribution lists for team notifications
- Configure appropriate notification triggers
- Keep email lists updated
- Test email delivery

---

## Sharing Test Results

API test results can be viewed and shared privately with other members of your team. You can also share test results with people outside of your organization by changing an API test result from **Private** to **Shareable**.

**Use when**: Sharing API Monitoring test results with team members or publicly via shareable links or configuring result retention policies.

### Creating a Shareable API Test Result

You can share any test result URL by viewing a test result and changing the Private/Shareable toggle to Shareable. Once the test result has been set to Shareable, you can copy the URL and send it to people outside of your team, as well as people not signed in to BlazeMeter. The test result is able to be viewed in detail, but the test is not editable or capable of being re-run by people outside of your team.

### Unsharing an API Test Result

An API test result can be made private at any time by signing in to your team, going to the shared test result URL, and changing the toggle from Shareable to Private. Team members will still be able to view and share the test result URL, but it will not be available to anyone else. You can only change the Private/Shareable status of test results that are owned by your team.

### API Test Result Retention

Currently, only the last 100 Passed tests and 100 Failed tests are retained in history. Because of this, test results older than the latest 100 Passed or Failed will not show the full test step Request/Response/Connection details.

**Important**: Export important results before they are removed from history, as older test results will not show full details.

### Best Practices

- Use private sharing for sensitive results
- Set appropriate retention periods (remember: only last 100 Passed and 100 Failed are retained)
- Regularly review shared links
- Remove access when no longer needed
- Export important results before they are removed from history

---

## Test Results Retention

Understand API Monitoring test result retention policies, including history limits and data retention periods.

**Use when**: Understanding API Monitoring test result retention policies or configuring history limits and data retention periods.

### Overview

Each API Monitoring test retains a limited amount of history:
- The full step (HTTP request/response) details are stored for the last 100 successes and the last 100 failures
- Test result summary information (pass/fail, no step details) is stored for the last 1,000 test runs
- Test retention also takes into account our data retention policy of **90 days**

### Viewing Test Results

To view a result from the dashboard, you may access the details of the last 100 successful and failed test runs from each test's *Results* page, or by clicking on the individual results in the red, green, or orange Latest Results bar on the *Overview* page. You may also retrieve additional summary history up to the last 1,000 test runs via the API.

### Storing Results for Longer Retention

To store results in a system of your choosing (e.g. S3) for longer retention, set up a webhook notification listener and store results as they are generated.

For more advanced analysis of results over time, connect BlazeMeter API Monitoring with an analytics provider like Splunk Cloud, Datadog, Keen, or New Relic Insights.

### Documentation References

For detailed information about API test results retention, use the BlazeMeter MCP help tools:

**API Test Results Retention**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-api-test-results-retention`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-api-test-results-retention"]}`

---

## Notifications Overview

When your API tests complete, you want to know what happened. API Monitoring supports a wide variety of notification options, including popular 3rd-party services, to make sure you are the first to know when there is an issue with your services.

**Use when**: Configuring various notification options for API Monitoring tests or setting up email, webhooks, and third-party service integrations like Slack and PagerDuty.

### Notification Options via API Monitoring

- **Email**: Send notifications to team members and custom email addresses
- **Webhooks**: Configure callback URLs to receive test completion notifications
- **Advanced Webhooks**: Customize webhook notifications with authentication, headers, and thresholds

### Notification Options via Integrations with Third-party Services

- **Slack**: Integrate with Slack for team notifications
- **PagerDuty**: Send alerts to PagerDuty for incident management
- **VictorOps**: Integrate with VictorOps for on-call management
- **Microsoft Teams (Preview)**: Send notifications to Microsoft Teams channels
- **Grove**: Integrate with Grove for team communication
- **Zapier**: Connect with Zapier for workflow automation
- **OpsGenie**: Integrate with OpsGenie for alerting and on-call management
- **ServiceNow**: Send notifications to ServiceNow for IT service management

### Email Notifications

Email notifications can be sent to:
- Individual team members
- Custom emails (non-member emails, external emails, or distribution list emails)

After selecting the members of your team to notify, you can choose to be notified based on the following options:
- After all test runs
- After all failed test runs
- After a certain number of consecutive failures for a specific location
- After a test fails due to an API failure (excluding Radar Agent issues)
- After a test fails due to an on-premise Radar Agent issue

Additionally, you may choose to send emails when a test returns to a successful state.

**Configuration:**
- Configure individual test email notifications from the **Email Notifications** page of any test
- For bucket-level test notifications, navigate to **Bucket Settings > Email Notifications**, accessible from the bucket's dashboard
- For more information, see the **Configure Email Notifications** sections on the [Managing Configuration with Environments](skill-blazemeter-api-monitoring://references/configuration.md) page

### Setting up Multiple Notification Configurations

Using [Environments](skill-blazemeter-api-monitoring://references/configuration.md), you can configure notification settings that only alert specific groups within your team, depending on the test or shared environment used to run your test.

### Webhook Notifications

You can specify callback URLs to be requested upon the completion of every test. From the **Notifications** page in the test editor enter the URL you would like to be notified at. All test runs, regardless of outcome, will trigger a webhook notification. To notify multiple URLs, enter one per line.

If you want more flexibility to customize your webhook notifications, check out our [Advanced Webhooks integration](skill-blazemeter-api-monitoring://references/advanced-features.md).

#### Webhook Request Data

**POST** Callback URL(s)

**Sample Request Data:**

```json
{
  "variables": {
    "foo": "bar",
    "baz": "qux"
  },
  "test_id": "76598752-cbda-4e1d-820f-6274a62f74ff",
  "test_name": "Buckets Test",
  "test_run_id": "9c15aa62-21f0-48f2-a819-c99bdf8e4543",
  "team_id": "6b9c7f65-9e11-4f77-85ad-e6ee7a28232d",
  "team_name": "Acme Inc.",
  "environment_uuid": "98290cfc-a008-4ab7-9ea4-8906f12b228f",
  "environment_name": "Staging Settings",
  "bucket_name": "Rocket Sled",
  "bucket_key": "",
  "test_url": "https://www.runscope.com/radar//76598752-cbda-4e1d-820f-6274a62f74ff",
  "test_run_url": "https://www.runscope.com/radar//76598752-cbda-4e1d-820f-6274a62f74ff/results/9c15aa62-21f0-48f2-a819-c99bdf8e4543",
  "trigger_url": "https://api.runscope.com/radar/09039249-fdfd-4e1d-820f-6274a62f74ff/trigger",
  "result": "fail",
  "started_at": 1384281308.548077,
  "finished_at": 1384281310.680218,
  "agent": null,
  "agent_expired": null,
  "region": "us1",
  "region_name": "US East - Northern Virginia",
  "initial_variables": {},
  "requests": [{
    "step_type": "request",
    "url": "https://api.runscope.com/",
    "variables": {
      "fail": 0,
      "total": 1,
      "pass": 1
    },
    "assertions": {
      "fail": 0,
      "total": 2,
      "pass": 2
    },
    "scripts": {
      "fail": 0,
      "total": 1,
      "pass": 1
    },
    "result": "pass",
    "method": "GET",
    "response_time_ms": 123,
    "response_size_bytes": 2048,
    "response_status_code": 200,
    "note": "Root URL"
  }]
}
```

#### Webhook Payload Data Attributes

| Attribute | Description |
|-----------|-------------|
| `variables` | A dictionary containing all initial variables for this test run, and the variables extracted and stored from each step |
| `test_id` | The unique ID for the test responsible for this test run |
| `test_name` | The name of the test responsible for this test run |
| `test_run_id` | The unique ID of this specific test run |
| `team_id` | The unique ID of the team this test's bucket belongs to |
| `team_name` | The name of the team this test's bucket belongs to |
| `environment_uuid` | The UUID of the environment used by this test run |
| `environment_name` | The name of the environment used by this test run |
| `bucket_name` | The name of the bucket the test belongs to |
| `bucket_key` | The key of the bucket the test belongs to |
| `test_url` | The URL for viewing and editing this test in the BlazeMeter API Monitoring dashboard |
| `test_run_url` | The URL for the test result detail page in the BlazeMeter API Monitoring dashboard |
| `trigger_url` | The [Trigger URL](skill-blazemeter-api-monitoring://references/integrations.md) for this test. Typically used to retry a test run |
| `result` | The result of the test run, either `pass` or `fail` |
| `started_at` | The UNIX timestamp for the start of the test run |
| `finished_at` | The UNIX timestamp for the completion of the test run |
| `agent` | The agent used to execute this test run, or `null` if a default BlazeMeter API Monitoring location was used |
| `agent_expired` | The status of the agent for this test run. This is `true` if the agent is expired, and `null` if the agent is available or if a default BlazeMeter API Monitoring location was used |
| `region` | The [region code for the location](skill-blazemeter-api-monitoring://references/configuration.md) the test was run from, or `null` if an agent was used |
| `region_name` | The full [region name and location](skill-blazemeter-api-monitoring://references/configuration.md) the test was run from, or `null` if an agent was used |
| `initial_variables` | A dictionary of the test run's initial variables. This is the variable state after the initial scripts and variables have been processed (bucket-wide and test-specific) prior to the execution of the first request |
| `requests` | A list of the HTTP requests that were executed in this test run with the method, URL and assertion, variable and script success/failure counts |

### Best Practices

- Configure appropriate notification triggers based on your needs
- Use multiple notification channels for critical tests
- Set up environment-specific notifications for different teams
- Test notification delivery to ensure reliability
- Use advanced webhooks for custom integrations
- Regularly review and update notification configurations

### Notification Types

- **Email Notifications**: Direct email alerts
- **Webhooks**: Custom webhook integrations
- **Third-Party Services**: Integrations with Slack, PagerDuty, etc.
- **In-App Notifications**: Notifications within BlazeMeter

### Configuration

1. **Select Notification Type**: Choose notification method
2. **Configure Settings**: Set up notification settings
3. **Set Triggers**: Define when notifications are sent
4. **Test Notifications**: Verify notification delivery

### Best Practices

- Use appropriate notification channels
- Configure meaningful notification triggers
- Test notification delivery
- Monitor notification effectiveness

---
- **ServiceNow**: Integrate with ServiceNow

### Email Notifications

Email notifications can be sent to:
- Individual team members
- Custom emails (non-member emails, external emails, or distribution list emails)

After selecting the members of your team to notify, you can choose to be notified based on the following options:
- after all test runs
- after all failed test runs
- after a certain number of consecutive failures for a specific location
- after a test fails due to an API failure (excluding [Radar Agent](skill-blazemeter-private-locations://references/radar-agent.md) issues)
- after a test fails due to an on-premise [Radar Agent](skill-blazemeter-private-locations://references/radar-agent.md) issue

Additionally, you may choose to send emails when a test returns to a successful state.

Configure individual test email notifications from the **Email Notifications** page of any test. For more information, see the **Configure Email Notifications** sections on the [Managing Configuration with Environments](skill-blazemeter-api-monitoring://references/configuration.md) page.

For bucket-level test notifications, navigate to **Bucket Settings > Email Notifications**, accessible from the bucket's dashboard.

### Setting up multiple notification configurations

Using [Environments](skill-blazemeter-api-monitoring://references/configuration.md), you can configure notification settings that only alert specific groups within your team, depending on the test or shared environment used to run your test.

### Webhook Notifications

You can specify callback URLs to be requested upon the completion of every test. From the **Notifications** page in the test editor enter the URL you would like to be notified at. All test runs, regardless of outcome, will trigger a webhook notification. To notify multiple URLs, enter one per line.

If you want more flexibility to customize your webhook notifications, check out our [Advanced Webhooks](skill-blazemeter-api-monitoring://references/notifications.md) integration.

---

## Advanced Webhooks

Advanced webhooks are a powerful option to integrate BlazeMeter API Monitoring test run notifications with any workflow or third-party application.

This integration allows users to specify a URL, which BlazeMeter will use to send a JSON payload that includes the results of a test run via a POST request. That URL can be the endpoint of a 3rd-party application, or your own application that you can build to receive results of BlazeMeter API Monitoring test runs and then integrate those results to fit into your team's workflow.

**Use when**: Integrating API Monitoring test run notifications with workflows or third-party applications, customizing webhook notifications, or building custom applications to receive test results.

### How to Use Advanced Webhooks

Follow these steps:

1. Go your team's **Connected Services** page.
2. Search for the advanced webhooks option, and select **Connect**:
3. Fill in the required fields:
   - **Description**: This is the name that will be displayed in your list of Connected Services, and on the Integrations tab of the Environment Settings.
   - **Threshold**: Select how often you want the notification to be sent.
   - **URL**: The URL that the POST request will be sent to.
   - **Authentication**: You can add Basic Authentication (username and password) to the request for security purposes.
   - **Headers**: Add any custom headers that your application might require.
4. Click **Save Changes**.

Your advanced webhooks integration is now ready to be used. Do not forget to enable the integration on your environment settings to start receiving notifications on the configured callback URLs.

### Webhook Request & Payload

#### Webhook Request Data

**POST** Callback URL(s)

##### Sample Request Data

```json
{
"variables": {
"foo": "bar",
"baz": "qux"
},
"test_id": "76598752-cbda-4e1d-820f-6274a62f74ff",
"test_name": "Buckets Test",
"test_run_id": "9c15aa62-21f0-48f2-a819-c99bdf8e4543",
"team_id": "6b9c7f65-9e11-4f77-85ad-e6ee7a28232d",
"team_name": "Acme Inc.",
"environment_uuid": "98290cfc-a008-4ab7-9ea4-8906f12b228f",
"environment_name": "Staging Settings",
"bucket_name": "Rocket Sled",
"bucket_key": "",
"test_url": "https://www.runscope.com/radar//76598752-cbda-4e1d-820f-6274a62f74ff",
"test_run_url": "https://www.runscope.com/radar//76598752-cbda-4e1d-820f-6274a62f74ff/results/9c15aa62-21f0-48f2-a819-c99bdf8e4543",
"trigger_url": "https://api.runscope.com/radar/09039249-fdfd-4e1d-820f-6274a62f74ff/trigger",
"result": "fail",
"started_at": 1384281308.548077,
"finished_at": 1384281310.680218,
"agent": null,
"agent_expired": null,
"region": "us1",
"region_name": "US East - Northern Virginia",
"initial_variables": {},
"requests": [{
"step_type": "request",
"url": "https://api.runscope.com/",
"variables": {
"fail": 0,
"total": 1,
"pass": 1
},
"assertions": {
"fail": 0,
"total": 2,
"pass": 2
},
"scripts": {
"fail": 0,
"total": 1,
"pass": 1
},
"result": "pass",
"method": "GET",
"response_time_ms": 123,
"response_size_bytes": 2048,
"response_status_code": 200,
"note": "Root URL"
}]
}
```

##### Webhook Payload Data Attributes

| Attribute | Description |
|---|---|
| `variables` | A dictionary containing all initial variables for this test run, and the variables extracted and stored from each step. |
| `test_id` | The unique ID for the test responsible for this test run. |
| `test_name` | The name of the test responsible for this test run. |
| `test_run_id` | The unique ID of this specific test run. |
| `team_id` | The unique ID of the team this test's bucket belongs to. |
| `team_name` | The name of the team this test's bucket belongs to. |
| `environment_uuid` | The UUID of the environment used by this test run. |
| `environment_name` | The name of the environment used by this test run. |
| `bucket_name` | The name of the bucket the test belongs to. |
| `bucket_key` | The key of the bucket the test belongs to. |
| `test_url` | The URL for this viewing and editing this test in the API Monitoring dashboard. |
| `test_run_url` | The URL for the test result detail page in the API Monitoring dashboard. |
| `trigger_url` | The [Trigger URL](skill-blazemeter-api-monitoring://references/integrations.md) for this test. Typically used to retry a test run. |
| `result` | The result of the test run, either `pass` or `fail`. |
| `started_at` | The UNIX timestamp for the start of the test run. |
| `finished_at` | The UNIX timestamp for the completion of the test run. |
| `agent` | The agent used to execute this test run, or `null` if a default API Monitoring location was used. |
| `agent_expired` | The status of the agent for this test run. This is `true` if the agent is expired, and `null` if the agent is available or if a default API Monitoring location was used. |
| `region` | The [region code for the location](skill-blazemeter-api-monitoring://references/configuration.md) the test was run from, or `null` if an agent was used. |
| `region_name` | The full [region name and location](skill-blazemeter-api-monitoring://references/configuration.md) the test was run from, or `null` if an agent was used. |
| `initial_variables` | A dictionary of the test runs initial variables. This is the variable state after the initial scripts and variables have been processed (bucket-wide and test-specific) prior to the execution of the first request. |
| `requests` | A list of the HTTP requests that were executed in this test run with the method, URL and assertion, variable and script success/failure counts. |

### Documentation References

For detailed information about Advanced Webhooks, use the BlazeMeter MCP help tools:

**Advanced Webhooks**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-advanced-webhooks`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-advanced-webhooks"]}`

#### Webhook Request Data

**POST** Callback URL(s)

The webhook payload includes comprehensive test run information including:
- Test and test run identifiers
- Team and bucket information
- Environment details
- Test result (pass/fail)
- Timestamps (started_at, finished_at)
- Agent and region information
- Variables extracted during test execution
- Request details with method, URL, response times, status codes, and assertion/variable/script results

For detailed information about webhook payload structure, see the [Notifications Overview](https://help.blazemeter.com/docs/guide/api-monitoring-notifications-overview.html#webhook) help documentation.

### Documentation References

For detailed information about API Monitoring notifications, use the BlazeMeter MCP help tools:

**Custom Emails**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-custom-emails`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-custom-emails"]}`

**Sharing Test Results**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-sharing-test-results`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-sharing-test-results"]}`

**Notifications Overview**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-notifications-overview`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-notifications-overview"]}`

