# API Monitoring Test Data

## Using Test Data CSV

You can use CSV files to drive API Monitoring tests by data stored in the CSV file.

**Use when**: Implementing data-driven testing in API Monitoring tests or using CSV files to parameterize test requests.

### Prepare Your CSV Data File

BlazeMeter supports data files with the extensions .csv, .txt, or .dat, with a file size of no more than 5 MB.

#### Set your variables

Use the header row to define your variable names in a list of comma-separated strings. No other separator is supported.

Example: `id,name,country` - This example has 3 data columns.

#### Data file example

The following is an example of a header row containing variable names and corresponding data values in the rows below. Each column corresponds to one variable and its values.

```
id,name,country
1,John,US
2,Jack,GB
3,Mike,IN
```

### Use CSV Data Files in API Monitoring Tests

To upload and use your CSV data file:

1. Go to the BlazeMeter API Monitoring tab
2. Open or create an API Monitoring Test
3. Go to **Editor > Environment > Test Settings** and select **Test Data**
4. Under *Test Data Source*, select **Add CSV File**
5. Select **Choose File**, add your data file, then click **Upload CSV File**
6. Define your **Run Options**. You can choose to use all the data rows in the file, or set a defined number of data rows from your file. Depending on your subscription plan, you may be subject to a limited number of data rows. If your specified Number of Rows exceeds the data row limit, the Test Data size will be automatically reduced to match your subscription
7. *(Optional)* Choose whether to **Run Data Iterations Sequentially**. By default, data-driven API tests are running data iterations in parallel, which is faster
8. Verify that the expected Test Data variables are now visible in the **Editor** under **Steps**
9. You can now add data parameters using the test data variables in your *Request* and *Assertions* sections, much like regular variables. For more information, see [Dynamic Data and Request Chaining](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html)

### Run Your Data-driven Test

After uploading and configuring your CSV data file or Data Entities, and adding parameters to your step Request or Assertions, click **Run Now**.

### View Test Iterations and Individual Data Line Results

For data-driven tests, test results will be grouped in Iterations. Each iteration represents a test execution using a single data line entry from the CSV file or Data Entity.

Each set of Iterations will show a failed count (if any). This represents the number of individual iterations that failed within that group.

#### Access individual data line result

To view an individual iteration/data line result:

1. Go into a test and select **Results**
2. Click on **View Iterations** to show the individual iterations
3. Identify the specific iteration by clicking **View Test Data**. This will bring up the data line from that particular iteration. Clicking View Test Data next to the test name in the Iterations view will show all the data lines used in all the iterations
4. Once you've identified the iteration, click **View result**. The individual data line result is shown

### Best Practices

- Use descriptive column names in CSV header row
- Ensure CSV data is valid and properly formatted (comma-separated)
- Test CSV data before production use
- Document CSV structure and usage
- Consider file size limits (5 MB maximum)
- Use sequential iteration if order matters, parallel for faster execution

---

## Using Test Data Entities

You can use Test Data from shared Data Entities to drive API Monitoring tests.

**Use when**: Using shared Data Entities to drive API Monitoring tests or implementing data-driven testing with shared test data.

### Prepare Your Data Entities

To add a Data Entity:

1. Go to the BlazeMeter Performance or Functional tab
2. Navigate to **Test Data**
3. Select **Add Data Entity**
4. Choose from **Create New Data Entity**, **Import Data Entity from exported file**, or **Create New Data Entity from exported file**. For more information on creating and modifying Data Entities, see How to Generate Synthetic Test Data
5. *(Optional)* Enable sharing of your Data Entities. See How to Share Test Data to learn more

### Add Data Entities to API Monitoring Test

To use your Test Data from shared Data Entities:

1. Go to the BlazeMeter API Monitoring tab
2. Open or create an API Monitoring Test
3. Go to **Editor > Environment > Test Settings** and select **Test Data**
4. Under *Test Data Source*, select **Add Test Data**
5. In the *Workspace* input drop-down, select the **Workspace** from which to draw your Test Data
6. Under *Test Data Entities*:
   - Select **Add Test Data Entity** and choose from the available list of entities. A preview of your entity will be available under *Test Data Preview*, and the variables will be listed under *Test Steps > Parameterisation*
   - *(Optional)* Add additional entities to use in the test
   - *(Optional)* Configure the Number of Rows and Data variant for each entity. If you are using multiple Data Entities, the test will draw the maximum number of data rows that have been specified among the entities. For instance, if you have three Data Entities with 1, 2, and 10 Number Of Rows specified, the test will draw 10 data rows. Depending on your subscription plan, you may be subject to a limited number of data rows. If your specified Number of Rows exceeds the data row limit, the Test Data size will be automatically reduced to match your subscription
   - *(Optional)* To execute data iterations in sequence instead of in a parallel run, check the **Run data iterations sequentially** box

### Add Your Parameters

You can now add data parameters using the test data variables in your *Request* and *Assertions* sections, much like regular variables. For more information, see [Dynamic Data and Request Chaining](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html).

Go to **Editor > Steps > Parameterisation** to view the available variables from your Data Entities, and add them to *Request* or *Assertions*.

**Note**: When using multiple Data Entities, the test will draw the maximum number of data rows that have been specified among the entities. For instance, if you have three Data Entities with 1, 2, and 10 Number Of Rows specified, the test will draw 10 data rows.

### Run Your Data-driven Test

After uploading and configuring your CSV data file or Data Entities, and adding parameters to your step Request or Assertions, click **Run Now**.

### View Test Iterations and Individual Data Line Results

For data-driven tests, test results will be grouped in Iterations. Each iteration represents a test execution using a single data line entry from the CSV file or Data Entity.

Each set of Iterations will show a failed count (if any). This represents the number of individual iterations that failed within that group.

#### Access individual data line result

To view an individual iteration/data line result:

1. Go into a test and select **Results**
2. Click on **View Iterations** to show the individual iterations
3. Identify the specific iteration by clicking **View Test Data**. This will bring up the data line from that particular iteration. Clicking View Test Data next to the test name in the Iterations view will show all the data lines used in all the iterations
4. Once you've identified the iteration, click **View result**. The individual data line result is shown

### Best Practices

- Use Data Entities for shared test data across multiple tests
- Organize entities by test domain or purpose
- Document entity structure and usage
- Keep entities updated and maintained
- Enable sharing when data needs to be used across multiple tests
- Consider data row limits based on subscription plan
- Use sequential iteration if order matters, parallel for faster execution

---

## Using Test Data in API Monitoring

You can use [CSV files](skill-blazemeter-api-monitoring://references/test-data.md) or Test Data from [Data Entities](skill-blazemeter-api-monitoring://references/test-data.md) to drive API Monitoring tests. This is useful for testing various input combinations using a single test to increase the test coverage of your API.

**Use when**: Using CSV files or Data Entities to drive API Monitoring tests, implementing data-driven testing, or testing various input combinations using a single test.

---

## Documentation References

For detailed information about API Monitoring test data, use the BlazeMeter MCP help tools:

**Using Test Data in API Monitoring**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-using-test-data-in-api-monitoring`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-using-test-data-in-api-monitoring"]}`

**Using Test Data CSV**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-using-test-data-csv`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-using-test-data-csv"]}`

**Using Test Data Entities**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-using-test-data-entities`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-using-test-data-entities"]}`

