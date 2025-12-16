# Test Data Management

## How to Find Usages

Find where test data entities are used across tests and virtual services, including usage tracking, test type identification, and last run information.

**Use when**: Finding where test data entities are used across tests and virtual services or tracking usage, test type identification, and last run information.

### Find Where Test Data is Used

Sometimes you need to identify which shared data is used in which tests or in which virtual services. For example, before you delete or edit test data, it's a best practice to see where it is in use.

1. Click **Test Data** in the top navigation
2. The **Test Data Management** window shows the list of shared Data Entities in this workspace
3. Expand a Data Entity in the list. Three tabs appear, Data Parameters, Usage, and Data Preview
4. Go to the **Usage** tab
5. Select either **Tests** or **Virtual Services**. BlazeMeter lists the Tests or virtual services (respectively) that use this Data Entity. The list includes the following details:
   - The names of the tests or virtual services, respectively
   - Test type (for tests only)
   - Either project name (for tests only) or Service name (for Service Virtualization only)
   - Last Run date and time
6. Click the name of the test or virtual service to open it

---

## How to Back Up

Back up test data entities by exporting to CSV files, exporting to files, importing from files, and managing data entity backups for disaster recovery.

**Use when**: Backing up test data entities or exporting to CSV files, importing from files, and managing data entity backups for disaster recovery.

### Back Up Test Data

Your test data is stored in Data Entities. For each Data Entity in the Test Data pane, use the **Ellipsis** menu next to its name to manage it:

- To export any Data Entity as a spreadsheet so you could import it, for example, into MS Excel, use the Ellipsis menu and select **... > Download Data As CSV**
- To share a Data Entity with your team, use the Ellipsis menu and select **... > Save to Workspace**. To use a shared Data Entity in your test, select **... > Load From Workspace**
- To make local backups, use the Ellipsis menu and select **... > Export to File**. To restore a Data Entity from such an exported file, select **... > Import From File**
- Use the Ellipsis menu to **Rename** or **Remove** Data Entities from the test. If you don't save them, removed Data Entities are also deleted from the Workspace

To learn more, see [How to Share Test Data](https://help.blazemeter.com/docs/guide/test-data-share.html)

---

## How to Manage Spreadsheets

Manage CSV test data files, including downloading, editing, and deleting spreadsheet files attached to data entities. BlazeMeter can load test data from CSV files. To learn more about their creation, see [How to Load Test Data from Spreadsheets](skill-blazemeter-test-data://references/core-concepts.md).

**Use when**: Managing CSV test data files or downloading, editing, and deleting spreadsheet files attached to data entities.

After creation, you can download, edit, or delete CSV files.

**Steps:**

1. Click **Test Data** in the top navigation, or open the **Test Data** pane in your test
2. Expand the Data Entity and hover the mouse over a CSV file entity in the data entity to access the following action buttons:
   - **Download CSV**: Download the CSV file for editing
   - **Edit CSV**: Edit the CSV file externally
   - **Delete CSV**: Remove the CSV file from the entity

---

## How to Manage Data Parameters

Manage test data parameters, including editing, previewing, copying, bulk operations, and parameter definition modifications. [Data Parameters](skill-blazemeter-test-data://references/core-concepts.md) are variable values in your tests, for example, the *number* of items to put in the shopping cart, which *username* you type, and similar. To learn how to create Data Parameters, see [Parameterize test data](skill-blazemeter-test-data://references/core-concepts.md). After creation, you can preview, copy, edit, or delete them.

**Use when**: Managing test data parameters or editing, previewing, copying, performing bulk operations, and modifying parameter definitions.

### Edit Data Parameters in the Current Test

Open the **Test Data** pane, hover the mouse over a parameter definition to show the editor buttons.

The four buttons have the following functionalities, from left to right:

- **Copy Parameter Name to Clipboard**: So you can paste it easily into the test definition
- **Preview**: One instance of generated data. Click again to switch back to the function view
- **Edit**: This parameter definition to change the parameter name, the function, or its arguments
- **Delete**: This parameter. If the deleted parameter is in use in a scenario step, the step breaks

### Bulk Operations on Data Parameters

To copy or delete Data Parameters in bulk within the same Data Entity, use the checkboxes:

1. Select individual Data Parameters that you want to bulk-copy, or click **Select All**. Additional bulk action buttons appear
2. Perform one of the following bulk actions on the selected parameters:
   - To copy, click **Clone Parameters**
   - To delete, click **Delete Parameters**

### Edit Data Parameters of All Data Entities

1. Click **Test Data** in the top navigation. The **Test Data Management** window shows the list of shared Data Entities in this workspace
2. You can sort shared Data Entities by name, by who last edited the entity, and by last updated date
3. Expand a Data Entity in the list. Three tabs appear: **Data Parameters**, **Usage**, and **Data Preview**
4. Go to the **Data Parameters** tab and select a Data Parameter from the list
5. Details appear in the right pane
6. You can edit the following properties

BlazeMeter auto-saves your changes when you leave a field.

---

## How to Manage Entities

Manage data entities at workspace level, including cloning, renaming, deleting, copying entity IDs, and viewing usage information. Data Entities are containers to store test data in BlazeMeter. You can clone, rename, or delete them, and copy their ID for API calls.

**Use when**: Managing data entities at workspace level or cloning, renaming, deleting, copying entity IDs, and viewing usage information.

### View All Data Entities

To view all Data Entities:

- Either click **Test Data** in the top navigation
- Or alternatively in the **Test Data** pane, click **TEST DATA... > Manage Data Entities**

If no team members have saved any shared data entities to the Workspace, the **Test Data Management** window can be empty.

### Entity Operations

Hover the mouse over a Data Entity to access editor buttons:

- **Clone Data Entity**: Click to make a copy that you can edit without interfering with tests that are using the original shared Data Entity
- **Rename Data Entity**: Click to enter a new name for this shared Data Entity
- **Delete Data Entity**: Click to remove a shared Data Entity from all tests. Verify whether the data is unused before deleting the Entity
- **Copy Entity ID to Clipboard**: Click to be able to refer to the Entity in an API call

### Data Entity Tabs

Each Data Entity has three tabs that let you drill deeper:

- The **Data Parameters** tab lets you [edit data parameters](skill-blazemeter-test-data://references/management.md)
- The **Usage** tab lets you see [which tests and which virtual services are using this shared Data Entity](skill-blazemeter-test-data://references/management.md)
- The **Data Preview** tab lets you [preview test data](skill-blazemeter-test-data://references/management.md) values

---

## How to Configure CSV

Configure CSV file handling settings, including delimiter configuration, header row handling, and quoted data support. When you [Load Test Data from Spreadsheets](skill-blazemeter-test-data://references/core-concepts.md), you can configure the column delimiter character, the header line, and whether quoted cells exist in the CSV file.

**Use when**: Configuring CSV file handling settings or setting up delimiter configuration, header row handling, and quoted data support.

**Steps:**

1. Open a test with CSV files attached
2. Click **Test Data**, then click **Iterations** (for GUI Functional Tests) or **Data Settings** (for Performance Tests), respectively
3. In the **Test Data Settings** window, choose one of these **Target Options**:
   - **Delimiter**: Indicates the column delimiter that your configuration files use for CSV data, for example `"\t"` for the tab character. The default delimiter is a comma
   - **Ignore First Line**: If set to true, BlazeMeter treats the first row of data as column headers. Headers become Data Parameter names. Set it to false if the first row contains data
   - **Allow Quoted Data**: If your column values can contain commas, and you also use commas as delimiters, then set this to true. **Example**: If a cell value can be `"123 Main street, Springfield"`, then allow the integration to surround the data with double quotes, otherwise the column is missegmented into two columns
4. Click **Save**

---

## How to Troubleshoot

Troubleshoot test data definition errors, including validation messages, type errors, function argument issues, and inline error resolution.

**Use when**: Troubleshooting test data definition errors or resolving validation messages, type errors, function argument issues, and inline errors.

### Common Issues

- **Validation Messages**: Understand validation errors
- **Type Errors**: Fix data type mismatches
- **Function Arguments**: Resolve function argument issues
- **Inline Errors**: Fix inline definition errors

---

## How to Preview

Preview test data before and after test runs, including data entity previews, shared data previews, and CSV download options. You can view test data before and after test runs.

**Use when**: Previewing test data before and after test runs or viewing data entity previews, shared data previews, and CSV download options.

### View Before a Test Run

Before a test run, you can preview your test data in the **Test Data** pane by clicking **Iterations** (for GUI Functional Tests) or **Data Settings** (for Performance Tests and virtual services), respectively.

### View After a Test Run

After a test run, go to the **History** tab, open the test **Report**, and go to the Summary tab. Under **Test Data**, click **Show Test Data** to review which data was used. Here you can also click the **Rerun** button to run this test again with the same test data, which can be useful for debugging.

### View Shared Data

You can also preview the data in all shared data Entities.

**Steps:**

1. Click **Test Data** in the top navigation. The **Test Data Management** window shows the list of shared Data Entities in this workspace
2. Expand a Data Entity in the list. Three tabs appear, Data Parameters, Usage, and Data Preview
3. Go to the **Data Preview** tab
4. Preview the data
5. (Optionally) Define the data size
6. (Optionally) Download the data as CSV file

---

## Settings

Control the number of test data rows used in tests, including single and multiple data source configurations, row limits, and iteration settings.

**Use when**: Controlling the number of test data rows used in tests or configuring single and multiple data source configurations, row limits, and iteration settings.

### Control the Number of Test Data Rows Used

When test data is generated by functions and not hard-coded, it is available at any quantity. When you load test data from CSV files, you choose whether you want to use all rows or a subset. The data size determines the number of test runs. To save time, or while debugging, you maybe prefer to run fewer row of test data (fewer iteration).

### Single Data Source

1. Open a GUI Functional or Performance Test with CSV files attached
2. Click **Test Data**, then click **Iterations** (for GUI Functional Tests) or **Data Settings** (for Performance Tests), respectively
3. Under **Test Data Settings > Run Options > Defined Number of Rows**, enter how many rows, for example, 1

### Multiple Data Sources

A test can have multiple CSV files attached that contain different numbers of rows of test data. In this case, you determine the number of rows from all applicable files that are used, skipped, or looped, respectively.

To control how many rows of test data are used:

1. Open a GUI Functional or Performance Test with CSV files attached
2. Click **Test Data**, then click **Iterations** (for GUI Functional Tests) or **Data Settings** (for Performance Tests) respectively
3. In the **Test Data Settings** window, choose one of these **Run Options**:
   - **Defined Number of Rows** Specify a number between 1 and 1000000. The test runs with test data from this number of rows, from all files. Extra rows from longer files are skipped, rows from shorter files are used repeatedly
   - **All Rows From This CSV** Select an attached CSV file or Find&Reserve model. The test runs with test data from all rows of this file or model. Extra rows from other files or models are skipped, rows from shorter files or models are used repeatedly
   - **All Rows From Longest CSV, Loop Others** The test runs with test data from all rows of the longest attached file or model. Rows from shorter files or models are used repeatedly
   - **All Rows From Shortest CSV, Do Not Loop** The test runs with test data from all rows of the shortest file or model. Additional rows from longer files or models are skipped
4. Click **Save**

### Examples for Iterations with Two Data Sources

| File A | File B | Option selected | Outcome | Iterations |
|--------|--------|-----------------|---------|------------|
| 5 rows | 100 rows | Run 1 row (default) | Use the first row from file A. Use the first row from file B. | 1 |
| 10 rows | 100 rows | Run 5 rows | Use the first 5 rows from file A. Use the first 5 rows from file B. | 5 |
| 5 rows | 100 rows | Run 10 rows | Loop twice over the 5 rows from file A. Use the first 10 rows from file B. | 10 |
| 5 rows | 100 rows | Run all rows from file B | Loop 20 times over the 5 rows from file A. Use all 100 rows from file B. | 100 |
| 20 rows | 100 rows | Run all rows from longest file, loop others | Loop 5 times over the 20 rows from file A. Use all 100 rows from file B. | 100 |
| 20 rows | 100 rows | Run all rows from shortest file, don't loop | Use 20 rows from file A. Use the first 20 rows from file B. | 20 |

---

## Share Entities Within Workspace

Share data entities within a workspace, including saving to workspace, loading from workspace, and team collaboration on test data. In addition to [sharing spreadsheets](skill-blazemeter-test-data://references/management.md), you can also share data entities with team members in the same Workspace.

**Use when**: Sharing data entities within a workspace or saving to workspace, loading from workspace, and collaborating on test data with team members.

To share a test's local data entity, save it to the workspace first. The saved data entity contains copies of all test parameters. Attached CSV files and spreadsheets from Shared Folders are *not* included in data entities saved to the workspace. To share and load these files as well, see [Export and import test data files](skill-blazemeter-test-data://references/management.md).

**Steps:**

1. Open a test and go to the **Configuration** tab
2. Click the **Test Data** button
3. Click the ellipsis menu and select **Save to Workspace**. The **Save Test Data Entity** window opens
4. Define a **Test Data Entity Name** that helps your team members to identify what to use this test data for, and click **Save**. After saving a data entity, the shared copy is no longer linked to the original local test. If you regenerate the local test's synthetic data, the shared data entity remains unaffected
5. Open a test into which you want to load the shared data entity, and go to the **Configuration** tab
6. Click the **Test Data** button
7. Click the ellipsis menu and select **Load From Workspace**
8. Select a shared test data entity and click **Open**. Opening a data entity overwrites *all* current test parameters and settings in the test

---

## Share Spreadsheets Within Workspace

Share CSV spreadsheets within a workspace using shared folders, including folder creation, file upload, and attachment to tests. In addition to [sharing data entities](skill-blazemeter-test-data://references/management.md), you can also share test data from spreadsheets in CSV format with your workspace.

**Use when**: Sharing CSV spreadsheets within a workspace or creating shared folders, uploading files, and attaching spreadsheets to tests.

### Create Shared Folders for CSVs

To share a spreadsheet within a Workspace, ask a Workspace administrator to create a shared folder and to upload the CSV files there.

**Steps:**

1. Prepare spreadsheets with test data as usual. **Example**: The column name becomes the test parameter `${name}`, the column age becomes the test parameter `${age}`, and the rows contain the test data values. Example:
   ```
   name,age
   Jack,76
   Joe,29
   Jill,50
   ```
2. Save the spreadsheets in CSV format
3. Log on as a Workspace Administrator
4. Click **Settings > Workspace > Shared Folders**
5. To create a shared folder, click **Plus**, type the new folder a name (without spaces), and press Enter
6. Click a shared folder to open it
7. Drag and drop the CSV files from your local machine onto the drop area, or click to upload files from the file browser

The uploaded files become available to workspace members.

### Attach CSVs from Shared Folders to a Test

After the Shared Folder and its contents are ready, team members can attach shared test data to their tests.

**Steps:**

1. Open a test and go to the **Configuration** tab
2. Click the **Test Data** button
3. Click **Plus**, and then select **Attach... CSV File from Shared Folders**. The **Shared Folders** window opens
4. Select the desired folders so that a checkmark appears, then click **Accept** to use the selected test parameters in your test definition

### Remove Shared CSVs from a Test

To stop using shared test data in a test, return to the **Shared Folders** window, and deselect the shared folder. The test data remains available for other users of this workspace. To learn more, see [Unshare test data](skill-blazemeter-test-data://references/management.md)

---

## Unshare

Unshare test data (spreadsheets and data entities) from workspace, including removal from shared folders and deletion of shared entities. To prevent everyone from using a shared data set, for example, because it is outdated, you want to stop sharing it with the team. You can unshare spreadsheets or data entities.

**Use when**: Unsharing test data from workspace or removing spreadsheets and data entities from shared folders and deleting shared entities.

### Unshare a Spreadsheet

**Steps:**

1. Click **Settings > Workspace > Shared Folders**
2. In the **Shared Folders** window, deselect the shared folder
3. Click the delete button to remove the spreadsheet for everyone in the Workspace

### Unshare a Data Entity

**Steps:**

1. Click **Test Data** in the top navigation. The **Test Data Management** window shows the list of shared Data Entities in this workspace
2. Hover the mouse over the **Actions** column of a shared data entity. Inline action buttons appear
3. Click the **Delete** action to remove the data entity from all tests

---

## Import Export

Export and import test data files between workspaces, including ZIP file creation, data entity export, and cross-workspace data migration. You can export a data entity as a zip file to your local computer, and import it into any test with test data support in another workspace. The zip file contains all test parameters, attached CSV files, and CSV files from shared folders.

**Use when**: Exporting and importing test data files between workspaces or creating ZIP files, exporting data entities, and migrating data across workspaces.

### Export Data Entities to Other Workspaces

**Steps:**

1. Open the source test and go to the **Configuration** tab
2. Click the **Test Data** button
3. Click the ellipsis menu and select **Export to File**
4. Define the Test Data Entity Name and click **Export**. You download the data entity as a ZIP file
5. Open the target test and go to the **Configuration** tab
6. Click the **Test Data** button
7. Click the ellipsis menu and select **Import**
8. Select the exported ZIP file and click **Open**

**Important**: Importing a data entity overwrites *all* current test parameters and settings in the test.

After the import, you can remove test parameters that you don't need, and add new test parameters to the test.

### Import Shared Folders

**Steps:**

1. Export the data entity from the source Workspace
2. Work with the workspace administrators of the target workspace to recreate the Shared Folder structure with the same names and have them upload the CSV files from the source Workspace
3. Go to the target workspace and open a test
4. Click the **Test Data** button and click the **Plus** button
5. Select **Import Data Entity From Exported File**
6. Select the exported ZIP file and Click Open

**Important**: Importing a data entity overwrites *all* current local test parameters and settings in the test.

---

## How to Add Entity

Add new data entities to workspace, including entity creation, parameter definition, and initial configuration. In BlazeMeter, a Data Entity is a container for Test Data Parameters. You can add test data from various sources, such as CSV files or synthetic test data.

**Important**: GUI Functional tests support one single [Data Entity](skill-blazemeter-test-data://references/core-concepts.md) only. Performance tests support multiple Data Entities.

**Use when**: Adding new data entities to workspace or creating entities, defining parameters, and configuring initial settings.

### Add a Data Entity to a Performance Test

Follow these steps:

1. Open a Performance test and click **Test Data** to open the Test Data pane
2. Click either the big blue **Plus** button or click **TEST DATA... > Add Data Entity**. Choose one of the following options:
   - **Create New Data Entity**: Use this option to manually add Data Parameters. Give the Data Entity a descriptive, unique name
   - **Create New Data Entity From CSV File**: Select a CSV file with test data from your file system
   - **Attach CSV Files From Test Configuration**: Use this option to create a new Data Entity from an already present CSV file in the test configuration
   - **Load Data Entity From Workspace**: Select a shared Data Entity that is stored in your workspace
   - **Import Data Entity From Exported File**: Use this option to create a new data entity from a previously exported file
3. Click **Add**. The test data parameters in the entity are now available to the test

---

## Resolve Test Data Definition Errors

No data can be generated as long as there are errors in the data definition. To troubleshoot test data definitions, check the following:

**Use when**: Resolving test data definition errors, troubleshooting data generation issues, or fixing validation errors in test data parameters.

### Overview

Errors can be caused by misspelled functions, missing arguments of functions, missing mandatory values, inappropriate data types (such as entering text where a number is expected), unpaired quotation marks or parentheses, missing files, and so on.

Errors are clearly indicated by the inline validation in the **Test Data** pane, so you can address each warning immediately. If you have loaded a Data Model that contains multiple errors, an error bar indicates the number of issues to address before data can be generated. Click the number in the error bar to review a detailed list of detected issues and a description of the error. Then click each listed data parameter or data entity to quickly navigate to the item to fix it.

### Troubleshooting Example

**Symptom:**

I see the validation message "*Type string is not assignable to type number*" for `randInt( 1 + ${x} , ${y} + 1000 )`. I've defined two numeric data parameters `x` and `y` and used them in an addition inside function arguments. How do I make the `+` operator interpret the parameters as numbers?

**Solution:**

The overloaded `+` operator accepts either two strings (concatenation) or two numbers (addition). Inside a function argument, the `+` operator resolves the unknown types as string. The function expects a number and throws a type validation error. Use the `ToNumber()` function on the number to make the `+` operator act as numeric addition and not as string concatenation. 

**Correct syntax:**
```
randInt(1+ToNumber(${x}), ToNumber(${y})+100)
```

### Common Error Types

- **Misspelled functions**: Check function names against the [Test Data Generator Functions](skill-blazemeter-test-data://references/generation.md) documentation
- **Missing arguments**: Ensure all required function arguments are provided
- **Missing mandatory values**: Fill in all required fields
- **Inappropriate data types**: Verify that text is not entered where numbers are expected, and vice versa
- **Unpaired quotation marks or parentheses**: Check for matching quotes and parentheses
- **Missing files**: Verify that referenced CSV files or other data sources are available

### Documentation References

For detailed information about resolving test data definition errors, use the BlazeMeter MCP help tools:

**Resolve Test Data Definition Errors**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `test-data-how-to-troubleshoot`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-how-to-troubleshoot"]}`

---

## Documentation References

For detailed information about test data management, use the BlazeMeter MCP help tools:

**Test Data Management**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `test-data-how-to-find-usages`, `test-data-how-to-back-up`, `test-data-how-to-manage-spreadsheets`, `test-data-how-to-manage-data-parameters`, `test-data-how-to-manage-entities`, `test-data-how-to-configure-csv`, `test-data-how-to-troubleshoot`, `test-data-how-to-preview`, `test-data-settings`, `test-data-share-entities-within-workspace`, `test-data-share-spreadsheets-within-workspace`, `test-data-unshare`, `test-data-import-export`, `test-data-how-to-add-entity`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-how-to-find-usages", "test-data-how-to-back-up", "test-data-how-to-manage-spreadsheets", "test-data-how-to-manage-data-parameters", "test-data-how-to-manage-entities", "test-data-how-to-configure-csv", "test-data-how-to-troubleshoot", "test-data-how-to-preview", "test-data-settings", "test-data-share-entities-within-workspace", "test-data-share-spreadsheets-within-workspace", "test-data-unshare", "test-data-import-export", "test-data-how-to-add-entity"]}`

