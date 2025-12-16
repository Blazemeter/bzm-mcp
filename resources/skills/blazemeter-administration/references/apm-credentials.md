# APM Credentials Management

## Administration Creating APM Credentials

You can integrate application performance monitoring (APM) tools into your workspace using credentials. APM credentials consist of the authentication details (such as API keys, access tokens, or secret keys) required to securely connect BlazeMeter to your APM (Application Performance Monitoring) tool. These credentials authorize BlazeMeter to retrieve performance data from the connected APM system.

Credentials can be shared across multiple APM profiles to streamline configuration and ensure consistency.

**Use when**: Creating and managing APM credentials for integrating APM tools into BlazeMeter workspaces or when setting up AppDynamics, CloudWatch, Datadog, DX APM, Dynatrace, or New Relic integrations.

### Supported APM Tools

- **AppDynamics**: Application performance monitoring
- **CloudWatch**: AWS cloud monitoring
- **Datadog**: Infrastructure and application monitoring
- **DX APM**: CA Application Performance Management
- **Dynatrace**: Full-stack monitoring
- **New Relic**: Application and infrastructure monitoring (APM and Infrastructure)
- **New Relic Insights**: For API Monitoring integration

### Add APM Credentials

To add APM credentials, follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. Go to **Settings** > **Workspace** > **APM Credentials**
2. Click the < + > symbol
3. Select the APM tool of your choice
4. Enter the credential settings for the selected APM (see detailed configuration below)
5. Click **Validate**, then **Next**
6. The credential is created

Once your APM credentials are added, they will appear in the list below along with a confirmation message.

**Note**: When you have completed the form for any APM tool, click **Validate**, then **Next**. The credential is created. For more information about specific integrations, see the integration guides listed in the Documentation References section below.

### Overview

You can integrate application performance monitoring (APM) tools into your workspace using credentials. APM credentials consist of the authentication details (such as API keys, access tokens, or secret keys) required to securely connect BlazeMeter to your APM (Application Performance Monitoring) tool. These credentials authorize BlazeMeter to retrieve performance data from the connected APM system.

Credentials can be shared across multiple APM profiles to streamline configuration and ensure consistency.

### Credential Configuration by Tool

#### AppDynamics

The AppDynamics integration connects to an AppDynamics Controller to retrieve configuration data and send back information about the monitored environment. Fill in the following fields:

- **Credential Name**: A unique name for the credential, without spaces or special characters
- **Private Location ID (Optional)**: A unique key associated with a private location that can be found under **BlazeMeter Settings** -> **Workspaces** -> **Private Locations** -> <Your Private Location> -> **Private Location Details**, under the **Id** column
- **Controller Host**: The hostname or IP address of the AppDynamics Controller, for example, 192.168.1.22 or myhost or myhost.abc.com. This is the same host used to access the AppDynamics browser-based user interface
- **Controller Port**: The port on which the Controller listens for integration traffic
- **Choose Authentication Method**: Either **Username/Password** or **Access Token**
  - **Username/Password**:
    - **Account Name**: The name of the account listed in the Controller
    - **Username**: The name of the user listed in AppDynamics
    - **Access Key**: A unique key associated with the Controller account
  - **Access Token**:
    - **Access Token**: A unique key associated with the Controller account, generated in AppDynamics either from the Controller UI or through an API

#### CloudWatch

Enter your new CloudWatch IAM Key details:

- **IAM Key Name**: Enter a unique name for this credential. This name will help you identify the key later. Avoid using special characters or spaces
- **IAM Access Key ID**: Enter the Access Key ID provided when creating your IAM user in AWS
- **IAM Secret Access Key**: Enter the secret access key associated with the Access Key ID. Copy it directly from AWS when creating the IAM user, as it will not be displayed again. Avoid storing the secret key in insecure locations

#### Datadog

Fill in the following fields:

**Basic Configuration:**
- **Key Name** - Name of the key you want to create and reference in BlazeMeter
- **Datadog APM URL** - The full URL to access your Datadog environment (exclude the trailing / in your URL, for example, http://yourHostAtDatadog.com)
- **App Key** - Authentication key, used in conjunction with your organization's API key, that gives users access to Datadog's programmatic API
- **API Key** - Authentication key granting BlazeMeter access to Datadog's API for data transmission and retrieval. API keys are unique to your organization. An API key is required by the Datadog Agent to submit metrics and events to Datadog

**Advanced Configuration:**
- **Private Location ID** - The private location to use to run the APM functionality (for information where to get this value, see [Where can I find the Harbor ID and Ship ID?](https://help.blazemeter.com/docs/guide/private-locations-where-to-find-harbor-id-and-ship-id.html)). If you're using Datadog on the cloud, you don't need to provide the private location ID. The integration will work seamlessly without it

For more information, see [Datadog documentation](https://docs.datadoghq.com/).

#### DX APM

This configuration supports two-way integration between DX APM and BlazeMeter. Fill in the following fields:

- **Configuration name** - A name for the configuration to be used in BlazeMeter
- **DX APM Security Token** - A token created in DX APM
- **DX APM URL** - The URL for accessing the DX APM Webview or the DX APM Team Center (without the port number)

**Advanced Settings:**
- **Port number for DX APM Webview/DX APM Team Center** - If the port is not provided, the default value 8080 is used
- **Port number for metrics API** - Port number for DX APM metrics API. If no port number is provided, the default value 8081 is used
- **Private Location ID** - Leave empty
- **Filter for DX APM Agents that show up in the BlazeMeter report** - Enter a regular expression. If not, all agents are selected

#### Dynatrace

This configuration supports integration between Dynatrace and BlazeMeter. Fill in the following fields:

**Basic Configuration:**
- **Key Name** - Name of the key you want to create and reference in BlazeMeter
- **Environment ID** - The full URL containing your environment ID (Exclude the trailing / in your URL, for example, http://yourHostAtDynatrace.com)
- **Token** - Access token for your DynaTrace environment

**Advanced Configuration:**
- **Private Location ID** - The ID of the Private Location to use to run the APM functionality (see [here](https://help.blazemeter.com/docs/guide/private-locations-where-to-find-harbor-id-and-ship-id.html) for where to get this value). If you're using DynaTrace on the cloud, you don't need to provide the Private Location ID. The integration will work seamlessly without it

#### New Relic

This configuration supports integration between New Relic APM and BlazeMeter. Fill in the following fields:

- **Select which New Relic API key to use**: Select **Create a new New Relic API Key**
- **New Relic key title**: Type a name for your New Relic API key
- **New Relic API key**: Paste your New Relic REST API key

#### New Relic Infrastructure

This configuration supports integration between New Relic Infrastructure APM and BlazeMeter. Fill in the following fields:

- **Select which New Relic Insights API query key to use**: Select **Create a new New Relic Insights API Query Key**. Insights was the name for the New Relic product that previously governed the reporting of custom events, and the ability to query and chart New Relic data. These features are now a fundamental part of the New Relic platform and are no longer governed by the Insights product or name
- **Profile Name**: Type a name for your New Relic Infrastructure profile (configuration)
- **Account Id**: Paste your New Relic account ID
- **New Relic Insights API Query key**: Paste your New Relic API query key

#### New Relic Insights

This configuration supports integration between New Relic Insights and API Monitoring. Fill in the following fields:

**Note**: Insights was the name for the New Relic product that previously governed the reporting of custom events, and the ability to query and chart New Relic data. These features are now a fundamental part of the New Relic platform and are no longer governed by the Insights product or name.

- **Credential Note** - Provide a descriptive note for this credential. Use a name or purpose that helps you identify this credential easily, such as *Team A Monitoring*
- **Account ID** - Enter your New Relic account ID. This is the numeric identifier associated with your New Relic Insights account
- **Credential Key** - Enter your New Relic API key. Ensure it is entered exactly as provided by New Relic. The API key authorizes access to Insights data

### Delete APM Credentials

To delete APM (Application Performance Monitoring) credentials in BlazeMeter, follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. In the **Workplace** section, click **APM Credentials**
3. On the **Manage APM Credentials** page, select the table row containing the required credentials, and click the trash can

Once confirmed, the selected APM credential will be permanently deleted from your BlazeMeter workspace.

### Managing Credentials

- **Edit Credentials**: Update API keys or configuration
- **Test Connection**: Use the Validate button to verify credentials are valid before saving
- **Delete Credentials**: Remove unused credentials using the trash can icon
- **View Usage**: See which tests use the credentials

### Security Best Practices

- Rotate API keys regularly
- Use least-privilege access for API keys
- Store credentials securely (encrypted in BlazeMeter)
- Monitor credential usage
- Revoke unused credentials

### Using APM Credentials in Tests

Once created, APM credentials can be selected in:
- Performance test configurations
- APM integration settings
- Test execution profiles

### Troubleshooting

- Verify API keys are valid and not expired
- Check network connectivity to APM service
- Review APM service logs for connection issues
- Validate credential permissions

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Creating APM Credentials**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-creating-apm-credentials`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-creating-apm-credentials"]}`

**Specific APM Tool Integration Guides**:
- **AppDynamics**: `integrations-integrate-with-appdynamics` (Category: `root_category`, Subcategory: `guide`)
- **New Relic APM**: `integrations-new-relic-apm` (Category: `root_category`, Subcategory: `guide`)
- **Datadog**: `integrations-integrate-with-datadog` (Category: `root_category`, Subcategory: `guide`)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-integrate-with-appdynamics", "integrations-new-relic-apm", "integrations-integrate-with-datadog"]}`

---

## Administration Manage APM Profiles

APM profiles are configurations that define how BlazeMeter interacts with an APM tool for a specific test. Profiles specify which credentials to use and additional connection details tailored for specific tests or environments. Profiles act as a bridge between the credentials and individual test scenarios, allowing workspace owners to customize APM integration for each use case.

You can view the profiles created by workspace members and delete as needed.

**Use when**: Managing APM profiles, viewing existing profiles, or when you need to understand how profiles connect credentials to specific tests or environments.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Manage APM Profiles**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-workspace-manage-profiles.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-workspace-manage-profiles.htm"]}`

### View Existing Profiles

To view existing profiles, go to **Settings > Workspace > Profiles**.

### Manage Profiles Page Columns

The following columns appear on the **Manage Profiles** page, detailing their purpose and how they help users monitor and organize their APM profiles:

- **Type**: Indicates the type of APM integration (for example, AppDynamics, Datadog, New Relic)
- **Name**: Displays the name of the profile. Using descriptive names makes it simpler to associate profiles with specific tests or environments
- **Entity Type**: Describes the scope of the integration, such as a workspace-level or test-level entity
- **Entity Name**: Specifies the name of the entity (for example, a specific test, workspace, or other associated objects) the profile is linked to
- **Metrics**: Lists the performance or monitoring metrics associated with the profile (for example, response time, throughput, error rate)

### Delete Profiles

You can delete profiles as needed from the Manage Profiles page. Only workspace members with appropriate permissions can delete profiles.

