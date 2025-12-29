# Service Management

## Rename/Move

Rename and move virtual services, including display name editing and location changes between private locations.

**Use when**: Renaming and moving virtual services or editing display names and changing locations between private locations.

### Rename a virtual service

To rename a virtual service, stop it if it is running. Now you can edit the display name field.

### Move a virtual service

You can change the location of a virtual service from one private location to another. To move a virtual service, stop it if it is running. Now you can select a new location from the drop-down.

Moving deploys the virtual service on the new private location. The existing container, its logs, etc. are removed from the old location.

---

## Clone Service with all Transactions

Clone services with all transactions to new services, including find and replace text functionality and creating virtual services after cloning.

**Use when**: Cloning services with all transactions to new services or using find and replace text functionality and creating virtual services after cloning.

### Clone All Transactions in a Service

Follow these steps:

1. Navigate to the **Service Virtualization** tab, **Virtual Services**, and expand the **Service** drop-down list
2. Hover over the service entries to see the pop-up action icons next to each entry
3. Click the **Clone Service** icon for the service that you want to clone. A new **Clone Service** window opens
4. Enter a service name. Use a unique service name for each clone. If the service name already exists, the **Clone** button is disabled. For APIs, a clone with a duplicate service name returns an HTTP 400 Bad Request error message. To learn more, see [Cloning API](https://help.blazemeter.com/docs/guide/api-cloning-api.html)
5. Click **Clone**

**Note**: Services are logical groupings for Transactions and virtual services. You can clone Transactions that are under a specific service to a new service. After you clone a transaction, a virtual service is created under the new service.

### Find and Replace Text in Transactions while Cloning

Use this option if you want to modify parts of transactions while cloning. For example, you might need to change an API version from v1 to v2 for all transactions. You can make this change in bulk while cloning, instead of manually.

Follow these steps:

1. Navigate to the **Service Virtualization** tab, **Virtual Services** and expand the **Service** drop-down list
2. Hover over the service entries to see the pop-up action icons next to each entry
3. Click the Clone icon for the service that you want to clone. A new **Clone Service** window opens
4. Enter a service name. Use a unique service name for each clone
5. Enable the **Find and Replace Text in Transactions** button
6. Enter a text to **Find** and a text to **Replace** it with, and a **Location**. You can find and replace in the following entities: Query Parameters, Cookies, Request Headers, Request Body, Response Headers, Response Body, Proxy URL, Path, Everywhere
7. (Optional) Click the Plus button to search and replace more strings
8. (Optional) Click the Delete button to remove a line
9. Click **Clone**

### Create a Virtual Service after Cloning

Use this option if you wish to have a virtual service created with all the transactions that have been cloned.

Follow these steps:

1. Navigate to the **Service Virtualization** tab and expand the **Service** drop-down list
2. Hover over the service entries to see the pop-up action icons next to each entry
3. Click the Clone icon for the service that you want to clone. A new **Clone Service** window opens
4. Enter a service name. Use a unique service name for each clone
5. Enable the **Create Virtual Service for Cloned Service** button
6. Click **Clone**. You will be redirected to the Virtual Service page. A virtual service is created under the new service and contains all the transactions that have been cloned
7. Verify the created virtual service and click **Run** to deploy the cloned virtual service

---

## Export and Import Services with all Transactions

Services are logical groupings for Transactions and virtual services, usually named after a specific live service. Anytime you upload Transactions or create a new virtual service, you are prompted to assign it to a Service, to create a new Service, or assign a default.

As a workspace manager or an administrator, you can export all transactions under a specific Service as a zipped JSON file. You can then import all Transactions from the zipped JSON file into another workspace.

**Example use cases:**
- You have Workspace A and Workspace B in your environment. There are transactions in the Asset catalog as a part of an existing service in Workspace A. You want the same transactions in Workspace B as well. You can export the zipped JSON file with transactions from Workspace A and upload the JSON file to Workspace B. If any of the transaction already exist in Workspace B, we append a time stamp to the imported transaction name so you can distinguish them.
- To prevent accidentally losing your Services, you want to periodically make backups. Export the Services as zipped JSON files and the Service Data as CSV files, to be able to import them back later. This enables you to restore any Services, including transactions, processing actions, test data, and associations.

**Use when**: Exporting and importing services with all transactions as ZIP files or exporting from one workspace and importing to another, and backing up services.

**This article covers the following topics:**
- [Export All Transactions in a Service as ZIP File](skill-blazemeter-service-virtualization://references/management.md)
- [Import Transactions from the Exported ZIP File](skill-blazemeter-service-virtualization://references/management.md)

### Export All Transactions in a Service as ZIP file

You can export transactions from a specific service to a zipped JSON file. If any Service Data is associated with that Service, it is included in the ZIP file as CSV files.

Follow these steps:

1. Navigate to the **Service Virtualization** tab, go to the **Asset Catalog**, and expand the **Service** drop-down list.
2. Hover over the service entries to see the pop-up action icons next to each entry.
3. Click the **Export a Service to a File** action icon for the service that you want to export.

A zipped ZIP file is downloaded and named after the service name. The ZIP file contains the transaction data in JSON format and Service Data in CSV format.

**Example:** For a service named **Default Service**, the JSON file name is **Default Service.json**.

### Import Transactions from the Exported ZIP File

There are two ways to import transactions:

- To import all the Transactions that are in the exported ZIP file, click the **Asset Catalog**tab and drag and drop the ZIP file into the upload area.
- Click the **Service Virtualization** tab, **+**, **Create from Transactions** and drag and drop the file in the upload area.

To learn more about Export API, see [Export API](skill-blazemeter-api-reference://references/api-overview.md).

**Example use cases:**
- You have Workspace A and Workspace B in your environment. There are transactions in the Asset catalog as a part of an existing service in Workspace A. You want the same transactions in Workspace B as well. You can export the zipped JSON file with transactions from Workspace A and upload the JSON file to Workspace B
- To prevent accidentally losing your Services, you want to periodically make backups. Export the Services as zipped JSON files and the Service Data as CSV files, to be able to import them back later

**Note**: To learn more about Export API, see [Export API](https://help.blazemeter.com/docs/guide/api-export-api.html).

---

## Rename or Delete a Service

Rename or delete services as workspace manager or administrator, including restoring deleted transactions and showing service IDs.

**Use when**: Renaming or deleting services as workspace manager or administrator or restoring deleted transactions and showing service IDs.

### Rename a Service

Follow these steps:

1. Navigate to **Virtual Services** and expand the **Service** drop-down list
2. Hover over the service entries to see the pop-up action icons next to each entry
3. Click the **Rename Service** icon for the service that you want to rename. A new **Rename Service** window opens
4. Enter the new service name and click **Save**

### Delete a Service

Follow these steps:

1. Navigate to **Virtual Services** and expand the **Service** drop-down list
2. Hover over the service entries to see the pop-up action icons next to each entry
3. Click the **Delete Service** icon for the service that you want to delete. A new **Delete Service** window opens notifying you that you cannot undo this action. Any virtual services, Virtual Service Templates, or Transactions associated with this Service will be deleted
4. Click **Delete**

### Restore Deleted Transactions

Workspace Admins can recover deleted transactions within 30 days of deletion, whether intentional or accidental. After 30 days, the transactions will be permanently deleted and unrecoverable.

1. Navigate to the **Asset Catalog** and expand the **Transactions** tab
2. To the right hand side of the **Services** menu, click the **Restore Transactions** button. The **Restore Transactions** window opens showing all transactions deleted in the last 30 days
3. (Optional) Select a Service to filter
4. Enable the checkboxes for the transactions that you want to restore
5. Click **Restore**

### Show Service ID

Service ID is the ID associated with the service name. Service ID is used in the endpoints that are generated after you deploy your virtual service. When you know your service ID, you can predict the format of your virtual service endpoint:

```
http(s)://(mock-name[40])(serviceid[9])-<port>-<namespace>.<sub-domain>
```

To view the Service ID, expand to the **Service** drop-down list and click the **Show Service ID** icon. You can copy the Service ID to clipboard.

---

## Test Data

Use test data with Service Virtualization, including service data entities, parameterization of request matchers and responses, data settings, and integration with tests.

**Use when**: Using test data with Service Virtualization or parameterizing request matchers and responses with service data entities and data settings.

### Service Data Entities

- **Create Entities**: Create data entities for services
- **Parameterize**: Use entities to parameterize transactions
- **Data Settings**: Configure data settings for services

### Parameterization

- **Request Matchers**: Parameterize request matching rules
- **Responses**: Use data entities in response generation
- **Dynamic Content**: Generate dynamic responses from data

### Integration with Tests

- **Test Integration**: Use virtual services in tests
- **Data Sharing**: Share data between tests and services
- **Consistent Data**: Maintain consistent test data

---

## Upgrade Outdated

Upgrade outdated virtual services to latest versions, including automatic upgrades for cloud locations and manual upgrades for private locations.

**Use when**: Upgrading outdated virtual services to latest versions or managing virtual service versions across cloud and private locations.

### Upgrade an Outdated Virtual Service

New features, capabilities and improvements are added to virtual services on a regular basis. To help you recognize if your virtual services are running on the latest image, you can now see warning messages for outdated virtual services.

If your virtual services run on a provisioned cloud location, the upgrade is done automatically. If your virtual services run on a private location, you can upgrade them manually. To view virtual services that are using older image versions, navigate to the Virtual Services tab. If any of your virtual services are outdated, you will see a warning message there.

Follow these steps:

1. Navigate to the **Service Virtualization** tab. If any of your virtual services are outdated, you will see a warning message: `Some Virtual Services contain warnings. You can display all Virtual Services with warnings and explore the details.`
2. To filter, click **Only Virtual Services With Warnings**
3. Click the yellow exclamation mark icon next to a virtual service. Information about the virtual service version is shown
4. Click the **Upgrade** button
5. Select an option to upgrade the virtual service or all virtual services in this location

---

## Documentation References

For detailed information about service management, use the BlazeMeter MCP help tools:

**Service Management**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `mock-service-rename-move` (rename/move)
  - `mock-service-clone-service-with-transactions` (clone)
  - `mock-service-export-import-services-with-transactions` (export/import)
  - `mock-service-rename-or-delete-a-service` (rename/delete)
  - `mock-service-upgrade-outdated` (upgrade)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-rename-move", "mock-service-clone-service-with-transactions", "mock-service-export-import-services-with-transactions", "mock-service-rename-or-delete-a-service", "mock-service-upgrade-outdated"]}`


