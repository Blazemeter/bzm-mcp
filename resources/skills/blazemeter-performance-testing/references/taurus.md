# Taurus

## Create Taurus Test

Create Taurus Performance Tests in BlazeMeter by uploading YAML/JSON configuration files with test assets. Taurus is an open source test automation tool that extends and abstracts the functionality of leading open source testing tools, including executors such as JMeter, Gatling, Locust.io, JUnit, Selenium, K6, and more.

**Use when**: Creating Taurus Performance Tests in BlazeMeter, uploading YAML/JSON scripts with test assets, or running Taurus tests in BlazeMeter cloud or from local machine CLI.

### Overview

Taurus provides a unified, simplified way to configure and run automated performance tests, then present the results in the most effective form. Taurus can consume configuration files written in JSON or YAML languages that are human-readable and simple to use.

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

1. In the main menu, click the **Performance** tab
2. Click **Create Test**
3. Select a project
4. Click **Performance Test**

### Upload a YAML/JSON Script with Test Assets

Click **+** to upload your script and any additional test files, or drag the files over the **Upload Script** box.

**Important**: The Taurus `included-configs` setting is not supported in the BlazeMeter cloud. If your YAML references a secondary YAML via `included-configs` for additional configuration settings, merge all settings into one YAML before uploading your test.

For more information, see:
- [Scenario Definition](skill-blazemeter-performance-testing://references/scenarios.md)
- [Uploading Files & Shared Folders](skill-blazemeter-performance-testing://references/advanced-features.md)

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

1. Name your test
2. (Optional) Click **Debug Test** to validate your test configuration. For more information about debugging, see [Debug Test: Low-Scale Test Run and Enhanced Logging](skill-blazemeter-performance-testing://references/troubleshooting.md)
3. Click **Run Test**

### Run Taurus Tests on Your Local Machine (CLI)

An alternative method is to call Taurus from the command line on your local machine, then have the test run in BlazeMeter automatically by adding **provisioning: cloud** to the configuration. This method does not require a web browser. For more information, see the [Taurus documentation](https://gettaurus.org/kb/Basic1/#Scaling-With-Cloud-Provisioning).

---

## Taurus Calibration

You may find that when you run a Performance test with a low number of threads (users), the test executes successfully, but once you begin scaling up to a higher load, the test fails or returns unexpected errors. This is often a sign that your test is in need of calibration, which must be performed to ensure a test will reliably run at higher loads.

This article offers some advice for calibrating a [Taurus](https://gettaurus.org/?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test) test for getting the best results in BlazeMeter. Taurus is an open-source test automation framework, which enables running 20+ open source testing tools, easily. For more information, see [Creating a Taurus Test](skill-blazemeter-performance-testing://references/taurus.md).

If you're instead running a JMeter test without a Taurus YAML, please refer to our [Calibrating a JMeter Test](skill-blazemeter-performance-testing://references/jmeter-configuration.md) guide.

**Use when**: Calibrating Taurus performance tests for optimal engine utilization, determining users per engine, configuring full load tests, or when tests work at low load but fail at higher loads.

### Overview

1. [Create Your Script](skill-blazemeter-performance-testing://references/taurus.md)
2. [Test Locally with Taurus](skill-blazemeter-performance-testing://references/taurus.md)
3. [Create a BlazeMeter Test](skill-blazemeter-performance-testing://references/taurus.md)
4. [Run a Debug Test](skill-blazemeter-performance-testing://references/taurus.md)
5. [Determine Users per Engine](skill-blazemeter-performance-testing://references/taurus.md)
6. [Configure Your Full Load Test](skill-blazemeter-performance-testing://references/taurus.md)
7. [Use a Multi-Test for Multiple Scenarios](skill-blazemeter-performance-testing://references/taurus.md)

### Step 1: Create Your Script

There are various ways to create your script, which include:
- Creating a new [JMeter](http://jmeter.apache.org) script via a Taurus YAML file. For details on how to do so, please refer to the Taurus article [Creating a JMeter Script Using YAML](https://gettaurus.org/kb/Basic1/#Creating-a-JMeter-Script-Using-YAML?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test).
- Creating a new YAML configuration file that references an existing script (such as a script from JMeter, [Selenium](https://www.seleniumhq.org/), or [Gatling](https://gatling.io/)). There is a list of articles about [Learning Taurus](https://gettaurus.org/kb/Index/?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test) that provide details on each option, such as [How to Run an Existing JMeter Script](https://gettaurus.org/kb/Basic1/#How-to-Run-an-Existing-JMeter-Script?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test).
- Using the [BlazeMeter Proxy Recorder](skill-blazemeter-recorders://references/proxy-recorder.md) or [BlazeMeter Chrome Extension](skill-blazemeter-recorders://references/chrome-extension.md) to record your script.

If you generate a JMeter script from a recording, keep in mind that:

1. You'll need to change certain parameters, such as username and password. You can also upload a CSV file with those [test data](skill-blazemeter-test-data://references/core-concepts.md) values so each user can be unique.
2. You might need to extract elements such as Token-String, Form-Build-Id and others, by using Regular Expressions, the [JSON Path Extractor](https://www.blazemeter.com/blog/advanced-usage-json-path-extractor-jmeter?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test), or the [XPath Extractor](https://www.blazemeter.com/blog/using-xpath-extractor-jmeter-0?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test). This will enable you to complete requests like "AddToCart", "Login" and more.
3. Keep your script parameterized and use configuration elements like HTTP Requests Defaults to make your life easier when switching between environments.

### Step 2: Test Locally with Taurus

Begin debugging your script with one thread and one iteration.

```yaml
execution:
concurrency: 1
hold-for: 2m30s
ramp-up: 1m
iterations: 1
scenario: Thread Group

scenarios:
Thread Group:
requests:
- label: blazedemo
method: GET
url: http://blazedemo.com/
```

When the test is running, watch for any items that may be listed under the "Errors" section. Also monitor and be mindful of any irregularities with the "Connect" or "Latency" values.

After your local Taurus test completes, check the bzt.log and jmeter.log files that were generated for any errors or unexpected behavior.

You can examine test results in JMeter by opening the kpi.jtl file, which can be viewed via the "View Results Tree" listener. You can also view the JMX file that Taurus automatically created (if you created a new test via the YAML) or modified (if you ran an existing test via the YAML) by reviewing the JMX file the test generated.

After the script has run successfully using one thread, raise it to 0-20 threads for ten minutes and check:

1. Are the users coming up as unique (if this was your intention)?
2. Are you getting any errors?
3. If you're running a registration process, take a look at your backend. Are the accounts created according to your template? Are they unique?
4. Check test statistics under "Cumulative Stats". Do they make sense (in terms of average times, hits)?

### Step 3: Create a BlazeMeter Test

Now that your test is running successfully locally, you're ready to test it in the cloud! There are two ways you can run your Taurus test via BlazeMeter:

- You can upload your test to BlazeMeter as described in our article [Creating a New Taurus Test](skill-blazemeter-performance-testing://references/taurus.md).
- You can edit the YAML script to automatically run in the BlazeMeter cloud, as detailed in [Scaling With Cloud Provisioning](https://gettaurus.org/kb/Basic1/#Scaling-With-Cloud-Provisioning?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test) on the Taurus site.

### Step 4: Run a Debug Test

Start with a [Debug Test](skill-blazemeter-performance-testing://references/troubleshooting.md), which makes a logical copy of your test and runs it at a lower scale. The test will run with 10 threads and for a maximum of 5 minutes or 100 iterations, whichever occurs first.

This Debug configuration allows you to test your script and backend and ensure everything works well.

Here are some common issues you might come across:

1. Your firewall may block BlazeMeter's engines from reaching your application server. For more information, see [Load Testing Behind Your Corporate Firewall](https://www.blazemeter.com/blog/top-three-options-running-performance-tests-behind-your-corporate-firewall).
2. Make sure all of your test files (CSVs, JARs, JSON, user.properties, etc.) are uploaded to the test. For more information, see [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md) & [Shared Folders](skill-blazemeter-performance-testing://references/taurus.md).
3. Make sure you didn't use any paths with your file names.

If you're still having trouble, look at the [Errors Report](skill-blazemeter-performance-testing://references/reporting.md) and [Logs Report](skill-blazemeter-performance-testing://references/reporting.md) for errors. This will allow you to get enough data to analyze the results and ensure the script was executed as you expected.

You should also check the [Engine Health Report](skill-blazemeter-performance-testing://references/reporting.md) to see how much memory and CPU was used, which is key to the next step.

Lastly, keep an eye out for common issues that may result in your test [running locally but not on BlazeMeter](skill-blazemeter-performance-testing://references/troubleshooting.md) or your [test not starting at all](skill-blazemeter-performance-testing://references/troubleshooting.md).

### Step 5: Determine Users per Engine

Now that we're sure the script runs flawlessly in BlazeMeter, we need to figure out how many users we can apply to one engine. (For details on how to configure users per engine in Taurus, please refer to the article [Load Settings for Cloud](https://gettaurus.org/docs/Cloud/#Load-Settings-for-Cloud?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test).)

Set your test configuration to:
- Concurrency: 500
- Ramp-up: 40 minutes
- Hold-for: 50 minutes
- Do not use any local engines
- Use 1 cloud engine

Run the test and monitor your test's engine via the [Engine Health Report](skill-blazemeter-performance-testing://references/reporting.md).

```yaml
execution:
concurrency: 300
hold-for: 5m
ramp-up: 15m
scenario: Thread Group
locations:
us-east-1: 1

scenarios:
Thread Group:
requests:
- label: blazedemo
method: GET
url: http://blazedemo.com/
```

If your engine didn't reach either a 75% CPU utilization or 85% memory usage (one time peaks can be ignored), then:
- Change the number of threads to 700 and run the test again.
- Raise the number of threads until you get to 1,000 threads or 60% CPU.

If your engine passed the 75% CPU utilization or 85% Memory usage (one time peaks can be ignored) then:
- Look at when your test first got to 75% and see how many users you had at this point.
- Run the test again. This time, decrease the threads per engine by 10%.
- Set the ramp-up time you want for the real test (5-15 minutes is a great start) and set the duration to 50 minutes.
- Make sure you don't go over 75% CPU or 85% memory usage throughout the test.

### Step 6: Configure Your Full Load Test

With your calibration testing complete, you're now ready to run your real test! Now you can:
- Configure the actual amount of users you require.
- Set the number of engines you need for handling the load.

Ensure you keep the users per engine the same as your final successful result in your calibration tests from [Step 3](skill-blazemeter-performance-testing://references/taurus.md).

Consider the following example, where we run a 1,000-user test using five engines:

```yaml
execution:
concurrency: 1000
hold-for: 2h
ramp-up: 30m
scenario: Thread Group
locations:
us-east-1: 2
us-west-1: 3

scenarios:
Thread Group:
requests:
- label: blazedemo
method: GET
url: http://blazedemo.com/
```

Once you're ready, press the "Run Test" button!

### Step 7: Use a Multi-Test for Multiple Scenarios

This step is optional and only applies if your test includes multiple scenarios, in which case you should set up your test as a Multi-Test via the web UI. (For a detailed walkthrough, refer to our guide on [Multi-Tests](skill-blazemeter-performance-testing://references/scenarios.md).)

1. Create a new Multi-Test.
2. Add each single test.
3. You can change the configuration of each scenario as detailed in the Modify the Scenarios section of our [Multi-Test](skill-blazemeter-performance-testing://references/scenarios.md) guide.
4. Click "Run Test" to launch all of your scenarios. Additional options are covered in the Run the Multi-Test section of our [Multi-Test](skill-blazemeter-performance-testing://references/scenarios.md) guide.

The aggregated report of your Multi Test will start generating results in a few minutes, which also can be filtered for each individual scenario. For more information about how to use these filters, refer to our [Reporting Selectors for Scenario and Location](skill-blazemeter-performance-testing://references/reporting.md) guide.

---

## Configure Engines

Configure engine allocation and load distribution for Taurus tests using locations-weighted parameter, controlling how concurrency is spread across engines and locations. The `locations_weighted` parameter in your Taurus configuration file (yml) determines how many engines are allocated to run a test and how the Concurrency is spread over these engines.

**Use when**: Configuring engine allocation and load distribution for Taurus tests or controlling how concurrency is spread across engines and locations.

### Locations-Weighted Parameter

- **`locations-weighted: false`**: Start the given number of machines at each location and spread the load over these engines pro ratio
- **`locations-weighted: true`** (or not specified): The amount specified for each location is only used to calculate the percentage of the concurrency to run at that location

### Example 1: locations-weighted: false with Multiple Locations

Running 20 users using `locations-weighted: false` and 2 locations.

The result is 20 users running on 5 different engines: 3 from us-central1-a and 2 from us-east-1. Each engine will run 4 virtual users, since we have 20 users divided into 5 engines.

```yaml
concurrency: 20
locations:
  us-central1-a: 3
  us-east-1: 2
locations-weighted: false
```

### Example 2: Default Behavior (locations-weighted: true) with Multiple Locations

Running 20 users without specifying the `locations-weighted` field and 2 locations.

The result is 20 users running on 2 different engines: 3/5 of the users (12 users) will run from us-central1-a. 2/5 of the users (8 users) will run from us-east-1. As the BlazeMeter default value allows up to 500 virtual users per engine, this example will run 1 engine per location, and a total of 2 engines for the test.

```yaml
concurrency: 20
locations:
  us-central1-a: 3
  us-east-1: 2
```

### Example 3: Default Behavior with Single Location

Running 20 users without specifying the `locations-weighted` field and 1 location.

The result is 20 users running on 1 location. As the BlazeMeter default value allows up to 500 virtual users per engine, this example will run 1 engine per location, and a total of 1 engines for the test.

```yaml
concurrency: 20
locations:
  us-central1-a: 3
```

### Example 4: locations-weighted: false with Single Location

Running 20 users using `locations-weighted: false` and 1 location.

The result is 20 users running on 2 different engines, both of them from us-central1-a. Each engine will run 10 virtual users, since we have 20 users divided into 2 engines.

```yaml
concurrency: 20
locations:
  us-central1-a: 2
locations-weighted: false
```

### Documentation References

For detailed information about configuring engines for Taurus tests, use the BlazeMeter MCP help tools:

**Configure Engines**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-taurus-configure-engines`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-taurus-configure-engines"]}`

---

## Shared Folders with Taurus

Like other types of BlazeMeter tests, Taurus tests support the use of [shared folders](skill-blazemeter-performance-testing://references/advanced-features.md). For Taurus tests specifically, to ensure that all files are included correctly, perform the following steps:

**Use when**: Using shared folders with Taurus tests, managing and reusing files across multiple tests with YAML configuration and script file organization, or organizing Taurus YAML and script files in shared folders.

1. Place the Taurus YAML configuration and script files in the same shared folder:

2. When creating the Taurus test in BlazeMeter, under the Upload Script option, click "Shared Folder":

3. Place a check next to the shared folder to be used, then click Accept:

4. Ensure that the YAML file refers to the script, including the shared folder:

---

## Create Taurus Dedicated IP

The option to run your Taurus test with Dedicated IPs is available in the YAML configuration file that you execute for your scenario.

**Use when**: Creating Taurus tests with dedicated IP addresses, connecting from behind corporate firewalls with static IP requirements, or configuring dedicated IPs in Taurus YAML files.

Your BlazeMeter account must have the "[Dedicated IPs](skill-blazemeter-performance-testing://references/advanced-features.md)" feature enabled. Then you can configure dedicated IP addresses in your YAML config file as follows:

```
modules:
blazemeter:
dedicated-ips: true
```

You can find the location names by using the command detailed in the [Taurus Cloud Configuration](http://gettaurus.org/docs/Cloud/#Configuring-Cloud-Locations) article.

Here is a detailed example:

```
execution:
- scenario: dummy
concurrency:
local: 5
cloud: 1000
ramp-up: 10s
hold-for: 5m
locations:
europe-west3-a: 1
europe-west2-a: 1
us-east4-a: 1
us-west1-a: 1
provisioning: cloud

modules:
blazemeter:
dedicated-ips: true
```

Your account must have Dedicated IPs in the `locations` configured within your YAML file, so these resources can be provisioned when the test is executed.

---

## Test Data with Taurus Scripts

Use test data (CSV files and Data Entities) in Taurus performance tests, including data-sources configuration, parameterization, and data preview. Same as other script types, Taurus scripts can load test data from external CSV files and from BlazeMeter Data Entities.

As with all test types, BlazeMeter supports the following data sources to provide test data to a Performance test:

- [Load Test Data from Spreadsheets](skill-blazemeter-test-data://references/core-concepts.md)
- [Generate Synthetic Test Data](skill-blazemeter-test-data://references/core-concepts.md)

You can use one or combine multiple data sources in a Taurus test, as needed. To learn more about BlazeMeter's test data integration in general, see [What are Data Entities and Data Parameters?](skill-blazemeter-test-data://references/core-concepts.md) and [How to Use Test Data](skill-blazemeter-test-data://references/core-concepts.md).

**Use when**: Using test data in Taurus performance tests, configuring data-sources, parameterization, and data preview with CSV files and Data Entities, or replacing hard-coded values with dynamic test data.

### Example Scenario

This article assumes a scenario where you already have a Taurus Performance test in YAML format. The Performance test sends requests to the online store endpoint at `http://blazedemo.com/buy/123-phone`. You want to use more varied test data in place of the product id "123" and the product name "phone". To do this, you have the option to load existing data from a CSV file or let BlazeMeter generate synthetic test data.

### Prepare Your Test Data

1. Create a Performance test
2. Upload the Taurus script with hard-coded test data. For example:

   **TaurusPerformanceTest.yaml:**
   ```yaml
   execution:
     - concurrency: 100
       ramp-up: 1m
       hold-for: 1m30s
       scenario: simple
   
   scenarios:
     simple:
       think-time: 0.75
       requests:
         - http://blazedemo.com/buy/123-phone # hard-coded test data "123-phone"
   ```

3. Open the Test Data pane
4. Create Test Data Entities using one or more of the following methods:
   - **Upload a CSV file** and attach it to the test. Example: Upload "MyTestDataFile.csv" which contains the columns `id` and `name`
   - **Create a Data Entity** for the test. Example: Create "MyDataEntity1" that contains synthetic test data which contains the Data Parameters `randomid` and `randomname`
   - **Load a shared Data Entity** from the BlazeMeter Workspace. Example: Load "myshareddata.csv" from "MyTeamFolder" which contains the columns `username` and `password`

5. Identify the Data Parameter names that you want to use in the test. Examples:
   - To use values from the CSV column `id`, reference `${id}`
   - To use values from the CSV column `name`, reference `${name}`
   - To use the synthetic `randomid`, reference `${randomid}`
   - To use the synthetic `randomname`, reference `${randomname}`
   - To use the shared `username`, reference `${username}`
   - To use the shared `password`, reference `${password}`

### Prepare the Taurus Test

Adding the `data-sources` section to the Taurus script is optional when a Data Entity is associated with the test in BlazeMeter. When a test is executed, BlazeMeter dynamically adds any Data Entities associated with the test, using default Data Settings.

1. Edit the Taurus Test in the Test Configuration
2. Parameterize the request by replacing the hard-coded values. For example, replace "123" and "phone" by `${id}` and `${name}`:
   ```
   http://blazedemo.com/buy/${id}-${name}
   ```

3. (Optional) To override the default Data Settings, define your Data Entities in the `data-sources` section of the Taurus file.

   Use the following options:

   - **path**: Defines the path to an attached CSV file or Data Entity. To identify the implicit file name of the Data Entity, click the **info** button next to its name. Example: Reference the Data Entity `MyDataEntity1` as `MyDataEntity1.csv`
   - **delimiter**: Defines the CSV delimiter. Default: Auto detect. Values: '.' for dot, ',' for comma, 'tab' for a tab symbol
   - **quoted**: Interprets the CSV columns as quoted data. Can be true or false. Default: auto detect
   - **encoding**: Defines the encoding type. Example: "utf-8"
   - **loop**: Defines the behavior when BlazeMeter reaches the end of the test data:
     - If set to true, BlazeMeter loops over and continues again from the beginning of the test data
     - If set to false, BlazeMeter stops looping
   - **variable-names**: Defines the comma-separated list of Data Parameter names for the CSV columns. If the first row of the CSV file already contains column headings, leave this option empty. If the first row contains data, define column name mappings here; to skip a column in the mapping, add an extra comma with no name. Default: The first line of the CSV file is used as Data Parameter names. Example: `variable-names: id,name`

   To learn more about the options, see [Taurus DataSources documentation](https://gettaurus.org/docs/DataSources/).

   The Taurus script now looks like the following example:

   **TaurusPerformanceTest.yaml:**
   ```yaml
   execution:
     - concurrency: 100
       ramp-up: 1m
       hold-for: 1m30s
       scenario: simple
   
   scenarios:
     simple:
       think-time: 0.75
       requests:
         - http://blazedemo.com/buy/${id}-${name} # use Data Parameters in test
   
   # list your Data Entities
   data-sources:
     - path: MyTestDataFile.csv # load Data Parameter values from a CSV file
       delimiter: ','
       quoted: false
       encoding: "utf-8"
       loop: true
       variable-names: id,name # define Data Parameter names for columns
   ```

   To override the default Data Settings of other data sources, such as shared files from the BlazeMeter Workspace or synthetic data from a Data Entity, add more `path`s and settings. For example:

   ```yaml
   - path: MyTeamFolder/myshareddata.csv # load shared Data Entity from the Workspace
     variable-names: username,,password # skip the second column, rename the first and third
   
   - path: MyDataEntity1.csv # load Data Parameter values from a Data Entity
     loop: false # don't loop this data
   ```

### Preview Test Data

Previewing your test data is helpful when you are combining data from multiple files, or generating synthetic test data, so you can review values in context.

1. Open a Performance Test with test data attached
2. Verify that at least one data parameter is defined to be able to generate the data preview
3. Click **Test Data**, **Data Settings**. The Test Data Settings window opens and shows the data preview

---

## Using Shared Folders with Taurus

Like other types of BlazeMeter tests, Taurus tests support the use of shared folders. For Taurus tests specifically, to ensure that all files are included correctly, perform the following steps.

**Use when**: Using shared folders with Taurus tests, organizing test files across multiple tests, or sharing test assets between tests.

### Steps to Use Shared Folders

1. **Place the Taurus YAML configuration and script files in the same shared folder**
2. **When creating the Taurus test in BlazeMeter**, under the Upload Script option, click **Shared Folder**
3. **Place a check next to the shared folder to be used**, then click **Accept**
4. **Ensure that the YAML file refers to the script**, including the shared folder

### Best Practices

- Organize related test files in shared folders
- Use shared folders for reusable test assets
- Ensure YAML files correctly reference scripts in shared folders
- Verify file paths when using shared folders

---

## How To Create a Taurus Test with Dedicated IPs

The option to run your Taurus test with Dedicated IPs is available in the YAML configuration file that you execute for your scenario.

**Use when**: Creating Taurus tests with dedicated IP addresses, configuring dedicated IPs for Taurus tests, or ensuring consistent IP addresses for testing.

### Prerequisites

Your BlazeMeter account must have the **Dedicated IPs** feature enabled. Then you can configure dedicated IP addresses in your YAML config file as follows:

```yaml
modules:
  blazemeter:
    dedicated-ips: true
```

### Configuration Example

You can find the location names by using the command detailed in the [Taurus Cloud Configuration](http://gettaurus.org/docs/Cloud/#Configuring-Cloud-Locations) article.

Here is a detailed example:

```yaml
execution:
- scenario: dummy
  concurrency:
    local: 5
    cloud: 1000
  ramp-up: 10s
  hold-for: 5m
  locations:
    europe-west3-a: 1
    europe-west2-a: 1
    us-east4-a: 1
    us-west1-a: 1
  provisioning: cloud

modules:
  blazemeter:
    dedicated-ips: true
```

### Important Notes

- Your account must have Dedicated IPs in the `locations` configured within your YAML file, so these resources can be provisioned when the test is executed
- Dedicated IPs provide consistent IP addresses for testing
- Ensure your account has the Dedicated IPs feature enabled before using this configuration

---

## Documentation References

For detailed information about Taurus, use the BlazeMeter MCP help tools:

**Taurus**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**:
  - `performance-create-taurus-test` (create test)
  - `performance-taurus-calibration` (calibration)
  - `performance-taurus-configure-engines` (configure engines)
  - `performance-shared-folders-taurus` (shared folders)
  - `performance-create-taurus-dedicated-IP` (dedicated IP)
  - `test-data-with-taurus-scripts` (test data)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-create-taurus-test", "performance-taurus-calibration", "performance-taurus-configure-engines", "performance-shared-folders-taurus", "performance-create-taurus-dedicated-IP", "test-data-with-taurus-scripts"]}`

