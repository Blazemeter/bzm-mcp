# GUI Functional Tests

## Overview

Understand GUI Functional Testing overview, including scriptless test creation, YAML file upload, IDE-based test creation, test execution settings (location, browser, virtual services), and test suites/cases concepts.

**Use when**: Understanding GUI Functional Testing overview or learning about scriptless test creation, YAML file upload, IDE-based test creation, test execution settings, and test suites/cases concepts.

### Overview

A GUI Functional Test provides a means of testing your GUI's functionality via Selenium on the cloud, which in turn generates a robust report that will allow you to review how your test performed step-by-step, even providing a recorded video of your test as it executed in the engine's web browser!

You create and [run](https://help.blazemeter.com/docs/guide/functional-test-run.html) your GUI Functional test, and then you review your [GUI Functional Test Report](https://help.blazemeter.com/docs/guide/functional-gui-test-report.html).

This article is an overview of your test creation options that leads you to more details articles below.

### Create a Scriptless Test

You as tester or subject matter expert can create a GUI Functional Test even without writing any code, by creating a "scriptless" test. This means you create and edit tests by dropping predefined actions and objects into a test scenario. (It's "scriptless" in that *you* don't have to write the script; BlazeMeter automatically generates the script behind the scenes!)

This approach relies on the provided [Taurus Actions for GUI Functional Testing](https://help.blazemeter.com/docs/guide/functional-taurus-actions-scriptless.html), and your custom [Test Action Library](https://help.blazemeter.com/docs/guide/functional-test-action-library.html). You can also use the [BlazeMeter Chrome Extension](https://help.blazemeter.com/docs/guide/recorders-blazemeter-chrome-extension.html) to record a test and edit it in the scenario editor later.

For more details, refer to our guide on [Creating Scriptless GUI Functional Tests](https://help.blazemeter.com/docs/guide/functional-create-scriptless-test.html).

### Create a Test By Uploading a Taurus YAML Script

Another way how you as a tester can create a GUI Functional Test requires uploading your own [Taurus](https://gettaurus.org/) YAML configuration files. All Selenium commands must be executed within said YAML file (as opposed to referencing an external Selenium script file). This is the simplest method for executing a BlazeGrid test.

You can either write your own YAML configuration file from scratch, or you can use the [BlazeMeter Chrome Extension](https://help.blazemeter.com/docs/guide/recorders-blazemeter-chrome-extension.html) to automatically generate the file for you.

For more details, check out our guide on [Creating a GUI Test by Uploading a YAML File](https://help.blazemeter.com/docs/guide/functional-gui-create-yaml-file.html).

### Create a Test from Your IDE

If you as a developer prefer to execute a Selenium Java or Python script, you can do so by modifying your script to communicate with BlazeMeter, then execute the script from your local integrated development environment (IDE), which will in turn automatically create a BlazeGrid test on the cloud.

We have two guides to choose from:
- [Creating a GUI Test from a Java IDE](https://help.blazemeter.com/docs/guide/functional-gui-test-create-from-java-ide.html)
- [Creating a GUI Test from a Python IDE](https://help.blazemeter.com/docs/guide/functional-gui-test-create-from-python-ide.html)

### Set Up Test Execution Settings

- **Location:** You can choose a public Cloud location, or a private location for test execution. For more information, see [Cloud vs Private Location](https://help.blazemeter.com/docs/guide/private-locations-vs-cloud.html) and [Get the Location Name](https://help.blazemeter.com/docs/guide/api-get-the-location-name.html). The choice of location determines which browsers are available. **Important**: Functional tests don't run on Private Locations that have more than one agent. To run Functional tests, ensure you have only a single agent assigned.
- **Browser:** For a test that has a location assigned, you can choose browser and browser version. For more information, see [Supported browsers](https://help.blazemeter.com/docs/guide/functional-supported-browsers.html). Each test can be run in multiple browsers and multiple versions. By default, and if no location is selected, the test runs in the latest Chrome browser. If you have [created a private location](https://help.blazemeter.com/docs/guide/private-locations-create.html) that has custom browsers and versions configured, you can select additional browsers. For each choice of browser and version, you can choose to record a video of the test execution as part of the test report. By default, video recording is enabled.
- **Virtual Services Configuration:** If you have created a [virtual services configuration](skill-blazemeter-service-virtualization://references/introduction.md), you can assign it to this test.

### Run Grid Proxy over HTTPS

Grid Proxy enables you to run Selenium functional tests in BlazeMeter without using a local server. You can run Grid Proxy over the HTTPS protocol.

**Use when**: Running Grid Proxy over HTTPS for Selenium functional tests, configuring SSL certificates for Grid Proxy, or setting up secure connections for functional tests.

### Overview

You can run Grid Proxy over the HTTPS protocol using either of the following methods:

- **blazemeter.bzmGridProxyScheme**: The default value is 'http'. To run over HTTPS, set this value to 'https'.
- **blazemeter.bzmGridProxyDomain**: This method specifies the domain on which the proxy server is running. If blazemeter.bzmGridProxyScheme is set to 'https', you must provide the domain. If not provided, the proxy server will not start and will fail with a relevant error message.

### Prerequisites

- Selenium scripts include both the **blazemeter.bzmGridProxyScheme** and **blazemeter.bzmGridProxyDomain** methods.
- **SSL Certificates**: Users must provide their own custom SSL certificate and key. BlazeMeter does not provide any default certificates.
- **Domain**: Users must generate and provide a domain for Grid Proxy. BlazeMeter does not provide a default domain.

### Example Configuration

**Python Example:**
```python
bzm_options = {
    "blazemeter.reportName": REPORT_NAME,
    "blazemeter.apiKey": API_KEY,
    "blazemeter.apiSecret": API_SECRET,
    "blazemeter.buildId": BUILD_ID,
    "blazemeter.locationId": HARBOR_ID,
    "blazemeter.projectId": PROJECT_ID,
    "blazemeter.videoEnabled": "True",
    "blazemeter.sessionName": SESSION_NAME,
    "blazemeter.bzmGridProxyScheme": 'https',
    "blazemeter.bzmGridProxyDomain": "example.com",
}
```

### Private Location Configuration

You can run Grid Proxy over HTTPS in Docker and Kubernetes private locations. For more information, see:
- [Configure a Docker Installation to Use CA Bundle for Grid Proxy](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-docker-installation-to-use-ca-bundle.html#Configur)
- [Configure a ConfigMap for Grid Proxy](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-kubernetes-agent-to-use-ca-bundle.html#Configur)

### Documentation References

For detailed information about running Grid Proxy over HTTPS, use the BlazeMeter MCP help tools:

**Run Grid Proxy over HTTPS**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-run-gridproxy-over-https.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-run-gridproxy-over-https.htm"]}`

---

### GUI Test Desired Capabilities Options

To execute on the BlazeMeter cloud directly from your IDE, BlazeMeter has custom capabilities that you pass into a Webdriver session through a Desired Capabilities class. You can enable and configure various optional settings by referring to them via this dictionary.

**Use when**: Configuring custom capabilities for GUI Functional Tests executed from IDE or setting up test execution options like project ID, test ID, location, video recording, etc.

BlazeMeter supports Selenium 4.1.3 and 4.1.4 and higher. For 4.1.3, a *desired_capabilities{}* dictionary is required for a Python Selenium script; a *DesiredCapabilities()* Java object is required for a Java Selenium script. For 4.1.4 or higher, a *browser_options{}* dictionary is required for a Python Selenium script; and a *bzmOptions* HashMap for a Java Selenium script.

#### Available Options

- **platformName** - which platform to use (windows/linux).
- **browserName** - which browser the test will run on. Accepted values are "chrome", "firefox", "MicrosoftEdge" and "safari". Apart from "MicrosoftEdge", remember to input all other browser names in lowercase.
- **browserVersion** - what specific version of the browser to use.
- **blazemeter.projectId** - if you want to add your test to some existing BlazeMeter project. If the ID is wrong, the test will not launch, and you'll get an error.
- **blazemeter.buildId** - if you run tests in parallel in several browser sessions at a time (several Webdriver instances in parallel), use this ID to group sessions in the report. If the buildId is not provided in the Desired Capabilities, then a unique buildId is recorded for each session, and every session appears in a separate report. Set the buildID in each script to a string of your choice (for example, a timestamp in milliseconds) to have sessions with the same buildId appear in the same BlazeMeter report.
- **blazemeter.testId** - if you want to attach your report to an existing test, add its Test ID. If the ID is wrong, the test will not launch, and you'll get an error. (Remember: the chosen test must be a Functional GUI Test.)
- **blazemeter.testName** - if you want to attach your report to an existing test, add its testName. If the name does not exist, a new test is created. If the test name exists, but it's not a Functional GUI Test, the test will not launch, and you'll get an error.
- **blazemeter.reportName** - you may name your report, which you'll then see in the Reports drop-down menu and on the dashboard.
- **blazemeter.sessionName** - you may name the session, which will then appear in the drop-down menu in the upper-right corner of the test report.
- **blazemeter.sessionTimeout** - default value is 300 seconds. If you expect a gap between commands in your test is more than 300 seconds, you may need to increase this value (to a maximum 1200 seconds).
- **blazemeter.locationId** - you may use the [Location ID (aka Location Name)](skill-blazemeter-api-reference://references/overview.md) of one of the available BlazeMeter locations or your own [private location](skill-blazemeter-private-locations://references/introduction.md). To see the list of available locations, create a new GUI Functional Test in the UI, upload a YAML file, and review the options available that appear when you click the "Select test location" drop-down menu.
- **blazemeter.videoEnabled** - whether you want video enabled on your test report (true or false).

#### Default Capabilities

Below is list of selenium capabilities that we set by default (we will use your value in case you will pass same capability from your script):

- **acceptInsecureCerts** - to allow testing apps with self signed (untrusted) certificates.

To see all available browsers, use the API [https://a.blazemeter.com/api/v4/grid/capabilities](https://a.blazemeter.com/api/v4/grid/capabilities). The API outputs only apply to the available browserName and browserVersion options.

### Parameterize Tests (Taurus YAML Scripts)

In GUI functional testing, sometimes you may want to parameterize your test to use external data instead values hard-coded in the test body. You can upload a CSV file with comma-separated data that you want to inject into your test. The file must have the .csv suffix.

**Use when**: Parameterizing test data in a Taurus YAML script or using external CSV data instead of hard-coded values in GUI Functional Tests.

This article covers parameterizing test data in a Taurus YAML script. Alternatively, you can also [Parameterize Test Data in Scriptless Tests](skill-blazemeter-test-data://references/core-concepts.md).

#### Process

1. **Create data-provider file**: Create a CSV file with comma-separated data. The first row represents the names of parameters, the following rows are the values for the parameters.
2. **Upload file to BlazeMeter**: Attach the CSV file to a test in BlazeMeter. Open the Test Configuration, switch the test to **Script Mode**, and click the blue **plus** button.
3. **Refactor the test to use data from the file**:
   - Set the "iterations" parameter to 0, which means do as many iterations as there are rows of data in the file.
   - Link the scenario to the data-provider file as data source: `data-sources: - params.csv`
   - Replace hard-coded values in test steps by Data Parameters: `${fromPort}`, `${toPort}`, etc.
4. **Run the test**: The test is executed multiple times, each time with different data (1 iteration = 1 row of data). Each iteration is executed in a separate session of the web driver.

**Note**: If test data is defined in the YAML file, and you open the Test Data pane, the pane will be read-only, and it indicates that the test data is defined in the YAML file. You will not be able to use the Test Data pane to edit, rename, or delete test data within the BlazeMeter web UI, nor can you add parameters through the pane. To make changes to test data and settings, edit the YAML file directly.

### Using Test Data in GUI Functional Tests

Your goal is to replace hard-coded parameter values in test steps with dynamic test data. For example, you replace the static address that you typed in during the recording by the parameter `${address}`; and then provide dynamic address data for that value. You can use one or combine multiple of these data sources in a test, CSV files or synthetic data, as needed.

**Use when**: Using test data in GUI Functional Tests or replacing hard-coded values with dynamic test data from CSV files or synthetic data generation.

#### Define Test Data Parameters

A Data Entity is a container for Data Parameters. A Data Parameter is a dynamic value such as a date, name, address, credit card number, that you want to use in a test instead of hard-coded values. You reference these values in test steps as `${date}`, `${name}`, `${address}`, `${creditcardnumber}`, and so on.

1. Go to the BlazeMeter **Functional** tab and open a GUI Functional Test configuration.
2. Click **Test Data**. The Test Data pane opens on the right side.
3. Click the **Plus** button to add one or more Data Entities. See the respective specific article for details:
   - [Generate synthetic data parameters](skill-blazemeter-test-data://references/generation.md)
   - [Load test data from a CSV file](skill-blazemeter-test-data://references/core-concepts.md)

#### Use Data in GUI Functional Tests

After you have loaded or defined test data, you use it in your test. For more information, see [How to Use Test Data](skill-blazemeter-test-data://references/core-concepts.md).

1. Go to the BlazeMeter **Functional** tab and open your GUI Functional Test configuration that has test data parameters defined.
2. Open the **Test Data** pane, go to each data parameter, and click **Copy parameter name to clipboard**.
3. Return to the test steps and replace hard-coded values by pasting the copied parameter name.

#### Define Iteration Settings for GUI Functional Tests

When attaching test data, the number of rows in the CSV files determines the number of test iterations that will be executed. But in a GUI Functional test's configuration, you can also manually control how many rows of data are used, by opening the **Test Data** pane and clicking **Iterations**.

For more information about Run Options, see [How to Control the Number of Rows Used - Test Data Iteration Settings](skill-blazemeter-test-data://references/management.md).

#### Preview Test Data

Previewing your test data is helpful when you are combining data from multiple files, or generating synthetic test data, so you can review values in context.

1. Open a GUI Functional Test with test data attached.
2. Verify that at least one data parameter is defined to be able to generate the data preview.
3. Click **Test Data**, **Iterations**. The Test Iteration Settings window opens and shows the data preview.

#### Manage Test Data

Open a GUI Functional Test and click **Test Data** to open the Test Data pane. Each GUI Functional test can currently have one data entity attached, which can contain a mix of CSV files and synthetic Test Parameters.

Any team member can save their data entity to the Workspace to share it, and load saved entities into their tests. For more information about managing shared test data, see [How to Share Test Data](skill-blazemeter-test-data://references/management.md) and [How to Use Test Data](skill-blazemeter-test-data://references/core-concepts.md).

### What Are Test Suites and Test Cases?

On the Test Creation screen, you can optionally organize your tests into test suites. Here, we will clarify what is meant by "test cases" and "test suites".

A **test case** is a set of one or more steps. For example, the steps to navigate to a URL, fill out a form, and click a button may be organized into a single test case. In the example test report below, we have a test case named "Homepage" that consists of one step, which is navigating to the URL specified.

A **test suite** is a collection of test cases. You may have one or more test cases in a test suites. The same test case can be associated with several test suites. In the following example, the test case goes to the homepage again, only this time we have designated it as the second test case inside a test suite. In the screenshot, the test suites are named "BlazeDemo Website 1" and "BlazeDemo Website 2".

These report examples show that "pass" messages are highlighted in green and "fail" messages in red.

---

## Creating Scriptless Functional Tests

You can create and edit GUI Functional Tests manually by dropping pre-defined Actions and Objects into a Test Scenario. This scriptless test creation approach is the preferred method for testers who do not want to write and upload scripts manually. Every time you change the building blocks, the Taurus script behind the scenario editor is updated, and you can immediately run the test.

**Use when**: Creating and editing GUI Functional Tests manually using scriptless approach, dropping pre-defined Actions and Objects into test scenarios, or recording tests with Chrome Extension and editing them in the scenario editor.

### Overview

[Record scriptless GUI Functional Tests](skill-blazemeter-recorders://references/chrome-extension.md) using the [BlazeMeter Recorder Extension](skill-blazemeter-recorders://references/chrome-extension.md). Advanced users can also choose to use the integrated [Debugger](skill-blazemeter-functional-testing://references/debugging.md) to troubleshoot Scriptless tests.

To edit Scriptless GUI Functional Tests, you need to understand the following concepts: [Objects](skill-blazemeter-functional-testing://references/action-library.md) (GUI elements such as buttons and fields), [Actions](skill-blazemeter-functional-testing://references/gui-tests.md) (such as click or select) and Groups.

### How to Create a Scriptless Test Manually

1. Ensure you have the "Functional" tab selected
2. Click the "Create Test" button near the top-center of the screen
3. Select a project
4. Click the "GUI Functional Test" button to create a new test
5. Under Configuration, Test Definition, click the Pencil button to give the test scenario a name
6. Define your Scriptless test in one of the following ways:
   - **Record Test Scenarios in Chrome**: Verify that you have the BlazeMeter Extension installed. Click **Start UI Recorder** on an empty canvas. A new browser window opens. The Chrome extension opens. Open your web app and perform your test steps. When you're done, click **Stop Recording** in the Chrome Extension. The recorded test opens in the Scriptless Scenario Editor
   - **Build Test Scenarios out of building blocks**: Drag Actions from the **Groups** and **Actions** tabs and drop them onto the scenario canvas. For each Action, define step name, target object, and values
7. Click the **Debug Test** button to do a test run. A test run does not count against the metrics
8. Click the **Run Test** button to execute your test

### Scriptless Scenario Creation Tips

- To reorder steps, drag them to new locations in the scenario list
- To remove a step from the scenario, click the trash can button
- To create an editable copy, click the **Duplication** button
- To find Objects, Actions, and Groups by name, use the search box
- To view the appearance of the Object in the user interface, click the **Screenshot** button

### Create Objects

Objects are GUI elements in your system under test, such as text fields and buttons. When you start a new project, your Object list is empty. You manage Objects from the [Test Action Library](skill-blazemeter-functional-testing://references/action-library.md) tab. To create an Object, you must provide a unique way to locate the element in the DOM.

You can create Objects by using any of the following methods:
- Let the [BlazeMeter Chrome Extension](skill-blazemeter-recorders://references/chrome-extension.md) record and create Objects automatically
- Use the Object Picker to change an existing object
- Create Objects manually from the test definition window

**Manually create Objects:**
1. Add an Action to the scenario
2. In the **Object** box, click **Create New Object**
3. Define an object name
4. In the **Locator** list, click one or more of the following types: By CSS Class, By ID, By Name, By Xpath
5. In the **Value** field, define the locator as a text string. For example, you can enter the object ID
6. Click **Create**

The Object is added to the Object library for this project and can be used in this test.

### Edit Objects

From the Test Action Library, you can edit only the name and description of Objects. Editing other Object properties impacts scenarios in ways that require debugging and validation, which can be done only when the Object is used in the context of a scenario.

1. Find the Object inside a step in the Scenario Editor and click the step to select it. Use the [Test Action Library](skill-blazemeter-functional-testing://references/action-library.md) to find where the Object is used if you cannot find it in a Scenario
2. Click the **Edit Object** button (pencil icon) and modify locators manually, or click the **Object Picker** button (arrowhead in square icon) and then click an object in the web app under test
3. (Optional) Expand and review the revision history of the Object. The change log contains the time of the edit, who made the change, and a change note
4. Make any additional changes and save the updates
5. Debug your test to verify results
6. (Optional) To save your changes to the shared Test Action Library, click **Override Group Action**

### Define Scenario Steps

You create scenario steps out of Actions, Objects, and parameter values.

The [Taurus Actions](skill-blazemeter-functional-testing://references/gui-tests.md) are a predefined set. You cannot create new Actions. Available Actions include assertions, clicking buttons, selecting dropdown items, entering text, pausing, submitting a form, opening URLs, and many more.

For each scenario step, you can define a name, an Action, an Object, and values. In a test step such as clicking a button, or typing text into a form field, an Action is applied to an Object. Use the **Object** menu to search the project for existing Objects or to record new Objects, such as buttons.

Lastly, in the **Value** field, define any applicable values. A value can be, for example, a name to enter into a form field, a postal code number, a time selected from a selector, a URL, and more. Not all actions require values.

### Create Groups

A custom Group contains multiple Actions that occur together in a given order. For example, you can create a custom "Login" Group that contains a sequence of three Actions, "Enter User ID," "Enter Password," "Click Submit."

Groups are useful because they can be shared, but the use of groups is not mandatory to create scenarios. You add Groups to a scenario in the same way as you add single Actions.

To create a Group directly from the Test Definition, drag a sequence of Actions into the Scenario Editor, and select their check boxes. The selected steps must be consecutive without gaps. Then enter a name for the Group and click **Save As Group Action**.

You can nest Groups inside other Groups, but you will not be able to drill down and edit nested Groups directly in the Scenario Editor.

### Edit Groups

From the Test Action Library, you can edit only the name and description of a Group. You edit the Actions, Objects, and values inside a Groups from the Scenario Editor. Such local changes are automatically saved only in the current scenario.

You can overwrite the values of the original Group in the Test Action Library, or choose to save your changes as a new Group in the Test Action Library.

1. Find the Group in the Scenario Editor and expand it. If you cannot find the Group in the Scenario, use the [Test Action Library](skill-blazemeter-functional-testing://references/action-library.md) to find where the Group is used
2. Click the Edit button (pencil icon) to edit elements of the Group
3. Debug your test to validate your changes
4. (Optional) Click **Override Group Action** to save your changes to the shared Test Action Library

---

## Create YAML File

If you opt to use a Taurus YAML file to execute your Selenium test, you can simply upload the file to BlazeMeter, then execute your test.

**Use when**: Creating GUI Functional Tests by uploading Taurus YAML files or configuring script mode, file upload, test execution settings, and YAML validation.

### Upload Process

**To upload a YAML test file, do the following:**

1. Select the "Functional" tab
2. Click the "Create Test" button near the top-center of the screen
3. Select a project
4. Click the "GUI Functional Test" button to create a new test
5. Click **</> Script Mode**. A dialog advises you not to switch back to **↯ UI mode** if you intend to use your uploaded file
6. Drag your YAML file over the "Upload Script" area, or click the "**+**" button to select a YAML file to upload. All Selenium commands must be within the YAML script itself. For this method, the YAML cannot reference a Selenium script file
7. Review the test. Your YAML configuration appears in the **Scenario Definition** pane. Any values that are defined in the YAML file appear read-only in the **Test Data** pane
8. Click the "Run Test" button to execute your test

### Test Execution Settings

- **Location:** You can choose a specific public Cloud or private location to run the test. For more information, see [Cloud vs Private Location](skill-blazemeter-private-locations://references/introduction.md) and [Get the Location Name](skill-blazemeter-api-reference://references/identifiers.md)
- **Browser:** By default, the test runs in the latest Chrome browser. If you have [created a private location](skill-blazemeter-private-locations://references/introduction.md) that has other browsers and versions configured, you can select specific browsers in which to run the test. For more information, see [GUI Functional Testing - Supported Browsers](skill-blazemeter-functional-testing://references/browsers.md)
- **Virtual Services Configuration:** If you have created a [virtual services configuration](skill-blazemeter-service-virtualization://references/introduction.md), you can assign it to this test

---

## Create from Java IDE

If you as a Java developer prefer to use your own Selenium script instead of a YAML configuration file, you can do so by modifying your script to automatically create a BlazeGrid test when executed from your local Java IDE.

**Use when**: Creating GUI Functional Tests from Java IDE using Selenium or setting up BlazeMeter authentication, desired capabilities configuration, connection setup, test suites/cases, and automatic report launching.

### Overview

Here we will outline required modifications. For the purpose of this guide, all examples here will assume a Selenium script written in Java, though [Selenium scripts in Python](skill-blazemeter-functional-testing://references/gui-tests.md) are also supported. BlazeMeter supports Selenium 4.1.3 and 4.1.4 or higher.

To see a sample JUnit script with these features in action, please check out our [example script](https://github.com/Blazemeter/GUI-Functional-Test-Examples/tree/master/java/junit4) located in our [BlazeMeter GitHub repository](https://github.com/Blazemeter).

**Note**: Whereas this guide's purpose is to advise how to add BlazeMeter functionality to your own existing script, please be aware that BlazeMeter Support does not provide scripting assistance.

### Step 1: Setup BlazeMeter Authentication

Set values for the variables *base* (the URL to BlazeMeter), *API_KEY*, and *API_SECRET* to ensure an authenticated connection to your BlazeMeter account. (For more information on how to find or generate your API key, see [BlazeMeter API keys](skill-blazemeter-api-reference://references/authentication.md).)

```java
private final static String API_KEY = "{your API key}";
private final static String API_SECRET = "{your secret key}";
private final static String BASE = "a.blazemeter.com";
private final static String curl = String.format("https://%s/api/v4/grid/wd/hub", BASE);
```

**Note**: You may have noticed that the handling of API keys is considerably different in this guide's example compared to the example provided in the Python guide. This is because the Selenium library for Java uses Java's HTTP Client, which does not support HTTP authentication; instead, the keys must be passed via `DesiredCapabilities()`, as explained in the next step.

### Step 2: Configure BlazeMeter Features

You can specify a variety of settings that enable optional features or specify certain configurations. For a full list of what can be included in this dictionary, please see our [GUI Test "Desired Capabilities" Options](skill-blazemeter-functional-testing://references/gui-tests.md) reference guide.

For Selenium 4.1.3, `DesiredCapabilities()` is a Java object that stores key/value pairs for various browser properties. Use this object to specify the various GUI Functional Test features you want to enable for your script:

```java
DesiredCapabilities capabilities = new DesiredCapabilities();
capabilities.setCapability("blazemeter.apiKey", API_KEY);
capabilities.setCapability("blazemeter.apiSecret", API_SECRET);
capabilities.setCapability("blazemeter.reportName", "Demo Grid test");
capabilities.setCapability("blazemeter.sessionName", "Chrome browser test");
capabilities.setCapability("browserName", "chrome");
```

For Selenium 4.1.4 and higher, wrap the blazemeter.* parameters inside a bzmOptions HashMap:

```java
ChromeOptions browserOptions = new ChromeOptions();
browserOptions.setBrowserVersion("default");
Map<String, Object> bzmOptions = new HashMap<>();
bzmOptions.put("blazemeter.apiKey", API_KEY);
bzmOptions.put("blazemeter.apiSecret", API_SECRET);
bzmOptions.put("blazemeter.reportName", "Demo Grid test");
bzmOptions.put("blazemeter.sessionName", "Chrome browser test");
browserOptions.setCapability("bzm:options", bzmOptions);
```

### Step 3: Configure BlazeMeter Connection

To ensure your script connects to and runs on BlazeMeter with all the features you specified, simply configure your remote web driver to connect to BlazeMeter with the capabilities you defined previously:

```java
URL url = new URL(curl);
driver = new RemoteWebDriver(url, capabilities);
```

You can actually stop here if you like, as you've now implemented the minimum requirements to run your test on BlazeMeter -- it IS that easy! However, you may want to add some additional features to further tweak how your test will appear in BlazeMeter, in which case, continue reading below.

### Step 4: Setup Test Suites & Test Cases

You can optionally designate BlazeMeter test suites and test cases in your script. (If you opt not to, your test will appear in the report under "Default Test Suite" and "Default Test Case".)

Basically each class will serve as a test suite and each test method within a class will serve as a test case.

To demonstrate, let's create a very basic one-command test like so:

```java
public class blazegrid_java {
    @Test
    public void myTestCase() {
        driver.get("http://blazedemo.com");
    }
}
```

To assign our own suite and case names, we can utilize JUnit's [TestRule](https://junit.org/junit4/javadoc/4.12/org/junit/rules/TestRule.html) class ([TestName](https://junit.org/junit4/javadoc/4.12/org/junit/rules/TestName.html), specifically) to set the suite name to our class name and the case name to our test method by utilizing a hash map and JUnit's Runner [Description](https://junit.org/junit4/javadoc/4.12/org/junit/runner/Description.html) class:

```java
@Rule
public final TestName bzmTestCaseReporter = new TestName() {
    @Override
    protected void starting(Description description) {
        Map<String, String> map = new HashMap<>();
        map.put("testCaseName", description.getMethodName());
        map.put("testSuiteName", description.getClassName());
        driver.executeAsyncScript("/* FLOW_MARKER test-case-start */", map);
    }
};
```

The last line in the above sample uses `executeAsyncScript()` to mark the beginning of the test case.

### Step 5: Add Pass/Fail/Broken Statuses

Another optional feature you can add is pass/fail status reporting. (If you opt not to perform this step, all statuses will default to a blue "Undefined" in the test report.)

In the following example, we added a method inside our TestName object that sets a "success" message before a test case stops:

```java
@Override
protected void succeeded(Description description) {
    if (driver != null) {
        Map<String, String> map = new HashMap<>();
        map.put("status", "success");
        map.put("message", "");
        driver.executeAsyncScript("/* FLOW_MARKER test-case-stop */", map);
    }
}
```

We can also add another method to manage "failed" and "broken" messages. This method will kick in if a test method fails an assertion, resulting in either a "failed" or "broken" status depending on the outcome:

```java
@Override
protected void failed(Throwable e, Description description) {
    Map<String, String> map = new HashMap<>();
    if (e instanceof AssertionError) {
        map.put("status", "failed");
    } else {
        map.put("status", "broken");
    }
    map.put("message", e.getMessage());
    driver.executeAsyncScript("/* FLOW_MARKER test-case-stop */", map);
}
```

### Automatically Launch Browser to Show Report

If you would like your script to automatically launch your web browser to immediately show you your BlazeMeter test report, first create a simple method to launch your local machine's web browser:

```java
public static void openInBrowser(String string) {
    if (java.awt.Desktop.isDesktopSupported()) {
        try {
            java.awt.Desktop.getDesktop().browse(new URI(string));
        } catch (Exception e) {
            System.out.println("Failed to open in browser");
        }
    }
}
```

You can then call that method and feed your yet-to-be-generated report URL into it:

```java
String reportURL = String.format("https://%s/api/v4/grid/sessions/%s/redirect/to/report", BASE, driver.getSessionId());
openInBrowser(reportURL);
```

After you complete the steps above, simply finish writing the rest of your script as you would normally. That's it!

---

## Create from Python IDE

If you as a Python developer prefer to use your own Selenium script instead of a YAML configuration file, you can do so by modifying your script to automatically create a GUI Functional Test when executed from your local Python IDE.

**Use when**: Creating GUI Functional Tests from Python IDE using Selenium or setting up BlazeMeter authentication, desired capabilities configuration, connection setup, test suites/cases, and automatic report launching.

### Overview

Here we will outline required modifications. For the purpose of this guide, all examples here will assume a Selenium script written in Python, though [Selenium scripts in Java](skill-blazemeter-functional-testing://references/gui-tests.md) are also supported. BlazeMeter supports Selenium 4.1.3 and 4.1.4 or higher.

**Note**: Whereas this guide's purpose is to advise how to add BlazeMeter functionality to your own existing script, please be aware that BlazeMeter Support does not provide scripting assistance. You can find example python scripts [here](https://github.com/Blazemeter/GUI-Functional-Test-Examples).

### Step 1: Setup BlazeMeter Authentication

Set values for the variables *base* (the URL to BlazeMeter), *API_KEY*, and *API_SECRET* to ensure an authenticated connection to your BlazeMeter account. (For more information on how to find or generate your API key, see [BlazeMeter API keys](skill-blazemeter-api-reference://references/authentication.md).)

```python
base = 'a.blazemeter.com'
API_KEY = '{your API key}'
API_SECRET = '{your secret key}'
blazegrid_url = 'https://{}:{}@{}/api/v4/grid/wd/hub'.format(API_KEY, API_SECRET, base)
```

### Step 2: Configure BlazeMeter Features

Specify the GUI Functional Test features you want to enable for your script. You can specify a variety of settings that enable optional features or specify certain configurations. For a full list of what can be included in this dictionary, please see our [GUI Test "Desired Capabilities" Options](skill-blazemeter-functional-testing://references/gui-tests.md) reference guide.

For Selenium 4.1.3:

```python
desired_capabilities = {
    'browserName':'firefox',
    'blazemeter.sessionName': 'My Session',
    'blazemeter.videoEnabled': 'True'
}
```

For Selenium 4.1.4 or higher:

```python
bzm_options = {
    'blazemeter.sessionName': 'My Session',
    'blazemeter.videoEnabled': 'True'
}
browser_options = webdriver.FirefoxOptions()
browser_options.browser_version = 'default'
browser_options.set_capability('bzm:options', bzm_options)
```

### Step 3: Configure BlazeMeter Connection

To ensure your script connects to and runs on BlazeMeter with all the features you specified, simply add the following line to set the *blazegrid_url* value:

For Selenium 4.1.3:

```python
driver = webdriver.Remote(command_executor=blazegrid_url, desired_capabilities=desired_capabilities)
```

For Selenium 4.1.4 or higher:

```python
driver = webdriver.Remote(command_executor=blazegrid_url, options=browser_options)
```

You can actually stop here if you like, as you've now implemented the minimum requirements to run your test on BlazeMeter -- it IS that easy! However, you may want to add some additional features to further tweak how your test will appear in BlazeMeter, in which case, continue reading below.

### Step 4: Add Test Suites & Test Cases

You can optionally designate BlazeMeter test suites and test cases in your script. (If you opt not to, your test will appear in the report under "Default Test Suite" and "Default Test Case".)

Doing so is easy -- First, simply create a dictionary that assigns names to the variables *testSuiteName* and *testSuiteCase*:

```python
args = {
    'testSuiteName': 'My Test Suite',
    'testCaseName': 'My Test Case Name'
}
```

Next, add `execute_script()` calls before and after your test steps to mark the beginning and end of the test case. In the following example, we have a single-line test that simply navigates to our demo site:

```python
driver.execute_script("/* FLOW_MARKER test-case-start */", args)
driver.get('http://blazedemo.com')
driver.execute_script("/* FLOW_MARKER test-case-stop */", args)
```

All you're doing is wrapping the test suite/case around your existing test.

If you want to break your test up into multiple test suites and cases, just repeat the process with another dictionary and new start/stop execute_script() calls.

If you want to add another test case to the existing test suite, then in your next dictionary, repeat the previous *testSuiteName* value and add a new *testCaseName* value. If you want a both a new suite and a new case, add new values to both.

### Step 5: Add Pass/Fail/Broken Statuses

Another optional feature you can add is pass/fail status reporting. (If you opt not to perform this step, all statuses will default to a blue "Undefined" in the test report.)

Simply expand your dictionary to include status reporting by adding a value to the "status" variable. You can also add a "message" variable to assign a custom message that will appear when you hover over the status in the report:

```python
args = {
    'testSuiteName': 'My Test Suite',
    'testCaseName': 'My Test Case Name',
    'status': 'passed',
    'message': 'Look! It passed!'
}
```

In the resulting report, a "pass" status will appear in green in the report, a "fail" status will appear in red, and a "broken" status will appear in orange.

**Note**: Passed/failed (past tense) in the code results in pass/fail (present tense) in the report.

### Automatically Launch Browser to Show Report

If you would like your script to automatically launch your web browser to immediately show you your BlazeMeter test report, simply add the following:

```python
webbrowser.open('https://'+ base +'/api/v4/grid/sessions/' + driver.session_id + '/redirect/to/report')
```

After you complete the steps above, simply finish writing the rest of your script as you would normally. That's it!

---

## Report

Review GUI Functional Test reports, including summary tab (test status, scenarios, data iterations), details tab (iterations/sessions, video/selenium commands, waterfall, logs, metadata, errors), and report management (rename, share, move, delete).

**Use when**: Reviewing GUI Functional Test reports or viewing summary tab, details tab, and managing reports with rename, share, move, and delete operations.

### Summary Tab

- **Test Status**: View overall test status
- **Scenarios**: Review test scenarios
- **Data Iterations**: See data iteration results

### Details Tab

- **Iterations/Sessions**: View individual iterations
- **Video**: Watch test execution videos
- **Selenium Commands**: Review Selenium commands
- **Waterfall**: Analyze request waterfall
- **Logs**: View test logs
- **Metadata**: Access test metadata
- **Errors**: Review error details

### Report Management

- **Rename**: Rename reports
- **Share**: Share reports with team
- **Move**: Move reports between projects
- **Delete**: Delete reports

---

## Duplicate, Delete, Move, or Rename a Functional Test

For any test that you create, you have the option to duplicate, delete, rename the test, or move it to another project. Under certain conditions, you can convert it to a **Browser Performance Test**.

**Use when**: Duplicating, deleting, moving, renaming, or converting Functional Tests to Browser Performance Tests.

### Test Operations

Follow these steps:

1. Navigate to the **Functional** tab
2. Select a test from the **Tests** drop-down list
3. Click the **Actions** menu for the test
4. Select one of the actions from the menu:
   - **Duplicate Test**: Create a copy of the test
   - **Convert to Browser Performance Test**: This pre-GA (Generally Available) feature is currently accessible to a subset of enterprise customers. If you are an enterprise customer and are interested in accessing this feature before GA, contact [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com)
   - **Move Test**: Move the test to another project
   - **Delete Test**: A confirmation message appears
5. (Optional) Click the pen icon to **rename** the test

### Documentation References

For detailed information about duplicating, deleting, moving, or renaming Functional Tests, use the BlazeMeter MCP help tools:

**Duplicate, Delete, Move, or Rename a Functional Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-duplicate-delete-move-rename-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-duplicate-delete-move-rename-test"]}`

---

## Test Data

Use test data in GUI Functional Tests, including defining test data parameters, using data in tests, defining iteration settings, previewing test data, and managing test data entities.

**Use when**: Using test data in GUI Functional Tests or defining test data parameters, using data in tests, defining iteration settings, previewing test data, and managing test data entities.

### Test Data Configuration

- **Define Parameters**: Set up test data parameters
- **Use in Tests**: Reference data in test scripts
- **Iteration Settings**: Configure data iteration
- **Preview Data**: Preview test data before execution
- **Manage Entities**: Manage test data entities

---

## Parameterize Taurus YAML Scripts

Parameterize GUI functional tests using Taurus YAML scripts, including creating data-provider CSV files, uploading files, refactoring tests to use data, and configuring iterations.

**Use when**: Parameterizing GUI functional tests using Taurus YAML scripts or creating data-provider CSV files, uploading files, refactoring tests to use data, and configuring iterations.

### Parameterization Process

1. **Create CSV**: Create data-provider CSV files
2. **Upload Files**: Upload CSV files to BlazeMeter
3. **Refactor Tests**: Update tests to use data
4. **Configure Iterations**: Set up iteration settings

---

## Desired Capabilities Options

Configure desired capabilities for GUI functional tests executed from IDEs, including platform, browser, version, project/test IDs, location, video, and session settings.

**Use when**: Configuring desired capabilities for GUI functional tests executed from IDEs or setting up platform, browser, version, project/test IDs, location, video, and session settings.

### Capability Options

- **Platform**: Set target platform
- **Browser**: Select browser type
- **Version**: Choose browser version
- **Project/Test IDs**: Configure project and test IDs
- **Location**: Set execution location
- **Video**: Enable/disable video recording
- **Session Settings**: Configure session parameters

---

## Custom JavaScript Actions

The [Scriptless Scenario Editor](skill-blazemeter-functional-testing://references/gui-tests.md) supports several [actions](skill-blazemeter-functional-testing://references/gui-tests.md) which you as a developer can use to execute custom JavaScript code snippets in your GUI Functional Tests:

- **Assert Eval** action
- **Script Eval** action
- **Store Eval** action

The option to execute custom JavaScript code during a test makes Scriptless Testing very extensible and lets advanced users overcome limitations that a purely "scriptless" approach might bring.

All Taurus actions also support `${Taurus Variables}` that you can reference directly in your JavaScript code.

**Use when**: Implementing custom JavaScript actions for scriptless GUI Functional Tests, extending test functionality with custom scripts, or executing custom JavaScript code snippets in GUI Functional Tests.

### Data Types and Return Statements

All of the actions available in Scriptless GUI Functional Tests run in the context of the web page you are testing, and you can access the `document` of the page in order to perform operations. For more information, see [JS Document, W3C Schools](https://www.w3schools.com/js/js_htmldom_document.asp).

Write actions that are wrapped with a return statement by using immediately invoked function expressions (IIFE).

```javascript
(function() {
// Code goes here...
})();
```

IIFEs are a very basic wrapper that create the function and call it right away. The inner function in this example can contain a return statement that is properly handled, and the returned result is propagated.

#### How Data Types Are Resolved

By default, variables in scripting actions are either of type number or string. In the following example, you use the `storeEval` action to save the number 5 in a variable named `sum`.

Depending on how you use this variable `sum`, its type is resolved differently. For example, if you use it in a string context

```javascript
'${sum}' + ' items'
```

then, after expansion, the variable resolves to a string:

```javascript
'5' + ' items'
```

In this case, the strings are concatenated using the plus operator to `'5 items'`.

On the other hand, if you have a numeric context

```javascript
${sum} + 10
```

then, after expansion, the variable resolves to a number:

```javascript
5 + 10
```

And the numbers are added using the plus operator, resulting in `15`.

The same type resolution rule applies to comparison operators.

#### Working With Complex Data Types

In BlazeMeter, there is no complex data type, instead you serialize JSON data into a string, and then deserialize it back in another code snippet. In this example, you have used the `storeEval` action to create the variable `person`, and you serialize the array using the following script:

```javascript
(function() {
const person = {name: 'John', surname: 'Doe'};
return JSON.stringify(person);
})();
```

Later on, you can deserialize the data and use the array fields in another action:

```javascript
(function() {
const person = JSON.parse('${person}');
console.log(person.name); // Will print 'John'
console.log(person.surname); // Will print 'Doe'
})();
```

### JavaScript Actions

#### ScriptEval

**Description**

ScriptEval is the basic action for running custom JavaScript code. The action does not return a value. You can consider it equivalent to returning 'void' in programming languages.

**Syntax**

For ScriptEval, the entire expression is evaluated, but a common best practice is to have the first line be a call to a function that is defined below, or to an anonymous function

```javascript
myFunction();
function myFunction(){
document.getElementById("buttonID").setAttribute("disabled", true);
//you can add as many instructions here as needed
}
```

In the simple example above, the custom action sets the `disabled` attribute of a button to true so you can verify with another action that the button is no longer clickable.

BlazeMeter evaluates the function `myFunction();` which starts executing the instructions.

**Usage**

Almost all interaction with the page in JavaScript is done through the [JS Document (see W3C Schools).](https://www.w3schools.com/js/js_htmldom_document.asp) In all actions, you can reference `${Taurus Variables}` directly inside the code. These variables may come from a test data parameter or a CSV file, or they may have been set by other actions.

Here is an example where you set the innerText of the button to a string.

```javascript
myFunction();
function myFunction(){
document.getElementById("buttonID").innerText = "${variableName}";
}
```

Taurus replaces the variable `${variableName}` with the value just before the step is executed.

#### StoreEval

**Description**

StoreEval is the basic action for running custom code, and it stores the return value of the script in a `${Taurus Variable}` so that you can use the output of a script in the rest of your test.

**Syntax**

For StoreEval, BlazeMeter prefixes your code with an implicit `return`call. Otherwise, the syntax is the same as the other actions. For example, you enter the following code snippet:

```javascript
myFunction();
function myFunction(){
document.getElementById("buttonID").setAttribute("disabled", true);
//you can add as many instructions here as needed
}
```

And BlazeMeter prefixes it implicitly with a `return`statement:

```javascript
return myFunction();
function myFunction(){
document.getElementById("buttonID").setAttribute("disabled", true);
}
```

However, if you add the `return` statement yourself and entered the following code:

```javascript
return myFunction();
function myFunction(){
document.getElementById("buttonID").setAttribute("disabled", true);
}
```

Then BlazeMeter would treat it as a duplicated `return` statement:

```javascript
return return myFunction();
function myFunction(){
document.getElementById("buttonID").setAttribute("disabled", true);
}
```

The main thing that's different for StoreEval is that it takes an extra parameter, the name of the variable to store the result from the script:

**Usage**

In this example, you store the return value from the script in the variable `outputText`. Then, in a laterType action, you *use*the variable reference `${outputText}` to type the returned value into an address field. Note that when you *declare* the variable `outputText` in the StoreEval Action, you do not wrap it in `${ .. }` characters.

In this example, BlazeMeter executes the first line as `return myFunction();`. And inside myFunction() it executes the line:

```javascript
return document.getElementById("buttonID").innerText;
```

The function returns the innerText of the button. The action returns the value and stores it in the variable `outputText` which you can then reference as `${outputText}` elsewhere.

#### AssertEval

**Description**

AssertEval is a shortcut that evaluates a custom JavaScript code snippet and asserts that the result returns true. If it does not return true, the action is interpreted as an unmet assertion and the test fails.

**Syntax & Usage**

When `myFunction()` is evaluated, it either returns true or false. In this example, the result depends on the presence of a button with a certain text.

```javascript
myFunction();
function myFunction(){
if(document.getElementById("buttonID").innerText = "Expected Text")
{return true;}
else
{return false;}
}
```

Simply verifying whether text exists on the web page can more easily be accomplished by the Assert Text action. This is just a trivial example of how a custom JavaScript returning a true or false value lets you pass or fail an assertion.

### Worked Examples

The following two examples show how custom JavaScript functions can read any values that are not directly accessible named Objects, and how a they can modify any value while the script is running, for example, to calculate intermediate values or to normalize text.

#### Example 1: Working With Values From Basic Tables

The web page you want to test contains a regular HTML table. In this first worked example, you want to calculate the sum of the numeric values in the third column of this table so you can compare it in an assertion later:

| a | x | 1 |
|---|---|---|
| b | y | 2 |
| c | z | 3 |

The following code snippet selects cells from the third column, and then applies a custom calculation script to the cells' innerText contents.

```javascript
(function() {
const col3 = document.querySelectorAll('table tr td:nth-child(3)');
return Array.from(col3).reduce((res, x) => res + Number(x.innerText), 0);
})();
```

You use this custom script in a `storeEval` action and declare the variable `sum` to store the result. This way, you can reference the calculated value later as `${sum}` in another action. In the example below, you use the result in a conditional if-then-else statement. Since the `reduce` function returned a number, you can use the result with numeric comparison operators such as `if ${sum} > 5`.

#### Example 2: Verify a Value in a Complex Table

In the second worked example, you want to verify that a particular value in an HTML table is correct. The table is however irregular and columns and values are sometimes included and sometimes omitted, which means the precise position of values in the HTML document changes depending on circumstances. This causes issues with identifying the Object reliably since, if you attempted to reference it like a static object, you would often read the wrong value.

**Solution: Theory**

While the data isn't in a consistent place each time, you notice an implicit relationship between labels (keys) and values. In this example, `MLR Year` is the key and the number `2019` is its value. Similarly, `Exclusion Exception` is the key and the text `Does not apply` is its value, and so on.

You can use this consistency to identify a particular value in the table with a minimum level of reliability.

**Devising a custom function**

You want to devise a custom JavaScript function that takes a pair of key and expected value, and returns true if the value for that key found in the table is the expected value, and false otherwise.

More formally:

```
F(Key,Value) -> True/False
```

1. If the key is in the table: If the value for that key is the expected value, return true. If the value for that key is not the expected value, return false.
2. If the key is not in the table: Return false

**Locating the data**

Before you can start looking for the value in the table, first find the table on the page, and get each of its rows:

```javascript
function valueVerifier(key, value) { // replace by ${key} and ${value} later
let table = document.getElementsByTagName("table").item(0);
let tableBody = table.getElementsByTagName("tbody").item(0);
let rows = tableBody.getElementsByTagName("tr");
// more code to be added here
}
```

**Searching the value**

Now that you have the collection of rows to iterate over, you plan out the main loop:

1. For each row, loop over each column. For each column, compare the cell's inner text to the 'key' value.
   - If the key is present, read the next column to the *right*and compare it to the expected value.
   - If the expected value is present, return true and stop searching.
   - If the value is not present, continue the search.
   - If the key is not present, continue the search.
2. If, after you have checked every column and every row without finding the key-value pair, you return false.

The following code sample loops over all rows to search for the target value:

```javascript
for (let row of rows) {
let cols = row.getElementsByTagName("td");
for (let colIndex = 0; colIndex < cols.length; colIndex++) {
let col = row.getElementsByTagName("td").item(colIndex);
if (col.textContent.includes(key)) {
if (colIndex + 1 < cols.length) {
let nextColVal = row.getElementsByTagName("td").item(colIndex + 1).textContent;
if (nextColVal.includes(value)) { return true; }
}
}
}
}
```

**Calling the custom function**

The last thing you need to do is call the function with some arguments. For that you add the line `console.log(valueVerifier("MLR Year", "2019"));`

**Debugging the code snippet**

The simplest way to debug a piece of JavaScript like this is by using Chrome Dev Tools on the target web page. For more information, see [Chrome DevTools](https://developer.chrome.com/docs/devtools/).

To open the Dev Tools, press F12 in Chrome. On the Dev Tools pane, paste the entire code snippet into the Console tab and press enter. It returns true or false depending on whether it found the key value pair in the first table.

If you add the line `debugger;`, it triggers a breakpoint in the Chrome debugger. The Chrome Debugger helps you see the exact state of the scope and code at that point, and lets you step through the code line by line.

**Running the JavaScript Snippet in a Scriptless Test**

Now that you have written your custom code snippet and debugged it, you want to [use it in a Scriptless test](skill-blazemeter-functional-testing://references/gui-tests.md).

In this case you only care about *whether* the value is present, so you use an `Assert Eval` action. If you cared about *what* the value was, you could adjust your code and use a `Store Eval` action.

In the action, switch to Fullscreen Edit Mode and paste the script. Make two adjustments to the code:

1. Remove the `console.log()` debug line. You want only the true/false result from `valueVerifier()` function.
2. Use Taurus variables for values in the `valueVerifier()` function:

```javascript
valueVerifier("${Key}", "${Value}");
```

BlazeMeter replaces the Taurus variables `${Key}` and `${Value}` by test data values that you have set earlier in the test, or from a CSV file.

**Notes**

- The HTML DOM is the context for all scripts, and there is a lot of public information on this and how to use it with JavaScript.
- Writing these scripts is best done in an IDE like VisualStudio Code or alike.
- Debugging these scripts is best done in Chrome with dev tools (F12), and be sure to use the `debugger;` statement.
- When using your snippet in Scriptless, remember it will implicitly insert a return call at the start of the code.
- Usually, it is best practice to do most of the work in a function, then calling that function on the first line.
- You can use ${Taurus Variables} directly in the code, but remember these will come in as strings and you should wrap them in "double quotes".
- AssertEval will assert based on the return value, StoreEval will store the returned value, and ScriptEval will run your script but return nothing.

---

## Taurus Actions Scriptless

Reference guide for all available Taurus actions in scriptless GUI Functional Testing, including actions, control structures, and parameters.

**Use when**: Creating scriptless GUI Functional Tests with Taurus actions or referencing available actions, control structures, and parameters.

### Available Actions

- **Navigation**: Navigate to URLs
- **Click**: Click elements
- **Type**: Type text
- **Assert**: Assert conditions
- **Wait**: Wait for conditions

### Control Structures

- **If/Else**: Conditional logic
- **Loops**: Iteration structures
- **Try/Catch**: Error handling

---

## Running a Functional Test

From the test configuration view of any API Functional Test or GUI Functional Test, run your test by clicking the "Run Test" button.

**Use when**: Running GUI Functional Tests or API Functional Tests from the test configuration view.

### Running a Test

When you're executing an API Functional Test, you are forwarded to the test booting screen. Wait while the test is running.

When the first results are ready, you are forwarded to the [GUI Functional Test Report](skill-blazemeter-functional-testing://references/gui-tests.md) or [API Functional Test Report](https://help.blazemeter.com/docs/guide/functional-api-test-report.html), respectively.

### Stopping a Functional Test

If you need to manually stop the test for any reason, refer to our guide on [Stopping a Test](skill-blazemeter-performance-testing://references/scenarios.md).

### Scheduling a Functional Test

The process for scheduling a Functional test to run repeatedly is the same as for Performance tests. For detailed information, see [Scheduling a Performance Test](skill-blazemeter-performance-testing://references/scenarios.md).

**To schedule a Functional test:**

1. On the **Functional** tab, click **Tests**, and open a test
2. In the **Schedule** section on the left side, click **Add**
3. Select the required frequency: **Weekly**, **Monthly**, or **Advanced**
4. **On Time:** Configure the run time of the test. BlazeMeter's default time zone is UTC+0
5. **Advanced**: Alternatively, enter your own CRON expression in the format "min hour day month weekday". **Example**: If we use "30 10 * 2 1", the test will run at 10:30 AM UTC+0, on each (*) Monday (1) of February (2). Take care not to accidentally set the interval too small. Use the scheduler validation below your expression to verify your schedule. For example, you would not want to schedule a test to run every second, or every five minutes. Whereas the **On Time** option is expressed in UTC+0, the **Your next 3 tests** verification message will display in the time zone of your choice, matching whatever the value of your [time zone override](https://help.blazemeter.com/docs/guide/administration-time-zone-override.html) is (if the override is enabled)

**To manage scheduled tests:**

Open a test. All of your scheduled tests are listed on the left panel in the **Schedule** section.

- To disable or enable a scheduled test, toggle the slider on or off to enable or disable the schedule
- To delete a scheduled test, hover over the test in the **Schedule** section until the **Delete** context action appears, then click the delete icon
- To modify a schedule, delete the schedule and create a new one

**To review all scheduled tests of a workspace:**

1. Click the **Settings** icon in the top right corner
2. In the left column, expand the **Workspace** section
3. Click **Scheduled Tests**
4. Review all schedules assigned for all tests within the selected workspace

Here you can enable, disable, or delete any schedule without having to navigate to the test itself.

---

## GUI Functional Test Report

Soon after a [GUI Functional Test](skill-blazemeter-functional-testing://references/gui-tests.md) executes, the test report is available for review. This report is divided into "Summary" and "Details" tabs.

**Use when**: Reviewing GUI Functional Test reports, analyzing test execution results, or debugging test failures.

### Report Structure

- When you open the report, you will be greeted by the Summary tab
- The Details tab is divided into its own subtabs: "Video" and/or "Selenium Commands", "Waterfall", "Logs", and "Metadata"

**Note**: If you set `blazemeter.videoEnabled` to "no" in your Selenium script, only the list of Selenium commands executed will appear instead of a video.

### The Summary Tab

The **Summary** tab provides a high-level overview of the test's execution for individual test cases. Here you'll find useful information such as how long the test took to execute, how many test cases were included, how many test cases succeeded, etc.

The Summary report is divided into two sections.

**Latest Runs section** displays the cumulative statistics of all test sessions:

- **Overall Test Status** - The test status, either Passed, Failed or Undefined
- **Overall Suite Status** - (For Test Suites only) The status, either Passed if all tests passed, or Failed if at least one test failed, or Undefined
- **Scenarios Passing** - Overall number and percentage of passed scenarios for all test cases in all test sessions
- **Total Test Passing** - (For Test Suites only)
- **Total Scenarios Passing** - (For Test Suites only)
- **Total Data Iterations Passing** - When a data source is used with multiple rows of CSV data to dynamically provide data to the test, this column lists the number of iterations from the rows of data that passed, versus the overall number of iterations
- **Duration** - The difference between the "Started" date/time and the "Ended" date/time. Be aware this will span multiple test launches
- **Started** - The date and time the first command of the first session was executed
- **Ended** - The date and time the last command of the last session was executed
- **Locations** - The geographical zone and location where this test was run or if it was a private cloud
- **Show Test Data** - (For tests with [test data](skill-blazemeter-test-data://references/core-concepts.md) only.) Review and download the test data that was used. Click the **Rerun** button here to run an individual test again with the same test data

Optionally, you can add your own notes in the "**Add Report Notes...**" field, then click the "Save" button to save them to that specific report.

**Test Scenarios section** provides additional details specific to each test scenario within the test:

- The test suite and the test scenarios belonging to that suite
- The Status of the test suite, either Passed, Failed, or Undefined
- **Passed Data Iterations** shows the percentage of rows that have passed if you use test data from a CSV file. Otherwise the column is empty
- The last columns show the status for runs in various browsers, for each test case, and show whether the specific test case passed or failed

Test cases may have the following states:

- **Passed**, designated by a green check mark
- **Failed**, designated by a red X
- **Undefined**, designated by a blue dash, meaning no status was set in the script
- **Broken**, designated by an orange exclamation mark, meaning the test could not be executed. Click the exclamation mark to navigate to that test case's description within the Details tab

Lastly, if you click the browser name in this table, you will be taken to the Details tab for that particular test.

### The Details Tab

The **Details** tab provides a wealth of detail about the Selenium test.

**Note**: You'll likely initially see a spinning progress icon instead while the test starts running. This is ok! The test needs to execute for a time before any data can be displayed.

The **Details** tab is divided into four sections, listed on the left of the report, and detailed in the following sections below.

#### Iterations/Sessions

The Details view is broken down by Sessions. When a test is run, each scenario in the test runs in each browser defined for the test. Each of these scenario/browser runs are stored as individual Sessions in the test report.

The results of each Session are viewed one at a time in the Details view, meaning when the Details view is opened, only one session is displayed in the view.

**Note**: When external data is used, each row/record of data creates a session as well.

**To access other Sessions:**

1. In the upper-right of the Details view, click the Select field. A dropdown displays all the sessions in the report with a system-generated name for each Session
2. Select a Session to load the data into the Details view. **Note**: The Select field only displays in the Details view

#### Video/Selenium Commands

The Video section, the first section displayed when viewing the Details tab, shows both the video recording of your Selenium test executing (in the engine's browser) and a list of all Selenium steps the script executed, organized by test case/suite.

If the video option was disabled in your script, then "Video" will be replaced by "Selenium Commands" and only the list of Selenium steps will be displayed.

You can play the entire video to watch the recording of the script executing from start to finish or you can click individual steps in the Selenium commands list to the right, which will allow you to jump to the timestamp in the video in which that specific step executed.

The commands are displayed in one of two modes, selected via the toggle located at the top-right of the commands list:

- **Test Steps Only** shows only the commands from the script
- **All Commands** shows all the commands necessary to launch and run the test

This is especially useful for debugging failed steps. By clicking a command in the list, you can jump to the point in the video in which it executed and the failure occurred. In the event a command had trouble executing during the test, it will be flagged with an orange exclamation mark icon.

Look for a *Webdriver closed* command to appear at the end of the list. If this command does not appear, then there was a problem with the test.

#### Video/Screenshots

In addition to video timestamps, you can also view screenshots, one for each URL navigated by the script. The screenshot icon is located to the right of each URL.

**Note**: No screenshots are recorded after a **go** or **open** action that either goes to a different domain, or that starts from an empty tab. To work around this browser limitation, start your recording on the target page, or click anywhere inside the Recorder Extension after going to or opening a new page.

When a failure or error occurs, generate a link to the specific step with the issue and share it for debugging. To the right of each screenshot icon, click the **link** button to copy the URL to your clipboard. This link opens the report in the browser for anyone with access to view the report, and jumps to that step in the report.

#### Waterfall

The waterfall report shows the page load time on the network level for each step, which can be useful when looking for any pages that might take too long to load and thus result in a delay in the test.

The waterfall report can aid you in uncovering performance issues. As you review the waterfall report, you can click to expand each performed request to view more details about it. This is similar to what you would see if you were to open the developer tools for a real browser and examine the network tab.

You can also hover your mouse over each graph in the waterfall report to see expanded information on request phases and their elapsed times.

#### Logs

The logs section provides a thorough list of possible logs to refer to.

Click the "Select a log file" field to open a drop-down menu which will display all logs available for download.

The logs available in this list will vary depending on what options you had chosen when configuring your script and what type of user you are. For example, admin users will have more logs available to view than standard users.

#### Metadata

The metadata section displays detailed information pertaining to the test itself.

Here you can find some useful data about the test, such as its session ID, driver used, browser used, etc.

**Note**: Each command's response includes a delay that is equal to the implicit wait timeout. To shorten this delay, which defaults to 60 seconds, you can change the webdriver's implicit wait parameter within your test script to a value such as 30 seconds.

#### Errors

The errors section displays detailed information pertaining to errors found in the test (if any). Clicking on a specific error item will take you to the point where it occurs during the test.

### Managing Reports

#### How to Rename a Report

1. Open the report and click in the report name
2. The Name field opens for editing
3. Change the name of the report
4. Click anywhere out of the Name field to save the changes

#### How to Share a Report

When sharing is enabled, anyone with the link can access the report. Every time you disable and re-enable sharing, BlazeMeter creates a new token. Thus previous links to this report won't work anymore.

**Steps:**

1. Open the report
2. Next to the report name, click the Ellipsis icon
3. Click **Share Report**
4. Enable or disable sharing for this report
5. If you've enabled sharing: Click **Copy to Clipboard**. Share the report by pasting the link in an email or chat message to the recipient

#### How to Move a Report

Reports are stored in the same project as the test used to create the report, they are tied to the test. Because of this dependency, reports can only be moved to a different project by moving the test to the project.

#### How to Delete a Report

1. Open the report
2. Next to the report name, click the Ellipsis icon
3. Click **Delete** and confirm

---

## Managing Sensitive Data Securely with Secrets

Secrets are objects that contain sensitive data, such as passwords, tokens, credit card numbers, or any other data that shouldn't be exposed. By using secrets, you do not have to hard code any sensitive data into your test scripts. When you run a test, whenever an enabled secret appears in reports or logs during and after run time, the value of the secret is replaced with asterisks (*).

**Use when**: Managing sensitive data in GUI Functional tests, avoiding hard-coding passwords or tokens in test scripts, or when you need to secure sensitive information in test results and logs.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Functional Secrets**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-secrets.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-secrets.htm"]}`

### Prerequisites

To use secrets, you need to create them in your Workspace settings. For more information on how to create secrets in your workspace, see [Create and Manage Secrets](skill-blazemeter-administration://references/security.md).

### Security Best Practices

When using secrets, ensure that:
- Only production and non-sensitive secrets are used
- All secrets are strictly limited in scope and privilege, and access only test-specific resources or data
- Secrets should be temporary and rotated regularly
- You avoid the use of secrets that provide access to productions environments or sensitive customer data

### Use Secrets in YAML

In YAML, you can reference a configured secret using the prefix **BZM_SECRET**. Add a default value to your secret after the secret name. If the secret is not configured in your workspace, the test uses the default value.

```yaml
${__P(BZM_SECRET_secret1,DefaultValue)}
```

**Automatic Detection:**
- Secrets included in your test script are automatically detected when you upload your test script when your test script is written in YAML
- The **Secrets** section appears as enabled, but is read only
- If no secrets are detected in your YAML script, you can [manually choose which secrets to include](#manually-enable-secrets)

### Manually Enable Secrets

You can manually enable secrets when:
- Using executors other than YAML. Because BlazeMeter cannot automatically detect secrets that are not written in YAML, you need to configure the secrets in your workspace settings and then enable them manually
- You want to enable Secrets due to the possibility of sensitive data showing in test results or logs. Any selected secrets that appear in your test results or logs are replaced with asterisks (*)

**To enable the Secrets section and choose which configured secrets to include in your test:**

1. On the test configuration page, scroll to the **Secrets** section and toggle the button ON
2. Select all relevant secrets for your test script. Search for secrets using the search bar
3. To only show the secrets you have already selected, click **Show Selected Secrets**

---

## Documentation References

For detailed information about GUI Functional Tests, use the BlazeMeter MCP help tools:

**GUI Functional Testing Overview**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-testing-overview`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-testing-overview"]}`

**Creating Scriptless Functional Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-create-scriptless-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-create-scriptless-test"]}`

**Creating a GUI Test by Uploading a YAML File**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-gui-create-yaml-file`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-gui-create-yaml-file"]}`

**Creating a GUI Test from a Java IDE**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-gui-test-create-from-java-ide`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-gui-test-create-from-java-ide"]}`

**Creating a GUI Test from a Python IDE**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-gui-test-create-from-python-ide`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-gui-test-create-from-python-ide"]}`

**Running a Functional Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-test-run`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-test-run"]}`

**GUI Functional Test Report**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-gui-test-report`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-gui-test-report"]}`

**GUI Test Desired Capabilities Options**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-gui-test-desired-capabilities-options`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-gui-test-desired-capabilities-options"]}`

**Parameterize Tests (Taurus YAML Scripts)**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-gui-test-parameterize-taurus-yaml-scripts`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-gui-test-parameterize-taurus-yaml-scripts"]}`

**Using Test Data in GUI Functional Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-test-data`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-test-data"]}`

**Run Grid Proxy over HTTPS**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-run-gridproxy-over-https.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-run-gridproxy-over-https.htm"]}`

**Custom JavaScript Actions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-custom-javascript-actions`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-custom-javascript-actions"]}`

**Duplicate, Delete, Move, or Rename a Functional Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-duplicate-delete-move-rename-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-duplicate-delete-move-rename-test"]}`

