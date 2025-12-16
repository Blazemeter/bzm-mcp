# Bulk Operations APIs

## Service Virtualization Bulk Operations APIs

This document provides details about the new APIs that were added as part of Bulk Service Virtualization operations (Start/Stop/Delete). These APIs enable programmatic management of multiple Service Virtualization services simultaneously.

**Use when**: Using bulk operations APIs for Service Virtualization or performing bulk start, stop, and delete operations with tracking objects and status monitoring.

### Overview

Bulk Operations APIs enable programmatic management of multiple Service Virtualization services simultaneously, providing:
- **Bulk Start**: Start multiple services at once
- **Bulk Stop**: Stop multiple services at once
- **Bulk Delete**: Delete multiple services at once
- **Operation Tracking**: Track bulk operation status
- **Status Monitoring**: Monitor operation progress

### Response Format of Service Virtualization Bulk APIs

When performing a bulk action on virtual services, a tracking object will be given as a response. This tracking object can be monitored in order to know the status of the bulk action.

The **trackingID** field of the tracking object can be used with the existing tracking API to look up the current status of the bulk action:

```
GET /api/v1/trackings/{trackingId}
```

**Note**: Use the tracking API endpoint `Get tracking object by ID - GET /api/v1/trackings/{trackingId}` to monitor the status of bulk operations. The tracking object will show the status of each individual service operation within the bulk action.

For bulk actions, a tracking object of the type **MASTER_TRACKING** is used, which contains one or more child tracking objects in its **serviceMockTrackingDtos** field; each of these child tracking objects represents the status of the action for one of that virtual service that the bulk action is being performed on.

### API Endpoint

**PATCH** `https://mock.blazemeter.com/api/v1/workspaces/{workspaceId}/service-mocks`

**Swagger link**: https://mock.blazemeter.com/swagger-ui.html#/Service%20Mock/bulkMockOperationsUsingPATCH

### Required Request Body Fields

- **action** (String, required): Must be set to "START", "STOP", or "DELETE"
- **mockServiceIds** (Number[], required): List of virtual service Ids that need to be operated on
- **credentialsId** (String, optional): For START action, credentials ID
- **username** (String, optional): For START/STOP actions, base64 encoded username
- **password** (String, optional): For START/STOP actions, base64 encoded password

### Bulk Start Service Virtualization API

**Action**: Set `action` to `"START"`

**Sample Request:**
```json
{
  "action": "START",
  "mockServiceIds": [1],
  "credentialsId": "myCredentialsId",
  "username": "base64EncodedValue",
  "password": "base64EncodedValue"
}
```

**Sample cURL:**
```bash
curl --request PATCH \
  --url https://mock.blazemeter.com/api/v1/workspaces/28906/service-mocks \
  --header 'Authorization: Basic <credentials>' \
  --header 'Content-Type: application/json' \
  --data '{
    "action": "START",
    "mockServiceIds": [1],
    "credentialsId": "myCredentialsId",
    "username": "base64EncodedValue",
    "password": "base64EncodedValue"
  }'
```

### Bulk Stop Service Virtualization API

**Action**: Set `action` to `"STOP"`

**Sample Request:**
```json
{
  "action": "STOP",
  "mockServiceIds": [1],
  "username": "base64EncodedValue",
  "password": "base64EncodedValue"
}
```

**Sample cURL:**
```bash
curl --request PATCH \
  --url https://mock.blazemeter.com/api/v1/workspaces/28906/service-mocks \
  --header 'Authorization: Basic <credentials>' \
  --header 'Content-Type: application/json' \
  --data '{
    "action": "STOP",
    "mockServiceIds": [1],
    "username": "base64EncodedValue",
    "password": "base64EncodedValue"
  }'
```

### Bulk Delete Service Virtualization API

**Action**: Set `action` to `"DELETE"`

**Sample Request:**
```json
{
  "action": "DELETE",
  "mockServiceIds": [1]
}
```

**Sample cURL:**
```bash
curl --request PATCH \
  --url https://mock.blazemeter.com/api/v1/workspaces/28906/service-mocks \
  --header 'Authorization: Basic <credentials>' \
  --header 'Content-Type: application/json' \
  --data '{
    "action": "DELETE",
    "mockServiceIds": [1]
  }'
```

### Sample Response

All bulk operations return a tracking object with **MASTER_TRACKING** type:

```json
{
  "apiVersion": 1,
  "error": null,
  "result": [
    {
      "id": null,
      "code": 0,
      "message": null,
      "trackingDto": {
        "trackingId": "f03ca79a-610f-4aa9-b708-284aefef7d14",
        "status": "RUNNING",
        "errors": [],
        "warnings": [],
        "trackingUrl": "/api/v1/trackings/f03ca79a-610f-4aa9-b708-284aefef7d14",
        "data": {
          "dataType": "MASTER_TRACKING",
          "serviceMockTrackingDtos": [
            {
              "serviceMockId": 1,
              "serviceMockName": "MockService-Jan_26_08:57:32:679 PM",
              "trackingDto": {
                "trackingId": "7676187b-68f7-4508-b380-dcaa310aaf8f",
                "status": "PENDING",
                "errors": [],
                "warnings": [],
                "trackingUrl": "/api/v1/trackings/7676187b-68f7-4508-b380-dcaa310aaf8f",
                "data": {
                  "dataType": "CONFIGURATION",
                  "values": [39488]
                },
                "created": 1611698461,
                "createdBy": null,
                "updated": 1611698461,
                "updatedBy": "user@example.com",
                "ended": null
              }
            }
          ]
        },
        "created": 1611698461,
        "createdBy": null,
        "updated": 1611698461,
        "updatedBy": "user@example.com",
        "ended": null
      }
    }
  ],
  "requestId": "4035070a00714041"
}
```

### Tracking Operations

Use the **trackingId** from the response to monitor the status of the bulk operation:

```
GET /api/v1/trackings/{trackingId}
```

### Use Cases

- **Environment Management**: Manage multiple services in environments
- **Bulk Operations**: Perform operations on multiple services simultaneously
- **Automation**: Automate service management workflows
- **Resource Management**: Manage service resources efficiently

---

## Documentation References

For detailed information about Bulk Operations APIs, use the BlazeMeter MCP help tools:

**Bulk Operations APIs**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-mock-services-bulk-operations-apis`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-mock-services-bulk-operations-apis"]}`

