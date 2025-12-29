# Troubleshooting

## Test Won't Start Troubleshooting

What do you do if you try to run a Performance test, but it fails to start? You may have been met with a Failed Report Summary showing the following error message:

*Session ended without load report data*

Another variation of this behavior may instead result in an empty report being generated:

Alternatively, you may have observed that your test hangs indefinitely at the starting stage, generating the above message only after you manually terminate it.

**Use when**: Troubleshooting Performance tests that fail to start, resolving missing files, misconfigured tests, Private Locations failures, or when tests hang at startup.

### First Steps

When this happens, the first thing to do is to click the Logs tab to review your [Logs Report](skill-blazemeter-performance-testing://references/reporting.md). Download the *artifacts.zip* and review the logs included in it.

The most common causes of a startup hang or failure fall under these categories:

- [Missing Files](skill-blazemeter-performance-testing://references/troubleshooting.md)
- [Misconfigured Test](skill-blazemeter-performance-testing://references/troubleshooting.md)
- [Private Locations Failure](skill-blazemeter-performance-testing://references/troubleshooting.md)

### Missing Files

The #1 most common cause for a startup hang or failure is a missing file, such as a missing CSV file that your test script references, for example. The tell-tale sign that this is the problem is when you find the following message in one of your log files (usually the bzt.log or, when running a JMeter test, the jmeter.log):

```
2019-05-01 21:21:40,919 ERROR o.a.j.t.JMeterThread: Test failed!
java.lang.IllegalArgumentException: File your_file_name.csv must exist and be readable
```

This means one of the following:

- **You may not have uploaded all files required** to run your test script in BlazeMeter. If your test script requires any additional files (CSVs, JARs, etc.), then refer to our guides on [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md) and [Shared Folders](skill-blazemeter-performance-testing://references/advanced-features.md).
- **You may have uploaded a required file, but your test script still refers to it using a local file path**. For example, a CSV Data Set Config element may still refer to a CSV file using a local path. This is likewise explained in our guide on guides on [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md) and [Shared Folders](skill-blazemeter-performance-testing://references/advanced-features.md).
- **You may have uploaded a required file, but the filename referenced in your script is in a different case than the filename of the one uploaded**. BlazeMeter engines run on Linux, which treats filenames as case-sensitive, so *Your_File_Name.csv* is a different file from *your_file_name.csv* or *Your_File_name.csv*. Make sure your filename references are consistent with the case used in your uploaded filename.

### Misconfigured Test

- **You may have accidentally designated the wrong file as your main test file**. In the following example, we have a [Taurus](skill-blazemeter-performance-testing://references/scenarios.md) YAML file pointing to a Gatling script file, and the YAML is correctly designated as the main file: However, if you accidentally click the other file, the arrow will move to it, changing it to the main file: The second scenario will fail to start since BlazeMeter requires a YAML in order to execute the Gatling script, yet in this configuration, BlazeMeter will ignore the YAML file entirely. To fix it, just click the YAML again to reinstate it as the main test file.
- **You may have tried to run a test that requires more engines than your plan allows for**. For example, if you are on a [Basic Plan](https://www.blazemeter.com/pricing) which only allows for two engines (load generators), but attempt to start a test configured to utilize four engines, the test may hang on startup since it is trying to spin up two additional engines that are not available under the terms of the subscription plan. If you have enabled [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md), please be aware that this feature requires running on an additional engine of its own. For example, a one-engine test with EUX Monitoring enabled requires two engines in total.

### Private Locations Failure

If you're executing your test via a [Private Location](skill-blazemeter-private-locations://references/introduction.md) instead of a cloud engine, then the problem may not be with your test, but with your agent.

- **The most common problems with agents include connection issues or the agent running out of disk space**, both of which can be addressed by ensuring all [System Requirements](skill-blazemeter-private-locations://references/installation.md) are met and testing for any [connection issues between the agent and BlazeMeter](skill-blazemeter-private-locations://references/troubleshooting.md).
- Make sure to [review your agent's logs](skill-blazemeter-private-locations://references/management.md) and [verify all image tags](skill-blazemeter-private-locations://references/troubleshooting.md) appears as they should.

---

## High Response Time

**Symptom**: My average response time for a test is higher than what was expected or desired.

Examples:
- A BlazeMeter test has a higher average response time than the same test run locally
- Two different BlazeMeter tests show different average response times
- Two runs of the same BlazeMeter test show different average response times
- Tests run from different locations or engine providers show different average response times

**Use when**: Troubleshooting high response times in performance tests, identifying bottlenecks, analyzing response time patterns, or optimizing test configuration.

### Understanding BlazeMeter's Role

**BlazeMeter is Merely the Messenger**: BlazeMeter only reports these metrics as observed by the engine from the location or provider you selected. BlazeMeter does not in any way impact or interfere with these metrics; it only reports them. BlazeMeter has no control over response time, nor does BlazeMeter affect actual response times. (Service Virtualization can [Simulate Irregular Response Latencies](https://help.blazemeter.com/docs/guide/mock-service-think-time-irregular-response-latency.html) *in addition* to the response time.)

**Waiting for a Call Back**: When you run a test from BlazeMeter, the system can only know how long it took your application server to respond; it doesn't know why it took as long as it did.

### Solution

To find out why your application server took as long to respond to the test engines as it did, investigate your own server and network internally with the appropriate teams that can help you troubleshoot. Here are some pointers to help you get started.

#### (1) A BlazeMeter test has a higher average response time than the same test run locally

BlazeMeter's engines are in different geographical locations and on different networks than your local machine, so response times are not comparable between the two. If your local machine is on the same network as your application server, data has less distance to travel. There will always be a difference between the routes from each engine to your server compared to from your local machine to your server.

**Solution**: To test locally, set up a [Private Location](https://help.blazemeter.com/docs/guide/private-locations-intro.html): your own BlazeMeter engine which you install within your own network.

#### (2) Two different BlazeMeter tests show different average response times

There are many reasons why response times may differ between two different tests. For example, expect a multi-test to experience higher response times than a single test. A more complex script puts a heavier strain on your application server or your network, resulting in bottlenecks that affect response time. Keep in mind that no two test scripts are alike, so some differences are inevitable.

#### (3) Two runs of the same BlazeMeter test show different average response times

It's not uncommon for two runs of the same test to have considerably different average response times. If this happens, work with your application server and network teams to investigate what conditions differed between the time frames of the two runs. It's possible an internal server or network issue caused a momentary delay in getting responses out to BlazeMeter's engines.

#### (4) Tests run from different locations or engine providers show different average response times

Variances in response times are to be expected, because (a) data sent to engines in two different geographic locations travels different routes and (b) different providers (Google, AWS, Azure) provide different machines, and though they are comparable, they are not exactly the same.

In case of the former, if the difference in response times is severe, you may need to work with your network team internally to identify bottlenecks in sending data to some locations versus other locations.

---

## 500 Response

**Symptom**: When executing your JMeter test script via BlazeMeter, the test encounters a number of HTTP 500 errors in response to some of your samplers, which will appear under the Errors tab of your report.

**Use when**: Troubleshooting 500 Internal Server Error responses in performance tests or resolving server-side issues, configuration problems, and test script errors.

### Reason

The HTTP server response 500 means "internal server error". This is a generic code that requires investigating in your application server itself to troubleshoot. On the BlazeMeter side, your server does not send us any additional information by which to know why it sent a 500 code.

### Solution

This error code usually does not point to a problem with BlazeMeter, but to a scripting problem. We recommend investigating this problem in two ways:

1. **Ensure your script can run in your local JMeter environment** before running it through BlazeMeter
2. **Investigate your application server**, starting with your application server's logs, to see why your server returned 500 codes during the time frame of the test

---

## Partial Load

**Symptom**: You only see a partial load in your Performance test.

You can see the occurrence in the log files. Either the engine's log file will be missing (defunct), or there will be an error in the console log when trying to connect, or both.

In case of a defunct engine, a message will appear in the test session dashboard.

**Use when**: Troubleshooting partial load issues where tests don't reach expected load levels, resolving engine allocation problems, or addressing defunct engine issues.

### Reason

The cause is most likely that one of the engines was found defunct or it took too long to launch and the test has started without it. This is normal and can happen occasionally.

### Solution

In either scenario, we recommend restarting the session (press reboot). This solves the common scenario of the engine taking too long to launch.

---

## Selenium vs JMeter Load Testing

Using Selenium for load testing is not recommended. Whereas JMeter is well suited for high-load performance tests, especially through BlazeMeter, Selenium is more suited for UI functional tests.

**Use when**: Understanding differences between Selenium and JMeter for load testing, choosing between Selenium and JMeter based on use cases and performance characteristics, or determining when to use Selenium vs JMeter for performance testing.

### Why Selenium is Not Recommended for Load Testing

This is primarily because each "user" in a Selenium test runs through its own individual browser, which means if you're running 10 users on 1 engine, you are launching 10 web browsers simultaneously. Launching many multiple browser instances is a major CPU consumption per engine.

### Recommendations for Running Selenium Tests on BlazeMeter

For running Selenium tests on BlazeMeter, we recommend using [Taurus](skill-blazemeter-performance-testing://references/taurus.md) and starting with a maximum of 5 [users per engine](skill-blazemeter-performance-testing://references/taurus.md), then adjust accordingly as resources allow (which you can monitor via the Engine Health tab of your test report). Additional guidance on how to properly calibrate a test for best performance can be found in [Calibrating a Taurus Test](skill-blazemeter-performance-testing://references/taurus.md).

### Multi-Test Approach for Higher Loads

There is a way around the recommended five-user maximum, however: You can execute a [multi-test](skill-blazemeter-performance-testing://references/scenarios.md) in which each single test runs no more than five users each. You can add the single test multiple times to the multi-test. For example, if you wanted to test a fifteen-user load, you could create a multi-test that includes three instances of the single five-user test.

---

## Test Works Locally but Not in BlazeMeter

There are various reasons why a test script that works on your local machine will fail to run through BlazeMeter.

**Use when**: Troubleshooting tests that work locally but fail in BlazeMeter, resolving environment differences, configuration issues, and network problems, or debugging JMeter test failures in BlazeMeter.

### First Steps

The first and the foremost thing you should do is check the errors found in your test's [Errors Report](skill-blazemeter-performance-testing://references/reporting.md), then download and review the logs from your test's [Logs Report](skill-blazemeter-performance-testing://references/reporting.md).

The most common causes for this problem fall under these categories:

- [Missing File(s)](skill-blazemeter-performance-testing://references/troubleshooting.md)
- [Network Issues](skill-blazemeter-performance-testing://references/troubleshooting.md)
- [Load/Performance Issues](skill-blazemeter-performance-testing://references/troubleshooting.md)

### Missing Files

- **You may not have uploaded all files required** to run your test script in BlazeMeter. If your test script requires any additional files (CSVs, JARs, etc.), then refer to our guides on [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md) and [Shared Folders](skill-blazemeter-performance-testing://references/advanced-features.md).
- **If you submit your test from CLI** (e.g. using the -cloud option), make sure your yml includes a *files:* section and list all files that are referenced in your script so they will be uploaded to the test. See section "Specifying Additional Resource Files" in [this article](http://gettaurus.org/docs/Cloud/) for details on how to do this.
- **You may have uploaded a required file, but your test script still refers to it using a local file path**. (For example, a CSV Data Set Config element may still refer to a CSV file using a local path.) This is likewise explained in our guides on [Uploading Files](skill-blazemeter-performance-testing://references/scenarios.md) and [Shared Folders](skill-blazemeter-performance-testing://references/advanced-features.md).
- **You may have uploaded a required file, but the filename referenced in your script is in a different case than the filename of the one uploaded**. BlazeMeter engines run on Linux, which treats filenames as case-sensitive, so *Your_File_Name.csv* is a different file from *your_file_name.csv* or *Your_File_name.csv*.
- **You may have used a JMeter plugin but did not upload the plugin's JAR files**. BlazeMeter automatically includes most standard JMeter plugins, but some plugins must be uploaded with the test. Check the [logs report](skill-blazemeter-performance-testing://references/reporting.md) for any references to missing plugins.

### Network Issues

- **Your application server may only be accessible inside your local network**. If you see errors in your [Errors Report](skill-blazemeter-performance-testing://references/reporting.md) such as "connection refused", "socket closed", "connection timed out", "unknown host", 404 error codes, or similar errors, this means that even though your local machine (behind your internal network's firewall) can reach your application server, BlazeMeter's engines (outside of your firewall) cannot. Review our options for [Load Testing Behind Your Firewall](https://www.blazemeter.com/blog/top-three-options-running-performance-tests-behind-your-corporate-firewall).
- **If your application server returns connection errors** as mentioned in the above bullet, but BlazeMeter was able to establish some connections prior to the errors, then this is also indicative of a problem with either your application server or network. Unlike the above scenario, it may not necessarily be a firewall issue, but an issue with your server or network struggling with the load or frequency of connections, or some other internal server/network issue that results in only partial connectivity during the test.
- **You may be trying to test one of the [Websites Forbidden to Test Using BlazeMeter](https://help.blazemeter.com/docs/answers/answers-forbidden-domains.html).

### Load/Performance Issues

- **You may have been running your local test as a small-load test** (executing only a few threads/users), but the test you configured in BlazeMeter is a significantly higher-load test. If this is the case, depending on the type of test you're attempting to run, review our guide on [Calibrating a JMeter Test](skill-blazemeter-performance-testing://references/jmeter-configuration.md) or [Calibrating a Taurus Test](skill-blazemeter-performance-testing://references/taurus.md).
- **Please be aware that a local test run cannot be compared to a cloud run** because your local machine will have a very different allocation of CPU/memory/etc. than a cloud VPC.
- **If you're running a Selenium test**, be aware of our limitations on [using Selenium for load testing](skill-blazemeter-performance-testing://references/troubleshooting.md).

---

## Taurus Test Works Locally but Not in BlazeMeter

There are various reasons why a Taurus script that is working locally fails to run through BlazeMeter. Inspect the failed result and check the log file to identify the issues.

**Use when**: Troubleshooting Taurus tests that work locally but fail in BlazeMeter, resolving YAML configuration issues, or fixing file path and location configuration problems.

### Common Scenarios

Some of the common scenarios when a locally successful test fails to run in BlazeMeter are as follows:

- **You have not uploaded all the required data files** alongside the Taurus script in BlazeMeter.
- **The Taurus script includes an absolute path to a local CSV file** in the YML file. Replace it by a relative path.
- **You did not specify the "locations" parameter** (followed by a cloud location) in the YAML file. To get the list of available locations, run the following command: `bzt -locations -o modules.cloud.token=<API Key>`
- **You did not specify "provisioning: cloud"** when running the Taurus script from the command line. There is, however, no need to specify it when running the test from BlazeMeter UI.

---

## Debug Test: Low-Scale Test Run and Enhanced Logging

The Debug Test feature lets you validate your test configuration by creating a logical copy of your test and running it at a low-scale. The test will run with 10 threads and for a maximum of 5 minutes or 100 iterations, whichever occurs first. Any test initiated by clicking the **Debug Test** button is considered as free and will not charge a credit or VUH (Variable Unit Hour) for the test run.

**Use when**: Validating test configuration before full-scale runs, debugging test scripts, or troubleshooting test setup issues.

### Run a Debug Test

The data for **Debug Test** runs is deleted after 30 days.

Follow these steps:

1. In **Performance** tab, click **Tests**.
2. Select a test that you want to debug.
3. Click the **Debug Test** button.
4. Review the configuration and click **Start Debug Run**.

A low-scale test run is created. Use the test run to validate your configuration.

If you encounter the following error when starting a debug test, `Bad Request: Multiple scenarios are not supported in Debug mode.` see [Debug Tests Fails with "Multiple scenarios are not supported"](skill-blazemeter-performance-testing://references/troubleshooting.md) for more details.

### View Results of Debug Test Runs

Follow these steps:

1. Select a test.
2. Navigate to the **History** tab of the test configuration.
3. Select the **Debug** toggle.

You will see your Debug Test runs in **Reports**:

### View Detailed Request and Response Data

Detailed request and response information can be found in the **trace.jtl** file that is added to the artifacts.zip file for **Debug Test** runs.

The **Debug Test** runs do not appear in test trends, the **Reports** drop-down menu, or the **Show All Reports** lists. Also, they do not enforce or display a **Passed/Failed** status.

---

## Debug Test Multiple Scenarios

**Symptom:**

When attempting to execute a [Debug Test](skill-blazemeter-performance-testing://references/troubleshooting.md), you are met with this pop-up error message:

*Bad Request: Multiple scenarios are not supported in debug run*

**Use when**: Troubleshooting debug test failures with multiple scenarios error, resolving scenario configuration issues, or understanding debug test limitations.

### Reason

A 'Debug Test' only supports running with one engine. When executing a test, each scenario defined requires its own dedicated engine, which means that a 'Debug Test' likewise only supports running with one scenario.

### Solution

There are two ways in which your test may try to run more than one scenario:

- **If executing your test via a Taurus YAML configuration file**, you may have defined more than one scenario under the **execution:** section. Remove additional scenarios so that the YAML only executes one scenario.
- **You may have enabled [End User Experience Monitoring](skill-blazemeter-performance-testing://references/advanced-features.md)**. If so, this feature requires an additional engine, as the End User Experience (EUX) test is considered its own scenario apart from your main test scenario. This feature is not supported for Debug Tests, so make sure to disable it before running it in debug mode.

---

## Why are HTTP 200 OK Responses Counted as Errors?

**Symptom:** Performance Tests with a 200 response code are marked as failed in your Errors report.

**Reason:** This is not a mistake. BlazeMeter saves the Sample.jtl files in an XML format, as this is the correct way to store successful HTTP requests.

**Use when**: Understanding why HTTP 200 OK responses are marked as errors, troubleshooting assertion failures, or analyzing embedded resource errors.

### How JMeter Calculates Whether a Response is an Error or Not

A successful HTTP 200 OK HTTP request has `s="true"` which means it's successful. The `s=true` flag, followed by the `rc=200` assures us that the entire HTTP request was successfully completed.

### Assertion Errors

An HTTP request which is also a 200 OK but has a failed assertion will have `s="false"` even though `rc="200"`. A common scenario for these types of errors is a failed login, because although the request was processed successfully (that's why we got 200 OK) the credentials were false, and that's why the assertion failed the request.

Another scenario is a "Duration Assertion". If we won't accept a response time over 5s of a certain page, then we should apply a "Duration Assertion" to fail the request.

### Embedded Errors

An HTTP request can be 200 OK with no assertions, but the successful flag is still false (`s=false`). This means that JMeter was unable to retrieve one of the embedded resources (such as pictures, JavaScripts, CSS etc.) and marked the request as unsuccessful. For example, JMeter could not retrieve a jquery.js element and got 404 for it.

### Viewing Your Test's sample.jtl File

To view your test's sample.jtl file, download the ZIP of your test and extract it.

### Documentation References

For detailed information about HTTP 200 OK errors, use the BlazeMeter MCP help tools:

**HTTP 200 OK Errors**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-200-ok-errors`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-200-ok-errors"]}`

---

## Why Doesn't My Report Contain Data?

To generate a report, your test should last at least 1-5 minutes. Each dot in the chart represents one minute during the test. If the test duration is less than a minimum of 1 minute, the chart will not appear.

**Use when**: Troubleshooting reports with no data, understanding minimum test duration requirements, or resolving file naming issues.

### Common Causes

If you are getting a 'No Data For This Report' message, remove any spaces from your JMX file name and from any additional file you might have uploaded to BlazeMeter.

### Minimum Test Duration

Your test should last at least 1-5 minutes to generate a report. Each dot in the chart represents one minute during the test.

### Documentation References

For detailed information about reports with no data, use the BlazeMeter MCP help tools:

**No Data for Report**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-no-data-for-report`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-no-data-for-report"]}`

---

## Documentation References

For detailed information about performance test troubleshooting, use the BlazeMeter MCP help tools:

**Troubleshooting**:
- **Category**: `root_category`
- **Subcategory**: `guide` (for `performance-test-won-t-start`), `answers` (for other help_ids)
- **Help ID**: 
  - `performance-test-won-t-start` (test won't start) - subcategory: `guide`
  - `answers-high-response-time` (high response time) - subcategory: `answers`
  - `answers-performance-500-response` (500 response) - subcategory: `answers`
  - `answers-performance-partial-load` (partial load) - subcategory: `answers`
  - `answers-performance-selenium-versus-jmeter-load-testing` (Selenium vs JMeter) - subcategory: `answers`
  - `answers-performance-troubleshoot-jmeter` (JMeter works locally) - subcategory: `answers`
  - `answers-performance-troubleshoot-taurus` (Taurus works locally) - subcategory: `answers`
  - `answers-performance-debug-test-multiple-scenarios` (debug test) - subcategory: `answers`
  - `performance-200-ok-errors` (HTTP 200 OK errors) - subcategory: `guide`
  - `performance-no-data-for-report` (no data for report) - subcategory: `guide`
- **Read help**: 
  - For `performance-test-won-t-start`, `performance-200-ok-errors`, `performance-no-data-for-report`: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-test-won-t-start", "performance-200-ok-errors", "performance-no-data-for-report"]}`
  - For other help_ids: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-high-response-time", "answers-performance-500-response", "answers-performance-partial-load", "answers-performance-selenium-versus-jmeter-load-testing", "answers-performance-troubleshoot-jmeter", "answers-performance-troubleshoot-taurus", "answers-performance-debug-test-multiple-scenarios"]}`

