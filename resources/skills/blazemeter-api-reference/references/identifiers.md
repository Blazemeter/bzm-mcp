# Identifiers

## Get Your Workspace ID

In BlazeMeter, you can obtain your Workspace ID into a document for later use. This ID (`workspacesId`) will be used as a parameter in the API to identify a specific workspace of your test(s) and reports(s) in BlazeMeter, or as a parameter in other features (Private Location, Dedicated IPs, integrations, and more).

**Use when**: Obtaining Workspace ID for API calls or configuring features that require workspace identification.

### Methods to Get Workspace ID

You can find your 'Workspace ID' in the following ways:

- **In the URL line of your BlazeMeter Dashboard or Report**: The workspace ID appears in the URL
- **In the Settings page, at the 'Workspaces' section**: Available to Admin Users

**Usage**: This ID (`workspacesId`) will be used as a parameter in the API to identify a specific workspace of your test(s) and reports(s) in BlazeMeter, or as a parameter in other features (Private Location, Dedicated IPs, integrations, and more).

### Usage

- **API Calls**: Use in API endpoint URLs
- **Feature Configuration**: Configure workspace-specific features (Private Location, Dedicated IPs, integrations)
- **Resource Identification**: Identify workspace resources

---

## Get the Project ID

For some API requests, you will need the Project ID for the project you want to place your test in.

**Use when**: Obtaining Project ID for API calls or identifying projects in API requests.

### Methods to Get Project ID

You can find this ID in the URL line of your BlazeMeter Dashboard or Report.

### Usage

- **API Calls**: Use in API endpoint URLs
- **Project Identification**: Identify specific projects
- **Resource Management**: Manage project resources

---

## Get the Test or Collection ID

After a test has been created, make note of the test ID for later use. This ID will be used as a parameter in the API to identify a test.

Multi-tests are identified using a Collection ID.

**Use when**: Obtaining Test ID or Collection ID for API calls or identifying tests or multi-tests in API requests.

### Methods to Get Test/Collection ID

- **Test Interface**: Find in test interface
- **Test URL**: Extract from test URL
- **API Response**: Get from API responses

**Note**: After a test has been created, make note of the test ID for later use. This ID will be used as a parameter in the API to identify a test. Multi-tests are identified using a Collection ID.

### Usage

- **API Calls**: Use in API endpoint URLs
- **Test Identification**: Identify specific tests
- **Collection Management**: Manage test collections (multi-tests)

---

## Get the Scenario ID

Retrieve Scenario ID from test reports using Masters API, including scenario mapping and identification.

**Use when**: Retrieving Scenario ID from test reports or using Masters API for scenario mapping and identification.

### Methods to Get Scenario ID

- **Test Reports**: Extract from test reports
- **Masters API**: Use Masters API to retrieve
- **Scenario Mapping**: Map scenarios to IDs

### Usage

- **API Calls**: Use in scenario-specific API calls
- **Scenario Identification**: Identify specific scenarios
- **Report Analysis**: Analyze scenario-specific results

---

## Get the Master ID

Obtain Master ID from test reports (URL or API response) for identifying specific test execution masters.

**Use when**: Obtaining Master ID from test reports or identifying specific test execution masters in API calls.

### Methods to Get Master ID

- **Test Report URL**: Extract from report URL
- **API Response**: Get from API responses
- **Report Interface**: Find in report interface

### Usage

- **API Calls**: Use in execution-specific API calls
- **Execution Identification**: Identify specific test executions
- **Report Access**: Access execution reports

---

## Get the Session ID

Obtain Session ID from test reports for identifying specific test execution sessions and engines.

**Use when**: Obtaining Session ID from test reports or identifying specific test execution sessions and engines.

### Methods to Get Session ID

- **Test Reports**: Extract from test reports
- **API Response**: Get from API responses
- **Engine Identification**: Identify specific engines

### Usage

- **API Calls**: Use in session-specific API calls
- **Session Identification**: Identify specific sessions
- **Engine Tracking**: Track individual engine sessions

---

## Get the Location Name

Get location names for API calls and Taurus YAML configurations, including AWS, Google Cloud, Azure, and Private Location formats.

**Use when**: Getting location names for API calls or configuring Taurus YAML files with location names.

### Location Formats

- **AWS**: AWS location format
- **Google Cloud**: GCE location format
- **Azure**: Azure location format
- **Private Locations**: Private location format

### Usage

- **API Calls**: Use in location-specific API calls
- **Taurus YAML**: Configure in Taurus YAML files
- **Location Selection**: Select test execution locations

---

## Documentation References

For detailed information about obtaining identifiers, use the BlazeMeter MCP help tools:

**Identifiers**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-get-your-workspace-id` (Workspace ID), `api-get-the-project-id` (Project ID), `api-get-the-test-or-collection-id` (Test/Collection ID), `api-get-the-scenario-id` (Scenario ID), `api-get-the-master-id` (Master ID), `api-get-the-session-id` (Session ID), `api-get-the-location-name` (Location Name)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-get-your-workspace-id", "api-get-the-project-id", "api-get-the-test-or-collection-id", "api-get-the-scenario-id", "api-get-the-master-id", "api-get-the-session-id", "api-get-the-location-name"]}`

