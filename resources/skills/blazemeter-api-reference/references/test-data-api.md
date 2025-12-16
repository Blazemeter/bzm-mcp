# Test Data API

## Test Data API

The Test Data API is used by all test types to store and generate test data. The API takes in a workspace ID and a model ID.

After you have defined a [Data Model](https://help.blazemeter.com/docs/guide/test-data-what-are-data-entities-data-parameters.html) in a workspace, you can associate it with any Functional tests, Performance tests, and virtual services in this workspace. You can use API calls to generate and supply test data during test execution.

**Use when**: Using Test Data API for generating and managing test data, integrating with Asset Repository API, data model generation, or orchestrating test data preparation.

### Overview

The test data integration uses two separate APIs:

- **The Asset Repository API**: A CRUD (create/read/update/delete) API to manage assets and asset metadata. Use the [Asset Repository API](https://ar.blazemeter.com/api-doc/v3/) to store test data, to organize assets into packages, and to manage dependencies between assets. The Asset Repository API is reachable via `https://ar.blazemeter.com/api/v3/`

- **The Test Data API**: Use the [Test Data API](https://help.blazemeter.com/apidocs/test-data/index.htm) to generate data for adhoc Data Models and for Data Models stored in the Asset Repository, to validate adhoc Data Models and Data Models in the Asset Repository, and to read or "publish" test data values as part of [orchestration](https://help.blazemeter.com/docs/guide/test-data-orchestration.html). To do that, the Test Data API references the Asset Repository API. The Test Data API also includes an introspection API to list [available seed lists and test data generator functions](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html). The Test Data Management API is reachable via `https://tdm.blazemeter.com/api/v1/`

### Data Generation

You can generate data of a Data Model that is stored in the Asset Repository, or you can pass an adhoc Data Model inside a request to the `generate` endpoint. 

- **To generate data for one entity**: Use the `generate` endpoint
- **To generate data for all entities in the data model**: Use the `/generatefile` endpoint

### API Endpoints

- **Data Entities**: Manage data entities via Asset Repository API
- **Data Parameters**: Manage data parameters
- **Data Generation**: Generate test data using Test Data API
- **Asset Repository**: Access Asset Repository API for CRUD operations
- **Orchestration**: Read or "publish" test data values as part of orchestration

### Use Cases

- **Automated Data Generation**: Generate test data automatically
- **Data Management**: Manage test data programmatically
- **Integration**: Integrate with external systems
- **Orchestration**: Orchestrate test data preparation
- **Validation**: Validate adhoc Data Models and Data Models in the Asset Repository

---

## Documentation References

For detailed information about Test Data API, use the BlazeMeter MCP help tools:

**Test Data API**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-test-data-api`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-test-data-api"]}`

