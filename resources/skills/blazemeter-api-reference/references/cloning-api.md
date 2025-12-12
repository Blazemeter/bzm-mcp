# Cloning API

## Cloning API

The Cloning API is used to clone all the transactions within a service to another new service. The API takes in a service ID and a new service name which needs to be unique and an optional list of find and replace entries that search text in DSLs and replace it with values specified. The response of this API is a tracking object with a UUID and a user can poll the tracking API to check if the cloning has completed based on the status field and also has the new service ID which denotes the cloned service.

**Use when**: Using the Cloning API to clone all transactions within a service to a new service, using find and replace functionality, or tracking clone operations.

### Overview

The Cloning API enables programmatic cloning of Service Virtualization services, allowing:
- **Service Cloning**: Clone entire services with all transactions
- **Find and Replace**: Replace text during cloning (optional)
- **Operation Tracking**: Track clone operations via tracking object
- **Automation**: Automate service cloning

### API Endpoint

**POST** `https://mock.blazemeter.com/api/v1/workspaces/{workspaceId}/services/clone`

**Note**: The sample code uses a workspaceId of 123456. Use the actual ID value of your workspace.

### Request Body

- **serviceId** (required): The ID of the service to clone
- **newServiceName** (required): A unique name for the new cloned service
- **findAndReplace** (optional): A list of find and replace entries that search text in DSLs and replace it with values specified

### Sample Request

```json
{
  "serviceId": 19,
  "newServiceName": "serviceA Cloned at Jul_23_3:34:05 PM",
  "findAndReplace": [{"find": "v1", "replace": "v2"}]
}
```

### Sample cURL

```bash
curl 'https://mock.blazemeter.com/api/v1/workspaces/123456/services/clone' \
  -X POST \
  -H 'accept: */*' \
  -H 'authorization: Basic Aa1Bb2Cc3Dd4Ee5Ff6Gg7Hh8Ii9Jj0Aa1Bb2Cc3Dd4Ee5Ff6' \
  -H 'Content-Type: application/json' \
  -d '{
    "serviceId": 1,
    "newServiceName": "My unique new service",
    "findAndReplace": [{"find": "v1", "replace": "v2"}]
  }'
```

### Response

The response is a tracking object with a UUID. You can poll the tracking API to check if the cloning has completed based on the status field. The response also includes the new service ID which denotes the cloned service.

**Note**: The cloning operation is asynchronous. Use the tracking API to monitor the clone operation status. The `newServiceId` field in the response indicates the ID of the newly created cloned service once the operation completes.

**Sample Response:**
```json
{
  "apiVersion": 1,
  "error": null,
  "result": {
    "trackingId": "ea8ce5ab-39c9-406f-984f-cad5328db9ec",
    "status": "PENDING",
    "errors": [],
    "warnings": [],
    "trackingUrl": "/api/v1/trackings/ea8ce5ab-39c9-406f-984f-cad5328db9ec",
    "data": {
      "dataType": "CLONE_SERVICE",
      "value": {
        "serviceId": 19,
        "newServiceName": "serviceA Cloned at Jul_23_3:34:05 PM",
        "newServiceId": 26,
        "findAndReplace": [{"find": "v1", "replace": "v2"}]
      }
    },
    "created": 1627072979,
    "createdBy": null,
    "updated": 1627072979,
    "updatedBy": "j.smith@example.com",
    "ended": null
  },
  "requestId": "e91bddfc4a99e7ac"
}
```

### Use Cases

- **Service Duplication**: Duplicate services for different environments
- **Environment Setup**: Set up test environments
- **Automation**: Automate service cloning workflows
- **Find and Replace**: Update service configurations during cloning

---

## Documentation References

For detailed information about Cloning API, use the BlazeMeter MCP help tools:

**Cloning API**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-cloning-api`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-cloning-api"]}`

