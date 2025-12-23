# Integration Troubleshooting

## New Relic Reporting

Integrate BlazeMeter with New Relic for reporting, including APM, Infrastructure, and Insights integrations with proper API keys and agent installation.

**Use when**: Troubleshooting integration issues with New Relic reporting, setting up APM, Infrastructure, or Insights integrations, or configuring proper API keys and agent installation.

### Overview

The BlazeMeter integration with New Relic lets a New Relic agent gather performance metrics while you're running a BlazeMeter Performance test. Thanks to this integration you can evaluate the end-user experience and application system KPIs (Key Performance Indexes) using a single dashboard in New Relic. Additionally, you can view BlazeMeter's API Monitoring metrics in a New Relic dashboard.

### Which Reports Can I Visualize?

You can view your application and infrastructure monitoring data alongside your user-experience and performance data in timeline reports during or at any time after a BlazeMeter test runs. With BlazeMeter, you can access past test data, compare past results, or even compare past results to real-time results.

### Integration Types

#### New Relic APM Integration
The [New Relic APM](https://help.blazemeter.com/docs/guide/integrations-new-relic-apm.html) integration lets you view your application monitoring data alongside your end-user experience and performance data, and lets you access this data after testing ends.

**Required**: New Relic Account ID, New Relic User key  
**Test Domain**: Performance tests  
**Agent installation**: Yes  
**Data Source**: New Relic  
**Data Visualization**: BlazeMeter Timeline Report

#### New Relic Infrastructure Integration
The New Relic Infrastructure integration lets you view your infrastructure monitoring data alongside your application performance data in aggregated reports.

**Required**: New Relic Account ID, New Relic User key  
**Test Domain**: Performance tests  
**Agent installation**: Yes  
**Data Source**: New Relic  
**Data Visualization**: BlazeMeter Timeline Report

#### New Relic Insights Integration
By connecting New Relic with BlazeMeter API Monitoring, you can collect metrics from your API tests in BlazeMeter, and transform them into actionable insights about your applications in New Relic.

**Required**: New Relic Account ID, New Relic Ingest License key  
**Test Domain**: API Monitoring  
**Agent installation**: No  
**Data Source**: BlazeMeter API Monitoring Report  
**Data Visualization**: New Relic Dashboard

### Common Issues

#### API Key Configuration
- **Symptom**: Integration fails with authentication errors
- **Solution**: Verify API key is correct and has proper permissions
- **Prevention**: Use valid API keys with required permissions

#### Agent Installation
- **Symptom**: Metrics not appearing in New Relic
- **Solution**: Verify New Relic agent is installed and running
- **Prevention**: Follow New Relic agent installation guidelines

#### Integration Settings
- **Symptom**: Integration not working as expected
- **Solution**: Review and correct integration configuration
- **Prevention**: Verify integration settings match requirements

### Troubleshooting Steps

1. **Verify API Keys**:
   - Check API key is valid and not expired
   - Verify API key has required permissions
   - Regenerate API key if necessary

2. **Check Agent Status**:
   - Verify New Relic agent is installed
   - Check agent is running and connected
   - Review agent logs for errors

3. **Review Integration Configuration**:
   - Check integration settings in BlazeMeter
   - Verify application names match
   - Ensure correct integration type selected

4. **Test Integration**:
   - Run test and verify metrics appear in New Relic
   - Check data is being sent correctly
   - Verify metrics are displayed properly

### Which New Relic API Keys Do I Need?

To use these integrations, you will need New Relic Keys and the Account ID that you find in your New Relic account. Keep your API keys secure as explained in the [New Relic documentation](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/).

New Relic provides the following relevant API keys and identifiers:
- Your Account ID gives you access to New Relic services
- Your Ingest License keys are for getting data from BlazeMeter into New Relic
- Your User keys are for getting data from New Relic into BlazeMeter

### What is My Account ID?

Log on to your New Relic account. In the bottom left, find your user menu and select **API Keys**. Copy your Account ID from here. You have only one Account ID and you do not need to create it.

### How Do I Create API Keys?

Log on to your New Relic account. In the bottom left, find your user menu and select **API Keys**. The API Keys page gives you an overview of your keys and ID, and links to relevant New Relic doc.

On this page, you generate **User keys** and **Ingest License keys**.

1. Click **Create a Key**
2. Select the **Key Type to generate**. Select one of the following options: **User** or **Ingest – License**
3. Give the key a name that reminds you of the purpose why you have created it. For example, "BlazeMeter performance testing" or "BlazeMeter API monitoring". The name can be up to 120 characters long
4. Optionally, leave yourself a note on how long or for which project you intend to use this key
5. Click **Create a Key**. The key is added to your API Key list

### How Do I Install the New Relic Agents?

You have a server with a web app that you want to monitor using APM.

New Relic offers two APM agents:
- The Infrastructure Agent provides data about CPU, memory, disk I/O, etc.
- The Java APM Agent provides data about CPU usage, memory, garbage collection, threads, etc.

**Note**: The API Monitoring integration does not require a New Relic Agent.

#### How Do I Install the Infrastructure Agent?

1. Log on to the New Relic Explorer
2. Add an Infrastructure Agent by following the instructions in the New Relic web UI. For more information, see [Install the infrastructure agent (New Relic Documentation)](https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/get-started/install-infrastructure-agent/)
3. In the Dashboard, go to **All Entities > Hosts**. The Infrastructure Agent is now listed as a Host

With the app under load, you can now see New Relic Infrastructure report the details.

#### How Do I Install the APM Agent?

1. Log on to the New Relic Explorer
2. Install an APM Agent by following the interactive webform at [Monitor your Java app (New Relic Documentation)](https://docs.newrelic.com/install/java/)
   - Download the following zip file: `curl -O https://download.newrelic.com/newrelic/java-agent/newrelic-agent/current/newrelic-java.zip`
   - Unzip the archive
   - Enter your app name and license key into the [interactive web form](https://docs.newrelic.com/install/java/), then download your custom config file `newrelic.yml`
   - Create a New Relic directory under `/opt/newrelic` and move the downloaded files there
3. In the Dashboard, go to **All Entities > Services APM**. The Java APM Agent now appears listed as a service. For more information, see [Introduction to New Relic for Java (New Relic Documentation)](https://docs.newrelic.com/docs/apm/agents/java-agent/getting-started/introduction-new-relic-java/)
4. Configure your application to use the downloaded Java APM Agent. Details depend on your app and environment. For example, for Tomcat: `CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/newrelic/newrelic.jar"`

With the app under load, you can now see New Relic APM report the details.

Once the agents are reporting to New Relic, you can connect them to BlazeMeter reporting.

### How Do I Connect New Relic Agents to BlazeMeter?

After the agents are reporting to New Relic, integrate them with a BlazeMeter Performance test to view the aggregated results in BlazeMeter.

#### Connect the Infrastructure Agent to BlazeMeter

1. Log on to BlazeMeter and open your Performance test
2. Edit the test configuration and select New Relic Infrastructure
3. Enter your Account ID and User Key (query key) when prompted
4. Select one or more metrics to be included in the BlazeMeter report. Then click Next
5. Give the profile a name and click Save Profile
6. Select your newly created profile and apply it to the test
7. Run the Performance test in BlazeMeter. The system metrics are now available in the BlazeMeter report

#### Connect the APM Agent to BlazeMeter

1. Log on to BlazeMeter
2. Open the Performance test
3. Edit the test configuration and select New Relic APM
4. Enter your Account ID and User Key (query key) when prompted
5. Under Build Profile, select Applications, and select your app
6. From the dropdown, select one or more metrics to be included in the BlazeMeter report. Then click Next
7. Give the profile a name and click Save Profile
8. Run the Performance test in BlazeMeter. The BlazeMeter report now combines APM metrics with the BlazeMeter results

#### Activate New Relic for BlazeMeter API Monitoring

Your third option is to display BlazeMeter API Monitoring results from Runscope tests as insights in New Relic.

1. Go to the BlazeMeter API Monitoring tab
2. Click your profile on the top-right, and select **Connected Services**
3. Click **Connect New Relic Insights**. Select your data region. Enter your **New Relic Account ID** and **License Key**. Click **Connect Account**
4. Open your API test and click **Editor**
5. Expand **Test Settings**, click the **Integrations** tab in the left-hand menu, and toggle the **New Relic Insights integration** on

Now you can run NRQL Queries in the "Query Your Data" screen within your New Relic dashboard.

For example, to get BlazeMeter test result counts for the past week, make the following query:
```
SELECT count(*) FROM RunscopeRadarTestRun FACET result TIMESERIES SINCE 1 week ago
```

Filter queries by bucket as needed using WHERE clauses:
```
(WHERE bucket_name = 'My Bucket') or test (WHERE test_name = 'My API Tests')
```

More examples can be found at [New Relic Insights Integration](https://help.blazemeter.com/docs/guide/api-monitoring-new-relic-insights-integration.html).

### What About the Legacy Keys That I Am Using?

Previously, New Relic used "**Insights insert keys**", "**Insights query keys**", and "**REST API keys**". New Relic no longer recommends using these legacy keys. The current New Relic keys are more user-friendly and give you access to more features.

- If you are using legacy API keys and if your legacy integrations still work, you can keep using them. They are still supported by New Relic as of 2023
- If you are setting up a new integration or are updating your old keys, start using the new API keys

When prompted by the integrations in BlazeMeter, enter the following keys:
- Replace the New Relic Insights Insert Key with your New Relic License Key
- Replace the **New Relic API Query key** with your **User key**. For more information, see [https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/)

### Best Practices

- **Use Valid API Keys**: Always use valid API keys with proper permissions
- **Monitor Integration**: Regularly check integration status
- **Keep Agents Updated**: Keep New Relic agents updated
- **Document Configuration**: Document integration configuration for reference


---

## Documentation References

For detailed information about New Relic integration troubleshooting, use the BlazeMeter MCP help tools:

**New Relic Integration**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-integration-new-relic-reporting`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-integration-new-relic-reporting"]}`

