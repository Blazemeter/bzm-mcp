# Export API

## Export API

The Export API is used to export all the transactions within a service to a JSON file. The API takes in a service ID and other query parameters (limit value -1, type GENERIC_DSL and exportAsFile value true). The response of this API is a JSON file with transactions array.

**Use when**: Using the Export API to export all transactions within a service to JSON files, configuring query parameters, or understanding response formats.

### Overview

The Export API enables programmatic export of Service Virtualization services, allowing:
- **Service Export**: Export services with all transactions
- **JSON Format**: Export to JSON format
- **Query Parameters**: Configure export parameters
- **Response Formats**: Understand response formats

### API Endpoint

**GET** `https://mock.blazemeter.com/api/v1/workspaces/{workspaceId}/transactions`

**Note**: The sample code uses a workspaceId of 123456. Use the actual ID value of your workspace.

### Query Parameters

- **serviceId** (required): The ID of the service to export
- **limit** (required): Set to `-1` to export all transactions
- **type** (required): Set to `GENERIC_DSL`
- **exportAsFile** (required): Set to `true`
- **sort** (optional): Sort order (e.g., `-id` for descending by ID)

### Sample Request

```
GET https://mock.blazemeter.com/api/v1/workspaces/123456/transactions?serviceId=156&sort=-id&limit=-1&type=GENERIC_DSL&exportAsFile=true
```

### Sample cURL

```bash
curl "https://mock.blazemeter.com/api/v1/workspaces/27206/transactions?serviceId=156&limit=-1&type=GENERIC_DSL&exportAsFile=true" \
  -X GET \
  -H 'Authorization: Basic Aa1Bb2Cc3Dd4Ee5Ff6Gg7Hh8Ii9Jj0Aa1Bb2Cc3Dd4Ee5Ff6' \
  -H 'Content-Type: application/json'
```

### Response

The response is a JSON file with a transactions array containing all transactions from the service.

**Note**: The export includes all transaction details including DSL (Domain-Specific Language) definitions for both request and response configurations, making it suitable for backup, migration, or version control purposes.

**Sample Response Structure:**
```json
{
  "transactions": [
    {
      "id": 93461,
      "name": "Transaction-Aug_11",
      "serviceId": 156,
      "serviceName": "Default Service",
      "description": "",
      "priority": null,
      "dsl": {
        "priority": 1,
        "requestDsl": {
          "method": "GET",
          "host": "http://petstore.swagger.io",
          "path": "/api/pets",
          "url": {...},
          "headers": [...],
          "queryParams": [],
          "cookies": [],
          "credentials": {...},
          "body": []
        },
        "responseDsl": {
          "binary": false,
          "status": 200,
          "statusMessage": "OK",
          "headers": [],
          "contentType": "text",
          "content": "",
          "charset": "UTF-8"
        }
      },
      "sampleBody": null,
      "tags": [],
      "created": 1629225867,
      "updated": 1629225867,
      "createdBy": "user@example.com",
      "updatedBy": "user@example.com",
      "createdDate": "August 17, 2021",
      "updatedDate": "August 17, 2021"
    }
  ]
}
```

### Use Cases

- **Service Backup**: Backup services programmatically
- **Migration**: Migrate services between workspaces
- **Version Control**: Version control service configurations
- **Automation**: Automate service export workflows

---

## Documentation References

For detailed information about Export API, use the BlazeMeter MCP help tools:

**Export API**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-export-api`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-export-api"]}`

