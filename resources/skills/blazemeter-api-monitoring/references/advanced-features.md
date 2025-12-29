# API Monitoring Advanced Features

## AI Script Assistant

The API Monitoring AI Script Assistant introduces a streamlined method for generating and refining scripts across various sections of test settings and steps. This tool leverages natural language input to automate script creation.

**Use when**: Using the AI Script Assistant to generate and refine scripts or creating Initial Script, Pre-request Scripts, and Post-response Scripts using natural language input.

### About the AI Script Assistant

- The AI Script Assistant is accessible within the Initial Script, Pre-request Scripts, and Post-response Scripts sections
- The functionality is supported for both Test Settings (environment-level configuration) and individual Test Steps
- Input Interface: A UI-based form enables you to define script logic using descriptive instructions
- Only user-provided query input is sent to the AI model. No additional user or system data is transmitted
- If needed, AI features can be disabled by the team owner in the team settings

### Generate Scripts using the AI Script Assistant

1. Navigate to **Test Settings** or **Test Steps** where scripting is required. The AI Script Assistant is available in the *Initial Script*, *Pre-request Scripts*, and *Post-response Scripts* sections
2. Click the **AI Script Assistant** button located in the script editor
3. A pop-up input form will appear. Enter a description of the script logic you want to generate, such as: "Get the last Sunday date." Click **Ask AI**
4. The AI model will generate a script and insert it directly into the editor textbox. Review the output to ensure it aligns with your requirements
5. (Optional) If you would like to adjust the script, you can insert a new query and include the existing script in the prompt by selecting the **Add Existing Script to Prompt** box. Click **Ask AI**. See the Tips section to learn best practices about using JavaScript variables versus BlazeMeter (Runscope) variables with the AI Assistant
6. Validate the script, make any necessary adjustments, and save your configuration

### Convert Postman Scripts

You can also convert Postman test scripts into scripts compatible with API Monitoring. While some highly specific Postman logic may still fall outside current support, most common patterns can be converted by invoking a prompt such as: "Convert this Postman script into a BlazeMeter compatible script."

### Tips for writing good queries

- Your query should be related to the JavaScript code or script generation in the context of API Monitoring tool only. For unrelated queries, the AI model may reject the query with this error message: "Unable to generate a valid response for the given input. Please ensure the input is related to generation of scripts."
- If you wish to store or retrieve data in or from an API Monitoring variable, explicitly mention "blazemeter" in the query. For example: "Assert the response status code is 200 and assign it to a blazemeter variable." If BlazeMeter is not mentioned, the AI model will assign the value to a JavaScript variable. As a reminder, JavaScript variables and API Monitoring variables have different syntax:
  - JavaScript variables: `var x = value`
  - API Monitoring (Runscope) variables: `variables.set('x', value)`

### Example Queries

Want to start right away? Here are some example queries that you can try immediately with the AI Script Assistant:

- **Get a BlazeMeter variable**: "Get blazemeter variable \"status\" and print its value"
- **Set a BlazeMeter variable**: "Set blazemeter variable \"status\" and print its value"
- **Clear a global variable**: "Delete blazemeter variable \"status\" from initial variables"
- **Check status code**: "Validate that status code is 200"
- **Check response body**: "Check response body contains string \"string_you_want_to_search\""
- **Check JSON attribute**: "Check response body \"attribute_to_search\" is \"value_to_search\""
- **Validate POST success**: "Validate that the response status code is either 201 or 202"
- **Convert XML to JSON**: "Convert xml response into json"
- **Validate JSON schema**: "Validate for json schema"

### Example AI responses

The following examples show unedited responses from the AI Script Assistant model based on natural language queries:

**User query: Validate if POST request is successful**
```javascript
if (request.method === 'POST' && response.status >= 200 && response.status < 300) {
  log('POST request successful');
} else if (request.method === 'POST') {
  log('POST request failed with status: ' + response.status);
}
```

**User query: Convert XML response body to JSON**
```javascript
var xmlString = response.body;
var jsonData = runscope_xml2json(xmlString);
log(jsonData);
```

**User query: Get the last Sunday date**
```javascript
function getLastSunday() {
  const today = new Date();
  const day = today.getDay();
  const diff = today.getDate() - day + (day === 0 ? -7 : 0);
  return new Date(today.setDate(diff));
}

const lastSunday = getLastSunday();
log(lastSunday);
```

**User query: Extract a key 'timestamp' from the API response and add 1 day to it**
```javascript
function addDayToTimestamp(timestamp) {
  const date = new Date(timestamp);
  date.setDate(date.getDate() + 1);
  return date.toISOString();
}

const timestamp = response.body.timestamp;

if (timestamp) {
  const newTimestamp = addDayToTimestamp(timestamp);
  log(newTimestamp);
} else {
  log('Timestamp not found in the response body.');
}
```

**User query: Extract a key 'hex' from the API response and calculate its MD5 value**
```javascript
function calculateMD5(key) {
  // Check if CryptoJS is available
  if (typeof CryptoJS === 'undefined') {
    throw new Error('CryptoJS library is not available.');
  }
  return CryptoJS.MD5(key).toString();
}

const hexKey = response.body.hex;

if (hexKey) {
  const md5Hash = calculateMD5(hexKey);
  log("MD5 Hash: " + md5Hash);
} else {
  log("Key 'hex' not found in the response body.");
}
```

### Best Practices

- Provide clear and specific descriptions
- Review generated code before using
- Refine scripts based on your specific needs
- Test generated scripts thoroughly
- Mention "blazemeter" when working with API Monitoring variables
- Use "Add Existing Script to Prompt" to refine existing scripts

---

## GraphQL Testing

You can integrate GraphQL queries into your tests, expanding your ability to handle modern API architecture.

**Use when**: Integrating GraphQL queries into API Monitoring tests or importing from Postman, using variables, and testing GraphQL APIs.

### Getting Started with GraphQL Testing

To create and run tests using GraphQL, follow these steps:

1. Create or edit an API Monitoring test
2. In *Steps*, add an API request. Set Request Type to **POST** and provide the Endpoint URL
3. In *Parameters*, select **Add GraphQL Body**
4. Input Your GraphQL body in the **Query** box. Click the **Auto Fetch** button to retrieve the latest API schema. The rich text editor enhances readability with syntax highlighting, real-time auto-complete, and error validation
5. Once the query is in place, click **Run Now** or **Save & Run** to validate the response

### Importing GraphQL Queries from Postman

API Monitoring supports migration of GraphQL queries from Postman. You can import individual GraphQL queries from a Postman collection file, or do a bulk import of multiple collection files using a ZIP file.

To import GraphQL queries:

1. In API Monitoring, select **Create Test > Import Test**
2. In *Import Tests*, select **Postman Collection v2 / v1 / Data Dump** and choose a file to upload. Supported format: JSON (for individual collection) or ZIP (for multiple JSON files)
3. Click **Import Requests** and review the imported queries in the test editor

### Using Variables in GraphQL Tests

You can combine GraphQL with variables to make dynamic queries. Here's an example of how to incorporate variables into your tests:

1. Go back to the test you created earlier and click **Edit Test**
2. In the POST request, define your variables and values in the **GraphQL Variables** box. For example: `{ "limit": 5 }`

You can also use API Monitoring Initial Variables as follows:

- Navigate to **Environment > Test Settings > Initial Variables**
- Define the **Name** and **Value** for each initial variable. For example, the variable name is `launches` and the value is `2`
- Return to your POST request. You'll find available variables listed in the right-hand frame under **Parameterisation > Available Variables**
- In the **GraphQL Variables** box, replace a value with an initial variable either by hardcoding it directly, or by clicking on the variable name from the available variables list. For example: `{ "limit": {{launches}} }`

3. Click **Save & Run** to validate the dynamic behavior of your query

### Best Practices

- Use GraphQL variables for dynamic queries
- Use Initial Variables for reusable values
- Validate GraphQL response structure
- Test different query types (queries, mutations, subscriptions)
- Document GraphQL schema and queries
- Use Auto Fetch to retrieve latest API schema
- Leverage syntax highlighting and auto-complete in the editor

---

## SOAP/WSDL Testing

API Monitoring tests support any HTTP request, including making SOAP requests. SOAP responses can be evaluated using the built-in XML assertions, or the Marknote XML parser library in scripts.

**Use when**: Testing SOAP APIs in API Monitoring or validating responses with XML assertions and using Marknote XML parser in scripts.

### Testing a SOAP API Endpoint

Here's what a request to a SOAP API looks like:

```
POST /ip2geo/ip2geo.asmx HTTP/1.1
Host: ws.cdyne.com
Content-Type: text/xml; charset=utf-8
Content-Length: length
SOAPAction: "http://ws.cdyne.com/ResolveIP"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
               xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ResolveIP xmlns="http://ws.cdyne.com/">
      <ipAddress>string</ipAddress>
      <licenseKey>string</licenseKey>
    </ResolveIP>
  </soap:Body>
</soap:Envelope>
```

**Notes:**
- This example uses SOAP 1.1, but the API also supports SOAP 1.2, and you can test both versions using API Monitoring
- For this example, we're going to be using an IP address which will return an address from Chicago, US. You can use your own public IP address, and you can find it by searching for "what's my IP" on Google, or by typing the command in your terminal: `curl httpbin.org/ip`

To test the SOAP API endpoint:

1. Create a new test in the API Monitoring interface, and set the following parameters:
   - Method: POST
   - URL: https://ws.cdyne.com/ip2geo/ip2geo.asmx
   - Headers:
     - SOAPAction: "http://ws.cdyne.com/ResolveIP"
     - Content-Length: length
     - Content-Type: text/xml; charset=utf-8

2. Add the request's envelope body by clicking **+ Add Body**. Set the following two parameters:
   - ipAddress: Change it to your IP address. This example uses "73.247.157.30"
   - licenseKey: Set this to 0 since we're just testing the API

   Example body:
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
     <soap:Body>
       <ResolveIP xmlns="http://ws.cdyne.com/">
         <ipAddress>73.247.157.30</ipAddress>
         <licenseKey>0</licenseKey>
       </ResolveIP>
     </soap:Body>
   </soap:Envelope>
   ```

3. Click **Save & Run** to run the request

4. To view results, click on the first item under **Recent Test Runs**. The SOAP API is going to return an XML object

### Validating Response Data with Assertions

Once you've established that the test and the SOAP API are working, let's make sure the response is returning the correct data. There are two methods for creating assertions in the API Monitoring interface:

#### Built-in XML Assertions

To use the built-in XML assertions:

1. Click the **Assertion** tab in the test editor. A default assertion is already set up to return a 200 status code
2. Click **+ Add Assertion** to add another assertion that will check that the City element is equal to the city our IP address resolves to
3. Set the following parameters:
   - Source: XML Body
   - Property: `//*[local-name()='City']/text()` - This represents an XPath expression to search for all elements named "City" and extract their text value. Learn more about XPath expression by using this [XPath Tester/Evaluator tool](http://www.freeformatter.com/xpath-tester.html)
   - Comparison: equals
   - Target Value: The city your IP address resolves to. In this case, we use "Chicago"
4. Rerun the test by clicking **Save & Run**
5. Check that the test run result page returns a 200 status code, and that the city our IP resolves to is equal to "Chicago"

#### Post-response Scripts

Another method for testing that the response data is correct is by using Post-response Scripts. We can use one of the included libraries, [marknote XML Parser](https://code.google.com/archive/p/marknote/wikis/DevelopersGuide.wiki), to work with the XML response and retrieve the elements we want to test.

To use Post-response Script:

1. In test *Steps*, navigate to the **Post-response Script** tab
2. Add the following script:
   ```javascript
   var str = response.body;
   var parser = new marknote.Parser();
   var xml = parser.parse(str);
   var body = xml.getRootElement();
   var resp = body.getChildElement("ResolveIPResponse");
   var result = resp.getChildElement("ResolveIPResult");
   var city = result.getChildElement("City");
   assert(city.getText() === "Chicago", "Windy City is correct!");
   ```
3. Rerun the test by clicking **Save & Run**
4. View the script output and success message in the test result

If you run into any issues with the Marknote parser, you can also convert your XML to JSON to more easily access properties. For example, our post-response script would be:

```javascript
var jsonResponse = JSON.parse(xmltojson(response.body));
var city = jsonResponse['ResolveIPResponse']['ResolveIPResult']['City'];
assert(city === "Chicago", "Windy City is correct!");
```

Using scripts can be useful if you plan to do something more complex with the data you get back from your SOAP API. You can also combine scripts with snippets to avoid repeating that boilerplate XML parsing code in our example script, and reuse assertions across multiple tests.

### SOAP Versions

- **SOAP 1.1**: Legacy SOAP version support
- **SOAP 1.2**: Modern SOAP version support
- **WSDL 1.1**: WSDL 1.1 specification support

### XML Validation

- **XML Assertions**: Validate XML structure and content
- **XPath Queries**: Use XPath for XML data extraction
- **Marknote Parser**: Parse XML in scripts using Marknote

### Best Practices

- Import WSDL for automatic operation discovery
- Use XML assertions for response validation
- Leverage XPath for data extraction
- Test both SOAP 1.1 and 1.2 if needed

---

## File Uploads and Multipart Requests

**The File Uploads feature requires a qualifying plan. Contact Sales to get started.**

The File Uploads feature enables teams to upload files to their BlazeMeter API Monitoring account that can be used to test and monitor endpoints that require `multipart/form-data` information, such as uploading a JSON file, an image, or a combination of multiple file types.

**Use when**: Uploading files for multipart/form-data requests, testing endpoints that require file uploads, or working with binary file bodies in API Monitoring tests.

### Manage Files

Users with "Manage Files" permission can access and manage a team's files. In the *File Uploads* page you can find three main sections: Upload a File, Existing Files, and History.

- **Upload a File** allows users with "Manage Files" permission to upload files to the team's account. There is a limit of 5 MB per file, and a total limit of 50 files per team.
- **Existing Files** will display all the files that are available for use under the account's team. You can see the filenames as well as delete any files by clicking on the trash icon on the right side.
- **History** will display a timeline of all the actions related to uploading and deleting files. You can see which user uploaded or deleted which files, as well as a timestamp with the exact time.

### Upload Files to the File Library

Follow these steps:

1. Click your profile on the top-right, and select **File Uploads** from the dropdown.
2. In the **Upload a file**section, click the **Choose File** button to choose the file you want to upload.
3. Click the **Upload File** button to upload your file. The maximum file size accepted is 5 MB, and there are no restrictions on file extensions.

You should now see your file available under the **Existing Files** section, as well as a new entry under the **History** section.

### Make Requests with a Multipart File Body or a Binary File

Follow these steps:

1. Select a bucket and create a new test, or open an existing test in the test editor.
2. Create a new **Request** step, and set your endpoint method to POST, PUT, PATCH, or DELETE.
3. Under **Parameters**, select one of the following: **+ Add Multipart Form Parameters**: Choose this option to pass a file in multiple parts. **+ Add Binary Body:** Choose this option to pass binary files such as images, video files, PDF, zip, HTML, or XML files.
4. Name your file parameter (required for multipart requests, optional for binary body), and click the drop-down next to it to select the file from your available uploaded files. BlazeMeter API Monitoring will try to set the Content-Type based on the file extension you have selected, such as application/json or image/jpeg, but you can also manually edit it. For binary files, the `Content-Type` can be found under Headers:
5. Click **Save & Run**.

After your test runs, you can click the new test run result on the left-hand side to check the details for your request. By expanding the details of a successful request step with the multipart file or binary file body, you should see:

- Under the **Request** tab, the file that you uploaded with your request (clicking on the link will download that file), as well as the body that we parsed and sent to the endpoint.
- Under the **Response** tab, any files that were returned by the API (clicking on the link will download that file), as well as any other headers and body information.

### Decode and Pass Binary Content to Another Request

You can decode and pass your binary content to another request.

**Example:** For the following binary content:

1. Perform a GET request on the binary file. The binary content is extracted into a variable under **Post-response Scripts**:

```javascript
variables.set("img", response.body);
```

2. In another request, under **Pre-request Scripts**, add the variable in request.body and populate request.content_type with the information found in the header:

```javascript
request.body = variables.get("img");
request.content_type = "image/jpeg"
```

3. Click **Save & Run**.

For more information on chaining requests, see [Dynamic Data and Request Chaining](skill-blazemeter-api-monitoring://references/advanced-features.md).

---

## Dynamic Data and Request Chaining

Variables allow you to dynamically insert data into a request using [built-in functions](skill-blazemeter-api-monitoring://references/advanced-features.md) (timestamps, random strings, hashes), configuration data from [environments](skill-blazemeter-api-monitoring://references/configuration.md) and data extracted from a previous response in a test run. Data is inserted into requests using a simple template format.

**Use when**: Using variables to pass data between test steps, working with environment variables, built-in functions, extracting data from JSON/XML responses, or chaining requests together.

### Use Variables to Pass Data Between Steps (Chained Requests)

Request steps can define variables that extract data from HTTP responses returned when running the test.

To create a variable, follow these steps:

1. Expand a request within your test.
2. Click **Variables**.
3. Specify the location of the data you want to extract from the response.
4. Choose a variable name to reference it in a subsequent request.

**Source** The location of the data to extract. Data can be extracted from HTTP header values, JSON body, response size or time, response status code, text body, or XML body.

**Property** The property of the source data to retrieve. For HTTP headers this is the name of the header. For XML and JSON content, see below. This field is unused for Text Body and Status Code.

**Variable Name** The name of the variable to assign the extracted value to. In subsequent requests you can retrieve the value of the variable by this name. See [Using Variables in Requests](skill-blazemeter-api-monitoring://references/advanced-features.md).

You can extract data through the following methods:

- **Extract data from JSON Body Content** Data from a JSON response body can be extracted by specifying the path of the target data using standard JavaScript notation. [View sample JSON expressions for data extraction](skill-blazemeter-api-monitoring://references/scripting.md).
- **Extract data from XML Body Content** Data from an XML response body can be extracted by specifying the path of the target data using [XPath](https://www.freeformatter.com/xpath-tester.html). In the 'Property' box of a variable definition that uses 'XML Body' as the source, enter an XPath expression to locate the data to extract and assign to the variable.
- **Extract data from Text Body** Saves the entire text of the response to a variable.
- **Extract data from Text Body using Post-response Scripts** You can specify the start and end boundaries of data to be extracted by running an extractor script through [Post-response Scripts](skill-blazemeter-api-monitoring://references/scripting.md).

### Environment Variables

[Environments](skill-blazemeter-api-monitoring://references/configuration.md) allow you to manage configuration on a per-test or per-bucket level. Common values (base URLs, API tokens, etc.) that are shared across requests within a test, or tests within a bucket, should be stored in an Initial Variable or Initial Script within an environment. Once defined, the variable is available to all requests within the test.

#### Initial Variables

Initial Variables specify data available to all requests in a test, including the first request. This can be useful for storing values that are common to all requests (like API keys) or other data required to set up the test run. Each test run will use the initial variables specified by the selected environment. To override variables on a per-run basis, use a [Trigger URL with Custom Initial Variables](skill-blazemeter-api-monitoring://references/integrations.md).

#### Initial Script

Initial Scripts are executed before the first request in a test is made, but after the Initial Variables have been evaluated. `variables.get()` and `variables.set()` can be used to read and write variable values to be used by requests in the test. See: [Scripts: Initial Script](skill-blazemeter-api-monitoring://references/scripting.md) and [Evaluation Order of Initial Variables](skill-blazemeter-api-monitoring://references/advanced-features.md).

### Use Built-in Variables and Functions

In addition to the variables you define yourself, you can use these built-in variables and functions to generate common types of data.

| Variable/Function | Description | Example Output |
|---|---|---|
| `{{timestamp}}` | Integer Unix timestamp (seconds elapsed since January 1, 1970 00:00 UTC) | 1384035195 |
| `{{utc_datetime}}` | UTC datetime string in ISO 8601 format. | 2013-11-07T19:24:41.418968 |
| `{{format_timestamp(value, format)}}` | Timestamp of the specified value in the specified `format`. Any delimiters (e.g. -, /, ., *, etc.) can be used in the `format` with a combination of any of the following date/time format options. Also accepts variables. E.g. `{{format_timestamp({{timestamp}}, YYYY-MM-DD)}}`<br>**YYYY** - 4 digit year (e.g. 2016)<br>**YY** - 2 digit year (e.g. 16)<br>**MM** - month<br>**DD** - day<br>**HH** - 24 hour (e.g. 13 == 1pm)<br>**hh** - 12 hour (e.g. 01 == 1pm)<br>**mm** - minutes<br>**ss** - seconds | 2013-31-03 |
| `{{timestamp_offset(value)}}` | Integer Unix timestamp offset by the specified `value` in seconds (going back in time would be a negative offset value). Values should be passed without surrounding quotes. | 1383948795 |
| `{{random_int}}` | Random integer between 0 and 18446744073709551615. | 407370955 |
| `{{random_int(a,b)}}` | Random integer value between `a` and `b`, inclusive. | 44674407370 |
| `{{random_string(length)}}` | Random alphanumeric string of the specified `length` (max 1000 characters). | ddo1qlQR81 |
| `{{uuid}}` | Random universally unique identifier (UUID). | 99386c08-6da7-4833-bb31-e70ce747c921 |
| `{{encode_base64(value)}}` | Encodes `value` in Base64. Values should be passed without surrounding quotes. Also accepts variables e.g. `{{encode_base64({{username}}:{{password}})}}` | dTpwDQo= |
| `{{md5(value)}}` | Generate an MD5 hash based on `value`. Values should be passed without surrounding quotes. Also accepts variables e.g. `{{md5({{timestamp}})}}` | 50b7fe4da64720232c25bc7c6d66f6c5 |
| `{{sha1(value)}}` | Generate an SHA-1 hash based on `value`. Values should be passed without surrounding quotes. Also accepts variables e.g. `{{sha1({{timestamp}})}}` | e0bd9304537cd8cb4e69ef5d73771fe218c484f5 |
| `{{sha256(value)}}` | Generate an SHA-256 hash based on `value`. Values should be passed without surrounding quotes. Also accepts variables e.g. `{{sha1({{timestamp}})}}` | e3376ffb4b1e2c04b0fe68b52e8654696814b4883b47a56ff5a7df883725d8c1 |
| `{{hmac_sha1(value,key)}}` | Generate an HMAC using the SHA-1 hashing algorithm based on `value` and `key`. Values should be passed without surrounding quotes. Also accepts variables e.g. `{{hmac_sha1({{timestamp}},key)}}` | 163a04cd86a82b948a7e85f0ed3cd3b5929a7d0c |
| `{{hmac_sha256(value,key)}}` | Generate an HMAC using the SHA-256 hashing algorithm based on `value` and `key`. Values should be passed without surrounding quotes. Also accepts variables e.g. `{{hmac_sha1({{timestamp}},key)}}` | eb0b5c5b2a04ac25ff52c886e115f2e60c0dd8d50bab076dc065e95f5fd37fb9 |
| `{{url_encode(value)}}` | Create a percent-encoded string suitable for URL querystrings. *This is not required for URL or form parameters defined in the request editor which are automatically encoded.* Only use this if you need to double encode a value in a URL or include a URL encoded string in a header value. | This%20is%20100%25%20URL%20encoded. |
| `{{runscope_environment}}` | The name of the environment used for this test run. | prod |
| `{{runscope_environment_uuid}}` | The unique ID of the environment used for this test run. | ab34b187-bcde-4f41-9ec1-ff77e99aa2d6 |
| `{{runscope_bucket}}` | The bucket key for the API Monitoring Bucket the executing test is contained within. | y0z5xkr1oa3m |
| `{{runscope_bucket_name}}` | The name of the API Monitoring Bucket the executing test is contained within. | Jumping Rabbit |
| `{{runscope_test_uuid}}` | The unique identifier for the API Monitoring test. | a8ea3ddd-73bb-435c-bc44-7c4bc8d99647 |
| `{{runscope_test_name}}` | The name of the API Monitoring test. | Sample Test |
| `{{runscope_region}}` | The region code indicating the [location](skill-blazemeter-api-monitoring://references/configuration.md) in which this test run was initiated. | eu1 |
| `{{runscope_agent}}` | The unique identifier for the [agent](skill-blazemeter-private-locations://references/radar-agent.md) which is running the agent. Blank if run from a API Monitoring location. | 83a24630-323d-501a-74a1-a7e51485ca12 |

Request an additional built-in variable or function by [contacting support](mailto:support-blazemeter@perforce.com?subject=Requesting built-in variable or function for API Monitoring).

When using a built-in variable in the value of an initial variable, the value will be generated once and remain constant across all the requests in a test (unless later overridden by another variable definition).

### Override Built-in Variables

You can define a variable that uses the same name as a built-in variable or function. This will override the built-in value with the value extracted from the test response.

### Use Variables in Requests

Once a variable has been defined, you can use it in any subsequent request. The test steps editor will display the 'Available Variables' that have been defined prior to the selected request. Variables can be used in any request data field including the method, URL, header values, parameter values and request bodies.

To include the value of a variable in a request, enter the name of the variable surrounded by double braces e.g. `{{variable_name}}`.

If a variable is undefined when a request using that variable is executed, the test will fail.

### Evaluation Order of Initial Variables

Variables can be set at various points in the setup of a test run. At each step of the setup, a variable value specified in an earlier step can be overridden. Variables defined via Trigger URLs, Initial Scripts and Initial Variables will be evaluated in the following order:

1. Variables defined in **a shared environment** (if the selected environment for a test run [inherits](skill-blazemeter-api-monitoring://references/configuration.md) from one).
2. Variables defined in an **individual test environment**.
3. Variables set via an environment-specific or a bucket-wide **Trigger URL**.
4. Variables set using `variables.set()` in a **shared environment's Initial Script**.
5. Variables set using `variables.set()` in an **individual test environment's Initial Script**.

---

## Convert to Performance Test

You can convert your API Monitoring tests into BlazeMeter Performance tests. This feature works by converting your existing JSON files (used for monitoring) into JMX files, the standard format for performance testing with Apache JMeter.

**Use when**: Converting API Monitoring tests into BlazeMeter Performance tests, transforming JSON configurations into JMX files for load testing, or scaling from functional monitoring to performance testing.

### How Conversion Works

API Monitoring tests are built to ensure the functionality and health of your APIs. By converting them into Performance tests, you can evaluate how your APIs perform under different load and stress conditions.

BlazeMeter takes your JSON configuration, which defines API calls, endpoints, request methods, parameters, and assertions, and transforms it into a JMX file format. This JMX file can be used directly in JMeter, saving you time and effort in recreating these tests manually.

By leveraging this feature, you can go beyond functional monitoring and gain deeper insights into your API's performance. Load test your APIs, check response times under various levels of stress, and pinpoint bottlenecks more effectively.

### Convert Your API Monitoring Test

To convert your API Monitoring test into a Performance test:

1. Navigate to the Test Editor by clicking on an existing test or selecting **Create Test**.
2. From the left pane, select **Convert**.
3. Select the **Workspace** and **Project** from your BlazeMeter account to convert the test into. A new Performance Test will be generated within the specified workspace and project.
4. Select **Convert to Performance Test**. Upon successful conversion, you will be redirected to the new Performance Test in a separate tab. The redirect will occur only if popups are enabled.

### Conversion Limitations

During conversion, steps like Request, Pause, and Conditional If are generally supported, but some limitations apply:

- **API Monitoring Test Settings**: Test settings (such as test environments) will not be converted into JMeter equivalents.
- **Unsupported Step Types**: Incoming/Inbound Requests, Conditional Loops, Subtests, and browser performance test steps will not be converted.
- **Assertion Limitations**: For Request steps, while API Monitoring supports various Assertions and Variable Extraction combinations, JMeter has limitations. For instance, API Monitoring allows you to assert that a specific JSON field's value is greater than 0, but JMeter's JSON Assertion does not have greater_than or less_than options, opting instead for comparisons like equal, not_empty, empty and not_equal. Incompatible assertions will be skipped during conversion.
- **Pause Step Handling**: In JMeter, Timers are always executed before a request (or any Sampler). If there is a Pause step between two requests in API Monitoring, JMeter attaches a Constant Timer to the second request. However, if a Pause step is at the end of a test or block (such as Conditional If), it is skipped during conversion as it serves no purpose. For example, a Pause step at the end of a Conditional If block will be omitted from the JMX file.
- **Script Conversion**: Pre-request and post-request scripts will be converted to JSR223PreProcessor and JSR223PostProcessor in JMeter, respectively. However, if a script uses any API Monitoring-specific functions, its content is not automatically converted. You will need to manually adjust the syntax.
- **File Operations**: Any API Monitoring operation that includes interaction with files, such as adding multipart bodies, binary bodies, or snippets, are not included in the conversion. You will have to handle them manually after the conversion process.

### Best Practices

- Review converted test before execution
- Adjust load configuration appropriately
- Test converted test with small load first
- Validate test behavior matches original
- Manually adjust API Monitoring-specific script functions
- Handle file operations manually after conversion

---

## Importing and Exporting Tests

You can export tests to the API Monitoring Export Format, and import request definitions from other services to create API Monitoring tests.

**Use when**: Exporting API Monitoring tests for sharing between teams or accounts, importing tests from other services (Postman, Swagger, OpenAPI, HAR, etc.), or migrating tests between environments.

### Exporting API Tests

The API Monitoring Export Format is a JSON representation of your API Test's steps.

**Export All Tests in a Bucket:**

1. Open a bucket's dashboard
2. Click **Export Now** at the bottom of the page

**Export Individual Tests:**

1. Open a test
2. Select the **Export** option on the left-hand side menu

You can import the downloaded file into any team's bucket to create a new test with the same step information. To learn more about the structure of exported tests, visit the [API Test Detail specification](https://help.blazemeter.com/apidocs/api-monitoring/tests_test_detail.htm).

### Importing API Tests

The following import formats are supported:

- **API Monitoring Export Format**: Import previously exported API Monitoring test steps
- **SmartBear Ready! API / SoapUI**: Export test suite as Swagger 2.0 JSON and use the Swagger importer
- **Swagger 2.0 (JSON, YAML)**: Import API definitions in JSON or YAML format
- **OpenAPI Specification 3.x (JSON, YAML)**: Import OpenAPI 3.x specifications
- **AWS API Gateway**: Import from AWS API Gateway
- **Postman**: Import Postman collections v1 and v2.1, individually or in bulk from a zip file
- **HTTP Archive (HAR) 1.1 and 1.2**: Import from Fiddler and Charles Proxy HAR exports
- **VCR Cassettes**: Import VCR versions 1 and 2 in YAML or JSON format
- **Paw**: Use the BlazeMeter API Monitoring API Test generator extension

### API Monitoring Export Format

You can import API Monitoring test steps that have been previously exported to the API Monitoring Export Format. Importing and exporting API tests is useful for sharing tests between teams or accounts. Imported tests must have at least one test step, and fewer than 100 steps.

### Swagger 2.0 and OpenAPI 3.x Import

**Swagger 2.0:**

- Each definition parses out to one test
- Each Operation Object corresponds to one test request step
- JSON pointers are supported, but multi-file uploads are not
- You can import all paths into a single test
- BlazeMeter can add an Accept request HTTP header based on the content type of the response

**Host and basePath:**

- The top-level Swagger `host` field is extracted and set to a variable `{{host}}`
- If no host field is present, defaults to `yourapihere.com`
- If a `basePath` is present, it is prepended to all request paths

**Parameters:**

- **Query Parameters**: Extracted as `?id={{id}}` format
- **Header Parameters**: Set as header name and value with uninitialized variables
- **Path Parameters**: Replaced by uninitialized variables (e.g., `/user/{id}` becomes `/user/{{id}}`)
- **Form Parameters**: Parsed same way as query parameters
- **Body Parameters**: Uninitialized variable appears as the raw body

**Security Requirements:**

- If `APIAuth` type is present, parsed as query or header parameter
- If `basic` type is present, basic auth is set with `{{username}}` and `{{password}}`

**OpenAPI 3.x:**

- Similar to Swagger 2.0 with additional options
- You can import all paths into a single test
- BlazeMeter can add an Accept request HTTP header based on the content type

### Postman Import

**Postman Dump Files:**

- Includes all collections, globals, environments, variables, and header presets
- Globals and scripts are not supported and will be ignored
- Each collection will be turned into an API test

**Postman Collections:**

- Supports Postman collections v1 and v2.1
- Can import individually or in bulk from a zip file
- Importing an individual collection will create a single test

### HAR Import

Currently, the only HAR field supported is `entries`, which represent HTTP requests. `Pages`, `comment`, `browser`, `creator` are ignored.

You can generate a HAR file from Fiddler and Charles Proxy from their Export menus.

### VCR Cassettes Import

- VCR versions 1 and 2 are supported
- Accepts import formats in YAML or JSON
- Currently not supported: `body-encoding` field and `http version` fields on the response object

### Best Practices

- Review imported tests for placeholder variables
- Set values for uninitialized variables after import
- Validate test steps after import
- Use export/import for test backup and version control
- Share tests between teams using export format

---

## Advanced Webhooks

Advanced webhooks are a powerful option to integrate BlazeMeter API Monitoring test run notifications with any workflow or third-party application.

**Use when**: Integrating API Monitoring test results with external systems, building custom workflows based on test results, or sending test run notifications to third-party applications.

### How Advanced Webhooks Work

This integration allows users to specify a URL, which BlazeMeter will use to send a JSON payload that includes the results of a test run via a POST request. That URL can be the endpoint of a 3rd-party application, or your own application that you can build to receive results of BlazeMeter API Monitoring test runs and then integrate those results to fit into your team's workflow.

### How to Use Advanced Webhooks

Follow these steps:

1. Go to your team's **Connected Services** page
2. Search for the advanced webhooks option, and select **Connect**
3. Fill in the required fields:
   - **Description**: The name that will be displayed in your list of Connected Services, and on the Integrations tab of the Environment Settings
   - **Threshold**: Select how often you want the notification to be sent
   - **URL**: The URL that the POST request will be sent to
   - **Authentication**: You can add Basic Authentication (username and password) to the request for security purposes
   - **Headers**: Add any custom headers that your application might require
4. Click **Save Changes**

Your advanced webhooks integration is now ready to be used. Do not forget to enable the integration on your environment settings to start receiving notifications on the configured callback URLs.

### Webhook Request & Payload

**Request Method:** POST

**Callback URL:** The URL you configured in the Connected Services

#### Sample Request Data

```json
{
  "variables": {
    "foo": "bar",
    "baz": "qux"
  },
  "test_id": "76598752-cbda-4e1d-820f-6274a62f74ff",
  "test_name": "Buckets Test",
  "test_run_id": "9c15aa62-21f0-48f2-a819-c99bdf8e4543",
  "team_id": "6b9c7f65-9e11-4f77-85ad-e6ee7a28232d",
  "team_name": "Acme Inc.",
  "environment_uuid": "98290cfc-a008-4ab7-9ea4-8906f12b228f",
  "environment_name": "Staging Settings",
  "bucket_name": "Rocket Sled",
  "bucket_key": "",
  "test_url": "https://www.runscope.com/radar//76598752-cbda-4e1d-820f-6274a62f74ff",
  "test_run_url": "https://www.runscope.com/radar//76598752-cbda-4e1d-820f-6274a62f74ff/results/9c15aa62-21f0-48f2-a819-c99bdf8e4543",
  "trigger_url": "https://api.runscope.com/radar/09039249-fdfd-4e1d-820f-6274a62f74ff/trigger",
  "result": "fail",
  "started_at": 1384281308.548077,
  "finished_at": 1384281310.680218,
  "agent": null,
  "agent_expired": null,
  "region": "us1",
  "region_name": "US East - Northern Virginia",
  "initial_variables": {},
  "requests": [{
    "step_type": "request",
    "url": "https://api.runscope.com/",
    "variables": {
      "fail": 0,
      "total": 1,
      "pass": 1
    },
    "assertions": {
      "fail": 0,
      "total": 2,
      "pass": 2
    },
    "scripts": {
      "fail": 0,
      "total": 1,
      "pass": 1
    },
    "result": "pass",
    "method": "GET",
    "response_time_ms": 123,
    "response_size_bytes": 2048,
    "response_status_code": 200,
    "note": "Root URL"
  }]
}
```

#### Webhook Payload Data Attributes

| Attribute | Description |
|-----------|-------------|
| `variables` | A dictionary containing all initial variables for this test run, and the variables extracted and stored from each step |
| `test_id` | The unique ID for the test responsible for this test run |
| `test_name` | The name of the test responsible for this test run |
| `test_run_id` | The unique ID of this specific test run |
| `team_id` | The unique ID of the team this test's bucket belongs to |
| `team_name` | The name of the team this test's bucket belongs to |
| `environment_uuid` | The UUID of the environment used by this test run |
| `environment_name` | The name of the environment used by this test run |
| `bucket_name` | The name of the bucket the test belongs to |
| `bucket_key` | The key of the bucket the test belongs to |
| `test_url` | The URL for viewing and editing this test in the API Monitoring dashboard |
| `test_run_url` | The URL for the test result detail page in the API Monitoring dashboard |
| `trigger_url` | The Trigger URL for this test. Typically used to retry a test run |
| `result` | The result of the test run, either `pass` or `fail` |
| `started_at` | The UNIX timestamp for the start of the test run |
| `finished_at` | The UNIX timestamp for the completion of the test run |
| `agent` | The agent used to execute this test run, or `null` if a default API Monitoring location was used |
| `agent_expired` | The status of the agent for this test run. This is `true` if the agent is expired, and `null` if the agent is available or if a default API Monitoring location was used |
| `region` | The region code for the location the test was run from, or `null` if an agent was used |
| `region_name` | The full region name and location the test was run from, or `null` if an agent was used |
| `initial_variables` | A dictionary of the test run's initial variables. This is the variable state after the initial scripts and variables have been processed (bucket-wide and test-specific) prior to the execution of the first request |
| `requests` | A list of the HTTP requests that were executed in this test run with the method, URL and assertion, variable and script success/failure counts |

### Best Practices

- Use Basic Authentication for secure webhook endpoints
- Configure custom headers as needed for your application
- Set appropriate thresholds to control notification frequency
- Handle webhook payloads asynchronously in your application
- Validate webhook signatures if implementing custom security
- Monitor webhook delivery and implement retry logic if needed

---

## Convert API Monitoring Test to Performance Test

Convert API Monitoring tests to Performance tests to run load tests based on your API Monitoring test scenarios.

**Use when**: Converting API Monitoring tests to Performance tests, running load tests based on API Monitoring scenarios, or migrating from API Monitoring to Performance Testing.

### Overview

The Convert to Performance Test feature allows you to transform your API Monitoring test into a Performance test that can be executed with load. This enables you to:

- Run load tests based on your API Monitoring test scenarios
- Scale your API tests to higher concurrency levels
- Leverage Performance Testing features like advanced reporting and analytics
- Combine API Monitoring and Performance Testing workflows

### How to Convert

Follow these steps:

1. Open your API Monitoring test
2. Navigate to the test settings or options menu
3. Select **Convert to Performance Test**
4. Configure the Performance test settings (users, duration, ramp-up, etc.)
5. Review and adjust the converted test configuration
6. Save and run the Performance test

### Considerations

- The converted test will maintain the same request structure and assertions
- You may need to adjust load configuration for Performance Testing
- Some API Monitoring-specific features may not be available in Performance Testing
- Review the converted test configuration before running at scale

### Documentation References

For detailed information about converting API Monitoring tests to Performance tests, use the BlazeMeter MCP help tools:

**Convert to Performance Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-convert-to-performance`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-convert-to-performance"]}`

---

## Documentation References

For detailed information about API Monitoring advanced features, use the BlazeMeter MCP help tools:

**AI Script Assistant**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-ai-script-assistant`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-ai-script-assistant"]}`

**GraphQL Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-graphql`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-graphql"]}`

**SOAP Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-soap-wsdl`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-soap-wsdl"]}`

**Dynamic Data and Request Chaining**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-dynamic-data-and-request-chaining`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-dynamic-data-and-request-chaining"]}`

**File Uploads and Multipart Requests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-file-uploads-and-multipart-requests`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-file-uploads-and-multipart-requests"]}`

**Convert to Performance Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-convert-to-performance`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-convert-to-performance"]}`

**Importing and Exporting Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-importing-exporting-tests`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-importing-exporting-tests"]}`

**Advanced Webhooks**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-advanced-webhooks`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-advanced-webhooks"]}`

