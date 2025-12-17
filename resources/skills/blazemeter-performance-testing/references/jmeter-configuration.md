# JMeter Configuration

## JMeter Properties

JMeter Properties can be used to parameterize your test. One version of your script can then be used in several different test configurations. JMeter properties also allow you to make mid-test changes to script behavior.

**Use when**: Configuring JMeter properties in BlazeMeter tests for parameterization, changing test behavior during test execution, or using one script version for multiple test configurations.

### Configure JMeter Properties

Follow these steps:

1. In the **Performance Testing** tab, click **Tests** and open a test
2. Click the **Configuration** tab
3. Scroll down to the **JMeter Properties** section
4. (Optional) From the drop-down menu for JMeter and Java version, specify the desired JMeter and/or Java version to run the test with. If left at their default selections, BlazeMeter will attempt to auto-detect the version of JMeter in which the uploaded test script was created. The default Java version is shown as well. The JMeter and Java versions available in the drop-down menus are the only versions supported
5. Set the JMeter parameters before the test launch. Slide the toggle to ON
6. Enter the property and value. Once you add a property, a new section for another property and value appears automatically. To remove a line, click the bin icon next to the line

### Change JMeter Properties mid-test with Remote Control

You can change JMeter Properties during a test with the Remote Control button in the live reporting screen. For more information, see [Live Remote Control for JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md).

### Upload a Custom user.properties File

Alternatively, you can upload an existing user.properties file containing JMeter Properties to your BlazeMeter test configuration. Make sure there are local file path references to the user.properties file, then BlazeMeter will automatically pick it up when the test executes. For more information, see [Upload a Custom user.properties File](skill-blazemeter-performance-testing://references/jmeter-configuration.md).

---

## JMeter User Properties

Upload custom user.properties files to configure JMeter behavior, including parser, SSL, HTTP client, and other settings. Any part of a JMeter script can be customized by JMeter Properties, starting from look and feel, time stamps, log levels, output file formats and ending with low-level parameters of underlying libraries like HTTP Client timeouts, bind addresses, and so on, used for different protocols connections.

**Use when**: Uploading custom user.properties files to configure JMeter behavior, customizing parser, SSL, HTTP client, or other JMeter settings, or using existing user.properties files from local JMeter installations.

### Upload a Custom user.properties File

You can upload your own user.properties file to your BlazeMeter test configuration. Make sure there are local file path references to the user.properties file, then BlazeMeter will automatically pick it up when the test executes. For more information about how to attach the file to the test, see [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md).

### Which Features Does a user.properties File Control?

Configure the user.properties file to alter the following features (ref. JMeter Version 3.3):

- **XML Parser** - Parser configuration
- **SSL configuration** - SSL settings
- **Look and Feel configuration** - UI appearance
- **Toolbar display** - Toolbar settings
- **JMX Backup configuration** - Backup settings
- **Remote hosts and RMI configuration** - Remote configuration
- **Include Controller** - Include controller settings
- **HTTP Java configuration** - HTTP Java settings
- **Apache HttpClient common properties** - HTTP client properties
- **Kerberos properties** - Kerberos authentication
- **Apache HttpClient logging examples** - HTTP client logging
- **Apache HttpComponents HTTPClient configuration (HTTPClient4)** - HTTPClient4 settings
- **HTTP Cache Manager configuration** - Cache settings
- **Results file configuration** - Results file settings
- **Settings that affect SampleResults** - Sample result settings
- **Upgrade** - Upgrade settings
- **JMeter Test Script recorder configuration** - Recorder settings
- **Test Script Recorder certificate configuration** - Certificate settings
- **JMeter Proxy configuration** - Proxy settings
- **HTML Parser configuration** - HTML parser settings
- **Remote batching configuration** - Remote batching
- **JDBC Request configuration** - JDBC settings
- **OS Process Sampler configuration** - OS process settings
- **TCP Sampler configuration** - TCP settings
- **Summariser - Generate Summary Results - configuration** (mainly applies to non-GUI mode)
- **Aggregate Report and Aggregate Graph - configuration** - Report settings
- **BackendListener - configuration** - Backend listener settings
- **BeanShell configuration** - BeanShell settings
- **MailerModel configuration** - Mailer settings
- **CSVRead configuration** - CSV read settings
- **time() function configuration** - Time function settings
- **CSV DataSet configuration** - CSV dataset settings
- **LDAP Sampler configuration** - LDAP settings
- **Miscellaneous configuration** - Other settings
- **Classpath configuration** - Classpath settings
- **Reporting configuration** - Reporting settings
- **Additional property files to load** - Additional files
- **Thread Group Validation feature** - Thread group validation
- **Timer related feature** - Timer settings
- **Naming Policy** - Naming policy settings

You can customize these JMeter Properties in the user.properties file for your needs. For more information, see the [official Apache JMeter Properties guide](http://jmeter.apache.org/usermanual/properties_reference.html).

---

## Live Remote Control for JMeter Properties

While [you can set JMeter properties directly in BlazeMeter](skill-blazemeter-performance-testing://references/jmeter-configuration.md), you may also want to change the behavior of your test while the test is running. BlazeMeter allows you to remotely change the value of any JMeter property in real-time, using the **Remote Control** feature.

**Use when**: Changing JMeter properties in real-time during test execution or using Remote Control feature for dynamic test configuration.

- [Update JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
- [Advanced Features](skill-blazemeter-performance-testing://references/jmeter-configuration.md) [Remote Control for Multi-Tests](skill-blazemeter-performance-testing://references/jmeter-configuration.md) [Filter JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md) [Add New JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
- [Other Live Features](skill-blazemeter-performance-testing://references/jmeter-configuration.md)

### Update JMeter Properties

Follow these steps:

1. Add one or more properties to the [JMeter Properties](skill-blazemeter-performance-testing://references/jmeter-configuration.md) section of your test configuration.
2. Start your test.
3. When the test report appears, click the **Run Time Control** button at the top-right and click **Remote Control**. The button is only available while the test is running and will disappear after the test completes.
4. The **Remote Control Live** window appears, listing all JMeter properties available for updating. This by default includes all scenarios in all locations. For more details, see [Advanced Features](skill-blazemeter-performance-testing://references/jmeter-configuration.md).
5. Enter a new value for each property you want to update and click **Send** to update the property on all engines.

### Advanced Features

#### Remote Control for Multi-Tests

Remote Control works for both single tests and multi-tests. If a test has multiple scenarios, the default option for the **Remote Control Live** window is to show all properties for all scenarios. This is especially useful for a [multi-test](skill-blazemeter-performance-testing://references/scenarios.md) in which various single tests have different properties to adjust.

#### Filter JMeter Properties

For tests / [multi-tests](skill-blazemeter-performance-testing://references/scenarios.md) with multiple scenarios, you can filter the **Remote Control Live** window to show JMeter properties that only relate to a specific scenario and/or location. Use the Scenario and/or Location filters in the top-right corner of the test report before clicking the **Remote Control** button.

#### Add New JMeter Properties

Apart from modifying existing properties, you can also add new JMeter properties.

Follow these steps:

1. In the **Remote Control Live** window, in the **New Key** row, click **Select Scenario**.
2. From the drop-down list, select the scenario (in a multi-scenario test) to which you want to add the new property.
3. Fill out the remaining fields for the **New Key** row.
4. Click **Add**.
5. Click **Send**.

### Other Live Features

There are more options you can adjust while running a test beyond JMeter properties. See the following guides for some more options you can adjust mid-test:

- If you want to modify your Requests Per Second (RPS) on the fly, see the **Changing RPS Limits 'On The Fly'** section of the [Load Configuration](skill-blazemeter-performance-testing://references/load-configuration.md) guide.
- When executing a [multi-test](skill-blazemeter-performance-testing://references/scenarios.md), you can add users dynamically to adjust the load while the test is in progress. For more information, see [Adding Users Dynamically](skill-blazemeter-performance-testing://references/advanced-features.md).

---

## JMeter Auto Correlation Rules

After recording a Performance test in Apache JMeter, the recorded test is not immediately able to maintain the same session. Certain dynamic values change every time you make a request: the session ID, CSRF tokens, time stamps, and so on. Before the automated test can run, you must identify these dynamic values in the HTTP requests and responses, and replace them with variables. This manual process is called correlation.

Correlation is not the same as parameterization where hard-coded values are replaced by test data, because test data is from a different source. Correlation means extracting values *from a previous response* and passing them as arguments *to the next request*. Correlation is important in Performance testing because without it, generally, tests won't run at all or not as intended.

You as Tester typically use regular expressions or other extractors to extract values from responses; you store extracted values in variables and insert those variables in subsequent requests. This complex manual task takes up a lot of test creation time. BlazeMeter offers a JMeter plugin to assist you with correlation by doing repetitive tasks automatically.

**Use when**: Automatically detecting and fixing correlation issues in JMeter tests or using the Auto Correlation Recorder plugin.

### Use the Auto Correlation Recorder Plugin

The BlazeMeter **Auto Correlation Recorder** is an open-source JMeter plugin that provides automatic correlation for JMeter tests. The plugin accelerates the test creation process, eliminates much of the complexity of correlation, and saves time. The plugin is built on top of the old BlazeMeter Correlation Plugin.

The recording process is the same as recording with the [Apache JMeter Proxy Recorder](https://jmeter.apache.org/usermanual/jmeter_proxy_step_by_step.html), see the Apache documentation for details.

The plugin adds the following functionality to JMeter:
- If a JMeter test plan replay has errors, the plugin suggests correlations to fix them.
- The plugin opens an **Automatic Correlation Wizard** where you can choose which suggestions you want to apply. To provide context, the wizard lists attribute names and values from the response, when they were used, and where they were obtained from.
- From your selections, the plugin creates templates of correlation rules.
- The plugin lets you save and load your correlation rule templates files.

### Resources

- Download the plugin from [github.com/Blazemeter/CorrelationRecorder](https://github.com/Blazemeter/CorrelationRecorder/releases).
- For official usage documentation, see [blazemeter.github.io/CorrelationRecorder/guide](https://blazemeter.github.io/CorrelationRecorder/guide/).

### Types of Correlation Templates

- Buit-in templates - Are free to use.
- Enterprise templates - Require you to have an account that is not free.
- Workspace templates - Can be edited and exported. They are also shared with anyone invited to your account.

### Store Correlation Rule Templates

A BlazeMeter repository stores and shares correlation rule templates across your account. A correlation rule template contains one or more correlation rules files. To add templates, export them from JMeter's correlation recorder plugin in JSON format and click **Upload**.

To see which correlation rules you have stored in your BlazeMeter workspace, go to **Settings, Workspace, Correlation Rules**. Browse your Correlation Rule templates to see their names and versions.

Your own rules are available in your workspace only. You have access to all built-in rule templates that are part of your plan, and to all user rule templates that you have created in the specific workspace, including all detection files and correlation files that you have uploaded yourself.

### Create a Correlation Template

Follow these steps:

1. In JMeter, use the Correlation Recorder plugin to create your Correlation Template.
2. In your JMeter installation folder, navigate to your local correlation-template folder.
3. Locate the Template JSON file that you want to upload. If you want to edit Name, Version, and Description, edit the JSON file in a text editor now.
4. In BlazeMeter, go to **Settings, Workspace, Correlation Rule Templates**.

You can find the new template in your list of templates.

To remove a template, click the delete button in the **Actions** column of the rule template.

### Version Control and Test History

Version Control and test history for correlations is designed to enhance your testing workflow and reduce debugging time.

You can:

- **Undo changes** and restore your test plan to the original state
- **View detailed history** of your test plan, including all actions, steps, and versions
- **Select and restore** the version of your test plan that you need

#### Restore a previous version of a test plan

Follow these steps:

1. In your **Test Plan**, go to **bzm - Correlation Recorder**
2. Navigate to the **Correlation** tab, and click **History**. A History Manager window opens
3. Check the box next to the version of the test plan that you want to revert to
4. Click **Restore**

### JSON Correlation Rules

JSON was added as a configurable element in the correlation rules. Instead of creating complex regular expressions, you can now create JSON-type correlation rules and save and use templates with JSON rules.

#### Create a JSON-type correlation rule

Follow these steps:

1. In JMeter, bzm-Correlation Recorder, click the **Correlation** tab
2. Click **Add**
3. For Correlation Extractor and Correlation Replacement drop-down lists, select the **JSON** rule type and fill out the JSON path expression
4. Enable **Legacy Correlation** mode. This will allow you to record, using the current rules. If you already have a template and want to run an analysis of a particular flow, do not check the **Legacy Correlation** checkbox. Then, in the pop-up window, select **Existing Correlation Templates**
5. Click **Start** to record your flow
6. A pop-up window shows. Click **Yes** to confirm that the legacy mode is enabled

After you stop the recording, click **Recording Controller** in the left menu to see details. You can see the JSON Path extractor there. It contains the JSON path expression that you've set.

---

## Calibrating a JMeter Test

You may find that when you run a Performance test on BlazeMeter with a low number of threads (users), the test executes successfully, but once you begin scaling up to a higher load, the test fails or returns unexpected errors. This is often a sign that your test is in need of calibration, which must be performed to ensure a test will reliably run at higher loads.

This article offers some advice for calibrating a JMeter test for getting the best results in BlazeMeter. Using a Taurus YAML with your test? If so, then please follow our [Calibrating a Taurus Test guide](skill-blazemeter-performance-testing://references/taurus.md).

**Use when**: Calibrating JMeter tests for higher loads, ensuring tests run reliably at scale, or troubleshooting test failures when scaling up.

### Overview

1. [Create Your Script](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
2. [Test Locally with JMeter](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
3. [Run a Debug Test](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
4. [Determine Users per Engine](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
5. [Configure Your Full Load Test](skill-blazemeter-performance-testing://references/jmeter-configuration.md)
6. [Use a Multi-Test for Multiple Scenarios](skill-blazemeter-performance-testing://references/jmeter-configuration.md)

### Step 1: Create Your Script

There are two ways to create your script:
- Use the BlazeMeter Proxy Recorder or BlazeMeter Chrome Extension to record your script.
- Go manually all-the-way and construct everything from scratch. This is more common for functional/QA tests.

If you generate a JMeter script from a recording, keep in mind that:

1. You'll need to change certain parameters, such as username and password. You can also upload a CSV file with those [test data](skill-blazemeter-test-data://references/core-concepts.md) values so each user can be unique.
2. You might need to extract elements such as Token-String, Form-Build-Id and others, by using Regular Expressions, the [JSON Path Extractor](https://www.blazemeter.com/blog/advanced-usage-json-path-extractor-jmeter?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test), or the [XPath Extractor](https://www.blazemeter.com/blog/using-xpath-extractor-jmeter-0?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test). This will enable you to complete requests like "AddToCart", "Login" and more.
3. You should keep your script parameterized and use configuration elements like HTTP Requests Defaults to make your life easier when switching between environments.

### Step 2: Test Locally with JMeter

Start debugging your script with one thread, one iteration, and using the View Results Tree element, Debug Sampler, and Dummy Sampler. Keep the Log Viewer open in case any JMeter errors are reported.

Go over the True and False responses of all the scenarios to make sure the script is performing as you expected.

After the script has run successfully using one thread, raise it to 0-20 threads for ten minutes and check:

1. Are the users coming up as unique (if this was your intention)?
2. Are you getting any errors?
3. If you're running a registration process, take a look at your backend. Are the accounts created according to your template? Are they unique?
4. Check test statistics under "Cumulative Stats". Do they make sense (in terms of average times, hits)?

Once your script is ready:

1. Clean it up by removing any Debug/Dummy Samplers and deleting your script listeners.
2. If you use Listeners (such as "Save Responses to a file") or a CSV Data Set Config, make sure you don't use any paths; use only the filename (as if it was in the same folder as your script).
3. If you're using your own proprietary JAR file(s), upload them.
4. If your script uses more than one thread group, be aware of how BlazeMeter divides users among multiple thread groups, as detailed in our explanation of [Total Users](skill-blazemeter-performance-testing://references/load-configuration.md).
5. If your script uses special thread groups, be aware of how BlazeMeter handles such thread groups. Our guide of how [Ultimate Thread Groups](skill-blazemeter-performance-testing://references/scenarios.md) are handled provides these details.

### Step 3: Run a Debug Test

Start with a [Debug Test](skill-blazemeter-performance-testing://references/troubleshooting.md), which makes a logical copy of your test and runs it at a lower scale. The test will run with 10 threads and for a maximum of 5 minutes or 100 iterations, whichever occurs first.

This Debug configuration allows you to test your script and backend and ensure everything works well.

Here are some common issues you might come across:

1. Your firewall may block BlazeMeter's engines from reaching your application server. For more information, see [Load Testing Behind Your Corporate Firewall](https://www.blazemeter.com/blog/top-three-options-running-performance-tests-behind-your-corporate-firewall).
2. Make sure all of your test files (CSVs, JARs, JSON, user.properties, etc.) are uploaded to the test. For more information, see [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md) & [Shared Folders](skill-blazemeter-performance-testing://references/advanced-features.md).
3. Make sure you didn't use any paths with your file names.

If you're still having trouble, look at the [Errors Report](skill-blazemeter-performance-testing://references/reporting.md) and [Logs Report](skill-blazemeter-performance-testing://references/reporting.md) for errors. This will allow you to get enough data to analyze the results and ensure the script was executed as you expected.

You should also check the [Engine Health Report](skill-blazemeter-performance-testing://references/reporting.md) to see how much memory and CPU was used, which is key to the next step.

Lastly, keep an eye out for common issues that may result in your test [running locally but not on BlazeMeter](skill-blazemeter-performance-testing://references/troubleshooting.md) or your [test not starting at all](skill-blazemeter-performance-testing://references/troubleshooting.md).

### Step 4: Determine Users per Engine

Now that we're sure the script runs flawlessly in BlazeMeter, we need to figure out how many users we can apply to one engine. (For details on how to configure users per engine in Taurus, please refer to the article [Load Settings for Cloud](https://gettaurus.org/docs/Cloud/#Load-Settings-for-Cloud?utm_source=BM&utm_medium=kb&utm_campaign=calibrating-a-taurus-test).)

Set your test configuration to:
- Number of threads: 500
- Ramp-up: 40 minutes
- Duration: 50 minutes
- Use 1 engine.

Run the test and monitor your test's engine via the [Engine Health Report](skill-blazemeter-performance-testing://references/reporting.md).

If your engine didn't reach either a 75% CPU utilization or 85% memory usage (one time peaks can be ignored), then:
- Change the number of threads to 700 and run the test again.
- Raise the number of threads until you get to 1,000 threads or 60% CPU.

If your engine passed the 75% CPU utilization or 85% Memory usage (one time peaks can be ignored) then:
- Look at when your test first got to 75% and see how many users you had at this point.
- Run the test again. This time, decrease the threads per engine by 10%.
- Set the ramp-up time you want for the real test (5-15 minutes is a great start) and set the duration to 50 minutes.
- Make sure you don't go over 75% CPU or 85% memory usage throughout the test.

### Step 5: Configure Your Full Load Test

Once we know the script is working and we how many users each engine can sustain, we can finally configure the test to achieve our load testing goal.

Let's assume these values (as an example):
- One engine can have 500 users
- We aim to test for 10K users

This means to achieve our goal, our test needs 20 engines (10,000 \ 500). Those 20 engines can either be all in one geographic location, or spread across multiple locations. For more information, see [Load Distribution](skill-blazemeter-performance-testing://references/load-configuration.md).

### Step 6: Use a Multi-Test for Multiple Scenarios

This step is optional and only applies if your test includes multiple scenarios, in which case you should set up your test as a Multi-Test via the web UI. (For a detailed walkthrough, refer to our guide on [Multi-Tests](skill-blazemeter-performance-testing://references/scenarios.md).)

1. Create a new Multi-Test.
2. Add each single test.
3. You can change the configuration of each scenario as detailed in the Modify the Scenarios section of our [Multi-Test](skill-blazemeter-performance-testing://references/scenarios.md) guide.
4. Click **Run Test** to launch all of your scenarios. Additional options are covered in the Run the Multi-Test section of our [Multi-Test](skill-blazemeter-performance-testing://references/scenarios.md) guide.

The aggregated report of your Multi Test will start generating results in a few minutes, which also can be filtered for each individual scenario. For more information about how to use these filters, refer to our [Reporting Selectors for Scenario and Location](skill-blazemeter-performance-testing://references/reporting.md) guide.

---

## Documentation References

For detailed information about JMeter configuration, use the BlazeMeter MCP help tools:

**JMeter Configuration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `performance-jmeter-properties` (properties)
  - `performance-jmeter-user-properties` (user properties)
  - `performance-live-remote-control-for-jmeter-properties` (live remote control)
  - `performance-jmeter-auto-correlation-rules` (auto correlation)
  - `performance-jmeter-calibration` (calibration)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-jmeter-properties", "performance-jmeter-user-properties", "performance-live-remote-control-for-jmeter-properties", "performance-jmeter-auto-correlation-rules", "performance-jmeter-calibration"]}`

