# Performance Testing Troubleshooting

## High Response Time

Diagnose and resolve high response time issues in performance tests, including comparing local vs cloud tests, different test scenarios, and location/provider differences.

**Use when**: Diagnosing and resolving high response time issues in performance tests, comparing local vs cloud tests, different test scenarios, or location/provider differences.

### Overview

High response times in performance tests can indicate various issues, from application performance problems to network latency or test configuration issues. Systematic diagnosis is required to identify the root cause.

**Important**: BlazeMeter is merely the messenger. BlazeMeter only reports these metrics as observed by the engine from the location or provider you selected. BlazeMeter does not in any way impact or interfere with these metrics; it only reports them. BlazeMeter has no control over response time, nor does BlazeMeter affect actual response times. (Service Virtualization can [Simulate Irregular Response Latencies](https://help.blazemeter.com/docs/guide/mock-service-think-time-irregular-response-latency.html) *in addition* to the response time.)

When you run a test from BlazeMeter, the system can only know how long it took your application server to respond; it doesn't know why it took as long as it did. This is often referred to as "waiting for a call back" - BlazeMeter can only report what it observes, not the root cause of the response time.

### Diagnostic Scenarios

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

### Solution

To find out why your application server took as long to respond to the test engines as it did, investigate your own server and network internally with the appropriate teams that can help you troubleshoot.

**Note**: The solution requires internal investigation of your server and network. BlazeMeter can only report the metrics it observes; it cannot diagnose why your application server took as long as it did to respond.

---

## 500 Response

Investigate and resolve HTTP 500 errors in performance tests, including checking application server logs and ensuring scripts run locally before cloud execution.

**Use when**: Investigating and resolving HTTP 500 errors in performance tests, checking application server logs, or ensuring scripts run locally before cloud execution.

### Overview

HTTP 500 errors indicate server-side errors. The HTTP server response 500 means "internal server error". This is a generic code that requires investigating in your application server itself to troubleshoot. On the BlazeMeter side, your server does not send us any additional information by which to know why it sent a 500 code.

**Note**: HTTP 500 errors will appear under the Errors tab of your report. These errors typically indicate a problem with your application server or test script, not with BlazeMeter itself.

### Investigation Steps

This error code usually does not point to a problem with BlazeMeter, but to a scripting problem. We recommend investigating this problem in two ways:

1. **Ensure your script can run in your local JMeter environment before running it through BlazeMeter**
2. **Investigate your application server, starting with your application server's logs**, to see why your server returned 500 codes during the time frame of the test

---

## Debug Test Multiple Scenarios

Resolve "Multiple scenarios are not supported" errors in debug tests by ensuring single scenario execution and disabling EUX monitoring.

**Use when**: Resolving "Multiple scenarios are not supported" errors in debug tests, ensuring single scenario execution, or disabling EUX monitoring.

### Overview

A 'Debug Test' only supports running with one engine. When executing a test, each scenario defined requires its own dedicated engine, which means that a 'Debug Test' likewise only supports running with one scenario.

### Solution

There are two ways in which your test may try to run more than one scenario:

1. **If executing your test via a Taurus YAML configuration file**, you may have defined more than one scenario under the **execution:** section. Remove additional scenarios so that the YAML only executes one scenario.

2. **You may have enabled [End User Experience Monitoring](https://help.blazemeter.com/docs/guide/performance-eux-monitoring.html)**. If so, this feature requires an additional engine, as the End User Experience (EUX) test is considered its own scenario apart from your main test scenario. This feature is not supported for Debug Tests, so make sure to disable it before running it in debug mode.

### Best Practices

- **Always Use Single Scenario**: Debug tests should always use single scenario
- **Disable EUX Monitoring**: EUX monitoring is not supported in debug tests
- **Test Locally First**: Test script locally before running debug test in cloud

---

## Partial Load

Diagnose and resolve partial load issues in performance tests caused by defunct engines or slow engine launches, including restarting sessions.

**Use when**: Diagnosing and resolving partial load issues in performance tests, troubleshooting defunct engines or slow engine launches, or restarting sessions.

### Overview

Partial load occurs when not all test engines start successfully or when some engines fail during test execution. This results in lower than expected load and can affect test results.

You can see the occurrence in the log files. Either the engine's log file will be missing (defunct), or there will be an error in the console log when trying to connect, or both. In case of a defunct engine, a message will appear in the test session dashboard.

### Reason

The cause is most likely that one of the engines was found defunct or it took too long to launch and the test has started without it. This is normal and can happen occasionally.

### Solution

In either scenario, we recommend restarting the session (press reboot). This solves the common scenario of the engine taking too long to launch.

---

## Selenium vs JMeter Load Testing

Understand when to use Selenium vs JMeter for load testing, including limitations, recommendations for user counts per engine, and multi-test strategies.

**Use when**: Understanding when to use Selenium vs JMeter for load testing, evaluating limitations, recommendations for user counts per engine, or multi-test strategies.

### Overview

Using Selenium for load testing is not recommended. Whereas JMeter is well suited for high-load performance tests, especially through BlazeMeter, Selenium is more suited for UI functional tests.

This is primarily because each "user" in a Selenium test runs through its own individual browser, which means if you're running 10 users on 1 engine, you are launching 10 web browsers simultaneously. Launching many multiple browser instances is a major CPU consumption per engine.

### Recommendations for Selenium Load Testing

For running Selenium tests on BlazeMeter, we recommend using [Taurus](https://gettaurus.org/docs/Selenium/) and starting with a maximum of 5 [users per engine](https://help.blazemeter.com/docs/guide/performance-taurus-configure-engines.html), then adjust accordingly as resources allow (which you can monitor via the Engine Health tab of your test report). Additional guidance on how to properly calibrate a test for best performance can be found in [Calibrating a Taurus Test](https://help.blazemeter.com/docs/guide/performance-taurus-calibration.html).

### Multi-Test Strategy

There is a way around the recommended five-user maximum, however: You can execute a [multi-test](https://help.blazemeter.com/docs/guide/performance-create-multi-test.html) in which each single test runs no more than five users each. You can add the single test multiple times to the multi-test. For example, if you wanted to test a fifteen-user load, you could create a multi-test that includes three instances of the single five-user test.

---

## Test Works Locally but Not in BlazeMeter

Resolve issues when JMeter tests work locally but fail in BlazeMeter, including missing files, network issues, load/performance problems, and forbidden domains.

**Use when**: Resolving issues when JMeter tests work locally but fail in BlazeMeter, troubleshooting missing files, network issues, load/performance problems, or forbidden domains.

### Overview

When JMeter tests work locally but fail in BlazeMeter, the issue is typically related to differences between local and cloud environments, such as missing files, network configuration, or resource constraints.

The first and the foremost thing you should do is check the errors found in your test's [Errors Report](https://help.blazemeter.com/docs/guide/performance-errors-report.html), then download and review the logs from your test's [Logs Report](https://help.blazemeter.com/docs/guide/performance-logs-report.html).

### Common Issues and Solutions

#### Missing Files

- **You may not have uploaded all files required to run your test script in BlazeMeter**. If your test script requires any additional files (CSVs, JARs, etc.), then refer to our guides on [Uploading Files](https://help.blazemeter.com/docs/guide/performance-upload-files.html) and [Shared Folders](https://help.blazemeter.com/docs/guide/performance-shared-folders.html)
- **If you submit your test from CLI (e.g. using the -cloud option)**, make sure your yml includes a *files:* section and list all files that are referenced in your script so they will be uploaded to the test. See section "Specifying Additional Resource Files" in [this article](http://gettaurus.org/docs/Cloud/) for details on how to do this
- **You may have uploaded a required file, but your test script still refers to it using a local file path**. (For example, a CSV Data Set Config element may still refer to a CSV file using a local path.) This is likewise explained in our guides on [Uploading Files](https://help.blazemeter.com/docs/guide/performance-upload-files.html) and [Shared Folders](https://help.blazemeter.com/docs/guide/performance-shared-folders.html)
- **You may have uploaded a required file, but the filename referenced in your script is in a different case than the filename of the one uploaded**. BlazeMeter engines run on Linux, which treats filenames as case-sensitive, so *Your_File_Name.csv* is a different file from *your_file_name.csv* or *Your_File_name.csv*
- **You may have used a JMeter plugin but did not upload the plugin's JAR files**. BlazeMeter automatically includes most standard JMeter plugins, but some plugins must be uploaded with the test. Check the [logs report](https://help.blazemeter.com/docs/guide/performance-logs-report.html) for any references to missing plugins

#### Network Issues

- **Your application server may only be accessible inside your local network**. If you see errors in your [Errors Report](https://help.blazemeter.com/docs/guide/performance-errors-report.html) such as "connection refused", "socket closed", "connection timed out", "unknown host", 404 error codes, or similar errors, this means that even though your local machine (behind your internal network's firewall) can reach your application server, BlazeMeter's engines (outside of your firewall) cannot. Review our options for [Load Testing Behind Your Firewall](https://www.blazemeter.com/blog/top-three-options-running-performance-tests-behind-your-corporate-firewall)
- **If your application server returns connection errors as mentioned in the above bullet, but BlazeMeter was able to establish some connections prior to the errors**, then this is also indicative of a problem with either your application server or network. Unlike the above scenario, it may not necessarily be a firewall issue, but an issue with your server or network struggling with the load or frequency of connections, or some other internal server/network issue that results in only partial connectivity during the test
- **You may be trying to test one of the [Websites Forbidden to Test Using BlazeMeter](https://help.blazemeter.com/docs/answers/answers-forbidden-domains.html)**

#### Load/Performance Issues

- **You may have been running your local test as a small-load test (executing only a few threads/users), but the test you configured in BlazeMeter is a significantly higher-load test**. If this is the case, depending on the type of test you're attempting to run, review our guide on [Calibrating a JMeter Test](https://help.blazemeter.com/docs/guide/performance-jmeter-calibration.html) or [Calibrating a Taurus Test](https://help.blazemeter.com/docs/guide/performance-taurus-calibration.html)
- **Please be aware that a local test run cannot be compared to a cloud run** because your local machine will have a very different allocation of CPU/memory/etc. than a cloud VPC
- **If you're running a Selenium test**, be aware of our limitations on [using Selenium for load testing](https://help.blazemeter.com/docs/answers/answers-performance-selenium-versus-jmeter-load-testing.html)

---

## Taurus Test Works Locally but Not in BlazeMeter

Resolve issues when Taurus tests work locally but fail in BlazeMeter, including missing data files, absolute paths, location parameters, and provisioning settings.

**Use when**: Resolving issues when Taurus tests work locally but fail in BlazeMeter, troubleshooting missing data files, absolute paths, location parameters, or provisioning settings.

### Overview

Taurus tests that work locally may fail in BlazeMeter due to differences in file paths, data file handling, location configuration, or provisioning settings. Inspect the failed result and check the log file to identify the issues.

### Common Issues and Solutions

Some of the common scenarios when a locally successful test fails to run in BlazeMeter are as follows:

- **You have not uploaded all the required data files alongside the Taurus script in BlazeMeter**
- **The Taurus script includes an absolute path to a local CSV file in the YML file**. Replace it by a relative path
- **You did not specify the "locations" parameter (followed by a cloud location) in the YAML file**. To get the list of available locations, run the following command: `bzt -locations -o modules.cloud.token=<API Key>`
- **You did not specify "provisioning: cloud" when running the Taurus script from the command line**. There is, however, no need to specify it when running the test from BlazeMeter UI

---

## Test Won't Start

Troubleshoot issues when performance tests fail to start, including configuration errors, resource availability, and test validation issues.

**Use when**: Troubleshooting issues when performance tests fail to start, checking configuration errors, resource availability, or test validation issues.

### Overview

When a performance test fails to start, it's typically due to configuration errors, resource unavailability, or test validation failures. Systematic troubleshooting is required to identify and resolve the issue.

### Common Causes

- **Configuration Errors**: Invalid test configuration
- **Resource Unavailability**: Insufficient resources at selected location
- **Test Validation Failures**: Test script validation errors
- **Location Issues**: Selected location unavailable or misconfigured

### Troubleshooting Steps

1. **Review Test Configuration**:
   - Check test configuration for errors
   - Verify all required fields are filled
   - Ensure configuration is valid

2. **Check Resource Availability**:
   - Verify resources available at selected location
   - Check location capacity
   - Try different location if needed

3. **Validate Test Script**:
   - Review test script for errors
   - Verify script format is correct
   - Check script dependencies

4. **Review Error Messages**:
   - Check error messages in test execution
   - Look for specific validation errors
   - Address errors identified

### Solutions

- **Fix Configuration**: Correct any configuration errors
- **Select Different Location**: Try different test location
- **Fix Test Script**: Correct any script errors
- **Contact Support**: If issues persist, contact BlazeMeter support

---

## Documentation References

For detailed information about performance testing troubleshooting, use the BlazeMeter MCP help tools:

**High Response Time**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-high-response-time`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-high-response-time"]}`

**500 Response Errors**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-performance-500-response`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-performance-500-response"]}`

**Debug Test Issues**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-performance-debug-test-multiple-scenarios`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-performance-debug-test-multiple-scenarios"]}`

**Partial Load**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-performance-partial-load`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-performance-partial-load"]}`

**Selenium vs JMeter Load Testing**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-performance-selenium-versus-jmeter-load-testing`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-performance-selenium-versus-jmeter-load-testing"]}`

**Test Works Locally but Not in BlazeMeter (JMeter)**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-performance-troubleshoot-jmeter`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-performance-troubleshoot-jmeter"]}`

**Taurus Test Works Locally but Not in BlazeMeter**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-performance-troubleshoot-taurus`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-performance-troubleshoot-taurus"]}`

**Performance Test Won't Start**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-test-won-t-start`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-test-won-t-start"]}`

