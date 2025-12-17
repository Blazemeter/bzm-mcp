# Virtual Services

## Create Your First Virtual Service

Create your first virtual service using the Learn More wizard, including uploading files, selecting transactions, configuring parameters, and running the service.

**Use when**: Creating your first virtual service using the Learn More wizard or uploading files, selecting transactions, configuring parameters, and running the service.

### Creating Your First Virtual Service

The full set of configuration options is available when you create a virtual service from the **Virtual Services** page. To learn more, see [Creating a Virtual Service](https://help.blazemeter.com/docs/guide/mock-service-create.html).

**To create your first Virtual Service:**

1. Log in to BlazeMeter and click the **Service Virtualization** tab
2. Click **Asset Catalog** at the top of the page
3. Obtain a file that contains all Transactions that you want to use for your virtual service. Drag the file into the upload area, or click the area to browse and find the file you want. To learn more about supported file formats of transactions, see [Adding Transactions](https://help.blazemeter.com/docs/guide/mock-service-add-transactions.html). To upload multiple Swagger files using a zip file, the main file in the zip file must be named index.json or index.yaml for the upload to work. The **Virtual Services** page opens, and the first virtual service that you see listed was newly generated from the file you uploaded
4. Click the arrow next to the virtual service name to expand the details for the virtual service
5. Enter a name for the virtual service in the **Name** field or keep the generated default name
6. Leave the default selection in the **Select Service** drop-down. A virtual service created by the Wizard automatically creates a Service for you. To learn more about Services and how you create them in a typical scenario, see [Creating a Virtual Service](https://help.blazemeter.com/docs/guide/mock-service-create.html)
7. From the **Location** drop-down, select the location where you want to deploy your virtual service
8. Select either **HTTPS** or **HTTP** from the **Protocol** drop-down. The default is HTTPS
9. Click the **Virtual Services > Transactions** tab. Creating a virtual service from "Learn More" automatically adds all Transactions from your uploaded file to the virtual service. You include Transactions by moving them to the right pane, and exclude them by moving them to the left pane. Use a quick action to move transactions from one column to the other: Click the **Include this transaction in the Virtual Service** icon in the left column or the **Remove this transaction from the Virtual Service** icon in the right column
10. Click the **Virtual Services > Parameters** tab. (Optional) Set the **Think Time** to control an artificial delay between the request and the response. The default is "No Delay". To learn more, see [Simulating Irregular Response Latencies](https://help.blazemeter.com/docs/guide/mock-service-think-time-irregular-response-latency.html). (Optional) In the **No Matching Requests** field, choose what to do when a request against the virtual services does not match any of the provided transactions. The request can either throw an error or be redirected to the live service. If you select **Redirect to live system**, a new field **Live System Endpoint** appears where you fill in the live system's URL. To learn more about generic or conditional redirects, see [Live System Endpoint](https://help.blazemeter.com/docs/guide/mock-service-add-transactions.html#h_01F8XBM7A57RC0A59107YGA0PN) in the [Adding Transactions](https://help.blazemeter.com/docs/guide/mock-service-add-transactions.html) article
11. Leave all other defaults and click **Save**. The virtual service is created and available on the **Virtual Services** page

Now, [run the service](https://help.blazemeter.com/docs/guide/mock-service-run.html) to activate the virtual endpoint and run tests against it!

---

## Create a Virtual Service

Create virtual services in BlazeMeter using various methods, including creating from transactions, from recordings, from templates, and from existing services.

**Use when**: Creating virtual services in BlazeMeter using various methods, creating from transactions, recordings, templates, or existing services, or configuring virtual service properties.

### Overview

In BlazeMeter, you can create a virtual service from transactions, from a recording, or from a template.

**Use one of the following ways to create Virtual Services:**
- **From transactions**: [Create a new service from transactions](skill-blazemeter-service-virtualization://references/virtual-services.md) or [Create a virtual service from an existing service](skill-blazemeter-service-virtualization://references/virtual-services.md)
- **From recording**: [Create a virtual service using the BlazeMeter Proxy Recorder](skill-blazemeter-service-virtualization://references/virtual-services.md)
- **From template**: [Create a virtual service from a virtual service template](skill-blazemeter-service-virtualization://references/virtual-services.md)

**After creating virtual services, set up transactions:**
- [Complete the configuration of your virtual service](skill-blazemeter-service-virtualization://references/virtual-services.md)
- [Add transactions to the Service](skill-blazemeter-service-virtualization://references/virtual-services.md)
- [Include/Exclude Transactions in a virtual service](skill-blazemeter-service-virtualization://references/virtual-services.md)
- [Modify transactions in a running virtual service](skill-blazemeter-service-virtualization://references/virtual-services.md)
- [Define the priority of multiple matching transactions](skill-blazemeter-service-virtualization://references/virtual-services.md)

**After setting up transactions, configure optional properties:**
- [Configure runtime properties](skill-blazemeter-service-virtualization://references/virtual-services.md)
- [Group multiple virtual services under a single endpoint](skill-blazemeter-service-virtualization://references/virtual-services.md)
- [(Optional) Virtualize Message Queues](skill-blazemeter-service-virtualization://references/virtual-services.md)

### Create a New Service from Transactions

In BlazeMeter, a "Service" is the representation of the underlying live service, and it serves as a container for Transactions. You first create a Service, and upload Transactions into the Service.

Having at least one Service with transactions is a prerequisite for creating a virtual service. If you already have a Service, jump directly to [Create a Virtual Service from an Existing Service](skill-blazemeter-service-virtualization://references/virtual-services.md).

Follow these steps:

1. Navigate to the **Service Virtualization** tab and click **Virtual Services**
2. In the **Virtual Services** tab, click the **Plus** button to create a virtual service, and select **Create from Transactions**. A new row is added to the top of the **Virtual Services** list
3. Enter a name for the virtual service in the **Name** field
4. Click the arrow next to the virtual service name to expand the details for the virtual service
   - (Optional) Enter a **Description** for your virtual service
   - (Optional) Select a **Configuration**. If needed, define attribute-value pairs for your environment variables on the **Configurations** tab
   - (Private Location only) Under **Create Log**, enable or disable logging on the Private Location. To learn more, see [Running Virtual Services on Private Locations](skill-blazemeter-service-virtualization://references/virtual-services.md)
5. Drag your transaction file into the upload area, or click the Upload area to browse to the file. Select a file that contains the transactions for your virtual service. To upload multiple Swagger files using a zip file, the main file in the zip file must be named index.json or index.yaml for the upload to work. The **Import Transactions** dialog opens
6. Select the Service you want to add these transactions to. The Service is a representation of the underlying live service, and it serves as a container for the Transactions you will upload. If an existing Service contains Transactions that are needed for this virtual service, select the existing Service. Or create a new service: Click **Add Service**
   - (Optional) To assign one or more tags, type the tag name(s) in the **Tags** field and press **Enter**. Tags make Transactions easier to identify, especially within a large Service. You can provide tag definitions here to apply the defined tags to all imported Transactions. Or you can define tags at the Transaction level after import. To enter multiple tags, press **Enter** after each tag name
   - Click **Import**

### Create a Virtual Service from an Existing Service

In BlazeMeter, a "Service" is the representation of the underlying live service, and it serves as a container for the Transactions. In this scenario, you create a virtual service by selecting an existing service that already contains the transactions that you need for your virtual service.

Follow these steps:

1. Navigate to the **Service Virtualization** tab and click **Virtual Services**
2. In the **Virtual Services** tab, click the **+** button to create a virtual service, and select **Create from Transactions**. A new row is added to the top of the **Virtual Services** list
3. From the **Service** drop-down list, select the service that contains the Transactions that you need for your virtual service

### Create Virtual Services Using the BlazeMeter Proxy Recorder

You can record a series of interactions from your browser, capture those interactions as transactions, and create a virtual service based on those transactions. Use the BlazeMeter Proxy Recorder to record the interactions.

Follow these steps:

1. Navigate to the **Service Virtualization** tab and click **Virtual Services**
2. In the Virtual Services tab, click the **+** button to create a new virtual service, and select **Create from Recording**. The BlazeMeter Recorder page opens in a separate tab
3. Follow the steps (starting with Step 3) in [Creating the Proxy Recorder](skill-blazemeter-recorders://references/proxy-recorder.md) to create your proxy for recording
4. Follow the steps for setting up recording based on your operating system:
   - [Recording Using Android Devices](skill-blazemeter-recorders://references/proxy-recorder.md)
   - [Recording Using Apple Devices](skill-blazemeter-recorders://references/proxy-recorder.md)
   - [Recording Using Firefox](skill-blazemeter-recorders://references/proxy-recorder.md)
   - [Recording Using Chrome](skill-blazemeter-recorders://references/proxy-recorder.md)
5. Click the **Record** button and record the necessary interactions within your application
6. Click **Pause** when finished
7. Click Virtual Service to export the recording to a virtual service. This creates a virtual service under the selected Service with all of the recorded Transactions assigned to it
8. Disable any proxy settings you had to enable to create the recording

### Complete the Configuration of Your Virtual Service

After you have created a virtual service using one of the above methods, complete its configuration.

1. Enter a name for the virtual service in the **Name** field
2. Click the arrow next to the virtual service name to expand the details for the virtual service
   - (Optional) Enter a **Description** for your virtual service
   - (Optional) Select a **Configuration**. If needed, define attribute-value pairs for your environment variables on the **Configurations** tab
   - (Private Location only) Under **Create Log**, enable or disable logging on the Private Location. To learn more, see [Running Virtual Services on Private Locations](skill-blazemeter-service-virtualization://references/virtual-services.md)
3. In the **Location** drop-down list, select the location that you want to deploy your virtual service to. Select from the available Google Cloud Platform locations (US East or EU West) depending on your location. Or select a [Private Location](skill-blazemeter-service-virtualization://references/virtual-services.md)
4. Select either **HTTPS** or **HTTP** from the **Endpoint** drop-down list. The default is HTTPS
5. (Optional) If you plan to run the virtual service in a [private location](skill-blazemeter-service-virtualization://references/virtual-services.md), select a **preferred port** in the **Port** field. To learn more about preferred ports, see [Select a Preferred Port](skill-blazemeter-service-virtualization://references/virtual-services.md)
6. Under **Runner**, leave the default **HTTP Runner**. To learn more about the optional **Messaging Runner**, see [Virtualizing Message Queues](skill-blazemeter-service-virtualization://references/virtual-services.md)

### Add Transactions to the Service

To add Transactions to a Service, you can upload additional Transactions directly on the **Service Virtualization** tab without having to switch tabs. Drop a file into the upload area or click the Plus button to create new Transactions. To learn more about supported transaction file formats, see [Adding Transactions](skill-blazemeter-service-virtualization://references/transactions.md).

### Include/Exclude Transactions in a Virtual Service

After you have [added transactions](skill-blazemeter-service-virtualization://references/transactions.md) to the Service and have created a virtual service, the next step is always to select the transactions for this virtual service and define their parameters.

**On the Transactions tab:**

1. Select transactions that you want to include. You have several options:
   - Search and filter transactions in the columns by entering a tag or search text. To select all transactions *visible in the column* (not all Transactions *in the service*), click the check box in the column header
   - Or, manually select checkboxes in the columns
2. Move selected transactions from the **Other Transactions in Your Catalog** column to the **Transactions in This Virtual Service** column. You have several options how to do this:
   - Click the **Right Arrow** to move selected transactions from **Other Transactions in Your Catalog** column to the **Transactions in This Virtual Service** column
   - Select checkboxes in the **Transactions in This Virtual Service** column and click the **Left Arrow** to remove these transactions from the virtual service
   - Use the quick action to move selected transactions with a single click: Click the **Include this transaction in the Virtual Service** icon in the left column. To remove a transaction from the virtual service, click the corresponding **Remove this transaction from the Virtual Service** icon in the right column
3. (Optional) In **Transactions in This Virtual Service** column, expand each transaction and define a **Priority** to control the matching order when a request matches multiple transactions. The transaction with the lowest priority number matches first. For details, see [Priority of Multiple Matching Transactions in a Virtual Service](skill-blazemeter-service-virtualization://references/virtual-services.md)

**On the Parameters tab:**

1. (Optional) In the **Think Time** section, define an artificial delay between the request and the response. To learn more, see [Simulating Irregular Response Latencies](skill-blazemeter-service-virtualization://references/transactions.md). Default: "No Delay"
2. (Optional) In the **No Matching Requests** section, choose the correct logic for when a request against the virtual services does not match any of the provided transactions. The request can either throw an error or be [redirected to the live service](skill-blazemeter-service-virtualization://references/transactions.md). Default: Return no match found (404)
3. (Optional) In the **Proxy** section, define a proxy to connect to the live system endpoint. Default: No proxy
   - Proxy URL
   - Username
   - Password
   - Certificate — Upload or select a certificate needed for the connection
   - No Proxy — Provide a comma-separated list of URLs to exclude from this proxy
4. (Private Locations/Docker only) Select an **SSL Authentication**. To learn more, see [Running Virtual Services on Private Locations](skill-blazemeter-service-virtualization://references/virtual-services.md)
5. Click **Save**. Your virtual service is saved and added to the list of available virtual services

The virtual service is not active until you run it. Click **Run Virtual Service** to run it. For information about the next steps, see [Run a Virtual Service](skill-blazemeter-service-virtualization://references/virtual-services.md).

---

## Run a Virtual Service

Running a virtual service makes it available for you to test against. Running a virtual service is a simple two step process:
1. Run the Virtual Service
2. Connect your application to the running virtual service

**Use when**: Running a virtual service to make it available for testing or connecting your application to a running virtual service.

### Run a Transaction-Based Virtual Service

**Steps:**

1. Find your virtual service on the **Service Virtualization** tab and click **Run**. The Status changes to Running, and the endpoint for the running virtual service appears
2. Copy the endpoint for the virtual service and redirect your application to point to the virtual service instead of the real Service. Do not refer to a Kubernetes-based virtual service by its plain IP address
3. You implement the redirect configuration in your application, not within BlazeMeter. How you do it depends on your application. It's often as simple as changing a value in an application properties file from the live service address to the virtual service endpoint
4. After you redirect your application to the virtual service, restart the application

The user and date when the virtual service was **Created** and **Updated** are indicated here for your reference. After you have run a virtual service at least once, no matter with which status (running, failed, stopped, configuring), the details view also indicates the **Version** of the image.

### Filter Virtual Services by Status

In the Virtual Services tab, you can filter the transactions based on their status. The filter helps in cases where there are many virtual services defined. By using this filter option, it is easy to display a subset of virtual services based on a certain status. For example, you can display only virtual services that are running or stopped.

### Bulk Run Virtual Services

You can bulk run virtual services from the **Virtual Services** tab or from the **Asset Catalog** tab.

**Steps:**

1. Click the **Service Virtualization** tab
2. Click **Virtual Services** at the top of the page
3. Find your virtual services on the **Service Virtualization** tab
4. Select the checkbox next to each virtual service that you want to run
5. Select the **Run Virtual Services** button next to the virtual service

**Important Notes:**
- If one of the services is already running when you apply the bulk action, the **Run Virtual Services** button is disabled. Conversely, if one of the services is in the stopped state, then bulk stopping is disabled
- Additionally, you can also delete virtual services in bulk
- Bulk actions are limited to deploying 25 virtual services at a time

### Configure SSL Connection to Virtual Services

BlazeMeter can configure HTTPS connections to virtual services over TLS/SSL. When you run a virtual service over HTTPS, verify that your application can connect to the virtual service. You can connect your application using the SSL certificate that we provide.

#### Deploy Virtual Services to a Cloud Location

When you deploy a virtual service to a cloud location, it uses a certificate signed by the Let's Encrypt certificate authority.

If the application or browser you're using to access a virtual service does not trust certificates issued by Let's Encrypt, then you will need to configure it to trust the following certificates:
- Let's Encrypt Authority X3 intermediate certificate
- DST Root CA X3 root certificate, which is used to cross-sign at the previous certificate

Refer to your application, language, or operating system documentation for details on how to import these certificates.

#### Deploy Virtual Services to a Private Location

When you deploy a virtual service to a Private Location, the HTTPS endpoint is based on the IP address of the agent that deployed the virtual service. No FDQN resolution occurs by default.

Use the following self-signed certificate to connect to a virtual service deployed to a private location:

```
-----BEGIN CERTIFICATE-----
MIIC4jCCAcqgAwIBAgIEXSSpbDANBgkqhkiG9w0BAQsFADAgMR4wHAYDVQQDDBUq
Lm1vY2suYmxhemVtZXRlci5uZXQwHhcNMTkwNzA5MTQ0OTE2WhcNNDYxMTIzMTQ0
OTE2WjAgMR4wHAYDVQQDDBUqLm1vY2suYmxhemVtZXRlci5uZXQwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQCoePRBvFbV5We4CmR/68AddxloEeH3oLeg
ylZpZuPbQt0kEg93mYo4j1xvrTThS4gqCWg1bg7eh4pvVeNTUvTZf/BvCq4RGohG
dfodFzHSuSNMVAhCrMmlUi+T3M4nrBjCj41ZgDB7bijMSbYhb5oOAqXHxLSNCgO/
3UDlUwdbyTzlag0p5iu8spI6IoS6XtWR44h8Jm+WOkBSp7PIc8SMQC2xj5DWHrxx
NlTTj9dC099jvvsR4ncelYNwQGEM5xj6HqTFdD6NGYkyV7r2egjl25uBbruC+M7k
1k4k5BgzuR4g/M1D9y0Yw1ezUvYMaT5g4aCSU5RV3ha4IBJaItZTAgMBAAGjJDAi
MCAGA1UdEQQZMBeCFSoubW9jay5ibGF6ZW1ldGVyLm5ldDANBgkqhkiG9w0BAQsF
AAOCAQEARRPDOPPHQgZCmNqamVcC4rjuG6Q5uDrOejg9uoI2iYHa4ScD8WZxKUy/
7FTzYMBkBSb6NbhEJfIP/D7PL+MWG115080LM01WDdYN8Avjqx4ZlmyQyAwTsdKt
hkGErTVqwiBjuDxjNosFi/0w1XeYIRdZ41iE5x9wqy0qio9pVyc30rwAimIbFFDc
aKtLTEom3yAhj4vpBojN35YyEY6jnTkpQBcd4bnarwtqYvTbqiSIbMJivmTHl88e
eWsSBE53G/u2aDPOyx+Lg24Rqh6I+ssgRVmNDZIc4Vj8cvEeTmihMVY6DTpwPls5
yuLi+DPQq6qM479piqLVP7LPV5vs/A==
-----END CERTIFICATE-----
```

If you want to generate a hostname for the HTTPS endpoint, add an entry to your operating system's host file that lists the IP address followed by a host name that ends with mock.blazemeter.net.

**Example:**
```
10.1.1.100 testmock.mock.blazemeter.net
```

---

## Run Virtual Services on Private Locations

After you have [created a virtual service](skill-blazemeter-service-virtualization://references/virtual-services.md), you can configure it to run on a Private Location.

**Use when**: Running virtual services on Private Locations, configuring virtual services for Docker or Kubernetes deployments, or sharing Private Locations across workspaces.

### Configuration Steps

1. Navigate to the **Service Virtualization** tab and click **Virtual Services**.
2. Under **Create Log**, enable or disable logging on the Private Location. If enabled, it will create one log file per virtual service on the Private Location, or if the file exists, append the log.
3. If you plan to run the virtual service in a Private Location, select a **preferred port** in the **Port** field.

### Virtual Services on Private Locations using Docker

The following best practices apply to virtual services on Private Locations using Docker.

On the **Parameters** tab of a mock service, you can configure authentication:

1. Select an **SSL Authentication** type:
   - No Authentication (default)
   - 1-way SSL
   - 2-way SSL
2. If you selected SSL:
   - Select an existing **Keystore** or upload a new one.
   - Provide the **Keystore Password** and the password used to access individual keys in the keystore.
   - (Optional) To define how to identify during SSL/TLS communication using an alias for a `private key entry` defined in your keystore, select the **Alias** and provide an **Alias Password**.

#### Select a Preferred Port

If you plan to run the virtual service in a Private Location and you are creating a Docker-based transaction virtual service, you can define a preferred port. If the port is available, it will be assigned to the virtual service.

- If you leave the **Port** field blank, a port is chosen from the range defined for the Private Location. To learn more, see [Setting Port Range on Your Agent](skill-blazemeter-recorders://references/proxy-recorder.md).
- If the preferred port is outside of the defined port range, a notification message is shown and a new port within the defined range has to be entered.
- If an existing service is running on the preferred port already, a notification message appears when you run the virtual service. BlazeMeter then selects the first available port within the defined range.

To update the preferred port for a virtual service running in a Docker-based Private Location, follow these steps:

1. Stop the running virtual service.
2. Update the existing preferred port to the new port number.
3. Run the virtual service again. If the port is available, it will be assigned to the virtual service.

### Virtual Services on Private Locations using Kubernetes

The following best practices apply to virtual services on Private Locations using Kubernetes.

#### Rules for Endpoints Generated for Kubernetes Virtual Services Deployment

For a Private Location that uses Kubernetes, the URL format is the following:

```
http(s)://(mock-name[40])(serviceid[9])-<port>-<namespace>.<sub-domain>
```

- **Virtual Service Name**: First 40 lowercase alpha numeric characters of the virtual service name. If the first 40 characters of a virtual service name conflict with any other existing virtual service name, a unique ID is added to the endpoint.
- **Service ID**: ID associated with the service name. Service ID is used in the endpoints that are generated after you deploy your virtual service. When you know your service ID, you can predict the format of your virtual service endpoint. View the Service ID in the **Service** drop-down list and copy it to clipboard.
- **Port**: 8080 for transaction virtual services.
- **Namespace**: Your Kubernetes namespace.
- **Sub-domain**: Configured as a part of an agent set up.

### Share Private Locations across Workspaces

If you have several BlazeMeter workspaces, you can choose to maintain separate Private Locations for each workspace, or share Private Locations across several workspaces.

Sharing Private Locations across multiple workspaces in Service Virtualization helps you to:

- Use your Private Locations more efficiently.
- Manage them more easily on the account level.
- Deploy virtual services from any workspace that shares the location.

To learn more about sharing Private Locations, see [Manage Private Locations](skill-blazemeter-administration://references/private-locations.md).

**To use shared locations:**

1. (For existing virtual services) Stop the virtual service and verify it is stopped.
2. Share the location with the required workspaces. The Location dropdown now includes the new the shared Private Locations.
3. Select a shared Private Location and choose a port.
4. Start the virtual service on the shared Private Location.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Run Virtual Services on Private Locations**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-on-private-locations`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-on-private-locations"]}`

---

## Embed Virtual Services in a Taurus Script

The Taurus automation testing framework now includes definitions to add virtual services within a Taurus test file. As long as the virtual service already exists in BlazeMeter, you can include it in a Taurus test definition file.

**Use when**: Embedding virtual services in Taurus test scripts or defining virtual service dependencies in Taurus YAML configuration files.

Taurus includes a dependencies node that allows you to define dependencies; `mock service` is the first dependency you can define.

### Taurus Dependencies Structure

To include a virtual service in a Taurus test, define the following nodes in your Taurus file:

- **dependencies**: The root node and parent object for the inclusion of virtual services in a test definition file.
- **service**: Child node of `dependencies`. Defines the Service or Services that contain assets that are dependencies for the test. Enter a [Service](skill-blazemeter-service-virtualization://references/introduction.md) name that exists in BlazeMeter Service Virtualization. You can define more than one Service as needed, but at least one is required.
- **mock service**: Child node of `service`. Defines the virtual service to use as the virtual endpoint for hosting the Transactions to test against. You can define more than one virtual service, but either one virtual service or one tag is required.
- **mock service template**: (Optional) Child node of `service`. Defines the Template from which to load Transactions into the virtual service. The Template must exist in the defined Service. If you do not define a Template, the test takes the Transactions from specific Transaction definitions in the Taurus file.
- **transactions**: (Optional) Child node of `service`. Defines the specific Transactions to include in the virtual service. If you define Transactions separately, they override the Transactions provided directly in the virtual service. The Transactions must be in the repository and exist within the defined service.
- **transaction-filter**: (Optional) Child node of `service`. Defines filter criteria for Transactions in the specified virtual service. At this time, you can only filter by tags.
- **tags**: (Optional) Child node of transaction-filter. Defines the tags by which to filter the Transactions in the test.

### Example Taurus File with Dependencies

```yaml
execution:
- iterations: 50
  concurrency: 100
  ramp-up: 1m
  hold-for: 5m
  scenario: quick-test

scenarios:
  quick-test:
    requests:
    - http://my-application.com

dependencies:
  services:
  - service: Identity
    mock-service: IdentityMock
    mock-service-template: Identity (OK responses)
  - service: PaymentGateway
    mock-service: PaymentGatewayMock
    transactions:
    - ProcessPayment
    - AddPaymentMethod
    - RemovePaymentMethod
```

### Important Notes

- The transaction names within the same service must be unique. If you name a transaction that is part of the same service with the same name that already exists, an error message appears.
- Individual transactions not contained in a template do not have priorities associated with them. There is no priority at the transaction level as the same transaction might have a different priority in various services.
- When you run this test, the Transactions are loaded into the virtual service from the Template or the inline Transaction definitions.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Embed Virtual Services in a Taurus Script**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-embed-in-taurus-script`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-embed-in-taurus-script"]}`

---

### Modify Transactions in a Running Virtual Service

You can add and remove transactions or modify existing transactions without having to restart the virtual service.

- To add a transaction to or remove it from the virtual service, update the virtual service's transaction list in the virtual services tab and then click the **Update** button. When you run the test again, the changes will be reflected
- To modify a transaction, make the changes and click **Save** in the transaction. Then click the **Update** button in the virtual services tab. When you run the test again, the changes will be reflected

### Define Priority of Multiple Matching Transactions in a Virtual Service

When you test against a virtual service, the virtual service first attempts to match incoming requests against any of its Transactions. The Transactions can be explicitly spelled out requests or regular expressions. When a virtual service receives a request that matches multiple Transactions, the virtual service chooses the Transaction with the *lowest* value in the **Priority** field.

**Examples:**
- Say you have a virtual service for a service that searches by zip code with two transactions. Transaction A matches a parameter value of 75024, and Transaction B matches any five-digit number. You want the Transaction with the *more specific* matching criteria (Transaction A) to have the *higher priority* so that it matches first, and the *broader* matching criteria (Transaction B) shall only match if the specific zip for Transaction A is not entered, so you give it *lower* priority
- After importing 100 transactions, they are all assigned the same default priority of 10. Fifteen of them are generic transactions that should be matched only *after* the more specific eighty five are matched. You don't want to have to manually change the priority level of eighty five transactions to 9. In this case, it's quicker to give the fifteen generic transactions a priority of 20, below the default of 10

Consider this matching logic when determining which Transactions to add to a virtual service, and whether one or more virtual services are required to meet your testing requirements.

Every transaction is added with the default priority level of 10.

- To have a Transactions match first, set its priority to 1
- To have a Transactions match *before* another, set its priority to a lower number
- To have a Transactions match *after* another, set its priority to a higher number
- To have a Transactions match last, set its priority to 20

You can assign the same priority to multiple transactions. Therefor it can happen that multiple *matching* Transactions have the same priority. In this case, the virtual service chooses the most recent Transaction first (the one with the highest Transaction ID number). To have fine control over the priority over default transactions, assign them unique priorities. Unique priorities use an index counter that defines the order without ambiguity.

**To assign unique priorities:**

1. Add transactions that can match
2. Enable **Unique Priorities**. The **Customize Unique Transaction Priorities** window opens and a table lists all included transactions
3. Arrange the rows in order of highest to lowest priority. You can use the following methods:
   - Click the handle and drag a transaction up to increase its priority
   - Click the handle and drag a transaction down to decrease its priority
   - To reorder a transactions to be first, click **Move Transaction to Beginning**
   - To reorder a transactions to be last, click **Move Transaction to End**
   - To reorder multiple transactions, enable their checkboxes and click the **Move Transaction to Beginning** or **Move Transaction to End** button (respectively) above the table
   - To reorder priorities after **Unique Priority** has been enabled, click the **Customize** button

### Configure Runtime Properties

(Optional) Go to **Virtual Services** and open the **Virtual Service** tab to configure optional runtime properties.

- **Show Logs**: Choose whether you want to capture runtime logs. Show Logs Max Size - Specify the maximum amount of logs to be captured. Enter a number between 0 and 100
- **Inspection Data**: Choose whether you want to capture inspection data. If you enable it, configure the following fields:
  - Inspection Data Max Request Size - Enter a number between 0 and 100
  - Inspection Data Max Requests Per Second - Enter a number between 0 and 5
  - Inspection Data Max Actions Per Second - Enter a number between 0 and 50
  - Inspection Data Max Body Size - Enter a number between 0 and 1024000
- **Matcher Logs Console**: Matcher Logs Enabled Show Logs Matcher Logs Enabled Matcher Logs Cache Max Size - Enter a number between 1 and 1000
- **More...**:
  - Jetty Container Threads - (Optional) Define the number of threads in the Eclipse Jetty container. Enter a value between 1 and 1000
  - Jetty Acceptors - (Optional) Define the number of acceptors in the Eclipse Jetty container. Enter a value between 1 and 1000
  - Request Timeout - Enter a number between 0 and 60000 milliseconds

### Group Multiple Virtual Services Under a Single Endpoint

(Optional) If you are running multiple virtual services across different Services, and the requirement arises that you need to run them under a single endpoint and port, you can group them.

1. Go to **Virtual Services** and open the **Virtual Service Groups** tab
2. Click the blue **Plus** button to create a Virtual Service Group
3. Give the group a name and description
4. Select a **Location**
5. Select an **Endpoint Protocol**
6. Define an **Endpoint Port**
7. (Optional) Define **tags**
8. On the **Virtual Services** tab, click **Assign Virtual Service** to add one or more virtual services to the group
9. On the Parameters tab, optionally, configure **SSL Authentication**

Now, under Actions, click the green **Run** button to run this group under a single endpoint.

---

## Create a Virtual Service Template

Virtual Service Templates are common collections of Transactions and Parameter selections that you can reuse when you need to test against those Transactions. For example, for a login service, you might create a Template that includes a few Transactions required for negative testing. Then, when you need to test those scenarios, you can quickly provision a virtual service based on that Template to test with.

Templates override the Transactions that are directly in a virtual service, and are meant to be a more persistent way to add commonly grouped Transactions to a virtual service on the fly.

**Use when**: Creating virtual service templates for reusable transaction collections or creating templates, creating virtual services from templates, assigning templates, and creating templates from virtual services.

### Create a Virtual Service Template

Follow these steps:

1. Log into your BlazeMeter account
2. On the **Service Virtualization** tab, click **Virtual Services**
3. Go to the Virtual Service Templates tab and click the Add button
4. Give the Template a meaningful name. Provide meaningful names and descriptions because when testers are using the Virtual Services Configuration to add virtual services to tests, they need to understand what might be relevant to their tests based on names only
5. Select or create the associated Service. The Service is a representation of the underlying live service, and it serves as a container for the Transactions you will upload. If an existing Service contains Transactions that are needed for this virtual service, select the existing Service. To create a new Service: Click **Select Service**. Enter the name for your new Service and click **Add Service**
6. Click the arrow to the left of the Template name to edit Template details
7. Enter a description for the Template
8. (Optional) If the Transactions needed for the Template don't yet exist, drag a supported file type into the upload box. If the Transactions already exist in the Service you selected, skip to Step 10. **Note:** If you want to upload multiple Swagger files using a zip file, the main file in the zip file must be named index.json or index.yaml for the upload to work. The Import Transactions dialog opens
9. Select the Service that you specified in the Service field next to the Template name
10. If you want to assign one or more tags to these transactions, type the tag name(s) in the **Tags** field and press **Enter**. Tags make Transactions easier to identify, especially within a large Service. You can provide tag definitions here to apply the defined tags to all imported Transactions. Or you can define tags at the Transaction level after import. To enter multiple tags, press **Enter** after each tag name
11. Click **Import**. The imported Transactions appear in the Other Transactions in Your Catalog pane
12. Select the Transactions to include in the Template, and click the right arrow icon to move them to the Transactions in this Virtual Service Template pane. You can use a quick action to move transactions with a single click. Click the **Include this transaction in the Virtual Service** icon in the left column. To remove a transaction from the virtual service, you can click the **Remove this transaction from the Virtual Service** icon in the right column
13. (Optional) Expand each Transaction in the Virtual Service Template and enter values in the Priority field to control the matching order to follow when a request matches multiple Transactions. The Transaction with the lowest number matches first. By default, all Transactions have the same Priority value, and a multiple matching scenario matches on the Transaction with the highest ID number. Setting a priority for a Transaction only applies to that Transaction within the specific Template. In other virtual services or Templates, the Transaction can have a different priority value
14. Click the **Parameters** tab
15. In the **No Matching Requests** field, choose the correct logic for when a request against the virtual service does not match any of the provided transactions. The request can either throw an error or be redirected to the live service
16. Set the **Think Time** in milliseconds to control the amount of time spent between when the virtual service receives a request and returns a response. The default is 0, but you can update the field to simulate delayed responses of a fixed length in milliseconds, or define a randomized Think Time with Lognormal or Uniform distribution within bounds
17. Click **Save**

## Create a Virtual Service Template

Virtual Service Templates are common collections of Transactions and Parameter selections that you can reuse when you need to test against those Transactions. For example, for a login service, you might create a Template that includes a few Transactions required for negative testing. Then, when you need to test those scenarios, you can quickly provision a virtual service based on that Template to test with.

Templates override the Transactions that are directly in a virtual service, and are meant to be a more persistent way to add commonly grouped Transactions to a virtual service on the fly.

**Use when**: Creating virtual service templates, reusing common collections of Transactions, or provisioning virtual services from templates.

### Create a Virtual Service Template

Follow these steps:

1. Log into your BlazeMeter account.
2. On the **Service Virtualization** tab, click **Virtual Services**.
3. Go to the **Virtual Service Templates** tab and click the **Add** button.
4. Give the Template a meaningful name. Provide meaningful names and descriptions because when testers are using the Virtual Services Configuration to add virtual services to tests, they need to understand what might be relevant to their tests based on names only.
5. Select or create the associated Service. The Service is a representation of the underlying live service, and it serves as a container for the Transactions you will upload. If an existing Service contains Transactions that are needed for this virtual service, select the existing Service. To create a new Service: Click **Select Service**. Enter the name for your new Service and click **Add Service**.
6. Click the arrow to the left of the Template name to edit Template details.
7. Enter a description for the Template.
8. (Optional) If the Transactions needed for the Template don't yet exist, drag a supported file type into the upload box. If the Transactions already exist in the Service you selected, skip to Step 10. **Note**: If you want to upload multiple Swagger files using a zip file, the main file in the zip file must be named index.json or index.yaml for the upload to work. The Import Transactions dialog opens.
9. Select the Service that you specified in the Service field next to the Template name.
10. If you want to assign one or more tags to these transactions, type the tag name(s) in the **Tags** field and press **Enter**. Tags make Transactions easier to identify, especially within a large Service. You can provide tag definitions here to apply the defined tags to all imported Transactions. Or you can define tags at the Transaction level after import. To enter multiple tags, press **Enter** after each tag name.
11. Click **Import**. The imported Transactions appear in the Other Transactions in Your Catalog pane.
12. Select the Transactions to include in the Template, and click the right arrow icon to move them to the Transactions in this Virtual Service Template pane. You can use a quick action to move transactions with a single click. Click the **Include this transaction in the Virtual Service** icon in the left column. To remove a transaction from the virtual service, you can click the **Remove this transaction from the Virtual Service** icon in the right column.
13. (Optional) Expand each Transaction in the Virtual Service Template and enter values in the Priority field to control the matching order to follow when a request matches multiple Transactions. The Transaction with the lowest number matches first. By default, all Transactions have the same Priority value, and a multiple matching scenario matches on the Transaction with the highest ID number. Setting a priority for a Transaction only applies to that Transaction within the specific Template. In other virtual services or Templates, the Transaction can have a different priority value.
14. Click the **Parameters** tab.
15. In the **No Matching Requests** field, choose the correct logic for when a request against the virtual service does not match any of the provided transactions. The request can either throw an error or be redirected to the live service.
16. Set the **Think Time** in milliseconds to control the amount of time spent between when the virtual service receives a request and returns a response. The default is 0, but you can update the field to simulate delayed responses of a fixed length in milliseconds, or define a randomized Think Time with Lognormal or Uniform distribution within bounds.
17. Click **Save**.

### Create a Virtual Service from a Virtual Service Template

At any time after saving the Template, click **Create Virtual Service** to the right of the Template name to dynamically provision a virtual service that includes the transactions in the Template.

1. Go to the **Virtual Service Templates** tab.
2. In the **Actions** column, click the **Create Virtual Service** button.

Your virtual service is created and you can find it in the **Virtual Services** tab.

### Assign a Template to a Virtual Service

You can assign a Template to a new or existing virtual service at any time.

To assign a Template to a virtual service:

1. Navigate to a virtual service and in the **Actions** column, click the icon for **Assign Virtual Service Template from this Virtual Service**.
2. Select the Template to assign and click **Apply**.

The Template is assigned to the virtual service. If the virtual service already contained Transactions, they are overwritten by the Transactions in the Template.

A template can be assigned to a virtual service if the service is stopped or running. In either case, the transactions in the virtual service will be overwritten with the transactions from the template assigned.

### Create a Virtual Service Template from a Virtual Service

After you create a virtual service with Transactions, you may realize that you need to reuse that virtual service at a later date. Create a Template from the virtual service to preserve its configuration for future use.

In the **Actions** column for the virtual service, click the icon for **Create Virtual Service Template from this Virtual Service** to dynamically provision a virtual service that includes the transactions in the Template.

A template is created with the same configuration as the virtual service and you can find it in the **Virtual Service Templates** tab.

### Documentation References

For detailed information about creating virtual service templates, use the BlazeMeter MCP help tools:

**Create a Virtual Service Template**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-template-create`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-template-create"]}`

---

### Create a Virtual Service from a Virtual Service Template (Legacy Section)

At any time after saving the Template, click **Create Virtual Service** to the right of the Template name to dynamically provision a virtual service that includes the transactions in the Template.

1. Go to the **Virtual Service Templates** tab
2. In the **Actions** column, click the **Create Virtual Service** button

Your virtual service is created and you can find it in the **Virtual Services** tab.

### Assign a Template to a Virtual Service

You can assign a Template to a new or existing virtual service at any time.

To assign a Template to a virtual service:

1. Navigate to a virtual service and in the **Actions** column, click the icon for **Assign Virtual Service Template from this Virtual Service**
2. Select the Template to assign and click **Apply**

The Template is assigned to the virtual service. If the virtual service already contained Transactions, they are overwritten by the Transactions in the Template.

A template can be assigned to a virtual service if the service is stopped or running. In either case, the transactions in the virtual service will be overwritten with the transactions from the template assigned.

### Create a Virtual Service Template from a Virtual Service

After you create a virtual service with Transactions, you may realize that you need to reuse that virtual service at a later date. Create a Template from the virtual service to preserve its configuration for future use.

In the **Actions** column for the virtual service, click the icon for **Create Virtual Service Template from this Virtual Service** to dynamically provision a virtual service that includes the transactions in the Template.

A template is created with the same configuration as the virtual service and you can find it in the **Virtual Service Templates** tab.

---

## Configure Environment Variables

Configure environment variables for virtual services using the Configurations tab, including creating configurations, using configuration values, and enabling/changing configurations.

**Use when**: Configuring environment variables for virtual services or creating configurations, using configuration values, and enabling/changing configurations using the Configurations tab.

### Create a Virtual Services Configuration

Before deploying a virtual service, create and select the desired configuration.

1. Go to the **Service Virtualization** tab and open the **Configurations** tab
2. For each configuration, click **Create New Configuration**
3. Enter a **Name** for the configuration, for example `staging`, `development`, `testing`
4. (Optional) Enter a **Description** that informs team members of the purpose of this configuration
5. For each property, click **Add Property** and enter a **Name** and its **Value**
6. Click **Save**

Now you can use the values and enable this configuration for a virtual service.

### Use the Configuration Values

Rather than hard-coding recurring configuration values in a virtual service, transaction, or processing action, you can define environment variables for virtual services to use at runtime, such as a different server and port for testing and staging.

1. Go to the **Service Virtualization** tab and open the virtual service
2. For each virtual service, identify the respective hard-coded values
3. Replace the hard-coded values with custom properties in `${config.name}` format. For example, to reference a custom port, use `${config.port}`. Click the **Copy** button next to the property name to copy the correct syntax into the clipboard

### Enable or Change a Virtual Services Configuration

You cannot change the active configuration while the virtual service is running.

1. Go to the **Service Virtualization** tab and open the virtual service
2. If the virtual service is running, click **Stop**
3. (Optional) Edit the configuration values on the **Configurations** tab if needed
4. Open the virtual service definition and select the desired configuration
5. Click **Run Virtual Service** to restart the virtual service with the new profile

**Note**: Rather than hard-coding recurring configuration values in a virtual service, transaction, or processing action, you can define environment variables for virtual services to use at runtime, such as a different server and port for testing and staging. Use the **Configurations** tab to create custom configurations to store your attribute-value pairs. To use a configuration value, refer to it in `${config.name}` format. For example, to reference a custom port, use `${config.port}`

---

## Add a Virtual Service to a Test

As a tester, you may need to configure your tests to:
- Test functionality that is difficult to reproduce using the live service, like negative scenarios or other uncommon behavior
- Test against a service that is not available
- For other use cases, see [Service Virtualization Use Cases and Capabilities](skill-blazemeter-service-virtualization://references/introduction.md)

**Use when**: Adding virtual services to performance or functional tests, configuring tests to use virtual services instead of live services, or testing against unavailable services.

### Overview

In the past, perhaps you worked with a center of excellence or other group to obtain virtual services to cover your specific testing scenario, or you built and managed them yourself using another tool. With Service Virtualization fully integrated into BlazeMeter, it is a much simpler process to associate a virtual service with your test. The test creation page includes a virtual service configuration that lets you quickly see the available virtual services, choose what you need based on your test requirements, and obtain the endpoint for the virtual service.

### Add Virtual Services to Tests

The Virtual Services Configuration is available for performance and functional tests.

**Steps:**

1. Access the **Configuration** tab for a performance or GUI functional test
2. Find the **Virtual Services Configuration** and click the slider to open it
3. Click the **+** button and select **Add Virtual Service**
4. Select a virtual service from the **Virtual Service Name** drop-down list. The virtual services are categorized by Service. Services represent the underlying live service. For example, for testing AWS integration in your application, the Service name might be AWS Service, and the virtual service might be a virtualization of one part of that service, such as AWS S3. These names are all controlled by the user who created the virtual services

After you select the virtual service, its information appears on the same row. If the Status is **Stopped**, the virtual service is not running, and any tests run against that virtual service will fail. [Run the virtual service](skill-blazemeter-service-virtualization://references/virtual-services.md) from the Service Virtualization tab to be able to use it in a test. If the Status is **Running**, your virtual service is ready, and the endpoint for the virtual service is available.

You can add multiple virtual services as needed. When you delete a virtual service from this pane, it only deletes it from that test, not from the product.

5. (Optional) Select the **Template** that contains the Transactions and Parameters you want to load into the virtual service. Templates offer common groupings of Transactions. For example, a Template could contain the Transactions required to test key negative scenarios for the AWS S3 service. If you have not selected a template, the virtual service runs with the transactions that it was configured with
6. With your selections in place, you should then verify if the application has been configured to test against the virtual service. If not, copy the endpoint and make the necessary change at the application level to ensure that the test runs against the virtual service instead of the live service

**Important Notes:**
- When you run the test, the data from the Template is loaded into the virtual service at runtime, and it overrides any existing Transactions that were defined directly in the virtual service
- If you want to load a virtual service into a test without using a Template, add the virtual service [directly in the Taurus script](https://help.blazemeter.com/docs/guide/mock-service-embed-in-taurus-script.html) and not in the UI

### Add Individual Virtual Services and Tags

Click the **Service Virtualization** tab to select individual virtual services and to add tags to a single test.

The yaml construct will be updated accordingly.

---

## Create a Virtual Service for AWS Testing

BlazeMeter includes a set of pre-built Transactions for testing AWS S3 cloud storage operations in your application. To find these Transactions, select the **AWS S3 Sample** service on the Asset Catalog page.

This tutorial describes how to use these Transactions to create a virtual service to test key S3 operations in your application. We'll use Templates to group positive and negative scenarios from the Service, from which we can then dynamically provision virtual services for each scenario as needed.

**Follow these steps:**

1. Navigate to the **Service Virtualization** tab and click **Virtual Services**
2. Go to the **Virtual Service Templates** subtab and click the **Plus** button
3. Name the Template "AWS S3 - Positive Scenarios", select the AWS S3 Sample service, and give the Template a meaningful description. When you select the AWS S3 Sample Service, the left pane of the Template populates with all of the transactions in that Service. Expand each Transaction to view details. Each pre-built Transaction contains a clear description so you understand what the request will do. If you need to know more details about the Request or Response, find the Transaction on the [Transactions](skill-blazemeter-service-virtualization://references/transactions.md) page
4. Move the following Transactions to the right pane:
   - Return object metadata (ok response)
   - Delete object (ok response)
   - Store object (ok response)
   - Retrieve object (ok response)
5. Click **Save**. The Template is created
6. Click Add again to create the Template for negative scenarios
7. Name the Template "AWS S3 - Negative Scenarios", select the AWS S3 Sample Service, and give the Template a meaningful description. When you select the AWS S3 Sample service, the left pane of the Template populates with all of the Transactions in that service
8. Move the following Transactions to the right pane:
   - Delete object (AccessDenied error)
   - Retrieve object (NoSuchBucket error)
   - Store object (OperationAborted error)
9. Click **Save**. The Template is created

Because we created Templates for these transactions, there are multiple ways you can leverage the Templates to become virtual services. Let's cover one way for each Template.

10. Click **Create Virtual Service** to the right of the AWS S3 - Positive Scenarios Template
11. Name the virtual service "AWS S3 - PUT and DELETE", leave the AWS S3 Sample service selected, and give the virtual service a meaningful description
12. Remove the Return and Retrieve object transactions from the right pane. As specified in the description, you only want to test a PUT and DELETE with this virtual service. The Template presented all positive scenarios, and from those you chose the Transactions required for this particular test
13. Click **Save**
14. Click **Run Virtual Service**. The virtual service is running and available to use for testing
15. Redirect the application under test to use the endpoint for the virtual service instead of the live service. You can write and run a test or tests that uses the report.json object defined in the Transactions to test S3 functionality using the virtual service

Now, let's create a virtual service that a tester can use for negative testing when defining a test.

16. Click the Add button next to **Virtual Services**
17. Name the virtual service "AWS Testing", add no Transactions, and click **Save**
18. Click **Run Virtual Service**. The AWS Testing virtual service is running and available. Now, when a tester needs a virtual service to test AWS S3, they can reference the virtual service and an associated Template within the test
19. Create a test in BlazeMeter, or update an existing test. Access the Configuration screen
20. Enable the **Virtual Services Configuration**
21. Click Add, and select the virtual service you created and the Template that contains the negative testing scenarios. The virtual service is now built into the test and will include all of the Transactions in the negative testing Template
22. Copy the endpoint and redirect the application under test to use the virtual service endpoint in place of the live service before running the test

---

## Create a Virtual Service for Testing a Web Application

This tutorial shows an end-to-end scenario for testing a digital banking application, using virtual services to simulate a third-party service.

The example application for this tutorial is called Digital Bank, and it represents a simple web interface for online banking, built as a basic Java app.

The Digital Bank application, like any other application, uses third party components wherever possible. One such third party service enables the functionality that lets users search for a banking location based on zip code. The service is a third-party API that the application connects to based on the API URL, which is defined in the application's properties file.

Testing is a continuous exercise, and interruptions in third-party services or costs associated with testing against the API should not be blockers.

This scenario assumes a situation where the API service unexpectedly becomes unavailable. Were this a common occurrence, perhaps a virtual service would already be available as a Template. But this situation is not common, and with a release looming, testing against the API is an operation that can't wait. Now, let's see how BlazeMeter helps you mitigate this situation in minutes to complete critical testing without being affected by constraints.

**Follow these steps:**

1. Locate a source of Transaction data for the live service. For this tutorial, assume that you have a HAR file with a couple of example ATM searches. If you do not have a file available, access the Swagger specification for the API and download it as a JSON file
2. Open BlazeMeter, click the **Service Virtualization** tab, and select **Asset Catalog**
3. Drag the HAR file onto the upload box. The **Import Transactions** dialog opens
4. Type 'ATM Search', and click **Add Service**
5. Add a tag named ATM, and press Enter. You can add tags now to automatically tag all Transactions that you import. Tags can help you find Transactions within a large service. As you add more Transactions to the ATM Search service over time, you can give the Transactions more specialized tags
6. Click **Import**. The Transactions in the HAR file are imported into the repository
7. Filter the Transactions view by the newly created ATM Search service. You can now see the two transactions imported from the HAR file into the ATM Search service
8. Expand the first transaction. For reuse and sharing, it's important that you give all entities unique names
9. Give the transaction a meaningful name and description. Add a 'positive' tag to denote that the URL should return a positive result
10. Examine the URL in the **Request Matcher** field. This Transaction sends a simple GET request to the API. The **Query Parameters** section shows that this Transaction searches specifically for 94203, and the response data shows that two ATM locations match the query. You are happy with this Transaction and will use it for your ATM search acceptance test

You typically add more Transactions to the Service over time. For example, you will go back and cover other scenarios for the service, such as an invalid zip code, a partial match zip code, and more. For this tutorial, because the goal is to quickly verify that the API is working, you move forward with a single Transaction.

11. Go to the **Virtual Services** tab and click the **Add** button next to **Virtual Services**
12. Give the virtual service a meaningful name and description, select the ATM Search Service, and move the single Transaction in the service to the right pane
13. Click **Save**
14. Click **Run Virtual Service**. When the virtual service status is Running, that means that BlazeMeter has created an endpoint containing the Transactions previously defined in your virtual service for you to run your tests against
15. Click the icon next to the Endpoint field to copy the endpoint of the virtual service to your clipboard. To test against the virtual service, you have to redirect the Digital Bank application to call the virtual service instead of the real one. This step is required for any application, but will differ based on the application architecture and which service you are redirecting. The Digital Bank stores the ATM Search connection information in a properties file
16. Open the `application.properties` file for the Digital Bank, find the `io.demo.bank.atm.host` section, add a new line with the virtual service endpoint, uncomment the new line and comment out the line with the live service URL, and save the file
17. Restart the Digital Bank application. The Digital Bank is now running against the virtual service. At this point, any testing of the ATM search functionality will return results based on the Transactions in the virtual service. A search for 94203 returns the two results stored in the Transaction. Other searches might not return meaningful results, because the virtual service only has a single Transaction

This tutorial showed how you can quickly provision a virtual service to remove testing constraints and help your testing keep up with the speed of your application delivery pipeline.

---

## Create a Virtual Service for Third Party Login Services

Modern applications typically provide multiple options for authentication, almost always including options for logging in using common third party systems. Some apps even completely bypass native authentication and rely heavily on login from third party sources to grant access to their applications. In this scenario, thorough testing of application flows that use third party login services becomes vital to ensuring an easy and error free login experience for customers.

BlazeMeter includes sample Transactions for two common third-party login services:
- **Facebook**
- **Salesforce**

These providers maintain public APIs that control login to a remote application using valid credentials for their service. During application testing, there are scenarios where you would want to avoid hitting the real service and perform thorough login testing using a virtual service that simulates these public APIs. For example, you might want to virtualize the service when you are performance testing your application so that you can focus on the performance of the natively built services of your application.

The prebuilt Transaction bundles in BlazeMeter let you virtualize a service that controls access to your application through either Facebook or Salesforce login. The Transactions include the basic API requests, common positive and negative test scenarios, and common query parameters that you can customize based on the needs of your application.

Let's consider a sample scenario where your application leverages the Salesforce Login API for authentication. You need to create a virtual service to test your application login, which will require hitting the Salesforce APIs.

**Follow these steps:**

1. Click the **Service Virtualization** tab, and click **Asset Catalog**
2. In the **Filter by Service** drop-down list, select **Salesforce Login Sample**
3. Examine the available Transactions. Out of the box, BlazeMeter includes the following:
   - Successful requests to the Salesforce Authorization and Access Token APIs
   - Unsuccessful requests to the Salesforce Authorization and Access Token APIs that fail for common reasons, including:
     - Invalid Client ID
     - Invalid Redirect URL
     - Expired Authorization code
     - Invalid client secret
4. Find the '**Salesforce authorization token API with valid parameters**' Transaction, and click the clone icon at the right of the Transaction row
5. Expand the newly created Transaction, which will have the same name appended by the phrase 'Cloned at <timestamp>'
6. Expand the Service drop-down list, and type the name of a new service to contain your duplicated transactions. For this example, we will use **My Salesforce Application** for the service name
7. Click **Add Service**. The new service is created
8. Click **Save**. The cloned Transaction is moved to the **My Salesforce Application** service
9. Repeat Steps 4-5 to clone the positive **Salesforce Access Token API** Transaction, and any of the negative Transactions that you require. Instead of creating a new service, assign them to the **My Salesforce Application** service that you already created and click **Save**. You should now have copies of all of the Salesforce Transactions that you need in your own service
10. Clean up the names for each Transaction. Instead of a cloned time stamp, use the name and tags to distinguish your cloned Transactions from the template ones. For example, you could preface or append the Transaction name with your application name, or add a tag with your application name
11. Edit the Transaction request matching parameters as needed. The Transactions were designed to require little to no customization. The query parameters for each required value are configured with regular expressions to match any value, meaning any input to the Transaction within a virtual service will produce the desired result. You can leave the Transactions as is with broad criteria, or you can update the parameter values to be more specific to your application, with its Client ID, Redirect URL, and other values. If you do that, exercise the live service so that you can copy in appropriate responses for your updated Transactions. For this scenario, we did not edit the default request matching criteria or responses
12. Click the Virtual Services page, and create a new template. Name the template **Successful Salesforce Login**. Select the Transactions from the Catalog pane on the left, then click the right arrow icon to move them to the Transactions in the Template pane on the right. Both Transactions would be required for a successful login, because the Salesforce Login API requires both to pass through to the integrated application
13. Create a new template that collects all of the negative Salesforce login Transactions

You now have templates for positive and negative scenarios that you can add to a virtual service at any time to simulate successful or unsuccessful Salesforce logins to your application during your testing. In this example, any call to the APIs virtualized by the Transactions will return the desired result, because of the broad matching criteria. This configuration is useful if you simply want to ensure the desired response for login during testing without consistently hitting the public API. The Transactions are fully customizable and can easily support more complex scenarios, as well.

---

## Using Test Data with Service Virtualization

Virtual Services often reference data parameters, such as user names, properties, ids, or numeric values. You can either hard-code these values -- or parameterize the virtual service with different variable values.

**Use when**: Using test data with Service Virtualization, parameterizing virtual services with data entities, or creating data-driven virtual services.

### Overview

You can associate transactional virtual services with Service Data Entities that can contain the following sources of test data:

- Synthetic data
- Comma Separated Values (CSV) files
- or a combination of the above

Transactional virtual services can also share their Service Data Model with GUI Functional tests and Performance tests that have the virtual service associated with them.

### Example Use Cases

For example, as a tester, you want to use test data in your GUI Functional or Performance tests. If these tests also rely on virtual services, the test cases expect the same data values in the virtual service's responses. You wouldn't want to hard-code all possible responses as virtual service transactions. By parameterizing the request matcher and response, you can ensure that the data returned by the virtual service (the Service Data Model) is consistent with the data that drives the test (the Test Data Model):

- **Use Case #1 - Stand-alone virtual service:** Support for test data is beneficial in the stand-alone case where the virtual service is not directly related to a test, but returns responses in a look-up approach driven by CSV files. The service data can be statically provided or synthetically generated.
- **Use Case #2 - Virtual service as part of a test:** When a virtual service is associated with a test, its service data model becomes available in the test's Test Data pane.

### Features

- Parameterize the request matcher and the response with dynamic test data loaded from data entities. Data-driven matching is supported only for certain request matchers, such as "equals".
- Define which data models to use for a particular configuration of virtual service.
- Define data models and data size for virtual services, and also for Virtual Service Templates.
- Preview and download test data.

### How to Create Data-Driven Virtual Services

1. Open or create a virtual service with transactions
2. Add service data to the transactions
3. Configure data settings
4. Run the virtual service
5. (Optional) Add data-driven virtual services to tests

### Add Service Data to Transactions

The virtual services' equivalent of the Test Data pane is the Service Data pane. A Service Data Model contains one or more Data Entities. You can create several data entities, each of which can contain, for example, CSV files or other data parameters.

**To add Service Data to transactions:**

1. Go to the **Service Virtualization** tab.
2. Open **Asset Catalog > Transactions**.
3. Click **Service Data**. The **Service Data** pane opens on the right side.
4. Select a service.
5. Click the Ellipsis button and click **Add Data Entity**.
6. Parameterize the transaction by defining data parameters: Click the Plus button next to the data entity and **Create a New Data Parameter**, or attach a **CSV File**.
7. Click **Copy parameter name to clipboard** on a parameter that is used as identifier.
8. Replace a hard-coded identifier value in the **Request Matcher** and in the **Response** with the pasted parameter name.
9. (Optional) Copy and paste additional parameters as needed.
10. Run the virtual service.

### Configure Data Settings

On the **Service Virtualization** tab, click **Virtual Services**. Open a virtual service and go to its **Data Settings** tab. Data Settings are the same as for other test types.

If a CSV file is attached, BlazeMeter uses all rows by default. If only synthetic data is defined, it generates one row of synthetic data by default. You can either define the number of data rows used as a number, or as the number of rows from CSV files -- just as for the other test types.

### Add Data-Driven Virtual Services to Tests

If the virtual service is to be part of a GUI Functional or Performance test, override the parameters in the Test Data Model with values from the Service Data Model.

**To add a data-driven Virtual Service to a test:**

1. Open a Performance or GUI Functional test.
2. Scroll down in the **Test Configuration** to the **Virtual Services Configuration** section.
3. Click the blue Plus button and add a virtual service to the test.
4. Open the **Test Data** pane and scroll down to the **Service Data Model**. The **Service Data Model** from the virtual service and the **Test Data Model** from the test appear one after the other in the **Test Data** pane.
5. For each parameter, click **Copy parameter name to clipboard** and replace a hard-coded value.

### Preview and Download Test Data

1. On the **Service Virtualization** tab, click **Virtual Services**.
2. Open a running virtual service and go to its **Data Settings** tab.

The **Data Settings** tab displays a preview of the current test data for this virtual service, so you see which data is being used. The preview has a 100 row limit; to review all rows, download the CSV file.

Click the **Download** button above the preview to save a copy of the current test data as a CSV file to your local machine.

### Supported Request Matchers

Data-driven matching is supported only for the following request matchers:

- Equals
- Equals ignore case
- Equals to json (Accepts parameters only in the value, not as the key)
- Matches json
- Equals to xml (Accepts parameters only in the node value, not as the node name)
- Matches xml
- Url equals

For query parameters, headers, and cookies, you can use data parameters only in the value fields. You can use several parameters in a single value, such as "order created ${date} at ${time}".

### Limits

The maximum size of the test data that you can use with virtual services is limited. The limit for the data file is 100MB. You can estimate the size of your data file by multiplying the number of columns times the number of rows times the size of the cell content.

A second limit is the time for deployment. Each part of the deploy process has a 5-minute time limit. If any step in the deployment exceeds this time limit, the whole deployment fails.

### Documentation References

For detailed information about using test data with Service Virtualization, use the BlazeMeter MCP help tools:

**Using Test Data with Service Virtualization**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-test-data`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-test-data"]}`

---

## Make SQL Queries Against Service Data

When using test data for Service Virtualization, you sometimes have the requirement to create more complicated data manipulations when using multiple Service Data models. Service Data models are stored as standard SQL tables and you can run standard SQLite queries against test data, such as JOINs, GROUP BY, filtering, subqueries.

**Use when**: Creating complex data manipulations with multiple Service Data models, running SQL queries against service data, or creating custom views from multiple data tables.

### Example Scenarios

You have one Service Data table `profiles_view` containing columns named email and role. You want to use this Service Data in your transactions, but you want to exclude rows with user data for admins. You accomplish this with a standard SQLite query:

```sql
SELECT * FROM profiles_view WHERE email = "${request.query.email}" AND role <> "Admin"
```

Or maybe you have two Service Data tables, `users` and `user_profiles` as Service Data, and you want BlazeMeter to create the view `profiles_view` that contains joined columns from both tables. In this case, you can enter a custom SQL bootstrap script to create this custom view.

### Prerequisites

1. Log in to BlazeMeter and go to the **Service Virtualization** tab.
2. Create your transactions and virtual services.
3. Define Service Data tables and reference the variables in transactions.

### Define Your SQL Bootstrap Script

You can associate multiple Service Data models with a Service. Either use them as is in your virtual services, or optionally, write a Bootstrap Script to create custom views.

1. Go to the **Virtual Services** tab and open a virtual service.
2. Open the **Data Settings** tab.
3. In the **Test Data Implementation** section, choose *one* of the following options:
   - **Default NO-SQL** - BlazeMeter generates a default SQLite query. You can edit the query in the **SQL Hint** tab if needed.
   - **SQL (with bootstrap script)** - Write a custom SQLite query to create a view from multiple Service Data models.

### Define Your Query

1. Go to the **Asset Catalog** tab and open the transaction.
2. Go to the **SQL Hint** tab.
3. Review the default SQLite query. BlazeMeter automatically generates a SQLite query based on the Request field of the transaction.
4. Edit this default SQLite query to create your custom complex SQLite query.

### Define Your Response

1. Go to the **Asset Catalog** tab and open the transaction.
2. Go to the **Response > Body** tab.
3. Define the response body by calling a SQLite query, for example:

```
${#each (sql 'SELECT * FROM users WHERE id > 10') as |user| }
  name: ${user.name}, email: ${user.email}
${/each}
```

### Documentation References

For detailed information about making SQL queries against service data, use the BlazeMeter MCP help tools:

**Make SQL Queries Against Service Data**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-test-data-sql-tables`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-test-data-sql-tables"]}`

---

## How to Integrate Virtual Services and Test Data with LoadRunner Tests

Read this practical guide to learn how to use BlazeMeter virtual services in LoadRunner and how to generate synthetic test data on-demand for use in LoadRunner.

**Use when**: Integrating BlazeMeter virtual services with LoadRunner tests, generating synthetic test data for LoadRunner, or using virtual services in LoadRunner performance tests.

### How to Use BlazeMeter Virtual Services in LoadRunner

Other than actually running the test from LoadRunner Pro, there are merely three things you'll need to take care of:

1. Create the virtual services in BlazeMeter.
2. In LoadRunner, in the **Init Action** step, spin up the virtual services.
3. In LoadRunner, in the **End Action** step, stop the virtual services.
4. Point the app-under-test or test script to the virtual service. You are running your LoadRunner test while utilizing BlazeMeter Service Virtualization to virtualize your dependencies.

### LoadRunner Sample Scripts

In the sample script below:

- Replace `<workspaceId>` with the workspace ID your BlazeMeter virtual services resides in.
- Replace `<mockId>` with the ID of our BlazeMeter virtual service.
- Replace `{auth token}` with a Base 64 encoding of your BlazeMeter API key id:secret pair.

**To start the service:**

Use the LoadRunner script to call the BlazeMeter API to deploy the virtual service. The script should:
1. Add the Authorization header with your Base64 encoded API key pair
2. Make a GET request to `https://mock.blazemeter.com/api/v1/workspaces/<workspaceId>/service-mocks/<mockId>/deploy`
3. Extract the tracking URL from the response
4. Poll the tracking URL until the status is "FINISHED"
5. Wait for the service to be ready

**To stop the service:**

Use the LoadRunner script to call the BlazeMeter API to stop the virtual service. The script should:
1. Add the Authorization header with your Base64 encoded API key pair
2. Make a GET request to `https://mock.blazemeter.com/api/v1/workspaces/<workspaceId>/service-mocks/<mockId>/stop`
3. Extract the tracking URL from the response
4. Poll the tracking URL until the status is "FINISHED"

### How to Generate a Data Set On-demand With Test Data for LoadRunner

1. Create your shared data model in BlazeMeter.
2. Go to the **Test Data** tab and copy the data model ID in BlazeMeter.
3. Create a scenario in the LoadRunner Controller and create two groups. The first group is the "starter" script that fetches the generated data from BlazeMeter. The second group is the script that will make use of the generated data.
4. To set up the "starter" test, add the following script in your VuGen Init Action:
   - Set the Basic Authorization header with your base64 encoded apiKeyId:apiKeySecret
   - Make a POST request to `https://tdm.blazemeter.com/api/v1/workspaces/{workspaceId}/datamodels/{Your_Data_Model_ID}/generatefile?entity=default`
   - Save the response to a CSV file
5. Run the Init and view the data set values in the log viewer in VuGen.
6. Parameterize your second script (your actual test) with variables that you pull from the CSV file.
7. Set the scenario in the LoadRunner Controller to schedule the test by groups (one group per script), and set the second group to run when the first group finishes.

You've successfully set up a test in LoadRunner while utilizing BlazeMeter synthetic data generator to incorporate dynamic test data in your performance test.

---

## Virtualize Message Queues

Virtualize message queues using BlazeMeter Service Virtualization to simulate IBM MQ components (queue managers, queues, channels) for testing, development, or integration purposes.

**Use when**: Virtualizing message queues when the actual IBM MQ infrastructure is unavailable, too costly, or impractical to use during development or testing phases.

### Introduction to Messaging Service Virtualization

Messaging Service Virtualization simulates the behavior of IBM MQ components (e.g., queue managers, queues, channels) to mimic real-world scenarios for testing, development, or integration purposes. This is particularly useful when the actual IBM MQ infrastructure is unavailable, too costly, or impractical to use during development or testing phases.

With BlazeMeter Service Virtualization, your application under test does not need to communicate through the live message broker during the test. A Messaging Runner virtual service gives you deterministic control over requests and responses and their timings. You attach message recordings to virtual services just as you attach transactions.

### Supported Features

To run automated tests against applications that rely on MQs, you can choose to virtualize the messaging. Supported messaging protocols:

- **IBM WebSphere MQ 9.4+**
- **Apache ActiveMQ Classic 6+**
- **Apache ActiveMQ Artemis 2+**

Supported environment:
- Docker
- Kubernetes

Supported messaging architectures:
- **Point-to-Point**: Producer sends message to Queue with destination Consumer
- **Publish-Subscribe**: Publisher sends message to Topic, Subscribers receive copies
- **Request-Reply**: Requester sends message to Request Queue, Responder acknowledges on Reply Queue

### Create a Messaging Runner

Create a virtual service and configure it as Messaging Runner:

1. Open the **Service Virtualization** tab
2. Click the **Plus** button and select **Create from Transaction**. A new virtual service is created
3. Define **Name**, **Description**, **Service**, and **Endpoint Protocol**, as with any virtual service
4. Under **Location**, select your Private Location that has Service Virtualization enabled
5. Under **Runner**, select **Messaging Runner** to enable messaging support
6. Enable **Runner Active** to be able to configure the Runner
7. Go to the **Broker Configuration** tab and configure:
   - **Broker Type**: Embedded or External (External for all protocols, Embedded for ActiveMQ only)
   - **Messaging Protocol**: IBM_MQ9_JMS, IBM_MQ9_NATIVE, ACTIVE_MQ_CLASSIC, or ACTIVE_MQ_ARTEMIS
   - **Hostname**, **Port**, **Channel**, **Queue Manager**, **Username**, **Password**
   - **Use SSL Authentication** (optional)
8. On the **Queues** tab, click the **Plus** button to define your queues
9. On the **Topics** tab, click the **Plus** button to define your topics
10. Go to the **Flows** tab and click the **Plus** button to configure flows (reusable configurations for message transmission)
11. Go to the **Recordings** tab and assign recordings. If you have no recordings yet, create message recordings now
12. Click **Update**. The MQ-enabled virtual service is saved

### Virtualize Message Recordings

BlazeMeter can mock different protocols within the same Service Virtualization environment, including simulating the behavior of IBM Message Queue (MQ) components when the actual IBM MQ infrastructure is not available during testing. You virtualize MQ transactions by recording messages from your live message broker.

**Option 1: Record Live Messages**

1. Configure your MQ to run against the virtual queues that you have defined
2. Open the **Service Virtualization** tab and edit the Messaging Runner virtual service
3. Go to the **Runner** tab and switch **Recording Mode** on
4. Go to the **Recording Configuration** tab
5. Under **Settings**, configure Max Message Count and Max Messages per Second
6. Under **Bindings**, click the **Plus** button to add mappings (map virtual inbound queue/topic to live outbound queue/topic)
7. Click **Save**
8. Click **Start Recording**
9. Run your MQ against the virtual queues and make requests
10. Click **Stop Recording** when you have recorded enough messages
11. Click **Save Recording**. The message recording is saved in the **Asset Library**
12. Go to the **Runner** tab and switch **Recording Mode** off

**Option 2: Create Message Recordings Manually**

1. Open the **Service Virtualization** tab
2. Click **Asset Catalog** and go to the **Recordings** tab
3. Select a **Service**
4. Click the **Plus** button to create a **Message Recording**
5. Define Name, Description, Service, and Tags
6. Click **Save**
7. Click the **Plus** button to add a new Message
8. Define Name, Correlation ID, Message Type, Delay, Destination name, Destination Type, Body, Header matchers, and Properties
9. Click **Save**

### Convert Recordings to Transactions

If you are virtualizing request-reply pairs, convert recordings to sets of transactions. This conversion involves grouping messages by their correlation ID, which are then split into pairs.

**Follow these steps:**

1. Open the **Service Virtualization** tab
2. Click **Asset Catalog** and go to the **Recordings** tab
3. Identify the recordings that you want to convert
4. Set or update correlation IDs manually as needed. The converter converts only messages with correlation IDs
5. Under **Actions**, click the **Convert to transaction** button
6. Assign the transactions to the virtual service as usual

### Messaging Service Virtualization FAQ

**Does a virtual service with a Messaging Runner expose a port?**

If the virtual service includes only a single enabled messaging runner that does not have an Embedded Broker, it does not expose any port. The messaging runner with External Broker functions solely as a client for the broker.

**Do HTTP Runners and Messaging Runners share the same dataset snapshot?**

Yes, both runners operate on the same dataset snapshot. Any state update actions performed in one runner's transaction will be visible in the other runner's transaction.

**How many requests per second can the Messaging Runner handle?**

Performance varies based on the protocol used. When using the IBM_MQ9_JMS protocol, runners processed approximately 400 requests per second, while those using the IBM_MQ9_NATIVE protocol achieved around 760 requests per second.

**Which messaging protocol should I choose?**

- **IBM_MQ9_JMS**: Recommended when using standard JMS interfaces, JMS message types (STREAM_MESSAGE, OBJECT_MESSAGE, MAP_MESSAGE)
- **IBM_MQ9_NATIVE**: Recommended when using MQ9 native interfaces, need to match specific MQMD headers, or need to respond using specific MQMD headers

### Documentation References

For detailed information about messaging service virtualization, use the BlazeMeter MCP help tools:

**Messaging Service Virtualization - Concepts**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-mq-concepts.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-mq-concepts.htm"]}`

**Virtualize Message Queues**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-mq-messaging.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-mq-messaging.htm"]}`

**Virtualize Message Recordings**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-mq-recording.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-mq-recording.htm"]}`

**Messaging Service Virtualization FAQ**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-mq-faq.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-mq-faq.htm"]}`

---

## Managing Sensitive Data Securely with Secrets

Use secrets to manage sensitive data securely in virtual services, such as passwords, tokens, credit card numbers, or any other data that shouldn't be exposed.

**Use when**: Managing sensitive data in virtual services, avoiding hard-coded sensitive data in test scripts, or securing credentials and tokens in virtual service configurations.

### Overview

Secrets are objects that contain sensitive data, such as passwords, tokens, credit card numbers, or any other data that shouldn't be exposed. By using secrets, you do not have to hard code any sensitive data into your test scripts. Whenever an enabled secret appears in reports or logs during and after run time, the value of the secret is replaced with asterisks (*).

To use secrets, you need to create them in your Workspace settings. To learn more about how to create secrets in your workspace, see [Create and Manage Secrets](https://help.blazemeter.com/docs/guide/administration-secrets.htm).

### Best Practices

- Only production and non-sensitive secrets are used
- All secrets are strictly limited in scope and privilege, and access only test-specific resources or data
- Secrets should be temporary and rotated regularly
- Avoid the use of secrets that provide access to production environments or sensitive customer data

### Use Secrets in Your Virtual Services

Once you have your secrets configured in your workspace settings, you can use them in your Virtual Services. You can reference a configured secret using the prefix **BZM_SECRET**.

**Syntax:**
```
${BZM_SECRET.secretname}
```

**Example:**
```
${BZM_SECRET.api_key}
${BZM_SECRET.database_password}
```

### Documentation References

For detailed information about managing secrets in virtual services, use the BlazeMeter MCP help tools:

**Managing Sensitive Data Securely with Secrets**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-secrets.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-secrets.htm"]}`

---

### Documentation References

For detailed information about integrating virtual services and test data with LoadRunner tests, use the BlazeMeter MCP help tools:

**Integrate Virtual Services and Test Data with LoadRunner Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-test-data-loadrunner`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-test-data-loadrunner"]}`

---

## Documentation References

For detailed information about virtual services, use the BlazeMeter MCP help tools:

**Virtual Services**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `mock-service-create-first` (create first)
  - `mock-service-create` (create service)
  - `mock-service-run` (run virtual service)
  - `mock-service-add-to-test` (add to test)
  - `mock-service-create-for-AWS-testing` (AWS testing tutorial)
  - `mock-service-create-for-testing-web-application` (web application tutorial)
  - `mock-service-create-for-third-party-login-services` (third party login tutorial)
  - `mock-service-on-private-locations` (private locations)
  - `mock-service-embed-in-taurus-script` (Taurus integration)
  - `mock-service-mq-concepts.htm` (messaging concepts)
  - `mock-service-mq-messaging.htm` (virtualize message queues)
  - `mock-service-mq-recording.htm` (virtualize message recordings)
  - `mock-service-mq-faq.htm` (messaging FAQ)
  - `mock-service-secrets.htm` (managing secrets)
  - `mock-service-template-create` (create template)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-create-first", "mock-service-create", "mock-service-run", "mock-service-add-to-test", "mock-service-create-for-AWS-testing", "mock-service-create-for-testing-web-application", "mock-service-create-for-third-party-login-services", "mock-service-on-private-locations", "mock-service-embed-in-taurus-script", "mock-service-mq-concepts.htm", "mock-service-mq-messaging.htm", "mock-service-mq-recording.htm", "mock-service-mq-faq.htm", "mock-service-secrets.htm", "mock-service-template-create"]}`

**Environment Variables**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-configurations`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-configurations"]}`

**Test Data Integration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `mock-service-test-data` (using test data)
  - `mock-service-test-data-sql-tables` (SQL queries)
  - `mock-service-test-data-loadrunner` (LoadRunner integration)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-test-data", "mock-service-test-data-sql-tables", "mock-service-test-data-loadrunner"]}`

