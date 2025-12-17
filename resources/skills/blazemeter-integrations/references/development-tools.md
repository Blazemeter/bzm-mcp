# Development Tools

## BlazeMeter Visual Studio Code Plugin

Use BlazeMeter's Visual Studio Code extension for local test creation, validation, execution, and synchronization with BlazeMeter cloud platform.

**Use when**: Using BlazeMeter's Visual Studio Code extension for local test creation, validation, execution, and synchronization with BlazeMeter cloud platform.

### Overview

The BlazeMeter Visual Studio Code extension provides a local development environment for creating and managing BlazeMeter tests. It enables:
- Local test creation and editing
- Test validation before upload
- Local test execution
- Synchronization with BlazeMeter cloud

### What is Visual Studio Code?

Visual Studio Code (VSC) is a free lightweight code editor from Microsoft for building web, desktop, and mobile applications. It is a separate app from the paid MS Visual Studio.

### How to Install the BlazeMeter Extension for VSC

1. Download the BlazeMeter extension from [https://marketplace.visualstudio.com/items?itemName=PerforceSoftware.bzm-vscode-extension](https://marketplace.visualstudio.com/items?itemName=PerforceSoftware.bzm-vscode-extension)
2. Install the .vsix file by double-clicking the file and following the installer. For more information, see [Install without using Extension Manager (microsoft.com)](https://learn.microsoft.com/en-us/visualstudio/ide/finding-and-using-visual-studio-extensions?view=vs-2022#install-without-using-extension-manager)
3. Install Taurus. For more information, see [https://gettaurus.org/install/Installation/](https://gettaurus.org/install/Installation/)
4. Verify that you have the Taurus command line tool `bzt` installed. For more information, see [https://gettaurus.org/docs/CommandLine/](https://gettaurus.org/docs/CommandLine/)

### Features

- **Test Creation**: Create tests locally in VS Code
- **Test Validation**: Validate test scripts before upload
- **Local Execution**: Run tests locally for debugging
- **Cloud Sync**: Synchronize tests with BlazeMeter cloud
- **Test Management**: Manage tests directly from VS Code

### Documentation References

For detailed information about Visual Studio Code Plugin, use the BlazeMeter MCP help tools:

**Visual Studio Code Plugin**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-visual-studio-code-plugin`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-visual-studio-code-plugin"]}`

### How to Configure the BlazeMeter Extension for VSC

Configure the extension by providing your BlazeMeter API credentials and selecting the BlazeMeter project that you want to work with.

After installing the VSC extension, you see the BlazeMeter Settings page.

**To enable VSC to log on to a.blazemeter.com:**

In your browser:
1. Log on to [https://a.blazemeter.com/app/#/settings/api-keys](https://a.blazemeter.com/app/#/settings/api-keys)
2. Click the Plus button to generate an API key. For more information, see [BlazeMeter API keys](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html). Name it, for example, "VSC integration". Define an expiry time
3. Copy the API key and API Secret and store them in a safe place

Return to VSC:
1. Paste the API key and API Secret into the BlazeMeter Extension Settings
2. After the credentials validate, continue defining the extension's Application Settings. Select your BlazeMeter account. Select your BlazeMeter workspace in that account. Select your BlazeMeter project in that workspace
3. Close the Settings window

You now see a BlazeMeter Explorer icon on the left side of the VSC interface.

### How to Use the BlazeMeter Extension for VSC

Open CSV code and open the local folder that contains your tests in the Explorer. Associate a local test with a BlazeMeter project and edit and validate the test locally. Sync the test and run it to generate the report in BlazeMeter.

**To save a local test on the server:**
1. Open a local test in VSC
2. Run the command "BlazeMeter: Create new test." The Command Palette bar prompts you for values
3. Type the response into the Command Palette bar and press Enter to confirm, or press Escape to cancel. **Enter Test Name...**
4. Wait for the extension to set up the new test on the server. A dialog opens and asks whether you want VSC to open an external website. To open the test in the default browser, click **Open**. To copy the URL to paste into another browser, click **Copy**. To not open a browser window, click **Cancel**

**To associate a local test with a BlazeMeter project:**

To get BlazeMeter reporting, you need to associate the test with a project.

1. Open a local test in VSC
2. Run the command "BlazeMeter: Set up BlazeMeter reporting." The Command Palette bar prompts you for values
3. Type each of the responses into the Command Palette bar and press Enter to confirm, or press Escape to cancel:
   - Enter Report Name... For example: My report
   - Enter Test Name... My test
   - Enter Project Name... Default
4. The extension adds the `blazemeter` module to the YAML file

**To execute a local test:**
1. Open the local test in VSC
2. Run the command "BlazeMeter: Launch test locally." Taurus CLI runs the test and opens BlazeMeter in a browser window
3. The report appears in the BlazeMeter web UI under **Reports > Recent test runs**

**To update a local test:**

After you have made local changes, you want to upload the latest version of the test to BlazeMeter:

1. Open a local test in VSC
2. Run the command "BlazeMeter: Sync local folder with test." The Command Palette bar prompts you for values
3. Select the response in the Command Palette bar and press Enter to confirm, or press Escape to cancel. Select the target to which you want to sync files...
4. Run the command "BlazeMeter: Open test link" to view the updated test in the BlazeMeter web UI

The test and its dependencies are updated in the associated BlazeMeter project and in `blazemeter.config.json`.

**To browse tests:**
1. Click the BlazeMeter Explorer icon on the left side of VSC. The explorer has two collapsed sections, Performance tests and Functional tests
2. Expand the sections and type to filter tests by name
3. Select a test and click the action buttons to perform the following tasks:
   - Run the test
   - Open the test in the VSC editor
   - Open the test in the BlazeMeter web UI

**To validate tests:**
1. Browse to and open a test in VSC
2. In the bottom bar, click **Validate BlazeMeter test**
3. Review error messages in VSC

**Note**: Validation helps catch errors before uploading tests to BlazeMeter, saving time and ensuring test quality. The extension provides immediate feedback on test configuration issues.

### Command Reference

In VSC, open the Command Palette and search for "BlazeMeter" to view a list of all integrated commands:
- BlazeMeter: Sync local folder with test
- BlazeMeter: Create a new test
- BlazeMeter: Launch test locally
- BlazeMeter: Open test link
- BlazeMeter: Set up BlazeMeter reporting
- BlazeMeter: Show Settings view

### Best Practices

- Use VS Code extension for local development
- Validate tests before uploading
- Test locally before cloud execution
- Keep tests synchronized with cloud

---

## BlazeMeter MCP Server

Install and configure BlazeMeter MCP Server to connect AI tools to BlazeMeter's performance testing platform, including CLI tool, binary installation, Docker deployment, and custom CA certificates.

**Use when**: Installing and configuring BlazeMeter MCP Server to connect AI tools to BlazeMeter or using CLI tool, binary installation, Docker deployment, and custom CA certificates.

### Overview

The BlazeMeter MCP Server provides programmatic access to BlazeMeter through the Model Context Protocol (MCP), enabling AI tools to interact with BlazeMeter's platform. It supports:
- User management
- Account and workspace management
- Project and test management
- Test execution and results

**Note**: MCP Server is a modular, extensible service that exposes tools, data, and workflows to AI models via the Model Context Protocol (MCP). It acts as a bridge between AI agents and real-world systems, enabling seamless interaction with APIs, databases, applications, and more.

### Use Cases

The BlazeMeter MCP Server is built for developers and QA teams who want to connect their AI tools to BlazeMeter's enterprise-grade performance testing capabilities, from simple test creation to complex multi-step automation workflows.

- **Performance Test Management**: Create, configure, and manage performance tests with automated script uploads and asset management
- **Test Execution & Monitoring**: Start tests, monitor execution status, and retrieve comprehensive reports including summary, errors, and request statistics
- **Workspace & Project Organization**: Navigate through accounts, workspaces, and projects to organize your testing infrastructure
- **Load Configuration**: Configure test parameters including concurrency, iterations, duration, ramp-up settings, and geographic distribution
- **Report Analysis**: Access detailed execution reports, error analysis, and performance metrics for comprehensive test insights
- **Account & Permission Management**: Manage multiple accounts and workspaces with proper AI consent controls and permission validation

### Install BlazeMeter MCP Server

You can deploy BlazeMeter MCP Server locally.

**Installation options:**
- Installation using our interactive CLI tool
- Manual client configuration Binary installation from remote source code
- Docker MCP Client Configuration

**Prerequisites:**
- BlazeMeter API credentials (API Key ID and Secret)
- Compatible MCP host (VS Code, Claude Desktop, Cursor, Windsurf, etc.)
- Docker (only for Docker-based deployment)
- [uv](https://docs.astral.sh/uv/) (a high-performance Python package) and Python 3.11+. Both required only for installation from source code distribution
- BlazeMeter's AI-assisted features require account owner consent. For more information, see [Manage AI Consent](https://help.blazemeter.com/docs/guide/administration-ai-consent.html)

### Configure Your MCP Client with the CLI Tool

1. Get the BlazeMeter API credentials (API Key ID and Secret). For more information, see [BlazeMeter API Keys](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html). When downloading your API keys from BlazeMeter, save the `api-keys.json` file in the same folder where you'll place the MCP binary
2. From the [Releases](https://github.com/BlazeMeter/bzm-mcp/releases) page, download the appropriate binary file for your operating system. Select the binary that matches your OS (Windows, macOS, Linux)
3. Place the binary in the same folder as your `api-keys.json` file
4. Execute or double-click the binary to launch the interactive configuration tool

The tool automatically generates the MCP JSON Key configuration for you.

**Troubleshooting:**

For macOS, you may encounter a security alert "Apple could not verify 'bzm-mcp-macos' is free of malware."

To resolve this issue:
1. Go to **System Settings**, **Privacy & Security**, **Security**
2. Locate the blocked application and click **Allow Anyway**
3. Run the binary again

### Configure the Client Manually (Binary Installation)

1. From the [Releases](https://github.com/BlazeMeter/bzm-mcp/releases) page, download the binary for your operating system
2. Configure your MCP client with the following settings:

```json
{
  "mcpServers": {
    "BlazeMeter MCP": {
      "command": "/path/to/bzm-mcp-binary",
      "args": ["--mcp"],
      "env": {
        "BLAZEMETER_API_KEY": "/path/to/your/api-key.json"
      }
    }
  }
}
```

### Configure the Client Manually (from Remote Source Code)

1. Install uv and Python 3.11+
2. Configure your MCP client with the following settings:

```json
{
  "mcpServers": {
    "BlazeMeter MCP": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/Blazemeter/bzm-mcp.git@v1.0.1",
        "-q", "bzm-mcp", "--mcp"
      ],
      "env": {
        "BLAZEMETER_API_KEY": "/path/to/your/api-key.json"
      }
    }
  }
}
```

The uvx installs and runs the package and its dependencies in a temporary environment. You can change to any version that has been released or any branch you want. Package support for uvx command is supported from version 1.0.1 onwards. For more information on the uv/uvx arguments used, see the official [uv documentation](https://docs.astral.sh/uv/).

**Note**: The uvx command provides a convenient way to run the MCP Server without installing it permanently, making it ideal for testing or temporary deployments.

### Configure the MCP Client for Docker

Use the following settings:

```json
{
  "mcpServers": {
    "Docker BlazeMeter MCP": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount",
        "type=bind,source=/path/to/your/test/files,target=/home/bzm-mcp/working_directory/",
        "-e",
        "API_KEY_ID=your_api_key_id",
        "-e",
        "API_KEY_SECRET=your_api_key_secret",
        "-e",
        "SOURCE_WORKING_DIRECTORY=/path/to/your/test/files",
        "ghcr.io/blazemeter/bzm-mcp:latest"
      ]
    }
  }
}
```

To get the API_KEY_ID and API_KEY_SECRET, see [BlazeMeter API keys](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html).

### Configure Custom CA Certificates in Docker (Corporate Environments)

Use custom Certificate Authority (CA) certificates in Docker when one or more of the following conditions apply:
- Your organization uses self-signed certificates
- You're behind a corporate proxy that performs SSL inspection
- Your environment includes a custom CA
- You encounter SSL certificate verification errors during test execution

Custom CA certificate bundles require the following configuration:
- **Certificate Volume Mount**: Mount your custom CA certificate bundle into the container
- **SSL_CERT_FILE Environment Variable**: Explicitly set the SSL_CERT_FILE environment variable to point to the certificate location inside the container

Example configuration:

```json
{
  "mcpServers": {
    "Docker BlazeMeter MCP": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount",
        "type=bind,source=/path/to/your/test/files,target=/home/bzm-mcp/working_directory/",
        "-v",
        "/path/to/your/ca-bundle.crt:/etc/ssl/certs/custom-ca-bundle.crt",
        "-e",
        "SSL_CERT_FILE=/etc/ssl/certs/custom-ca-bundle.crt",
        "-e",
        "API_KEY_ID=your_api_key_id",
        "-e",
        "API_KEY_SECRET=your_api_key_secret",
        "-e",
        "SOURCE_WORKING_DIRECTORY=/path/to/your/test/files",
        "ghcr.io/blazemeter/bzm-mcp:latest"
      ]
    }
  }
}
```

In the above example, replace:
- /path/to/your/ca-bundle.crt with your host system's CA certificate file path
- The container path /etc/ssl/certs/custom-ca-bundle.crt can be any path you prefer (ensure it matches `SSL_CERT_FILE`)

The `SSL_CERT_FILE` environment variable must be set to point to your custom CA certificate bundle. The `httpx` library automatically respects the `SSL_CERT_FILE` environment variable for SSL certificate verification.

### Best Practices

- Use binary installation for simple setups
- Use Docker for containerized environments
- Configure custom CA certificates for corporate environments
- Secure API credentials properly

### Documentation References

For detailed information about MCP Server, use the BlazeMeter MCP help tools:

**MCP Server**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-mcp-server`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-mcp-server"]}`

---

## BlazeMeter MCP Server Tools

Understand and use BlazeMeter MCP Server tools for user management, account management, workspace management, project management, test management, and execution management.

**Use when**: Using BlazeMeter MCP Server tools for user management, account management, workspace management, project management, test management, and execution management.

### Overview

BlazeMeter MCP Server provides a comprehensive set of tools for managing all aspects of BlazeMeter through programmatic access. These tools enable:
- Automated test management
- Programmatic test execution
- Results retrieval and analysis
- Workflow automation

The BlazeMeter MCP Server provides comprehensive access to BlazeMeter's API through six main tools.

| Tool | Purpose | Key capabilities |
|------|---------|------------------|
| User | User Information | Get current user details, default account/workspace/project |
| Account | Account Management | List accounts, check AI consent, read account details |
| Workspace | Workspace Management | Manage workspaces, get locations, check billing usage |
| Project | Project Management | Organize projects, get test counts, manage project settings |
| Tests | Test Management | Create, configure, and manage performance tests |
| Execution | Test Execution | Run tests, monitor status, retrieve reports |

### User Management

Get information about your BlazeMeter account and default settings.

| Action | What you get |
|--------|--------------|
| Get user info | Your username, default account, workspace, and project IDs |

**Use case:** Start here to get your default account, workspace, and project IDs.

### Account Management

Manage your BlazeMeter accounts and check permissions.

| Action | What you get |
|--------|--------------|
| Get account details | Account information and AI consent status |
| List accounts | All accounts you have access to |

**Use case:** Verify AI consent and access account-level information.

### Workspace Management

Navigate and manage your testing workspaces.

| Action | What you get |
|--------|--------------|
| Get workspace details | Workspace information and billing details |
| List workspaces | All workspaces in an account |
| Get locations | Available test locations for different purposes |

**Use case:** Navigate your testing infrastructure and check available locations.

### Project Management

Organize your tests within workspaces.

| Action | What you get |
|--------|--------------|
| Get project details | Project information and test count |
| List projects | All projects in a workspace |

**Use case:** Organize tests within workspaces and check project statistics.

### Test Management

Create, configure, and manage your performance tests.

| Action | What you get |
|--------|--------------|
| Get test details | Test configuration and current settings |
| Create test | New performance test |
| List tests | All tests in a project |
| Configure load | Set users, duration, ramp-up settings |
| Configure locations | Set geographic distribution |
| Upload files | Upload test scripts and assets |

**Use case:** Create and configure performance tests with scripts and load parameters.

### Execution Management

Run tests and analyze results.

| Action | What you get |
|--------|--------------|
| Start test | Launch a configured test |
| Get execution status | Current test status and details |
| List executions | All executions for a test |
| Get summary report | Test execution summary |
| Get error report | Error analysis and details |
| Get request stats | Request statistics and performance metrics |
| Get all reports | Complete test results (summary, errors, stats) |

**Use case:** Run tests and analyze results with comprehensive reporting.

### Usage Examples

The MCP Server tools can be used through any compatible MCP host (VS Code, Claude Desktop, Cursor, Windsurf, etc.). The tools are accessed through the MCP protocol, allowing AI agents to interact with BlazeMeter programmatically.

**Example Workflows:**

1. **Getting Workspace Information**: Use `blazemeter_workspaces` tool with action `read` and args `{"workspace_id": 12345}` to get workspace details
2. **Listing Tests**: Use `blazemeter_tests` tool with action `list` and args `{"project_id": 67890}` to get a list of tests
3. **Starting Test Execution**: Use `blazemeter_execution` tool with action `start` and args `{"test_id": 11111}` to start a test execution

### Best Practices

- Use MCP tools for automation workflows
- Leverage tools for CI/CD integration
- Use tools for programmatic test management
- Implement error handling for tool operations

---

## ShiftLeft Converter for LoadRunner

Convert LoadRunner or SOAPUI scripts to open-source formats (JMeter, Selenium, Taurus) using the free ShiftLeft Converter tool.

**Use when**: Converting LoadRunner HTTP to JMeter, LoadRunner TruClient to Selenium, or SOAPUI scenarios to Taurus and BlazeMeter.

### Overview

The [Free Script Converter](https://shiftleft.blazemeter.com/) can convert LoadRunner HTTP to [JMeter](http://jmeter.apache.org/) and LoadRunner TruClient to [Selenium](http://www.seleniumhq.org/) in a short time, as well as SOAPUI scenario(s) to [Taurus](http://gettaurus.org/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and [BlazeMeter](http://www.blazemeter.com/signup?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes).

For more information about converting scripts to Selenium, see [Convert LoadRunner to Open-Source Selenium in Minutes](https://www.blazemeter.com/blog/convert-loadrunner-to-open-source-selenium-in-minutes).

### Convert to JMeter

You can convert the tests assuming only HTTP(S) protocols (and derivatives). In LoadRunner terms, these are:

- Web - HTTP/HTML
- Web Services
- RTE
- Winsock
- MQ
- JMS
- Soap

**Prerequisites:**
- You have JMeter installed.

**Follow these steps:**

1. Go to [https://shiftleft.blazemeter.com](https://shiftleft.blazemeter.com/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and upload the ZIP file.
2. Open the test in BlazeMeter and download the zip file that contains all converted assets.
3. Open the downloaded file, and open the folder named "Your JMeter or Selenium Scripts".
4. Copy the JMX file to a folder on your computer.
5. Open the JMX file in JMeter, and adjust the script if you needed, and run it.

### Convert to Taurus

With the Script Converter, you can convert your tests to Taurus, an open-source automation framework. Taurus allows you to run and automate open-source tests and view analytics. For more information about Taurus, see [gettaurus.org](http://gettaurus.org).

**Prerequisites:**
- You have JMeter installed.

**Follow these steps:**

1. Go to [https://shiftleft.blazemeter.com](https://shiftleft.blazemeter.com/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and upload the ZIP file.
2. Open the test in BlazeMeter and download the zip file that contains all converted assets.
3. Copy the YML and .TXT files, and put these in the same folder in your computer. Adjust the YML file in your Text editor of choice, if needed.
4. [Install Taurus](http://gettaurus.org/install/Installation/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) if necessary.
5. Run the command `$ bzt <your_filename.yml>`
6. View and analyze the results.

You just ran your LoadRunner file in Taurus.

### Convert to BlazeMeter

**Prerequisites:**
- You have JMeter installed.

You can convert LoadRunner scripts to BlazeMeter.

1. Go to [https://shiftleft.blazemeter.com](https://shiftleft.blazemeter.com/?utm_source=blog&utm_medium=BM_blog&utm_campaign=convert-loadrunner-to-open-source-jmeter-in-minutes) and upload the ZIP file.
2. Open the test in BlazeMeter and download the zip file that contains all converted assets.
3. Configure your tests from the converted ZIP file, either:
   - Extract the JMX and [create a JMeter test](skill-blazemeter-performance-testing://references/scenarios.md); OR
   - Extract the YML and [create a Taurus test](skill-blazemeter-performance-testing://references/scenarios.md).
4. In BlazeMeter, the "Test History" tab displays various details such as the Test execution engine is used, the number of Concurrent Users/Threads, and the available Locations and providers (AWS, Google, Azure) from where the tests can be executed.
5. Launch the test for the default duration of 20 mins.

You can now view the test results on BlazeMeter.

### Enhance LoadRunner Scripts with AI

After converting LoadRunner scripts, you can use an AI-powered assistant to suggest and apply optimal configurations and assertions to the JMeter YAML scripts. The assistant analyzes each LoadRunner script and takes into account best practices and your plan details (available credits, plan limits, and so on).

**Steps to Enhance with AI:**

1. Go to [https://shiftleft.blazemeter.com](https://shiftleft.blazemeter.com/) and upload your LoadRunner script ZIP file.
2. After conversion, if the converted percentage is less than 100% and your script contains unsupported functions, click **Enhance Conversion**. The script is converted with AI and now shows 100% conversion.
3. Click **Improve Script With AI**.
4. You can select from up to 5 optimal configuration changes and 5 assertion types, tailored to the script's structure and goals. Review, accept, and apply any combination of suggested assertions, and select one configuration update per iteration.
5. (Optional) Click **View Yaml File** to review it or compare to a previous version.
6. Click **Open Test in BlazeMeter**. The YAML file opens in BlazeMeter. You can download, copy, or delete the file.

### Supported Files and Functions (LoadRunner HTTP and TruClient)

The ShiftLeft Converter supports conversion of LoadRunner HTTP to JMeter and LoadRunner TruClient to Selenium. It also supports SOAPUI scenarios conversion to Taurus and BlazeMeter.

**Supported Formats:**
- **DataSources**: All data input files (***.DAT** files) will be migrated to ***.CSV** files
- **TruClient**: Any LR scripts written in **.C** format are supported. Also, **.HAR** files are now supported. Java or VisualBasic code are not supported.
- **SOAP UI**: XML file format, upload in .ZIP file

**TruClient Supported Actions:**
- Navigate, Add Tab, Activate Tab, Close Tab
- Click, Double Click, Verify, Type, Select, Scroll, Wait
- Evaluate JavaScript, If, If2, For, Press Key, Resize
- clearCookies, Drag, WaitForFileDownload
- Dialog - Prompt, Dialog - Confirm, Dialog - Alert
- Set, Set Day, Reload

**HTTP based protocols Supported Functions:**
The converter supports a wide range of LoadRunner HTTP functions including:
- Transaction functions (lr_start_transaction, lr_end_transaction)
- Parameter functions (web_reg_save_param, lr_eval_string)
- Web functions (web_url, web_submit_data, web_custom_request)
- Think time functions (lr_think_time)
- Error handling functions (lr_continue_on_error, lr_abort)
- And many more HTTP, web service, and messaging functions

For a complete list of supported functions, see the documentation.

### Resolve Errors

When using the ShiftLeft Converter, occasionally error messages appear after uploading your LoadRunner script.

**Troubleshooting Steps:**

1. Check that your folder contains the LoadRunner script and relevant files in the *.ZIP file.
2. Review the list of supported files and functions to ensure your script uses supported functions.
3. If conversion percentage is less than 100%, use the **Enhance Conversion** feature with AI to improve conversion.
4. If issues persist, contact [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com) for assistance.

**Common Issues:**
- Unsupported functions: Use AI enhancement to convert unsupported functions
- Missing files: Ensure all required files are included in the ZIP
- Format errors: Verify file formats match supported types

### Documentation References

For detailed information about ShiftLeft Converter, use the BlazeMeter MCP help tools:

**ShiftLeft Converter for LoadRunner**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-shiftleft-converter-for-loadrunner`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-shiftleft-converter-for-loadrunner"]}`

**ShiftLeft Converter - Enhance with AI**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-shiftleft-converter-enhance-with-AI`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-shiftleft-converter-enhance-with-AI"]}`

**ShiftLeft Converter - Files and Functions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-shiftleft-files-and-functions`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-shiftleft-files-and-functions"]}`

**ShiftLeft Converter - Troubleshooting**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-shiftleft-converter-troubleshooting`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-shiftleft-converter-troubleshooting"]}`

**ShiftLeft Converter - Changelog**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-shiftleft-converter-changelog`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-shiftleft-converter-changelog"]}`

**Note**: The changelog help_id may have technical issues when reading. For the latest ShiftLeft Converter updates and changes, visit the [ShiftLeft Converter website](https://shiftleft.blazemeter.com/) or contact BlazeMeter support.

---

---

## JMX Converter

Convert various testing scripts and logs into JMeter-compatible JMX files using the BlazeMeter JMX Converter tool.

**Use when**: Converting HAR files, Selenium scripts, PCAP files, or supported JSON formats to JMeter JMX files for use in BlazeMeter or JMeter.

### Overview

The JMX Converter tool by BlazeMeter lets you convert various testing scripts and logs into JMeter-compatible JMX files. This enables you to leverage existing test artifacts and integrate them into JMeter-based testing workflows seamlessly. The JMX Converter supports multiple input formats, including Selenium, PCAP, and specific JSON formats, making it a versatile tool for test conversion.

### Supported Input Formats

The JMX Converter supports the following input formats:

- **HAR (HTTP Archive)**: Browser network capture files
- **Selenium Builder Scripts**: Selenium test scripts
- **PCAP (Packet Capture) Files**: Network packet capture files
- **JSON**: JSON files from the BlazeMeter Chrome Extension, HAR, and Selenium Builder. If your JSON file is an API Monitoring test, see [Convert API Monitoring Test to Performance Test](https://help.blazemeter.com/docs/guide/api-monitoring-convert-to-performance.html) instead. The converter does not accept arbitrary JSON files. Only JSON files generated by the BlazeMeter Chrome Extension or similar sources are supported.

### Converting from HAR to JMX

When using the converter to convert your HAR scripts to JMX, note the following limitations:

- **No Page Splitting**: If there is a delay of several seconds between URLs, page splitting will not occur.
- **No Pause Between Pages**: Timers, such as the Uniform Random Timer, will be placed under each request rather than pausing between pages.
- **No HTTP Defaults**: Hostname, scheme, and port will be hard-coded in all HTTP samplers, with no use of HTTP Default settings.
- **No URL Filtering**: There are no options to include or exclude specific URLs during the conversion process.
- **No URL Numbering**: URLs will not be numbered or prefixed.
- **No `record.xml` File**: This file, crucial for future correlations, is not generated during the conversion.
- **HAR File Size Limit**: There is a limit on the upload size for the HAR file.
- **Sensitive Data Transmission**: Sensitive data contained in the HAR file may be transmitted to the BlazeMeter site.

Consider the limitations listed above when preparing your scripts for conversion to ensure they meet your testing requirements.

### How to Use the JMX Converter

**Steps:**

1. In your browser, navigate to [https://converter.blazemeter.com/](https://converter.blazemeter.com/).
2. Click **Choose file** and select the file you wish to convert from your local system. Ensure the file is in one of the supported formats (HAR, Selenium, PCAP, or supported JSON).
3. To upload the file, click **Open**.
4. Click **Convert**. The conversion process will begin, and you will see a progress indicator. Once the conversion is complete, a download link for the JMX file will appear.
5. Click the download link to save the converted JMX file to your local system.

**Result:**

You can now use this JMX file in BlazeMeter or JMeter for further testing.

### Example Use Case

**Converting a HAR File to JMX:**

1. **Capture HAR Data**: Use your browser's developer tools to capture HAR data during a web session.
2. **Upload HAR File**: Upload the captured HAR file to the JMX Converter.
3. **Convert and Download**: Convert the HAR file and download the resulting JMX file.
4. **Run in JMeter/BlazeMeter**: Import the JMX file into JMeter/BlazeMeter and configure it for your testing needs.

### Common Issues and Troubleshooting

**Unsupported JSON Error:**

If you receive an error stating that the JSON file is unsupported, ensure that your JSON file is generated by the BlazeMeter Chrome Extension or similar supported sources.

**Conversion Errors:**

If the conversion process fails, check the following:

- Ensure your input file is in one of the supported formats.
- Verify that the file is not corrupted and is correctly formatted.
- Check file size limits if uploading large files.
- If the issue persists, contact BlazeMeter support for assistance.

### Documentation References

For detailed information about JMX Converter, use the BlazeMeter MCP help tools:

**JMX Converter**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-jmx-converter.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-jmx-converter.htm"]}`

---

## Documentation References

For detailed information about BlazeMeter development tools, use the BlazeMeter MCP help tools:

**Visual Studio Code Plugin**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-visual-studio-code-plugin`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-visual-studio-code-plugin"]}`

**MCP Server**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-mcp-server`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-mcp-server"]}`

**MCP Server Tools**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-blazemeter-mcp-server-tools`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-blazemeter-mcp-server-tools"]}`

**ShiftLeft Converter for LoadRunner**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-shiftleft-converter-for-loadrunner`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-shiftleft-converter-for-loadrunner"]}`

