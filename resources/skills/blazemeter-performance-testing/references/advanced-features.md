# Advanced Features

## AI Log Analysis Report

Use AI Log Analysis to summarize lengthy log files in human-readable format, identify root causes, and get remediation recommendations. The AI Log Analysis tab is a tool that sums up lengthy log files in a helpful, human-readable format.

**Use when**: Using AI Log Analysis to summarize lengthy log files, identifying root causes, getting remediation recommendations, or analyzing errors across multiple engines.

### Use Case

After running a Performance test, BlazeMeter possibly alerts you to some errors. You download multiple log files for multiple engines, extract them, search through them, correlate them, read third-party documentation to investigate the cause of errors and warnings, before you find a solution. Manual log analysis is quite time intensive.

**Benefits:**
- To help you pinpoint the root causes, BlazeMeter AI Log Analysis presents you with a summary of pertinent error messages and warnings that helps you understand common issues happening during test executions
- The analysis covers all logs across engines so you don't have to search through several logs
- If applicable, it will give you recommendations for remediation
- The summary includes links to pertinent log files to help with your investigation
- The analysis distinguishes whether issues stem from the system under test or from the test script

### AI Consent

BlazeMeter's AI-assisted features require explicit consent from the account owner before team members can use them. By default, AI features are disabled. For more information, see [AI Consent](skill-blazemeter-administration://references/security.md).

### Use AI to Analyze the Log

You can generate AI insights only for completed test runs of Performance tests and Browser-Based tests. Multi-tests are not supported.

Follow these steps:

1. On the **Performance** tab, select **Reports**. The most recent reports are shown on top
2. Click **Show all reports** and select a report to view its details
3. Start the AI Log analysis: Either click **Run AI Log Analysis** on the **Summary** tab. Or click **Run AI Log Analysis** on the **AI Log Analysis** tab
4. Wait while BlazeMeter analyzes the logs and shows you a list of detected errors grouped by solutions. Each group is assigned a **Priority value** based on how the errors impact your test
5. Expand the list of errors and view the suggested solutions:
   - **Title**: Error group title
   - **Original Message**: Indicates the original error message or warning found in the log
   - **Explanation**: Informs you what this log message means and in which situations it typically occurs, so you can evaluate the impact and relevance for your system or test
   - **Recommendation**: Contains typical solutions to solve this issue or recommends best practices to avoid a warning, if applicable
   - **Found in Logs**: Click **Check Logs** to jump to the **Logs** tab, where you can download the relevant log files. If you are using multiple engines, this action displays only the engines relevant to the error

### Priority Value

To help you know which errors are the most critical, AI assigns each group of errors a priority value. Priority values can range from 0-100, with 100 being the most critical errors:

- **90-100**: Critical infrastructure issues, authentication failures, system crashes
- **70-89**: High-frequency errors, significant functionality failures
- **50-69**: Moderate impact errors, performance issues, configuration problems
- **30-49**: Low-frequency issues, minor functionality problems
- **0-29**: Cosmetic issues, warnings, non-blocking problems

#### AI Assigns Priority Values Based on the Following:

| What is being assessed | Weight | Types of errors |
|------------------------|--------|-----------------|
| Impact on Test Success | 40% | Errors that prevent tests from running or cause complete failures get higher priority |
| Error Frequency | 25% | More frequent errors (higher `errorCount`) deserve higher priority |
| Error Origin Category | 20% | `system under test_infrastructure` errors: Usually high priority (80-100) as they affect system stability<br>`blazemeter_infrastructure` errors: Medium-high priority (60-90) as they affect the test execution platform<br>`test_code` errors: Medium priority (40-80) as you can often work around them |
| Scope of Impact | 15% | Errors that appear in more tests and files get higher priority |

### Filter Results

If necessary, select the category by which you want to filter the results:

- **System Under Test**: Filter errors related to the system being tested
- **Test Script**: Filter errors related to the test script
- **Default**: Show all errors

---

## Add Users Dynamically

Add additional tests to active Multi-Test runs on the fly to increase load or add new scenarios without stopping and restarting the test. Adding users dynamically is valuable in [Multi-Test](skill-blazemeter-performance-testing://references/advanced-features.md) runs which assess the target server limits. While running a load test, you might notice that the target servers are handling the load quite well. As an alternative to shutting down and starting a new test with a different configuration, you can simply add additional tests to your active Multi-Test on the fly, adding more users or load. Once a test is added to the Multi-Test, its results will be aggregated with the rest of the Multi-Test results, forming a big picture analysis.

**Use when**: Adding additional tests to active Multi-Test runs on the fly, increasing load or adding new scenarios without stopping and restarting the test, or assessing target server limits during test execution.

**Important**: Only tests within the same project can be included in a Multi-Test.

### Add Tests Dynamically

You can add any test while the Multi-Test is running by simply starting the single test, then selecting the option to add it to the Multi-Test.

Follow these steps:

1. Create a [Multi-Test](skill-blazemeter-performance-testing://references/advanced-features.md) and run it
2. If you believe you could use some more load, or want to add another scenario to the Multi-Test, select and run your single test as usual. Click **Tests**, **Show all tests**. A list of all available tests appears on the left side panel
3. Click the 'Play' button for the test you want to add
4. In the pop-up window, expand the **Run this test as part of a master session?** drop-down list
5. Select to run as a single standalone test, or as part of any Multi-Test that is currently active

If you choose to run the test under the Multi-Test, then right after the new test finishes its startup stage, its results will be aggregated together with the overall results of the Multi-Test. In the report, notice the moment in which a new test was added to the load.

### Add Tests via the API

Alternatively, you can add a single test to a currently running multi-test via the API. To do so, perform a **POST** to the following endpoint:

```
https://a.blazemeter.com/api/v4/tests/{{testId}}/start?delayedStart=true&masterId={{masterId}}
```

The above API includes the following options:

- **{{testID}}** = The test ID of the single test you wish to add
- **{{masterID}}** = The master ID of the multi-test you wish to add the single test to

For more information, see the [API documentation](https://help.blazemeter.com/apidocs/performance/multi_tests_add_tests.htm).

---

## APM Integration

Integrate Application Performance Monitoring tools (DX APM, AppDynamics, CloudWatch, New Relic, DynaTrace, Datadog) with BlazeMeter Performance tests.

**Use when**: Integrating Application Performance Monitoring tools with BlazeMeter Performance tests or connecting DX APM, AppDynamics, CloudWatch, New Relic, DynaTrace, or Datadog.

### Overview

BlazeMeter makes it easy to leverage the power of performance testing and Application Performance Monitoring (APM) combined.

### Configure APM Integration

Follow these steps:

1. Navigate to a test and click the **Configuration** tab
2. Scroll down to the **APM Integration** section
3. Click the APM tool in use in your environment

For more information about the configuration screens for these APM tools, see the links below.

### Supported APM Tools

- **[DX APM](https://help.blazemeter.com/docs/guide/integrations-blazemeter-integration-with-dx-apm-saas.html)**: CA Application Performance Management
- **[AppDynamics](https://help.blazemeter.com/docs/guide/integrations-integrate-with-appdynamics.html)**: Application performance monitoring
- **[AWS CloudWatch](https://help.blazemeter.com/docs/guide/integrations-blazemeter-integration-with-cloudwatch.html)**: AWS cloud monitoring
- **[New Relic APM](https://help.blazemeter.com/docs/guide/integrations-new-relic-apm.html)**: Application and infrastructure monitoring
- **[New Relic Infrastructure](https://help.blazemeter.com/docs/guide/integrations-new-relic-infrastructure.htm)**: Infrastructure monitoring
- **[DynaTrace APM](https://help.blazemeter.com/docs/guide/integrations-blazemeter-integration-with-dynatrace-apm.html)**: Full-stack monitoring
- **[Datadog](https://help.blazemeter.com/docs/guide/integrations-integrate-with-datadog.html)**: Infrastructure and application monitoring

**Note**: For detailed configuration instructions for each APM tool, see [APM Credentials](skill-blazemeter-administration://references/apm-credentials.md) and the respective integration guides.

---

## Create Browser Test

Browser-Based Performance Testing operates similarly to script-based performance tests, but the test analyzes browser interactions instead of running conventional scripts. This test type has the same features as a performance test, but it uses an embedded Selenium script to execute the test directly in a browser.

**Use when**: Creating Browser-Based Performance Tests, when correlation is unavailable or infeasible, for complex UI testing, or when you have limited resources for script management.

### Why Use Browser-Based Performance Testing?

Browser-Based Tests are particularly useful in the following scenarios:

- **When correlation is unavailable or infeasible**: Cases where auto-correlation plugins cannot be used due to proxy settings or other restrictions, making manual UI recording a practical alternative. For example, many organizations have security policies that prevent the use of auto-correlation plugins and traditional JMeter scripts
- **Complex UI testing**: Applications with dynamically generated UI elements where element names or HTTP calls are unknown
- **Limited resources**: Users who lack the time, skills, or access to write or manage complex test scripts

### Prerequisites

To edit Browser Performance Tests, you must understand the following concepts:
- **Objects**: GUI elements such as buttons and fields
- **Actions**: Such as click or select
- **Group Actions**: Collections of actions

When using a Private Location, you need to only enable the **Performance** functionality to use Browser Performance Tests.

### Create a Browser Performance Test

Follow these steps:

1. From the Home screen, click the **Performance** tab
2. Click **Create Test**
3. Select a project
4. Click **Performance Test**
5. Click **Define Test Scenario**
6. Define your Scriptless test in one of the following ways:
   - **Start Recording**: Test scenarios in Chrome. Verify that you have the BlazeMeter Extension installed. To record test scenarios for browser performance tests using the BlazeMeter Chrome extension, ensure you are using version 6.6.0 or higher. Click **Start UI Recorder** on an empty canvas. A new browser window opens. The Chrome extension opens. Open your web app and run your test. When you're done, click **Stop Recording** in the Chrome Extension. Click **Run**. In the menu, click **Browser Performance (Selenium)**. The recorded test opens on the Test Configuration page. For more information, see [The BlazeMeter Chrome Extension](https://help.blazemeter.com/docs/guide/recorders-blazemeter-chrome-extension.html) and [Chrome Extension - Record](https://help.blazemeter.com/docs/guide/recorders-chrome-extension-record.html)
   - **Build Step by Step**: Test scenarios using building blocks. Drag Actions from the **Groups** and **Actions** tabs and drop them onto the scenario canvas. For each Action, define a step name, target object, and values
7. On the Test Configuration page, configure one or more of the following options:
   - Load Configuration ([Select Total Users](https://help.blazemeter.com/docs/guide/performance-load-configuration.html#Select), [Configure Duration or Iterations](https://help.blazemeter.com/docs/guide/performance-load-configuration.html#Configur))
   - [Load Distribution](https://help.blazemeter.com/docs/guide/performance-load-distribution.html)
   - **Max users per engine** is currently four (4) for performance reasons. Consider allocating one CPU core per browser-based virtual user. Ensure your private location has sufficient resources before increasing the **Max Users Per Engine** setting
   - [Virtual Services Configuration](https://help.blazemeter.com/docs/guide/mock-service-add-to-test.html)
   - [Failure Criteria](https://help.blazemeter.com/docs/guide/performance-failure-criteria.html)
   - [APM Integration](https://help.blazemeter.com/docs/guide/performance-apm-integration.html)
   - [JMeter Properties](https://help.blazemeter.com/docs/guide/performance-jmeter-properties.html)
   - [DNS Override](https://help.blazemeter.com/docs/guide/performance-dns-override.html)
   - [Network Emulation](https://help.blazemeter.com/docs/guide/performance-network-emulation.html)
8. (Optional) Enable **Run Video Recording** and choose a location. If you are using a private location, that private location is selected by default. For more information, see [Private Locations](https://help.blazemeter.com/docs/guide/private-locations-intro.html). This action enables BlazeMeter to record a video of the test run, capturing browser actions and providing visual context for any errors encountered. Each video recording consumes 100 Variable Unit Hours (VUH)
9. (Optional) To do a test run, click **Debug Test**. A debug test run does not affect metrics
10. Click **Run Test**

After this test runs, review the performance report by using BlazeMeter's tools. Filter, compare, and investigate errors, anomalies, and logs, as you would for any other performance report.

### Create Objects

Objects are GUI elements in your system under test, such as text fields and buttons. When you start a new project, your Object list is empty. You manage Objects from the **Test Action Library** tab. To create an Object, you must provide a unique way to locate the element in the DOM.

You can create Objects by using any of the following methods:
- Let the [BlazeMeter Chrome Extension](skill-blazemeter-recorders://references/chrome-extension.md) record and create Objects automatically
- Use the Object Picker to change an existing object
- Create Objects manually in from the test definition window

**Manually create Objects:**

1. Add an Action to the scenario
2. In the **Object** box, click **Create New Object**
3. Define an object name
4. In the **Locator** list, click one or more of the following types:
   - By CSS Class
   - By ID
   - By Name
   - By Xpath
5. In the **Value** field, define the locator as a text string. For example, you can enter the object ID
6. Click **Create**

The Object is added to the Object library for this project and can be used in this test.

### Edit Objects

From the Test Action Library, you can edit only the name and description of Objects. Editing other Object properties impacts scenarios in ways that require debugging and validation, which can be done only when the Object is used in the context of a scenario.

Follow these steps:

1. Find the Object inside a step in the Scenario Editor and click the step to select it. Use the **Test Action Library** to find where the Object is used if you cannot find it in a Scenario
2. Click the **Edit Object** button (pencil icon) and modify locators manually, or click the **Object Picker** button (arrowhead in square icon) and then click an object in the web app under test
3. (Optional) Expand and review the revision history of the Object. The change log contains the time of the edit, who made the change, and a change note
4. Make any additional changes and save the updates
5. Debug your test to verify results
6. (Optional) To save your changes to the shared Test Action Library, click **Override Group Action**

### Define Scenario Steps

You create scenario steps out of Actions, Objects, and parameter values.

The [Taurus Actions](skill-blazemeter-functional-testing://references/gui-tests.md) are a predefined set. You cannot create new Actions. Available Actions include assertions, clicking buttons, selecting dropdown items, entering text, pausing, submitting a form, opening URLs, and many more.

For each scenario step, you can define a name, an Action, an Object, and values. The following example shows a test step that selects a flight departure time of 10:00 AM from a menu object.

In a test step such as clicking a button, or typing text into a form field, an Action is applied to an Object. Use the **Object** menu to search the project for existing Objects or to record new Objects, such as buttons.

Lastly, in the **Value** field, define any applicable values. A value can be, for example, a name to enter into a form field, a postal code number, a time selected from a selector, a URL, and more. Not all actions require values.

### Add and Modify Scenario Sections

Scenario sections help you gain granularity in your test data. The scenario sections you set up when creating your test show as labels in your test results. You can Rename, Duplicate, or Delete scenario sections by opening the more options menu at the end of the row.

To add a scenario section:

1. Click the **+ Add scenario section** button at the bottom of the scenario window. You can add as many scenario sections as you like
2. Name the scenario section
3. Define the scenario section by dragging actions from other scenarios to it, or add new actions from the left panel

### Create Groups

A custom Group contains multiple Actions that occur together in a given order. For example, you can create a custom "Login" Group that contains a sequence of three Actions, "Enter User ID," "Enter Password," "Click Submit."

Groups are useful because they can be shared, but the use of groups is not mandatory to create scenarios. You add Groups to a scenario in the same way as you add single Actions.

To create a Group directly from the Test Definition, drag a sequence of Actions into the Scenario Editor, and select their check boxes. The selected steps must be consecutive without gaps. Then enter a name for the Group and click **Save As Group Action**.

You can nest Groups inside other Groups, but you will not be able to drill down and edit nested Groups directly in the Scenario Editor.

### Edit Groups

From the Test Action Library, you can edit only the name and description of a Group. You edit the Actions, Objects, and values inside a Groups from the Scenario Editor. Such local changes are automatically saved only in the current scenario.

You can overwrite the values of the original Group in the Test Action Library, or choose to save your changes as a new Group in the Test Action Library.

Follow these steps:

1. Find the Group in the Scenario Editor and expand it. If you cannot find the Group in the Scenario, use the **Test Action Library** to find where the Group is used
2. Click the Edit button (pencil icon) to edit elements of the Group
3. Debug your test to validate your changes
4. (Optional) Click **Override Group Action** to save your changes to the shared Test Action Library

### Create a Browser-Based Test

You can create a Browser-Based Test by uploading a YAML script with a Selenium executor. For more information, see [Creating a Taurus Test](skill-blazemeter-performance-testing://references/taurus.md).

### Scriptless Scenario Creation Tips

- To reorder steps, drag them to new locations in the scenario list
- To remove a step from the scenario, click the trash can button
- To create an editable copy, click the **Duplication** button
- To find Objects, Actions, and Groups by name, use the search box
- To view the appearance of the Object in the user interface, click the **Screenshot** button

### Test Execution Settings

- **Location**: You can choose a specific public cloud or private location to run the test
- **Browser**: By default, the test runs in the latest Chrome browser. If you created a private location that has other browsers and versions configured, you can select specific browsers in which to run the test
- **Virtual Services Configuration**: If you created a virtual services configuration, you can assign it to this test

---

## Create a Performance Test

BlazeMeter engines run on [Taurus](https://gettaurus.org/) and support various different open-source testing tools. Upload your own JMX script to run a JMeter test, or run a Gatling test by uploading a .scala file. The same goes for [K6](https://help.blazemeter.com/docs/guide/performance-create-k6-test.htm), Selenium Java/Ruby/Python and others. Additional files distributed to every test engine can be added too.

**Use when**: Creating a Performance Test in BlazeMeter or uploading test scripts for various testing tools (JMeter, Gatling, K6, Selenium, etc.).

### Create a Performance Test

**Steps:**

1. In the main menu, click the **Performance** tab
2. Click **Create Test**
3. Select a project
4. Click **Performance Test**

The **Configuration** tab for the test opens.

**Note**: If you uploaded a test script but BlazeMeter did not automatically recognize what type of test it is, consider adding a YAML configuration file to help identify it and configure the system.

### Configure a Test

How you configure your test from here depends on what type of test you want to use. The options are:

- If you uploaded a JMeter JMX script, see [Creating a JMeter Test](skill-blazemeter-performance-testing://references/advanced-features.md)
- If you uploaded a Taurus YAML configuration file with your script, see [Creating a Taurus Test](skill-blazemeter-performance-testing://references/taurus.md)
- If you want to create a Scriptless URL or API test, see [Creating a URL/API Performance Test](skill-blazemeter-performance-testing://references/advanced-features.md)
- If you uploaded a script without including a YAML configuration file, fill out the configuration options in your test

### Load Testing Best Practices

To learn more about advanced performance test configuration options, see:
- [Scenario Definition](skill-blazemeter-performance-testing://references/scenarios.md)
- [Load Configuration](skill-blazemeter-performance-testing://references/load-configuration.md)
- [Load Distribution](skill-blazemeter-performance-testing://references/load-configuration.md)
- [Virtual Services Configuration](skill-blazemeter-service-virtualization://references/virtual-services.md)
- [Failure Criteria](skill-blazemeter-performance-testing://references/advanced-features.md)
- [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md)
- [APM Integration](skill-blazemeter-performance-testing://references/advanced-features.md)
- [JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
- [DNS Override](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Network Emulation](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Duplicate, Delete or Move a Test](https://help.blazemeter.com/docs/guide/performance-duplicate-delete-move-test.html)
- [Debug Test: Low-Scale Test Run, Enhanced Logging](skill-blazemeter-performance-testing://references/troubleshooting.md)
- [Original Test Configuration Report](https://help.blazemeter.com/docs/guide/performance-original-test-configuration-report.html)
- [Reporting Selectors for Scenario and Location](https://help.blazemeter.com/docs/guide/performance-filter-by-location-scenario.html)

---

## Create JMeter Test

Apache JMeter is an open source load testing tool that enables you to execute performance tests on your app or website. To run a load test, create a script that will detail the steps of your testing scenario and then run it. You can run your JMeter script locally on JMeter, in the Cloud, or from behind a firewall on BlazeMeter.

**Use when**: Creating and running JMeter Performance Tests in BlazeMeter, uploading JMX files, calibrating tests, or running at full load.

This article will take you through an overview of running a JMeter test on BlazeMeter.

### Step 1: Write and Test Your Script in JMeter

You can create your script manually in JMeter or automatically by recording your scenario in:
- [BlazeMeter Chrome Extension](skill-blazemeter-recorders://references/chrome-extension.md)
- [BlazeMeter Proxy Recorder](skill-blazemeter-recorders://references/proxy-recorder.md)
- Apache JMeter HTTP(S) Test Script Recorder

For additional guidance on how to create and test your script in JMeter, see Step 1 and Step 2 in the [Calibrating a BlazeMeter test](skill-blazemeter-performance-testing://references/jmeter-configuration.md) guide.

### Step 2: Upload Your JMX and Test Assets

Follow these steps:

1. In the main menu, click the **Performance** tab
2. Click **Create Test**
3. Select a project
4. Click **Performance Test**
5. Click **+** to upload your JMX script and any additional test files, such as CSV or JAR files, or drag the files over the **Upload Script** box

**Important Notes:**
- All the files in your account are downloaded to the remote servers at the beginning of each test
- Files from the original test configuration may be updated or deleted at any time. Doing so will not impact a test while it's running

You created a Scenario Definition. For more information, including what to do if your file fails validation, see [Scenario Definition](skill-blazemeter-performance-testing://references/scenarios.md) and [Uploading Files](https://help.blazemeter.com/docs/guide/performance-upload-files.html).

### Step 3: Calibrate Your Test

Before running your test at load, you must calibrate your test according to the [Calibrating a BlazeMeter test](skill-blazemeter-performance-testing://references/jmeter-configuration.md) guide. Configure your test options and set up overrides in preparation for running your JMeter Performance Test at full load.

### Step 4: Run Your Test

Click **Run Test**. You can also click **Debug Test** to validate your test configuration. For more information about debugging, see [Debug Test: Low-Scale Test Run and Enhanced Logging](skill-blazemeter-performance-testing://references/troubleshooting.md).

When your test begins, a report of test results shows, beginning with the [Summary Report](skill-blazemeter-performance-testing://references/reporting.md).

### Additional Test Options

There are optional settings to further enhance testing. For more information, see:
- [Failure Criteria](skill-blazemeter-performance-testing://references/advanced-features.md)
- [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md)
- [APM Integration](skill-blazemeter-performance-testing://references/advanced-features.md)
- [JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
- [DNS Override](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Network Emulation](skill-blazemeter-performance-testing://references/advanced-features.md)
- [JMeter Auto Correlation](https://help.blazemeter.com/docs/guide/performance-jmeter-auto-correlation-rules.html)
- [Ignore Labels in Reports](https://help.blazemeter.com/docs/guide/performance-ignore-labels-in-reports.htm)

---

## Create Multi Test

Create multi-tests for distributed load testing. The multi-test synchronizes and aggregates the results from multiple test sessions into a single aggregated report. The multi-test configuration includes individual test configurations orchestrated to run simultaneously. Each test is still individual and can be run independently as well.

**Note**: In order to create multi-tests, you must have an account on a Pro subscription or higher.

**Use when**: Creating multi-tests for distributed load testing, synchronizing and aggregating results from multiple test sessions into a single aggregated report, or running multiple test scenarios simultaneously.

### Set Up a Multi-Test

**Important Constraints:**
- Only tests within the same project can be included in a multi-test
- You cannot add a specific test multiple times to the same multi-test with the same name. Instead, make one or more copies of the test, each with unique test names that are different from the original test name. Then, when building the multi-test, add the original test and its copies
- You can only add up to 20 scenarios in one multi-test

Follow these steps:

1. In the main menu, click the **Performance** tab
2. Click **Create Test**
3. Select a project
4. Click **Multi Test**. A multi-test configuration screen opens
5. Click the **Add tests** search box. A drop-down list with tests appears
6. Check the box next to each test that you want to add to the multi-test. You can also type in a name of the test and then select the test
7. Click the **Add tests** button at the bottom of the list

To close the window, click anywhere outside of the window.

### Review the Summary

The main **Summary** section of the configuration page provides an overview of the combined multi-test:

- **Scenarios**: Shows the total number of scenarios (single tests) that you chose for the multi-test, and lists the name of each scenario
- **Locations**: Lists all locations used by all scenarios combined
- **Duration**: The total duration of the entire multi-test. This duration is determined by the duration of your single scenarios
- **VU**: The total number of virtual users (VUs) executed across all scenarios combined

The graph to the right of the summary is a visual representation of the total VUs (y-axis) across the total duration (x-axis).

Your multi-test summary shows all the combined information from the individual tests.

### Review the Scenarios

Under the summary is a section dedicated to each individual scenario within the multi-test. The initial scenario window displays (from top-left to bottom-right):
- The name of the single test
- The name of the single tests scenario(s)
- The type of test
- The location(s) the test will run from
- The total virtual users to run
- The duration of the single test

### Modify the Scenarios

To expand the scenario summary to see additional details, click the right arrow (>) in the individual scenario summary. To remove a test, click the bin icon for the scenario.

A miniature version of the [Load Configuration](https://help.blazemeter.com/docs/guide/performance-load-configuration.html) and the [Load Distribution](https://help.blazemeter.com/docs/guide/performance-load-distribution.html) screens appears. You can modify an individual test scenario but only when it runs as part of this multi-test.

**Important**: Disabling overrides in Load Configuration will cause the values to be taken from the single test's original script, and not from that test's original configuration (if overrides are enabled).

### Run the Multi-Test

Once you are satisfied with the summary and have made any adjustment to your scenarios, click the **Run Test** button on the left-hand side of the screen to run your new multi-test.

The next screen provides a final summary of the test you are about to execute. There are two options you can select prior to launching:

- **Synchronized start**: Ensures that all servers are up before actually starting the test. Select this option if you have a concern that some servers or locations are significantly slower than others and you wish to synchronize them
- **Run test in the background**: Executes the test behind the scenes so that you can continue working in BlazeMeter

### Add Load or Logic During a Test

You can add additional load or entirely new test logic to a large test that is already running. No need to stop, reconfigure and re-launch. Launch an additional test and join it to the multi-test in progress.

Follow these steps:

1. Start a multi-test
2. Once the multi-test is started, start an individual single test
3. On the **Launch Test** screen, click the dropdown menu under **Run this test as part of a master session?** and select **Run as a test under {name of your multi-test}**
4. Click the **Launch Servers** button

You can then return to your multi-test in progress, which is now running with the additional scenario.

For more information, including how to add tests via the API, see [Adding Users Dynamically](https://help.blazemeter.com/docs/guide/performance-add-users-dynamically.html).

---

## Create URL/API Test

Creating a new URL/API Test in BlazeMeter is as simple as performing a single GET to a URL. When a more advanced test is needed, the URL/API Test Scenario Definition provides a range of advanced options. The automatic scripting feature generates a Taurus YAML script that executes a JMeter test in where each virtual user will hit each URL sequentially. Each virtual user has their own browser session, cache, and cookies.

To record complex scripts directly from your Google Chrome browser, use the Chrome Extension or Proxy Recorder.

**Use when**: Creating URL/API Performance Tests with automatic scripting, adding query parameters, headers, body, assertions, or extracting data from responses.

### Create a Test

Follow these steps:

1. In the main menu, click the **Performance** tab
2. Click **Create Test**
3. Select a project
4. Click **Performance Test**
5. Click the arrow for the **URL / APIs Test**
6. Add requests. Enter the **Request name** and **URL**
7. (Optional) If you want to run multiple API calls, you can create a sequential chain of multiple requests. To add more requests, click **+** in the **Scenario Definition** section
8. (Optional) To select a different request method, expand the drop-down list
9. (Optional) To duplicate or delete requests, click the dots menu
10. On the left panel, edit the test name
11. (Optional) Enter the test **Description** and add **Schedule**

### Add Details to a Test

The advanced options available in the Scenario Definition let you quickly create more complex URL/API tests.

#### Add Query Parameters

The Query Parameters tab provides option fields for adding parameters to an API call for querying specific data:

1. In **Scenario Definition**, click the **Query parameters** tab
2. Enter values into the **Key** and **Value** fields. New lines are added automatically
3. (Optional) To delete an entry, click the bin icon on the right

BlazeMeter creates the API call automatically appending the parameters to the end of the URL.

**Example**: The API endpoint *https://api.demoblaze.com/entries* allows the use of the **Name**, **Name2** and **Name3** keys to query name values. BlazeMeter creates: *https://api.demoblaze.com/entries?Name=Value&Name2=Value2&Name3=Value3*.

#### Add Headers

**Key** and **Value** fields for adding HTTP headers to your API call may be required by your application server:

1. In **Scenario Definition**, click the **Headers** tab
2. Enter values into the **Key** and **Value** fields. New lines are added automatically
3. (Optional) To delete an entry, click the bin icon on the right

#### Add Body

The **Body** tab only appears if the request type allows sending body data. For example, for a **GET** request, there will be no **Body** tab available:

1. In **Scenario Definition**, click the **Body** tab
2. Enter the values

You can enter body data in the following formats:
- **Key Value** - If the application server requires body data to be sent via specific keys
- **Text** - For entering raw text, such as JSON content
- **Content from file** - If you have a file containing the required body data, upload it here
- **Attach binary files** - This option consists of three fields: a parameter name field, an option to upload a file for the parameter, and a field for providing the mime-type (determined automatically if let blank)

#### Add Assertions

Add assertions to verify the existence of specific data in the response:

1. In **Scenario Definition**, click the **Assertions** tab
2. From the drop-down list, select the type
3. Fill in the values and click **Add**
4. (Optional) Add multiple assertions

If you add a **Text** assertion, BlazeMeter automatically changes the assertion to a **Regex** type and checks the body for the entered value.

If an assertion fails, it shows under the **Errors** tab in the test report. Click the **Assertion Name** tab to review the failures.

#### Extract Data from Responses

You can extract data from the response and store it in a variable for future use:

1. In **Scenario Definition**, click the **Extract from response** tab
2. From the drop-down list, select the type
3. Enter the values and click **Add**
4. (Optional) Copy the variable
5. (Optional) You can then paste the variable into another request, to add it to a URL or other request field. The variable will show in the format of *${variable}*

### Configure Load

Follow these steps:

1. Configure the load by specifying the total users, duration, and ramp up time. For more information, see [Load Configuration](skill-blazemeter-performance-testing://references/load-configuration.md)
2. Configure the load distribution to decide where traffic will be coming from. For more information, see [Load Distribution](skill-blazemeter-performance-testing://references/load-configuration.md)
3. Click **Run Test** to start the test or **Debug Test** to validate your test configuration. For more information about debugging, see [Debug Test: Low-Scale Test Run and Enhanced Logging](skill-blazemeter-performance-testing://references/troubleshooting.md)

### Additional Test Options

In addition to the required settings above, there are optional settings to further enhance testing. For more information, see:
- [Failure Criteria](skill-blazemeter-performance-testing://references/advanced-features.md)
- [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md)
- [APM Integration](skill-blazemeter-performance-testing://references/advanced-features.md)
- [DNS Override](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Network Emulation](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Ignore Labels in Reports](https://help.blazemeter.com/docs/guide/performance-ignore-labels-in-reports.htm)
- [Ignore Labels in Reports](https://help.blazemeter.com/docs/guide/performance-ignore-labels-in-reports.htm)

#### Add Assertions

Add assertions to verify the existence of specific data in the response:

1. In **Scenario Definition**, click the **Assertions** tab
2. From the drop-down list, select the type
3. Fill in the values and click **Add**
4. (Optional) Add multiple assertions

If you add a **Text** assertion, BlazeMeter automatically changes the assertion to a **Regex** type and checks the body for the entered value.

If an assertion fails, it shows under the **Errors** tab in the test report. Click the **Assertion Name** tab to review the failures.

#### Extract Data from Responses

You can extract data from the response and store it in a variable for future use:

1. In **Scenario Definition**, click the **Extract from response** tab
2. From the drop-down list, select the type
3. Enter the values and click **Add**
4. (Optional) Copy the variable
5. (Optional) You can then paste the variable into another request, to add it to a URL or other request field. The variable will show in the format of *${variable}*

### Configure Load

Follow these steps:

1. Configure the load by specifying the total users, duration, and ramp up time. For more information, see Load Configuration
2. Configure the load distribution to decide where traffic will be coming from. For more information, see Load Distribution
3. Click **Run Test** to start the test or **Debug Test** to validate your test configuration

### Additional Test Options

In addition to the required settings above, there are optional settings to further enhance testing:
- Failure Criteria
- End User Experience Monitoring
- APM Integration
- DNS Override
- Network Emulation
- Ignore Labels in Reports

---

## Dedicated IPs

Assign dedicated (static) IP addresses to BlazeMeter engines for connecting from behind corporate firewalls, including purchasing and activating dedicated IPs. If you need to connect from behind the corporate firewall, you need the BlazeMeter engines to have dedicated (static) IP addresses. You can assign dedicated IPs to your BlazeMeter engines. Each IP address belongs to a specific region, for instance, US East (Virginia), EU West (London), or any other Google Cloud location.

When you run tests in BlazeMeter using dedicated IPs, a specific pool of IP addresses within a selected region is reserved for your workgroup. When you initiate a test with dedicated IPs, BlazeMeter assigns an IP from this pool to execute the test. Once the test is complete, the IP is released back into the pool for future use. If multiple tests from the same workspace and region use dedicated IPs, they may end up using the same IP address, even if the tests run on different engines. This reuse of IPs is not an issue as long as the tests are not executed simultaneously.

**Use when**: Assigning dedicated IP addresses to BlazeMeter engines, connecting from behind corporate firewalls, or purchasing and activating dedicated IPs.

### Purchase Dedicated IPs

Typically, you purchase one IP address for every engine on your plan. The purchased IP addresses are reserved exclusively per customer.

**Examples:**
- 20 engines plan = 20 IPs
- 50 engines plan = 50 IPs
- 100 engine plan = 100 IPs

### Activate Dedicated IPs

To request for dedicated IPs in your BlazeMeter account, [create a support ticket](https://help.blazemeter.com/docs/answers/support-ticket.html) or contact your BlazeMeter account manager.

The following information is required:

- The account associated email address in BlazeMeter
- The region(s) you want and how many IP addresses should be allocated to each region. For example: 10 IPs in Oregon, 20 IPs in Sydney, 30 IPs in Sao Paulo

BlazeMeter will follow up with you and complete the purchase order for these IPs. Your static IP address allocation takes up to 24 hours after receiving confirmation from the step above.

**Available regions include:**

**Google:**
- US Central (Iowa) - us-central1-a
- US West (Oregon) - us-west1-a
- US West (California) - us-west2-a
- US East (Virginia) - us-east4-a
- US East (South Carolina) - us-east1-b
- Canada East (Montreal) - northamerica-northeast1-a
- EU West (London) - europe-west2-a
- EU West (Frankfurt) - europe-west3-a
- EU West (Belgium) - europe-west1-b
- EU West (Netherlands) - europe-west4-b
- Asia East (Taiwan) - asia-east1-a
- Asia Northeast (Japan) - asia-northeast1-a
- Japan (Osaka) - asia-northeast2
- Asia Southeast (Singapore) - asia-southeast1-a
- Asia South (Mumbai) - asia-south1-a
- Australia (Sydney) - australia-southeast1-a
- Brazil (Sao Paulo) - southamerica-east1-a

**Amazon Web Services:**
- US East (Virginia)
- US East (Ohio)
- US West (N.California)
- US West (Oregon)
- Canada (Central)
- EU West (Ireland)
- EU West (London)
- EU West (Paris)
- EU Central (Frankfurt)
- Asia Pacific (Tokyo)
- Asia Pacific (Mumbai)
- Asia Pacific (Seoul)
- Asia Pacific (Singapore)
- Australia (Sydney)
- South America (Sao Paulo)

### View Dedicated IPs

Follow these steps:

1. Click the **Settings** button in the top right corner
2. From the menu on the left, expand the **Workspace** drop-down list
3. Click **Dedicated IPs**

Your IP addresses are available for you at any time when you run a test in the region that you purchased.

### Run a Test with Dedicated IPs

1. Create a new test or configure an existing one
2. Go to the **Configuration** tab
3. Scroll down to **Load Distribution** section
4. From the **Locations** drop-down list, select your test location
5. Select the **Use Dedicated IPs** checkbox. The number of IP addresses should be the same as the number of servers used in the test

### Sharing Dedicated IPs with other Workspaces

You can share Dedicated IPs with several workspaces to use them more efficiently. Users in different workspaces on your account can use the same shared Dedicated IPs as testing locations. But remember, only one test can use a shared Dedicated IP at a time.

To do so, [contact our support team (support-blazemeter@perforce.com)](mailto:support-blazemeter@perforce.com?subject=Sharing dedicated IPs with other workspaces) and tell them which Dedicated IPs you want to share and with which workspaces you want to share them in your account.

After the shared Dedicated IPs are set up, users in different workspaces can assign the shared Dedicated IPs to their tests and then run those tests.

---

## Failure Criteria

The Failure Criteria feature allows you to set the pass or fail criteria of your test for various metrics, such as response times, errors, hits per second, test duration, and so on.

**Use when**: Setting pass/fail criteria for performance tests, automating test result determination, or comparing test results against baselines.

### Enable and Define Failure Criteria

To enable failure criteria, follow these steps:

1. In the Performance tab, click **Create Test**, **Performance Test**
2. Scroll down to the **Failure Criteria** section and toggle the button ON

The following parameters are available:

- **Label**: Specify if you want to use this rule on a particular label from your script. It is set to **ALL** (all labels) by default
- **KPI**: Select the specific metric you want to apply a rule for. Expand the drop-down menu and review the available metrics to monitor
- **Condition**: To see the binary comparison operators for this rule, expand the drop-down menu. Operators include **Less than**, **Greater than**, **Equal to**, and **Not Equal to**
- **Threshold**: The numeric value you want this rule to apply to
- **Stop Test**: You can only select this option together with the **1-min slide window eval** option. When selected, the test will stop immediately after the first violation is detected. Otherwise, the test continues running uninterrupted until the test ends
- **Delete Failure Criteria**: Click the trash bin icon to delete the criteria
- **1-min slide window eval**: Select this option to configure the test to evaluate the failure criteria during the test run. The failure criteria are evaluated every 10 seconds for a period of 60 seconds instead of just once at the end of the test. The failure criteria will fail the test if at least one violation is found
- **Ignore failure criteria during ramp-up** (Advanced configuration drop-down): Checking this box causes the test to ignore any failures that occur during ramp-up so that criteria are only evaluated after ramp-up ends

If implemented, the pass/failure results can be seen via the workspace dashboard, making it easier to monitor your testing over time. The dashboard is accessed by selecting the Workspace of interest from the Workspace menu drop-down list.

For Taurus tests (tests that use a YAML configuration file), the majority of Taurus pass/fail capabilities are translated into BlazeMeter failure criteria. This ensures that when a YAML script is uploaded to BlazeMeter, the pass/fail module in the script will automatically appear in the test UI. You can also execute a test from Taurus with cloud provisioning, and the pass/fail module will be recognized by BlazeMeter and displayed in the report.

### Define Failure Criteria Using the Baseline

One of the most useful things about having a baseline to compare with, and fail the test in comparison to it (baseline-based failure criteria), is to have more accurate failures when automating your tests.

When you set a report as a baseline, you can also set the failure criteria against the baseline. If performance degrades compared to the baseline in a subsequent test, the test will fail automatically.

**Steps:**

1. Go to the **Performance** tab, click **Tests** and select a test from the drop down list. The test reports window opens
2. Click the **Configuration** tab and scroll down to the **Failure Criteria** section
3. Toggle the button for **Failure Criteria** on
4. Check the box for **Use from baseline**. This checkbox is available only if there is a baseline selected for the test
5. You can:
   - Set the threshold for each failure criteria from the selected baseline
   - Define an offset from baseline you want to tolerate, so that minor deviation from baseline will not be defined as a failure. If you use Baseline to define the threshold, the threshold will be visible after save

Subsequent tests are compared against the baseline with these failure criteria. If performance degrades compared to the baseline and the defined offset, the test will fail automatically.

### Fail Tests against the Baseline when Running from Taurus

In this section, we will focus on defining baseline-based failure criteria in Taurus.

The failure criteria using the Baseline can be configured in the YAML and "translated" into BlazeMeter failure criteria.

**Important**: Failing tests from Taurus in comparison to the baseline is only possible in case:
- The test is already defined in BlazeMeter (not for new tests created via Taurus)
- The test has a baseline defined in BlazeMeter (you can't set a baseline for a test while running it in Taurus)

You can define the failure criteria in the YAML file. This can be done when:
- Running YAML test in BlazeMeter
- Running existing Taurus tests from Command line in the cloud (in BlazeMeter) and not locally

For each pass/fail criteria, you can define if it is taken from baseline and with which offset.

**Example:**
```yaml
reporting:
- module: passfail
criteria:
- avg-rt>baseline, stop as failed
- avg-rt>baseline+5%, stop as failed
- hits<baseline-5%, stop as failed
```

The above example uses baseline as a threshold for the criteria.

**Format:**
```
[KPI] [Condition] baseline [Offset]
```

**Explanation:**
- **KPI**: the KPI that will be compared
- **Condition**: the comparison operator, one of >, <, >=, <=, =, == (same as =)
- **Baseline**: the phrase "baseline" indicates that the value to compare with (the threshold) is taken from the baseline
- **Offset**: the percent of deviation from baseline that should be tolerable and not fail the test

**Validations:**
- If the condition is > or >=, the offset must be defined, with a "+" sign
- If the condition is < or <=, the offset sign must be defined, with a "-" sign
- If the condition is = or ==, offset must not be defined

In case validation failed or syntax is incorrect, the pass/fail criteria will not be recognized and enforced by BlazeMeter.

### Stop Tests when Running from Taurus

You can configure tests to stop from Taurus and YAML scripts.

In a Taurus YAML script, you can configure a test to stop in the event that it reaches a threshold, by defining the `timeframe` value and `stop` action. `timeframe` is converted in BlazeMeter to the **1-min slide window eval** option and `stop` to the "**Stop Test?** option.

In the `pass/fail` module in the YAML script, set `timeframe` to `for 1m` (`for 60s` is also valid), and define the test to stop with one of the following actions: `stop as fail`/`stop as failed`/`stop`.

**Examples:**
```yaml
avg-rt>20s for 1m, stop as fail
avg-rt>20s for 60s, stop as failed
avg-rt>20s for 1m, stop
```

For all the above examples, the failure criteria in BlazeMeter will look as follows with **1-min slide window eval** and **Stop Test?** enabled.

You can also configure the test to continue even if it reaches the threshold, if you use `continue` instead of `stop`. For example:
```yaml
avg-rt>20s for 1m, continue
```

**Important Notes:**
- Timeframes other than `for` are not supported by BlazeMeter. In this case, the `pass/fail` module is converted to a failure criteria **without** the **1-min slide window eval** and **Stop Test?** options
- Timeframes other than one minute (60 seconds) are not supported by BlazeMeter. In this case, the `pass/fail` module is converted to a failure criteria **without** the **1-min slide window eval** and **Stop Test?** options
- The test result (`pass`, `failed`) cannot be configured through Taurus. In BlazeMeter, the test result is calculated based on the failure criteria. If at least one threshold is reached, the test result is `failed`. If you use Taurus syntax to set the test result to `pass` (for example `avg-rt>20s for 1m, stop as pass`), it is ignored

### Baseline-Based Taurus Failure Criteria in BlazeMeter UI

Like other Taurus pass/fail criteria, baseline-based criteria in YAML are translated to BlazeMeter failure criteria and appear in the test configuration UI.

- **KPI**: the Key Performance Indicator defined in the pass/fail criteria
- **Condition**: the comparison operator in the pass/fail criteria will be translated to the parallel phrase, e.g. ">=" will be translated to "Greater than or equal to"
- **Threshold**: the value is calculated from the baseline and offset. For example, if average response time in baseline is 100 ms and the criteria had a "+5%" offset, the threshold would be baseline+5% which is 105 ms
- **Use from baseline?**: true
- **% offset** = the percentage defined in the pass/fail without the +/- sign. The +/- sign will be used to add or reduce the offset percent from the baseline when calculating the threshold

---

## DNS Override

Override DNS resolution in test engines to point hostnames to different IP addresses during tests without editing scripts. Override DNS places entries in /etc/hosts of each test engine so a hostname in your script is resolved to a different IP address during your test. This allows you to "point" your test at an alternate server without editing the script.

**Use when**: Overriding DNS resolution in test engines or pointing hostnames to different IP addresses during tests without editing scripts.

### Configure DNS Override

Follow these steps:

1. In the Performance tab, click **Create Test**, **Performance Test**, or open an existing test
2. Scroll down to the **DNS Override** section
3. Toggle the DNS Override ON
4. Enter the hostname and alternate IP address
5. (Optional) You can override as many hostnames as needed. A new line shows up automatically

**How it works**: When DNS Override is enabled, BlazeMeter adds entries to the `/etc/hosts` file on each test engine. This ensures that when your script references a hostname, it resolves to the IP address you specify instead of the default DNS resolution.

This feature is particularly useful when:
- Testing against staging or pre-production environments
- Redirecting traffic to different servers for load balancing testing
- Testing with different IP addresses without modifying test scripts
- Avoiding DNS resolution delays during tests
- Testing with custom DNS configurations

---

## End User Experience Monitoring

Configure End User Experience Monitoring for performance tests, including URL monitoring and Selenium scenario execution.

**Use when**: Configuring End User Experience Monitoring for performance tests or monitoring real user experience with Selenium scenarios.

### Overview

To gain better understanding of real user experience of your application server performance under load, enable the End User Experience (EUX) Monitoring option in BlazeMeter while running a load test. EUX monitoring is available only for Pro or higher subscription plans.

For example, you might find that your backend can handle the load, but the page takes ten seconds to reach a state that is adequate for a user to interact with. The waterfall report can aid you in uncovering performance issues like page loading in the browser — issues that JMeter alone is not able to identify.

### How Monitoring Works

End User Experience Monitoring uses Taurus to execute a Selenium test (YAML) in the background while your load test is running. The goal of EUX is not to report whether the functional test passes; EUX only uses the test to capture response times. The Waterfall Report surfaces the load times that users experience in their web browsers at different points during the load test. This is especially helpful when trying to debug why a page failed to load properly *from the users' point of view* at a certain point in the load test.

When a test is executed with **End User Experience Monitoring** enabled, BlazeMeter wraps the label and the URL specified with a YAML configuration file. Alternatively, you can supply a YAML script of your own. BlazeMeter executes the YAML script via Taurus and Selenium for the full duration of the load test.

The End User Experience Monitoring report can record videos that reflect the user experience of opening the URL or running the Selenium scenario. For each choice of browser and version, the test report includes a video of the test execution. By default, video recording is enabled. In addition to the waterfall view, you also see test steps, logs and metadata.

### Requirements for End User Experience Monitoring

- **Subscription**: EUX monitoring is available only for Pro or higher subscription plans
- **Engines**: Tests with EUX monitoring configured require at least four engines:
  - One engine for the performance test
  - Three engines for the Selenium test
- **Private Locations**: EUX tests don't run on Private Locations that have more than one agent. To run EUX tests, ensure to have only a single agent assigned

### Prerequisites

- Ensure your workspace is on a Pro plan or higher to meet engine requirements and access EUX features. Multiple URLs can only be monitored with paid plans
- Verify you have enough concurrent engines available in your plan to avoid test interruptions. Pro plans and higher support up to 20 concurrent engines, which is essential for running EUX tests
- EUX tests don't run on Private Locations that have more than one agent. To run EUX tests, ensure to have only a single agent assigned

### Configure End User Experience Monitoring

Follow these steps:

1. Open the **Performance** tab
2. Click **Create Test** and click **Performance Test**, or open an existing test
3. Scroll down to the **End User Experience Monitoring** section and toggle the button ON
4. Choose one of the following options:
   - **URL list**: The EUX test opens one or more specified web pages. See [Choose a URL to Monitor](#choose-a-url-to-monitor)
   - **Selenium Scenarios**: The EUX test performs the steps defined in the scenarios. See [Upload Selenium Scenarios](#upload-selenium-scenarios)

### Choose a URL to Monitor

To test the user experience of opening one page, follow these steps:

1. In the **URL list** tab, specify at least one URL to monitor during the test. Start each URL with either "http://" or "https://". An empty line to add another URL appears automatically
2. For each URL, enter a label name to identify this test case later in the report

### Upload Selenium Scenarios

Instead of specifying only URLs, you can upload Selenium scenarios to run via Taurus.

Follow these steps:

1. Create a Taurus YAML configuration to execute your Selenium scenario and upload it to the test. End User Experience Monitoring only supports YAML files in which the Selenium scenario is scripted within the YAML. It does not support pointing a YAML to a separate script, such as one written in Java or Python
2. Identify the test's "**Start test with:**" property. Ensure that the Performance test script is still selected as the main file, and not the Selenium scenario. In the following sample screenshot, you see that the JMX file is correctly selected
3. On the **Selenium Scenarios** tab, select the boxes for scripts that you want to execute as monitoring tests
4. Define the test execution settings
5. Run the test

### Define Test Execution Settings

For End User Experience Monitoring tests, you can define Location and Browser:

- **Location**: Choose a public Cloud location, or a private location for test execution. For more information, see [Cloud vs Private Location](https://help.blazemeter.com/docs/guide/private-locations-vs-cloud.html) and [Get the Location Name](https://help.blazemeter.com/docs/guide/api-get-the-location-name.html). The choice of location also determines which browsers are available. When you do not select a location, the EUX test uses the default location for GUI Functional tests
- **Browser**: (If the test has a location assigned:) Choose browser and browser version. For each choice of browser and version, the test report includes a video of the test execution. For more information, see [Supported browsers](https://help.blazemeter.com/docs/guide/functional-supported-browsers.html). Each test can be run in multiple browsers and multiple versions. By default, and if no location is selected, the EUX test runs in the latest Chrome browser. If you have created a private location that has custom browsers and versions configured, you can select additional browsers

### Run the Test

After specifying either the URLs to access or uploading your Selenium scenarios, click **Run Test**.

After the test starts, you see both the load test and the user experience monitoring test executed simultaneously.

When the test report appears, you see the report tabs and the **End User Experience Monitoring** tab.

### View the Report

There are two ways to view the End User Experience Monitoring report:

- If you want to go straight to the monitoring report, navigate to the **End User Experience Monitoring** tab
- If you want to see monitoring results alongside other test metrics first, navigate to the **Timeline Report** tab. Under the KPI Selection on the left, expand the **Real User Experience** section

You will find your named label(s) for your monitored URL(s). Select a label and it will be displayed as a series of dots on the graph.

The vertical Y axis represents page load time in the web browser. The horizontal X axis represents time. Each single dot represents the execution time of the Selenium test at a specific moment in time, where higher dots represent longer execution time.

Click a dot to open the **End User Experience Monitoring** tab.

### View the End User Experience Monitoring Tab

Regardless of which of the two methods you choose to follow from above, click the **End User Experience Monitoring** tab to see a graph consisting of individual timeline columns.

Each column in this graph for a label correlates with each dot in the **Timeline Report** for the same label.

### View the Waterfall Report

To open a waterfall report for that moment in time, click a column in the monitoring report.

The waterfall report shows what your users experience when your site is under load. The time shown for each horizontal bar refers to the page load time on the network level.

As you review the waterfall report, you can click to expand each performed request to view more details about it. This is similar to what you would see if you were to open the developer tools for a real browser and examine the network tab.

You can also hover your mouse over each graph in the waterfall report to see expanded information on request phases and their elapsed times.

The waterfall report reveals how long each request took and which requests had the most impact on page load time.

---

## Mainframe Testing (RTE)

Run Performance Tests against mainframes using JMeter-RTE-plugin, supporting TN3270, TN5250, and VT420 protocols. The [JMeter-RTE-plugin](https://github.com/Blazemeter/RTEPlugin) project implements a JMeter plugin to support RTE (Remote Terminal Emulation) protocols. It provides a recorder for automatic test plan creation, configuration, and sampler for protocol interactions with mainframe applications. The plugin supports TN3270, TN5250, and VT420 protocols.

**Use when**: Running Performance Tests against mainframes, using JMeter-RTE-plugin with TN3270, TN5250, and VT420 protocols, or testing mainframe applications with RTE protocols.

### Use the RTE Plug-in with BlazeMeter

Follow these steps:

1. **[Download the plug-in](https://github.com/Blazemeter/RTEPlugin/blob/master/README.md)** through the JMeter Plugins Manager
2. Follow the instructions included for using the RTE Recorder to record the JMX file
3. Upload the following files to the BlazeMeter Performance test:
   - The JMeter script file (JMX)
   - `dm3270-lib-0.5.1.jar`
   - `xtn5250-2.0.1.jar`
   - `jmeter-bzm-rte-1.0.2.jar`
   - Any other files used in your script (CSV, JARs, etc.)

   For more information about how to upload files, see [Shared Folders](skill-blazemeter-performance-testing://references/advanced-features.md) and [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md)

4. Define the load configuration for the test. For more information, see [Load Configuration](skill-blazemeter-performance-testing://references/load-configuration.md)
5. Save the test and press the green **Run** button

You have created a Mainframe load test and it is now running.

BlazeMeter creates a detailed report that provides different KPIs that you can analyze and compare with previous tests. For more information about reporting services and features, see [Summary Report](skill-blazemeter-performance-testing://references/reporting.md).

---

## Network Emulation

Impair connection between BlazeMeter test engines and system under test to observe impact on KPIs, including bandwidth limits, latency, and packet loss.

**Use when**: Impairing connection between BlazeMeter test engines and system under test or observing impact on KPIs with bandwidth limits, latency, and packet loss.

### Overview

Network emulation allows you impair the connection between BlazeMeter test engine and the system(s) you are testing in order to observe the impact on your key performance indicators (KPIs).

### Add Network Emulation to Your Test

Follow these steps:

1. In the Performance tab, click **Create Test**, **Performance Test**
2. Scroll down to the **Network Emulation** section
3. Toggle the feature ON
4. Choose the desired network type
5. (Optional): Customize any of the settings by dragging the sliders or entering values in the boxes

### Network Emulation Configurations

The following configurations are available:

- **Max Bandwidth Per User**: Applies only to JMeter scripts. The bandwidth limit per user can range between 240 and 1,000,000 Kb
- **Max Global Bandwidth**: The bandwidth limit per engine. Value can range between 240 and 1,000,000 Kb
- **Latency - Network Delay (Milliseconds)**: Add network delay to simulate real-world network conditions
- **Packet loss %**: Simulate packet loss percentage. Packet loss % is at 0% by default. Add packet loss with care as a little can have a significant impact

**Important Notes:**
- Bandwidth limits apply to both directions (download and upload)
- Packet loss % is at 0% by default. Add packet loss with care as a little can have a significant impact
- Scroll down to the **Load Configuration** section to configure these settings

---

## Shared Folders

You can use the same files across multiple tests. Upload the files to Shared Folders and include the folders in as many tests as you like. Shared Folders provide a more advanced alternative to simply uploading files to each test. You select which folders to include (rather than individual files). The folders are then downloaded to each of the engines in your test before it starts.

This approach gives you great power. You can update a large number of tests instantly by updating the contents of a single Shared Folder.

**CAUTION!** Always consider that any change you make will impact **every test** that includes that folder, not just the test you are currently configuring.

**Note**: JDBC drivers are an exception to this rule. These must be uploaded directly to the test, as shared folders do not currently support driver uploads.

**Use when**: Using Shared Folders to manage and reuse files across multiple tests, creating folders, uploading files, or referencing files in scripts.

### Create Shared Folders and Upload Files

There are two ways to create a shared folder:

#### Create Folders and Upload Files from within a Test

Follow these steps:

1. Create a new Performance test
2. Click the **Shared Folder** link in the **Upload Script** section
3. To create a new shared folder, click the **+** button. To choose an existing folder, select the checkbox next to the folder
4. If you are creating a new folder, fill in the folder name. Spaces and special characters are not allowed
5. (Optional) To expand the folder and view the files, click the **>** arrow
6. To upload new files to a shared folder, click the **Upload file to folder** icon
7. Click **Accept**

You can find your shared folders in the test in **Configuration**, **Scenario Definition**. The name of the shared folder shows in the **Shared Folder** column.

Once you create a shared folder, it is available to use with any test, not just the test you created it for.

#### Create Folders from the Workspace Menu

1. Navigate to **Settings** in the top right corner
2. From the **Settings** menu on the left, expand the **Workspace** section and select **Shared Folders**. You can view your existing shared folders
3. To create a new shared folder, click the **+ New Folder** button
4. To add files to a folder, click the folder name
5. Drop or upload files
6. (Optional) To make the file read-only, toggle the **Readonly** button

### Reference Shared Folders in Your Script

To point to a file from an included Shared Folder in your script, use the "folder/filename" style path: `folder1/file11.csv` (no leading slash).

**Example paths:**
- A Data Entity created in BlazeMeter named "My test data" → `"My_test_data.csv"`
- A CSV file `my_test_data.csv` uploaded to BlazeMeter and attached to a test → `"my_test_data.csv"`
- A CSV file `our_test_data.csv` uploaded to BlazeMeter's Shared Folder `our_shared_folder` → `"our_shared_folder/our_test_data.csv"`

### Remove a Shared Folder from a Test

Follow these steps:

1. Open a test and navigate to the **Configuration** tab
2. In the **Scenario Definition** section, hover over the **+** button on the right. Once a shared folder is added to a test, a **Shared Folders** button is shown
3. Click **Shared Folders**
4. Uncheck the folders that you want to remove from the test
5. Click **Accept**

### Delete Shared Folders or Files

**CAUTION!** This procedure deletes the folder **and its contents** from **all tests that include this folder**.

There are two ways to delete a shared folder:

#### Delete Shared Folders or Files from a Test Configuration Menu

1. Open a test and navigate to the **Configuration** tab
2. In the **Scenario Definition** section, hover over the **+** button on the right. Once a shared folder is added to a test, a **Shared Folders** button is shown
3. Click **Shared Folders**
4. To delete a shared folder, click the **Delete folder** bin icon next to the folder name that you want to delete. The shared folder will be deleted from all tests that are using the folder
5. To delete a file from a shared folder, expand the folder to display files and click the **Delete file** bin icon for the file that you want to delete. The file will be deleted from all tests that are using the shared folder in which the file is located

#### Delete Shared Folders or Files from the Workspace Menu

1. Navigate to Settings in the top right corner
2. From the Settings menu on the left, expand the **Workspace** section and select **Shared Folders**
3. To delete a shared folder, click the bin icon next to the folder that you want to delete. The shared folder will be deleted from all tests that are using the folder. If the **Readonly** toggle is ON for the shared folder, you cannot see the bin icon and cannot delete the shared folder
4. To delete a file from a shared folder, click the shared folder name to open it and then click the bin icon next to the file that you want to delete. The file will be deleted from all tests that are using the shared folder in which the file is located

---

## Use Test Data in Testing

JMeter scripts can load test data either from external CSV files or from BlazeMeter Data Entities. JMeter test configurations have a script element that lets you read lines from an external file and assign them as values to variables in your script. This element is called the **CSV Data Set Config**. In addition to BlazeMeter's own test data integration, BlazeMeter supports uploaded JMeter scripts with existing CSV Data Set Config.

A Data Entity is a container to store, manage, and share test data in BlazeMeter. BlazeMeter Data Entities support any combination of the following data sources to provide test data to a Performance test:
- CSV spreadsheets
- Generated synthetic test data

You can use one or combine multiple of these data sources in a test, as needed.

**Use when**: Using Test Data in JMeter Performance Tests, working with CSV files, Data Entities, or referencing test data in CSV Data Set Config elements.

### How Do I Reference CSV Files?

Before uploading an existing test configurations to BlazeMeter, edit the JMX and make sure to reference your CSV files using *relative* paths, as shown here. Next, upload existing CSV files or create new Data Entities in BlazeMeter to extend or replace CSV files. When you create a Data Entity in BlazeMeter, BlazeMeter creates a corresponding CSV file that you could download and reference from your JMeter script.

**Data Source Paths:**
- A Data Entity created in BlazeMeter named "My test data" → `"My_test_data.csv"`
- A CSV file `my_test_data.csv` uploaded to BlazeMeter and attached to a test → `"my_test_data.csv"`
- A CSV file `our_test_data.csv` uploaded to BlazeMeter's Shared Folder `our_shared_folder` → `"our_shared_folder/our_test_data.csv"`

### Create Data Entities in BlazeMeter

The BlazeMeter test data integration is flexible: You can start by creating a Data Entity in BlazeMeter and later edit the JMeter file to use it. Or, you can upload existing JMX and CSV files together, and expand the test data in BlazeMeter later. Or, you can record a JMeter test using the Chrome Recorder Extension, and add data entities and CSV files later.

1. Go to the BlazeMeter **Performance** tab
2. Open an existing Performance Test
3. Click **Test Data** and click the Ellipsis button to add a data entity. The **Test Data** pane in BlazeMeter is visible only after you have uploaded or recorded a test script
4. Click the small **plus** button to add one or more data parameters to the data entity
5. (Optional) Download the data entity as a CSV file for external use

### Prepare the Test Configuration File

BlazeMeter uses the first row of data as parameter names to refer to the columns in the CSV file. If the first row of the CSV file does not contain column names, provide a comma-separated list of variable names in the test configuration.

Open the JMX script in JMeter and edit the following fields in the **CSV Data Set Configuration**:

- **File Name**: Provide the *relative* file path of the file attached in BlazeMeter. Example: File Name: `My_test_data.csv`
- **Variable names**: If the first row of the CSV contains column headers, leave this field empty. If the first row contains data, define column name mappings here. To skip a column in the mapping, add an extra comma with no name. Example: Variable names: `lastname,firstname,,street,number,,`
- **Delimiter**: Comma is the default delimiter, but if your file uses tabs, enter `\t` here
- **Ignore first line?**: If the first row of the CSV file contains column headers, enable this option. If the first row contains data, disable this option
- **Allow quoted data?**: If your values can contain commas, and you also use commas as delimiters, then allow quoted values. Example: If a value can be "123 Main street, Springfield", make sure to surround it by double quotes and enable this option, otherwise it will be split into two columns

**Example**: The file "mydata.csv" has six columns and no column headings. You want to reference address data in column 1, 2, 4, and 5, and ignore column 3 and 6. Therefore, you declare the following in the **Variable names** field: `lastname,firstname,,street,number,,`

In a test script, you are now able to reference the values of column 1 as `${lastname}`, column 2 as `${firstname}`, column 4 as `${street}`, and so on.

### Link the Test Data to the Test Configuration

1. Log on to BlazeMeter and go to the **Performance** tab
2. Upload the prepared JMeter file
3. Click **Test Data** to open the Test Data pane
4. If the script has unresolved references and variable names in its **CSV Data Set Config**, BlazeMeter now lists the missing files. Choose from the following options:
   - Click **Upload CSV File** to attach the missing test data in CSV format
   - Click **Suggest Data** to generate synthetic test data for the defined variable names
   - Click **Load Data Entity** to load existing shared test data from the workspace

For more information, see [CSV Data Set Config in the JMeter user manual](https://jmeter.apache.org/usermanual/component_reference.html#CSV_Data_Set_Config).

**Important**: Make sure to create and define all parameters that are referenced in your script before running the test.

### How many files can I add in a BlazeMeter test?

You can add any files you need to be used as part of your script during your test.

### What is the maximum file size?

Individual files up to 50MB can be uploaded. If a file is larger, please zip it. BlazeMeter will unzip it prior to script execution.

### Preview Test Data

Previewing your test data is helpful when you are combining data from multiple sources, or generating synthetic test data, so you can view values in context.

1. Open a Performance Test with test data attached
2. Verify that at least one data parameter is defined to be able to generate the data preview
3. Click **Test Data**, **Data Settings**. The Test Data Settings window opens and shows the data preview
   - Click **Upload CSV File** to attach the missing test data in CSV format
   - Click **Suggest Data** to generate synthetic test data for the defined variable names
   - Click **Load Data Entity** to load existing shared test data from the workspace

Make sure to create and define all parameters that are referenced in your script before running the test.

**File Limits:**
- You can add any files you need to be used as part of your script during your test
- Individual files up to 50MB can be uploaded. If a file is larger, please zip it. BlazeMeter will unzip it prior to script execution

### Preview Test Data

Previewing your test data is helpful when you are combining data from multiple sources, or generating synthetic test data, so you can view values in context:

1. Open a Performance Test with test data attached
2. Verify that at least one data parameter is defined to be able to generate the data preview
3. Click **Test Data**, **Data Settings**. The Test Data Settings window opens and shows the data preview

---

## Introduction to Performance Testing

Performance testing for websites and mobile applications is critical for every developer to deliver the best experience to end users.

**Use when**: Understanding performance testing fundamentals, learning about performance testing importance, or getting started with performance testing.

### What is Performance Testing?

Performance testing is a fairly general term that can be applied to many aspects of your website or application. However, they all aim to determine the usability, scalability and reliability of a piece of software.

Performance testing enables you to identify, and resolve, two main types of issues that are highly important for any modern application, whether mobile or web-based:

1. Length of load times (high response time issues)
2. Failures in loading certain features (increased failure rate under load)

These issues can be caused by various issues and performance testing enables you to determine the actual cause in order to resolve them and bring your application up-to-speed with potential uses cases.

### Importance Of Performance Testing

There are several reasons that you should consider performance testing your application. Some of those reasons are technical, but perhaps the most important is ensuring your web application, website, and server are all acting as expected under increased load.

Regular performance tests helps ensure your website performs at its highest level, resulting in better uptime, less maintenance, and greater user interactivity while on site.

Basic benefits of undergoing performance testing include:

- Increased customer satisfaction
- Better overall customer experiences
- Higher quality applications
- Reduced risk of system downtime
- Implementing performance patches before taking your product live
- Eliminating scalability issues
- Benchmarking tools for performance engineering teams

### Documentation References

For detailed information about introduction to performance testing, use the BlazeMeter MCP help tools:

**Introduction to Performance Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-planning-load-tests`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-planning-load-tests"]}`

---

## Functional Testing

Functional testing is a software testing technique that focuses on verifying that a software application's functions work as intended. It ensures that the application's features, user interfaces, APIs, and integrations perform correctly, meeting the specified requirements.

**Use when**: Understanding functional testing concepts, learning about functional testing types, or implementing functional testing in your testing strategy.

### Functional vs Non-Functional Requirements

Functional requirements are essential features of the product without which the system won't work. Non-functional requirements specify how the system should perform the functions, that is, they are the product characteristics that make it easy to use and ensure a better user experience. Even if these requirements aren't met, the system will still work.

### BlazeMeter Functional Testing Support

BlazeMeter supports a variety of testing features, including:

- **Scripted and Scriptless Testing** — BlazeMeter supports both scripted and scriptless testing approaches. With scripted testing, users can leverage popular scripting languages such as JMeter, Gatling, and Selenium to create custom test scenarios. On the other hand, the scriptless testing option enables testers and non-technical stakeholders to design tests through an intuitive graphical interface, streamlining the testing process.
- **Cross-Browser Testing** — BlazeMeter enables testers to validate the functionality of their web applications across different browsers and versions. This ensures a consistent user experience and helps identify any browser-specific issues that may impact the application's performance.
- **Parallel Execution** — Efficient testing is crucial for timely releases. BlazeMeter's functional testing capabilities support parallel execution, allowing multiple test scenarios to run simultaneously. This accelerates the testing process and provides rapid feedback to development teams.
- **Comprehensive Reporting** — Detailed and actionable insights are essential for effective testing. BlazeMeter provides comprehensive reports that highlight key performance indicators, identify bottlenecks, and offer insights into the application's functional behavior. These reports help you make informed decisions that can enhance application performance.
- **Integration with Continuous Integration (CI) Tools** — Seamless integration with popular CI tools such as Jenkins, Bamboo, and TeamCity enables teams to incorporate functional testing into their CI/CD pipelines. This ensures that every code change is thoroughly tested, promoting early detection and resolution of issues.

### Functional Testing Types

The following are sample use cases for functional testing types:

- Testing login features — Verification of login functionalities against valid and invalid inputs to ensure seamless operation.
- Transaction processing system — Assessment of the payment gateway's functionality within a transaction processing system, including user notification in case of a failed attempt.
- File uploading feature — Testing the file uploading feature to ensure it appropriately sends an error message if the file size exceeds the limit.

### Documentation References

For detailed information about functional testing, use the BlazeMeter MCP help tools:

**Functional Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-functional-tests`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-functional-tests"]}`

---

## Backend Testing

Performance testing includes both **Backend Testing** and **Functional Testing.** While some tests may be more pertinent to your particular needs, both testing methodologies can drastically optimize a website's performance.

**Use when**: Understanding backend testing concepts, learning about backend testing types, or implementing backend testing in your performance testing strategy.

### Backend vs Functional Testing

Backend testing relates to tasks like testing the code base for bugs and performance, testing the network capacity, and the architecture of an application.

Functional testing relates to tasks like responsiveness, browser layout and user experience.

When most testers in the industry refer to performance testing, they are referring to backend testing, and tweaking server performance to meet load needs.

### Backend Testing Goals

Breaking down the goals of performance testing helps to further categorize tests into three key components. During testing, performance testers hope to gain insight into website **functionality** (APIs), **performance** (server response times, and so on), and system **stability** while a server is under increased load. These tests focus on functionality, performance, and stability issues that may arise.

### Backend Test Types

Backend tests include:

- **Capacity Test** - Identifies how many concurrent users an application can handle before "breaking"
- **Load Test** - Measures the performance of an application under different levels of user activity, including peak load
- **Stress Test** - Measures a website's ability to handle incremental load, and then determines the point at which it will crash or fail due to high server load
- **Fail-over Test** - Measures a specific component of an application, or infrastructure, while executing a performance test
- **Endurance Test** - Determines whether a system can sustain continuous expected load over an extended period

### Documentation References

For detailed information about backend testing, use the BlazeMeter MCP help tools:

**Backend Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-backend-testing-the-specifics`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-backend-testing-the-specifics"]}`

---

## Building Your Script

Creating effective test scripts is a crucial aspect of performance testing with BlazeMeter. Whether you're using JMX (Java Sampler) or YAML scripts, following best practices can help to ensure accurate, reliable, and insightful performance testing results.

**Use when**: Creating test scripts in BlazeMeter, learning best practices for JMX and YAML scripts, or optimizing test scripts for better performance.

### Considerations for JMX Scripts

In JMeter:

- **Thread Group Configuration** - Set appropriate values for the number of threads, ramp-up time, and duration in the Thread Group. Consider the expected user load and concurrency.
- **Sampler Configuration** - Utilize the HTTP Request Sampler for web-based applications. Ensure accurate endpoint URLs, HTTP methods, and parameterization for dynamic values. Configure HTTP defaults, including protocol (HTTP/HTTPS), server name, and port.
- **Assertions** - Implement assertions to validate the expected behavior of your application. Check response data, status codes, or other relevant metrics.
- **Listeners** - Choose relevant listeners based on your testing goals. Aggregate Report, Summary Report, and View Results Tree are commonly used for result analysis.
- **Parameterization** - Parameterize your test data using CSV files or other data sources. This allows you to simulate real-world scenarios with diverse inputs.
- **Think Time** - Introduce think time between requests to simulate real user behavior accurately.
- **Cookies and Sessions** - Manage cookies and sessions appropriately, especially when dealing with authentication and user-specific scenarios.

### Considerations for YAML Scripts

- **Concurrency and Ramp-up** - Specify the concurrency and ramp-up time in the YAML script. Ensure it aligns with your testing goals and expected user load.
- **Scenario Definitions** - Define scenarios that represent different user journeys or use cases. Each scenario should contain relevant requests and actions.
- **HTTP Requests** - Clearly define HTTP requests within each scenario. Pay attention to the URL, method, and any necessary headers or parameters.
- **Variables** - Utilize variables for dynamic data, such as user credentials or session tokens. This ensures realistic test scenarios.
- **Assertions and Validations** - Include assertions within the YAML script to validate the correctness of responses. Ensure that the application behaves as expected under load.
- **Reusable Components** - Consider creating reusable components or modules for shared functionalities across scenarios. This enhances script maintainability.

### Documentation References

For detailed information about building your script, use the BlazeMeter MCP help tools:

**Building Your Script**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-build-your-script`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-build-your-script"]}`

---

## Define the Test Scope

Define your goals and establish clear boundaries and objectives for performance testing initiatives, delineating the specific functionalities, user scenarios, and performance metrics to be assessed.

**Use when**: Defining performance test goals, establishing test scope, or identifying key performance indicators for your tests.

### Define Your Goals

Typical goals of a load test, for web or mobile applications, are as follows:

- **Determine the user limit** - The user limit is the maximum number of simultaneous users that the application can support while remaining stable and providing reasonable response time to users as they use the application as intended. The user limit should be higher than the required number of concurrent users that the application must support when it is deployed.
- **Determine client-side degradation** - Can users get to the application in a timely manner? Are users able to use the application as intended within an acceptable time? How does the time of day, number of concurrent users, transactions and usage affect the performance of the application? Is the degradation "graceful?"
- **Determine server-side robustness** - Does the Web server crash under heavy load? Does the application server crash under heavy load? Do the other middle-tier servers crash or slow down under heavy load? Does the database server crash under heavy load?

### Know Your KPIs

Your KPIs (Key Performance Indicators) for web applications probably include the following:

**Response Metrics:**
- Average Response Time
- Error Rate
- Slowest (Peak) Response Time

**Volume Metrics:**
- Requests per Second
- Throughput - Kilobytes per Second
- Concurrent Users

### Documentation References

For detailed information about defining test scope, use the BlazeMeter MCP help tools:

**Define the Test Scope**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-define-test-scope`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-define-test-scope"]}`

---

## Planning Your Tests

Creating and running effective performance tests require proper planning. This section is dedicated to making sure that you are properly implementing these various elements into your performance testing process.

**Use when**: Planning performance tests, identifying stakeholders, quantifying performance acceptance criteria, or establishing performance testing processes.

### Things To Consider During Performance Test Planning

Below are the most important elements that need exploring while planning a performance test:

- Identify the types of performance tests required (stress / load / endurance) based on the business requirements provided.
- Ensure that you have up-to-date performance targets and any Service Level Agreements (SLAs) determined before starting the performance tests.
- Performance tests should not occur on production environment sites and servers except for acute or specific scenarios.
- Ensure that the performance test environment is an exact (or close to exact) replica of production environment.
- Base all performance tests on business targets, objectives, or potential issues that require validating - don't try to conduct tests without a clear objective or scope.
- Add "ThinkTime" and "pacing time" to scripts. They should replicate the production scenarios.
- Use co-relation points and data files to make scripts more dynamic and the test scenario more like production.
- The test environment should be manually tested to ensure that workflows execute properly with one user.
- Clear all logs from the controller and load generator machines after every 3-4 tests so that the test numbers are not affected in a negative manner.

### Stakeholders Involved And Their Roles

Here are some key stakeholders you should consider and the roles they play throughout the performance testing process:

- **Customers or "End Users"** - Help shape the requirements of the application through feature requests, reported bugs, or general feedback.
- **Business Analysts, Project Managers, And Product Owners** - Provide business level targets to test managers.
- **Performance Test Managers** - Play a key role in the service level agreement identification process and create the performance test strategy.
- **Performance Test Analysts** - Understand the performance test requirements and convert those into business scripts, work flow models & documents.
- **Performance Engineers And Developers** - Play a key role in performance tests. In the case of any performance issues, they debug the system and resolve performance issues.

### Documentation References

For detailed information about planning your tests, use the BlazeMeter MCP help tools:

**Planning Your Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-planning-your-tests`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-planning-your-tests"]}`

---

## Preparing For Your Load Test

This topic describes how to prepare for a load test using JMeter.

**Use when**: Preparing for a load test, debugging scripts, optimizing test scripts, or verifying test configuration.

### Preparation Steps

1. **Debug your script** - Make sure all files and plugins are there.
2. **Verify you have your APM installed and configured**.
3. **Use the latest JMeter stable version**.
4. **Optimize your script**:
   - Use JSR233 + Groovy + compilation key instead of BSF
   - Disable your script listeners
   - Run in Non-GUI mode
   - Optimize your Java configuration to meet your needs
   - Use CSV as your output format
   - Prefer using Regular Expression Extractor (RegEx) instead of XPath
5. **Use the ramp-up period wisely**.
6. **Check your distributed configuration and verify it works**.

### Documentation References

For detailed information about preparing for your load test, use the BlazeMeter MCP help tools:

**Preparing For Your Load Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-prepare-for-your-load-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-prepare-for-your-load-test"]}`

---

## Scripting Your Test

This section reviews, and helps to establish proper scripting processes for running effective performance tests.

**Use when**: Scripting performance tests, learning scripting best practices, managing dynamic content, or implementing text/image checkpoints.

### The Right Approach To Scripting

Scripting is a critical part of performance testing and is the actual activity that validates and creates the results of the test. Although different testing software uses different scripting languages and processes, the core concepts for scripting are the same.

Below are the most important parts of the scripting process to ensure that your performance tests are working:

- **Record & Playback** - Most performance testing tools, like JMeter, provide you with the ability to record a script and then playing back the same (after making any required changes to the script) test.
- **Modular scripting** - Adopt Modular scripting if the performance testing team prefers to create regression suite or a performance testing framework.
- **Transaction naming** - You can carry out transaction naming while recording the script or while updating the scripts. Add both transaction starts, and end points to the script, as these are essential to getting the response time for a page.
- **ThinkTime & Pacing Time** - ThinkTime is the time that a virtual user waits on a page (and thinks) before moving to the next page. Pacing time is the time lag between two consecutive sessions for a virtual user.
- **Text / Image check point** - Add Text checkpoints for each page, and select the text that needs checking so that that text is unique for that page.
- **Data management** - In order to make the test scenario closer to production scenarios, add data files to scripts at where data needs to be input by the end user.
- **Dynamic content management** - While recording the script, generate items like session IDs, time stamp values, etc. Replaying these values may cause the script replay to fail. This is due to the fact that for every session the server may demand a different session ID for that specific session. In such cases co-relation functions are useful.

### Scripting Best Practices

Additional critical scripting best practices should include consideration of the following items:

1. If you are using a tool that records and playback your script, then try adding transaction names and comments while recording the script.
2. Parameterize your script in order to create a test scenario as identical as possible to the production scenario.
3. For every web page, it's important to have text (and or) image check point.
4. ThinkTime is critical to have implemented for production like live user sessions.
5. Before any performance tests run, it's critical to ensure that you've cleared the application logs, web logs and database logs.
6. Monitor your servers during the test and note the time (in seconds if possible) for any abnormal observations.
7. If your application has a lot of AJAX requests and activities happening on the client side, it is good to test a single user and response time observed for the same in GUI mode.
8. Always keep an eye on the capacity of your load generators and don't over stress the load generators during the test.
9. It is common practice to have a separate test environment for performance test.
10. Use the 80-20 rule while designing scenarios: While designing scenarios, go for functionalities and transactions that execute 80 % of the time by end users and form only 20% of the system.

### Documentation References

For detailed information about scripting your test, use the BlazeMeter MCP help tools:

**Scripting Your Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-scripting-your-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-scripting-your-test"]}`

---

## More About Performance Testing

Understand important aspects of performance testing and industry technologies, including cloud testing, Agile workflows, and mobile application testing.

**Use when**: Understanding important aspects of performance testing, learning about cloud testing benefits, implementing performance testing in Agile workflows, or testing mobile applications.

### Performance Testing In The Cloud

Cloud technology has changed the way applications work and the expectations of users in terms of features such as real-time syncing. The key difference when running a performance test for the cloud is to try and test the application for its performance (usability, scalability and reliability) in a non functional test (performance test).

The user experience when an application is under load is studied in load - stress - performance test. However setting up the performance test infrastructure is a key activity before starting a test and includes a lot of factors:

- **Environment usage planning** is extremely important since the resources are costly. If not planned well, mismanagement may lead to inappropriate planning and consequently insufficient usage of infrastructure resources
- Most of the times the servers are managed by one team and utilized by another. With increasing complexity in infrastructure, teams are required to depend on each other causing delays in the core work of software development
- Software that needs to be installed on the servers can be expensive
- Along with the financial investment, infrastructure management requires a significant amount of time investment with activities like procurement of servers, software installation, and so on

Due to the factors listed above, setting up a performance testing environment can be very costly (optimization is the key). It therefore makes sense to outsource this activity. Running the test infrastructure through the cloud can provide the following benefits:

- **Focus on core performance testing activity**
- **Pay-per-use**
- **Virtual services**: You can easily set up test instances using virtual services at minimal cost

### BlazeMeter: Load - Performance - Stress Testing on Cloud

BlazeMeter's Load Testing Platform for Developers is designed for professional use, is equipped with a self-service, on-demand platform and advanced scripting capabilities leveraging [JMeter](http://jakarta.apache.org/jmeter/) and [Selenium](http://seleniumhq.org/) [(WebDriver)](http://blazemeter.com/blog/jmeter-webdriver-sampler). BlazeMeter can run multiple load tests that easily simulate the load of 2,000,000 and more globally distributed virtual users from both the public cloud or [inside the corporate firewall](skill-blazemeter-private-locations://references/introduction.md), enabling you to quickly locate and fix performance bottlenecks.

You can create proprietary test scripts and load scenarios using a graphical web environment. BlazeMeter offers web-based test management, archiving, repository, cloud-based monitoring, rich scripting language, and supports HTTP/S, web-services, XML, TCP, SQL, Login (Flash, images, streaming) and more.

BlazeMeter enables you to write load test-scripts using JMeter and user-experience test-scripts using Selenium. BlazeMeter generates a load based on the JMeter script. The Selenium script is used during the load to automate the launch of real browsers to measure the real end-user experience.

The load and monitoring uses a pre-configured distributed load testing environment. The environment is ready to use and available at all times.

If you are not familiar with Selenium and do not wish to create a Selenium test-script, the system can generate one for your programmatically based on landing pages you provide (Using our [Google Chrome Extension](skill-blazemeter-recorders://references/chrome-extension.md)). If you want the same for your JMeter script, BlazeMeter generates JMeter scripts automatically.

With BlazeMeter, all you need is to write the test-scripts, choose the amount of load-engines and run the test. The system takes care of the everything else. Load engines are pre-configured and available at your disposal. Detailed graphical reports are generated during the load.

### Performance Testing In Agile

Agile development is a software creation methodology that encourages incremental or iterative development, making an application better with each update, over time. Performance testing is still a necessary component; however, the workflow is different from traditional corporate environments.

Here are a few tactics designed to help you embrace performance testing within an Agile workflow:

- **Team work**: Agile is about working in teams, but traditionally performance testers were independent contributors. Today, these testers now work in teams. Not only do they have to find performance bugs, but they also have to collaborate with developers and performance engineers in resolving the issues
- **Start early**: Unlike in the past, performance testing now starts early in the development process, and not at the end of it
- **Iterations**: As iterative development happens, performance testing must be undertaken at each stage of the process. It's easier to make adjustments to new bugs when they arise than at the end of an applications development cycle
- **Over-communicate**: Agile requires exhaustive communication and sometimes over-communication. This helps reduce lost time, and eliminates time waste

Here are some suggested steps to perform in Agile performance testing:

- **Define your goal**: Understand the goal and vision of the project and define a high level overview
- **Define business targets**: Define business targets within the application (for example, "a response time of less than 1 sec for every page")
- **Set performance SLAs**: Performance test managers collaborate with business and technical stakeholders to set the performance targets or SLAs
- **Identify the tests and plan for specific scenarios**: Based on the goals and targets, identify proper tests, and create proper business scenarios to emulate
- **Strategy document**: Create a basic strategy document/wiki page that has information about all key test elements and share it with appropriate stakeholders
- **Test environment**: Environment creation and documentation both happen in parallel. Create a testing infrastructure (tool and other setup) to meet testing demands. Replicate production environments
- **Tasks**: Identify tasks and delegate jobs where appropriate
- **Scripting & test execution**: Create scripts and execute tests based on the scenarios, as identified in the test planning phase
- **Analyze results**: Analyze results and add them to the test result reports. Document bugs and add them to bug tracking tools. Publish results, and contact stakeholders
- **Re-testing**: After completing these changes, re-testing should occur, and notes should written about possible app updates

### Performance Testing And Mobile Applications

To deal with the increasing demand for highly functioning mobile applications, developers now also need to ensure their mobile application with the same robustness and performance that consumers demanded on other computing devices.

However, the mobile frontier has also brought with it new challenges. Listed below are some of the more important things we need to consider:

- Network availability at the place where the device is in use plays a very important role and there is no way to control this environment
- Mobile phones make more requests (thus create more load) on the servers compared to desktop devices
- There are many types of operating systems, and we need to make the app compatible with each
- Innovations happen quickly in the mobility space, we need to keep up
- Executing a performance test and simulating the production behavior of mobile users is essential, but difficult since users keep moving from one location to another while using the app. Their network capabilities change quickly from one place to another

### Performance Testing Mobile Apps

- Try to bring the test as close to the production environment as possible
- Don't worry about the factors that are beyond control
- Use network simulators while running the tests, and through these simulators, try decreasing and increasing the available bandwidth to reproduce real-life environments and variables
- Perform tests that replicate clients getting disconnect from a network. If something like this happens, try to resolve the issue and retest to avoid data loss. Sharing key details in the user sessions helps in such situations
- While using simulators (during your load tests), try performing the same functionalities using a mobile device and check for the app performance in manual mode
- While simulating the test, focus only on the key end users (operating systems & devices) that cover 70-80% of your business scenarios and don't go for exceptions (not necessary to go for all devices), unless the exceptions are too critical. This will help you save on your resources

---

## Checklist

Use a comprehensive checklist for optimizing application performance, including test scope definition, script building, preparation, and report analysis.

**Use when**: Using a comprehensive checklist for optimizing application performance or defining test scope, building scripts, preparing tests, and analyzing reports.

### Defining the Test Scope

- Know your scenario and put it into words/flowchart
- Define your goals
- Get the amount of your daily users
- Understand your application spike hours
- Know your KPIs

### Building Your Script

- Choose the right Thread group for your scenario
- Use Default HTTP request to control your HTTPs requests (Server/IP, protocol, implementation, and so on)
- Verify you added a cookie manager
- Check you fetch every dynamic values (for example, `form_build_id`) and use a RegEx and a variable for it
- User Define Variables VS User parameters preprocess - know which to use and when
- Use assertion when you can't count on the HTTP response code (for example, `login`)
- Use the header manager to control your requests headers (user-agent) and change the values if needed

### Preparation Toward Your Load Test

- Debug your script, make sure all files and plugins are there
- Verify you have your APM installed and configured
- Use the latest JMeter stable version
- Optimize your script:
  - Use JSR233 + Groovy + compilation key instead of BSF
  - Disable your script listeners
  - Run in non-GUI mode
  - Optimize your Java configuration to meet your needs
  - Use CSV as your output format
  - Prefer using Regular extractor instead of XPath
  - Use the ramp-up wisely
  - Check your distributed configuration and verify it works

### What to Notice in Your Load Report

- The right way to scale up ([look here](http://blazemeter.com/blog/how-run-load-test-50k-concurrent-users))
- Identify your bottlenecks and errors

---

## Testing Process

Follow the complete performance testing process, including targets and requirements, test environment setup, test strategy, scripting, test data, workflow models, environment checks, execution, and results analysis.

**Use when**: Following the complete performance testing process or setting up targets and requirements, test environment, test strategy, scripting, test data, workflow models, and results analysis.

### Key Activities In Performance Testing

It's important to focus on some of the key activities that you and your team should be performing throughout the various stages of this process. Here are the most important activities for each part of the process:

### Targets and Requirements

- All business requirements, discussed with sponsors and product owners
- Business targets converted into a technical Service Level Agreement(s)
- Discuss Service Level Agreements with the technical team (feasibility, and correctness)
- Discuss performance test targets with technical and business stakeholder(s)
- Set Service Level Agreements

### Test Environment

There are two parts in this phase of the performance testing process:

- **Part 1**: Deploy the application on a separate performance testing environment. (Note: creating an exact replica of production environment is optimal while designing a performance test.)
- **Part 2**: Performance test infrastructure: Procure performance testing software licenses (if required). Setup Software infrastructure based on business requirements. Make the software available for the entire testing team

### Test Strategy

This series of tests address business targets:

- Conduct, and finalize, various work load models for each different type of tests
- Recreate, and run tests from different geographic locations where potential clients may use the application

### Scripting

- Write, or record, any needed testing scripts and update them where appropriate
- Add think time and pacing time values
- Add text (and image) checkpoints to the script
- Define correlation points (for dynamic content)

### Test Data

- Add production data to scripts, and make them more dynamic
- Add appropriate date and time functions

### Workflow Model

- Based on test design, create a workflow model using a scenario generator of different tools

### Environment Check

- Create an environment test scenario based on the final production infrastructure your application operates in (or will operate in)
- Manually execute the test environment before the performance test
- Clear any logs created in the environment before the test runs

### Test Execution

- Execute the test
- Monitor the application, database and web servers while the test executes

### Results Analysis

- Collate, and study client side counters
- Copy test results from analysis tools and compare with previous tests
- Note, and document, all necessary improvements to made in the application
- Identify all application issues, and show reports to performance engineering team

### Results Report

- Add all key items from the last phase into the report
- Add key client side counters to report
- Add error details to the report, along with necessary observations

---

## Documentation References

For detailed information about advanced performance testing features, use the BlazeMeter MCP help tools:

**Advanced Features**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `performance-create-test` (create performance test)
  - `performance-ai-log-analysis-report` (AI Log Analysis)
  - `performance-add-users-dynamically` (add users)
  - `performance-apm-integration` (APM)
  - `performance-create-browser-test` (browser test)
  - `performance-browser-tests-best-practices.htm` (browser test best practices)
  - `performance-convert-browser-perf-test-to-func-test.htm` (convert browser to functional)
  - `performance-create-k6-test.htm` (k6 test)
  - `performance-jmeter-dsl` (JMeter DSL)
  - `performance-create-jmeter-test` (JMeter test)
  - `performance-create-multi-test` (multi-test)
  - `performance-create-url-api-test` (URL/API test)
  - `performance-dedicated-ips` (dedicated IPs)
  - `performance-dns-override` (DNS override)
  - `performance-eux-monitoring` (EUX)
  - `performance-failure-criteria` (failure criteria)
  - `performance-mainframe-testing` (mainframe)
  - `performance-network-emulation` (network emulation)
  - `performance-shared-folders` (shared folders)
  - `performance-use-test-data-in-testing` (test data)
  - `performance-more-about` (more about)
  - `performance-check-list` (checklist)
  - `performance-testing-process` (testing process)
  - `performance-planning-load-tests` (introduction to performance testing)
  - `performance-functional-tests` (functional testing)
  - `performance-backend-testing-the-specifics` (backend testing)
  - `performance-build-your-script` (building your script)
  - `performance-define-test-scope` (define test scope)
  - `performance-planning-your-tests` (planning your tests)
  - `performance-prepare-for-your-load-test` (preparing for load test)
  - `performance-scripting-your-test` (scripting your test)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-ai-log-analysis-report", "performance-add-users-dynamically", "performance-apm-integration", "performance-create-browser-test", "performance-browser-tests-best-practices.htm", "performance-convert-browser-perf-test-to-func-test.htm", "performance-create-k6-test.htm", "performance-jmeter-dsl", "performance-create-jmeter-test", "performance-create-multi-test", "performance-create-url-api-test", "performance-dedicated-ips", "performance-dns-override", "performance-eux-monitoring", "performance-failure-criteria", "performance-mainframe-testing", "performance-network-emulation", "performance-shared-folders", "performance-use-test-data-in-testing", "performance-more-about", "performance-check-list", "performance-testing-process", "performance-planning-load-tests", "performance-functional-tests", "performance-backend-testing-the-specifics", "performance-build-your-script", "performance-define-test-scope", "performance-planning-your-tests", "performance-prepare-for-your-load-test", "performance-scripting-your-test"]}`

