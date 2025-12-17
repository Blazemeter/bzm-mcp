# API Monitoring Scripting

## Initial Script

For each test and shared environment, you can specify a script that runs prior to the first request of an API test. If you have a complicated signature or other value that needs to be generated and is common to all requests (e.g. random number generator), this is the place to define it.

The initial script is processed after the [Initial Variables](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html#initial-variables) are processed and has access to those values through the `variables` global. Any variable values set with `variables.set(name, value)` will be available to the requests in the test. Any assertions defined in the initial script will be ignored.

An Initial Script specified in the shared environment will be executed *before* the Initial Script defined in an individual test environment, if the shared environment is [inherited by that test environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html#inheritance).

**Use when**: Setting up initialization logic that runs once before all test steps, configuring global variables, or setting up test environment.

### Overview

Initial Scripts execute once at the beginning of a test run, before any test steps. They're ideal for:
- Setting up global variables
- Initializing test data
- Configuring test environment
- Performing one-time setup operations
- Generating values common to all requests (e.g., random number generators, signatures)

### Accessing Initial Variables

The initial script has access to Initial Variables through the `variables` global:
- Use `variables.get(name)` to retrieve Initial Variable values
- Use `variables.set(name, value)` to set variables that will be available to all requests in the test

### Common Use Cases

- **Global Variable Setup**: Initialize variables used across multiple test steps
- **Environment Configuration**: Set up environment-specific settings
- **Data Initialization**: Prepare test data before test execution
- **Authentication Setup**: Configure authentication tokens or credentials
- **Complex Value Generation**: Generate signatures, random numbers, or other values common to all requests

### Using the AI Script Assistant

The AI Script Assistant can help generate Initial Scripts. When writing queries for the AI Script Assistant:

- User query should be related to the JavaScript code/script generation in context of API Monitoring (Runscope) tool only. The AI model will reject queries that are not related to script generation with the error: "Unable to generate a valid response for the given input. Please ensure the input is related to generation of scripts."
- If users want to store/get any kind of data in/from Runscope variable, they have to mention this explicitly in the query. For example: "Assert the response status code is 200 and assign it to a Runscope variable"
- If they don't mention Runscope variable, the AI model might assign the value to a JS variable. Remember syntax is different to assign values to a JS variable (`var x = value`) or Runscope variable (`variables.set('x', value)`)
- Keep queries crisp and clear for best results

### Best Practices

- Keep initialization logic concise
- Use for setup that applies to all test steps
- Avoid time-consuming operations in initial scripts
- Use `variables.set()` to make values available to all test steps
- Remember that assertions in initial scripts are ignored

---

## Pre-request Scripts

Pre-request Scripts give you a chance to modify the request after variables have been resolved, but before the request is made. You can use this script to do any last minute processing like adding additional headers or parameters to your shared environment, test, or test step. You can directly assign to any of the request data (except for size_bytes).

**Use when**: Modifying requests before execution, adding authentication headers, preparing request data, implementing request-level logic, or adding dynamic parameters and headers after variable resolution.

### Overview

Pre-request Scripts run before each HTTP request in a test step. They allow you to:
- Modify request headers
- Add authentication tokens
- Prepare request body data
- Set dynamic request parameters
- Modify request data after variables have been resolved

### Pre-Request Script Ordering

Defining pre-request scripts at the shared environment or environment level enables these scripts to run automatically for every Request test step. However, pre-request scripts are only applicable to Request test steps and do not work with other step types like Incoming Request or Condition.

If you set pre-request scripts at different levels (such as shared environment, test, or step), none of the scripts will be overwritten. Instead, they will execute in the following order:

1. **Shared Environment Pre-Request Scripts** - Execute first
2. **Environment (Test Settings) Pre-Request Scripts** - Execute second
3. **Test Step Pre-Request Scripts** - Execute last

### Common Use Cases

- **Dynamic Headers**: Add headers based on test data or previous responses
- **Authentication**: Add authentication tokens to requests (e.g., S3 authentication, OAuth)
- **Data Transformation**: Transform data before sending requests
- **Request Validation**: Validate request data before execution
- **URL Parameters**: Add or modify querystring parameters dynamically
- **Custom Headers**: Add custom headers based on request context

### Examples

#### Adding/Editing URL Parameters

```javascript
// Add a new querystring parameter ?foo=bar
request.params.push({name:"foo", value: "bar"});

// request.params is an array because we want to preserve the ordering of elements,
// but we also support and convert a dict/hash/object
request.params = {};
request.params["foo"] = "bar";
```

#### Adding a Custom Header

```javascript
var scheme = request.scheme;
var path = request.path;
// Add a new custom header that is the concatenation of the request
// scheme and path
request.headers["Custom-Header"] = scheme + " - " + path;
```

#### S3 Authentication

This example will automatically sign and authorize S3 requests for URLs that are private S3 resources. Just use the editor to make a request to a private S3 url (e.g. `GET https://s3.amazonaws.com/bucket-name/filename.txt`) and add this Pre-request Script to add authentication.

**Note**: This script requires you to define the following initial variables:
- `SecretAccessKeyId`
- `AWSAccessKeyId`

```javascript
// See https://docs.aws.amazon.com/AmazonS3/latest/userguide/RESTAuthentication.html
// for an explanation of the S3 authentication scheme

var date = moment().format("ddd, DD MMM YYYY HH:mm:ss ZZ");
var data = request.method + "\n" +
"" + "\n" + // content-md5 is "" for GET requests
"" + "\n" + // content-type is "" for GET requests
date + "\n" +
request.path;

var hash = CryptoJS.HmacSHA1(data, variables.get("SecretAccessKeyId"));
var signature = hash.toString(CryptoJS.enc.Base64);
// Build the auth header
var auth = "AWS " + variables.get("AWSAccessKeyId") + ":" + signature;
request.headers["Authorization"] = auth;
request.headers["Date"] = date;
```

### Best Practices

- Use for request-specific modifications
- Keep scripts focused on single responsibility
- Reuse code through snippets when possible
- Remember that pre-request scripts execute after variables are resolved
- Pre-request scripts only work with Request test steps, not other step types

---

## Post-response Scripts

Post-response Scripts allow you to evaluate the response from an individual request, typically to make assertions to validate the data. You can also extract information from the response headers or body content and store in a variable for later use. Lastly, Post-response scripts can modify HTTP request and responses to remove sensitive information before it is stored.

**Use when**: Validating responses, extracting data from responses, implementing response-level logic, preparing data for subsequent requests, defining complex assertions, or removing sensitive data from stored requests/responses.

### Overview

Post-response Scripts run after each HTTP response is received. They enable:
- Response validation beyond assertions
- Data extraction from responses
- Response transformation
- Complex test logic based on responses
- Defining assertions using Chai Assertion Library
- Getting and setting variables
- Removing sensitive data from HTTP requests and responses

### Post-response Script Ordering

Defining post-response scripts at the shared environment or environment level allows these scripts to run automatically after every Request test step is executed. However, post-response scripts are only applicable to Request test steps and do not work with other step types like Incoming Request, Condition, or others.

If you define post-response scripts at multiple levels (shared environment, test, or step), no scripts will be overwritten; they will be executed in the following order:

1. **Shared Environment Post-Response Scripts** - Execute first
2. **Environment (Test Settings) Post-Response Scripts** - Execute second
3. **Test Step Post-Response Scripts** - Execute last

### Defining Assertions

Scripts allow for complex assertion definitions that are not possible to define in the test editor. Assertions are defined using the `assert` module of the [Chai Assertion Library](https://www.chaijs.com/api/assert/) which is included for every script. Both the request and response data objects are available to use in your assertions.

#### Common Assertion Syntax Reference

- `assert(expression, message)` - Write your own test expressions
- `assert.ok(object, [message])` - Asserts that object is truthy
- `assert.notOk(object, [message])` - Asserts that object is falsy
- `assert.equal(actual, expected, [message])` - Asserts non-strict equality (==)
- `assert.notEqual(actual, expected, [message])` - Asserts non-strict inequality (!=)

#### Additional Assertion Options

Chai.js by default truncates long assertion response messages. If you wish to see the full message without any truncation, add the following line of code at the top of your scripts:

```javascript
chai.config.truncateThreshold = 0;
```

Chai offers additional assertion options including checking for nulls, strict equality comparisons, type checking, regex matching, deep object comparisons and more. The library also includes `should` and `expect` assertion styles.

#### Assertion Examples

```javascript
// check for specific status code
assert.equal(response.status, 200, "status was 200 OK");

// parse JSON response body into object
var data = JSON.parse(response.body);

// check for specific JSON attribute value
assert.ok(data.is_admin, "customer is an admin");

// check an array for the presence of an item
var exists = false;
var customers = data.customers;
for (var customer in customers) {
  if (customers[customer].id === 123) {
    exists = true;
    break;
  }
}
assert.ok(exists, "customer 123 exists");

// check that all items in a list contain a numeric id with regex and Underscore.js library
assert(_.every(data.customers, function(customer) { 
  return customer.id.match(/^\d+$/); 
}), "IDs are all numeric");

// check for existence of key named id with Underscore.js library
assert(_.has(data, "id"), "contains 'id' key");

// check that a timestamp is less than now with Moment.js library
var created_at = moment.unix(data["created_at"]);
var now = moment();
assert(now.isAfter(created_at), "create date before now");
```

### Getting and Setting Variables

Scripts have access to all Variables that have been defined in Initial Variables/Initial Script, the test editor, and previous scripts through the `variables` global object. Setting a variable value will make it available to subsequent scripts and requests.

**Getting a Variable Value**:
```javascript
var id = variables.get("id");
```

**Setting a Variable Value**:
```javascript
// grab a newly-created user ID and store for later
var data = JSON.parse(response.body);
variables.set("id", data.id);
```

### Removing Sensitive Data from HTTP Requests and Responses

You can also use Post-response Scripts to remove data from the HTTP request and response before being stored for viewing. Edit the `request` and `response` objects directly to remove sensitive data like API keys:

```javascript
// clear out Authorization header
request.headers.Authorization = "";

// redact customer phone numbers
var data = JSON.parse(response.body);
for (var customer in data.customers) {
  customer.phone_number = customer.phone_number.slice(0, -4) + "XXXX";
}
response.body = JSON.stringify(data);
```

### Extracting Variable Data from Text Body

You can use Post-response Scripts to extract data from Text Body by defining the start and end boundaries of extraction.

For instance, if you wish to extract the value `QEJ342834982389dDJD` from the following response:

```html
<html lang="en">
<head>
<meta charset="utf-8">
<title> BlazeDemo</title>
<meta name="description" content="BlazeMeter demo app">
<meta name="sage" content="flights app">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
<script src="/assets/bootstrap.min.js"></script>
<script>var a = 22; var b = 30; EncryptedString = "QEJ342834982389dDJD"</script>
<script src="/assets/bootstrap-table.js"></script>
<link href="/assets/bootstrap.min.css" rel="stylesheet" media="screen">
<link href="/assets/bootstrap-table.css" rel="stylesheet" media="screen">
<style type="text/css">
body {
background: #f5f5f5);
}
.hero-unit {
background-color: #fff;
}
.center {
display: block;
margin: 0 auto;
}
</style>
</head>
</html>
```

You can run the following extractor script:

```javascript
var ResponseVar = variables.get("Response");
var extractedtext;
var leftboundary = "EncryptedString = \"";
var rightboundary = "\";</script";
extractedtext = ResponseVar.substring(
  ResponseVar.lastIndexOf(leftboundary) + leftboundary.length,
  ResponseVar.lastIndexOf(rightboundary)
);
variables.set("SecretCode", extractedtext);
console.log(extractedtext);
```

Which results in:
```
QEJ342834982389dDJD
```

### Common Use Cases

- **Data Extraction**: Extract values from responses for use in subsequent requests
- **Response Validation**: Implement custom validation logic using Chai assertions
- **Error Handling**: Handle errors and implement retry logic
- **Response Transformation**: Transform response data for analysis
- **Sensitive Data Removal**: Remove or redact sensitive information before storage
- **Complex Assertions**: Create assertions that go beyond the test editor capabilities

### Best Practices

- Use for response-specific processing
- Extract reusable logic into snippets
- Implement proper error handling
- Use Chai assertions for complex validation
- Remove sensitive data before storage
- Use variables to pass data between requests

---

## Custom Libraries

Upload and use custom JavaScript libraries in API Monitoring tests for extended functionality and code reuse.

**Use when**: Extending API Monitoring functionality with custom JavaScript libraries or reusing custom code across multiple API Monitoring tests.

### Overview

Custom Libraries allow you to upload and use your own JavaScript libraries in API Monitoring tests, enabling:
- Code reuse across tests
- Extended functionality
- Custom utility functions
- Shared business logic

### Uploading Custom Libraries

Custom Script Libraries belong to a team. From your team list, select "Script Library" to manage previously-uploaded libraries and to upload new ones.

1. Navigate to team settings
2. Select "Script Library" from the team list
3. Upload JavaScript library files (maximum 1MB per library)
4. Enable libraries in environment settings
5. Reference libraries in test scripts

### Enabling Custom Libraries in Environments

After a library is uploaded, you can make it available to scripts by enabling it in an environment:

1. Expand the Environment editor at the top of the test editor
2. Select "Script Libraries"
3. Toggle custom libraries on or off
4. Enable only the scripts required by tests using the environment

**Note**: Enabling many large script libraries may impact the run-time performance of your tests.

### Limitations

- Maximum library size: 1MB per library
- Built-in variables, functions and libraries are loaded first, followed by custom libraries. You may overwrite built-in functionality in your custom libraries and scripts, but doing so is unsupported and may cause unexpected results
- See [Script Engine Technical Details and Limitations](https://help.blazemeter.com/docs/guide/api-monitoring-script-engine-overview.html#technical-details) for complete information

### Example Libraries

We maintain a [GitHub repository](https://github.com/Runscope/script-libraries) of scripts that have been tested working with the script engine. Have a script you think may be useful to others? Submit a pull request!

### Best Practices

- Organize libraries by functionality
- Document library functions
- Version control library code
- Test libraries before production use
- Enable only required libraries to optimize performance

---

## Included Libraries

The following libraries are automatically included for every script. You can also upload your own [Custom Libraries](#custom-libraries).

**Use when**: Using built-in JavaScript libraries in API Monitoring scripts or understanding what libraries are available by default.

### Available Included Libraries

The Script Engine automatically includes the following libraries:

- **Underscore.js** (v1.13.6) - Utility library for JavaScript. Note: `_.matches()` is deprecated
- **Chai Assertion Library** (v4.3.8) - Assertion library for testing. Note: `deepProperty()` and `notDeepProperty()` are not available in the latest release
- **Chai JSON-Schema** (v1.1.0) - JSON schema validation for Chai
- **chai-fuzzy** (269c01e) - Fuzzy matching for Chai assertions
- **Moment.js** (v2.29.4) - Date and time manipulation library. Includes locales
- **CryptoJS** (v3.1.2) - Cryptographic functions. Supports AES, SHA-1, SHA-256, HMAC-SHA1, HMAC-SHA256, MD5 only
- **json2.js** (2014-02-04) - JSON parsing and stringification
- **marknote XML Parser** (v0.5.1) - XML parsing library. Note: HTTP retrieval is disabled

### Usage Examples

```javascript
// Using Underscore.js for data manipulation
const _ = require('underscore');
const filtered = _.filter(data, item => item.active);

// Using Moment.js for date manipulation
const moment = require('moment');
const date = moment().format('YYYY-MM-DD');

// Using CryptoJS for hashing
const CryptoJS = require('crypto-js');
const hash = CryptoJS.SHA256('message').toString();
```

---

## Custom Libraries

The Script Engine supports custom scripts and libraries uploaded by your team. Each library can be individually enabled on a per-environment basis.

**Use when**: Uploading custom JavaScript libraries for use in API Monitoring scripts or enabling custom libraries in test environments.

### Uploading a Library

Custom Script Libraries belong to a team. From your team list, select **Script Library** to manage previously-uploaded libraries and to upload new ones.

### Limitations

To ensure the performance and security of your tests, custom script libraries have a few limitations:
- Each uploaded library has a maximum size of 1MB
- When scripts are processed, built-in variables, functions and libraries are loaded first, followed by custom libraries
- You may overwrite built-in functionality in your custom libraries and scripts, but doing so is unsupported and may cause unexpected results

For more information, see [Script Engine Technical Details and Limitations](skill-blazemeter-api-monitoring://references/scripting.md).

### Enabling Custom Libraries in Environments

After a library is uploaded, you can make it available to scripts by enabling it in an environment:
1. Expand the Environment editor at the top of the test editor
2. Select **Script Libraries** to toggle custom libraries on or off
3. Enable only the scripts required by tests using the environment

**Note**: Enabling many large script libraries may impact the run-time performance of your tests.

### Example Libraries

We maintain a [GitHub repository](https://github.com/Runscope/script-libraries) of scripts that have been tested working with the script engine. Have a script you think may be useful to others? Submit a pull request!

### Related Topics

- [Script Snippets](skill-blazemeter-api-monitoring://references/scripting.md)
- [Script Engine Overview](skill-blazemeter-api-monitoring://references/scripting.md)

---

## Script Engine Overview

The Script Engine is a powerful tool for constructing API tests and validating API responses. Custom JavaScript can be executed at various points in the test execution lifecycle:
- Before the first step to set up environment data
- Before each individual request step to dynamically modify request data
- After a step completes to validate the response

Standard JavaScript modules like Math and RegExp are available along with a set of included helper libraries. Scripts have access to the current variable context and complete request and response data.

The Script Engine is ideal for cases that require more flexibility than simple Assertions and Variables. Scripts, assertions and variables work together seamlessly, each being evaluated at different points in the lifecycle of a test step.

**Use when**: Understanding JavaScript script engine capabilities and execution context or writing custom scripts for API Monitoring tests.

### Execution Context

- **Initial Script**: Runs once before all test steps
- **Pre-request Script**: Runs before each HTTP request
- **Post-response Script**: Runs after each HTTP response

### Built-in Variables and Functions

Every script has access to the following values:

#### Response Data

The `response` object is only available in post-response scripts:

- `response.body` - The response body as a string
- `response.headers` - A dictionary of response headers (keys are header names, values are arrays)
- `response.reason` - The reason portion of the HTTP status line (read-only)
- `response.response_time_ms` - The time taken to execute the request and receive the response in milliseconds (read-only)
- `response.size_bytes` - The size of the response body in bytes (read-only)
- `response.status` - The response's status code (read-only)

#### Request Data

The `request` object is available in both pre-request and post-response scripts:

- `request.body` - The request body as a string
- `request.form` - A dictionary of form parameters (keys are parameter names, values are arrays)
- `request.headers` - A dictionary of request headers (keys are header names, values are arrays)
- `request.host` - The hostname of the URL executed
- `request.method` - The request method (GET, POST, etc.)
- `request.params` - A dictionary of URL parameters/querystring (keys are parameter names, values are arrays)
- `request.path` - The path segment of the URL without URL parameters
- `request.scheme` - `http` or `https`
- `request.size_bytes` - The size of the request body in bytes (read-only)
- `request.url` - The fully-assembled URL that was accessed

#### API Test Variables

The `variables` global is available in both pre-request and post-response scripts:

- `variables.get(name)` - Return a value from the current variable context
- `variables.set(name, value)` - Set a variable value. Setting a variable in a pre-request script does not make the value available to the currently request step as scripts are evaluated after the template variables are inserted

#### Helper Functions

- `log(Object|string)` - Write a string or pretty-printed version of an object to the output log viewable in test results
- `encode_base64(value)` - Encode a string value as Base64
- `decode_base64(value)` - Decode a Base64-encoded string
- `runscope_bucket` - The key of the bucket the test belongs to and was executed in
- `get_secret(key)` - Returns the value for the secret with key name (see Secrets Management)

#### JavaScript Functions

The script interpreter also supports common JavaScript objects and functions:
- Math
- Date
- RegExp
- parseInt, parseFloat
- decodeURI, decodeURIComponent
- encodeURI, encodeURIComponent
- escape, unescape
- btoa (URL-friendly Base64 encode)
- atob (URL-friendly Base64 decode)

### Debugging Scripts

If you are receiving unexpected script errors, try the following to debug issues:

- Use the `log()` function to write out values to be viewed with the test results. `log()` will "pretty print" the values of objects so they are easily readable. Using `console.log` is not recommended
- Verify your JavaScript is valid with a tool like JSLint
- Make sure the script is completing execution in under 3 seconds
- Verify you are using functions supported in the documented version of included libraries
- Do not overwrite the `request` and `response` objects entirely. Edit only specific attributes as needed

### Technical Details and Limitations

The Script Engine is a V8-compatible (version 3.28), sandboxed JavaScript interpreter. To ensure the performance and security of your scripts and API data, some limitations have been put in place:

- The Script Engine is a raw interpreter and does not include a framework like Node.js. Network (XHR or otherwise) and file system access is also prohibited. All HTTP calls must be made from request steps in your tests
- Each script is evaluated as a single block with everything in the global scope. Module loaders like CommonJS, require(), AMD, etc. are not supported. While some npm modules may be able to be made to work, they do not by default
- Built-in variables, functions and libraries are loaded first, followed by custom libraries. You may overwrite built-in functionality in your custom libraries and scripts, but doing so is unsupported and may cause unexpected results
- All scripts must complete their execution within 20 seconds

---

## Reusable Snippets

Create and manage reusable JavaScript code snippets for API Monitoring tests to promote code reuse across requests and tests.

**Use when**: Creating reusable JavaScript code for API Monitoring tests or promoting code reuse across multiple requests and tests.

### Creating Snippets

1. Navigate to team or bucket settings
2. Create new code snippet
3. Write reusable JavaScript code
4. Save snippet with descriptive name

### Using Snippets

- Reference snippets in test scripts
- Pass parameters to snippets
- Use snippets across multiple tests
- Update snippets to affect all tests

### Best Practices

- Create snippets for common operations
- Document snippet parameters and usage
- Keep snippets focused and reusable
- Version control snippet code

---

## Validating Responses with Assertions

Assertions allow you to specify expected data in the response to a request made in a test run. When a test is run, the outcome is determined by whether or not all the assertions pass. If any assertion fails, the test fails. Assertions can be made against response header values, status code, response time/size, and content (like JSON or XML).

**Use when**: Validating API responses, checking status codes, verifying response content, ensuring response quality, or defining expected response data for test validation.

### Define Assertions

You can define zero or more assertions for any request in a test. The response data from the original request and the result of the last run are provided below the assertion editor for reference.

Each assertion consists of four items:

1. **Source** - The location of the data to extract for comparison. Data can be extracted from HTTP header values and JSON, XML or text body content. You can also create assertions based on the response status code, time and size.

2. **Property** - The property of the source data to retrieve. For HTTP headers, this is the name of the header. For XML and JSON content, see below. Unused for text content, status code, response time and response size.

3. **Comparison** - The type of operation to perform when comparing the extracted data with the target value. See [Comparisons](#comparisons) section below.

4. **Target Value** - The expected value used to compare against the actual value. The target value can contain a static value or a variable using the template syntax.

### Asserting Against Data from JSON Body Content

Data from a JSON response body can be extracted by specifying the path of the data using standard JavaScript notation. For example:
- `data.users[0].id` - Extract the id of the first user
- `data.status` - Extract the status field
- `data.items.length` - Extract the length of the items array

For more examples, see [Sample JSON Expressions for Data Extraction](skill-blazemeter-api-monitoring://references/scripting.md) section below.

### Asserting Against Data from XML Body Content

Data from an XML response body can be extracted by specifying the path of the data using [XPath](https://www.freeformatter.com/xpath-tester.html). In the 'Property' box of an assertion definition that uses 'XML Body' as the source, enter an XPath expression to locate the data to extract.

### Comparisons

When an assertion is processed, the **Actual Value** consists of the data located by Source and Property. The **Target Value** is the value you entered into the assertion editor.

| Comparison | Description |
|------------|-------------|
| **is empty** | The actual value exists and is an empty string or null. |
| **is not empty** | The actual value exists and is a value other than an empty string or null. |
| **equals** | A string comparison of the actual and expected value. Non-string values are cast to a string before comparing. For comparing non-integer numbers, use **equals (number)**. |
| **does not equal** | A string comparison of the actual and target value. |
| **contains** | The actual value contains the target value as a substring. |
| **does not contain** | The target value is not found within the actual value. |
| **has key** | Checks for the existence of the expected value within a dictionary's keys. The actual value must point to a dictionary (JSON only). |
| **has value** | Checks a list or dictionary for the existence of the expected value in any of the list or dictionary values. The actual value must point to a JSON list or dictionary (JSON only). |
| **is null** | Checks that a value for a given JSON key is null. |
| **is a number** | Validates the actual value is (or can be cast to) a valid numeric value. |
| **less than** | Validates the actual value is (or can be cast to) a number less than the target value. |
| **less than or equal** | Validates the actual value is (or can be cast to) a number less than or equal to the target value. |
| **greater than** | Validates the actual value is (or can be cast to) a number greater than the target value. |
| **greater than or equal** | Validates the actual value is (or can be cast to) a number greater than or equal to the target value. |
| **equals (number)** | Validates the actual value is (or can be cast to) a number equal to the target value. This setting performs a numeric comparison: for example, "1.000" would be considered equal to "1". |

### Assertion Types

- **Status Code Assertions**: Verify HTTP status codes
- **Body Assertions**: Validate response body content (JSON, XML, or text)
- **Header Assertions**: Check response headers
- **Response Time Assertions**: Validate response performance
- **Response Size Assertions**: Validate response size

### Best Practices

- Use appropriate assertion types for your validation needs
- Combine multiple assertions for comprehensive validation
- Use custom assertions in post-response scripts when needed for complex validation
- Use template variables in target values for dynamic assertions
- For numeric comparisons, use "equals (number)" instead of "equals" to avoid string comparison issues
- More advanced assertions can be created by using [Post-response Scripts](#post-response-scripts)

---

## Sample JSON Expressions for Data Extraction

When using [variables](skill-blazemeter-api-monitoring://references/advanced-features.md) or [assertions](skill-blazemeter-api-monitoring://references/scripting.md) that extract data from JSON bodies, you'll need to specify a JSON object expression to locate the data to extract. Here are some examples.

**Use when**: Extracting data from JSON response bodies, using JSON expressions in variables or assertions, or working with nested JSON structures and arrays.

### Sample Object Data

```
{
"firstName": "Grace",
"lastName": "Hopper",
"age": 107,
"address": {
"streetAddress": "21 2nd Street",
"city": "New York",
"state": "NY",
"postalCode": 10021
},
"phoneNumbers": [
{
"type": "home",
"number": "212-555-1234"
},
{
"type": "mobile",
"number": "646-555-4567"
}
]
}
```

### Example 1: Top-level property

**Expression**: `lastName`  
**Value**: `Hopper`

### Example 2: Nested property

**Expression**: `address.city`  
**Value**: `New York`

### Example 3: Nested property within array

**Expression**: `phoneNumbers[0].number`  
**Value**: `212-555-1234`

### Example 4: Nested property within last element of array

**Expression**: `phoneNumbers[-1].number`  
**Value**: `646-555-4567`

---

### Sample Array Data

```
[
{
"type": "home",
"number": "212-555-1234"
},
{
"type": "mobile",
"number": "646-555-4567"
},
{
"type": "work",
"number": "651-555-0000"
}
]
```

### Example 1: Object property within root-level array

**Expression**: `[2].number`  
**Value**: `651-555-0000`

### Example 2: Retrieve the type of the second to last item in the array

**Expression**: `[-2].type`  
**Value**: `mobile`

---

## Documentation References

For detailed information about API Monitoring scripting, use the BlazeMeter MCP help tools:

**Initial Script**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-initial-script`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-initial-script"]}`

**Pre-request Scripts**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-pre-request-scripts`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-pre-request-scripts"]}`

**Post-response Scripts**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-post-response-scripts`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-post-response-scripts"]}`

**Validating Responses with Assertions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-validating-responses-with-assertions`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-validating-responses-with-assertions"]}`

**Script Engine Overview**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-script-engine-overview`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-script-engine-overview"]}`

**Reusable Snippets**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-reusable-snippets`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-reusable-snippets"]}`

**Sample JSON Expressions for Data Extraction**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-sample-json-expressions-for-data-extraction`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-sample-json-expressions-for-data-extraction"]}`

**Included Libraries**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-included-libraries`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-included-libraries"]}`

**Custom Libraries**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-custom-libraries`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-custom-libraries"]}`

