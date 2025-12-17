# Scenarios

## Scenario Definition

The Scenario Definition section contains all files needed by your test. It also controls which test executor to use (JMeter, Gatling, Selenium, and so on.) and which file to begin the test with.

**Use when**: Configuring scenario definitions for performance tests, uploading files, selecting test types, choosing starting scripts, or distributing CSV files across engines.

### Upload or Include Files

Follow these steps:

1. In the **Performance** tab, click **Create Test**
2. Click **Performance Test**
3. Click the Upload Script icon to upload files or click **Shared Folder** to include files from Shared Folders. In the **Configuration** tab, a **Scenario Definition** section opens
4. (Optional) To add additional files, hover over the **+** icon on the right and select **Browse Files**
5. (Optional) To add or remove shared folders, hover over the **+** icon on the right and select **Shared Folders**

**Important Notes:**
- If your main test file shows **invalid**, or with a **missing scenario**, double-check your script and re-upload
- If a test file other than your main file (for example, an additional JMX test fragments), is marked invalid, you can ignore the warning. It only means there may be a problem if that file was designated as your main test script

For more information about uploading files and including files from Shared Folders, see [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md) and [Shared Folders](https://help.blazemeter.com/docs/guide/performance-shared-folders.html).

---

## Uploading Files

Sometimes multiple files are required for the successful execution of a performance test. With BlazeMeter, we handle the distribution of various types of files to all of a test's engines for you.

For a more advanced solution for uploading files to tests, see [Shared Folders](https://help.blazemeter.com/docs/guide/performance-shared-folders.html).

**Use when**: Uploading files to performance test configurations, understanding file restrictions, or managing file distribution to test engines.

### Uploading Files to a Test Configuration

You can upload files while configuring your test by clicking the **Upload Script** button, or you can simply drag and drop files to this location.

### File Name Restrictions

- File names should include only alphanumeric characters, underscores, and/or hyphens: [0-9],[aA-zZ],[_-]
- File names should always include an extension
- File names are treated as case-sensitive, so ensure all references to the file are consistent (if a file is named *File.csv*, then referring to *file.csv* in a script will result in an error)
- **File Names CANNOT include spaces**

**Examples:**
- A file named *my_file_no_4.csv* is acceptable
- A file name: *m$ file&* is not acceptable (note the space between "$" and "f"). Also, **$** and **&** characters are not supported

### File Content Restrictions

BlazeMeter cannot read files containing non-ASCII characters. Please ensure non-ASCII are removed before uploading and starting the test. ZIP files (but not the files they contain) and JAR files are exceptions to this rule.

### File Size Limit

BlazeMeter has a file size limit of 50 MB **per** file that can be uploaded. You can upload multiple files of up to 50mb in size to your test, as needed.

50mb is a hard limit. BlazeMeter does not provide any options for uploading larger files. For Performance tests however, if you are using private cloud locations, you may upload larger files to your own private locations and then reference those files in the script that you upload to your BlazeMeter test. In the "CSV Data Set Config", reference the filename as an absolute path, such as "/tmp/my-large-dataset.csv".

### Impact on Start Time

All files are downloaded to engines before a test starts, which may delay how quickly the test starts. Therefore avoid including large files that are not needed and be aware that:

- All files are downloaded to each of the test engines each time a test starts
- A test will not start until all of the files are downloaded

### Manually Select Test Type

BlazeMeter uses the file type to set the **Test type** (JMeter for a JMX file, Gatling for a Scala file, and so on).

Some testing tools use the same type of files, so you may need to set the **Test type** manually. Expand the drop-down list and select a test type.

### Manually Select Script to Start Test

The first file with an extension that matches a supported test type is selected as the primary script. The test starts with this script.

- The starting test is marked with a green arrow icon
- If you upload more than one script file, the additional files have an open circle icon
- To select a different script as a starting test, click the open circle icon. The icon changes to the arrow icon and the **Start test with** field is updated

### Distribute CSV Data to Engines: Split CSV

To split your CSV into unique files for each server, select the **Split CSV files with a unique subset per engine** checkbox in the Scenario Definition.

This ensures that each engine receives a unique subset of CSV data, preventing data conflicts and ensuring proper test data distribution across multiple engines.

For more information about using test data from a CSV file in your test, see [Using Test Data in JMeter Performance Tests](skill-blazemeter-performance-testing://references/advanced-features.md) and [How to Split or Distribute CSV Files in Performance Tests](skill-blazemeter-performance-testing://references/scenarios.md).

---

## Duplicate, Delete, or Move a Test

For any test that you create, you have the option to duplicate, delete or move the test to another project.

**Use when**: Duplicating, deleting, or moving performance tests to another project.

### Duplicate a Test

**Prerequisite**: You created a performance test. For more information, see [Creating a Performance Test](skill-blazemeter-performance-testing://references/advanced-features.md).

**Steps:**

1. Navigate to the **Performance** tab
2. Select a test from the **Tests** drop-down list or create a new test
3. Click the **Actions** menu for the test
4. Click **Duplicate Test**. A **Successfully cloned test** confirmation message appears. A new test is created and has the same name as your original test with '**-Copy**'
5. (Optional) Click the pen icon to rename the test

### Delete a Test

**Steps:**

1. Navigate to the **Performance** tab
2. Select a test from the **Tests** drop-down list or create a new test
3. Click the **Actions** menu for the test
4. Click **Delete Test**
5. A **Successfully deleted test** confirmation message appears

### Move a Test

**Prerequisite**: You created a performance test. For more information, see [Creating a Performance Test](skill-blazemeter-performance-testing://references/advanced-features.md).

**Steps:**

1. Navigate to the **Performance** tab
2. Select a test from the **Tests** drop-down list or create a new test
3. Click the **Actions** menu for the test. A new **Workspace Projects** window opens
4. Hover over the project you want to move your test to and click **Move Here**

**Important Notes:**
- Multiple projects have to be defined for the Move Test option to be available
- For Multi-Test tests, an additional **Data Files** option will be included in the **Actions** menu list

---

## Run Test

Execute performance tests in BlazeMeter, including first-time runs, repeated runs, boot screen monitoring, detailed engine status, and system log viewing.

**Use when**: Executing performance tests in BlazeMeter, monitoring boot screen, engine status, and system logs during test execution, or rerunning tests from reports.

### Overview

You [created your performance test](skill-blazemeter-performance-testing://references/scenarios.md) and you are ready to run the test. From the test configuration view, you can run the test by:

- Clicking the **Run Test** button to run a full [Performance Test](skill-blazemeter-performance-testing://references/scenarios.md)
- Clicking the **Debug Test** button to run a low-scale [Debug Test](skill-blazemeter-performance-testing://references/troubleshooting.md) with enhanced logging

### Run a Performance Test for the First Time

Follow these steps:

1. In **Performance** tab, click **Tests**
2. Select the test from the list of recently active tests. A **Launch Test** window opens
3. Review the configuration and click **Launch Servers** to start the test
4. Select the email options for sending test results
5. (Optional): Check the **Run test in the background** box if you do not want to see the startup status view. You will be returned to your previous view and the test runs in the background
6. (Optional): If two or more locations are configured, you will also see a **Synchronized Start** checkbox. This ensures that all servers are up before starting the test. Select this option if you have a concern that some servers or locations are significantly slower than others and you wish to synchronize them

### Run a Performance Test Repeatedly

Follow these steps:

1. In **Performance** tab, click **Tests**.
2. Click **Show all tests**. A list of all tests opens as a column on the left. Only tests that have been previously run show in the list of recently active tests.
3. Click the play button next to the test that you want to run. A **Launch Test** window opens.
4. Review the configuration and click **Launch Servers** to start the test.
5. Select the email options for sending test results.
6. (Optional): Check the **Run test in the background** box if you do not want to see the startup status view. You will be returned to your previous view and the test runs in the background. Next to the **Reports** drop-down list, you can see a number of currently running tests.

To abort the test, click the **Abort Test** button in the top right corner. For more information, see [Stopping a Test](skill-blazemeter-performance-testing://references/scenarios.md).

### Review the Boot Screen Summary

If you did not check the **Run test in the background** option, you will see the boot status of the engine(s) of your test:

- **Pending**: Indicates the percentage of engines are pending allocation on our end.
- **Booting**: Indicates the percentage of engines that have been allocated and are booting up.
- **Downloading**: Indicates the percentage of engines that have started downloading all the test assets.
- **Ready**: Indicates the percentage of engines that are ready to start.

If you want to get more detailed information on your engines and their statuses, click the **Show Engines** button.

### Review the Detailed Boot Status Screen

When you click the **Show Engines** button, you will see a detailed screen with a more detailed breakdown of the engines running:

- Name of the test with the link to the test configuration for this test run.
- The amount of time that has occurred since the start of the test run.
- **Hide Engines**: Returns the screen to the summary view described [above](skill-blazemeter-performance-testing://references/scenarios.md).
- **Force Start**: Force starts the test without waiting for the rest of the engines to be in **Ready** status.
- **Start Test**: Starts the test. Appears when all engines are in **Ready** status.
- **Abort Test**: Terminates the test, stopping all engines immediately upon confirmation.
- **Table refresh is on**: Set the refresh rate of the table.
- **Scenario** drop-down list: Filter the engines by scenario. The **Show only added scenarios** option shows only the scenarios you added to a test using [this feature](skill-blazemeter-performance-testing://references/advanced-features.md).
- **Location** drop-down list: Filter the engines by location.
- **Cloud Provider** drop-down list: Filter the engines by the cloud provider (AWS, Google Cloud, Azure, and [Private Locations](skill-blazemeter-private-locations://references/management.md)).
- **Status** drop-down list: Filter the engines by [status](skill-blazemeter-performance-testing://references/scenarios.md). The **Show only not Ready** option selects all options except for the Ready status. You will only see engines that are NOT in **Ready** status.
- **Search by Session ID**: Enter a session ID of one of the running engines to focus on just that engine.
- **IP**: Filter the engines that use dedicated IPs or all engines.
- **Show log**: Opens the system log for that specific machine. For more information, see [System Log](skill-blazemeter-performance-testing://references/scenarios.md).

For each engine in your test, you can see the following information:

- Scenario - The scenario this engine is running.
- Location - The cloud or private location where this engine is running.
- Cloud Provider - The name of the cloud provider where this engine is running.
- Script - The script this engine is starting with.
- IP - The IP address of this engine.
- Status - The status the engine is currently in.
- Session Id - The [sessionId](skill-blazemeter-api-reference://references/identifiers.md) for this engine.

### System Log

To see the system log, click the boxes in the bottom right corner.

To be able to see the boxes, you must select location first.

**System Log checkboxes:**
- **System** - Ensures system messages are included in the log.
- **User** - Shows the user logs form the system log.
- **Autoscroll** - Ensures the window automatically scrolls as new lines fill it up.
- **New Messages Alert** - Provides notifications for every new action.

You can complete other tasks while the test is running in the background, such as viewing reports or configuring and running other tests.

You can wait a few minutes until the test ends or you can stop the test yourself. If you need to manually stop the test for any reason, see [Stopping a Test](skill-blazemeter-performance-testing://references/scenarios.md).

### Rerun Tests from Reports

You can re-execute tests from the report header area. This functionality is particularly useful for conducting iterative testing, verifying fixes, or comparing performance metrics over time.

Rerunning performance tests in BlazeMeter helps you continuously assess and enhance the performance of your applications. During the rerun, you can monitor the progress of the test execution in real-time through the BlazeMeter user interface. You can track metrics such as response times, error rates, and system resource utilization to gauge the performance of the application under test.

After the rerun completes, you can analyze the test results to identify any performance issues, trends, or improvements compared to previous runs.

Based on the insights gained from the rerun, you can choose to iterate on your test scenarios, make adjustments to the application code, or implement performance optimizations before initiating subsequent reruns.

**Steps:**

1. From the **Performance** tab, click **Reports** and select the required test from the list of available tests.
2. (Optional) Before rerunning the test, modify test parameters such as number of users, duration, location, or scenario configuration to suit your testing requirements.
3. When satisfied with the test setup, click **Run Again** to initiate the rerun process.

---

## Stop Test

You can stop a test during the starting phase or while the test is running.

**Use when**: Stopping performance tests during startup or execution or choosing between graceful shutdown and immediate termination with artifact handling.

### Stop a Test During a Startup Phase

Follow these steps:

1. While the test is starting up, click the **Abort Test** button on the right. A **Stopping Test** window opens.
2. Click **Terminate servers**.

The test is terminated.

Tests that are stopped by the **Abort Test** command are assigned Aborted status in the **History**, **Recent Test Runs**, and **Report** pages.

### Stop a Test While It Runs

Follow these steps:

1. In **Performance** tab, click **Tests**.
2. Select the running test that you want to stop.
3. Click the stop button next to the test name.
4. Select one of the options:
   - **Graceful Shutdown**: Sends a signal to close the test, archive test and log files, then generate an *artifacts.zip* archive.
   - **Terminate Servers**: Terminates all servers immediately. This will result in the loss of all test and log files (except for the ones you originally uploaded). No *artifacts.zip* archive will be generated. This should be a last resort, since without any log files, it will be impossible to identify what may have caused a problem.

Or, you can click the "x" icon in the upper-right corner of the window to cancel and continue the test without interruption.

If you manually terminated a test because it hung indefinitely, for more information, see our knowledge base article [tests that fail to start](skill-blazemeter-performance-testing://references/troubleshooting.md).

---

## Configure Ultimate Thread Group Scenario

Configure Ultimate Thread Group and Concurrency Thread Group scenarios in BlazeMeter performance tests. A thread group represents a set of threads and provides a mechanism for collecting multiple threads and executing them all at once. When using a standard Thread Group, BlazeMeter overrides the Thread Group configuration of Threads, Iterations, Ramp-up and Duration. That is not the case when using an **Ultimate** or **Concurrency** Thread Group.

**Use when**: Configuring Ultimate Thread Group or Concurrency Thread Group scenarios in BlazeMeter performance tests, implementing complex load patterns, or creating custom load profiles with specific ramp-up and hold periods.

### Configure an Ultimate Thread Group Scenario

Upload your JMeter script to the test. If the script contains an Ultimate Thread Group Scenario, **Load Configuration** is automatically disabled.

### Configure Engines in a Multiple Engines Scenario

If you run a multiple engines test, you must adjust the **Threads** values in your **Ultimate** or **Concurrency** Thread Group.

**Example:**
You are running a multiple engines test with 2000 Concurrent Users using *five* load engines. Then you need to adjust the **Threads** values to *one fifth* of their current values. Set the Ultimate or Concurrency Thread Group to load up to 400 threads. Otherwise, each engine runs 2000 threads. It would result in the crash of the engines or massive overload on your app server side.

Follow these steps:

1. Click the current configured number of engines. A pop-up window shows
2. Configure the desired number of engines
3. Click anywhere outside of the pop-up window. The number of engines configured is updated

---

## CSV Split Distribute Engines

Depending on your Performance test scenario, you may want to run a multi-engines test with a single CSV file, or set up a separate CSV file for each JMeter engine.

**Use when**: Splitting or distributing CSV files across multiple engines in performance tests, ensuring unique data subsets per engine, or setting up separate CSV files for each JMeter engine.

### Run a Multi-Engines Test With a Single CSV File

If your test runs across multiple engines, you likely do not want two engines to use the same row of data. For example, you don't want to execute the registration test for the same test user twice. If you wish to run a multi-engine test with a single CSV file for all engines without using duplicate values, let BlazeMeter split the CSV file.

To split your CSV data into unique subsets for each engine, select the **Split CSV files with a unique subset per engine** checkbox in the Scenario Definition.

For example: You run a 1000-concurrent-users test, on 5 engines. You have uploaded a CSV file containing 1000 unique user names to simulate a registration scenario. Enable the '**Split CSV files**' checkbox, and when the test is initiating, the CSV file will be split 5 ways and each unique subset will be directed to a different engine. Line one will go to engine one, line two to engine two, line six again to engine one, line seven to engine two, and so on.

Note that Split CSV Files will not preserve the CSV header across engines. A best practice is to always omit the header row in the CSV file and to declare variable names in the [CSV Data Set Config](skill-blazemeter-performance-testing://references/advanced-features.md) instead. This ensures that you can always find where variables are set by searching your JMX files.

### Run a 'Multi Test' Simultaneously With a Single CSV File

A Multi Test is a feature which enables you to run several tests simultaneously. For more information regarding the Multi Test, see [Creating a Multi-Test](skill-blazemeter-performance-testing://references/scenarios.md).

If you wish to use one **CSV Data Set Config** for the entire Multi Test (unique data sets per engine, per test) then click **Data Files** and upload the CSV file when prompted. You will then be presented with a choice whether to split the CSV or not.

### How to Set up a Separate CSV File for Each JMeter Engine

If you want to use multiple JMeter engines with a different CSV file per JMeter engine, upload a different file for each JMeter engine and point to a variable to differentiate between each file.

Each JMeter engine uses a distinct variable TAURUS_SESSIONS_INDEX. The values for this variable start from 1 for the JMeter engines.

Each JMeter engine uses a distinct parameter `${__P(InstanceID)}`. The InstanceID values start from 1 for JMeter engines.

#### Example Scenario

In this scenario, you are using two JMeter engines. You upload two test data files named file1.csv and file2.csv.

#### Taurus Example

In the Taurus script's CSV Filename field, you specify: file${__env(TAURUS_SESSIONS_INDEX)}.csv.

Now, the first JMeter engine will read file1.csv. The second will read file2.csv. And so on.

#### JMX Example

In the JMX script's **CSV Data Set Config** section, enter the following in the CSV **Filename** field: `file${__P(InstanceID)}.csv`.

This way, the first JMeter engine will read file1.csv. The second will read file2.csv. And so on.

---

## Schedule Test

This page describes how to manage scheduled tests via the BlazeMeter UI. If you wish to manage scheduled tests via the API instead, see our [Test Scheduler](https://help.blazemeter.com/apidocs/performance/test_scheduler.htm) documentation. This page uses Performance tests as examples, but the same procedure also applies to Functional tests.

**Use when**: Scheduling performance tests to run at specific times or configuring recurring schedules and automated execution.

### Scheduling a Performance Test via GUI

Follow these steps:

1. On the **Performance** tab, click **Tests**.
2. Open a test.
3. In the **Schedule** section, click **Add**.
4. Select the required frequency:
   - **Weekly**: The test will run each week on the days selected. If the checkbox **Mon-Fri** is marked, the test will run daily Monday through Friday. Multiple checkboxes can be selected.
   - **Monthly**: The test will run on a specific day of the month according to selection. Multiple days can be selected.

For both **Weekly** and **Monthly** options, you can configure the run time of the test. Click the time box to the right of the frequency bar:

BlazeMeter default time zone is UTC+0. When using the **On Time** selector, convert the defined time from your local time zone to UTC+0.

**Advanced**: Enter your own CRON expression.

BlazeMeter default time zone is UTC+0. When using **CRON** as the frequency type, convert the defined time from your local time zone to UTC+0.

**Explanation of the CRON representation:**
```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │ 7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * command to execute
```

**Example**: If we use "30 10 * 2 1", the test will run at 10:30AM UTC+0, on each Monday of February.

Once you enter a crontab expression, the scheduler will automatically validate your expression, then repeat the expression in plain terms to verify that your expression has created the result you intended. Take care not to accidentally set the interval too small. Use the scheduler validation below your expression to verify your schedule. For example, you would not want to schedule a test to run every second, or every five minutes.

**Note**: Whereas the **On Time** option is expressed in UTC+0, the **Your next 3 tests** verification message will display in the time zone of your choice, matching whatever the value of your [time zone override](skill-blazemeter-administration://references/workspaces-projects.md) is (if the override is enabled).

A bonus feature to these three options above is that any selection made under one option carries over to the next during setup. For example, if you select **Weekly**, then select **Mon**, at **2:00am**, then switch from **Weekly** to **Advanced**, the crontab expression will automatically populate with your previous selection, expressed as:
```
0 2 * * 1
```

The reverse is also true, to a point: the crontab expression entered under **Advanced** will carry over to the UI selections in either **Weekly** or **Monthly**, if it is a basic enough expression to translate.

### View Scheduled Performance Tests

To view the list of scheduled tests, open a test. Any scheduled test is listed on the left panel.

### Disable or Enable a Scheduled Performance Test

Follow these steps:

1. In the **Performance** tab, click **Tests**.
2. Open a test. Scheduled tests are listed on the left panel.
3. In the **Schedule** section, toggle the slider on or off to enable or disable the schedule.

### Delete a Scheduled Performance Test

Follow these steps:

1. In **Performance** tab, click **Tests**.
2. Open a test. Scheduled tests are listed on the left panel.
3. In the **Schedule** section, hover over the test that you want to delete. The delete icon appears.
4. Click the delete icon.

Existing schedules cannot be edited. To modify a schedule, delete the schedule and create a new one.

### Review All Scheduled Performance Tests

Follow these steps:

1. Click the **Settings** icon in the top right corner.
2. In the left column, expand the **Workspace** section.
3. Click **Scheduled Tests**.

You can see all schedules assigned for all tests within the selected workspace. You can enable, disable, or delete a schedule from this view without having to navigate to the test itself.

To enable or disable, use the toggle icon. To delete a test, hover over the test and the delete icon appears.

This view only shows the schedules for tests belonging to the currently selected workspace. To see tests from other workspaces, use the **WORKSPACE** drop-down menu.

---

## Create JMeter Test

[Apache JMeter](https://www.blazemeter.com/solutions/jmeter?utm_source=knowledgebase&utm_medium=kb&utm_campaign=creating-a-jmeter-test) is an open source load testing tool that enables you to execute performance tests on your app or website. To run a load test, create a script that will detail the steps of your testing scenario and then run it. You can run your JMeter script locally on JMeter, in the Cloud, or from behind a firewall on BlazeMeter.

**Use when**: Creating JMeter performance tests, uploading JMX scripts and test assets, calibrating tests, or running JMeter tests in BlazeMeter.

### Step 1: Write and Test Your Script in JMeter

You can create your script manually in JMeter or automatically by recording your scenario in:

- [BlazeMeter Chrome Extension](skill-blazemeter-recorders://references/chrome-extension.md)
- [BlazeMeter Proxy Recorder](skill-blazemeter-recorders://references/proxy-recorder.md)
- Apache JMeter HTTP(S) Test Script Recorder

For additional guidance on how to create and test your script in JMeter, see Step 1 and Step 2 in the [Calibrating a BlazeMeter test](skill-blazemeter-performance-testing://references/jmeter-configuration.md) guide.

### Step 2: Upload Your JMX and Test Assets

Follow these steps:

1. In the main menu, click the **Performance** tab.
2. Click **Create Test**.
3. Select a project.
4. Click **Performance Test**.
5. Click **+** to upload your JMX script and any additional test files, such as CSV or JAR files, or drag the files over the **Upload Script** box.

**Important Notes:**
- All the files in your account are downloaded to the remote servers at the beginning of each test.
- Files from the original test configuration may be updated or deleted at any time. Doing so will not impact a test while it's running.

You created a Scenario Definition. For more information, including what to do if your file fails validation, see [Scenario Definition](skill-blazemeter-performance-testing://references/scenarios.md) and [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md).

### Step 3: Calibrate Your Test

Before running your test at load, you must calibrate your test according to the [Calibrating a BlazeMeter test](skill-blazemeter-performance-testing://references/jmeter-configuration.md) guide. Configure your test options and set up overrides in preparation for running your JMeter Performance Test at full load.

### Step 4: Run Your Test

Click **Run Test.** You can also click **Debug Test** to validate your test configuration. For more information about debugging, see [Debug Test: Low-Scale Test Run and Enhanced Logging](skill-blazemeter-performance-testing://references/troubleshooting.md).

When your test begins, a report of test results shows, beginning with the [Summary Report](skill-blazemeter-performance-testing://references/reporting.md).

### Additional Test Options

There are optional settings to further enhance testing. For more information, see:

- [Failure Criteria](skill-blazemeter-performance-testing://references/advanced-features.md)
- [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md)
- [APM Integration](skill-blazemeter-performance-testing://references/advanced-features.md)
- [JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
- [DNS Override](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Network Emulation](skill-blazemeter-performance-testing://references/advanced-features.md)
- [JMeter Auto Correlation](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
- [Ignore Labels in Reports](https://help.blazemeter.com/docs/guide/performance-ignore-labels-in-reports.htm)

---

## Create Taurus Test

[Taurus](https://gettaurus.org?utm_source=BM&utm_medium=kb&utm_campaign=creating-a-new-taurus-test) is an open source test automation tool that extends and abstracts the functionality of leading open source testing tools, including [executors](https://gettaurus.org/docs/ExecutionSettings/#Executor-Types) such as [JMeter](https://jmeter.apache.org), [Gatling](https://gatling.io), [Locust.io](https://locust.io), [JUnit](https://junit.org/junit5/), [Selenium](https://www.selenium.dev/), [K6](https://gettaurus.org/docs/K6/), and more. Taurus provides a unified, simplified way to configure and run automated performance tests, then present the results in the most effective form.

**Use when**: Creating Taurus performance tests, uploading YAML/JSON scripts with test assets, or running Taurus tests in BlazeMeter or locally via CLI.

Taurus can consume configuration files written in JSON or YAML languages that are human-readable and simple to use.

### Example

The following Taurus example shows a simple load test with 10 concurrent users, a ramp-up time of 1 minute, a duration of 2.5 minutes and hitting the site blazedemo.com with HTTP GET requests:

```yaml
execution:
concurrency: 10
hold-for: 2m30s
ramp-up: 1m
scenario: Thread Group

scenarios:
Thread Group:
requests:
- label: blazedemo
method: GET
url: http://blazedemo.com/
```

### Create a Taurus Performance Test in BlazeMeter

Follow these steps:

1. In the main menu, click the **Performance** tab.
2. Click **Create Test**.
3. Select a project.
4. Click **Performance Test**.

### Upload a YAML/JSON Script with Test Assets

Click **+** to upload your script and any additional test files, or drag the files over the **Upload Script** box.

**Important Note:** The Taurus `included-configs` setting is not supported in the BlazeMeter cloud. If your YAML references a secondary YAML via `included-configs` for additional configuration settings, merge all settings into one YAML before uploading your test.

For more information, see:

- [Scenario Definition](skill-blazemeter-performance-testing://references/scenarios.md)
- [Uploading Files & Shared Folders](skill-blazemeter-performance-testing://references/scenarios.md)

Under **Configuration Preview**, you will see the YAML/JSON code of the file that you uploaded.

If you are running a JMeter test with Taurus and have uploaded a CSV file with your script, the option to **split CSV files** shows below the script preview. Check this box to enable the feature. For more information, see [Scenario Definition](skill-blazemeter-performance-testing://references/scenarios.md).

There are additional options to add to your test configuration. For more information, see:

- [Failure Criteria](skill-blazemeter-performance-testing://references/advanced-features.md)
- [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md)
- [APM Integration](skill-blazemeter-performance-testing://references/advanced-features.md)
- [DNS Override](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Network Emulation](skill-blazemeter-performance-testing://references/advanced-features.md)

You have set up your Taurus test.

### Run Taurus Tests in BlazeMeter

1. Name your test.
2. (Optional) Click **Debug Test** to validate your test configuration. For more information about debugging, see [Debug Test: Low-Scale Test Run and Enhanced Logging](skill-blazemeter-performance-testing://references/troubleshooting.md).
3. Click **Run Test**.

### Run Taurus Tests on Your Local Machine (CLI)

An alternative method is to call Taurus from the command line on your local machine, then have the test run in BlazeMeter automatically by adding **provisioning: cloud** to the configuration. This method does not require a web browser. For more information, see the [Taurus documentation](https://gettaurus.org/kb/Basic1/#Scaling-With-Cloud-Provisioning?utm_source=BM&utm_medium=kb&utm_campaign=creating-a-new-taurus-test).

---

## Create Multi-Test

Create multi-tests for distributed load testing. The multi-test synchronizes and aggregates the results from multiple test sessions into a single aggregated report.

**Use when**: Creating multi-tests for distributed load testing, synchronizing and aggregating results from multiple test sessions, or running multiple tests simultaneously.

The multi-test configuration includes individual test configurations orchestrated to run simultaneously. Each test is still individual and can be run independently as well.

**Prerequisite:** In order to create multi-tests, you must have an account on a [Pro subscription or higher](https://www.blazemeter.com/pricing).

### Set Up a Multi-Test

**Important Notes:**
- Only tests within the same project can be included in a multi-test.
- You cannot add a specific test multiple times to the same multi-test with the same name. Instead, make one or more copies of the test, each with unique test names that are different from the original test name. Then, when building the multi-test, add the original test and its copies.

Follow these steps:

1. In the main menu, click the **Performance** tab.
2. Click **Create Test**.
3. Select a project.
4. Click **Multi Test**. A multi-test configuration screen opens.
5. Click the **Add tests** search box. A drop-down list with tests appears.
6. Check the box next to each test that you want to add to the multi-test. You can also type in a name of the test and then select the test.
7. Click the **Add tests** button at the bottom of the list. You can only add up to 20 scenarios in one multi-test.

To close the window, click anywhere outside of the window.

Your multi-test summary shows:

### Review the Summary

The main **Summary** section of the configuration page provides an overview of the combined multi-test.

- **Scenarios**: Shows the total number of scenarios (single tests) that you chose for the multi-test, and lists the name of each scenario.
- **Locations**: Lists all locations used by all scenarios combined.
- **Duration**: The total duration of the entire multi-test. This duration is determined by the duration of your single scenarios.
- **VU**: The total number of virtual users (VUs) executed across all scenarios combined.

The graph to the right of the summary is a visual representation of the total VUs (y-axis) across the total duration (x-axis).

### Review the Scenarios

Under the summary is a section dedicated to each individual scenario within the multi-test.

The initial scenario window displays (from top-left to bottom-right):

- The name of the single test.
- The name of the single tests scenario(s).
- The type of test.
- The location(s) the test will run from.
- The total virtual users to run.
- The duration of the single test.

### Modify the Scenarios

To expand the scenario summary to see additional details, click the right arrow (>) in the individual scenario summary. To remove a test, click the bin icon for the scenario.

A miniature version of the [Load Configuration](skill-blazemeter-performance-testing://references/load-configuration.md) and the [Load Distribution](skill-blazemeter-performance-testing://references/load-configuration.md) screens appears. You can modify an individual test scenario but only when it runs as part of this multi-test.

**Important Note:** Disabling overrides in Load Configuration will cause the values to be taken from the single test's original script, and not from that test's original configuration (if overrides are enabled).

### Run the Multi-Test

Once you are satisfied with the summary and have made any adjustment to your scenarios, click the **Run Test** button on the left-hand side of the screen to run your new multi-test.

The next screen provides a final summary of the test you are about to execute.

There are two options you can select prior to launching:

- **Synchronized start**: Ensures that all servers are up before actually starting the test. Select this option if you have a concern that some servers or locations are significantly slower than others and you wish to synchronize them.
- **Run test in the background**: Executes the test behind the scenes so that you can continue working in BlazeMeter.

### Add Load or Logic During a Test

You can add additional load or entirely new test logic to a large test that is already running. No need to stop, reconfigure and re-launch. Launch an additional test and join it to the multi-test in progress.

Follow these steps:

1. Start a multi-test.
2. Once the multi-test is started, start an individual single test.
3. On the **Launch Test** screen, click the dropdown menu under **Run this test as part of a master session?** and select **Run as a test under {name of your multi-test}**.
4. Click the **Launch Servers** button.

You can then return to your multi-test in progress, which is now running with the additional scenario.

For more information, including how to add tests via the API, see [Adding Users Dynamically](skill-blazemeter-performance-testing://references/advanced-features.md).

---

## Create URL/API Test

Creating a new URL/API Test in BlazeMeter is as simple as performing a single GET to a URL. When a more advanced test is needed, the URL/API Test Scenario Definition provides a range of advanced options. The automatic scripting feature generates a Taurus YAML script that executes a JMeter test in where each virtual user will hit each URL sequentially. Each virtual user has their own browser session, cache, and cookies.

**Use when**: Creating URL/API performance tests, adding query parameters, headers, body, assertions, or extracting data from responses.

To record complex scripts directly from your Google Chrome browser, use the [Chrome Extension](skill-blazemeter-recorders://references/chrome-extension.md) or [Proxy Recorder](skill-blazemeter-recorders://references/proxy-recorder.md).

### Create a Test

Follow these steps:

1. In the main menu, click the **Performance** tab.
2. Click **Create Test**.
3. Select a project.
4. Click **Performance Test**.
5. Click the arrow for the **URL / APIs Test**.
6. Add requests. Enter the **Request name** and **URL**.
7. (Optional) If you want to run multiple API calls, you can create a sequential chain of multiple requests. To add more requests, click **+** in the **Scenario Definition** section.
8. (Optional) To select a different request method, expand the drop-down list.
9. (Optional) To duplicate or delete requests, click the dots menu.
10. On the left panel, edit the test name.
11. (Optional) Enter the test **Description** and add **Schedule**. For more information about schedule, see [Scheduling a Test](skill-blazemeter-performance-testing://references/scenarios.md).

### Add Details to a Test

The advanced options available in the Scenario Definition let you quickly create more complex URL/API tests.

#### Add Query Parameters

The Query Parameters tab provides option fields for adding parameters to an API call for querying specific data.

Follow these steps:

1. In **Scenario Definition**, click the **Query parameters** tab.
2. Enter values into the **Key** and **Value** fields. New lines are added automatically.
3. (Optional) To delete an entry, click the bin icon on the right.

BlazeMeter creates the API call automatically appending the parameters to the end of the URL.

**Example:** The API endpoint `https://api.demoblaze.com/entries` allows the use of the **Name**, **Name2** and **Name3** keys to query name values. BlazeMeter creates: `https://api.demoblaze.com/entries?Name=Value&Name2=Value2&Name3=Value3`.

#### Add Headers

**Key** and **Value** fields for adding HTTP headers to your API call may be required by your application server.

Follow these steps:

1. In **Scenario Definition**, click the **Headers** tab.
2. Enter values into the **Key** and **Value** fields. New lines are added automatically.
3. (Optional) To delete an entry, click the bin icon on the right.

#### Add Body

The **Body** tab only appears if the request type allows sending body data. For example, for a **GET** request, there will be no **Body** tab available.

Follow these steps:

1. In **Scenario Definition**, click the **Body** tab.
2. Enter the values.

You can enter body data in the following formats:

- **Key Value** - If the application server requires body data to be sent via specific keys.
- **Text** - For entering raw text, such as JSON content.
- **Content from file** - If you have a file containing the required body data, upload it here.
- **Attach binary files** - This option consists of three fields: a parameter name field, an option to upload a file for the parameter, and a field for providing the mime-type (determined automatically if let blank).

#### Add Assertions

Add assertions to verify the existence of specific data in the response.

Follow these steps:

1. In **Scenario Definition**, click the **Assertions** tab.
2. From the drop-down list, select the type.
3. Fill in the values and click **Add**.
4. (Optional) Add multiple assertions.

If you add a **Text** assertion, BlazeMeter automatically changes the assertion to a **Regex** type and checks the body for the entered value.

If an assertion fails, it shows under the **Errors** tab in the test report. Click the **Assertion Name** tab to review the failures.

#### Extract Data from Responses

You can extract data from the response and store it in a variable for future use.

Follow these steps:

1. In **Scenario Definition**, click the **Extract from response** tab.
2. From the drop-down list, select the type.
3. Enter the values and click **Add**.
4. (Optional) Copy the variable.
5. (Optional) You can then paste the variable into another request, to add it to a URL or other request field. The variable will show in the format of `${variable}`.

### Configure Load

Follow these steps:

1. Configure the load by specifying the total users, duration, and ramp up time. For more information, see [Load Configuration](skill-blazemeter-performance-testing://references/load-configuration.md).
2. Configure the load distribution to decide where traffic will be coming from. For more information, see [Load Distribution](skill-blazemeter-performance-testing://references/load-configuration.md).
3. Click **Run Test** to start the test or **Debug Test** to validate your test configuration. For more information about debugging, see [Debug Test](skill-blazemeter-performance-testing://references/troubleshooting.md).

### Additional Test Options

In addition to the required settings above, there are optional settings to further enhance testing.

For more information, see:

- [Failure Criteria](skill-blazemeter-performance-testing://references/advanced-features.md)
- [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md)
- [APM Integration](skill-blazemeter-performance-testing://references/advanced-features.md)
- [DNS Override](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Network Emulation](skill-blazemeter-performance-testing://references/advanced-features.md)
- [Ignore Labels in Reports](https://help.blazemeter.com/docs/guide/performance-ignore-labels-in-reports.htm)

---

## Documentation References

For detailed information about performance test scenarios, use the BlazeMeter MCP help tools:

**Scenarios**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `performance-scenario-definition` (scenario definition)
  - `performance-upload-files` (uploading files)
  - `performance-duplicate-delete-move-test` (duplicate/delete/move)
  - `performance-run-test` (run test)
  - `performance-stop-test` (stop test)
  - `performance-configure-ultimate-thread-group-scenario` (Ultimate Thread Group)
  - `performance-cvs-split-distribute-engines` (CSV split)
  - `performance-schedule-test` (schedule)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-scenario-definition", "performance-upload-files", "performance-duplicate-delete-move-test", "performance-run-test", "performance-stop-test", "performance-configure-ultimate-thread-group-scenario", "performance-cvs-split-distribute-engines", "performance-schedule-test"]}`

**Creating Performance Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**:
  - `performance-create-jmeter-test` (JMeter test)
  - `performance-create-taurus-test` (Taurus test)
  - `performance-create-multi-test` (Multi-Test)
  - `performance-create-url-api-test` (URL/API test)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-create-jmeter-test", "performance-create-taurus-test", "performance-create-multi-test", "performance-create-url-api-test"]}`

