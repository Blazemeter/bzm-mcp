# API Functional Tests (Deprecated)

> **⚠️ IMPORTANT: This feature is deprecated. Use API Monitoring instead.**

## Create

Create API Functional Tests in BlazeMeter UI, including adding requests, modifying requests, query parameters, headers, body, assertions, extracting from responses, scenarios, and common functions.

**Use when**: Creating API Functional Tests in BlazeMeter UI (note: this feature is deprecated in favor of API Monitoring) or adding requests, modifying requests, query parameters, headers, body, assertions, and extracting from responses.

### Deprecation Notice

API Functional Tests are deprecated. Starting February 2022, the API Functional testing feature has been deprecated. Depending on your subscription plan, you may still be able to run existing tests but can no longer create new ones. **Please use BlazeMeter API Monitoring to create and run your API Functional Tests going forward.** See the `blazemeter-api-monitoring` skill for current API testing capabilities.

### Legacy Features (Deprecated)

- **Add Requests**: Add HTTP requests to tests
- **Modify Requests**: Edit request configurations
- **Query Parameters**: Configure query parameters
- **Headers**: Set request headers
- **Body**: Configure request body
- **Assertions**: Add response assertions
- **Extract from Responses**: Extract data from responses
- **Scenarios**: Organize requests into scenarios
- **Common Functions**: Use common test functions

---

## Report

Review API Functional Test reports, including report summary, request data, response data, report history, and sharing reports with pass/fail status and assertion results.

**Use when**: Reviewing API Functional Test reports (note: this feature is deprecated in favor of API Monitoring) or viewing report summary, request data, response data, report history, and sharing reports with pass/fail status and assertion results.

### Deprecation Notice

API Functional Test reports are deprecated. Use **API Monitoring** reports instead. See the `blazemeter-api-monitoring` skill for current reporting capabilities.

### Legacy Report Features (Deprecated)

- **Report Summary**: View test summary
- **Request Data**: Review request details
- **Response Data**: View response information
- **Report History**: Access historical reports
- **Sharing**: Share reports with team
- **Pass/Fail Status**: View test status
- **Assertion Results**: Review assertion outcomes

---

## Scripting in UI

Script API Functional Tests directly in the BlazeMeter UI using Taurus YAML format (deprecated, use API Monitoring instead).

**Use when**: Scripting API Functional Tests directly in the BlazeMeter UI (note: this feature is deprecated, use API Monitoring instead).

### Deprecation Notice

API Functional Test scripting in UI is deprecated. Use **API Monitoring** scripting instead. See the `blazemeter-api-monitoring` skill for current scripting capabilities.

---

## Create from Existing Script

Create API Functional Tests by uploading existing scripts (deprecated, use API Monitoring instead).

**Use when**: Migrating existing API test scripts to BlazeMeter (note: this feature is deprecated, use API Monitoring instead).

### Deprecation Notice

Creating API Functional Tests from existing scripts is deprecated. Use **API Monitoring** instead. See the `blazemeter-api-monitoring` skill for current script import capabilities.

### Migration Path

1. **Use API Monitoring**: Migrate to API Monitoring
2. **Import Scripts**: Import scripts into API Monitoring
3. **Configure Tests**: Set up API Monitoring tests
4. **Execute Tests**: Run tests in API Monitoring

**Note**: API Monitoring provides all the capabilities of API Functional Tests with enhanced features, better reporting, and active support. The migration path is straightforward, and existing test scripts can be adapted for API Monitoring.

---

## Documentation References

For detailed information about API Monitoring (the replacement for deprecated API Functional Tests), use the BlazeMeter MCP help tools:

**API Monitoring** (Recommended):
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-api-test-create` (create), `functional-api-test-report` (report), `functional-api-test-scripting-in-ui` (scripting), `functional-api-test-create-from-existing-script` (create from script). Note: API Functional Tests are deprecated; use API Monitoring instead.
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-api-test-create", "functional-api-test-report", "functional-api-test-scripting-in-ui", "functional-api-test-create-from-existing-script"]}`

**Note**: For API Functional Tests (deprecated), refer to legacy documentation, but strongly consider migrating to API Monitoring.

