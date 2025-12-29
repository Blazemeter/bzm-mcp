# API Monitoring Integrations

## Overview

BlazeMeter API Monitoring integrates with 30+ third-party services for notifications, incident management, analytics, and workflow automation. This reference covers all available integrations.

**Use when**: Integrating API Monitoring with external services for notifications, incident management, analytics, or workflow automation.

## Incident Management & Alerting

### PagerDuty Integration

BlazeMeter (API Monitoring) is a set of API debugging and monitoring tools used for testing. Developers and operations teams can use BlazeMeter (API Monitoring) to monitor their APIs via scheduled tests with automatic PagerDuty incident triggering and resolution. Integrating PagerDuty with BlazeMeter (API Monitoring) is done through PagerDuty Connect.

**Use when**: Implementing real-time incident management with automatic incident triggering and resolution.

#### Benefits

- Users are immediately notified about failures for the tests that are integrated with PagerDuty
- Users can set a custom notification threshold in API Monitoring to trigger an event
- Users can view the event data from API Monitoring with the link to the test that triggered the event
- Incidents will automatically resolve in PagerDuty when the metric in API Monitoring test returns to normal with bidirectional synchronization

#### Requirements

Only users with a base manager role and above are able to complete the integration with PagerDuty. Reach out to these roles in your organization to configure the integration.

#### Integrating With a PagerDuty Service

**In PagerDuty:**

Follow these steps:

1. From the **Configuration** menu, select **Services**
2. There are two ways to add an integration to a service:
   - If you are adding your integration to an existing service: Click the name of the service you want to add the integration to. Then, select the **Integrations** tab and click the **New Integration** button
   - If you are creating a new service for your integration: Follow the steps outlined in the **Create a New Service** section, selecting **BlazeMeter (API Monitoring)** as the Integration Type in step 4
3. Enter an **Integration Name** in the format monitoring-tool-service-name (e.g. BlazeMeter-Shopping-Cart) and select **BlazeMeter (API Monitoring)** from the **Integration Type** menu
4. Click the **Add Integration** button to save your new integration. You will be redirected to the **Integrations** tab for your service
5. An **Integration Key** will be generated on this screen. Keep this key saved in a safe place, as it will be used when you configure the integration with **BlazeMeter (API Monitoring)** in the next section

**In BlazeMeter (API Monitoring):**

1. In the **API Monitoring** dashboard home page, click **PagerDuty** in the **Connect BlazeMeter (API Monitoring) with Your Workflow** section
   - Or, select **Connected Services** from the top right menu. Find the PagerDuty icon and click **Connect PagerDuty**

**Note**: If the PagerDuty Service you want to integrate with is grayed out, you will need to "Enable Alerts" within the PagerDuty dashboard for the service first.

PagerDuty is now connected and integrated with BlazeMeter (API Monitoring).

#### Enable PagerDuty

You can enable PagerDuty in BlazeMeter (API Monitoring):
- In a test. PagerDuty will be enabled only for that specific test
- In a shared environment. PagerDuty will be enabled for all tests that belong to the shared environment

**Enable PagerDuty in a Test:**

1. Go to **API Monitoring**, and create a new Test
2. Expand the **Environments** section and click **Integrations**
3. For PagerDuty, toggle the button **ON**
4. Click **Save**

**Enable PagerDuty in a Shared Environment:**

1. Select **Shared Environments** and click **Add Shared Environment**
2. Click the **Unnamed** title to expand the window and enter a Name
3. Select **Integrations** from the menu
4. For PagerDuty, toggle the button **ON**
5. Click **Save**

#### Triggering and Resolving Incidents

When a connected PagerDuty service is enabled, any Radar test runs that fail will trigger an incident and send the notifications defined in your PagerDuty service settings. When any subsequent test run passes, the incident will be marked as resolved automatically. You can click the **BlazeMeter (API Monitoring)** URL to be linked directly to your **BlazeMeter (API Monitoring)** account.

In order to prevent one test from clearing an incident for another, we recommend creating a PagerDuty service for each of your tests.

#### FAQ

**Can you associate a BlazeMeter (API Monitoring) test with more than one PagerDuty service?**
Yes. You can connect as many PagerDuty services to your BlazeMeter (API Monitoring) team as you'd like. For each test within your team, select from the connected services available to enable the integration.

**Will PagerDuty incidents automatically resolve once the BlazeMeter (API Monitoring) test passes again?**
Yes, PagerDuty incidents will automatically resolve when the BlazeMeter (API Monitoring) test associated with them passes.

#### How to Disconnect

Follow these steps:
1. In BlazeMeter (API Monitoring), select **Connected Services** from the menu on the left
2. Find the PagerDuty integration that you want to disconnect and click **Disconnect**

### OpsGenie Integration

[OpsGenie](https://www.atlassian.com/software/opsgenie) makes notifications easy. Forward alerts from your IT monitoring tools and notify users via iPhone/Android push notifications, email, SMS and phone calls.

**Use when**: Forwarding alerts and notifying users via push notifications, email, SMS, and phone calls.

#### Configure OpsGenie Integration

Follow these steps:

1. From your OpsGenie dashboard, select **Integrations** from the top navigation bar.
2. Search for or locate BlazeMeter API Monitoring on the list and click **Add**.
3. Copy the callback URL and paste it into the webhook notifications section of your BlazeMeter API Monitoring [test environment](skill-blazemeter-api-monitoring://references/configuration.md) or [shared environment](skill-blazemeter-api-monitoring://references/configuration.md) settings.
4. From OpsGenie, select the desired recipients and notification settings. To notify everyone, enter 'all' into the recipients box.
5. Finalize the configuration by selecting **Save Integration**.

An alert is triggered when a test with this callback URL fails. The alert is automatically cleared when the test resumes passing.

For more information, see OpsGenie's [BlazeMeter API Monitoring Integration documentation](https://support.atlassian.com/opsgenie/docs/integrate-opsgenie-with-runscope/).

Having trouble configuring OpsGenie? [Contact our Support team](mailto:support-blazemeter@perforce.com?Subject=OpsGenie%20Integration%20Help).

### VictorOps/Splunk On-Call Integration

[VictorOps/Splunk On-Call](https://www.splunk.com/en_us/about-splunk/acquisitions/splunk-on-call.html) is a real-time incident management platform that focuses on lifecycle management and collaboration for IT and DevOps teams.

**Use when**: Implementing real-time incident management with lifecycle management and collaboration.

#### Configure VictorOps Integration

1. In VictorOps, enable the [BlazeMeter API Monitoring Integration](https://help.victorops.com/knowledge-base/victorops-runscope-integration/). Copy the **VictorOps API Key** to your clipboard.
2. In your BlazeMeter API Monitoring account, select **Connected Services**.
3. Select **Connect VictorOps**.
4. On the **Settings** screen, enter the VictorOps API Key generated above.
5. Enter a Routing Key (optional) if you would like to target a specific notification group.

#### Triggering and Resolving Incidents

When a connected VictorOps service is enabled, any API test runs that fail will trigger an incident and send the notifications defined in your VictorOps service settings. If you have enabled automatic resolution, the incident will be marked as resolved when any subsequent test run passes.

You can disconnect VictorOps at any time by disconnecting the service in your team's settings.

#### Configuring Alert Thresholds

You can wait to send VictorOps alerts after a certain number of consecutive failures by configuring your VictorOps integration settings from the Connected Services dashboard.

### BigPanda Integration
Connect BigPanda with BlazeMeter API Monitoring to send API test results to BigPanda dashboard for incident management.

**Use when**: Sending API test results to BigPanda dashboard for incident management.

## Communication & Collaboration

### Slack Integration

[Slack](https://slack.com/) is group chat and IM built for teams.

**Use when**: Receiving test result notifications in designated Slack channels via webhooks.

#### Setting up Slack

Follow these steps:

1. In Slack, go to your account's App Directory and [add a new Runscope (Legacy) integration](https://slack.com/services/new/runscope).
2. Select the Slack channel in which you want to receive notifications.
3. Scroll down to the **Integration** Settings section and copy the **Webhook URL** to your clipboard.

#### Setting up the API Monitoring Integration

Follow these steps:

1. Navigate back to your API Monitoring account.
2. Click your profile on the top-right and select **Connected Services**.
3. Find Slack in the list and select **Connect Slack**.
4. On the **Settings** screen, paste the Slack Webhook URL from the previous steps and enter a Channel Name (that is just for reference and to help differentiate between multiple Slack integrations). Select your notification preferences and click **Connect Account**.
5. For the final step, choose whether to activate Slack integration on individual tests, or on all tests in your bucket:
   - For individual tests, open the environment settings for a particular test, select **Integrations**, and activate your Slack integration.
   - To integrate Slack to all tests in the bucket, navigate to **Bucket Settings** from your bucket's dashboard. Scroll to **Integrations Notifications** and enable the Slack integration.
6. Save your test. Test result notifications should now be sent to your Slack channel.

Having trouble configuring Slack? [Contact our Support team](mailto:support-blazemeter@perforce.com?Subject=Slack%20Integration).

### Microsoft Teams Integration

You can set up a workflow in Microsoft Teams to post API Monitoring notifications to a designated channel.

**Use when**: Posting API Monitoring notifications to designated channels using webhooks.

#### Setting up a Microsoft Teams Workflow

Follow these steps:

1. Log in to your Microsoft Teams account. We recommend creating a new channel for API Monitoring notifications, as sometimes people in different teams might be interested in being notified of any API errors.
2. Choose which channel you want to send notifications to. Right-click or click the ". . ." symbol, and select **Workflows**.
3. Search for **webhook** and select the **Post to a channel when a webhook request is received** template.
4. Provide a name for the webhook and ensure it is connected to the right account. Select **Next**.
5. Select the correct Microsoft Teams team and channel, the select **Add workflow**.
6. Copy the workflow URL that Microsoft Teams generated for you.

#### Setting up the BlazeMeter API Monitoring Integration

Follow these steps:

1. Go to your BlazeMeter API Monitoring account. Log in, click your profile picture on the top-right and select **Connected Services**.
2. You should see all the integration options available for your API Monitoring account. Look for the Microsoft Teams options and click **Connect Microsoft Teams**.
3. In the next page there are three fields:
   - **Workflow URL**: paste the URL you got from the Microsoft Teams webhook configuration here.
   - **Channel Name**: you can add multiple Microsoft Team connections to the same API Monitoring account. The name can help you distinguish between multiple connections.
   - **Notifications**: select when you want to be notified after test runs are completed.
4. After you fill out all the fields, click **Connect Account**.

#### Activate Notifications for Tests

Choose whether to activate Teams notifications for individual tests, or for all tests in your bucket.

**To activate Teams notifications for individual tests:**

1. Go to the API tests you want to monitor in your API Monitoring account, and select **Editor** on the left-hand side.
2. Click your environment settings to bring down the full options menu, and select **Integrations**.
3. Click the toggle for the Microsoft Teams service we just connected.

**To activate Teams notifications for all tests in a bucket:**

1. Navigate to **Bucket Settings** from your dashboard.
2. Under *Integrations Notifications*, use the toggle to enable or disable integrations with Microsoft Teams.

If you chose to get a notification whenever your test runs are completed, click **Run Now** and you should see a notification pop-up in your Microsoft Teams channel.

Having trouble configuring Microsoft Teams? [Contact our Support team](mailto:support-blazemeter@perforce.com?Subject=Microsoft%20Teams%20Integration%20Help).

### Grove Integration

[Grove](https://grove.io) is a hosted, private IRC server.

**Use when**: Posting test result notifications to IRC channels.

#### Configure Grove Integration

Follow these steps:

1. In Grove, select the settings for your channel, then the **Service Integrations** tab.
2. Select 'Webhooks (POST)' and **copy your service endpoint URL**.
3. In your BlazeMeter API Monitoring account, select **Connected Services**.
4. Select **Connect Grove**.
5. Enter a name for this channel to refer to later.
6. Enter the service endpoint URL copied from above.
7. Select whether or not to post a message for all test runs, all failed test runs, or after a certain number of consecutive failures for a specific location. Additionally, you may choose to post messages when a test returns to a successful state.
8. Click **Connect Account** to complete the integration.

Having trouble configuring Grove? [Contact our Support team](mailto:support-blazemeter@perforce.com?Subject=Grove%20Integration%20Help).

## Monitoring & Analytics

### Datadog Integration
Integrate Datadog with BlazeMeter API Monitoring to create Events and Metrics for use in Datadog dashboards and alerts.

**Use when**: Creating Events and Metrics for use in Datadog dashboards and alerts.

### New Relic Insights Integration
Connect New Relic Insights with BlazeMeter API Monitoring to collect metrics and transform them into actionable insights in New Relic dashboards.

**Use when**: Collecting metrics and transforming them into actionable insights in New Relic dashboards.

### Splunk Cloud Integration
Connect Splunk Cloud with BlazeMeter API Monitoring using HTTP Event Collector (HEC) to send test run and test step events to Splunk.

**Use when**: Sending test run and test step events to Splunk using HTTP Event Collector.

### Keen Integration
Connect BlazeMeter API Monitoring with Keen analytics API to get flexible analytics for automated API test results with event collections.

**Use when**: Getting flexible analytics for automated API test results with event collections.

### DX APM Integration
Connect DX Application Performance Management (CA APM) with BlazeMeter API Monitoring to collect metrics and view APM traces.

**Use when**: Collecting metrics and viewing APM traces.

## Service Management

### ServiceNow Integration

[ServiceNow](https://www.servicenow.com/) is a flexible online platform that helps customers transform their digital workflows. One of the ways it can be used is to help IT departments with incident management.

In this tutorial, we are going to show you how to create a webhook receiver (as a Scripted REST API) inside of ServiceNow, and how to set up Advanced Webhooks in your BlazeMeter API Monitoring account to send test result notifications to ServiceNow to automatically create incidents in case of an API failure.

**Use when**: Automatically creating incidents in ServiceNow when API tests fail using Scripted REST API.

#### Requirements

- A BlazeMeter account Advanced Webhooks integration enabled (go to your [Connected Services](https://runscope.com/connected-services) page, and search for "Advanced Webhooks". If you don't find it, please reach out to Support).
- [ServiceNow](https://www.servicenow.com/) account (you can create a [free developer account here](https://developer.servicenow.com/app.do#!/home)).

#### Creating a Scripted REST API in ServiceNow

Follow these steps:

1. Log in to your [ServiceNow account](https://www.servicenow.com/).
2. On the left-hand side search box, type **Scripted REST**. Under System Web Services, Scripted Web Services, click **Scripted REST APIs**.
3. Click **New** to create a new API service.
4. Name your API and an API ID (we use **API Monitoring Webhooks** for our example). You can leave Protection Policy as **-- None --**.
5. Click **Submit**.
6. You are taken back to the list of Scripted Web Services. Search for the API we just created and click it.
7. Scroll down to the Resources tab and click **New**.
8. Name your resource (we use **event**) and change the **HTTP method** to **POST**.
9. Scroll down to the **Script** section and add the following snippet:

```javascript
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
  var apiKey = request.queryParams['apiKey'];
  var secret = "<secret>";
  if (apiKey == secret) {
    var event = request.body.data;
    var inc = new GlideRecord('incident');
    inc.initialize();
    var short_description = "Runscope Webhook - ";
    short_description += event.test_name;
    inc.short_description = short_description;
    inc.description = event.bucket_name + " - " + event.test_name;
    inc.work_notes = "Test run URL: " + event.test_run_url;
    inc.number = event.test_run_id;
    inc.state = 1;
    inc.impact = 2;
    inc.urgency = 2;
    inc.priority = 2;
    // optional - specific person to assign the incident to
    // inc.assigned_to = "<email>";
    inc.assignment_group.setDisplayValue("<group>");
    var comments = "Runscope Test URL: " + event.test_url;
    comments += "\nRunscope Test Run URL: " + event.test_run_url;
    inc.comments = comments;
    inc.insert();
  } else {
    gs.warn("Invalid API Key for Runscope Webhook");
  }
  // Runscope expects a 200 status code response back
  response.setStatus(200);
})(request, response);
```

There are three variables in the script that you need to update:
- `<secret>` - required - a random string, such as a UID. Save this value as we'll use it later when setting up the BlazeMeter API Monitoring webhook.
- `<group>` - required - the group that you want to assign the incident to.
- `<email>` - optional - the specific person to assign the incident to.

If you want to customize the code and add more information to the incident, go to [BlazeMeter API Monitoring webhook payload](skill-blazemeter-api-monitoring://references/notifications.md) to see what properties are available.

10. In the **Security** tab, uncheck the **Requires authentication** checkbox (we use the **secret** GUID variable to protect access to the API).
11. Click **Submit**.
12. Back on Scripted API page, look for the **Base API Path** field for our newly created API.

Our API endpoint will look similar to this:
```
https://<yourInstanceName>.service-now.com/<baseApiPath>?apiKey=<secret>
```

#### Sending BlazeMeter API Monitoring Notifications to ServiceNow via Advanced Webhooks

Follow these steps:

1. Log in to your BlazeMeter API Monitoring account.
2. Click your profile on the top-right and select [Connected Services](https://www.runscope.com/connected-services).
3. Search for "Advanced Webhooks", and click **Connect**.
4. Name your integration (we use **ServiceNow Integration**), and select a **Threshold**. We recommend leaving **Notify when a test run is completed** as the threshold for now for testing purposes.
5. In the URL field, paste your API endpoint that you got from the previous section. It should look similar to this: `https://<yourInstanceName>.service-now.com/<baseApiPath>?apiKey=<secret>` Make sure to replace <secret> at the end with the secret UID you used in the script.
6. Click **Save Changes**.

#### Testing Our Integration

To test the integration, you need to enable it in one of our tests so BlazeMeter can start sending webhooks to ServiceNow.

Follow these steps:

1. Go to one of your buckets dashboard and create a new test.
2. In the test editor, open the environment settings, click the **Integrations** tab and toggle the ServiceNow integration we just created to **On**.
3. To run the test, click **Save & Run**.
4. Back in **ServiceNow**, on the left-hand side search box, type "Incidents".
5. Under the **Service Desk** section, click **Incidents**. You should see a new incident created on the top of the list with information from your API Monitoring test run.

The integration is complete. Now that we know the ServiceNow API and the BlazeMeter API Monitoring integration are working, remember to adjust the Advanced Webhooks thresholds so alerts are only sent when you want them to. Go to the [Connected Services](https://www.runscope.com/connected-services) page and click the edit icon next to your integration to change the threshold options, so you can configure how often you want to create incidents for API failures.

Having trouble configuring ServiceNow? [Contact our Support team](mailto:support-blazemeter@perforce.com?Subject=ServiceNow%20Integration).

### Statuspage Integration
Connect Statuspage with BlazeMeter API Monitoring to add API response times as custom metrics to service status pages.

**Use when**: Adding API response times as custom metrics to service status pages.

## CI/CD & Build Tools

### CircleCI Integration
Integrate BlazeMeter API Monitoring tests with CircleCI builds using Python scripts and Trigger URLs to change build status based on test results.

**Use when**: Integrating API Monitoring tests with CircleCI builds or changing build status based on test results.

### Codeship Integration
Integrate BlazeMeter API Monitoring tests with Codeship builds, including Codeship Pro with Docker support, using Python scripts and Trigger URLs.

**Use when**: Integrating API Monitoring tests with Codeship builds or using Codeship Pro with Docker support.

### Build/Deployment Integration

Trigger URLs allow you to initiate one or more tests from scripts, code and third-party services by making simple HTTP requests.

**Use when**: Initiating API Monitoring tests from scripts, code, and third-party services or configuring batch triggers and custom initial variables.

#### Initiating a Test Run with a Trigger URL

The Trigger URL responds to any GET or POST request made to it. If a third-party service supports webhooks, use the Trigger URL as the value when configuring the hook. You can find the Trigger URL for a test in the [Environment Settings](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html).

The `runscope_environment` parameter specifies which configuration settings to use for the given test run. The full Trigger URL can be found in the Trigger URL section of the [environment editor](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html). If the parameter is omitted, the [default environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html) for a test is used.

Each Trigger URL has a rate limit of 10 triggers over a 10 second period. If you exceed this rate limit the trigger URL will respond with an HTTP 429 status code.

**Response Format:**
The response includes information about the initiated test runs, including `test_run_id`, `test_url`, `test_run_url`, and `variables` used. The response also includes `runs_failed`, `runs_started`, and `runs_total` counts.

**Request:**
- GET: `https://api.runscope.com/radar/:trigger_id/trigger?runscope_environment=:environment_uuid`
- POST: `https://api.runscope.com/radar/:trigger_id/trigger?runscope_environment=:environment_uuid`

**Response:**
The response includes information about the initiated test runs, including test_run_id, test_url, test_run_url, and variables used.

#### Trigger URLs with Custom Initial Variables

By default, the Trigger URL will start a test run with the settings defined in the test editor. You can also start a test run with custom Initial Variables and callback URLs by passing parameters to the test's Trigger URL.

Any `key=value` parameters you send to a Trigger URL will be passed to your test as Initial Variables. The custom variables can be specified in URL parameters when making a `GET` request, or as form parameters when making a `POST` request. Variables that start with `runscope_` are reserved for specifying values to override other test settings.

**Initial Variable Precedence:**
Custom variables set in Trigger URLs take precedence over those specified in the test editor. If you're using Initial Variables in a [shared environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html#shared) or Initial Scripts, see [Variables - Evaluation Order](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html#variables).

**Request:**
- GET: `https://api.runscope.com/radar/:trigger_id/trigger?baseUrl=https://yourapihere.com&apiKey=abc123`
- POST: `https://api.runscope.com/radar/:trigger_id/trigger` (with form parameters in request body)

**Reserved Trigger URL Parameters:**
- `runscope_environment`: The UUID of the environment settings to use for this test run
- `runscope_notification_url`: The URL to notify when the test run completes
- `runscope_agent`: The UUID of the Radar agent used to execute this test run's requests
- `runscope_region`: The region code(s) for the locations to initiate a test run in

#### Batch Trigger URL: All Tests in a Bucket

You can trigger a test run for all tests within a bucket (similar to clicking 'Run All' from the test list) using the bucket-wide Trigger URL. Locate the URL by going to your test list page and selecting **Bucket Settings**.

The `runscope_environment` parameter specifies which configuration settings to use for the set of batch test runs. Since this is running different tests, you can only specify a shared environment UUID to use. If the parameter is omitted, the [default environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html) for a test is used.

**Request:**
- GET: `https://api.runscope.com/radar/bucket/:trigger_id/trigger`
- POST: `https://api.runscope.com/radar/bucket/:trigger_id/trigger`

#### Batch Trigger URL: Single Test with Multiple Initial Variable Sets

The Batch Trigger URL allows you to queue up to 50 test runs at one time using different sets of initial variables, specified in the request's body as JSON. A run will be created for each object in the array, creating initial variables for each of the attribute/value pairs. Each test will use its [default environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html#default) if the `runscope_environment` parameter is not specified, and parameters specified in the batch request take precedence over environment settings.

**Request:**
- POST: `https://api.runscope.com/radar/:trigger_id/batch`

**Sample Request Data:**
```json
[
  {
    "runscope_environment": "your_environment_uuid",
    "baseUrl": "http://staging.example.com",
    "apiKey": "xyzzy"
  },
  {
    "baseUrl": "https://prod.example.com",
    "apiKey": "123456"
  }
]
```

#### Using Trigger URLs with Third-party Services

Many services allow you to configure a webhook to be notified when a commit, build or deploy is completed. Here are instructions for using the Trigger URL with popular continuous integration, source control and hosting services:

- **AWS CodePipeline**: CodePipeline is a continuous delivery and release automation service from Amazon Web Services. BlazeMeter API Monitoring test steps can be integrated from the AWS CodePipeline Console. To add an API test to your CodePipeline workflow, create a new Action in your Pipeline. Choose 'Testing' as the Action category, and **Runscope API Monitoring** will be available as a Test provider
- **CircleCI**: You can read our CircleCI Integration tutorial for more information. Alternatively, you can also use CircleCI webhooks by adding the Trigger URL to your circle.yml file
- **Codeship**: You can read our Codeship Integration tutorial for more information
- **GitHub**: To start a test run after a commit has been received, enter the Trigger URL into a repo's WebHook URLs located under **Settings > Service Hooks**
- **Heroku**: To start a test after a successful Heroku deploy, register the Trigger URL by adding App Webhooks
- **Jenkins**: To initiate a test run as a build step, install the BlazeMeter API Monitoring Plugin from within Jenkins. Alternatively, you can use the Notification Plugin to initiate a test run after a Jenkins build
- **TeamCity**: Mangopay has created a plugin to add BlazeMeter API Monitoring tests to your TeamCity builds
- **Zapier**: Integrate with 1,000+ services including Jira, BitBucket, New Relic, Windows Azure, GitHub, Asana, Trello, Slack and more using the Runscope app on Zapier

## API Management & Gateway

### Amazon API Gateway Integration
Connect Amazon API Gateway with BlazeMeter API Monitoring to automatically create API tests by importing API specifications from AWS account.

**Use when**: Automatically creating API tests by importing API specifications from AWS account.

### Layer7 API Management Integration
Import API or microservices endpoints from Layer7 API Gateway into BlazeMeter API Monitoring for monitoring and testing.

**Use when**: Importing API or microservices endpoints from Layer7 API Gateway for monitoring and testing.

## Workflow Automation

### Zapier Integration

[Zapier](https://zapier.com/) automates interactions between the services you use. The [BlazeMeter API Monitoring Zapier app](https://zapier.com/apps/runscope/integrations) connects your BlazeMeter API Monitoring account data with over 1,000 other services including Jira, BitBucket, New Relic, Windows Azure, GitHub, Asana, Trello, Twilio SMS, Slack, and more.

**Use when**: Integrating API Monitoring with 1,000+ services via Zapier or connecting with Jira, BitBucket, GitHub, Asana, Trello, Slack, and other services.

#### 'New Completed Test Run' Trigger

This trigger fires on the completion of any API test (formerly known as 'Radar test') that has the associated webhook URL (provided by Zapier when creating the zap) registered with it. This is useful for receiving notifications of completed or failed test runs.

#### Using Filters to Trigger Only on Failed Test Runs

By default the trigger will execute on any completed test run. You can limit the trigger to just failed test runs using [filters](https://help.zapier.com/hc/en-us/articles/8496276332557-Add-conditions-to-Zaps-with-filters).

#### Triggering API Test Runs with Zapier Webhook App

Zapier provides a generic 'Webhook' app for executing HTTP requests as an action for a zap. In combination with an API test's [Trigger URL](skill-blazemeter-api-monitoring://references/integrations.md), you can initiate test runs from your zaps. Here are some quick links to get started with [GitHub](https://zapier.com/apps/github/integrations/webhook), [GitLab](https://zapier.com/apps/gitlab/integrations/webhook), and [Webhooks](https://zapier.com/apps/webhook/integrations) by Zapier.

## Testing Tools

### Ghost Inspector Integration

Integrate Ghost Inspector UI tests with BlazeMeter API Monitoring tests, including connecting accounts, adding UI test steps, creating assertions, variables, and scripts.

**Use when**: Integrating Ghost Inspector UI tests with API Monitoring tests, adding UI test steps to API tests, or combining UI and API testing workflows.

### Overview

[Ghost Inspector](https://ghostinspector.com) is a powerful but simple tool for automated website testing. Ghost Inspector tests check specific functionality in your website or application and execute continuously from the cloud and alert you if anything breaks.

When connected, you can add Ghost Inspector test steps to your API Monitoring tests, allowing you to combine UI testing with API testing in a single workflow.

### Connecting Your Accounts

**Steps:**

1. From your API test, select **Editor** from the left-hand side or the **Edit Test** link under the test name
2. Expand the **Environment** section and select **Integrations**
3. Locate the Ghost Inspector logo and click **Connect Ghost Inspector**
4. Complete the authorization flow to grant BlazeMeter API Monitoring access to your Ghost Inspector account

**Note**: If you have multiple Ghost Inspector accounts, you can create multiple connected services.

### Adding UI Test Steps

Once connected, a new option will appear in the **Test Steps** editor allowing you to add a Ghost Inspector test step as part of your API test. After adding the step, select the test you want to execute from the dropdown list.

### Creating Assertions

Assertions can be created on the data generated by the Ghost Inspector test step. A JSON object containing data from the test run can be evaluated using the [JSON syntax used in assertions for HTTP request steps](skill-blazemeter-api-monitoring://references/scripting.md). An assertion for the status of the UI test run is created by default.

### Creating Variables

Data from the test run can be extracted and stored in a [variable](skill-blazemeter-api-monitoring://references/advanced-features.md) for use in subsequent requests. The same syntax for extracting data from HTTP request steps can be used for extracting data from the Ghost Inspector test run JSON result.

### Creating Scripts

To evaluate the Ghost Inspector test run result JSON with a Script, access the `request.body` value:

```javascript
// parse JSON result data into object
var data = JSON.parse(request.body);
```

After parsing the data, you can access it to create script [assertions](skill-blazemeter-api-monitoring://references/scripting.md) or [variables](skill-blazemeter-api-monitoring://references/scripting.md) using the same code as you use for scripts attached to HTTP request steps.

### Changing the Start URL

The start URL of your Ghost Inspector test can be optionally overridden with an alternate URL. You can enter a URL, or pass variables from BlazeMeter API Monitoring into your Ghost Inspector test as a start URL. [Learn more about reusing Ghost Inspector tests across different environments](https://docs.ghostinspector.com/reusing-tests-different-environments/).

### Documentation References

For detailed information about Ghost Inspector integration, use the BlazeMeter MCP help tools:

**Ghost Inspector Integration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-ghost-inspector-integration`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-ghost-inspector-integration"]}`

---

## Analytics & Monitoring

### Statuspage Integration

[Statuspage](https://www.statuspage.io/) provides service status pages with support for custom metrics. When connected, API response times can be added to your status pages and updated as tests are completed.

**Use when**: Adding API response times to status pages or displaying API monitoring metrics on public status pages.

#### Create a Custom Metric

Follow these steps:

1. [Sign in](https://manage.statuspage.io/) to your Statuspage account
2. Select **Public Metrics** from the left-hand navigation
3. Click **Add a Metric** and select **I'll submit my own data for this metric**
4. For the metric name and suffix, we recommend **API Response Time** and **ms**
5. Once created, you will see some sample code that contains the API key, page ID and metric ID that you will use when configuring the integration

#### Connect Statuspage

Once you have created the custom metric, return to BlazeMeter API Monitoring to complete the integration:

1. Sign in to your BlazeMeter API Monitoring account
2. Click on the **Profile & Account Settings** icon on top-right, and choose **Connected Services**
3. Find and click on **Connect StatusPage.io** from the list of services
4. Enter the API key, page ID and metric ID from values copied from the Statuspage code sample
5. After saving, enable the integration from the test-specific or shared environment settings of the test you'd like to generate the data

You can disconnect Statuspage at any time by disconnecting the service on the Connected Services page.

#### Recommended Setup

Because of the way Statuspage interpolates custom metrics, you'll want to make sure to only send metrics from tests running in a single location. If you have an existing test set up that runs from multiple locations, you can add another environment to that test specifically for sending data to Statuspage. Once the environment is created, select a single location in the location settings, enable the integration, and create a 1 or 5 minute schedule using this environment.

Once data is flowing into your Statuspage account, you can configure advanced display settings. For best results, set the "Y-Axis" minimum to **0**, "Rollup Display" to **Mean**, and "Data Display > Decimal Places" to **0**.

### Documentation References

For detailed information about Statuspage integration, use the BlazeMeter MCP help tools:

**Statuspage Integration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-statuspage-integration`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-statuspage-integration"]}`

---

## API Gateway Integrations

### Layer7 API Management Integration

[Layer7 API Management](https://www.ca.com/us/products/api-management.html) (formerly known as CA API Management) is an API Management solution that allows you to create, secure, deliver and manage the full lifecycle of APIs and microservices at scale. It includes tools for API creation, management, gateway, security, and analytics.

By connecting Layer7 API Management with BlazeMeter API Monitoring, you can import any API or microservices endpoints from your Layer7 API Gateway in seconds and start monitoring your systems, collecting API data, and transforming them into actionable insights.

**Use when**: Importing API endpoints from Layer7 API Gateway into BlazeMeter API Monitoring or monitoring Layer7-managed APIs.

**The Layer7 API Management integration requires a qualifying plan. Contact Sales to get started.**

#### Requirements

- BlazeMeter API Monitoring Account
- Layer7 API Gateway - Version 9.2 or higher (you can [sign up for a free 30-day trial](https://transform.ca.com/API-Management-Trial.html))
- API Test Toolkit - [Click here to download](https://storage.googleapis.com/runscope-downloads/API_Test_Toolkit.sskar)

#### Install the API Test Toolkit for Layer7 API Gateway

Follow these steps:

1. Install the API Test Toolkit for the Layer7 API Gateway. You can [download the toolkit (.sskar) file here](https://s3.amazonaws.com/runscope-downloads/API_Test_Toolkit.sskar)
2. Log in to your Policy Manager and navigate to **Tasks, Extensions and Add-Ons, Manage Solution Kits**
3. In the Manage Solution Kit dialog, click **Install**
4. Select the API Test Toolkit .sskar file and click **Next**
5. Follow the next steps in the wizard

#### Import API Management Endpoints into BlazeMeter API Monitoring

Follow these steps:

1. In your BlazeMeter API Monitoring account, go to a bucket's dashboard and select **Import Test** at the bottom
2. Select **CA API Gateway** from the list and click **Connect API Gateway Account**

#### Connect Your Layer7 API Gateway Account

Fill in the fields with your CA API Gateway URL, username and password, and select **Connect Account**.

#### Select Endpoints and Folders

After successfully connecting to your CA API Gateway URL, you should see a list of all available folders and endpoints.

You can select a folder to import all endpoints inside it, or expand each folder to select individual endpoints. After you finish selecting the folders/endpoints you want to import, select *Import Selected Tests*.

If the import was successful, you should see a list of all the tests that were created inside of BlazeMeter API Monitoring. The tests follow the same naming convention as the Layer7 API Gateway folders. Folders that contain more than 50 endpoints are split into multiple tests (for example, AuthorizationServer has 120 endpoints, it'll be split into AuthorizationServer 1 and 2 with 50 endpoints each, and AuthorizationServer 3 with the remaining 20 endpoints).

The next steps would be to create additional [assertions](skill-blazemeter-api-monitoring://references/scripting.md) for each test to validate their data, and set them on a [schedule](skill-blazemeter-api-monitoring://references/configuration.md).

Having trouble configuring the Layer7 API Management integration? [Contact our support team](mailto:support-blazemeter@perforce.com?Subject=Layer7%20API%20Management%20Integration%20Help).

### Documentation References

For detailed information about Layer7 API Management integration, use the BlazeMeter MCP help tools:

**Layer7 API Management Integration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-layer7-api-management-integration`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-layer7-api-management-integration"]}`

---

## Configuration Steps

### General Integration Setup

1. **Select Integration**: Choose the integration you want to configure
2. **Get Credentials**: Obtain API keys, webhooks, or credentials from the third-party service
3. **Configure in BlazeMeter**: Set up integration in API Monitoring settings
4. **Test Integration**: Verify integration works correctly
5. **Configure Triggers**: Set when integration should be triggered

### Best Practices

- **Secure Credentials**: Store credentials securely using Secrets Management
- **Test Before Production**: Test integrations thoroughly before production use
- **Monitor Integration Health**: Regularly check integration status
- **Document Configuration**: Document integration setup and configuration
- **Update Credentials**: Rotate credentials regularly for security

---

## Documentation References

For detailed information about API Monitoring integrations, use the BlazeMeter MCP help tools:

**Specific Integrations** (verified help_ids):
- **Slack**: `api-monitoring-slack-integration` 
- **PagerDuty**: `api-monitoring-pagerduty-integration`
- **Microsoft Teams**: `api-monitoring-microsoft-teams-integration`
- **VictorOps**: `api-monitoring-victorops-integration`
- **Grove**: `api-monitoring-grove-integration`
- **Zapier**: `api-monitoring-zapier-integration`
- **OpsGenie**: `api-monitoring-opsgenie-integration`
- **ServiceNow**: `api-monitoring-servicenow-integration`
- **Build/Deployment**: `api-monitoring-build-deployment-integration`

**Other Available Integrations** (help_ids follow similar naming pattern):
- **Datadog**: `api-monitoring-datadog-integration`
- **ServiceNow**: `api-monitoring-servicenow-integration`
- **Zapier**: `api-monitoring-zapier-integration`
- **Amazon API Gateway**: `api-monitoring-amazon-api-gateway-integration`
- **BigPanda**: `api-monitoring-bigpanda-integration`
- **CircleCI**: `api-monitoring-circleci-integration`
- **Codeship**: `api-monitoring-codeship-integration`
- **DX APM**: `api-monitoring-dx-application-performance-management-integration`
- **Ghost Inspector**: `api-monitoring-ghost-inspector-integration`
- **Grove**: `api-monitoring-grove-integration`
- **Keen**: `api-monitoring-keen-integration`
- **Layer7**: `api-monitoring-layer7-api-management-integration`
- **Microsoft Teams**: `api-monitoring-microsoft-teams-integration`
- **New Relic Insights**: `api-monitoring-new-relic-insights-integration`
- **OpsGenie**: `api-monitoring-opsgenie-integration`
- **Splunk Cloud**: `api-monitoring-splunk-cloud-integration`
- **Statuspage**: `api-monitoring-statuspage-integration`
- **VictorOps**: `api-monitoring-victorops-integration`

**Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-slack-integration", "api-monitoring-pagerduty-integration", "api-monitoring-microsoft-teams-integration", "api-monitoring-victorops-integration", "api-monitoring-grove-integration", "api-monitoring-zapier-integration", "api-monitoring-opsgenie-integration", "api-monitoring-servicenow-integration", "api-monitoring-build-deployment-integration", "api-monitoring-datadog-integration", "api-monitoring-amazon-api-gateway-integration", "api-monitoring-bigpanda-integration", "api-monitoring-circleci-integration", "api-monitoring-codeship-integration", "api-monitoring-dx-application-performance-management-integration", "api-monitoring-ghost-inspector-integration", "api-monitoring-keen-integration", "api-monitoring-layer7-api-management-integration", "api-monitoring-new-relic-insights-integration", "api-monitoring-splunk-cloud-integration", "api-monitoring-statuspage-integration"]}`

