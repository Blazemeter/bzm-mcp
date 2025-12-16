# Glossary

Reference glossary for BlazeMeter terminology, including definitions of key concepts like dynamic responses, parameters, and helpers.

**Use when**: Referencing BlazeMeter terminology or understanding definitions of key concepts like dynamic responses, parameters, and helpers.

### Dynamic Response

A referenced value in a transaction request that is not constant and that changes with time. A dynamic response is used in dynamic testing to validate that the referenced value is repeated appropriately in the response body.

There are two key components in a dynamic response:

- **Parameters** that control which data is returned, often based on request values
- **Helpers** that control the format of the returned data

**Note**: Dynamic responses are particularly useful in Service Virtualization scenarios where you need to simulate realistic responses that change based on request parameters or other conditions.

### Common Terminology

- **Test**: A performance or functional test configuration
- **Scenario**: A test scenario within a test
- **Execution**: A test run or execution instance
- **Workspace**: Organizational unit in BlazeMeter
- **Project**: Container for tests within a workspace
- **Location**: Geographic location for test execution
- **Virtual User (VU)**: Simulated user in performance tests
- **Response Time**: Time taken for a request to complete
- **Throughput**: Number of requests processed per unit of time

### Service Virtualization Terms

- **Transaction**: A request-response pair in Service Virtualization
- **Virtual Service**: A simulated service endpoint
- **Template**: Reusable service configuration
- **Dynamic Response**: Response that changes based on conditions

### API Monitoring Terms

- **Test Step**: Individual step in an API Monitoring test
- **Assertion**: Validation rule for test steps
- **Bucket**: Container for API Monitoring tests
- **Team**: Organizational unit for API Monitoring

---

## Documentation References

For detailed information about BlazeMeter terminology, use the BlazeMeter MCP help tools:

**Glossary**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `getting-started-glossary`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["getting-started-glossary"]}`

