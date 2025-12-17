# APM Integrations

## Overview

BlazeMeter integrates with Application Performance Monitoring (APM) tools to provide comprehensive performance insights by combining load test results with application performance metrics.

**Use when**: Integrating APM tools with BlazeMeter performance tests to visualize application performance metrics alongside load test results.

BlazeMeter integrates with a variety of tools to enhance your performance testing capabilities. These integrations can help you monitor, manage, and optimize your tests by providing connections to application performance management (APM) tools and data management solutions.

### Application Performance Management (APM)

BlazeMeter supports integration with many APM tools, enabling you to gain deeper insights into the performance of your applications during testing. For more information, see [APM Integration](https://help.blazemeter.com/docs/guide/performance-apm-integration.html).

### Data Management Solutions

BlazeMeter's integration with data management solutions like Delphix enables you to use data virtualization together with performance testing. Prepare a test server using virtualized data to run a Performance test against. Before and after running the test, you can start and stop your virtual databases and refresh data on the test server.

### Documentation References

For detailed information about integrations overview, use the BlazeMeter MCP help tools:

**Integrations Overview**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-overview.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-overview.htm"]}`

---

## AppDynamics

You can incorporate critical metrics from AppDynamics, a leading provider of application performance intelligence, into your BlazeMeter test scenarios to identify problem areas faster. This solution works by adding AppDynamics' monitoring profiles to BlazeMeter test scenarios.

The integration with AppDynamics is designed to help developers address issues that impact application performance with accuracy and consistency. You can incorporate critical metrics from AppDynamics into your BlazeMeter test scenarios to identify problem areas faster. You can then identify various metric groups associated with your applications, such as mobile, end-user experience, or business transactions. After that, you can select specific metrics, such as average response time, calls per minute, and errors per minute.

By integrating these metrics with BlazeMeter's timeline graphs, application performance management (APM) data can be plotted on the same graph as the test data, alongside metrics such as concurrent users, throughput, and latency, allowing you to discover where, when, and why problems occur.

Once identified, you can apply a fix and then validate it by testing as many times as you need to get sufficient information from AppDynamics. This method ensures that the fix was applied and that the problem no longer exists.

Not only are you able to view your application monitoring data alongside your user experience and performance data, but this data is accessible to you even after the test has ended.

**Use when**: Integrating AppDynamics APM with BlazeMeter performance tests, incorporating critical metrics into test scenarios, or visualizing APM metrics alongside performance test results.

### Prerequisites

- You are assigned either a manager or a tester role.
- If you are using AppDynamics' on-premise solution, the BlazeMeter account to be integrated with AppDynamics requires a [BlazeMeter private agent](skill-blazemeter-private-locations://references/introduction.md) to be installed with network access to the AppDynamics console. The private agent will communicate with AppDynamics' console to retrieve the list of available applications and metrics and then transmit the data you choose to our back-end during tests.
- If you are using AppDynamics cloud console, BlazeMeter uses its own servers to communicate with AppDynamics, and therefore no on-premise agents are required.

### Adding AppDynamics Credentials

An AppDynamics credential specifies the URL of the endpoint and its required authentication parameters in one definition.

1. Navigate to BlazeMeter Settings -> **Workspaces** -> **Credentials**, click the **Add Credential** icon (+), and select **AppDynamics**.
2. Fill in the following form:

   The AppDynamics integration connects to an AppDynamics Controller to retrieve configuration data and send back information about the monitored environment.

   - **Credential Name**: A unique name for the credential, without spaces or special characters.
   - **Harbor ID**: A unique key associated with a private location that can be found under **BlazeMeter Settings** -> **Workspaces** -> **Private Locations** -> <Your Private Location> -> **Private Location Details**, under the **Id** column.
   - **Controller Host**: The hostname or IP address of the AppDynamics Controller, for example, 192.168.1.22 or myhost or myhost.abc.com. This is the same host used to access the AppDynamics browser-based user interface.
   - **Controller Port**: The port on which the Controller listens for integration traffic.
   - **Choose Authentication Method**: Either **Username/Password** or **Access Token**.
     - **Username/Password**:
       - **Account Name**: The name of the account listed in the Controller.
       - **Username**: The name of the user listed in AppDynamics.
       - **Access Key**: A unique key associated with the Controller account.
     - **Access Token**:
       - **Access Token**: A unique key associated with the Controller account, generated in AppDynamics either from the Controller UI or through an API.

3. When you have completed the form, click **Validate**, then **Next**. The credential is created.

### Adding AppDynamics to Performance Tests

1. Create or edit a performance test.
2. In the test configuration window, scroll down to the **Integrations** section and select **AppDynamics**:
   - If a credential exists, click **Next**.
   - If a profile does not exist, fill in the following form:

     The AppDynamics integration connects to an AppDynamics Controller to retrieve configuration data and send back information about the monitored environment.

     - **Credential Name**: Type a unique name for the credential, without spaces or special characters.
     - **Harbor ID**: A unique key associated with a private location that can be found under **BlazeMeter Settings** -> **Workspaces** -> **Private Locations** -> <Your Private Location> -> **Private Location Details**, under the **Id** column.
     - **Controller Host**: The hostname or IP address of the AppDynamics Controller, for example, 192.168.1.22 or myhost or myhost.abc.com. This is the same host used to access the AppDynamics browser-based user interface.
     - **Controller Port**: The port on which the Controller listens for integration traffic.
     - **Choose Authentication Method**: Either **Username/Password** or **Access Token**.
       - **Username/Password**:
         - **Account Name**: The name of the account listed in the Controller.
         - **Username**: The name of the user listed in AppDynamics.
         - **Access Key**: A unique key associated with the Controller account.
       - **Access Token**:
         - **Access Token**: A unique key associated with the Controller account, generated in AppDynamics either from the Controller UI or through an API.

3. When you have completed the form, click **Validate**, then **Next**.
4. Create a profile (preset) and configure the metrics to retrieve during the load test. These metrics appear in visual reports and correlate to the performance KPIs.
5. Click **Next** and **Finish**.

### Result

After running a test with the AppDynamics profile configured, you can plot AppDynamics KPIs in BlazeMeter's timeline report. Note the AppDynamics KPIs in the KPI tree.

### Features

- Real-time metric visualization
- Application performance correlation
- Business transaction monitoring
- Performance baseline comparison
- Identify problem areas faster by incorporating critical metrics from AppDynamics into BlazeMeter test scenarios
- Identify various metric groups associated with your applications, such as mobile, end-user experience, or business transactions
- Select specific metrics, such as average response time, calls per minute, and errors per minute
- Plot APM data on the same graph as test data, alongside metrics such as concurrent users, throughput, and latency
- Access application monitoring data even after the test has ended

### Documentation References

For detailed information about AppDynamics integration, use the BlazeMeter MCP help tools:

**AppDynamics**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-integrate-with-appdynamics`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-integrate-with-appdynamics"]}`

---

## Datadog

BlazeMeter provides an integration with Datadog, an Application Performance Monitoring (APM) tool designed for analyzing the performance of application servers, database servers, and web services. You can use this integration for new or existing tests.

This integration supports the following integration modes:

- **Display Datadog Metrics in BlazeMeter**: Integrate your BlazeMeter tests with a specific Datadog profile and the scopes it contains. You can configure a test to send requests to your monitored servers, and view metrics collected by the Datadog monitoring tool in the BlazeMeter **Timeline Report**.
- **Display BlazeMeter Metrics in Datadog**: Send test results to the Datadog platform so that you can view and manipulate the test data in Datadog dashboards and the Metrics Explorer. This mode provides real-time reporting of test metrics such as latency, number of hits, users, maximum response time, connect time, and so on.
- **Display Both Ways**: Set up this bidirectional mode to send performance test metrics from Datadog to BlazeMeter, and vice versa.

**Use when**: Integrating Datadog APM with BlazeMeter, configuring bidirectional integration modes, metric display, or tag configuration.

### Configure a Datadog Key

To use this integration, you first need to create a key associated with a build profile and Datadog API and application keys.

**Steps:**

1. Navigate to the BlazeMeter Test Configuration page.
2. In the **Integrations** section, click **Datadog APM**.
3. Either choose an existing profile: Or create a new profile by entering the following details:

   **Basic Configuration:**
   - **Key Name**: Name of the key you want to create and reference in BlazeMeter.
   - **Datadog APM URL**: The full URL to access your Datadog environment (exclude the trailing / in your URL, for example, http://yourHostAtDatadog.com).
   - **App Key**: Authentication key, used in conjunction with your organization's API key, that gives users access to Datadog's programmatic API.
   - **API Key**: Authentication key granting BlazeMeter access to Datadog's API for data transmission and retrieval. API keys are unique to your organization. An API key is required by the Datadog Agent to submit metrics and events to Datadog. For more information, see [Datadog documentation](https://docs.datadoghq.com/).

   **Advanced Configuration:**
   - **Harbor ID**: The private location to use to run the APM functionality (for information where to get this value, see [Where can I find the Harbor ID and Ship ID?](skill-blazemeter-private-locations://references/management.md)). If you're using Datadog in the cloud, you don't need to provide the Harbour ID. The integration will work seamlessly without it.

4. You have completed the Datadog key step in the setup wizard. You can click **Next** to proceed to the **Select Metrics** step in the wizard.

### Display Datadog Metrics in BlazeMeter

Choose the **Display Datadog info in BM** integration mode to pull APM metrics from Datadog according to your profile setup to view in the BlazeMeter [Timeline Report](skill-blazemeter-performance-testing://references/reporting.md).

**Prerequisites**: A Datadog key is configured (see [Configure a Datadog Key](#configure-a-datadog-key)).

**Steps:**

1. In the Datadog integration setup wizard, after completing the Datadog key step, click **Next**. The **Select Metrics** screen opens. Here you can select your metrics and construct your profile. You specify your entity type and the metrics to include in the [Timeline Report](skill-blazemeter-performance-testing://references/reporting.md).
2. Select the **Datadog info in BM** option.
3. From the dropdown, select a reserved tag key for example, **Hosts**, and an associated entity.
4. From the **Select Entity** dropdown, select one or more metrics, and click **Next**. This action lets you preview what your profile will monitor.
5. Provide a profile name and click **Save Profile** to save it as a new profile for future tests.
6. Upon saving your profile, you'll see the following screen, allowing you to choose the profile(s) you want. To apply the profile(s) to your test, click **Apply**.

Your test is now integrated with Datadog.

To view the test metrics from Datadog, go to the [Timeline Report](skill-blazemeter-performance-testing://references/reporting.md), scroll to the bottom of the available KPIs, and then expand the Datadog section. You will then see all the metrics you selected listed there. You can click the checkboxes to add them to your report.

### Display BlazeMeter Metrics in Datadog

Choose the **Display BM info in Datadog** integration mode to push metrics from BlazeMeter into Datadog according to your profile setup. You assign tags to the transmitted data, so that you can use them to filter and group your data in your Datadog platform. Tags can be used to include or exclude data.

When configured, BlazeMeter sends the following load test metrics to Datadog:

| Metric name | Description |
|-------------|-------------|
| `bzm.bandwidth.avg` | The average bandwidth usage measured in bytes per second during a BlazeMeter load test. |
| `bzm.connectTime.avg` | The average time taken to establish a connection with the server during a BlazeMeter load test. |
| `bzm.errors` | The total count of errors encountered during a BlazeMeter load test. |
| `bzm.errors.avg` | The average number of errors encountered during a BlazeMeter load test. |
| `bzm.hits` | The count of HTTP requests or transactions executed during a BlazeMeter load test. |
| `bzm.hits.avg` | The average number of HTTP requests or transactions per second during a BlazeMeter load test. |
| `bzm.latency.avg` | The average latency, representing the time delay between sending a request and receiving the first byte of the response during a BlazeMeter load test. |
| `bzm.responseTime.avg` | The average response time for all executed requests during a BlazeMeter load test. |
| `bzm.responseTime.max` | The maximum response time recorded for executed requests during a BlazeMeter load test. |
| `bzm.responseTime.min` | The minimum response time recorded for executed requests during a BlazeMeter load test. |
| `bzm.responseTime.percentile.50` | The 50th percentile response time, indicating the point below which 50% of the executed requests fall in a BlazeMeter test. |
| `bzm.responseTime.percentile.90` | The 90th percentile response time, indicating the point below which 90% of the executed requests fall in a BlazeMeter test. |
| `bzm.responseTime.percentile.95` | The 95th percentile response time, indicating the point below which 95% of the executed requests fall in a BlazeMeter test. |
| `bzm.responseTime.percentile.99` | The 99th percentile response time, indicating the point below which 99% of the executed requests fall in a BlazeMeter test. |
| `bzm.users` | The number of virtual users or simulated clients generating load in a BlazeMeter test scenario. |

**Prerequisites**: A Datadog key is configured (see [Configure a Datadog Key](#configure-a-datadog-key)).

**Steps:**

1. In the Datadog integration setup wizard, after you've successfully added your key, click **Next**.
2. Select **Display BM info in Datadog**.
3. Enable **Send breakdown by label** to send your Blazemeter labels to Datadog. When enabled, your labels appear under **Tag** next to the **masterid** in Datadog.
4. In the **Tracking tags** text box, type one or more tags. To familiarize yourself with Datadog tagging requirements, see [Datadog documentation](https://docs.datadoghq.com/).
5. Click **Next** to preview what your profile will monitor. Provide a profile name and save it as a new profile for future tests.
6. Provide a profile name and click **Save Profile** to save it as a new profile for future tests.
7. Upon saving your profile, you'll see the following screen, allowing you to choose the profile(s) you want. To apply the profile(s) to your test, click **Apply**.

Your test is now integrated with Datadog.

To view the load test metrics in Datadog, go to the Dashboard or Metrics Explorer.

### Display Both Ways

Choose the **Both Ways** integration mode to push metrics from BlazeMeter into Datadog and vice versa, according to your profile setup. This configuration combines the Display Datadog metrics in BlazeMeter and Display BlazeMeter metrics in Datadog modes.

**Prerequisites**: A Datadog key is configured (see [Configure a Datadog Key](#configure-a-datadog-key)).

**Steps:**

1. In the Datadog integration setup wizard, after you've successfully added your key, click **Next**.
2. Select the **Both Ways** option.
3. Enable **Send breakdown by label** to send your Blazemeter labels to Datadog. When enabled, your labels appear under **Tag** next to **masterid** in Datadog.
4. In the **Tracking tags** text box, type one or more tags.
5. From the dropdown, select a reserved tag key for example, **Hosts**, and an associated entity.
6. From the **Select Entity** dropdown, select one or more metrics.
7. Click **Next** to preview what your profile will monitor. Provide a profile name and save it as a new profile for future tests.
8. Upon saving your profile, you'll see the following screen, allowing you to choose the profile(s) you want. To apply the profile(s) to your test, click **Apply**.

Your test is now integrated with Datadog.

You can view the load test metrics in BlazeMeter and in Datadog.

### Integration Modes

- **Display Datadog Metrics in BlazeMeter**: Pull APM metrics from Datadog to view in BlazeMeter Timeline Report
- **Display BlazeMeter Metrics in Datadog**: Push metrics from BlazeMeter into Datadog dashboards and Metrics Explorer
- **Both Ways**: Bidirectional mode combining both integration modes

### Features

- APM trace correlation
- Custom metric tags
- Dashboard integration
- Alert correlation
- Real-time reporting of test metrics
- Tag-based filtering and grouping

### Documentation References

For detailed information about Datadog integration, use the BlazeMeter MCP help tools:

**Datadog**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-integrate-with-datadog`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-integrate-with-datadog"]}`

---

## Delphix

BlazeMeter's integration with Delphix enables you to use data virtualization together with performance testing. Prepare a test server using Delphix data to run a Performance test against. Before and after running the test, you can start and stop your virtual databases and refresh data on the test server.

**Use when**: Integrating Delphix data virtualization with BlazeMeter performance tests or managing database refresh and start/stop operations.

### Overview

BlazeMeter's integration with Delphix enables you to use data virtualization together with performance testing. Prepare a test server using Delphix data to run a Performance test against. Before and after running the test, you can start and stop your virtual databases and refresh data on the test server.

**Overview:**
1. Create a Private Location Agent
2. Create Delphix keys and profiles
3. Use Delphix data with a performance test

### Create a Private Location Agent

Contact the Workspace manager to create the Private Location. If the Delphix server is not exposed to the internet, run the Delphix server and the BlazeMeter Private Location Agent on the same host.

1. Log into your BlazeMeter account as a workspace manager
2. Navigate to **Settings > Workspace > Private Locations**
3. Follow the procedure described in [Creating a Private Location](https://help.blazemeter.com/docs/guide/private-locations-create.html). Under **Location name** enter, for example, "Delphix Integration". In the **Set Up the Functionalities** step, select **Delphix Integration**
4. Follow the procedure described in [Installing a BlazeMeter Agent for Docker](https://help.blazemeter.com/docs/guide/private-locations-install-blazemeter-agent-for-docker.html). Click **Add Agent**. Under **Name**, enter, for example, "Delphix Agent". BlazeMeter generates and displays a Docker command. Click **Copy Command** and paste it in the Agent's terminal and run it. Open Docker Desktop and look at the dashboard to confirm that the "bzm crane component" is running
5. Return to **Settings > Workspace > Private Locations** in BlazeMeter and verify that the Private Location has fully downloaded and is running

### Create a Delphix Key

Credentials are shared within a workspace.

The Workspace manager can set up credentials (Delphix key) as part of the workspace Settings. A tester can create a Delphix key while configuring a Performance test.

1. Open the **Settings > Workspace > Private Location** window and view the Private Location descriptions to verify it has been set up for Delphix and that is it running.
2. Copy the **Agent ID**, you will need it when you are prompted to enter the **Harbor ID**.
3. Do one of the following two options:
   - If you are a workspace manager: Go to **Settings > Workspace > Credentials**. Click the **Plus** to add new credentials. Select **Delphix**.
   - If you are a tester: Edit the Performance test configuration. Scroll down to **Integrations**, and select **Delphix**. The **Delphix Integration** dialog opens. Select **Create a New Delphix Key**.
4. Fill in the following fields:
   - **Key Name**: Give the key a name that helps your team members recognize which credentials to choose.
   - **Data Control Tower URL**: The full URL to access your Delphix environment. Do not include a trailing slash!
   - **Token**: The Delphix authentication key granting BlazeMeter access to the Delphix API.
   - **Harbor ID**: The Agent ID of the BlazeMeter Private Location to use to communicate with the Delphix server. For information where to get this value, see [Where can I find the Harbor ID and Ship ID?](skill-blazemeter-private-locations://references/management.md).
5. Confirm the dialog.

### Managing Delphix Keys

To manage Delphix keys, Navigate to **Settings > Workspace > Credentials**.

- Each Delphix key is listed with its type ("Delphix"), name, and token.
- To delete a Delphix key, click the **Delete** button in its row.

### What is a Delphix Profile?

Each Delphix profile can perform one operation against the Delphix server:
- either refreshing data,
- or starting or stopping the server.

After the Workspace Admin has set up the Private Location, you as tester create Delphix profiles straight from the test configuration. Create multiple profiles, one for each operation. You can use profiles in multiple tests in the workspace.

Navigate to **Settings > Workspace > Profiles** to view existing profiles. As the Workspace manager, you can also delete profiles here.

### Use Delphix Data with a Performance Test

After the manager has set up the Private Location, you can use Delphix profiles in your Performance test to control test data.

1. Log on to BlazeMeter and open your Performance test.
2. Edit the test configuration, scroll down to Integrations, and select **Delphix**. The Delphix Integration dialog opens.
3. Select a Delphix Key (or [create one](skill-blazemeter-integrations://references/apm.md)) and click **Next**.
4. Build a profile:
   - Select a virtual database.
   - Select one Entity: **Database**, **Snapshot**, or **Bookmark**.
   - Select an Operation:
     - For Database only: Select either **start** or **stop**.
     - For Snapshot only: Select a database snapshot from which to refresh.
     - For Bookmark only: Select a bookmark from which to refresh.
5. Click **Next**.
6. Enter a **Name** for this profile. Name the profiles so your team members recognize which operation they perform. For example, "vdb1 start", "test database stop", "vdb1 snapshot July 3", "v-db-2 refresh from beginning".
7. Select profiles to execute before and after this test runs. You can select several profiles.

### Features

- Database refresh automation
- Environment provisioning
- Data snapshot management
- Test data preparation
- Start/stop virtual database operations
- Bookmark-based data refresh

---

## New Relic Integrations

Learn how BlazeMeter integrates with the New Relic observability platform to provide insight on application and infrastructure performance during and after load testing.

**Use when**: Integrating New Relic with BlazeMeter performance tests or monitoring application and infrastructure performance during load testing.

### Overview

BlazeMeter supports several integrations with New Relic:

- **New Relic APM**: Application performance monitoring integration
- **New Relic Infrastructure**: Infrastructure monitoring integration
- **New Relic Insights Into API Monitoring**: API monitoring metrics integration

You can combine multiple profiles in a test configuration. For example, you can combine one or more New Relic Infrastructure profiles with other APM profiles (including New Relic APM) in the same test.

### View New Relic KPIs in Timeline Report

You can view your application and infrastructure monitoring data alongside your user-experience and performance data in timeline reports during or at any time after test runs. With BlazeMeter, you can always access past test data, compare between past results or even compare past results to real time results.

### New Relic Insights Into API Monitoring

By connecting New Relic with BlazeMeter API Monitoring, you can collect metrics from your API tests in BlazeMeter, and transform them into actionable insights about your applications in New Relic.

### Documentation References

For detailed information about New Relic integrations, use the BlazeMeter MCP help tools:

**New Relic Integrations Overview**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-new-relic.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-new-relic.htm"]}`

---

## New Relic APM

Learn how to set up a New Relic APM integration with your BlazeMeter performance tests.

**Use when**: Integrating New Relic APM with BlazeMeter performance tests, configuring API keys, application selection, or KPI configuration.

### Overview

New Relic is an industry leader in the field of application performance management (APM), the monitoring and management of the performance and availability of software applications. The BlazeMeter integration with New Relic enables developers to easily monitor their application performance levels while load testing. You can evaluate the end-user experience and application system KPIs (Key Performance Indexes) using a single dashboard.

The New Relic APM integration lets you diagnose performance-related problems, apply fixes, and restart the cycle as needed.

You can view your application monitoring data alongside your end-user experience and performance data, and access this data after testing ends.

### Prerequisites

- You have a New Relic account.
- You are familiar with New Relic application performance monitoring.
- You have generated a REST API key in New Relic.
- You have configured one or more applications (entities) in New Relic.

For more information, see the [New Relic documentation](https://docs.newrelic.com/).

### Setup

1. Log in to your New Relic account and copy your New Relic REST API key.
2. Log in to BlazeMeter and do one of the following:
   - Click **Create Test** and scroll down to the **Integrations** section.
   - Open an existing performance test, click the **Configurations** tab, and scroll down to the **Integrations** section.
3. Click **New Relic APM**.
4. Fill in the following fields:
   - **Select which New Relic API key to use**: Select **Create a new New Relic API Key**.
   - **New Relic key title**: Type a name for your New Relic API key.
   - **New Relic API key**: Paste your New Relic REST API key.
5. Click **Next**.
6. Under **Build profile**, select **Applications**.
7. Select the required application. The key performance indicators appear automatically according to your New Relic application profile settings.
8. Click **Select Items** and select the KPIs to include in the BlazeMeter Timeline Report. As you click each item, they are added to the list of items that will be included in the report.
9. Click **Next**.
10. Enter a new profile name, and click **Save Profile**. A profile is basically a preset that is kept for your following tests, so you do not have to choose all the different metrics every time you run a test.
11. Click **Apply**.

### Result

Your application performance monitoring data will appear in the BlazeMeter Timeline Report as soon as you run your load test. You can now diagnose performance-related problems, apply fixes and start the cycle all over again.

### Features

- Application performance monitoring
- KPI tracking and visualization
- Transaction trace correlation
- Performance baseline comparison

### Documentation References

For detailed information about New Relic APM integration, use the BlazeMeter MCP help tools:

**New Relic APM**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-new-relic-apm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-new-relic-apm"]}`

---

## New Relic Infrastructure

Integrate New Relic Infrastructure with BlazeMeter to monitor infrastructure metrics alongside performance test results.

**Use when**: Integrating New Relic Infrastructure with BlazeMeter or monitoring infrastructure metrics during performance tests.

### Overview

New Relic provides visibility into your infrastructure, from services running in the cloud or on dedicated hosts to containers running in orchestrated environments. You can connect the health and performance of all your hosts to application context.

The New Relic Infrastructure integration lets you view your infrastructure monitoring data alongside your application performance data in aggregated reports. This integration provides a snapshot of the health of your host ecosystem and the impact your infrastructure has on your applications under test.

### Configuration Steps

1. **Get New Relic API Key**: Obtain Infrastructure API key from New Relic
2. **Create APM Credentials**: Create New Relic Infrastructure credentials in BlazeMeter
3. **Configure Metrics**: Select infrastructure metrics to monitor
4. **Test Integration**: Verify integration works correctly

### Features

- Infrastructure metric monitoring
- Server resource tracking
- Network performance metrics
- Infrastructure health correlation

### Setup

1. Log in to your New Relic account and copy your New Relic account ID and API query key
2. Log in to BlazeMeter and do one of the following:
   - Click **Create Test** and scroll down to the **Integrations** section
   - Open an existing performance test, click the **Configurations** tab, and scroll down to the **Integrations** section
3. Click **New Relic Infrastructure**
4. Fill in the following fields:
   - **Select which New Relic Insights API query key to use**: Select **Create a new New Relic Insights API Query Key**
   - **Profile Name**: Type a name for your New Relic Infrastructure profile (configuration)
   - **Account Id**: Paste your New Relic account ID
   - **New Relic Insights API Query key**: Paste your New Relic API query key
5. Click **Next**. The key performance indicators appear automatically according to your New Relic infrastructure profile settings
6. Click **Select Entry** and select the system (entity) to test
7. Click **Select Items** and select the KPIs to include in the BlazeMeter Timeline Report
8. Click **Next**
9. Enter a new profile name, and click **Save Profile**
10. Click **Apply**

### Result

Your infrastructure monitoring data will appear in the BlazeMeter Timeline Report as soon as you run your load test. You can now diagnose performance-related problems, apply fixes and start the cycle all over again.

### Documentation References

For detailed information about New Relic Infrastructure integration, use the BlazeMeter MCP help tools:

**New Relic Infrastructure**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-new-relic-infrastructure.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-new-relic-infrastructure.htm"]}`

---

## CloudWatch

Set up AWS IAM user and policy with CloudWatch access to integrate Amazon CloudWatch with BlazeMeter for monitoring AWS resources.

**Use when**: Setting up AWS IAM user and policy with CloudWatch access or integrating Amazon CloudWatch with BlazeMeter for monitoring AWS resources.

### What is CloudWatch?

CloudWatch is Amazon's out-of-the-box feature that enables users to monitor their AWS resources such as EC2s, ELBs, Route53, EBS and more for CPU usage, Disk I/O etc.

### Set Up AWS IAM

In order to proceed, you'll need an AWS IAM (Identity and Access Management) Key. If you don't have one yet, see [Set up AWS IAM](https://help.blazemeter.com/docs/guide/integrations-set-up-aws-iam.html).

**Steps to Access Amazon Access Key ID & Secret Access Key:**

1. Go to IAM Dashboard. Create a new group (in IAM)
2. Name a group, then click on 'Next Step'
3. Choose Custom Policy and click Select
4. Fill in the Policy Name and Document using the below parameters:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Action": [
           "autoscaling:Describe*",
           "cloudwatch:Describe*",
           "cloudwatch:List*",
           "cloudwatch:Get*",
           "ec2:Describe*",
           "ec2:Get*",
           "ec2:ReportInstanceStatus",
           "elasticache:DescribeCacheClusters",
           "elasticloadbalancing:Describe*",
           "sqs:GetQueueAttributes",
           "sqs:ListQueues",
           "rds:DescribeDBInstances",
           "SNS:ListTopics"
         ],
         "Effect": "Allow",
         "Resource": "*"
       }
     ]
   }
   ```
5. For more information regarding the policy setup and controlling User Access to your account, see [Identity and access management for Amazon CloudWatch (docs.aws.amazon.com)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/UsingIAM.html#ExamplePolicies_CloudWatch)
6. Click Create Group at the bottom of the page. (This specific policy set up gives the aforementioned, newly named group read-only access to all relevant AWS services currently supported by BlazeMeter's integration. Now that the new policy is set save the group creation)
7. Now go to Users and click Create a new user. Create a new user (that is, sign up) or log in with your user (these are the credentials we'll be providing) to the BlazeMeter integration with AWS CloudWatch
8. Write down your Access Key ID and Secret Access Key
9. Now let's assign the newly created user to a group we created a few steps earlier. Choose a user and click add User to Groups
10. Select the right group

Now you have a user with access to CloudWatch metrics. Once the user is created and we've logged in, make sure to SAVE the Access Key ID and Secret Access Key in BlazeMeter.

### How to Set Up CloudWatch BlazeMeter Integration for a Test

Follow these steps to set up the CloudWatch integration:

1. Click the 'Create Test' Button and choose any test option from the list
2. In the test configuration screen, scroll down to the **Integrations** section, then select CloudWatch. For older (V3) test options, you can simply click the CloudWatch button from the list of options
3. Select an existing IAM key or select 'create a new IAM Key'. Now enter your Amazon Access Key ID & the Secret Access Key of your Amazon account

### Creating a Profile

1. If the keys are correct, you should see the following screen below
2. Create a profile by specifying the region, namespace and items. Then select one or more of them
3. Enter a Profile name and click 'Save Profile'
4. You can start picking up resources which are being monitored by CloudWatch
5. Press the 'Apply' button

Subscribe to the profile you've just created (you can do this by clicking on the blue 'V', then clicking 'Apply'.)

### How to View CloudWatch Data

You can create many profiles and, once created, subscribe to them with any other tests you have.

To see the data, simply run the test! Your Timeline Report will now include options for displaying your CloudWatch real-time data.

### IAM Policy Requirements

The IAM policy must include read-only access to:
- CloudWatch (Describe*, List*, Get*)
- EC2 (Describe*, Get*, ReportInstanceStatus)
- Auto Scaling (Describe*)
- Elastic Load Balancing (Describe*)
- RDS (DescribeDBInstances)
- ElastiCache (DescribeCacheClusters)
- SQS (GetQueueAttributes, ListQueues)
- SNS (ListTopics)

### Features

- AWS resource monitoring
- CloudWatch metric visualization
- EC2, RDS, and other AWS service metrics
- Cost and performance correlation
- Real-time data display during test execution

---

## DX APM

Use this integration to run and investigate load tests through the test metadata. DX APM users can incorporate performance test scenarios and their key performance metrics into their business analysis. This leads to better optimization, faster detection of issues, and greater abilities to make decisions.

**Use when**: Integrating DX Application Performance Management (CA APM) with BlazeMeter, sending BlazeMeter data to DX APM, or setting up two-way integration between BlazeMeter and DX APM.

This integration supports both on-premises and SaaS versions of DX APM. There are two available options:

- **See BlazeMeter data in DX APM**: Send BlazeMeter test metadata to DX APM
- **Two-way integration**: Bidirectional integration between BlazeMeter and DX APM

### Send BlazeMeter Data to DX APM

Select this option to add headers to outbound traffic to DX APM containing the test name, test step (label), geographic region, test engine IP, and network emulation settings. This metadata enhances reporting of the test on the APM side. For example, test traffic will show up as business transactions in DX APM.

**Prerequisites:**
- An API token has been generated from DX APM. For more information, see the [product documentation](https://techdocs.broadcom.com/).
- A workspace administrator has set up credentials for DX APM, including a DX APM API token.

**Steps:**
1. In BlazeMeter, click **Create Test**, then **Performance Test**.
2. In the **Integrations** section, click **DX APM**.
3. Select **See BlazeMeter data in DX APM**.
4. Click **Apply**.

**Result:**
BlazeMeter adds relevant headers to the test script. The following information is sent to DX APM and displayed on its dashboard:

- Test name
- Label name
- Region
- Engine IP
- Network emulation

### Set Up Two-Way Integration

Use this option to:
- Add headers to outbound traffic from BlazeMeter to DX APM containing the test name, test step (label), geographic region, test engine IP, and network emulation settings.
- Make DX APM metrics available for overlay on the BlazeMeter [Timeline Report](skill-blazemeter-performance-testing://references/reporting.md).

**Prerequisites:**
- An API token has been generated from DX APM. For more information, see [the product documentation](https://techdocs.broadcom.com/).

**Steps:**
1. In BlazeMeter, click **Create Test**, then **Performance Test**.
2. In the **Integrations** section, click **DX APM**.
3. Select **Two way integration**.
4. Fill in the required fields (DX APM domain, API token, etc.).
5. Click **Apply**.

**Result:**

**In DX APM:**
BlazeMeter adds relevant headers to the test script. The following information is sent to DX APM and displayed on its dashboard:

- Test name
- Label name
- Region
- Engine IP
- Network emulation

**In BlazeMeter:**
After a test is run, you can see the DX APM data in the **Timeline Report**. To select your DX APM data, you can choose your DX APM domain and the available agents under **KPI Selection**.

### Documentation References

For detailed information about DX APM integration, use the BlazeMeter MCP help tools:

**DX APM**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-integration-with-dx-apm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-integration-with-dx-apm"]}`

---

## Dynatrace

Integrate Dynatrace APM with BlazeMeter performance tests to monitor application performance and correlate with load test results.

**Use when**: Integrating Dynatrace APM with BlazeMeter performance tests or monitoring application performance during load tests.

### Overview

Dynatrace is an Application Performance Monitoring (APM) tool designed for analyzing the performance of application servers, database servers, and web services.

BlazeMeter offers two integration options with Dynatrace:
- **Anonymous integration**: BlazeMeter sets up a test that sends HTTP requests to your monitored servers, and the resulting monitoring KPIs are instantly accessible within your Dynatrace application
- **Integration with a Dynatrace profile**: You can integrate your BlazeMeter tests with a specific Dynatrace profile. You configure a BlazeMeter test to send requests to your monitored servers, and the associated monitoring KPIs become readily available within your Dynatrace application

These integration options empower you to effectively monitor and optimize the performance of your applications, ensuring a seamless user experience.

BlazeMeter includes two versions of the Dynatrace APM integration:
- **Dynatrace APM - deprecated**
- **Dynatrace APM**
- If you are using a Dynatrace version that is 1.243 or higher, use the Dynatrace APM integration
- If you are using a Dynatrace version that is lower than 1.243, use the Dynatrace APM – deprecated integration

For more information, see [https://www.dynatrace.com/support/help/dynatrace-api/basics/deprecation-migration-guides](https://www.dynatrace.com/support/help/dynatrace-api/basics/deprecation-migration-guides)

### Set Up Dynatrace to Work with BlazeMeter

You can leverage Dynatrace metrics within BlazeMeter reports and send distributed tracing data from BlazeMeter to Dynatrace via headers. This section outlines the necessary setup steps within Dynatrace to facilitate this integration.

- **Pulling Metric Values into BlazeMeter Reports**: To pull metric values from Dynatrace into BlazeMeter reports, you can utilize BlazeMeter Profiles
- **Sending Distributed Tracing Data**: BlazeMeter can send distributed tracing data to Dynatrace via headers, enabling you to trace a request's path through its journey across various components such as apps, rpc (Remote Procedure Call), queue, and more

BlazeMeter adds a customer header to requests that are run through JMeter performance tests. This header includes the Sample Name, Number of VUs, and Load Locations for each request. This allows for distributed tracing of the request from source to end point.

To view the headers sent from BlazeMeter to Dynatrace and facilitate distributed tracing, perform the following steps in Dynatrace:

1. Create a new request attribute
2. Within the request attribute settings, add a new data source
3. Set the request attribute source to **HTTP Header Request**
4. Define the parameter name as "x-dynaTrace"
5. Set **Preprocess parameters by extracting substring** to **after** and **NA**

For more information, see [Dynatrace Documentation](https://docs.dynatrace.com/docs).

### Create an Anonymous Integration

This integration involves inserting header lines into your JMeter file, visible exclusively from the Dynatrace APM perspective. You can use this integration for a new or existing performance test.

No reports will be generated on the BlazeMeter side through your Dynatrace account.

1. Navigate to the BlazeMeter Test Configuration page
2. In the **Integrations** section, click **Dynatrace APM** (or **Dynamic APM - deprecated**)
3. Select the **Integrate using Dynatrace HTTP headers** option. When you execute this test, BlazeMeter appends a header line to the JMX of the test. This action enables Dynatrace's agent to identify the load test and display BlazeMeter's requests in a specific format, featuring request labels, thread numbers, response codes, and more
4. Access these results within Dynatrace. For more information, see the [Dynatrace documentation](https://www.dynatrace.com/support/help)

### Integrate BlazeMeter with Your DynaTrace Profiles

This integration enables you to access APM metrics from both the Dynatrace APM and BlazeMeter sides, depending on your profile setup.

You can use this integration for a new or an existing performance test.

1. Navigate to the BlazeMeter Test Configuration page
2. In the **Integrations** section, click **Dynatrace APM** (or **Dynamic APM - deprecated**)
3. Select the **Integrate using specific Dynatrace system profile** option
4. In BlazeMeter (not in a Dynatrace system profile), select and manage the profiles you want to use. You can also modify, duplicate, or delete your existing profiles by clicking the corresponding icons next to the profile. If you don't have any profiles set up, you can create new credentials by entering the following key details. You can locate the **Environment ID** and **Token** values in the [Dynatrace documentation](https://www.dynatrace.com/support/help/get-started/monitoring-environment/environment-id)):
   - **Basic Configuration**:
     - **Key Name** - Name of the key you want to create and reference in BlazeMeter
     - **Environment ID** - The full URL containing your environment ID (Exclude the trailing / in your URL, for example, http://yourHostAtDynatrace.com)
     - **Token** - Access token for your DynaTrace environment
   - **Advanced Configuration**:
     - **Private Location ID** - The ID of the private location to use to run the APM functionality (see [here](https://help.blazemeter.com/docs/guide/private-locations-where-to-find-harbor-id-and-ship-id.html) for where to get this value). If you're using DynaTrace in the cloud, you don't need to provide the private location ID. The integration will work seamlessly without it
5. Specify your entity type, Dynatrace entity, and the metrics to include in your BlazeMeter report. Use the search/autocomplete functionality in the Entry field after selecting an Entry Type (such as Hosts, Process, Application, or Services) to quickly find the desired entry
6. Click **Next** to review a preview of what your profile will monitor. Provide a profile name and save it as a new profile for future tests
7. Upon saving your profile, you'll see the following screen, allowing you to choose the profile(s) you want. To apply the profile(s) to your test, click **Apply**

Your test is now integrated with DynaTrace.

### View DynaTrace Metrics in Your Timeline Report

To view the metrics from Dynatrace, you can go to the **Timeline Report**, scroll to the bottom of the available KPIs, and then expand the Dynatrace APM section. You will then see all the metrics you selected listed there and can click the checkboxes to add them to your report.

### Features

- Application performance monitoring
- Real user monitoring (RUM)
- Synthetic monitoring correlation
- Performance baseline comparison
- Distributed tracing via HTTP headers
- Anonymous integration option
- Profile-based integration option

---

## Best Practices

- **Secure Credentials**: Store APM credentials securely using BlazeMeter credential management
- **Test Integration**: Always test integration before production use
- **Monitor Metrics**: Regularly review APM metrics in test reports
- **Update Credentials**: Rotate credentials regularly for security
- **Document Configuration**: Document APM integration setup for reference

---

## Documentation References

For detailed information about APM integrations, use the BlazeMeter MCP help tools:

**APM Integrations**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `integrations-integrate-with-appdynamics` (AppDynamics)
  - `integrations-integrate-with-datadog` (Datadog)
  - `integrations-integrate-with-delphix` (Delphix)
  - `integrations-new-relic-apm` (New Relic APM)
  - `integrations-blazemeter-integration-with-cloudwatch` (CloudWatch)
  - `integrations-set-up-aws-iam` (AWS IAM for CloudWatch)
  - `integrations-blazemeter-integration-with-dynatrace-apm` (Dynatrace)
  - `integrations-blazemeter-integration-with-dx-apm` (DX APM)
  - `integrations-new-relic-infrastructure.htm` (New Relic Infrastructure)
  - `integrations-new-relic.htm` (New Relic Integrations Overview)
  - `integrations-overview.htm` (Integrations Overview)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-integrate-with-appdynamics", "integrations-integrate-with-datadog", "integrations-integrate-with-delphix", "integrations-new-relic-apm", "integrations-new-relic-infrastructure.htm", "integrations-blazemeter-integration-with-cloudwatch", "integrations-set-up-aws-iam", "integrations-blazemeter-integration-with-dynatrace-apm", "integrations-blazemeter-integration-with-dx-apm", "integrations-new-relic.htm", "integrations-overview.htm"]}`

