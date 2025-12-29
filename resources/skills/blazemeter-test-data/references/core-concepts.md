# Test Data Core Concepts

## What are Data Entities and Data Parameters

Understand the concepts of data entities and data parameters in BlazeMeter, including parameter naming, scopes, entity containers, sharing, exporting, and data variants.

**Use when**: Understanding the concepts of data entities and data parameters in BlazeMeter or learning about parameter naming, scopes, entity containers, sharing, exporting, and data variants.

### What are Data Parameters?

Test steps often rely on variable values: In a test case for a web application, you select an *item* from a combobox, you type a *username*, you select *a number* of minutes to wait, and so on. You can either hard-code these parameter values, or fill them with variable test data. The advantage of replacing hard-coded values with Data Parameters is that the same test can iterate over rows of test data multiple times and perform test runs with a fresh set of values each time.

In BlazeMeter, the first letter of a Data Parameters is always a dollar sign, and the parameter name is surrounded by two braces. The name can only contain alphanumeric characters and the underscore character. The Parameter name cannot begin with a number. Parameter names must be unique within each test; if you attach a CSV file, BlazeMeter generates unique names for its columns and show them in the Test Data pane.

**Example:**
```
${my_variable}
```

To initialize a Data Parameter with test data, choose one of the following data sources:
- [Load Test Data from CSV Spreadsheets](https://help.blazemeter.com/docs/guide/test-data-load-from-spreadsheets.html)
- [Generate Synthetic Test Data](https://help.blazemeter.com/docs/guide/test-data-generate-synthetic.html)

When you load shared test data from the workspace into a test, you can still edit and *override* parameter values in your test. These "local" changes are not shared until you save them to the workspace. Local Parameter overrides can be helpful for one-off tests or temporary exceptions that you do not want to propagate to other team members' tests.

A data parameter can have the following scopes within a test:
- The data parameter is defined only in this test and not shared with the workspace
- The data parameter is loaded from the workspace and has not been changed
- The data parameter is loaded from the workspace and has been changed (overridden) for this test

Data parameters are defined in data entities.

### What are Data Entities?

In BlazeMeter, a Data Entity contains Data Parameters. A Data Entity can contain one or more Data Parameters from various data sources. GUI Functional tests support only a single Data Entity, Performance tests support multiple Data Entities.

You can save and load Data Entities within a workspace. Saving and loading is useful when you need to swap out different sets of test data, for example, you can load separate Data Entities for different geographies, or for minimal versus full test coverage, and so on. You reset locally overridden parameters by reverting to the original Data Entity.

Data entities can be exported in zip file format so you can back them up in an external version control system. You also use the exported files to move Data Entities between workspaces and accounts.

### What are Data Variants?

Data Variants help you create various instances of the same Data Entity, so that you can easily switch between them. The variants can be shared within the workspace as well, ensuring consistency. To learn more, see [Test Data Variants](https://help.blazemeter.com/docs/guide/test-data-variants.html).

---

## How to Use

Use test data in BlazeMeter tests, including parameterizing test cases, storing data parameters in data entities, and using shared test data consistently.

**Use when**: Using test data in BlazeMeter tests or parameterizing test cases, storing data parameters in data entities, and using shared test data consistently.

### Overview

Test steps often rely on [data parameters](skill-blazemeter-test-data://references/core-concepts.md), such as menu item names, usernames, or numeric values. You can either hard-code these values, or *parameterize* your test cases to use different variable values. You store these Data Parameters in Data Entities. BlazeMeter's test data integration helps you use shared test data consistently across all tests and virtual services.

### Parameterizing Test Cases

1. **Create Data Entity**: Create or select data entity. A Data Entity contains Data Parameters and can contain one or more Data Parameters from various data sources. GUI Functional tests support only a single Data Entity, Performance tests support multiple Data Entities
2. **Define Parameters**: Define parameters in entity. In BlazeMeter, the first letter of a Data Parameter is always a dollar sign, and the parameter name is surrounded by two braces (e.g., `${my_variable}`). The name can only contain alphanumeric characters and the underscore character. The Parameter name cannot begin with a number. Parameter names must be unique within each test
3. **Reference in Tests**: Reference parameters in test scripts using the `${parameter_name}` syntax
4. **Execute Tests**: Run tests with parameterized data. The same test can iterate over rows of test data multiple times and perform test runs with a fresh set of values each time

### Storing Data Parameters

- **Entity Storage**: Store parameters in data entities. You can save and load Data Entities within a workspace. Saving and loading is useful when you need to swap out different sets of test data, for example, you can load separate Data Entities for different geographies, or for minimal versus full test coverage
- **CSV Files**: Import data from CSV files. If you attach a CSV file, BlazeMeter generates unique names for its columns and shows them in the Test Data pane. See [Load Test Data from CSV Spreadsheets](https://help.blazemeter.com/docs/guide/test-data-load-from-spreadsheets.html)
- **Synthetic Generation**: Generate data using functions. See [Generate Synthetic Test Data](https://help.blazemeter.com/docs/guide/test-data-generate-synthetic.html)

### Using Shared Test Data

- **Consistent Data**: Use same data across multiple tests. When you load shared test data from the workspace into a test, you can still edit and *override* parameter values in your test. These "local" changes are not shared until you save them to the workspace. Local Parameter overrides can be helpful for one-off tests or temporary exceptions that you do not want to propagate to other team members' tests
- **Data Sharing**: Share entities within workspace. Data entities can be exported in zip file format so you can back them up in an external version control system. You also use the exported files to move Data Entities between workspaces and accounts
- **Data Reuse**: Reuse data entities in different test types. You reset locally overridden parameters by reverting to the original Data Entity

---

## Share

Share test data across test types and workspaces, including sharing CSV spreadsheets and data entities within workspaces and exporting/importing between workspaces.

**Use when**: Sharing test data across test types and workspaces or sharing CSV spreadsheets and data entities within workspaces and exporting/importing between workspaces.

### Sharing Within Workspace

- **Entity Sharing**: Share data entities within workspace
- **Spreadsheet Sharing**: Share CSV spreadsheets within workspace
- **Team Collaboration**: Collaborate on shared test data

### Export/Import Between Workspaces

- **Export Data**: Export entities and spreadsheets
- **Import Data**: Import data into other workspaces
- **Cross-Workspace**: Share data across workspace boundaries

### Documentation References

For detailed information about sharing test data, use the BlazeMeter MCP help tools:

**Share Test Data**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `test-data-share`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-share"]}`

---

## How to Parameterize

Parameterize test cases using data entities and parameters, including configuring parameter references and data-driven testing. Parameterization means replacing hard-coded values with Data Parameters that load data from other sources. BlazeMeter stores Data Parameters in [Data Entities](skill-blazemeter-test-data://references/management.md).

**Use when**: Parameterizing test cases using data entities and parameters or configuring parameter references and data-driven testing.

### When to Choose Which Option?

Parameterize your test cases to be able run the same test with different values:

- **Is your test data a list of fixed values? Are there fixed dependencies between columns?** Collect your data in [spreadsheet columns](skill-blazemeter-test-data://references/core-concepts.md) and attach the CSV file to the test
- **Do you need varied, dynamic test data?** [Generate test data synthetically](skill-blazemeter-test-data://references/generation.md) that looks like real or random data, but you have full control over its form

### Parameterization Options

You have the following options to store values:

- **Hard-coded values**: Static values directly in test scripts
- [Load Test Data from Spreadsheets](skill-blazemeter-test-data://references/core-concepts.md) (parameterization)
- [Generate Synthetic Test Data](skill-blazemeter-test-data://references/generation.md) (parameterization)
- Or any combination thereof

### Name Data Parameters Uniquely

Test Data Parameter names have to be unique across all Data Entities in your test. If two parameters have the same name, one overrides the other in an arbitrary order. Therefore, especially after uploading CSV files, review the loaded parameter names in the **Test Data Management** pane, and rename them, if needed. You can edit Data Parameters for a specific test, or edit shared data for everyone who uses it.

### Parameterization Steps

1. **Create Entity**: Create data entity with parameters
2. **Define Values**: Define parameter values (from CSV, synthetic generation, or hard-coded)
3. **Reference Parameters**: Reference parameters in test scripts using `${parameter_name}` syntax
4. **Configure Iterations**: Set up data iteration in tests to run with different values each time

---

## How to Use Parameters in Tests

Use data parameters in test scripts, including parameter references, data iteration, and parameter substitution.

**Use when**: Using data parameters in test scripts or configuring parameter references, data iteration, and parameter substitution.

### Overview

[Data Parameters](skill-blazemeter-test-data://references/core-concepts.md) are variable values in your tests, for example, the *number* of items to put in the shopping cart, which *username* you type, and similar. To learn how to create Data Parameters, see [Parameterize test data](skill-blazemeter-test-data://references/core-concepts.md). After creation, you insert them into tests.

### Steps to Use Parameters in Tests

Follow these steps:

1. Open a test and go to the **Configuration** tab
2. Click **Test Data**. A pane with [data entities](skill-blazemeter-test-data://references/core-concepts.md) opens on the right side
3. Click the **Plus** sign and create a parameter. To initialize the parameter, choose one of the following procedures:
   - [Generate Synthetic Test Data](skill-blazemeter-test-data://references/generation.md)
   - [Load Test Data from Spreadsheets](skill-blazemeter-test-data://references/core-concepts.md)
   You have now defined a parameter value
4. Click **Copy Parameter Name to Clipboard**. The clipboard now contains a string such as `${address}`
5. Return to the test configuration and edit the appropriate test step. For a GUI Functional test, edit a test step in the Scriptless Editor. For a performance test, edit a HTTP Request field in JMeter
6. Replace a hard-coded value with the pasted parameter. Example: In a GUI Functional Test, paste the parameter as a value into a test action
7. Click **Run Test** in the left column to execute the test

BlazeMeter now uses test data that is driven by your loaded Data Entities and replaces Data Parameters in the test with your chosen dynamic values.

### Parameter References

- **Syntax**: Use correct syntax for parameter references (e.g., `${my_variable}`)
- **Scope**: Understand parameter scope (test-only, workspace-loaded, overridden)
- **Substitution**: Parameters are substituted at runtime with values from Data Entities

### Data Iteration

- **Row Iteration**: Iterate through data rows automatically
- **Iteration Settings**: Configure iteration behavior in test settings
- **Data Limits**: Set limits on data usage via Test Data Settings

---

## Load from Spreadsheets

Test steps often rely on parameters, such as menu item names, usernames, or numeric values. You can either hard-code these values -- or use parameters with custom test data. BlazeMeter can load spreadsheet data either from files with comma separated values (CSV), or from [shared folders](skill-blazemeter-test-data://references/core-concepts.md) in your Workspace.

This article covers parameterizing test data using CSV data. Alternatively, you can also [parameterize test data in a Taurus YAML script](skill-blazemeter-test-data://references/core-concepts.md) or [Generate Synthetic Test Data](skill-blazemeter-test-data://references/generation.md).

---

## Using Test Data in Taurus Performance Tests

Use test data in Taurus performance tests, including loading data from CSV files and BlazeMeter Data Entities, configuring data sources, and previewing test data.

**Use when**: Using test data in Taurus performance tests, loading data from CSV files or Data Entities, or configuring data sources for Taurus YAML scripts.

### Overview

Same as other script types, Taurus scripts can load test data from external CSV files and from BlazeMeter Data Entities.

As with all test types, BlazeMeter supports the following data sources to provide test data to a Performance test:
- [Load Test Data from Spreadsheets](skill-blazemeter-test-data://references/core-concepts.md)
- [Generate Synthetic Test Data](skill-blazemeter-test-data://references/generation.md)

You can use one or combine multiple data sources in a Taurus test, as needed. To learn more about BlazeMeter's test data integration in general, see [What are Data Entities and Data Parameters?](skill-blazemeter-test-data://references/core-concepts.md) and [How to Use Test Data](skill-blazemeter-test-data://references/core-concepts.md).

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
3. (Optional) To override the default Data Settings, define your Data Entities in the `data-sources` section of the Taurus file. Use the following options:
   - **path**: Defines the path to an attached CSV file or Data Entity. To identify the implicit file name of the Data Entity, click the **info** button next to its name. Example: Reference the Data Entity `MyDataEntity1` as `MyDataEntity1.csv`
   - **delimiter**: Defines the CSV delimiter. Default: Auto detect. Values: '.' for dot, ',' for comma, 'tab' for a tab symbol
   - **quoted**: Interprets the CSV columns as quoted data. Can be true or false. Default: auto detect
   - **encoding**: Defines the encoding type. Example: "utf-8"
   - **loop**: Defines the behavior when BlazeMeter reaches the end of the test data: If set to true, BlazeMeter loops over and continues again from the beginning of the test data. If set to false, BlazeMeter stops looping
   - **variable-names**: Defines the comma-separated list of Data Parameter names for the CSV columns. If the first row of the CSV file already contains column headings, leave this option empty. If the first row contains data, define column name mappings here; to skip a column in the mapping, add an extra comma with no name. Default: The first line of the CSV file is used as Data Parameter names. Example: `variable-names: id,name`

To learn more about the options, see [Taurus DataSources Documentation](https://gettaurus.org/docs/DataSources/).

**Example Taurus Script with Data Sources:**

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

To override the default Data Settings of other data sources, such as shared files from the BlazeMeter Workspace or synthetic data from a Data Entity, add more `path`s and settings.

### Preview Test Data

Previewing your test data is helpful when you are combining data from multiple files, or generating synthetic test data, so you can review values in context.

1. Open a Performance Test with test data attached
2. Verify that at least one data parameter is defined to be able to generate the data preview
3. Click **Test Data**, **Data Settings**. The Test Data Settings window opens and shows the data preview

### Related Tasks

- [How to Use Test Data](skill-blazemeter-test-data://references/core-concepts.md)
- [What are Data Entities and Data Parameters?](skill-blazemeter-test-data://references/core-concepts.md)
- [How to Share Test Data](skill-blazemeter-test-data://references/core-concepts.md)
- [How to Switch Quickly Between Data Variants](skill-blazemeter-test-data://references/generation.md)
- [How to Control the Number of Rows Used - Test Data Iteration Settings](skill-blazemeter-test-data://references/management.md)

### Documentation References

For detailed information about using test data in Taurus performance tests, use the BlazeMeter MCP help tools:

**Using Test Data in Taurus Performance Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `test-data-with-taurus-scripts`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-with-taurus-scripts"]}`

---

**Use when**: Loading test data from CSV spreadsheets or uploading spreadsheets, attaching to entities, and using spreadsheet data in tests.

**This article covers the following topics:**
1. [How to create or edit test data](skill-blazemeter-test-data://references/core-concepts.md)
2. [How to create and upload test data files](skill-blazemeter-test-data://references/core-concepts.md)
3. [How to use test data parameters](skill-blazemeter-test-data://references/core-concepts.md)
4. [How to manage test data](skill-blazemeter-test-data://references/core-concepts.md)

### How to create or edit test data using the in-tool editor

1. Open a test and go to the **Configuration** tab.
2. Click **Test Data**.
3. Click the **Plus**button, and click **New CSV File (Data Table)**. The CSV Editor opens.

Each column represents a parameter. The first row must contain parameter names. Each row below the first contains parameter values. The CSV editor supports editing, selecting, copying, and pasting text. If you loaded the CSV file from [shared folders](skill-blazemeter-test-data://references/core-concepts.md), you cannot edit the column headers (the parameter names).

The empty last row and last column are shown only so you can more easily add data. Empty last rows and columns are removed automatically when you save the test data.

- To add a column, start typing in the last empty column, or right-click a cell and use the context menu. Press tab to save the cell.
- To add a row, start typing in the last empty row, or right-click a cell and use the context menu. Press tab to save the cell.
- To define a new parameter and its values, enter the name into a column's header (without "${}" characters), and enter the values in the rows below the name.
- To fill neighboring cells with an incremental series of numbers, select consecutive cells that contain numbers, and drag the cell corner down or to the side.
- To delete rows or columns, right-click a cell and use the context menu.

When you're done, click **Save** to save the file in CSV format. Or click **Cancel** to discard your changes.

### How to create and upload test data files

CSV is a human-readable plain-text file format for simple tabular data where fields are separated by commas. You can create CSV files outside BlazeMeter, either in a text editor or in MS Excel.

**To create test data in a text editor:**

Define the test data in a plain-text file:
- For GUI Functional tests, API Monitoring, and Service Virtualization, the first row of CSV data must be the header containing parameter names. For Performance tests, a header row is expected by default, unless specified otherwise in the JMeter CSV Dataset Config.
- In the second row and following, enter the respective parameter values, separated by commas. Each column contains values for one parameter.
- If a field contains a line-break, double-quote, or comma, wrap the field in double-quotes.
- If a quoted field contains a double-quote, replace it by two double-quotes.

Save the plain text file with a .csv suffix.

Return to BlazeMeter to atach it to a test:
1. Open a test and go to the **Configuration** tab.
2. Click **Test Data** and then the **Plus** button.
3. Click **Import CSV File**, and select the CSV file from your local machine to upload it.
4. [Define the number of test data rows (iterations) to use.](skill-blazemeter-test-data://references/management.md)

In the following three-column example, the parameter names are *name*, *city*, *year*:

```
name,city,year
Kim,"Canberra, Australia",2019
Jan,"Paris, France",2020
```

**To create test data in MS Excel:**

You can also use MS Excel to provide the test data in the described format: The column headers must be parameter names (in this example, the parameter names are *name*, *city*, *year*), and the rows below contain the values.

| | A | B | C |
|---|---|---|---|
| 1 | name | city | year |
| 2 | Kim | Canberra, Australia | 2019 |
| 3 | Jan | Paris, France | 2020 |

Export the spreadsheet from Excel as a CSV file. BlazeMeter cannot resolve parameters in other formats than CSV.

### How to use test data parameters

After defining and uploading test data, you can reference the values in parameters of action steps in test scripts. For example, you reference the columns *name*, *city*, and *year* from your test data as *${name}*, *${city}*, and *${year}* in your test.

### How to manage test data

When you upload multiple CSV files, the test definition uses parameter values from all files. Parameter names must be unique, that means, if the same column header is used in multiple files, the last uploaded data definition has priority.

Open the **Test Data** pane to see which data files are active for a specific test. You can also create, edit, preview, download, and delete test data here. To review shared CSV files, click **Test Data** in the top menu bar for your component.

---

## Documentation References

For detailed information about test data core concepts, use the BlazeMeter MCP help tools:

**Test Data Core Concepts**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `test-data-what-are-data-entities-data-parameters` (core concepts)
  - `test-data-how-to-use` (how to use)
  - `test-data-how-to-use-parameters-in-tests` (use parameters in tests)
  - `test-data-load-from-spreadsheets` (load from spreadsheets)
  - `test-data-how-to-parameterize` (how to parameterize)
  - `test-data-share` (share test data)
  - `test-data-with-taurus-scripts` (using test data in Taurus performance tests)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-what-are-data-entities-data-parameters", "test-data-how-to-use", "test-data-how-to-use-parameters-in-tests", "test-data-load-from-spreadsheets", "test-data-how-to-parameterize", "test-data-share", "test-data-with-taurus-scripts"]}`

