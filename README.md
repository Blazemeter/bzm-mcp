![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/blazemeter/bzm-mcp/total?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2FBlazemeter%2Fbzm-mcp%2Freleases)
[![GHCR Pulls](https://ghcr-badge.elias.eu.org/shield/Blazemeter/bzm-mcp/bzm-mcp?style=for-the-badge)](https://github.com/Blazemeter/bzm-mcp/pkgs/container/bzm-mcp)
---
# BlazeMeter MCP Server

The BlazeMeter MCP Server connects AI tools directly to BlazeMeter's cloud-based performance testing platform. This gives AI agents, assistants, and chatbots the ability to manage complete load testing workflows from creation to execution and reporting. All through natural language interactions.

> [!NOTE]  
> **For detailed documentation including use cases, available tools, integration points, and troubleshooting, see the [BlazeMeter MCP Server documentation](https://help.blazemeter.com/docs/guide/integrations-blazemeter-mcp-server.html).**

---

## Prerequisites

- BlazeMeter API credentials (API Key ID and Secret)
- Comply [Blazemeter AI Consent](https://help.blazemeter.com/docs/guide/administration-ai-consent.html)
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
>
> 1. **Place the binary** in the same folder as your `api-keys.json` file
> 2. **Execute or Double-click the binary** to launch the interactive configuration tool
> 3. **The tool automatically generates** the JSON configuration file for you

> [!IMPORTANT]  
> For macOS: You may encounter a security alert saying "Apple could not verify 'bzm-mcp-darwin' is free of malware." To resolve this:
>
> 1. Go to **System Settings** → **Privacy & Security** → **Security**
> 2. Look for the blocked application and click **"Allow Anyway"**
> 3. Try running the binary again

![CLI Demo](/docs/cli-tool.gif)

---

**Manual Client Configuration (Binary Installation)**

1. **Download the binary** for your operating system from the [Releases](https://github.com/BlazeMeter/bzm-mcp/releases) page
2. **Run the binary once** — it will print a JSON config and **clickable links** to add this MCP in Cursor or VS Code.
3. **Or configure your MCP client manually** with the following settings:

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

---

**Manual Client Configuration (From Remote Source Code)**

1. **Prerequisites:** [uv](https://docs.astral.sh/uv/) and Python 3.11+
2. **One-click install** or configure your MCP client manually:

[![Add to Cursor (uvx)](https://img.shields.io/badge/Add_to_Cursor-uvx_install-blue?style=for-the-badge)](cursor://anysphere.cursor-deeplink/mcp/install?name=BlazeMeter%20MCP&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXQraHR0cHM6Ly9naXRodWIuY29tL0JsYXplbWV0ZXIvYnptLW1jcC5naXRAdjEuMC4xIiwiLXEiLCJiem0tbWNwIiwiLS1tY3AiXSwiZW52Ijp7IkJMQVpFTUVURVJfQVBJX0tFWSI6IiJ9fQ) [![Add to VS Code (uvx)](https://img.shields.io/badge/Add_to_VS_Code-uvx_install-007ACC?style=for-the-badge&logo=visualstudiocode)](https://insiders.vscode.dev/redirect/mcp/install?name=BlazeMeter%20MCP&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2FBlazemeter%2Fbzm-mcp.git%40v1.0.1%22%2C%22-q%22%2C%22bzm-mcp%22%2C%22--mcp%22%5D%2C%22env%22%3A%7B%22BLAZEMETER_API_KEY%22%3A%22%22%7D%7D)

After installing, set `BLAZEMETER_API_KEY` to your `api-key.json` path in your client's MCP settings.

**Or configure manually** with the following settings:

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

> [!NOTE]  
> uvx installs and runs the package and its dependencies in a temporary environment.  
> You can change to any version that has been released or any branch you want. Package support for uvx command is supported from version 1.0.1 onwards.  
> For more details on the uv/uvx arguments used, please refer to the official [uv documentation](https://docs.astral.sh/uv/).

</details>

---

**Docker MCP Client Configuration**

1. **Prerequisites:** [Docker]([https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/))

[![Add to Cursor (Docker)](https://img.shields.io/badge/Add_to_Cursor-Docker_install-blue?style=for-the-badge)](cursor://anysphere.cursor-deeplink/mcp/install?name=BlazeMeter%20MCP&config=eyJjb21tYW5kIjoiZG9ja2VyIiwiYXJncyI6WyJydW4iLCItLXJtIiwiLWkiLCItZSIsIkFQSV9LRVlfSUQiLCItZSIsIkFQSV9LRVlfU0VDUkVUIiwiLWUiLCJTT1VSQ0VfV09SS0lOR19ESVJFQ1RPUlkiLCJnaGNyLmlvL2JsYXplbWV0ZXIvYnptLW1jcDpsYXRlc3QiXSwiZW52Ijp7IkFQSV9LRVlfSUQiOiIiLCJBUElfS0VZX1NFQ1JFVCI6IiIsIlNPVVJDRV9XT1JLSU5HX0RJUkVDVE9SWSI6IiJ9fQ) [![Add to VS Code (Docker)](https://img.shields.io/badge/Add_to_VS_Code-Docker_install-007ACC?style=for-the-badge&logo=visualstudiocode)](https://insiders.vscode.dev/redirect/mcp/install?name=BlazeMeter%20MCP&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22--rm%22%2C%22-i%22%2C%22-e%22%2C%22API_KEY_ID%22%2C%22-e%22%2C%22API_KEY_SECRET%22%2C%22-e%22%2C%22SOURCE_WORKING_DIRECTORY%22%2C%22ghcr.io%2Fblazemeter%2Fbzm-mcp%3Alatest%22%5D%2C%22env%22%3A%7B%22API_KEY_ID%22%3A%22%22%2C%22API_KEY_SECRET%22%3A%22%22%2C%22SOURCE_WORKING_DIRECTORY%22%3A%22%22%7D%7D)

After installing, set `API_KEY_ID`, `API_KEY_SECRET`, and optionally mount/working dir in your client's MCP settings.

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

**Custom CA Certificates (Corporate Environments) for Docker**

**When you need this:**

- Your organization uses self-signed certificates
- You're behind a corporate proxy with SSL inspection
- You have a custom Certificate Authority (CA)
- You encounter SSL certificate verification errors when running tests

**Required Configuration:**

When using custom CA certificate bundles, you must configure both:

1. **Certificate Volume Mount**: Mount your custom CA certificate bundle into the container
2. **SSL_CERT_FILE Environment Variable**: Explicitly set the `SSL_CERT_FILE` environment variable to point to the certificate location inside the container

<details><summary><strong>Example Configuration</strong></summary>

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

**Replace:**

- `/path/to/your/ca-bundle.crt` with your host system's CA certificate file path
- The container path `/etc/ssl/certs/custom-ca-bundle.crt` can be any path you prefer (just ensure it matches `SSL_CERT_FILE`)

> The `SSL_CERT_FILE` environment variable must be set to point to your custom CA certificate bundle. The `httpx` library [automatically respects the `SSL_CERT_FILE` environment variable](https://www.python-httpx.org/advanced/ssl/#working-with-ssl_cert_file-and-ssl_cert_dir) for SSL certificate verification.
</details>

---

## License

This project is licensed under the Apache License, Version 2.0. Please refer to [LICENSE](./LICENSE) for the full terms.

---

## Support

- **MCP Server Documentation**: [BlazeMeter MCP Server Guide](https://help.blazemeter.com/docs/guide/integrations-blazemeter-mcp-server.html)
- **API Documentation**: [BlazeMeter API Documentation](https://help.blazemeter.com/apidocs/)
- **Issues**: [GitHub Issues](https://github.com/BlazeMeter/bzm-mcp/issues)
- **Support**: Contact BlazeMeter support for enterprise assistance

