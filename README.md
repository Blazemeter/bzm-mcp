# BlazeMeter MCP Server

The BlazeMeter MCP Server connects AI tools directly to BlazeMeter's cloud-based performance testing platform. This gives AI agents, assistants, and chatbots the ability to manage complete load testing workflows from creation to execution and reporting. All through natural language interactions.

## Use Cases

- **Performance Test Management**: Create, configure, and manage performance tests with automated script uploads and asset management.
- **Test Execution & Monitoring**: Start tests, monitor execution status, and retrieve comprehensive reports including summary, errors, and request statistics.
- **Workspace & Project Organization**: Navigate through accounts, workspaces, and projects to organize your testing infrastructure.
- **Load Configuration**: Configure test parameters including concurrency, iterations, duration, ramp-up settings, and geographic distribution.
- **Report Analysis**: Access detailed execution reports, error analysis, and performance metrics for comprehensive test insights.
- **Account & Permission Management**: Manage multiple accounts and workspaces with proper AI consent controls and permission validation.

Built for developers and QA teams who want to connect their AI tools to BlazeMeter's enterprise-grade performance testing capabilities, from simple test creation to complex multi-step automation workflows.

---

## Prerequisites

- BlazeMeter API credentials (API Key ID and Secret)
- Compatible MCP host (VS Code, Claude Desktop, Cursor, Windsurf, etc.)
- Docker (only for Docker-based deployment)
- [uv](https://docs.astral.sh/uv/) and Python 3.11+ (only for installation from source code distribution)

## Setup

### **Get BlazeMeter API Credentials**
Follow the [BlazeMeter API Keys guide](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html) to obtain your API keys as JSON.

> [!IMPORTANT]
> When downloading your API keys from BlazeMeter, save the `api-keys.json` file in the same folder where you'll place the MCP binary.

### **Quick Setup with CLI Tool** ⚡

The easiest way to configure your MCP client is using our interactive CLI tool:

1. **Download the appropriate binary** for your operating system from the [Releases](https://github.com/BlazeMeter/bzm-mcp/releases) page

> [!NOTE]
> Choose the binary that matches your OS (Windows, macOS, Linux)
2. **Place the binary** in the same folder as your `api-keys.json` file
3. **Execute or Double-click the binary** to launch the interactive configuration tool
4. **The tool automatically generates** the JSON configuration file for you

> [!IMPORTANT]
> For macOS: You may encounter a security alert saying "Apple could not verify 'bzm-mcp-darwin' is free of malware." To resolve this:
> 1. Go to **System Settings** → **Privacy & Security** → **Security**
> 2. Look for the blocked application and click **"Allow Anyway"**
> 3. Try running the binary again

![CLI Demo](/docs/cli-tool.gif)

<details>
<summary><strong>Manual Client Configuration (Binary Installation)</strong></summary>

1. **Download the binary** for your operating system from the [Releases](https://github.com/BlazeMeter/bzm-mcp/releases) page
2. **Configure your MCP client** with the following settings:

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

</details>
<details>
<summary><strong>Manual Client Configuration (From Remote Source Code)</strong></summary>

1. **Prerequisites:** [uv](https://docs.astral.sh/uv/) and Python 3.11+
2. **Configure your MCP client** with the following settings:

```json
{
  "mcpServers": {
    "BlazeMeter MCP": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/Blazemeter/bzm-mcp.git@v1.1",
        "-q", "bzm-mcp", "--mcp"
      ],
      "env": {
        "BLAZEMETER_API_KEY": "/path/to/your/api-key.json"
      }
    }
  }
}
```
> [!NOTE]
> uvx installs and runs the package and its dependencies in a temporary environment.
> You can change to any version that has been released or any branch you want. Package support for uvx command is supported from version 1.1 onwards.
> For more details on the uv/uvx arguments used, please refer to the official [uv documentation](https://docs.astral.sh/uv/).

</details>
---

## Available Tools

The BlazeMeter MCP Server provides comprehensive access to BlazeMeter's API through six main tools:

| Tool | Purpose | Key Capabilities |
|------|---------|------------------|
| **User** | User Information | Get current user details, default account/workspace/project |
| **Account** | Account Management | List accounts, check AI consent, read account details |
| **Workspace** | Workspace Management | Manage workspaces, get locations, check billing usage |
| **Project** | Project Management | Organize projects, get test counts, manage project settings |
| **Tests** | Test Management | Create, configure, and manage performance tests |
| **Execution** | Test Execution | Run tests, monitor status, retrieve reports |

---

### **User Management**
**What it does:** Get information about your BlazeMeter account and default settings.

| Action | What you get |
|--------|-------------|
| Get user info | Your username, default account, workspace, and project IDs |

**When to use:** Start here to get your default account, workspace, and project IDs.

---

### **Account Management**
**What it does:** Manage your BlazeMeter accounts and check permissions.

| Action | What you get |
|--------|-------------|
| Get account details | Account information and AI consent status |
| List accounts | All accounts you have access to |

**When to use:** Verify AI consent and access account-level information.

---

### **Workspace Management**
**What it does:** Navigate and manage your testing workspaces.

| Action | What you get |
|--------|-------------|
| Get workspace details | Workspace information and billing details |
| List workspaces | All workspaces in an account |
| Get locations | Available test locations for different purposes |

**When to use:** Navigate your testing infrastructure and check available locations.

---

### **Project Management**
**What it does:** Organize your tests within workspaces.

| Action | What you get |
|--------|-------------|
| Get project details | Project information and test count |
| List projects | All projects in a workspace |

**When to use:** Organize tests within workspaces and check project statistics.

---

### **Test Management**
**What it does:** Create, configure, and manage your performance tests.

| Action | What you get |
|--------|-------------|
| Get test details | Test configuration and current settings |
| Create test | New performance test |
| List tests | All tests in a project |
| Configure load | Set users, duration, ramp-up settings |
| Configure locations | Set geographic distribution |
| Upload files | Upload test scripts and assets |

**When to use:** Create and configure performance tests with scripts and load parameters.

---

### **Execution Management**
**What it does:** Run tests and analyze results.

| Action | What you get |
|--------|-------------|
| Start test | Launch a configured test |
| Get execution status | Current test status and details |
| List executions | All executions for a test |
| Get summary report | Test execution summary |
| Get error report | Error analysis and details |
| Get request stats | Request statistics and performance metrics |
| Get all reports | Complete test results (summary, errors, stats) |

**When to use:** Run tests and analyze results with comprehensive reporting.

---

## Docker Support

### **MCP Client Configuration for Docker**

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
> [!IMPORTANT]
> For Windows OS, paths must use backslashes (`\`) and be properly escaped as double backslashes (`\\`) in the JSON configuration.
> E.g.: `C:\\User\\Desktop\\mcp_test_folder`

> [!NOTE]
> In order to obtain the `API_KEY_ID` and`API_KEY_SECRET` refere to [BlazeMeter API keys](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html)

---

## License

This project is licensed under the Apache License, Version 2.0. Please refer to [LICENSE](./LICENSE) for the full terms.

---

## Support

- **Documentation**: [BlazeMeter API Documentation](https://help.blazemeter.com/apidocs/)
- **Issues**: [GitHub Issues](https://github.com/BlazeMeter/bzm-mcp/issues)
- **Support**: Contact BlazeMeter support for enterprise assistance