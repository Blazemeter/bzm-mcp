# API Overview

## BlazeMeter REST APIs

BlazeMeter is a 100% JMeter-compatible, self-service web testing cloud. Performance tests and Functional tests are easily created and configured online. Once these tests are created, it is possible to run them using the BlazeMeter REST API. This means that instead of manually starting the tests, users simply create an automated script that will automatically run a predefined test via the API.

BlazeMeter has a new, improved API for performing the same actions programmatically as you can with our UI. The API is RESTful and works with JSON messages over HTTP. It relies on the standard HTTP verbs including GET, POST, PUT, DELETE, and PATCH.

**Use when**: Automating test execution with BlazeMeter REST APIs, getting test IDs, API keys, making common API calls, or integrating BlazeMeter with external systems.

### Overview

BlazeMeter provides comprehensive REST APIs for:
- **Test Execution**: Automate test execution
- **Resource Management**: Manage tests, projects, workspaces
- **Results Access**: Access test results and reports
- **Integration**: Integrate with external systems

### Common API Calls

- **Get Test IDs**: After the test has been created, copy and paste the test ID from the URL (e.g., `https://a.blazemeter.com/app/#/accounts/123456/workspaces/56789/projects/1212121/tests/59087221`). This ID will be used as a parameter in the API to identify the test
- **Get API Keys**: Obtain API keys for authentication. To learn about API keys, see [BlazeMeter API keys](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html)
- **Execute Tests**: Start and manage test executions
- **Retrieve Results**: Get test results and reports

### API Documentation

For detailed documentation of various useful APIs and Swagger doc, see **help.blazemeter.com/apidocs/**.

---

### API Endpoints

BlazeMeter provides different API endpoints for different services:

- **Performance and Functional testing**: All API URLs are relative to `https://a.blazemeter.com/api/v4/`. For example, the tests/start API call is reachable at `https://a.blazemeter.com/api/v4/tests/start`
- **Service Virtualization API**: Endpoints for Service Virtualization are reachable at **https://mock.blazemeter.com**
- **API Monitoring API**: Endpoints are reachable at **https://api.runscope.com**. This API is currently unversioned, but some features are only available by appending v1 in the URL. For instance, the bucket details API is reachable via `https://api.runscope.com/v1/buckets/<bucket_key>`
- **Test Data API**: Relies on the **Asset Repository API** and both are available for all test types. The Asset Repository API is reachable via `https://ar.blazemeter.com/api/v3/`, and the Test Data Management API is reachable via `https://tdm.blazemeter.com/api/v1/`

### Passing Request Data

Request data is passed to the API by POSTing JSON objects to the API endpoints with the appropriate parameters. The documentation for each API call will contain more detail on the parameters accepted by the call.

### API Documentation

For detailed documentation of various useful APIs and Swagger doc, see **help.blazemeter.com/apidocs/**.

### Available Endpoints

- **Performance**: Performance test endpoints (`https://a.blazemeter.com/api/v4/`)
- **Functional**: Functional test endpoints (`https://a.blazemeter.com/api/v4/`)
- **Service Virtualization**: Service Virtualization endpoints (`https://mock.blazemeter.com`)
- **API Monitoring**: API Monitoring endpoints (`https://api.runscope.com`)
- **Test Data Management**: Test Data API endpoints (`https://tdm.blazemeter.com/api/v1/`)
- **Asset Repository**: Asset Repository API endpoints (`https://ar.blazemeter.com/api/v3/`)

---

## Documentation References

For detailed information about BlazeMeter REST APIs, use the BlazeMeter MCP help tools:

**BlazeMeter API Overview**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-blazemeter-api-overview`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-blazemeter-api-overview"]}`

**BlazeMeter REST APIs**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-blazemeter-rest-apis`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-blazemeter-rest-apis"]}`

