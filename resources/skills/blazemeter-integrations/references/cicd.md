# CI/CD Integrations

## Overview

BlazeMeter integrates with CI/CD tools to automate performance testing as part of continuous integration and deployment pipelines.

**Use when**: Integrating BlazeMeter tests into CI/CD pipelines or automating performance testing as part of continuous integration and deployment workflows.

### Add BlazeMeter Performance Testing to Your CI/CD Pipeline

By incorporating load tests into your CI/CD pipeline, you can detect and address performance issues early in the development cycle. This approach lets you identify and fix potential bottlenecks before they impact your users, saving time, effort, and costs associated with addressing performance problems later in the development process.

To add BlazeMeter load tests to your CI/CD pipeline, you need the following:

- **SCM**: A source code management system. This is where you keep and version your application's source code. The SCM can also be used to version your test scripts and most companies do so. Most popular SCM tools are based on Git.
- **CI/CD**: A Continuous Integration and Continuous Delivery toolchain. CI/CD tools are used to build, test, package and ship your application to production. They offer multiple integration options as plugins and scripts to integrate with a huge ecosystem of tools. You need to have [Taurus CLI](https://gettaurus.org/docs/CommandLine/) available in your CI/CD runner/delegate because we are going to use it to trigger a BlazeMeter test.
- **BlazeMeter**: A leading Continuous Testing solution.

Including BlazeMeter load/performance tests in a CI/CD toolchain involves two steps:

1. In your CI/CD tool, you create a step to clone the git repository where you keep your test scripts (JMeter, Gatling, Taurus, and so on).
2. In your CI/CD tool, you create a step to execute a Taurus CLI command (Bash script). This step uploads to BlazeMeter the test scripts you downloaded in the previous step and then triggers the test. In the background, Taurus CLI uses BlazeMeter's REST API to update the test scripts and trigger the test. It also passes or fails tests according to the failure criteria you define in BlazeMeter.

### Documentation References

For detailed information about adding BlazeMeter performance testing to CI/CD pipelines, use the BlazeMeter MCP help tools:

**Add BlazeMeter Performance Testing to CI/CD Pipeline**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-add-load-tests-to-CI-CD.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-add-load-tests-to-CI-CD.htm"]}`

---

## Jenkins

Use BlazeMeter's Jenkins plugin to execute automatic load test scripts, view test reports in Jenkins, and set build status based on error percentage and response times.

**Use when**: Using BlazeMeter's Jenkins plugin to execute automatic load test scripts or viewing test reports in Jenkins and setting build status based on error percentage and response times.

### What is Jenkins?

[Jenkins](https://www.jenkins.io/) is an open-source [continuous integration](https://www.blazemeter.com/blog/continuous-integration-jenkins?utm_source=blog&utm_medium=BM_blog&utm_campaign=add-jenkins-to-your-deployment-processes) tool written in Java for automating tests. Builds can be started in various ways. For example, they can be triggered by a commit in a version control system, scheduled via a cron-like mechanism, or built when other builds have completed, and by request of a specific build URL.

### How to Install BlazeMeter's Plugin for Jenkins

You can also [download](https://plugins.jenkins.io/BlazeMeterJenkinsPlugin) BlazeMeter's Plugin to Jenkins, or install it through the Jenkins Dashboard:

1. Log in to Jenkins and go to the dashboard. Select 'Manage Jenkins' and then 'Manage Plugins'. Then, from the top tabs, select 'Available'
2. Hit 'Ctrl + F' / 'CMD +F' in your browser and search for BlazeMeter. Then mark the BlazeMeter check box
3. Scroll down and click 'Download now and install after restart'
4. After the download starts, click to restart Jenkins

### How to Configure BlazeMeter's Plugin for Jenkins

1. After the restart, click 'Manage Jenkins' and then click Configure System
2. Scroll down to the 'BlazeMeter Cloud' section. You will see the URL 'https://a.blazemeter.com'
3. Click Save
4. Click **Credentials > System > Global Credentials (unrestricted)**
5. Click the **Add Credentials** button and choose the **BlazeMeter Credentials** button. Add your BlazeMeter API Key Id and API Key Secret
6. Add a nickname for your key in the Description field
7. Leave the 'ID' field empty - it will be generated automatically once you save the credential
8. Click the **Test BlazeMeter credentials** button

### How to Configure a Job Using BlazeMeter's Jenkins Plugin

1. Click on an existing job or create a new one, then press Configure
2. Scroll down to the 'Build' steps. Click **Add Build Step** and choose **BlazeMeter**

### How to Set Up the Build's Test

If your keys were pre-configured correctly in the global settings, you will see your Workspaces and tests in two drop down menus.

1. Click the "Workspace ID" menu to choose the Workspace you want to see tests from. You will now see all your tests for your chosen Workspace in the drop down menu 'BlazeMeter Test'
2. Select a test to run
3. Either click 'Save' to save your Jenkins project and then click 'Build Now' to run the test. Or, use the plugin's additional configurations and only then save and build. There are a few options:
   - 'Download JTL report' checkbox - downloads the JTL report after finishing the test
   - 'Download JUnit report' - downloads the JUnit report after finishing the test
   - 'Advanced' - options include the following properties:
     - Path to the JTL and/or JUnit reports (if you checked the checkboxes)
     - Path to the main and additional test files. This files will be upload in your BlazeMeter test (override if this files already exists) before run test
     - Set Notes and JMeter properties for pushing to the BlazeMeter load test
     - Interrupt FreeStyleProject build, if BlazeMeter Build Step was failed
     - Set custom report link name to BlazeMeter report in your Jenkins build

For more information, see the [Setting Up Your CI/CD Pipeline With Jenkins and GitHub](https://www.blazemeter.com/blog/cicd-pipeline-jenkins-github) blog.

### Reports

The plugin supports downloading two kinds of reports, **JUnit** and **JTL**.

All reports are saved to the `${WORKSPACE}` by default, but this behavior can be overridden by defining paths. Paths can contain Jenkins variables, which are resolved to actual values.

When using the plugin with a master/agent Jenkins configuration, please keep in mind that, by default, the permissions that Jenkins has in the master filesystem differ from the agent permissions. For example, if you want to save `jtl/junit` artifacts outside of `$JENKINS_DATA_FOLDER`, set the permissions to 757 for the folder you want to use at master.

On the remote agent, the Jenkins agent has, by default, 777 permissions for the folder in /home. For example, if you're using ssh @ for connecting to the agent from master, then the Jenkins agent will have 777 permissions for `/home/<username>`.

### Adding Notes to Public Report

You can add notes to the public report. This feature is available both in `Freestyle projects` and in `pipeline` mode.

**Freestyle project**:
- Open the job
- Go to the BlazeMeter step
- Expand the `Advanced` section
- Enter the note in the `Notes` field

**Pipeline**:
For more information, see the [pipeline usage guide](https://github.com/Blazemeter/blazemeter-jenkins-plugin/blob/master/usingPipeline.md)

The syntax `notes:'a\\n\\b\\n\\t\\r'` produces a multiline note.

### Adding JMeter Session Properties to Test Session

There is an ability for adding jmeter properties to test session.
- Open the job configuration
- Expand the `Advanced` section
- Enter session properties in the `Session properties` field in the following format: `key=value,key1=value1,key2=value2`

[Snippet for using session properties with pipeline](https://github.com/Blazemeter/blazemeter-jenkins-plugin/blob/master/usingPipeline.md)

Sending properties for the test session is currently not supported for multi tests.

### How to Run a BlazeMeter Test in Jenkins Without a Plugin

Jenkins, like any other CI tool, enables executing shell commands. With shell commands you can execute API calls to start tests, create tests, update them, etc.

### How to Build a Job with BlazeMeter's Jenkins Plugin

1. Once inside the job, click 'Build Now'
2. Click the build that is running
3. Click 'Console Output' to see the build progress. You'll see the test parameters and an update every few seconds
4. When the test finishes, you'll see a summary of the test results and their impact on the build

You can now click 'BlazeMeter Report' to see the test report the same way you would see them on the BlazeMeter site.

You can also edit and compare test results to previous runs.

All logs and data generated during test runs are stored in a ZIP file which you can access directly from your BlazeMeter account, in the 'Logs' tab of the report.

### Using BlazeMeter with Jenkins Pipeline

For more information, see [https://github.com/Blazemeter/blazemeter-jenkins-plugin/blob/master/usingPipeline.md](https://github.com/Blazemeter/blazemeter-jenkins-plugin/blob/master/usingPipeline.md)

### Jenkins Reports

Jenkins' Reports provide great out-of-the-box intelligence and visualization. Let's take a look at them:

**Performance Trend Report**: The Trend Report presents information about the trends and robustness of successful and failed test results, over time. This report is generated by fetching the JUnit.xml report when a test ends. This capability is inherent to Jenkins and is provided by the common Performance Jenkins plugin.

**Performance Report**: The Performance Report provides a basic KPI/Transactions report that visualizes a JTL that is an artifact of the test run. This report is built by fetching the JTL file when a test comes to an end.

**Comprehensive Reporting Dashboard**: A far more comprehensive reporting dashboard is available during the test, and after the test has ended. By pressing the BlazeMeter link, the BlazeMeter reports are shown, providing a deep dive into the performance KPIs, helping you find performance bottlenecks.

### PASS/FAIL Criteria

The Plugin is using */ci-status* requests for setting the build result. Depending on this request, the plugin sets one of the build results available in Jenkins:

**SUCCESS** - This status is set in the following cases:
- the test has no thresholds; The test has thresholds and they were not violated; There were no errors in the ci-status response

**UNSTABLE** - The test was completed successfully, but there were errors in the */ci-status* response

**FAILURE** - This status is set in the following cases:
- The test has thresholds and they were violated
- The test has no thresholds, but there were specific errors in the */ci-status* response: *"errors":[{"code": 70404,"message": "Session ended without load report data","details": null}]* *"errors":[{"code":0,"Message":"Not enough resources"}]*
- The Jenkins job got an error on a */test/start* request
- The Jenkins job got an UNSTABLE status due to errors, for one of the possible reasons, which caused a FAILURE. FAILURE overrides UNSTABLE in all cases

The default behavior in cases where a request to BlazeMeter does not respond or fail is to set job status to FAILURE. But you can change this status to UNSTABLE under the 'Manage Jenkins' -> 'Configure System' -> 'BlazeMeter Cloud' section using the checkbox 'Mark build as UNSTABLE if BlazeMeter does not respond with pass or fail.'

The other way to make your build more stable is to set the number of request attempts that the plugin will do in BlazeMeter. By default, this value is 3 (plugin will repeat the GET request to BlazeMeter if a response returned a failure, or BlazeMeter didn't respond in time). You can configure the number of request attempts using Java System properties: Go to 'Manager Jenkins' -> 'Script Console' and set the property 'bzm.request.retries.count' using the command 'System.setProperty("bzm.request.retries.count", "5");'

### Logging

This Plugin comes with a *<bzm-log>* file which can simplify the debugging process in case of any issues with the running test. This file is kept in the workspace. Its location differs depending on which kind of build (Freestyle job, or pipeline) is run.

If you run a Freestyle job, then you can use the following URL: *http://<jenkins-host>/job/<job-name>/ws/<build-number>/*

In case of pipeline, do the following to find your log files:
- Go to *http://<jenkins-host>/job/<job-name>/<build-number>/flowGraphTable/*
- In the `Step` table, click `Allocate node:Start`
- Change to `Workspace` and go into the `build-number` folder

### Working with Proxy Server

Since version 4.2, the Setup Proxy configuration for master and all agents are in the section *'Manage Jenkins' > 'Manage Plugins' > 'Advanced'*

This config is applied for each of the agents and master nodes.

In case that you need to use some agent with a different Proxy server, or without it, you should add JVM params to this agent in the section *'Manage Jenkins' > 'Manage Nodes' > 'Select Node' > 'Configure' > 'Launch method' > 'Advanced' >'JVM Options'.* The argument *-Dproxy.override=true* means that this agent will use a different proxy configuration. If this agent doesn't use a proxy server, simply pass this argument below:

If you want to use a different proxy server, add the following options after the 'proxy.override' option:
-Dhttp.proxyHost=<IP> -Dhttp.proxyPort=<PORT> -Dhttp.proxyUser=<USER> -Dhttp.proxyPass=<PASSWORD>

The other way for passing these Java properties to the agent without restart, is by using the Script Console, as described below,
System.setProperty("proxy.override", "true"); System.setProperty("-Dhttp.proxyHost", "<IP>"); System.setProperty("-Dhttp.proxyPort", "<PORT>"); System.setProperty("-Dhttp.proxyUser", "<USER>"); System.setProperty("-Dhttp.proxyPass", "<PASSWORD>")

**Set Custom report link name**

Since version 4.2, you can set a custom link name for the link to your BlazeMeter report:

By default, the Max report link name length is 35, but you can increase this value using the Java System property or Jenkins environment variable "bzm.reportLinkName.length".

**Using Job DSL** - [https://github.com/jenkinsci/blazemeter-plugin/wiki/Using-Job-DSL](https://github.com/Blazemeter/blazemeter-jenkins-plugin/blob/master/usingDSL.md)

**Using BlazeMeter Jenkins plugin with Github** - [https://www.blazemeter.com/blog/cicd-pipeline-jenkins-github](https://www.blazemeter.com/blog/cicd-pipeline-jenkins-github)

Learn more about [JMeter + Jenkins Integration: Two Approaches](https://www.blazemeter.com/blog/jmeter-jenkins-integration?utm_source=knowledgebase&utm_medium=kb&utm_campaign=blazemeters-jenkins-plugin-a-guide).

### Features

- Automatic test execution
- Test report integration
- Build status based on test results
- Error percentage and response time thresholds
- JUnit and JTL report downloads
- Notes to public reports
- JMeter session properties support
- Pipeline support
- Proxy server configuration
- Custom report link names

### Documentation References

For detailed information about Jenkins integration, use the BlazeMeter MCP help tools:

**Jenkins**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-jenkins-plugin-guide`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-jenkins-plugin-guide"]}`

---

## GitHub Actions

Run BlazeMeter tests from GitHub Actions workflows using BlazeMeter API or CLI tools.

**Use when**: Running BlazeMeter tests from GitHub Actions workflows or integrating performance testing into GitHub CI/CD pipelines.

### Overview

To integrate performance testing into your development workflow, you can use GitHub Actions to create and run BlazeMeter load tests. GitHub Actions is an automation platform for continuous integration and continuous delivery (CI/CD) that lets you define workflows that trigger actions in response to events, such as code pushes, pull requests, or issue creation.

In this integration, GitHub Actions jobs are executed within Docker containers using the GitHub Actions framework. Use the BlazeMeter Docker image to create tests, run existing tests, update the test files of existing tests, and many more.

GitHub Actions rely on an action.yml file. For the full list of BlazeMeter-related functions performed by the Docker image, see [GitHub Actions and BlazeMeter-related Functions](https://help.blazemeter.com/docs/guide/integrations-github-actions-and-bzm-related-functions_.htm).

### Configuration Steps

1. **Log in to GitHub**: Log in to your GitHub account
2. **Create Repository**: Create a new repository
3. **Create Workflow Directory**: In your new GitHub repository, create a `.github/workflows` directory
4. **Create Workflow File**: In the `.github/workflows` directory, create a file named `action.yml`
5. **Configure Workflow**: Add BlazeMeter test configuration to the workflow file
6. **Set Up Secrets**: Add BlazeMeter API credentials as GitHub secrets
7. **Commit Changes**: Save your changes by clicking **Commit**
8. **Run Workflow**: Run the jobs in your pipeline by navigating to **Actions > All workflows**

### Available Functions

GitHub Actions supports various BlazeMeter functions including:
- Create a new test
- Run an existing test
- Upload or update existing test files
- Replace or add configuration files before running a test
- Update variables in Taurus files
- Run existing test and download artifacts log file
- Add JMeter properties
- Customize a report name
- Add notes to your test report
- Override iterations configuration
- Override load configuration parameters
- Update test data
- Run test by test name
- Pass first job result to another job
- Send Microsoft Teams webhook notifications

### Variables

GitHub Actions supports various BlazeMeter-related variables including:
- `apiKey` - User's BlazeMeter API Key
- `apiSecret` - User's BlazeMeter API Secret
- `testID` - BlazeMeter Test ID
- `showTailLog` - Show running log in real-time
- `createTest` - Create a new test in BlazeMeter
- `testName` - Name of the BlazeMeter Test
- `inputAllFiles` - Upload multiple files
- `inputStartFile` - Upload single start file
- `uploadFileCheck` - Enable file upload
- `totalUsers` - Number of target concurrent virtual users
- `duration` - Time to hold target concurrency (in minutes)
- `projectID` - BlazeMeter Project ID
- `rampUp` - Ramp-up time to reach target concurrency
- `continuePipeline` - Continue pipeline execution
- `multiTests` - Run multi-test
- `functionalTest` - Run functional test suite
- `modelData` - Update Test Data Model variables
- `envVariable` - Update variables in Taurus YAML file
- `jmeterProperties` - Add JMeter Properties
- `reportName` - Report Name in BlazeMeter
- `notes` - Notes section of a report
- `iterationsConfig` - Run test based on iterations
- `iterations` - Number of iterations
- `testRunByTestName` - Run test by name
- `ignoreSLA` - Ignore SLA failures
- `webhookURL` - Microsoft Teams webhook URL
- `enablePublicReportURL` - Enable public report URL
- `locations` - Comma separated location values
- `dedicatedIP` - Use dedicated IPs
- `disableLoadConfig` - Disable load configuration
- `steps` - Number of ramp-up steps
- `throughput` - Requests per second limit
- `concurrencyControlEnabled` - Enable concurrency control
- `iterationsEnabled` - Use iterations instead of duration

### Documentation References

For detailed information about GitHub Actions integration, use the BlazeMeter MCP help tools:

**Run BlazeMeter Tests from GitHub Actions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-run-bzm-tests-from-github-actions.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-run-bzm-tests-from-github-actions.htm"]}`

**GitHub Actions and BlazeMeter-related Functions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-github-actions-and-bzm-related-functions_.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-github-actions-and-bzm-related-functions_.htm"]}`

**GitHub Actions and BlazeMeter-related Variables**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-github-actions-and-bzm-related-variables.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-github-actions-and-bzm-related-variables.htm"]}`

---

## GitLab CI/CD

Integrate BlazeMeter tests into GitLab CI/CD pipelines using BlazeMeter API or CLI tools.

**Use when**: Integrating BlazeMeter tests into GitLab CI/CD pipelines or running performance tests as part of GitLab workflows.

### Overview

Learn how to create and run BlazeMeter tests from GitLab CI/CD. In this integration, GitLab Continuous Integration and Continuous Delivery (GitLab CI/CD) jobs are executed within Docker containers through the utilization of the GitLab framework. By design, GitLab CI/CD relies on runners on which jobs get executed inside Docker containers. A BlazeMeter Docker image was developed for this integration that performs various functions, including but not limited to, creating a test, running an existing test, updating the test files of an existing test, and so on.

For the full list of BlazeMeter-related functions performed by the Docker image, see [GitLab Docker Image and BlazeMeter-related Functions](https://help.blazemeter.com/docs/guide/integrations-gitlab-docker-img-and-bzm-related-functions.htm).

### Configuration Steps

1. **Log in to GitLab**: Log in to your GitLab CI/CD account
2. **Create Project**: Click **New Project** and create a project
3. **Create Pipeline File**: Create a `.gitlab-ci.yml` file
4. **Configure Pipeline**: Define pipeline configuration in the `.gitlab-ci.yml` file
5. **Set Up Variables**: Add BlazeMeter API credentials as GitLab CI/CD variables
6. **Commit Changes**: Save your changes by clicking **Commit**
7. **Run Pipeline**: Run the jobs in your pipeline by navigating to **CI/CD >> Pipelines** and clicking **Run Pipeline**

### Available Functions

GitLab CI/CD supports various BlazeMeter functions including:
- Create a new test
- Run an existing test
- Add or replace existing test files
- Replace or add configuration files before running a test
- Update variables in Taurus files
- Run existing test and download artifacts log file
- Add JMeter properties
- Customize a report name
- Add notes to your test report
- Override iterations configuration
- Override load configuration parameters
- Update test data
- Run test by test name

### Variables

GitLab CI/CD supports various BlazeMeter-related variables including:
- `apiKey` - User's BlazeMeter API Key
- `apiSecret` - User's BlazeMeter API Secret
- `testIdInput` - BlazeMeter Test ID
- `showTailLog` - Show running log in real-time
- `createTest` - Create a new test in BlazeMeter
- `testName` - Name of the BlazeMeter Test
- `inputAllFiles` - Upload multiple files
- `inputStartFile` - Upload single start file
- `uploadFileCheck` - Enable file upload
- `totalUsers` - Number of target concurrent virtual users
- `duration` - Time to hold target concurrency (in minutes)
- `projectId` - BlazeMeter Project ID
- `rampUp` - Ramp-up time to reach target concurrency
- `continuePipeline` - Continue pipeline execution
- `multiTests` - Run multi-test
- `functionalTest` - Run functional test suite
- `modelData` - Update Test Data Model variables
- `envVariable` - Update variables in Taurus YAML file
- `jmeterProperties` - Add JMeter Properties
- `reportName` - Report Name in BlazeMeter
- `note` - Notes section of a report
- `iterationsConfig` - Run test based on iterations
- `iterations` - Number of iterations
- `testRunByTestName` - Run test by name
- `ignoreSLA` - Ignore SLA failures
- `locations` - Comma separated location values
- `dedicatedIP` - Use dedicated IPs
- `disableLoadConfig` - Disable load configuration
- `steps` - Number of ramp-up steps
- `throughput` - Requests per second limit
- `concurrencyControlEnabled` - Enable concurrency control
- `iterationsEnabled` - Use iterations instead of duration

### Documentation References

For detailed information about GitLab CI/CD integration, use the BlazeMeter MCP help tools:

**Run BlazeMeter Tests from GitLab CI/CD**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-run-bzm-tests-from-gitlab-ci-cd.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-run-bzm-tests-from-gitlab-ci-cd.htm"]}`

**GitLab Docker Image and BlazeMeter-related Functions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-gitlab-docker-img-and-bzm-related-functions.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-gitlab-docker-img-and-bzm-related-functions.htm"]}`

**GitLab Docker Image and BlazeMeter-related Variables**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-gitlab-docker-img-and-bzm-related-variables.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-gitlab-docker-img-and-bzm-related-variables.htm"]}`

---

## Azure DevOps

Execute BlazeMeter tests via Azure DevOps Pipelines using BlazeMeter Azure DevOps Extension, including creating and running performance tests.

**Use when**: Executing BlazeMeter tests via Azure DevOps Pipelines or using BlazeMeter Azure DevOps Extension to create and run performance tests.

### How to Install the BlazeMeter Extension in Azure DevOps

You need to be a member of the [Project Collection Administrators group](https://learn.microsoft.com/en-us/azure/devops/organizations/security/look-up-project-collection-administrators?view=azure-devops) or an organization owner to install extensions.

For more information, see also [Azure DevOps - Install Extensions (microsoft.com)](https://learn.microsoft.com/en-us/azure/devops/marketplace/install-extension?view=azure-devops&tabs=browser).

1. Log in to your organization's Azure DevOps
2. Click the shopping bag icon and select **Browse Marketplace**
3. Search for BlazeMeter Integration and click **Get it free**
4. Select your organization from the dropdown menu
5. Click **Install** to install and add the extension to your Organization

You can now go to your organization to use the BlazeMeter extension.

### How to Use the BlazeMeter Extension in Azure DevOps

1. Log in to your organization's Azure DevOps
2. Select your project
3. Navigate to **Pipelines -> Releases**
4. Click **+New** and select **New Release Pipeline**
5. On the **Select a template** screen, start with an **Empty Job**
6. Click the text **1 job, 0 task** to add a new task to the stage
7. Click **+** to **Add a task to Agent Job**. When you add a task to the agent job, the **Add tasks** screen appears on your right
8. Search for BlazeMeter to see the **BlazeMeter Integration** extension and add it to the a task

### How to Configure the BlazeMeter Extension to Start a BlazeMeter Test

You have the following options under **Select Tasks**:
- Run Existing Performance Test
- Create Performance Test
- Create Multitest

**Run Existing Performance Test** (default):
1. Enter your **Test URL**. To find your Test URL, log in to your BlazeMeter account. Click **Tests**. Select the test you wish to use. Test details appear. Copy the URL of that page and paste it into the **Test URL** text box
2. For the **API Key** and **API Secret** text box, default values will appear. Note: Azure DevOps supports variables. If you wish to create your own variables and store the API Key and API Secret values within those variables, you may leave the defaults. Alternatively, you can clear the default values and configure the actual API Key and API Secret on the screen
3. (Optional) Define a **Report Name**
4. (Optional) Enable **Use Locations** or **Use Dedicated IPs**. Specify a comma separated list of Private Location names
5. (Optional) For **Do you want to update the test files before the test execution?**, choose one of the following options: No (default), Yes (update main test files and dependencies), or Yes (update several test files using JSON)
6. (Optional) Enable **Show Log** if you want to see a running log of the test in the console
7. (Optional) Enable **Ignore SLA** if you want the build to succeed regardless of the SLA
8. (Optional) Enable **Webhooks**
9. (Optional) If you are not using the load configuration from the JMeter file, define the **Load Configuration**
10. Click **Save**
11. Click **Create Release**
12. Your release is ready
13. Start your BlazeMeter test from the pipeline by clicking the **Deploy** button

**Create Performance Test**:
1. For the **API Key** and **API Secret** text box, default values will appear. Azure DevOps supports the use of variables
2. (Optional) Define a **Report Name**
3. (Optional) Enable **Use Locations** or **Use Dedicated IPs**
4. For **Select uploaded file type**, you can choose one of the following: Upload main test files and its dependencies (default) or Upload several test files using JSON
5. You can update main test files by checking **Update Main Test File**. Then, under **Upload Test Script**, upload the main test file
6. If you want to upload dependencies as well, you have to check **Upload Dependencies**. Then under **Upload Dependent Scripts** you have to upload the dependencies
7. Or, if you select **Upload several test files using JSON**: Upload a JSON file under **Upload JSON File For Update Main Test File Or Upload Dependencies**
8. Specify a Test Name
9. Specify a Project Id

**Create Multitest**:
1. In the Test Name Input field, specify a Test Name
2. In the Project Id field, you have to specify a Project Id
3. In the Multitest File field, upload a multitest JSON file in the specified format

### Define Load Configuration

You can choose whether to use the load configuration from the JMeter file or whether to define it here.

**Load Configuration**:
- **Disable Load configuration** - If you disable this option for an existing JMeter-based test, the load configuration will be taken from the JMeter script. If you enable this option, the values in the following section define the load configuration
- **Total Users** - The target number of users in this performance test
- **Duration** - Defines the target test duration in minutes. Alternatively, define iterations
- **Use Iterations instead** - Enable this option to specify the duration of the test in iterations. Disable this option to specify the duration in minutes
- **Iterations** - The number of iterations to run. Alternatively, define the duration
- **Ram up Time** - The ramp-up time of the performance test in minutes
- **Limit RPS** - You can limit the number of requests per second (RPS) for your test. Default is disabled (empty field). To enable it, use any number greater than 1. Once enabled, use 0 to disable it
- **Ramp Up Steps** - If you configure your test to ramp up in steps, this is the number of steps to reach the total users. Default is disabled (empty field). To enable it, use any number greater than 0. Once enabled, use 0 to disable it
- **Change the number of users at run time** - Enable this option to be able to change the number of users at runtime. Default is false (empty field)

### Using Azure DevOps Variable Groups

1. Log in to Azure DevOps
2. Select your project
3. Navigate to **Pipelines -> Library**
4. On the **Variable Groups** screen, select **+ Variable group**
5. Enter your **Variable group name**. For example: BlazeMeter Keys. The Description is optional
6. Click **+ Add** under Variables
7. Add the two variables APIKEY and APISECRET
8. Click **Save**
9. Return to your Release pipeline by navigating to **Pipelines -> Releases**
10. Select the Pipeline you created. Click **Edit**
11. Once in edit mode, click the **Variables** tab and select **Variable groups**
12. Click **Link variable group**. Select the name of your variable group and click **Link**

Your variable group is now linked with the release pipeline. This allows you to use this variable group inside multiple releases and tasks within the pipeline.

Once you have set your APIKEY and APISECRET as variables, reference them within your tasks as $(APIKEY) and $(APISECRET) respectively.

### Where to View BlazeMeter Test Reports

1. Once a release is successfully deployed, you will see a screen like below. If any failure criteria have been triggered, the task would show up as Failed
2. Click **BlazeMeter Integration** to view the log. The log displays the test Report URL at the beginning of the test execution
3. Navigate to that URL to view the detailed report on BlazeMeter
4. If you enabled the **Show Log** checkbox in your task configuration, you see a detailed log

### Features

- Azure DevOps Extension
- Pipeline task integration
- Test result reporting
- Build status management
- Run existing tests, create new tests, or create multitests
- Variable groups support
- Load configuration options
- File upload and update capabilities

### Documentation References

For detailed information about Azure DevOps integration, use the BlazeMeter MCP help tools:

**Azure DevOps**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-testing-via-azure-devops-pipeline`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-testing-via-azure-devops-pipeline"]}`

---

## AWS CodePipeline

AWS CodePipeline is a continuous delivery and release automation service. One of the great things about CodePipeline is that you very easily integrate external tools into any step of the release process. BlazeMeter, which has been named an AWS partner on CodePipeline, is the go-to choice for load and performance testing.

BlazeMeter enables AWS CodePipeline users to test their web applications easily and rapidly, as part of the Continuous Delivery process. From the CodePipeline console, users can easily connect to BlazeMeter and run tests.

**Use when**: Adding BlazeMeter tests to AWS CodePipeline workflows as testing actions, connecting BlazeMeter account, or running tests as part of continuous delivery.

### Add a BlazeMeter Test to Your Pipeline

1. Start by clicking on the 'AWS CodePipeline' link.
2. Select the Pipeline to which you would like to add a BlazeMeter test and click on 'Edit'.
3. If this is your first Pipeline, click **Create pipeline** and follow the widget. In this view you'll notice the Pipeline and its different stages and actions within them.
4. Click 'Edit' of any stage to see an 'Add action' button which can be added before, after or simultaneously to any other action.
5. Under 'Add Action', choose the 'Test' action.
6. Choose 'BlazeMeter' as 'Test Provider'.
7. Click 'Connect' to connect your BlazeMeter account. You are redirected to BlazeMeter.

If you are not connected, sign in (or sign up).

An account with two tests or less in it will be welcomed by a friendly screen with two options to create a test:

1. A JMeter script upload.
2. A URL test in which all you have to do is, enter a URL to test, the concurrency, and fail criteria. That's it.

### Manage Your Tests

After connecting your BlazeMeter account to your Pipeline, you can see, edit, and connect all of your tests that you've run so far.

- **Name** - The name you gave your test.
- **Location** - The GeoLocation from which you chose the load to originate from.
- **Type** - It can be a JMeter test, API test or Selenium Test.
- **Users/Engines** - The amount of load generators (engines) you chose to test with. If you haven't chosen a certain amount, you will see the number of users your test will load.
- **Fail Criteria** - The number of Thresholds you have set for this test.
- **Last Updated** - The last time you've edited or used this test.
- **Edit Test** - Redirects you to BlazeMeter's platform to this test's configuration page.
- **Connect to AWS Pipeline** - Adds this test as an action to your Pipeline.

After running your test, if any fail criteria have been triggered, you will see the 'BlazeMeter' test action show 'Failed'.

Also you can click on 'Details' and see a Link to the BlazeMeter report.

### Documentation References

For detailed information about AWS CodePipeline integration, use the BlazeMeter MCP help tools:

**AWS CodePipeline**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-testing-via-aws-codepipeline`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-testing-via-aws-codepipeline"]}`

---

## Bamboo

Bamboo is a Continuous Integration tool by Atlassian. Bamboo does more than just run builds and tests. It connects issues, commits, test results, and deploys so the whole picture is available to your entire product team – from project managers to devs and testers, to system admins.

The BlazeMeter plug-in to Bamboo allows you to load test your site using BlazeMeter, as part of your Continuous Integration/Delivery(CI/CD) process.

**Use when**: Using BlazeMeter plugin for Atlassian Bamboo to load test sites as part of CI/CD process, viewing reports, setting build status, or integrating performance testing into Bamboo workflows.

When using the plugin, Bamboo will show a report generated by the BlazeMeter test, and based on the results it will set the final build status as good or failed.

This plug-in works on Bamboo Server instance as well as remote agents.

### How to Install BlazeMeter's Plugin for Bamboo

1. Login to Bamboo and go to your dashboard. Click on the cog in the top right corner, and choose 'Overview'.
2. Scroll down to the Add-ons section on the left-hand side, and select 'Find new add-ons.'
3. In the search bar, search for BlazeMeter. You should see the 'BlazeMeter test trigger' pop up.
4. Click the Install button to install the BlazeMeter plugin.

### How to Configure BlazeMeter's Plugin for Bamboo

1. Once installed, click the cog in the upper right-hand corner and select 'Overview.'
2. On the left-hand side of the screen, you will see a section 'BlazeMeter Administration' is now present. Click on the 'Settings page'.
3. Enter your API key ID and API key secret from your BlazeMeter account (API key ID & API key secret can be found following [BlazeMeter API keys guide](skill-blazemeter-api-reference://references/authentication.md)), and in the 'Server URL', enter [https://a.blazemeter.com](https://a.blazemeter.com) and click the Save button.

### Troubleshooting Bamboo BlazeMeter Plugin

If the BlazeMeter plugin is having issues installing, try the following steps to resolve the issue:

1. Stop Bamboo.
2. Download the BlazeMeter plugin manually from the Atlassian Marketplace by clicking the 'Get it now' button, at this link: [https://marketplace.atlassian.com/plugins/com.blazemeter.bamboo.plugin.BlazeMeterBamboo/server/overview](https://marketplace.atlassian.com/plugins/com.blazemeter.bamboo.plugin.BlazeMeterBamboo/server/overview)
3. Go to the plugins folder ($BAMBOO_HOME/plugins or it can be in user-data-dir .atlassian/bamboo/plugins) and remove all BlazeMeter*.jars (if any).
4. Copy the downloaded *.jar from Step 2 to this location.
5. Start Bamboo.

### How to Configure a Job Using BlazeMeter's Bamboo Plugin

1. Edit an existing plan or create a new one, then click on a stage.
2. Click the 'Add task' button, under the 'Tasks' tab.
3. Search for BlazeMeter, or look for BlazeMeter Test and click it.

### Setting Up the Plan's Test

1. If your settings were pre-configured correctly in the global settings, you will now see all your tests in the drop-down menu 'BlazeMeter tests.'
2. Select a test to run.
3. You can enter session properties in "Send jmeter properties to test" field in the following format: `key=value,key1=value1,key2=value2`. Sending properties for test session is currently not supported for Taurus & multi tests.
4. "Add notes to test report" textarea allows to set notes, which will be visible at test report dashboard after starting the test. Note that Bamboo variables, e.g. `${bamboo.planKey}` will be resolved. More information on this is available [here](https://confluence.atlassian.com/bamboo/bamboo-variables-289277087.html)
5. Save your settings.
6. Make sure your plan is enabled, and you are ready to run.

### Reports

Plugin downloads two kind of reports after test session was over: `junit` & `jtl`.

- `junit` report contains data which is compatible with [any junit parser](https://www.junit.org/)
- `jtl` report contains data in [Apache Jmeter jtl format](https://wiki.apache.org/jmeter/JtlFiles)

`Download JTL report` & `Download Junit report` check-boxes are used for configuring whether or not reports should be downloaded. By default, reports are downloaded to `${BAMBOO_HOME}|${BAMBOO_AGENT_HOME}/xml-data/build-dir<PLAN_ID> - <PROJECT_ID> - <JOB_ID>/<build-number>`. User can override this path in task configuration(`Path to JTL report` & `Path to Junit report` fields) both with absolute and relative paths. Also [Bamboo variables](https://confluence.atlassian.com/bamboo/bamboo-variables-289277087.html) can be used in paths.

### Running a Build with BlazeMeter's Bamboo Plugin

1. Once inside your plan, click the 'Run' drop down and click 'Run Plan'
2. Once the build begins, it will take you to the following screen, showing you the console, where you can see the progress of your build.
3. When the test finishes, you will see a summary of the build. Also you will find the 'BlazeMeter Test Report' tab on your build page. It contains the link to the BlazeMeter report page.

### Working with Proxy Server

**Set up proxy on Atlassian Bamboo server:**
Add to `$BAMBOO_HOME/conf/catalina.properties` the following:
```
http.proxyHost=<IP>
http.proxyPort=<PORT>
http.proxyUser=<USER>
http.proxyPass=<PASSWORD>
```

**Set up proxy on Atlassian Bamboo remote agent:**
Open `${BAMBOO_REMOTE_AGENT_HOME}/conf/wrapper.conf`
Add the following entries to it:
```
wrapper.java.additional.3=-Dhttp.proxyHost=<proxyIP>
wrapper.java.additional.4=-Dhttp.proxyPort=<proxyPort>
wrapper.java.additional.5=-Dhttp.proxyUser=<proxyName>
wrapper.java.additional.6=-Dhttp.proxyPass=<proxyPass>
wrapper.java.additional.7=-Dhttp.nonProxyHosts=<AtlassianBambooServerHost>
```

### Pass/Fail Build Criteria

Plugin is using `/ci-status` request for setting build result. Depending on this request, plugin sets one of the available in Bamboo build result:

**SUCCESS**: This status is set in next cases:
- test has no thresholds;
- test has thresholds and they were not violated;
- there were no errors in `ci-status` response;

**ERROR**:
- test was completed successfully, but there were errors in `/ci-status` response;

**FAILED**:
- test has thresholds and they were violated;
- Bamboo job got error on `/test/start` request;
- test has no thresholds, but there were specific errors in `/ci-status` response: `"errors":[{"code": 70404,"message": "Session ended without load report data","details": null}]` `"errors":[{"code":0,"Message":"Not enough resources"}]`

### Logging

Plugin has separate log file, which can simplify debugging process in case of any issues with running test.

`http-log` - contains plugin - BlazeMeter server communication.

It's located in (`$BAMBOO_HOME`/`$BAMBOO_AGENT_HOME`)`xml-data/build-dir/<PLAN_ID> - <PROJECT_ID> - <JOB_ID>/build # <buildId>/http-log`

If build was interrupted at the Bamboo server side, log will be available using link `<server-host>/browse/<PLAN_ID> - <PROJECT_ID>-<JOB_ID>-<BUILD_ID>/log`. E.g. if you have plan `123` with project `234` with single job inside it, than log link will be `<server-host>/browse/123-234-JOB1-<BUILD_ID>/log`

### Changelog

For the latest changelog, see [https://github.com/Blazemeter/blazemeter-bamboo-plugin/blob/master/Changelog.md](https://github.com/Blazemeter/blazemeter-bamboo-plugin/blob/master/Changelog.md)

### Documentation References

For detailed information about Bamboo integration, use the BlazeMeter MCP help tools:

**Bamboo**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-plugin-to-bamboo`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-plugin-to-bamboo"]}`

---

## TeamCity

BlazeMeter has a plugin to TeamCity to simplify your load testing needs. You only need to connect your BlazeMeter account to TeamCity, configure a simple build step and you are good to go. You can configure TeamCity to run the BlazeMeter build step whenever you want, and the test will start with your pre-configured settings.

**Use when**: Using BlazeMeter plugin for TeamCity to simplify load testing needs, configuring build steps, viewing test reports in TeamCity, or integrating performance testing into TeamCity CI/CD workflows.

### What is TeamCity

TeamCity is a user-friendly continuous integration (CI) server for professional developers and build engineers working on .NET, Java, and Ruby projects.

### How to Install BlazeMeter's Plugin for TeamCity

1. Download the [TeamCity (JetBrains)](https://plugins.jetbrains.com/plugin/9020-blazemeter) plugin.
2. Here are two different ways to install the plugin:
   - **From UI**: The plugins installation page is accessible in TeamCity from the 'Administration' section, in the 'Plugins List' link on the left side of the screen.
   - **Manual Installation**: Copy the 'BlazeMeter.zip' file to the 'TeamCity Data Folder/plugins' directory, and restart the TeamCity server and agents.

**Example manual installation:**
```bash
$ ../TeamCity/bin/teamcity-server.sh stop
$ cp blazemeter.zip /Users/Blazy/.BuildServer/plugins
$ ../TeamCity/bin/teamcity-server.sh start
```

### How to Configure BlazeMeter's Plugin for TeamCity

First, Get the BlazeMeter user key. [How to get the API Key?](skill-blazemeter-api-reference://references/authentication.md)

1. The plugin's configuration page is accessible in TeamCity from the 'Administration' section, in the 'BlazeMeter' link on the left side of the screen.
2. Please set the 'BlazeMeter URL' field to [https://a.blazemeter.com](https://a.blazemeter.com)

### How to Configure a Build Using BlazeMeter's Plugin for TeamCity

Add a new build step with type 'BlazeMeter'.

1. If your keys were pre-configured in the global settings, you will now see all your tests in the drop down. Select a test to run.
2. Set the path for JUnit/JTL files. (Optional)
3. Add notes to your test (Optional). Notes will be visible at test report dashboard after starting the test. Note, that there is an ability to use TeamCity predefined variables, e.g. `%teamcity.version%`. More information on this is available [here](https://confluence.jetbrains.com/display/TCD10/Predefined+Build+Parameters)
4. Add JMeter Properties to your test. (Optional) Format of session properties: `key=value,key1=value1,key2=value2`. Sending properties for test session is currently not supported for Taurus & Multi tests.
5. Make sure to 'Save' your settings
6. When the test finished, you will see a summary of the build. Also you will find the 'BlazeMeter Test Report' tab on your build page. It contains the link to the BlazeMeter report page.

The TeamCity agent will wait for test results before being freed up to run any other task. This is a limitation of TeamCity and not the plugin. The only way to work around this limitation is to have multiple agents assigned to your test pool.

### JUnit/JTL Reports

The plugin downloads two kinds of reports after the test session ends: `junit` & `jtl`. The `junit` report contains data which is compatible with [any junit parser](https://www.junit.org/), while the `jtl` report contains data in [Apache Jmeter jtl format](https://wiki.apache.org/jmeter/JtlFiles).

The `Download JTL report` & `Download Junit report` checkboxes are used for configuring whether or not reports should be downloaded. By default, reports are downloaded to `${TEAMCITY_AGENT_HOME}/work/<unique-build-id-assigned-by-teamcity>`. The user can override this path in the task configuration(`Path to JTL report` & `Path to Junit report` fields), each with absolute and relative paths. [TeamCity variables](https://confluence.jetbrains.com/display/TCD10/Predefined+Build+Parameters) can likewise be used in paths.

### How to Configure Your Proxy Server Settings in TeamCity

**Set up proxy on teamcity server:**
Add to `$TEAMCITY_HOME/conf/catalina.properties` the following:
```
http.proxyHost=<IP>
http.proxyPort=<PORT>
http.proxyUser=<USER>
http.proxyPassword=<PASSWORD>
```

**Set up proxy on teamcity agent (repeat on every agent, if needed):**
- Edit `$TEAMCITY_AGENT_HOME/bin/agent.sh`
- Find `$TEAMCITY_AGENT_OPTS_ACTUAL` and change it to the following:
```bash
TEAMCITY_AGENT_PROXY_OPTS="-Dhttp.proxyHost=<IP> -Dhttp.proxyPort=<PORT> -Dhttp.proxyUser=<USER> -Dhttp.proxyPass=<PASSWORD>"
TEAMCITY_AGENT_OPTS_ACTUAL="$TEAMCITY_AGENT_OPTS -ea $TEAMCITY_AGENT_MEM_OPTS_ACTUAL -Dteamcity_logs=$LOG_DIR/ $TEAMCITY_AGENT_PROXY_OPTS"
```
- Make sure that these options are passed to the JVM;

### Pass/Fail Build Criteria

The Plugin is using a `/ci-status` request for setting the build result. Depending on this request, the plugin sets one of the following statuses in the TeamCity build result:

**FINISHED_SUCCESS**: This status is set in the following cases:
- test has no thresholds;
- test has thresholds and they were not violated;
- there were no errors in `ci-status` response;

**FINISHED_WITH_PROBLEMS**:
- test was completed successfully, but there were errors in `/ci-status` response;

**FINISHED_FAILED**:
- Test has thresholds and they were violated;
- TeamCity job got error on `/test/start` request;
- Test has no thresholds, but there were specific errors in the `/ci-status` response: `"errors":[{"code": 70404,"message": "Session ended without load report data","details": null}]` `"errors":[{"code":0,"Message":"Not enough resources"}]`

### Logging

The Plugin has a separate log file, which can simplify the debugging process in case of any issues with the running test.

`bzm-log` - contains the plugin-BlazeMeter server communication.

It's located in `$TEAMCITY_AGENT_HOME/logs/<project-id>/<buildId>/bzm-log`

### Changelog

For the latest changelog, see [https://github.com/Blazemeter/blazemeter-teamcity-plugin/blob/master/CHANGELOG.md](https://github.com/Blazemeter/blazemeter-teamcity-plugin/blob/master/CHANGELOG.md)

### Documentation References

For detailed information about TeamCity integration, use the BlazeMeter MCP help tools:

**TeamCity**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-teamcity-plugin`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-teamcity-plugin"]}`

---

## CircleCI

Integrate BlazeMeter tests with CircleCI builds using Python scripts and Trigger URLs to change build status based on test results.

**Use when**: Integrating BlazeMeter tests with CircleCI builds or using Python scripts and Trigger URLs to change build status based on test results.

### Configuration Steps

1. **Set Up Environment Variables**: Add BlazeMeter API credentials as environment variables
2. **Create Workflow**: Create CircleCI workflow configuration
3. **Add Test Job**: Add job to execute BlazeMeter test
4. **Use Trigger URLs**: Configure Trigger URLs for test execution
5. **Set Build Status**: Configure build status based on results

### Features

- Workflow integration
- Trigger URL support
- Python script support
- Build status management

---

## Codeship

Integrate BlazeMeter tests with Codeship builds, including Codeship Pro with Docker support, using Python scripts and Trigger URLs.

**Use when**: Integrating BlazeMeter tests with Codeship builds or using Codeship Pro with Docker support, Python scripts, and Trigger URLs.

### Configuration Steps

1. **Set Up Environment Variables**: Add BlazeMeter API credentials as environment variables
2. **Create Pipeline**: Create Codeship pipeline configuration
3. **Add Test Step**: Add step to execute BlazeMeter test
4. **Configure Docker** (Codeship Pro): Set up Docker environment if needed
5. **Set Build Status**: Configure build status based on results

### Features

- Pipeline integration
- Docker support (Codeship Pro)
- Trigger URL support
- Build status management

---

## ShiftLeft Converter for LoadRunner

Convert LoadRunner HTTP to JMeter and LoadRunner TruClient to Selenium, or SOAPUI scenarios to Taurus and BlazeMeter using the free Script Converter.

**Use when**: Converting LoadRunner HTTP to JMeter and LoadRunner TruClient to Selenium or converting SOAPUI scenarios to Taurus and BlazeMeter using the free Script Converter.

The [Free Script Converter](https://shiftleft.blazemeter.com/) can convert LoadRunner HTTP to [JMeter](http://jmeter.apache.org/) and LoadRunner TruClient to [Selenium](http://www.seleniumhq.org/) in a short time, as well as SOAPUI scenario(s) to [Taurus](http://gettaurus.org/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and [BlazeMeter](http://www.blazemeter.com/signup?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes).

### Convert to JMeter

You can convert the tests assuming only HTTP(S) protocols (and derivatives). In LoadRunner terms, these are:
- Web - HTTP/HTML
- Web Services
- RTE
- Winsock
- MQ
- JMS
- Soap

**Prerequisites**: You have JMeter installed.

**Follow these steps:**

1. Go to [https://shiftleft.blazemeter.com](https://shiftleft.blazemeter.com/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and upload the ZIP file
2. Open the test in BlazeMeter and download the zip file that contains all converted assets
3. Open the downloaded file, and open the folder named "Your JMeter or Selenium Scripts"
4. Copy the JMX file to a folder on your computer
5. Open the JMX file in JMeter, and adjust the script if you needed, and run it

### Convert to Taurus

With the Script Converter, you can convert your tests to Taurus, an open-source automation framework. Taurus allows you to run and automate open-source tests and view analytics. For more information about Taurus, see [gettaurus.org](http://gettaurus.org).

**Prerequisites**: You have JMeter installed.

**Follow these steps:**

1. Go to [https://shiftleft.blazemeter.com](https://shiftleft.blazemeter.com/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and upload the ZIP file
2. Open the test in BlazeMeter and download the zip file that contains all converted assets
3. Copy the YML and .TXT files, and put these in the same folder in your computer. Adjust the YML file in your Text editor of choice, if needed
4. [Install Taurus](http://gettaurus.org/install/Installation/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) if necessary
5. Run the command $ bzt <your_filename.yml>
6. View and analyze the results

You just ran your LoadRunner file in Taurus.

### Convert to BlazeMeter

**Prerequisites**: You have JMeter installed.

You can convert LoadRunner scripts to BlazeMeter.

1. Go to [https://shiftleft.blazemeter.com](https://shiftleft.blazemeter.com/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and upload the ZIP file
2. Open the test in BlazeMeter and download the zip file that contains all converted assets
3. Configure your tests from the converted ZIP file, either:
   - Extract the JMX and [create a JMeter test](https://help.blazemeter.com/docs/guide/performance-create-jmeter-test.html); OR
   - Extract the YML and [create a Taurus test](https://help.blazemeter.com/docs/guide/performance-create-taurus-test.html)
4. In BlazeMeter, the "Test History" tab displays various details such as the Test execution engine is used, the number of Concurrent Users/Threads, and the available Locations and providers (AWS, Google, Azure) from where the tests can be executed
5. Launch the test for the default duration of 20 mins

You can now view the test results on BlazeMeter.

### Supported Files and Functions

See [a list of supported files and functions (LoadRunner HTTP and TruClient)](https://help.blazemeter.com/docs/guide/integrations-shiftleft-files-and-functions.html)

### Resolve Errors

- See [how to resolve errors in ShiftLeft Converter](https://help.blazemeter.com/docs/guide/integrations-shiftleft-converter-troubleshooting.html)
- To report issues in BlazeMeter, contact [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com)

For more information about converting scripts to Selenium, see [Convert LoadRunner to Open-Source Selenium in Minutes](https://www.blazemeter.com/blog/convert-loadrunner-to-open-source-selenium-in-minutes).

### Conversion Types

- **LoadRunner HTTP → JMeter**: Convert LoadRunner HTTP scripts to JMeter
- **LoadRunner TruClient → Selenium**: Convert LoadRunner TruClient scripts to Selenium
- **SOAPUI → Taurus**: Convert SOAPUI scenarios to Taurus YAML

### Best Practices

- Review converted scripts before use
- Test converted scripts thoroughly
- Update scripts as needed after conversion
- Document conversion process

---

## Best Practices

- **Secure Credentials**: Store CI/CD credentials securely
- **Test Integration**: Test CI/CD integration before production use
- **Set Appropriate Thresholds**: Configure meaningful pass/fail criteria
- **Monitor Results**: Regularly review test results in CI/CD pipelines
- **Document Configuration**: Document CI/CD integration setup

---

## Documentation References

For detailed information about CI/CD integrations, use the BlazeMeter MCP help tools:

**CI/CD Integrations**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**:
  - `integrations-blazemeter-jenkins-plugin-guide` (Jenkins)
  - `integrations-blazemeter-plugin-to-bamboo` (Bamboo)
  - `integrations-blazemeter-teamcity-plugin` (TeamCity)
  - `integrations-shiftleft-converter-for-loadrunner` (ShiftLeft Converter)
  - `integrations-testing-via-aws-codepipeline` (AWS CodePipeline)
  - `integrations-testing-via-azure-devops-pipeline` (Azure DevOps)
  - `integrations-blazemeter-add-load-tests-to-CI-CD.htm` (Add to CI/CD Pipeline)
  - `integrations-run-bzm-tests-from-github-actions.htm` (GitHub Actions)
  - `integrations-github-actions-and-bzm-related-functions_.htm` (GitHub Actions Functions)
  - `integrations-github-actions-and-bzm-related-variables.htm` (GitHub Actions Variables)
  - `integrations-run-bzm-tests-from-gitlab-ci-cd.htm` (GitLab CI/CD)
  - `integrations-gitlab-docker-img-and-bzm-related-functions.htm` (GitLab Functions)
  - `integrations-gitlab-docker-img-and-bzm-related-variables.htm` (GitLab Variables)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-jenkins-plugin-guide", "integrations-blazemeter-plugin-to-bamboo", "integrations-blazemeter-teamcity-plugin", "integrations-shiftleft-converter-for-loadrunner", "integrations-testing-via-aws-codepipeline", "integrations-testing-via-azure-devops-pipeline", "integrations-blazemeter-add-load-tests-to-CI-CD.htm", "integrations-run-bzm-tests-from-github-actions.htm", "integrations-github-actions-and-bzm-related-functions_.htm", "integrations-github-actions-and-bzm-related-variables.htm", "integrations-run-bzm-tests-from-gitlab-ci-cd.htm", "integrations-gitlab-docker-img-and-bzm-related-functions.htm", "integrations-gitlab-docker-img-and-bzm-related-variables.htm"]}`

