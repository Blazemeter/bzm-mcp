# API Monitoring Scripting

## Custom Libraries

Upload and use custom JavaScript libraries in API Monitoring tests for extended functionality and code reuse.

**Use when**: Extending API Monitoring functionality with custom JavaScript libraries or reusing custom code across multiple API Monitoring tests.

### Overview

Custom Libraries allow you to upload and use your own JavaScript libraries in API Monitoring tests, enabling:
- Code reuse across tests
- Extended functionality
- Custom utility functions
- Shared business logic

### Uploading a Library

Custom Script Libraries belong to a team. From your team list, select "Script Library" to manage previously-uploaded libraries and to upload new ones.

**Steps:**
1. Navigate to your team list in API Monitoring
2. Select "Script Library" to manage libraries
3. Upload JavaScript library files
4. Enable libraries in environments as needed

### Limitations

To ensure the performance and security of your tests, custom script libraries have a few limitations. [Please review the Script Engine Technical Details and Limitations to learn more](https://help.blazemeter.com/docs/guide/api-monitoring-script-engine-overview.html#technical-details).

- **Maximum Size**: Each uploaded library has a maximum size of 1MB
- **Loading Order**: When scripts are processed built-in variables, functions and libraries are loaded first, followed by custom libraries. You may overwrite built-in functionality in your custom libraries and scripts, but doing so is unsupported and may cause unexpected results

### Enabling Custom Libraries in Environments

After a library is uploaded you can make it available to scripts by enabling it in an environment. Expand the Environment editor at the top of the test editor and select "Script Libraries" to toggle custom libraries on or off. Enable only the scripts required by tests using the environment. Enabling many large script libraries may impact the run-time performance of your tests.

**Steps:**
1. Expand the Environment editor at the top of the test editor
2. Select "Script Libraries"
3. Toggle custom libraries on or off
4. Enable only the scripts required by tests using the environment

### Example Libraries

We maintain a [GitHub repository](https://github.com/Runscope/script-libraries) of scripts that have been tested working with the script engine. Have a script you think may be useful to others? Submit a pull request!

### Best Practices

- Organize libraries by functionality
- Document library functions
- Version control library code
- Test libraries before production use
- Enable only required libraries in environments to optimize performance
- Keep library size under 1MB

---

## Included Libraries

Understand and utilize built-in JavaScript libraries available in API Monitoring script engine, including Chai, Lodash, and others.

**Use when**: Leveraging built-in JavaScript libraries in API Monitoring scripts or writing complex test logic that requires utility functions.

### Available Libraries

The following libraries are automatically included for every script. You can also upload your own [Custom Libraries](https://help.blazemeter.com/docs/guide/api-monitoring-custom-libraries.html).

| Library | Version | Restrictions |
|---------|---------|--------------|
| Underscore.js | 1.13.6 | `_.matches()` is deprecated. [View docs](https://underscorejs.org/) |
| Chai Assertion Library | 4.3.8 | `deepProperty()` is not available in the latest release. `notDeepProperty()` is not available in the latest release. Function name is changed from `PropertyNotVal()` to `notPropertyVal()`. Function name is changed from `deepPropertyNotVal()` to `notDeepPropertyVal()`. [View docs](https://www.chaijs.com/) |
| Chai JSON-Schema | 1.1.0 | [View docs](https://github.com/chaijs/chai-json-schema) |
| chai-fuzzy | 269c01e | [View docs](https://github.com/chaijs/chai-fuzzy) |
| Moment.js | 2.29.4 | Includes locales. [View docs](https://momentjs.com/) |
| CryptoJS | 3.1.2 | AES, SHA-1, SHA-256, HMAC-SHA1, HMAC-SHA256, MD5 only. [View docs](https://cryptojs.gitbook.io/docs/) |
| json2.js | 2014-02-04 | [View docs](https://github.com/douglascrockford/JSON-js) |
| marknote XML Parser | 0.5.1 | HTTP retrieval disabled. [View docs](https://github.com/andrewrk/node-marknote) |

### Usage Examples

**Using Chai for assertions:**
```javascript
// Chai is available globally, no require needed
expect(response.status).to.equal(200);
expect(response.body).to.be.a('string');
```

**Using Underscore.js for data manipulation:**
```javascript
// Underscore is available as _ globally
const filtered = _.filter(data, item => item.active);
const mapped = _.map(data, item => item.id);
```

**Using Moment.js for date/time:**
```javascript
// Moment is available globally
const now = moment();
const formatted = moment().format('YYYY-MM-DD');
```

**Using CryptoJS for encryption:**
```javascript
// CryptoJS is available globally
const hash = CryptoJS.SHA256('message');
const encrypted = CryptoJS.AES.encrypt('message', 'secret');
```

---

## Initial Script

Create initial scripts that run once before all test steps in API Monitoring tests, useful for setup and initialization.

**Use when**: Setting up initialization logic that runs once before all test steps, configuring global variables, or setting up test environment.

### Overview

For each test and shared [environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html), you can specify a script that runs prior to the first request of an API test. If you have a complicated signature or other value that needs to be generated and is common to all requests (e.g. random number generator), this is the place to define it.

The initial script is processed after the [Initial Variables](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html#initial-variables) are processed and has access to those values through the `variables` global. Any variable values set with `variables.set(name, value)` will be available to the requests in the test. Any assertions defined in the initial script will be ignored.

**Execution Order:**
- An Initial Script specified in the shared environment will be executed *before* the Initial Script defined in an individual test environment, if the shared environment is [inherited by that test environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html#inheritance)

Initial Scripts execute once at the beginning of a test run, before any test steps. They're ideal for:
- Setting up global variables
- Initializing test data
- Configuring test environment
- Performing one-time setup operations
- Generating values common to all requests (e.g. random number generator)

### Common Use Cases

- **Global Variable Setup**: Initialize variables used across multiple test steps
- **Environment Configuration**: Set up environment-specific settings
- **Data Initialization**: Prepare test data before test execution
- **Authentication Setup**: Configure authentication tokens or credentials
- **Random Value Generation**: Generate random numbers or values common to all requests

### Using the AI Script Assistant

Adding the advice for writing a good query:
- User query should be related to the JavaScript code/script generation in context of Runscope (API Monitoring) tool only. AI model will reject the query with this error message "Unable to generate a valid response for the given input. Please ensure the input is related to generation of scripts in case of any deviation from the expected behaviour."
- If users want to store/get any kind of data in/from the Runscope variable then they have to mention this in the query. For example: "Assert the response status code is 200 and assign it to a Runscope variable." If they don't mention Runscope variable then AI model might assign the value to JS variable. Remember syntax is different to assign values to a JS variable or Runscope variable.

### Best Practices

- Keep initialization logic concise
- Use for setup that applies to all test steps
- Avoid time-consuming operations in initial scripts
- Access initial variables through the `variables` global
- Set variables using `variables.set(name, value)` to make them available to requests
- Note that assertions defined in initial scripts will be ignored

---

## Script Engine Overview

Understand the JavaScript script engine in API Monitoring, including available functions, variables, and execution context.

**Use when**: Understanding JavaScript script engine capabilities and execution context or writing custom scripts for API Monitoring tests.

The Script Engine is a powerful tool for constructing API tests and validating API responses. Custom JavaScript can be executed at various points in the test execution lifecycle:
- [Before the first step](https://help.blazemeter.com/docs/guide/api-monitoring-initial-script.html) to set up environment data
- [Before each individual request step](https://help.blazemeter.com/docs/guide/api-monitoring-pre-request-scripts.html) to dynamically modify request data
- [After a step completes](https://help.blazemeter.com/docs/guide/api-monitoring-post-response-scripts.html) to validate the response

Standard JavaScript modules like Math and RegExp are available along with a set of included helper [libraries](https://help.blazemeter.com/docs/guide/api-monitoring-included-libraries.html). Scripts have access to the current variable context and complete [request and response data](https://help.blazemeter.com/docs/guide/api-monitoring-script-engine-overview.html#built-ins).

The Script Engine is ideal for cases that require more flexibility than simple [Assertions](https://help.blazemeter.com/docs/guide/api-monitoring-validating-responses-with-assertions.html) and [Variables](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html). Scripts, assertions and variables work together seamlessly, each being evaluated at different points in the [lifecycle of a test step](https://help.blazemeter.com/docs/guide/api-monitoring-test-steps.html).

### Execution Context

- **Initial Script**: Runs once before all test steps to set up environment data
- **Pre-request Script**: Runs before each HTTP request to dynamically modify request data
- **Post-response Script**: Runs after each HTTP response to validate the response

### Built-in Variables and Functions

Every script has access to the following values:

#### Response Data

The `response` object is only available in post-response scripts.

| Variable | Description |
|----------|-------------|
| `response.body` | The response body as a string |
| `response.headers` | A dictionary of response headers. The keys of the dictionary represent the header names. The dictionary values are arrays of values for the given key |
| `response.reason` | The reason portion of the HTTP status line returned. This value cannot be modified |
| `response.response_time_ms` | The time taken to execute the request and receive the response in milliseconds. This value cannot be modified |
| `response.size_bytes` | The size of the response body in bytes. This value cannot be modified |
| `response.status` | The response's status code. This value cannot be modified |

#### Request Data

The `request` object is available in both pre-request and post-response scripts.

| Variable | Description |
|----------|-------------|
| `request.body` | The request body as a string |
| `request.form` | A dictionary of form parameters sent with the request. The keys of the dictionary represent the parameter names. The dictionary values are arrays of values for the given key |
| `request.headers` | A dictionary of the request headers. The keys of the dictionary represent the header names. The dictionary values are arrays of values for the given key |
| `request.host` | The hostname of the URL executed |
| `request.method` | The request method (GET, POST, etc.) used to execute the request |
| `request.params` | A dictionary of URL parameters (querystring) sent with the request. The keys of the dictionary represent the parameter names. The dictionary values are arrays of values for the given key |
| `request.path` | The path segment of the URL without URL parameters |
| `request.scheme` | `http` or `https` |
| `request.size_bytes` | The size of the request body in bytes. This value cannot be modified |
| `request.url` | The fully-assembled URL that was accessed for the request |

#### API Test Variables

The `variables` global is available in both pre-request and post-response scripts.

| Function | Description |
|----------|-------------|
| `variables.get(name)` | Return a value from the current variable context. See: [Getting and Setting Variables](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html) |
| `variables.set(name, value)` | Set a variable value. See: [Getting and Setting Variables](https://help.blazemeter.com/docs/guide/api-monitoring-dynamic-data-and-request-chaining.html). Setting a variable in a pre-request script does not make the value available to the currently request step as scripts are evaluated after the template variables are inserted (see: [Execution Order](https://help.blazemeter.com/docs/guide/api-monitoring-test-steps.html)) |

#### Helper Functions

| Function | Description |
|----------|-------------|
| `log(Object\|string)` | Write a string or pretty-printed version of an object to the output log viewable in test results |
| `encode_base64(value)` | Encode a string value as Base64 |
| `decode_base64(value)` | Decode a Base64-encoded string |
| `runscope_bucket` | The key of the bucket the test belongs to and was executed in |
| `get_secret(key)` | Returns the value for the secret with key name. See: [Secrets Management](https://help.blazemeter.com/docs/guide/api-monitoring-secrets-management.html) |

#### JavaScript Functions

The script interpreter also supports common JavaScript objects and functions:
- Math
- Date
- RegExp
- parseInt
- parseFloat
- decodeURI
- decodeURIComponent
- encodeURI
- encodeURIComponent
- escape
- unescape
- btoa (URL-friendly Base64 encode)
- atob (URL-friendly Base64 decode)

### Debugging Scripts

If you are receiving unexpected script errors, try the following to debug issues:
- Use the `log()` function to write out values to be viewed with the test results. `log()` will "pretty print" the values of objects so they are easily readable. Using `console.log` is not recommended
- Verify your JavaScript is valid with a tool like [JSLint](https://www.jslint.com/)
- Make sure the script is completing execution in under 3 seconds
- Verify you are using functions supported in the documented version of [included libraries](https://help.blazemeter.com/docs/guide/api-monitoring-included-libraries.html)
- Do not overwrite the `request` and `response` objects entirely. Edit only specific attributes as needed

### Technical Details and Limitations

The Script Engine is a V8-compatible (version 3.28), sandboxed JavaScript interpreter. To ensure the performance and security of your scripts and API data, some limitations have been put in place:

- **No Node.js Framework**: The Script Engine is a raw interpreter and does not include a framework like Node.js. Network (XHR or otherwise) and file system access is also prohibited. All HTTP calls must be made from request steps in your tests
- **No Module Loaders**: Each script is evaluated as a single block with everything in the global scope. Module loaders like CommonJS, require(), AMD, etc. are not supported. While some npm modules may be able to be made to work, they do not by default
- **Loading Order**: Built-in variables, functions and libraries are loaded first, followed by custom libraries. You may overwrite built-in functionality in your custom libraries and scripts, but doing so is unsupported and may cause unexpected results
- **Execution Timeout**: All scripts must complete their execution within 20 seconds

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

## Documentation References

For detailed information about API Monitoring scripting, use the BlazeMeter MCP help tools:

**API Monitoring Scripting**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**:
  - `api-monitoring-script-engine-overview` (Script Engine Overview)
  - `api-monitoring-initial-script` (Initial Script)
  - `api-monitoring-included-libraries` (Included Libraries)
  - `api-monitoring-custom-libraries` (Custom Libraries)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-script-engine-overview", "api-monitoring-initial-script", "api-monitoring-included-libraries", "api-monitoring-custom-libraries"]}`

