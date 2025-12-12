# Transactional Analytics

## Transactional Analytics

Understand and use transactional analytics for virtual services, including monitoring transaction usage, performance metrics, and analytics insights.

**Use when**: Understanding and using transactional analytics for virtual services or monitoring transaction usage, performance metrics, and analytics insights.

### Overview

To better understand usage and behavior of a particular virtual service and to troubleshoot performance or matching issues, use Virtual Service Analytics for access to reporting, inspection and tracking data.

### View Analytics for a Transaction Virtual Service

1. Navigate to the **Service Virtualization** tab and click the **Analytics** tab
2. Click the **Open +** button and select a virtual service. The Analytics page with the **Inspection** tab opens and shows requests that hit the virtual service and whether any transactions matched the requests. To view other virtual services, click **Open +** repeatedly. A new tab will open for each virtual service
3. Navigate to the **Inspection** tab. You can view matched and not matched requests and their responses as well as the traffic inside the virtual service

### Inspection View

Inspection view displays details about recent traffic handled by a specific virtual service. Understanding which requests and responses were handled by your virtual services is critical in cases when there is a need to debug why certain requests were or were not returned by a virtual service. You can quickly identify specific requests by full-text search and display corresponding response details.

The Inspection view registers up to 5 requests per second, and 50 actions per second, per virtual service.

All actions share the same storage and are limited to 100. If there are more, the oldest are not visible. This means:
- The maximum total requests visible in the Inspection View is 100
- The maximum total actions visible in the inspection View is 100

This limit of 100 includes all types of actions, so it might show you "34 HTTP calls + 33 Webhooks + 33 State Updates" or "100 HTTP calls", depending on which actions are executed by your transactions.

The value shown on the main page is the total transaction count from the time on when the virtual service was created; this total is not reset by a restart.

### One-Click Access to the Matched Transaction from Inspection View

If network traffic was matched by your virtual service, it is important to know which transaction was responsible for that match. To review the matching rules, click the transaction ID. The transaction definition pop-up dialog opens.

### Create Transactions from a Live Service

Inspection view allows you to directly create transactions based on the real responses provided by the live system in case the virtual service is in *Redirect to live system* mode.

1. Navigate to the **Service Virtualization** tab and click the **Analytics** tab
2. In the **Inspection** tab, you can see the type of service in the **Source** column - **mock** or **live**
3. Create a new transaction from the live service. Hover over the **Live** tag in the **Source** column and click the display icon that appears
4. A window **Save Live Request / Response as a New Transaction** opens
5. Enter the Transaction Name
6. (Optional) Assign Tags
7. (Optional) Enable **Update Virtual Service** to update your virtual service with a newly created transaction

The transaction is created. You can view it in **Asset Catalog**.

### Quick Access to Analytics

When hovering over a row in the virtual services table, a bar chart icon appears next to the virtual service entry. Click this quick access button to open the **Analytics** tab directly to view reports for this virtual service.

### View Virtual Services Reports

For every virtual service, it is possible to display four different reports to analyze the utilization and behavior of the Service:

- **Transaction Daily Counts**: Displays the number of transactions in a defined time period for a selected virtual service. This report allows you to review your system loads by virtual service
- **Transaction Hits and Misses**: Displays the number of transactions that were performed on virtual services for a given time period. The report displays a bar chart with the total number of Node Hits, Specific Hits, and Misses
  - **Node Hits**: A node hit occurs when the node matches a meta or signature response in a service image
  - **Specific Hits**: A specific hit occurs when the request matches a specific transaction
  - **Misses**: A miss occurs when the request is unknown and the request does not match a signature or exact match
  - The data in this report is limited to a single virtual service. Click an item in the legend at the bottom of the report to hide or show the corresponding data
- **Virtual Service Response Time**: Establishes the current health of a specific virtual service. This report is useful for determining how different system loads or performance testing impacts the response times for a virtual service. Response times in this report include think time. The report displays the maximum, average, and minimum response times, in milliseconds, in the form of a line graph
- **Virtual Service Transactions per Second**: Establishes the current health of a specific virtual service. This report is useful for determining how different system loads or performance testing impacts the transactions per second for a virtual service. The report displays the maximum, average, and minimum transactions per second in the form of a line graph

**Note**: For Virtual Service Response Time and Virtual Service Transactions per Second reports, the following applies:
- For reports of range up to 6 hours, granularity of one minute is used
- For reports of range up to 168 hours, granularity of one hour is used
- For reports of range higher than 168 hours, granularity of one day is used

Follow these steps:

1. Navigate to the **Service Virtualization** tab and click the **Analytics** tab
2. Select the **Reporting** tab
3. Select a report from the drop-down list
4. Select a time range of data in which you are interested in. You can select an explicit range or use the presets

### View Usage Metrics in Settings

The Usage Report tab in Settings is only available to Administrators and is typically used for licensing/cost analysis. To learn more, see [How Do I View My Usage Reports?](https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html).

1. Navigate to **Settings**, **Workspace**, **Usage Report**
2. In the **Usage Report** section, open the drop-down list to view the metrics for this Workspace or Account, respectively
   - The **Virtual Services Transactions** report shows the number of transactions for Transactional Virtual Services by time range
   - The **Virtual Services Concurrent Usage** report shows the maximum number of Virtual Service Replicas for Transactional Virtual Services concurrently running for this Workspace or Account, respectively

---

## Documentation References

For detailed information about transactional analytics, use the BlazeMeter MCP help tools:

**Transactional Analytics**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-transactional-analytics`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-transactional-analytics"]}`

