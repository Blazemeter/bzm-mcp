# API Monitoring Configuration

## Create Your First API Monitoring Test

API Monitoring helps you evaluate the performance of your API from the API consumer point of view, in addition to monitoring the uptime and correctness of your API.

An **API test** is a group of one or more HTTP requests executed sequentially. For each step in the test, you can define [Assertions](skill-blazemeter-api-monitoring://references/scripting.md) to validate response data and [Variables](skill-blazemeter-api-monitoring://references/advanced-features.md) to extract data to be used in subsequent requests. A test **Passes** if all the assertions pass. A test **Fails** if any assertion fails, or another error is encountered, such as a network connection problem.

You can run tests [from the cloud](skill-blazemeter-api-monitoring://references/configuration.md) or from [behind your firewall](skill-blazemeter-private-locations://references/radar-agent.md) against any public or private API. To use tests for ongoing monitoring, configure a [schedule](skill-blazemeter-api-monitoring://references/configuration.md). After a test run completes, [notifications](skill-blazemeter-api-monitoring://references/notifications.md) can be sent via email, Webhook, [PagerDuty](skill-blazemeter-api-monitoring://references/integrations.md), [Slack](skill-blazemeter-api-monitoring://references/integrations.md), and more.

**Use when**: Creating your first API Monitoring test, learning the basics of API Monitoring, or setting up initial test configuration.

### Create Your First Test

Follow these steps:

1. [Add a Request Step](#1-add-a-request-step)
2. [Define Assertions](#2-define-assertions)
3. [Run your Test](#3-run-your-test)

If you haven't yet, [sign up for your free BlazeMeter account](https://www.blazemeter.com/signup). After completing the tutorial, start by creating a new test (or API Tests > Create Test). You can name the test anything you like.

### 1. Add a Request Step

After you create a test, you will see an HTTP request step with a sample URL was automatically created and added to your test.

Our sample URL is guaranteed to return a **200 OK** status code. Later on, when building your own tests, you can define requests with your own methods, URLs, headers, parameters, or body content.

### 2. Define Assertions

Define expected response data.

Follow these steps:

1. Expand the request to view details.
2. Select **Assertions**.
3. Add the following assertions (we created one for the status code automatically):

The assertions are evaluated after the request is executed for every test run. If any assertion fails, the test will fail. For your tests, you can create assertions that check response time, JSON or XML content, HTTP response headers and more.

### 3. Run Your Test

Click **Save & Run** to start a new test run. The request is executed and when complete, each assertion will be checked. You should see that the test run **Passed**. Select the test run from the results list to view the full HTTP request, response and test output.

### Next Steps

- [Use variables](skill-blazemeter-api-monitoring://references/advanced-features.md) to insert dynamic data and pass state between requests.
- Learn about the available [assertion sources and comparisons](skill-blazemeter-api-monitoring://references/scripting.md).
- Manage configuration across realms with [environments](skill-blazemeter-api-monitoring://references/configuration.md).
- Run API monitoring tests from a private location. You can use [Radar agent](skill-blazemeter-private-locations://references/radar-agent.md) to bridge BlazeMeter API Monitoring to private APIs not available over the public internet. Note that Radar agent is a wholly separate installation from [Private Location agents](skill-blazemeter-private-locations://references/introduction.md), and is specific only to BlazeMeter's API monitoring function.
- [Schedule your tests](skill-blazemeter-api-monitoring://references/configuration.md) to run automatically or run them as [part of your build and deployment process](skill-blazemeter-api-monitoring://references/integrations.md).
- [Receive email, Webhook, Slack, or PagerDuty notifications](skill-blazemeter-api-monitoring://references/notifications.md) when test runs complete (or when they fail).
- [Enable multiple locations](skill-blazemeter-api-monitoring://references/configuration.md) to monitor your APIs from around the globe.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Create Your First API Monitoring Test**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-create-your-first-api-monitoring-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-create-your-first-api-monitoring-test"]}`

---

## API Monitoring Global Locations

Locations allow you to monitor your APIs from multiple sources around the globe or from an agent running within your infrastructure. When enabled for a test environment or shared environment, each test run using that environment's configured locations (scheduled or otherwise) will be initiated from all of the selected locations simultaneously.

**Use when**: Configuring global test execution locations for API Monitoring tests or when selecting specific geographic regions or Radar Agents for test execution.

### IP Addresses and Allowlisting

Due to the elastic nature of the BlazeMeter API Monitoring infrastructure, we do not publish lists of IP addresses for allowlists. Between the regions that we use and depending on the load, you could see a wide variety of source IPs at any given time.

You can get a known source IP address for requests in your tests by using the [Radar Agent](skill-blazemeter-private-locations://references/radar-agent.md) on a host you control. The agent also allows you to send test requests from within your own infrastructure. Once running the agent acts just like any of the cloud locations and can be enabled within a test or shared environment.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Global Locations**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-global-locations`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-global-locations"]}`

**IP Addresses and Allowlisting**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-ip-addresses-allowlisting`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-ip-addresses-allowlisting"]}`

### Select Test Locations

Select Location to pick which regions and agents to run your tests from when using the selected environment. You can also configure locations using shared environment locations.

Follow these steps:

1. Log in to BlazeMeter and navigate to the **API Monitoring** tab
2. Click **Tests**
3. Click a test name
4. Click **Edit Test**
5. Expand **Test Settings**
6. Click **Locations**
7. Toggle the locations on and off as needed
8. Click **Save** or **Save & Run** if you want to run the test

### Available Locations

Tests can be run from any of the BlazeMeter API Monitoring service regions:

| Location | Provider | Region Code |
|----------|----------|-------------|
| US Virginia | Google Cloud | `us1` |
| US California | Google Cloud | `us2` |
| US Illinois | Rackspace | `us3` |
| US Texas | Rackspace | `us4` |
| US Oregon | Google Cloud | `us5` |
| Ireland | Amazon Web Services | `eu1` |
| Germany (Frankfurt) | Google Cloud | `eu2` |
| Australia (Sydney) | Google Cloud | `au1` |
| Singapore | Google Cloud | `sg1` |
| Hong Kong | Google Cloud | `hk1` |
| Japan (Tokyo) | Google Cloud | `jp1` |
| Brazil (São Paulo) | Google Cloud | `br1` |
| India (Mumbai) | Google Cloud | `in1` |
| US Ohio | Amazon Web Services | `us6` |
| Canada (Montreal) | Google Cloud | `ca1` |
| London | Google Cloud | `eu3` |
| US Iowa (us-central1) | Google Cloud | `gc1` |
| Finland (europe-north1) | Google Cloud | `gcpeu3` |
| US South Carolina (us-east1) | Google Cloud | `gcpus8` |

**Note**: On a free plan, only the following locations are available: US California, Hong Kong, Japan, Brazil, India, US Iowa, Finland, and US South Carolina.

### Radar Agents

The Radar Agent lets you run your tests from agents running within your infrastructure. When an agent is connected, it will appear in the list of available locations along with the default BlazeMeter API Monitoring locations.

### Shared Environment Locations

Locations can be enabled for all environments that inherit from a Shared Environment. You can edit these by going to the API Test page and selecting **Shared Environments**.

---

## API Monitoring Test Behaviors

Each test-specific or shared environment can have separate settings for test behaviors.

**Use when**: Configuring retry logic, timeout settings, or failure handling for API Monitoring tests or when customizing test execution behavior.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Test Behaviors**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-test-behaviors`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-test-behaviors"]}`

### Retry on Failure

When enabled, an additional test run will be triggered immediately after a failed *scheduled* test run. Only **one** new test run will be initiated per failure (failed re-runs will not re-run again). When combined with notifications set to use thresholds (e.g. notify after N failures), Retry on Failure can reduce notifications for false negatives (e.g. intermittent network issues).

### Stop on Failure

When enabled, test runs will stop executing after the first step that fails. All subsequent steps will be skipped.

### Use Cookies

When enabled, cookies will automatically be passed between requests in a test run. Cookie handling behavior is similar to a web browser, so cookies will follow typical domain, path and expiration rules. Cookie state is not persisted between test runs.

### Validate SSL

Select this option to enable strict validation of SSL certificates for all HTTPS connections established when this test runs with the selected environment. If you're using a self-signed or other untrusted SSL certificate, deselect this option.

### HTTP Version Support

You can determine the HTTP versions supported when executing request steps:
- **HTTP/1 only**: Use only HTTP/1.1 protocol
- **HTTP/2 only**: Use only HTTP/2 protocol
- **HTTP/2 compatibility**: Attempt HTTP/2, fallback to HTTP/1.1 if not supported

You can view the negotiated HTTP protocol version in the Connection tab of a test result.

### Force h2c

Enable this option to force HTTP/2 over cleartext for URLs with the HTTP scheme (not HTTPS). This allows HTTP/2 connections without TLS encryption.

### Advanced Diagnostics

Enable this option to add a new **Diagnostics** tab to your Results > Response section. Can be used to diagnose network issues. See [Enable and View Advanced Diagnostics](skill-blazemeter-api-monitoring://references/configuration.md) for more information.

---

## Enable and View Advanced Diagnostics

Enable and view advanced diagnostics for API Monitoring tests to troubleshoot network issues in real-time using diagnostic tools.

**Use when**: Troubleshooting network connectivity issues in API Monitoring tests, diagnosing performance bottlenecks, or using real-time network diagnostic tools.

### Overview

The Advanced Diagnostics feature provides API Monitoring customers with real-time network troubleshooting tools directly in the response view. When enabled, a new Diagnostics tab appears in the Results section, offering tools to identify and resolve connectivity issues quickly.

Advanced Diagnostics require a qualifying plan. Check your plan or [contact Sales to get started](mailto:sales-blazemeter@perforce.com).

### How to Enable Advanced Diagnostics

**Steps:**

1. Navigate to an API Monitoring test
2. In the test **Editor**, expand the **Test Settings** drop-down
3. Select **Behaviors**
4. Enable the toggle for **Advanced Diagnostics**. The default setting is OFF

### View Advanced Diagnostics

**Steps:**

1. Navigate to an API Monitoring test
2. In **Results**, find the test run you wish to diagnose and select **View result**
3. Expand the request to analyze and select **Diagnostics**

### Understand Advanced Diagnostics

Advanced Diagnostics provides a suite of tools designed to pinpoint network problems efficiently:

- **Ping**: Sends ICMP packets to check if the target host is reachable and measures latency. Use this tool to confirm basic connectivity and highlight latency issues that may indicate congestion or distance-related delays
- **Netcat**: Tests TCP/UDP connectivity to specific ports. Use this tool to verify if required ports (for example, 443 for HTTPS) are open and detects firewall or security restrictions
- **Dig**: Performs DNS lookups to resolve domain names. Use this tool to confirm DNS resolution, identify misconfigured records, and troubleshoot DNS-related delays
- **Traceroute**: Maps the network path from source to destination, showing each hop and its latency. Use this tool to pinpoint where slowness or packet loss occurs and to diagnose routing or ISP-level issues

These tools help teams troubleshoot performance bottlenecks and connectivity failures in real time without relying on external utilities.

### Documentation References

For detailed information about advanced diagnostics, use the BlazeMeter MCP help tools:

**Enable and View Advanced Diagnostics**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-diagnostics`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-diagnostics"]}`

---

## Environment Headers and Authentication

Common headers or authentication settings can be configured in an environment and applied to all requests within a test. When specified, default headers and auth settings will be automatically included in each request step for your test. Variables can be used, but will only be evaluated at the beginning of the test run, before the first step is executed.

**Use when**: Configuring default headers and authentication for API Monitoring tests, setting up OAuth 1.0/2.0, Basic Auth, or client certificates, or applying common headers across all requests in a test.

### Default Headers

Default headers are useful for specifying header values like user agents, content types, and OAuth 2.0 bearer tokens that apply to all requests within a test. If a header is specified in an environment but also a request, the request-specific value will take precedence when the test is executed. This setting is also inherited from a parent environment if specified, but can be overridden on a per-test basis.

### Default Authentication

You can add a default authentication method to be used for each test or request step. API Monitoring supports Basic authentication, OAuth 1.0, OAuth 2.0, and authentication using your local client certificate.

To add a default authentication:

1. In **API Monitoring**, create a new test or select one of your existing tests.
2. From the menu on the left, select **Editor**.
3. Expand **Test Settings**.
4. Click **Authentication**.
5. Select your chosen method under *Authentication Methods*.

To switch to another type of authentication, select **Clear Default Authentication**.

#### Add Basic Auth

Set a user name and password credential that will be added as an Authorization header, and will be included in all requests in the test.

#### Add OAuth 1.0

To set up OAuth 1.0, provide the following information:
- **Consumer Key**: The Consumer Key used for asking the service for authorization.
- **Consumer Secret**: The Consumer Secret used for asking the service for authorization.
- **Access Token**: The token used for accessing the resource.
- **Token Secret**: The secret that accompanies the access token.
- **Signature Type**: Choose to insert the signature type in **Authorization header**, **Querystring**, or **Body**.

The required signature will be automatically generated using these credentials and included in all requests in the test.

#### Add OAuth 2.0

To set up OAuth 2.0 authentication:

1. Provide access token. If none is available, create a new token.
2. Choose to add the authorization to **Authorization header** or **Request URL**.
3. *(Optional)* Enable the **Auto-Refresh Token** toggle to automatically replace expired tokens with new ones.

The required signature will be automatically generated using these credentials and included in all requests in this test. Once generated, you can also copy the token and its attributes.

To create a new token, use the *Create new token* form:
- **Grant Type:** Choose your grant type according to your test requirement. If the Client or Application... Choose this Grant Type: Is itself the Resource Owner (User), and you need an Application-to-Application interaction Client Credentials Is a web app executing on a server Authorization Code Is a single page app (JavaScript app) Authorization code with PKCE or Implicit Is trusted with User credentials Password Credentials Is a Native or Mobile app Authorization code with PKCE

For Authorization Code, Authorization Code with PKCE, and Implicit grant types, you must add or register the API Monitoring Redirect URI, [https://www.runscope.com/oauth2/callback](https://www.runscope.com/oauth2/callback), to the third-party authorization site. See [Redirect URI Registration](https://www.oauth.com/oauth2-servers/redirect-uris/redirect-uri-registration/) for details.

- **Auth URL:** Enter the third-party authorization URL.
- **Access Token URL:** Enter the URL for generating the access token.
- **Client ID:** Enter client ID.
- **Client Secret:** Enter client secret.
- **Code Challenge Method:** (*PKCE only)* Choose between SHA-256 or Plain.
- **Code Verifier:** *(PKCE only)* Enter the code verifier string generated by the app, if available.
- **Username:** *(Password Credentials only)* Enter the user name for authorization.
- **Password:** *(Password Credentials only)* Enter the password for authorization.
- **Scope:** Add the scope string, if one is used.
- **State:** Add the state string, if one is used.
- **Client Authentication:** Send as Basic Auth header, or as client credentials in the body.
- Select **Get Access Token**.

#### Add Client Certificate

Select this option to use your local client certificates for authentication.

### Client Certificates

Custom client certificates can be stored to be used by requests within a test.

You can create:
- A PEM-encoded, password protected certificate file that you upload. See [Upload Certificate Files](skill-blazemeter-api-monitoring://references/configuration.md).
- A PEM-formatted, non password protected certificate that you paste into the text area. See [Add Certificate Contents via Text](skill-blazemeter-api-monitoring://references/configuration.md).

Client Certificate support requires a qualifying plan. [Contact sales to get started](mailto:sales-blazemeter@perforce.com).

#### Upload Certificate Files

We support password-protected encrypted client certificates with the following specifics:
- A PEM-encoded certificate file. The max file size is 1 MB.
- A PEM private key file for the certificate (optional). The max file size is 1 MB.
- A Passphrase for the certificate (optional). The max length is 128 characters.For an even higher level of security, you can use a Team Secret or a Bucket Secret for the Passphrase.

Follow these steps:

1. In **API Monitoring**, select one of your existing tests.
2. From the menu on the left, select **Editor**.
3. Expand **Test Settings**.
4. Click **Authentication**.
5. In the **Client Certificates** section, select **Upload File**.
6. Upload a certificate file. Click **Choose File**.The max file size is 1 MB.
7. (Optional) Upload a key file. Click **Choose File**.The max file size is 1 MB.If you choose to upload a key file, your certificate has to be already uploaded.
8. (Optional) Enter a passphrase. If you choose to enter a passphrase, your certificate and key have to be already uploaded.
9. Click **Upload Certificate**.

You are now able to add the certificate to requests in your test by selecting **Add Client Certificate** under the **Authentication** options of an individual request or environment.

To delete the certificate, go to **Test Settings**, **Authentication**, **Client Certificates** section and click the delete icon. The certificate, key and passphrase will be deleted. Clear authentication by clicking **Clear Default Authentication** under **Authentication Methods**, if enabled.

#### Add Certificate Contents via Text

The text needs to be a PEM-formatted certificate which has the CERTIFICATE section, and PRIVATE KEY, both are required.

Follow these steps:

1. In **API Monitoring**, select one of your existing tests.
2. From the menu on the left, select **Editor**.
3. Expand **Test Settings**.
4. Click **Authentication**.
5. In the **Client Certificates** section, select **Add Certificates Via Text**.
6. Copy and paste the contents of a certificate. Example:`-----BEGIN CERTIFICATE-----CERTIFICATETXTCOMESHERE-----END CERTIFICATE-----\n-----BEGIN PRIVATE KEY-----PRIVATEKEYCONTENTSCOMESHERE-----END PRIVATE KEY-----`
7. Click **Save**.

Once saved, you will be able to add the certificate to requests in your test by selecting **Add Client Certificate** under the **Authentication** options of an individual request or environment.

To delete the certificate, go to **Test Settings**, **Authentication**, **Client Certificates** section and delete the certificate from the text box. Clear authentication by clicking **Clear Default Authentication** under **Authentication Methods**, if enabled.

### Documentation References

For detailed information about environment headers and authentication, use the BlazeMeter MCP help tools:

**Environment Headers and Authentication**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-environment-headers-and-authentication`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-environment-headers-and-authentication"]}`

---

## API Monitoring Test Steps

API tests consist of a series of steps, most often HTTP requests. In addition to requests, you can also add additional types of steps to your tests like pauses, conditions, and subtests.

**Use when**: Creating or configuring test steps in API Monitoring tests or when adding HTTP requests, assertions, custom scripts, pauses, conditions, or subtests to tests.

### Test Step Types

- **HTTP Request Step**: Standard HTTP requests (GET, POST, PUT, DELETE, etc.)
- **Pause Step**: Introduce delays between steps (1-180 seconds)
- **Incoming Request Step**: Pause execution until a request is received at a unique URL (useful for webhooks, max wait 10 minutes)
- **Curl Step**: Create requests from curl commands (experimental)
- **Condition Step**: Conditionally run test steps based on criteria
- **Conditional Loop Step**: Repeatedly make API calls until a favorable response is received (max 100 iterations, 11-minute timeout)
- **Subtest Step**: Run other BlazeMeter API Monitoring tests as part of a test run
- **Browser Test (Ghost Inspector) Step**: Run UI tests when connected with Ghost Inspector

### Request Lifecycle

When a request step is executed, the following order applies:

1. Pre-request Scripts are executed (variable context from initial/variables and previous steps available via `variables.get()`)
2. The HTTP request is executed and a response is returned
3. Variables defined in the editor are processed on the response
4. Post-response Scripts are processed (initial and request-specific variable values from previous steps available)
5. Assertions defined in the test editor are processed on the response

**Note**: If the `response` object was modified by a Post-response Script, the modified data is *not* available to be evaluated by an Assertion.

### Working with Test Steps

- **Create a Test from Steps**: Select one or more test steps and create a new test from them (useful for splitting large imported collections)
- **Changing Execution Order**: Drag and drop steps to reorder them
- **Test Step Actions**: Skip, unskip, duplicate, and delete requests using icons or the Actions dropdown

---

## API Monitoring Test Revisions

Restoring previously saved versions of your API tests is straightforward and simple. Additionally, you can restore any of your test-specific environments to a previous configuration. Test Revision History is available to teams on qualifying BlazeMeter plans.

**Use when**: Tracking changes to API Monitoring tests, comparing versions, or restoring previous test configurations.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Test Revisions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-test-revisions`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-test-revisions"]}`

### Restore Test Revisions

To restore a test step or environment configuration:

1. Select **Revisions** from your API test's sidebar navigation
2. Choose the test steps or environment version you would like and select **Restore**. Your API test steps or your test-specific environment configuration will be restored to that version

---

## API Monitoring Scheduling Test Runs

Tests can be scheduled to run on frequencies up to every minute. One or more schedules can be configured per test with each schedule using a unique Test-specific or Shared Environment.

**Use when**: Scheduling API Monitoring tests to run on frequencies up to every minute or when configuring multiple schedules per test and pausing scheduled tests for maintenance windows.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Scheduling Test Runs**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-scheduling-test-runs`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-scheduling-test-runs"]}`

### Configuring Schedules

To set a schedule, select one of your API tests and then click **Schedule**. Every schedule requires an environment and frequency. You can create up to 10 schedules per test (maximum recommendation).

The scheduled test runs will begin immediately after saving your changes. For example, if you choose "Every 15 minutes" and save your changes, a test run will begin immediately and then the scheduled test runs will occur every 15 minutes afterwards.

Schedules only affect the scheduled tests BlazeMeter API Monitoring runs on your behalf. You may initiate as many test runs as you like (up to your plan's request limit) via Trigger URLs or manually in the dashboard.

For custom schedules (for instance, at a specific time), use your preferred scheduler (like cron) along with a Trigger URL.

### Pausing Scheduled Tests (Creating a Maintenance Window)

You can pause all scheduled test runs temporarily, without modifying or deleting their scheduling logic. This is especially useful for planned maintenance windows, infrastructure changes, or avoiding false alerts during known downtime.

To pause all scheduled tests in your bucket, navigate to **Bucket Settings** from the dashboard and scroll to **Pause Scheduled Tests**, then enable or disable the pause toggle.

To pause scheduled tests in selected shared environments only, navigate to **Shared Environments**. Under your chosen environment settings, select **Behaviors** and enable or disable the **Pause Schedules** option.

During a pause, the following behaviors apply:

- Scheduled tests will be skipped while the pause is active
- The underlying schedule is not altered. After unpausing, tests will resume as normal, starting from the next scheduled run
- No backlogged or missed tests will be rerun after unpausing
- On your Tests list, all paused tests will display a paused indicator, showing that scheduled runs are temporarily disabled. The indicator shows whether a test is paused from the bucket level or the shared environments level
- The Schedules tab will also reflect the paused state to help clarify test inactivity

### Other Automation Options

To run your BlazeMeter API tests on every commit or deploy, check out Trigger URLs and CI integrations.

---

## API Monitoring Managing Configuration with Environments

An **Environment** is a group of configuration settings (initial variables, locations, notifications, integrations, etc.) used when running a test. Every test has at least one environment, but you can create additional environments as needed. For common settings (base URLs, API keys) that you'd like to use across all tests within a bucket, use a **Shared Environment**.

Environments are great for cases when you need to re-use the same set of test steps with different configurations e.g. executing the same test against your local dev version of an API as well as the live production version.

**Use when**: Managing test configuration using environments or when working with test-specific and shared environments, inheritance, default environments, and proxy setup.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Managing Configuration with Environments**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-managing-configuration-with-environments`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-managing-configuration-with-environments"]}`

---

## API Monitoring Test Steps

API tests consist of a series of steps, most often HTTP requests. In addition to requests, you can also add additional types of steps to your tests like pauses and conditions.

**Use when**: Understanding test step types in API Monitoring, adding different step types to tests, or managing test step execution order.

### Overview

The **Editor** is where you'll define the steps (HTTP requests, pauses, etc.) and execution order that make up a test. For each request in a test, you can specify the HTTP request data, [assertions](skill-blazemeter-api-monitoring://references/scripting.md), [variables](skill-blazemeter-api-monitoring://references/advanced-features.md) and [scripts](skill-blazemeter-api-monitoring://references/scripting.md) by clicking on a request.

### Test Step Types

- **HTTP Request Step**: Standard HTTP requests (GET, POST, PUT, DELETE, etc.)
- **Pause Step**: Introduce short delays between steps (1-180 seconds)
- **Incoming Request Step**: Pause execution until a request is received at a unique URL (useful for webhooks)
- **Curl Step (Experimental)**: Create requests using curl commands
- **Condition Step**: Conditionally run select test steps based on criteria
- **Conditional Loop Step**: Repeatedly make an API call until a favorable response is received
- **Subtest Step**: Run other BlazeMeter API Monitoring tests as part of a test run
- **Browser Test (Ghost Inspector) Step**: UI test steps when connected with Ghost Inspector

### Working with Test Steps

- **Create a Test from Steps**: Create a new test directly from selected test steps
- **Changing Execution Order**: Drag and drop to reorder steps
- **Test Step Actions**: Skip, unskip, duplicate, and delete requests

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Test Steps**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-test-steps`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-test-steps"]}`

### Select and Manage Environments

There are two primary places you will interact with your environment settings: the environments switcher (top right of the test editor) and the environment settings editor (above the test steps in the test editor). The switcher determines the current environment you are working with. When you switch between environments, the values in the settings editor will be updated to reflect the currently selected environment.

The environment switcher is where you create and delete environments. Create an empty environment by selecting **Add Environment** or alternately select **Duplicate** to create a copy of an existing one.

### Test-specific Environments

**Test environments** belong to a single test. They can optionally inherit settings from a shared environment, overriding variables and other settings specific to the test. The following settings are included in an environment:

- Initial Variables
- Initial Scripts
- Locations and Agents
- Email and Webhook Notifications
- 3rd-party Notification and Analytics Services
- SSL Verification and Cookie Handling Behaviors
- Environment Headers and Authentication
- Proxy setup

### Shared Environments

Shared environments belong to a bucket and can be used by any test within the same bucket either on their own, or via a test-specific environment set to inherit its settings.

### Inheriting From Shared Environments

When a test-specific environment is set to inherit from a shared environment, the shared environment is used as a base that the test environment builds on. Depending on the setting, you may be able to override settings in inheriting test environments:

- **Initial Variables and Initial Scripts**: See Evaluation Order of Initial Variables
- **Pre-request and Post-response Scripts**: You can run pre-request and post-response scripts at the environment level, the test level, and the test step level
- **Authentication**: Authentication settings in the shared environment can be overridden by test environment settings
- **Headers**: Headers in the shared environment with the same name as those in a test environment will be overridden by those in the inheriting test environment
- **Behaviors**: Behaviors that have their default values changed in a shared environment cannot be toggled in the inheriting test-environment. Otherwise, they can be toggled On or Off
- **Locations and Agents**: Locations and agents that have been enabled in a shared environment cannot be disabled from an inheriting test environment. Additional locations and agents can be enabled for the specific test environment
- **Email Notifications**: If email notification settings are specified in a shared environment, inheriting test environments can add to the list of team members to receive notifications, but cannot override the frequency or turn off notifications to team members specified in the shared environment
- **Webhooks**: Callback URLs specified in the shared environment will be called in addition to the callback URLs specified in the inheriting test environment
- **Integrations**: Connected services enabled in the shared environment cannot be disabled in the inheriting test environment. You can enable additional integrations in the per-test environment
- **Test Data**: If you are using a CSV data file, your test data variables and data settings cannot be changed in the inheriting test environment

### Proxy Setup

Traditionally, BlazeMeter's Radar agent is required to route API tests through your internal network, especially when testing from secure environments or behind firewalls. This setup involves deploying the Radar agent on the same system that has access to your internal infrastructure, ensuring that API requests can securely reach the desired endpoints.

By setting up a proxy, you no longer need to rely solely on a Radar agent. The custom proxy setup allows you to route requests through a specified proxy server, ensuring that you can test APIs from various environments, including both HTTP and HTTPS endpoints.

Here's how to configure it:

1. Navigate to **Test Settings** for the test you wish to configure
2. In the *Proxy setup* section, toggle the switch to **ON**
3. Configure Proxy Details:
   - **Proxy Type**: Select the type of proxy requests (**HTTP** and/or **HTTPS**) that should be routed through the proxy server. By default, both HTTP and HTTPS are enabled
   - **Proxy Server**: Enter the hostname or IP address of the proxy server. Ensure to also include the port number in the adjacent field (for example, `localhost`: `9090`)
   - **Proxy Authentication (Optional)**: If the proxy server requires authentication, toggle Proxy auth to **ON**
   - **Username and Password**: Enter the user name and password required for authentication
   - **Proxy Bypass (Optional)**: In the Proxy bypass field, specify any hosts you want to bypass the proxy for, separated by commas. For example, `google.com, ibm.com` will ensure requests to these hosts won't be routed through the proxy
4. After configuring the proxy details, click **Save** to apply the changes

### Default Environment

Every test has a default environment for backwards compatibility. Some features do not support specifying an environment. In these cases, the default is used instead. The default environment can be set by going to a test and selecting **Settings** from the left navigation.

Functions that do not currently support specifying an environment and will fallback to the default are:

- Bucket-wide Trigger URLs
- Batch Trigger URLs
- Trigger URLs with an unspecified environment (missing `runscope_environment` parameter)
- 'Run All Tests' button on the test list page
- 'Run Again' button on the test result page
- AWS CodePipeline test runs

---

## Importing and Exporting Tests

You can export tests to our API Monitoring Export Format, and import request definitions from other services to create API Monitoring tests.

**Use when**: Exporting API Monitoring tests, importing tests from other services (Postman, Swagger, OpenAPI, HAR, etc.), or sharing tests between teams or accounts.

### Exporting API Tests

The API Monitoring Export Format is a JSON representation of your API Test's steps.

You can export all the tests in a bucket. Open a bucket's dashboard and click **Export Now** at the bottom of the page.

Or, you can export individual tests. Open a test and select the **Export** option on the left-hand side menu.

You can import the downloaded file into any team's bucket to create a new test with the same step information. To learn more about the structure of exported tests, visit our [API Test Detail specification](https://help.blazemeter.com/apidocs/api-monitoring/tests_test_detail.htm).

### Importing API Tests

The following import formats are supported:

- [API Monitoring Export Format](skill-blazemeter-api-monitoring://references/configuration.md)
- [SmartBear Ready! API / SoapUI](skill-blazemeter-api-monitoring://references/configuration.md)
- [Swagger 2.0 (JSON, YAML)](skill-blazemeter-api-monitoring://references/configuration.md)
- [OpenAPI Specification 3.x (JSON, YAML)](skill-blazemeter-api-monitoring://references/configuration.md)
- [AWS API Gateway](skill-blazemeter-api-monitoring://references/integrations.md)
- [Postman](skill-blazemeter-api-monitoring://references/configuration.md)
- [Fiddler & Charles Proxy (via HAR Export)](skill-blazemeter-api-monitoring://references/configuration.md)
- [HTTP Archive (HAR) 1.1 and 1.2](skill-blazemeter-api-monitoring://references/configuration.md)
- [VCR Cassettes](skill-blazemeter-api-monitoring://references/configuration.md)
- [Paw](skill-blazemeter-api-monitoring://references/configuration.md)

#### API Monitoring Export Format

You can import API Monitoring test steps that have been previously exported to our [API Monitoring Export Format](skill-blazemeter-api-monitoring://references/configuration.md). Importing and exporting API tests is useful for sharing tests between teams or accounts. Imported tests must have at least one test step, and fewer than 100 steps.

#### SmartBear Ready! API / SoapUI

From within Ready! API (under Projects), export your test suite as a Swagger 2.0 JSON file (right click on suite, Export Swagger) and use the BlazeMeter API Monitoring [Swagger importer](skill-blazemeter-api-monitoring://references/configuration.md) to create tests from the export.

#### Swagger 2.0 API Definitions (JSON, YAML)

You can import or specify a URL for a Swagger 2.0 API definition in JSON or YAML format into a BlazeMeter API Monitoring test. Each definition parses out to one test, and each Operation Object corresponds to one test request step. JSON pointers are supported, but multi-file uploads are not.

You have the option to import all the paths in the JSON or YAML into a single test, and for BlazeMeter to add an Accept request HTTP header based on the content type of the response.

Because the Swagger specification describes what types of values may appear in a request, but doesn't necessarily specify actual values, we make heavy use of placeholders in the form of variables. When you first import a test, you'll have to give values to these variables.

**Host**

The top-level Swagger `host` field is extracted and set to a variable `{{host}}`. It acts the base url for every request in a test. If no host field is present, we default `{{host}}` to `yourapihere.com` but you can change it after the import is completed.

**basePath**

If a `basePath` is present on the Swagger object, it is prepended to all request paths. For example, an API with host `yourapihere.com`, a basePath `/v2`, and a path `/resource` would get assembled to `yourapihere.com/v2/resource`.

**Parameters**

Parameters on the Swagger Object are parsed based on the type of parameter. Both parameters at the Paths Object level, and at the Operation Object level are honored, with any Operation-level parameter overwriting a Paths-level parameter of the same name. For all parameters, we make use of the `name` and `in` fields. Form parameters use additional information from their Operation Object's `consumes` field.

- **Query Parameters** For each query parameter object, we extract the `name` field and use it as a query parameter field name. The value of the query parameter is set to an uninitialized variable of the same name. For instance, a query parameter named "id" would get appended onto a query string: as `?id={{id}}`. It is up to you to set the value of the variable to a real ID to use in a request step.
- **Header Parameters** Header parameters are parsed out of the header parameter object in the same way as query parameters; however, the value of the `name` field, and corresponding uninitialized variable are set as the header name and value in a test request step.
- **Path Parameters** Path parameters are replaced by uninitialized variables. A Swagger path with a parameter like `/user/{id}` is imported as `/user/{{id}}`.
- **Form Parameters** Form Parameters are parsed same way as Query parameters, with the exception that if `multipart/form-data` is the only content-type listed in the Operation Object's `consume` field, we skip parsing the form parameters.
- **Body Parameters** When a body parameter is present, an uninitialized variable set to the parameter object's `name` appears as the raw body. We do not currently support parsing of a body's Schema object.

**Security Requirement Object**

If a Security Requirement Object is present on an Operation Object, we first determine if there's an entry of type `APIAuth`. If there is, we parse the corresponding object the same way we would a query parameter object, if the `in` field is "query," or a header parameter object, if the `in` field is "header." If there is no APIAuth type object, and there's an object of type "basic," we set basic auth in the test request step as follows: username gets a value of `{{username}}`, and password gets the value `{{password}}`.

#### OpenAPI Specification 3.x (JSON, YAML)

You can import or specify a URL for an OpenAPI Specification 3.x in JSON or YAML format into a BlazeMeter API Monitoring test.

The following options are available:
- You can import all the paths in your Swagger file into a single test. If unchecked, an file with multiple paths will be imported as multiple tests.
- You can let BlazeMeter add an Accept request HTTP header based on the content type of the response

#### Postman

**Postman Dump Files**

We currently allow imports of Postman dump files which, in their data, include all collections, globals, environments, variables, and header presets. However, globals and scripts are not supported and will be ignored. [Learn more about Postman data formats](https://learning.postman.com/collection-format/getting-started/overview/).

Each collection will be turned into an API test in each test.

**Postman Collections**

We support imports of Postman collections v1 and v2.1, either individually or in bulk from a zip file.

Importing an individual collection will create a single test.

#### HTTP Archive Files (HAR)

Currently, the only HAR field we support is `entries`, which represent HTTP requests. `Pages`, `comment`, `browser`, `creator` are ignored.

You can generate a HAR file from Fiddler and Charles Proxy from their Export menus.

#### VCR Cassettes

VCR versions 1 and 2 are supported, and we accept import formats in YAML or JSON. Currently not supported are the `body-encoding` field, and the `http version` fields on the response object.

#### Paw

Install the [BlazeMeter API Monitoring API Test generator extension](https://paw.cloud/extensions/RunscopeTestGenerator) in Paw and upload the generated file using the API Monitoring Export Format.

### Documentation References

For detailed information about importing and exporting tests, use the BlazeMeter MCP help tools:

**Importing and Exporting Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-importing-exporting-tests`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-importing-exporting-tests"]}`


