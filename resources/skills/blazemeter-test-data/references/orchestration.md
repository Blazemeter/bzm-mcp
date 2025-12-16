# Test Data Orchestration

## Test Data Orchestration

Prepare test environments using Test Data Orchestration, including API requests for create/read/update/delete operations, cleanup requests, data targets, and environment preparation before/after test runs.

**Use when**: Preparing test environments using Test Data Orchestration or setting up API requests for create/read/update/delete operations and cleanup requests.

### Overview

When you have the recurring need to satisfy data dependencies in your test environment, use BlazeMeter's test data orchestration. The orchestration can create, read, update, and delete test data in your test environment *before* and *after* each test run. BlazeMeter can [generate test data](https://help.blazemeter.com/docs/guide/test-data-how-to-use.html) that drives the test according to your requirements; but some tests additionally depend on consistent data in the test environment.

**Usage example**: You use orchestration before the test run to seed the test environment with users. BlazeMeter does not have access to your application's business logic and therefore cannot guess or generate your proprietary user keys synthetically. In your Data Model, leave the Data Parameter for the proprietary userKey empty and have the orchestration initialize it later, before the test run. The orchestration's ability to *read* and store values (such as userKeys) from API responses ensures consistency between the seeded data and the tests.

**Examples of data dependencies include:**
- To test object reading, object deletion, or object updating, these objects must first be *created* in the test environment
- To test unique object creation, the test environment must be a clean slate; objects from previous tests must be *deleted*
- To amend your data model with unique generated IDs, you need the ability to *read* values from the test environment
- The test data row used in the test must be the same as the one used in the test environment

In these test situations, you want to prepare the environment *before* and *after* each test run. The orchestration relies on the APIs of your application under test.

### Benefits

Using Test Data Orchestration has the following benefits:
- Orchestration is available to GUI Functional tests and Performance tests as part of the Test Data integration
- Orchestration maintains data consistency by using existing data models in related tests
- Orchestration can be automated to run together with test execution
- Different kinds of test data can be part of the same data model. Examples: Test data can be generated synthetically or loaded from CSV files; other values can be defined by reading existing values from your test environment

BlazeMeter makes it easy for you to use the same data consistently and helps you manage the state of your test environments in context.

### Requirements

BlazeMeter relies on the application programming interface (API) of your web application. Familiarize yourself with your application's data model, endpoints, authentication, and usage.

If your application is only reachable within your premises, you must create a Private Location agent with **Data Orchestration** functionality enabled. Select this Private Location as your Publish Execution Location in the Data Target Settings.

Using Test Data Orchestration is well integrated with test data from Test Data Entities. This article assumes that you understand test data concepts and know how to create it. To learn more, see [How to Use Test Data](https://help.blazemeter.com/docs/guide/test-data-how-to-use.html).

Some advanced orchestration features, such as bulk publishing, require scripting knowledge. Testers without scripting experience can use the base functionality in the BlazeMeter web interface.

**To create a Private Location with Data Orchestration:**
1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Go to **Settings > Workspace > Private Locations**
3. Click the **Plus** to add a new Private Location and configure it as needed
4. Under **Functionalities**, enable the **Data Orchestration** toggle
5. Click **Apply**

### Concepts

- *API Requests* create, read, update, or delete data in a test environment *before* the test runs
- *Clean Up Requests* create, read, update, or delete data in a test environment *after* the test runs
- *Data Targets* are containers for API Requests, Clean Up Requests, and their settings. A test can have zero, one, or more Data Targets associated. A Data Target can be associated with several tests

**This article covers the following topics:**
- Introduction, Benefits, Videos, Requirements, Concepts
- How to prepare your test environment (create Data Target, define API requests, define clean up requests, define settings, run orchestration adhoc, run orchestration automatically, review log files)
- Usage scenarios (reference test data, extract response values, handle exceptions, publish data in bulk)
- Variables and functions (prefixes) reference

---

## Profiler

Automatically detect and parameterize hard-coded values in test scripts using the Data Profiler, including data type prediction, generator function suggestions, and automated data creation wizard.

**Use when**: Automatically detecting and parameterizing hard-coded values in test scripts or using data type prediction, generator function suggestions, and automated data creation wizard.

### Overview

The Data Profiler helps you parameterize Performance tests, Functional tests, and Service Virtualization.

One way to parameterize a test is that you manually replace hard-coded values by [Data Parameters](https://help.blazemeter.com/docs/guide/test-data-what-are-data-entities-data-parameters.html) and load values from a CSV file or using synthetic data generation functions. The **Automatic Data Creation Wizard** speeds up the manual parts of this process for you.

The Data Profiler is available for the following test types:
- Performance tests (JMX files) that contain hard-coded values, or whose CSV Data Set Configurations are linked to a static CSV file
- Functional tests (Taurus YAML files) that contain hard-coded values
- virtual services that contain hard-coded values

### What is Data Profiling?

BlazeMeter can automatically detect hard-coded values in your test scripts and replace them with dynamic Data Parameters. The advantage of dynamic test data is that you can extend it to any quantity, quality, and coverage. Feel free to run the wizard and see what it suggests; you can leave the wizard any time without making changes to your test. You can also choose to accept only a partial parameterization of a few values and keep the rest untouched. At any point you are in control: You can see which hard-coded values have been detected and how certain the type prediction is. Patterns such as common names are detected with higher certainty, while the type of anonymous numbers or unknown strings are detected with lower certainty.

- For each hard-coded value, you choose whether you want to replace it by a dynamic parameter or keep the existing static data untouched
- For each data parameter, you can review the suggested generator function and preview example values

You can edit or replace suggested generator functions right in the wizard — or manually edit it any time later, after closing the Data Profiler, in the Test Data pane.

### How to Create Test Data Based on Hard-Coded Values

The Data Profiler can generate test data for tests or Virtual Service transactions that contain hard-coded values and have no test data associated yet. You can also profile attached CSV or JMX files and so on. After running the Profiler, you can choose to accept the default suggestions, customize the changes, or cancel without making any changes.

By default, based on the characteristics of the hard-coded values found, the Profiler offers to generate a suitable number of rows of synthetic data; the Profiler makes a backup of your files and replaces hard-coded values by parameters that loop over generated values. You can customize these settings and choose which values to parameterize and which not.

1. Open the test or transaction
2. Click the **Data Creation Wizard** button next to the closed **Test Data / Service Data** button. The **Automatic Data Creation Wizard** opens and lists the hard-coded values that it detected in your test
3. (Optional) Choose whether you want **AI Enabled** for test data generation. To learn more, see [Test Data Pro](https://help.blazemeter.com/docs/guide/test-data-pro.html)
4. (Optional) Review the number of rows: By default, BlazeMeter generates 10 rows of test data. If you want more or fewer rows, click **Change Number of Rows**: Under **Number of Rows**, specify how much data you want to generate. (CSV file only) Choose one of the following **Data Creation Options**: **By Replacing CSV** The test uses synthetic values *in place* of the hard-coded columns in the CSV file. The CSV file itself is not edited. **By Extending CSV** The test uses synthetic values *in addition* to the hard-coded columns in the CSV file. The CSV file itself is not edited. Click **Save**
5. (Optional) Review your file parameterization options. By default, BlazeMeter creates a data entity with data parameters and does *not* replace the hard-coded values. Choose one of the following options: Parameterize Test and Back Up Original, Parameterize Test Without Backup, Don't Parameterize Test (Create Test Data Definitions only). Click **Save**
6. Verify that the detected **Field Name**, the **Original Hard-coded Value**, and its **Data Type Prediction** match your expectations. If the shown example is not unique for a field, click **Show All Values...** for more examples
7. Verify whether the **Suggested Data Generator Function** and its **Generated Data Example** match your expectations
8. (Optional) If a prediction or function is not applicable, click **Change Test Data Suggestions**: Select the checkboxes for the values that you want to replace by synthetic test data. (Optional) Clear the checkboxes for the hard-coded values that you want to leave untouched. Select a more appropriate **Data Type Prediction** from the menu. The profiler suggests a new synthetic function. Experienced users can select the **User Defined** option and edit the function and its arguments inline. To learn more, see [Data Generator Functions](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html). Click **Save**
9. Review the **Data Entity Preview**
10. Click **Save**

To leave your test or virtual service unchanged, you can click **Cancel** any time.

If you have chosen parameterization, the selected values in your script or in your Virtual Service Transactions, respectively, are now replaced by Data Parameters. If your data contained CSV files, BlazeMeter creates Data Entities for each CSV file. The attached CSV files themselves are not edited; BlazeMeter creates Data Parameters that override (extend or replace) columns in attached CSV files.

After you close the **Automatic Data Creation** wizard, you return to the **Test Configuration** page.
- You can change your test data any time in the Test Configuration on the **Test Data** pane
- You can change your service data any time later in the Virtual Service Asset Catalog by clicking the **Service Data** button

---

## Documentation References

For detailed information about test data orchestration, use the BlazeMeter MCP help tools:

**Test Data Orchestration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `test-data-orchestration` (orchestration), `test-data-profiler` (profiler)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-orchestration", "test-data-profiler"]}`

