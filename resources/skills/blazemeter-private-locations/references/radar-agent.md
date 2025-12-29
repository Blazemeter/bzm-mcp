# Radar Agent

## Overview

Understand and use the Radar Agent for API Monitoring to access private APIs, including how it works, downloading, running, command line options, and troubleshooting.

**Use when**: Understanding and using the Radar Agent for API Monitoring to access private APIs or downloading, running, configuring command line options, and troubleshooting Radar Agent.

### Overview

The Radar Agent bridges BlazeMeter API Monitoring to private APIs not available over the public internet. By running the agent within your infrastructure, BlazeMeter API monitors can run against endpoints that are otherwise inaccessible to the [cloud agents](https://help.blazemeter.com/docs/guide/api-monitoring-global-locations.html). The agent is particularly useful if you are looking to test or monitor an API in the following situations:

- **Monitoring private or internal APIs** that reside behind a firewall. For Radar Agents to function properly, you need to allow two types of network access through your firewall: access to api.runscope.com, and access to any endpoints your tests are targeting.
- Testing APIs on **localhost** or in a private staging environment.
- Accessing APIs that require a **fixed client IP address** (IP allowlisting).

**Use of the agent requires a trial or paid subscription.**

A Radar Agent is a wholly separate installation apart from a [Private Location](https://help.blazemeter.com/docs/guide/private-locations-intro.html). Private Location serves as an on-premise agent for running Functional Tests or Performance Tests. The Radar Agent serves as an on-premise agent for running [API Monitoring tests](https://help.blazemeter.com/docs/guide/api-monitoring-create-your-first-api-monitoring-test.html).

### How it Works

Monitoring and testing private APIs with API Monitoring uses a **hybrid on-premises** approach. The agent runs on a host within your infrastructure but test data is managed and stored in the BlazeMeter cloud. Using the API Monitoring dashboard, you have a single interface for defining tests, viewing results, configuring notifications and enabling 3rd-party integrations.

All communication from the agent to the BlazeMeter cloud is made over outbound requests to the BlazeMeter API via HTTPS on port 443. The agent requests work to be processed and sends back results over a TLS-encrypted connection and is not externally addressable.

### Download the Agent

Select an operating system to download the latest agent:
- [macOS (64-bit)](https://storage.googleapis.com/runscope-downloads/runscope-radar/latest/darwin-universal/runscope-radar.zip)
- [Windows (64-bit)](https://storage.googleapis.com/runscope-downloads/runscope-radar/latest/windows-amd64/runscope-radar.zip)
- [Linux (64-bit)](https://storage.googleapis.com/runscope-downloads/runscope-radar/latest/linux-amd64/runscope-radar.zip)

For information on previous releases, see [Radar Agent Changelog.](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-changelog.html)

#### Recommended Requirements

As a general guideline, we recommend a machine with:
- 4-core CPUs or higher
- 4GB RAM or higher

### Run the Agent

After downloading the agent, extract the executable from the .zip file so that you can run it from your command line.

If you do not yet have a token, follow these steps to create one:

1. Log in to BlazeMeter and navigate to the **API Monitoring** tab.
2. Click the Profile and Account Settings icon in the top right corner.
3. From the drop-down list, select **Personal Information**.
4. In the menu on the left, click **Applications**.
5. Click **Create Application**.
6. Name your app. You do not necessarily need a real application, as this app may simply serve as a placeholder for generating your token, so consider naming for example "API Monitoring Agent Token".
7. The app requires a website URL and callback URL. Since this can be a placeholder app, you may enter any URL you like, even completely imaginary URLs.
8. Click **Create Application**.
9. On the next page, scroll down to view your new Personal Access Token.

You may wonder why it is necessary to create a new application. The API Monitoring feature typically requires a token be associated with an application for general use cases, but in this context, we simply need a token to authenticate the agent with, so creating a fake "dummy" application in order to generate one will suffice.

Once you have a token, run your agent for the first time:

*Linux and macOS*
```
$ ./runscope-radar --token=your_personal_access_token
```

*Windows*
```
C:\> runscope-radar.exe --token=your_personal_access_token
```

If you are a member of multiple API Monitoring teams, then you will next be prompted to select which team to associate your new agent with.

Once authenticated, you can save a configuration file to be used for subsequent runs of the agent (without having to pass your token each time). To launch the agent with a specific configuration file, use the `-f` command line option. This is the recommended way to start the agent.

*Linux and macOS*
```
$ ./runscope-radar -f radar.conf
```

*Windows*
```
C:\> runscope-radar.exe -f radar.conf
```

If you examine the contents of this configuration file, you will find that it contains various parameters, including the API token you provided earlier, along with a unique Agent ID and the Team ID the agent is associated with.

With the agent running, you're now ready to use it for your tests.

### Using the Agent for Test Runs

After downloading and launching the agent, head over to the API test editor for the test you want to use the agent for. If everything is working correctly, the agent will appear as an option in the **Locations** section of the environment settings.

If you are testing an API across multiple realms (for example local, staging, prod), you may want to selectively [enable the agent per-environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html). The agent can also be enabled in a [shared environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html#shared) used across tests within a single bucket.

### Command Line Flags / Configuration File Reference

You can specify the following parameters in your configuration file, or on the command line, when executing the agent. The configuration file will override the same parameters used in the command line.

Key parameters include:
- `--agent-id` (string) - Agent UUID
- `--api-host` (string) - API host base URL
- `--cafile` (string) - CA certificate file
- `--cert` (string) - Client certificate file (PEM-encoded) for two-way HTTPS authentication
- `-f, --configfile` (string) - Start the agent with the configuration contained within the specified configuration file
- `--debug` - Enable debugging web server
- `--disable-dns-lookup` (boolean) - Default is "false" (DNS pre-checks enabled). Set to "true" to disable DNS pre-checks
- `--disconnect-timeout` (string) - Disconnect timeout. Default: "5"
- `--ignore-env-proxy` - Ignore HTTP_PROXY and HTTPS_PROXY environment variables. Requests to api.runscope.com will still use the proxy
- `--key` (string) - Client key file (PEM-encoded) for two-way HTTPS authentication
- `-l, --logfile` (string) - Write logfile to an external file
- `--name` (string) - The name of the agent to be displayed in the API Monitoring UI Locations menu
- `--pass` (string) - Passphrase for client key file
- `--pidfile` (string) - Pidfile
- `--private` (boolean) - Set the Radar agent to be only visible to user that created it. When set to true, the Radar agent will appear in a "read-only" mode to every other user when editing locations in a test environment, and only the user that created the Radar agent can enable or disable it within a test environment. The default is false, meaning that the Radar agent is visible to every user in the team that the agent is associated with
- `--team-id` (string) - Team UUID
- `--threads` (integer) - Number of worker threads. Default: 10
- `--timeout` (integer) - Connection idle timeout. Default: 20
- `-t, --token` (string) - API Monitoring Auth Token
- `--use-system-certs` - Use system/OS provided certificates for HTTPS authentication
- `-v, --verbose` - Log more information
- `--verify-ssl` (boolean) - Verify SSL
- `--version` - Get version number. Only works on the cli
- `--web-host` (string) - Web host base url. Default: https://www.runscope.com

### Examples

Running the agent in verbose mode, and ignoring env proxy variables:
```
$ ./runscope-radar -f radar.conf -v --ignore-env-proxy
```

Configuration file with increased threads value to support a higher amount of requests, and ignoring environment proxy variables:
```
api-host=https://api.runscope.com
threads=50
agent-id=your_agent_id
team-id=your_team_id
name=internal-1.local
timeout=20
disconnect-timeout=5
cafile=
token=your_runscope_token
ignore-env-proxy
```

### Troubleshooting

In the event that the Radar Agent is down or otherwise not available for any reason, BlazeMeter will expire any test executing on it and immediately set a status of "Remote Agent Expired" so that the user is alerted to the problem. Automated [email](https://help.blazemeter.com/docs/guide/api-monitoring-notifications-overview.html) and/or [Slack](https://help.blazemeter.com/docs/guide/api-monitoring-slack-integration.html) notifications may be sent as well. Please refer to the [Handling Radar Agent Availability Issues](https://help.blazemeter.com/docs/guide/private-locations-handle-radar-agent-availability-issues.html) guide for our recommended best practices.

All tests marked with the "Remote Agent Expired" status will be colored orange in the Dashboard, Latest Test Results, and Test Result progress bars in the GUI.

While an on-premise Radar Agent is down and until said agent comes back up (is available again), no scheduled test that tries to run on it will count toward any metrics calculation, nor will it count toward the owning team's test count.

If you run into any issues while setting up or running the agent, such as difficulty connecting to `api.runscope.com`, or intermittent test errors, check out the following troubleshooting articles:
- [Connection Errors](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-connection-errors.html)
- [HTTP/HTTPS Proxy Setup](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-http-https-proxy-setup.html)
- [Remote Agent Expired](https://help.blazemeter.com/docs/guide/private-locations-remote-agent-expired.html)
- [SSO Login Error](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-sso-login-error.html)

---

## Changelog

Track Radar Agent version history, release dates, and new features across different versions for API Monitoring agents. The following are released versions of the BlazeMeter API Monitoring Radar Agent.

**Use when**: Tracking Radar Agent version history, release dates, and new features or reviewing changes across different versions for API Monitoring agents.

### Version History

| Version | Release Date |
|---------|--------------|
| 1.31 (current, latest) | Sep 2, 2025 |
| 1.30 | Aug 5, 2025 |
| 1.28 | Jul 9, 2025 |
| 1.27 | Mar 17, 2025 |
| 1.26 | Oct 28, 2024 |
| 1.25 | Oct 17, 2024 |
| 1.24 | Sep 26, 2024 |
| 1.22 | Jun 1, 2024 |
| 1.21 | May 23, 2024 |
| 1.20 | Apr 9, 2024 |
| 1.18 | Sep 14, 2023 |
| 1.17 | Aug 31, 2023 |
| 1.16 | Jul 19, 2023 |
| 1.15 | Jun 28, 2023 |
| 1.13 | May 3, 2023 |
| 1.11 | Jan 30, 2023 |
| 1.10 | Nov 3, 2022 |
| 1.9 | Oct 21, 2022 |
| 1.8rc | Jun 13, 2022 |
| 1.6rc | Jan 18, 2022 |
| 1.5rc | Jan 5, 2022 |
| 1.4rc | Dec 21, 2021 |
| 1.3rc | Nov 11, 2021 |
| 1.2rc | Oct 5, 2021 |
| 1.1rc | Sep 30, 2021 |
| 1.0rc | Sep 28, 2021 |

### What's New in Recent Versions

**Version 1.31:**
- Presigned S3 URLs for remote Radar agents (fixes file upload errors)
- Deprecation of Runscope name in notices and logs (replaced with "BlazeMeter API Monitoring")

**Version 1.30:**
- Improved DNS resilience to handle intermittent failures (DNS lookups retried up to 5 times)

**Version 1.28:**
- Custom HTTP status code of '50000' for DNS-related errors (easy identification without opening failed test)

**Version 1.27:**
- Bug Fix: Fixed issue with decrypting private keys that require a passphrase when performing two-way authentication (mTLS) with an HTTPS server

**Version 1.26:**
- Allow Radar Agents to Be Hidden from Other Users: New `--private` flag added so agent is only visible to the user that created it (defaults to false)

**Version 1.25:**
- Custom Proxy support in BlazeMeter: Route requests through a designated proxy server, supporting both HTTP and HTTPS endpoints

**Version 1.24:**
- GraphQL support: BlazeMeter now supports GraphQL-based API testing and monitoring

**Version 1.22:**
- Bug fix: Fixed defect with Radar Agent not reporting failures in a timely manner (TT-4108)

**Version 1.21:**
- Built using Golang 1.21.10: Fixes several vulnerabilities and addresses regression related to HTTP/2 client performance

**Version 1.20:**
- Radar Agent as a Container: Docker image available, Helm chart available for Kubernetes deployment
- Use system/OS-level provided certificates by default for HTTPS authentication (default changed from false to true)

**Version 1.18:**
- Universal macOS binary: Can now use universal macOS binary to run on Intel or ARM processors
- Removal of 32-bit Windows and Linux Radar agents: Latest agent supports 64-bit versions only
- Standardized error handling for AWS S3 binary and multipart files

**Version 1.17:**
- Improved AWS S3 connection for binary file upload

**Version 1.16:**
- Support for binary file uploads and request chaining
- Improved efficiency of HTTP connections

**Version 1.15:**
- Local client authentication configuration options: Added `cert`, `key`, and `pass` command line flags/config file options for two-way HTTPS authentication (mTLS)
- Use system/OS-level provided certificates for HTTPS authentication: `use-system-certs` command line flag/config file option available

**Version 1.13:**
- Improved logging for configuration of trusted root certificates

**Version 1.11:**
- HTTP/2 Support: Radar agents support HTTP/2 when performing test requests
- Force h2c (HTTP/2 over cleartext): Support for forcing HTTP/2 over cleartext

**Version 1.10:**
- Use of Hostname in HTTP/S Proxy Connection: Hostname of test request URL now properly used instead of IP address

**Version 1.9:**
- Radar Agent Version Shown for Each Location: Can view radar agent version running on each location
- Option to Disable DNS Pre-Check: `disable-dns-lookup` command line flag/config file option available
- Built Using Golang 1.19.1
- Removed Support for HTTPS Common Name field in X509 Certificates

**Version 1.8rc:**
- Support for TLS 1.3: Radar agent now supports TLS versions 1.0 through 1.3
- Built Using Golang 1.16.15

For detailed information about each version, see the [Radar Agent Changelog](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-changelog.html) help documentation.

---

## Connection Errors

Troubleshoot Radar Agent connection errors, including version checks, ping/curl tests, verbose mode, proxy settings, and DNS error resolution. If your radar agent is unable to communicate with BlazeMeter, here are a couple of steps you can take to solve this issue.

**Use when**: Troubleshooting Radar Agent connection errors or performing version checks, ping/curl tests, verbose mode, proxy settings, and DNS error resolution.

### Troubleshooting Steps

1. **Version Check**: Make sure that you are running the latest version of the agent. You can check your agent version by running it with the `--version` flag. You can [download the latest version here](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-overview.html#downloading)

2. **Ping/Curl Tests**: Run a `ping` and `curl` request on the same machine that the agent is running on, and check that you receive a valid response. For example:
   ```
   ping -c 5 api.runscope.com
   curl https://api.runscope.com
   ```

3. **Verbose Mode**: Run the agent with the `--verbose` flag to get a more detailed output, and check for any error messages

4. **Proxy Settings**: Check your server's proxy settings to see if it's not blocking any requests to `api.runscope.com`. For more information on using the agent with a proxy, check the [HTTP/HTTPS Proxy Setup](#httphttps-proxy-setup) section

5. **Environment Configuration**: If the server is successfully communicating with BlazeMeter, and you have checked your proxy settings, check that your API test's environment is not misconfigured to use a disconnected remote agent with the same name

### DNS Errors

Radar agent currently performs a DNS pre-check before sending any actual HTTP/s request. If the hostname of the request is unable to be resolved by the local DNS resolver of the system that the agent is running on, the entire tests will fail with a message such as shown next:

*"Error communicating with www.example.com**DNS error resolving host: www.example.com: no such host"*

This causes issues for users that want to use a proxy to access hosts that are not directly accessible by the system that Radar is running on.

As of Radar agent version 1.9, you can disable DNS pre-checks through command line interface or config file.

**To disable DNS pre-checks:**
- **Through CLI**: `--disable-dns-lookup` OR `--disable-dns-lookup=true`
- **Through config file**: `disable-dns-lookup` OR `disable-dns-lookup=true`

**To enable DNS pre-checks:**
- **Through CLI**: `--disable-dns-lookup=false`
- **Through config file**: `disable-dns-lookup=false`

**Note**: The default is set to false (DNS pre-checks enabled)

---

## SSO Login Error

Resolve SSO login errors for Radar Agent by creating Personal Access Tokens and configuration files for teams with Single Sign-on enabled. In case your team has Single Sign-on (SSO) enabled, your login credentials will not work on the command-line for the Radar agent.

**Use when**: Resolving SSO login errors for Radar Agent or creating Personal Access Tokens and configuration files for teams with Single Sign-on enabled.

### Create a Personal Access Token

Follow these steps:

1. From your BlazeMeter API Monitoring account, click on the **Profile & Account Settings** icon on top right
2. On the left-hand tab, select **Applications**
3. If you don't already have an Application, click the **Create Application** button and fill in the details to create your new application. The "Website URL" and "Callback URL" fields can be filled in with placeholder values such as: `http://www.example.com`. Save your changes
4. Open your Application and scroll to the bottom of the page until you reach the "Personal Access Token" section
5. Copy the **Access Token** value. You will be pasting this into your On-Premise Agent "radar.conf" config file in a later step

### Create the Agent Configuration File

Follow these steps:

1. Create a new text file named "radar.conf" in the same directory where you saved the On-Premise Agent
2. Copy the following contents into your "radar.conf" file (make sure that you don't have any blank lines or LF/CR characters):
   ```
   api-host=https://api.runscope.com
   threads=10
   team-id=your_team_id
   name=On-Premises_Radar_Agent
   timeout=20
   disconnect-timeout=5
   cafile=
   token=your_auth_token
   ```
3. Replace the "your_team_id" value. You can find your team-id by viewing the details for your team from the *Teams & Usage* page. The team-id is available in the URL of your browser, for instance: `https://www.runscope.com/teams/**d8cf6f8d-4dd6-4437-8c64-220cd3c3b662**`
4. Replace the "your_auth_token" value in the "radar.conf" file with the **Access Token** value that you copied in the previous steps
5. (Optional) You can also change the agent "name". That is the name that will appear for your agent in the "Locations" drop-down menu
6. Save your changes when you're done
7. Run the On-premise Agent specifying the newly created "radar.conf" config file. For example, here is the command for Windows:
   ```bash
   runscope-radar.exe -f radar.conf
   ```

---

## HTTP/HTTPS Proxy Setup

Configure Radar Agent to use HTTP/HTTPS proxy servers, including environment variables, authentication, and bypassing proxies for specific domains. The following information is valid for a Linux agent. For a Windows agent, set the environmental variables separately before you run the radar executable.

**Use when**: Configuring Radar Agent to use HTTP/HTTPS proxy servers or setting up environment variables, authentication, and bypassing proxies for specific domains.

### Configuration

When using the Radar agent behind a proxy, you will need to use `http_proxy=`, or `HTTPS_PROXY=` (indicating the proxy and port), before executing the `runscope-radar` command. Here's an example of that command:

```bash
https_proxy=http://username:password@api.proxy.com:8080 ./runscope-radar
```

Our code will look for your proxy environment variables as:
- `https_proxy` or `HTTPS_PROXY`
- `http_proxy` or `HTTP_PROXY`

### Ignore Environment Proxy for Test Calls

You may also need to add `ignore-env-proxy` to your config file (or `--ignore-env-proxy` from the command line) to ignore the environment proxy variables for **test calls**, but not for external calls to runscope.com to push results back to us.

### Bypass Proxy for Specific Domains

If you'd like the agent to bypass your server's proxy, you can use the `NO_PROXY` environment variable and add your API's host IP or domains to it. For example:

```bash
NO_PROXY=api.example.com,yourapihere.com HTTP_PROXY=proxy.example.com ./runscope-radar
```

That would make the agent use `proxy.example.com` for all requests, except for the `api.example.com` and `yourapihere.com` domains

---

## High Availability/Failover Capability

Set up high availability and failover for Radar Agent by running multiple instances with the same configuration for load balancing and redundancy. In case you have a high number of tests running on the same Radar agent, or you want to have some failover capability besides using an [utility like nohup or screen](skill-blazemeter-private-locations://references/radar-agent.md), you can run multiple instances of the same agent.

**Use when**: Setting up high availability and failover for Radar Agent or running multiple instances with the same configuration for load balancing and redundancy.

### Setup

For that to work and the agents to load balance the requests, you can run the agent in the same, or separate, server, as long as they use the exact same config file.

The API Monitoring UI will still show a single agent in your environment's Location tab, and the test will be distributed to whichever agent is available.

**Key Points:**
- **Multiple Instances**: Run multiple agent instances on the same or separate servers
- **Same Configuration**: All instances must use the exact same config file
- **Load Balancing**: Requests are automatically distributed to whichever agent is available
- **UI Display**: The API Monitoring UI shows a single agent in the Location tab, even with multiple instances running
- **Failover**: If one agent instance fails, other instances continue to handle requests

---

## Handle Availability Issues

Monitor and handle Radar Agent availability issues, including creating monitoring tests, viewing test results, and using advanced webhooks for agent health monitoring. [Email](https://help.blazemeter.com/docs/guide/api-monitoring-notifications-overview.html), [Slack notifications](https://help.blazemeter.com/docs/guide/api-monitoring-slack-integration.html) or [advanced webhooks](https://help.blazemeter.com/docs/guide/api-monitoring-advanced-webhooks.html) may be used to monitor and/or notify on-premise Radar Agent outages. We recommend the following best practices for configuring alerts that will quickly let notify your team of any issues specific to your agents.

**Use when**: Monitoring and handling Radar Agent availability issues or creating monitoring tests, viewing test results, and using advanced webhooks for agent health monitoring.

### Create a Radar Agent Monitoring Test

This method will promptly notify the appropriate parties responsible for managing your Radar Agent so that they can quickly address any issues as soon as they occur.

If you have multiple on-premise Radar Agents, repeat the following steps so that you create a separate monitoring test for each agent.

Follow these steps:

1. Create a new test in API Monitoring
2. Name the test ("Monitoring Test for Remote Agent <remote agent name>", for example)
3. Open the **Editor** menu
4. Expand the **Test Settings** section
5. Open the **Locations** subsection
6. Select the Radar Agent you wish to monitor by toggling its option to **On**
7. Open the **Email Notifications** (or **Integrations** for Slack) subsection
8. Check the box for each team member that should be notified
9. Under *Select the frequency of email notifications*, select **Notify only when a test run fails due to on-premises agent issues**
10. Open the **Schedules** menu
11. Click **+ Add Schedule**
12. Schedule the test (for example, every 15 minutes) and click **Save Schedule**

### View Radar Agent Monitoring Test Results

If BlazeMeter is unable to communicate with your Radar agent, test results that attempt to use that agent will be marked as **Remote Agent Expired**. This status is indicated in orange in the Dashboard, Latest Test Results, and Test Result progress bars.

Test runs that cannot be completed due to issues with remote agents (both on-premises and cloud agents) as well as system errors are not counted towards test metrics such as success ratio, average response time, and more. In the following example, some test runs have failed due to an expired remote agent, but this does not impact the success rate.

### Use Advanced Webhooks

You can also monitor the health of your remote agents by using [advanced webhooks](https://help.blazemeter.com/docs/guide/api-monitoring-advanced-webhooks.html).

BlazeMeter's advanced webhooks supports an `agent_expired` parameter, which indicates the status of the agent for the test run:
- `true` indicates that the agent is expired
- `null` indicates that the agent is available, or if a default BlazeMeter API Monitoring location is used

---

## Remote Agent Expired

Diagnose and resolve "Remote Agent Expired" status for Radar agents, including debugging steps, agent communication verification, and monitoring agent health. If BlazeMeter is unable to communicate with your Radar agent regularly, test results that attempt to use that agent will be marked as **Remote Agent Expired**, and will be indicated in orange in the Dashboard, Latest Test Results, and Test Result progress bars.

Test runs that cannot be completed due to issues with remote agents as well as system errors are not counted towards test metrics such as success ratio, average response time, and more.

**Use when**: Diagnosing and resolving "Remote Agent Expired" status for Radar agents or performing debugging steps, agent communication verification, and monitoring agent health.

### Debugging

Here are some steps you can follow to help debug this issue:

1. **Version Check**: Make sure that you're running the latest version of the agent. You can check the agent version by running it with the `--version` flag, and you can [download the latest version here](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-overview.html#downloading)

2. **Agent Communication**: Ensure that your agent is actively communicating with BlazeMeter by inspecting the output of the agent. You can use the `--verbose` flag when running the agent to get a more detailed output

3. **Connectivity Verification**: If the agent is unable to communicate with BlazeMeter, verify it's general ability to make outbound HTTPS requests to `https://api.runscope.com` and `https://www.runscope.com`. Check our [Agent Connection Errors](#connection-errors) and [HTTP/HTTPS Proxy Setup](#httphttps-proxy-setup) sections for more information

4. **Intermittent Issues**: If the agent is successfully connecting to BlazeMeter, but you're seeing intermittent issues with your test runs, two common causes for this are:
   - **No open slots for work**: If the agent output includes the following message: `[ERROR] No open slots for work`, that means your agent is trying to run more tests than it can handle. To fix this, update your configuration file to use `threads=50`
   - **Connection timeout**: If you're **not** seeing the error message above in the agent output, the issue might be that the agent is having trouble connecting to BlazeMeter in a timely manner. This could be caused by multiple reasons, such as an increased latency in the server's network, for example. To fix this, update your configuration file to use `disconnect-timeout=15`. That setting determines how long BlazeMeter will wait before considering the agent offline, so increasing the timeout can potentially fix the issue. The only drawback for increasing that value is that when you turn off the agent, the UI will take longer before showing it as offline

### Monitor Remote Agent Health

You can monitor the health of your remote agents by creating a Radar Agent Monitoring test, or by using webhooks:

- [Create a Radar Agent Monitoring test](#handle-availability-issues): Follow the steps in the "Handle Availability Issues" section
- [Use advanced webhooks](https://help.blazemeter.com/docs/guide/api-monitoring-advanced-webhooks.html): BlazeMeter's advanced webhooks supports an `agent_expired` parameter, which indicates the status of the agent for the test run:
  - `true` indicates that the agent is expired
  - `null` indicates that the agent is available, or if a default BlazeMeter API Monitoring location is used

---

## Auto-Restart on Linux

Configure automatic restart of Radar Agent on Linux using systemd services, including service file creation, permissions, and enabling auto-start on reboot. This article provides instructions on how to automatically restart Radar agent services, when a reboot occurs across the Linux machine or server where the agent is running.

This method uses Linux services framework and treats the Radar agent as a system service.

**Use when**: Configuring automatic restart of Radar Agent on Linux or creating systemd service files, setting permissions, and enabling auto-start on reboot.

### Set Up Auto-Restart

To set up auto-restart of your Radar agent:

1. Download the [radar agent binary](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-overview.html)
2. Unzip the binary file
3. Create a configuration file with all the required token, team ID and other configs. For more information and example, see [Radar Agent Overview](skill-blazemeter-private-locations://references/radar-agent.md)
4. Create a service file in `/etc/systemd/system/` with a name like **radar-agent.service**
5. Include the following content in the service file. Include the path to the config file (`/root/myconf.conf`):
   ```
   [Unit]
   Description=radar agent
   [Service]
   Type=simple
   ExecStart=/usr/bin/runscope-radar -f /root/myconf.conf
   [Install]
   WantedBy=multi-user.target
   ```
6. Give 644 permission to the service file:
   ```
   chmod 644 /etc/systemd/system/radar-agent.service
   ```
7. Reload the daemon:
   ```
   systemctl daemon-reload
   ```
8. Start the agent:
   ```
   systemctl start radar-agent.service
   ```
9. Check the status of agent:
   ```
   systemctl status radar-agent.service
   ```
10. Enable the service:
    ```
    systemctl enable radar-agent.service
    ```

---

## Timeout Handling

Understand timeout handling in Radar Agent, including connection timeouts, read/write deadlines, and limitations for extended operations.

**Use when**: Understanding timeout handling in Radar Agent or troubleshooting timeout issues with extended read and write operations.

### Timeout Configuration

In the Radar system, a fixed connection timeout of 90 seconds is hard-coded for establishing a link with a remote system. Once connected, we enforce a deadline of 270 seconds for both read and write operations, derived by tripling the initial connection timeout.

### Limitations

For extended read and write operations, there is no mechanism to dynamically extend the deadline. This may lead to timeouts if data retrieval from the remote system exceeds the allotted timeframe.

### Understanding the Deadline

When referring to the "deadline" in the context of Radar's timeout handling, it signifies that the entire response, encompassing every last byte, must be read within 270 seconds or less. This is distinct from a scenario where the 270 seconds would serve as the read timeout between successive chunks of bytes retrieved from the server— a structure reminiscent of Python's requests module.

**Key Points:**
- **Connection Timeout**: 90 seconds (hard-coded)
- **Read/Write Deadline**: 270 seconds (3x connection timeout)
- **No Dynamic Extension**: The deadline cannot be extended dynamically
- **Complete Response**: The entire response must be read within the deadline

---

## Configuring Radar Agent Certificates

Configure API Monitoring Radar agent certificates, including supported SSL CA certificates and best practices for configuring trusted certificates.

**Use when**: Configuring API Monitoring Radar agent certificates or understanding supported SSL CA certificates and best practices for configuring trusted certificates.

### Supported SSL CA Certificates for Radar Agent

The Radar agent supports certificates from the following authority list: [Mozilla Included CA Certificate List](https://ccadb-public.secure.force.com/mozilla/IncludedCACertificateReport).

### Best Practices for Configuring Trusted Certificates

From October 2023, the Radar agent has transitioned to using public certificates issued by Let's Encrypt, which are in turn signed by the ISRG Root X1 trusted root certificate authority. A comprehensive guide on this process can be found on the [Let's Encrypt](https://letsencrypt.org/certificates/) website.

Given that the majority of operating systems and contemporary browsers recognize the ISRG Root X1 root certificate authority, you should not encounter any complications when using system- or OS-level certificate authority bundles.

We recommend the following best practices when configuring trusted certificates:

1. **Use the latest version of the Radar agent**
2. **Use system certificates when available**: When running the Radar agent, if your system or OS has been properly configured with the trusted certificate authorities, opt for the `use-system-certs` option
3. **Use custom CA bundle**: Alternatively, use the `cafile` option when running the Radar agent to supply a custom CA bundle. API Monitoring periodically updates leaf/child certificate for api.runscope.com or *.runscope.com. If you are providing the Radar agent with a custom CA bundle file, ensure to include the ISRG Root X1 trusted root certificate and not just the leaf/child certificate. Do this to avoid service interruption or failure when the certificates are refreshed
4. **Download CA bundle if needed**: If you are unsure if your system or OS has trusted certificate authorities configured properly and you do not have a custom CA bundle file, allow the Radar agent to download a trusted CA bundle from [https://mkcert.org/generate](https://mkcert.org/generate). This method requires network or firewall access to the mkcert.org domain

For more information on configuration options, see the configuration file reference in [Radar Agent Overview](skill-blazemeter-private-locations://references/radar-agent.md).

---

## HTTPS Common Name in X509 Certificates

Understand and work around HTTPS Common Name field deprecation in Radar Agent, including certificate validation, testing certificates, and fixing invalid certificates. As of Radar Agent version 1.9, the Common Name (CN) field in X509 certificates is no longer supported.

**Use when**: Understanding and working around HTTPS Common Name field deprecation in Radar Agent or performing certificate validation, testing certificates, and fixing invalid certificates.

### Background

Radar Agent versions 1.9 and higher are built using Golang 1.19.1, which affects the type of X509 certificates that are supported when making HTTPS requests.

RFC 2818, published in May 2000, [deprecates](https://datatracker.ietf.org/doc/html/rfc2818#section-3.1) the use of the Common Name (CN) field in HTTPS certificates for subject name verification. It recommends using the "Subject Alternative Name" extension (SAN) of the "dns name" type.

[In Golang 1.15](https://go.dev/doc/go1.15#commonname), the recommendations from RFC 2818 were implemented and support for X509 certificates that use the Common Name field *without* a SAN extension entry was deprecated, with it scheduled to be removed in later versions.

[With Golang 1.17 and later](https://go.dev/doc/go1.17), this deprecated support of X509 certificates *without* a SAN extension entry was finally [removed](https://cs.opensource.google/go/go/+/02ce4118219dc51a14680a0c5fa24cf6e73deeed:src/crypto/x509/verify.go;dlc=b211fe005860db3ceff5fd56af9951d6d1f44325).

### Implications

When Radar Agent version 1.9 or higher sends a HTTPS request to an endpoint, the X509 certificate presented by the target server will be validated for a SAN extension. If the target server's domain name only appears in the Common Name field of the certificate, the following error will be raised:

```
x509: certificate relies on legacy Common Name field, use SANs instead
```

### How to Test Certificate of Target Server

Use openssl to verify if the certificate of your target server is valid (contains a SAN extension entry).

To test your server validity:

1. From a terminal, set the following variables to indicate the host and port of the target server:
   ```bash
   host=example.com
   port=443
   ```

2. Then run the `openssl s_client` command to inspect the certificate of the target server:
   ```bash
   openssl s_client -showcerts -servername "$host" -connect "$host:$port" </dev/null 2>/dev/null | openssl x509 -noout -ext subjectAltName
   ```

3. If the output is empty, then the certificate has no SAN extension entries and must be replaced.

### Fixing Invalid Target Server Certificates

If the target server's certificate is invalid and does not contain a SAN extension entry, consider the following:

- **Replace the invalid certificate**: SAN extension entries can only be added by issuing a new certificate signing request with the appropriate extensions, and getting the CA to issue the certificate again
- **Disable SSL validation (temporary workaround)**: If unable to replace the invalid certificate, turn off the Validate SSL behavior setting for a test, as follows:
  1. Go to your test **Editor**
  2. Expand **Test Settings** and navigate to **Behaviors** tab
  3. Turn off the **Validate SSL** behavior

This will allow the Radar agent to communicate with the target server and ignore any SSL/TLS certificate issues.

---

## Run as Container

Run Radar Agent as a Docker or Kubernetes container, including pulling images, configuring with local files, custom certificates, client certificates, and proxy settings.

**Use when**: Running Radar Agent as a Docker or Kubernetes container or pulling images, configuring with local files, custom certificates, client certificates, and proxy settings.

### Container Deployment

- **Pull Images**: Pull Radar Agent images
- **Local Files**: Configure with local files
- **Custom Certificates**: Use custom certificates
- **Client Certificates**: Configure client certificates
- **Proxy Settings**: Set up proxy configuration

---

## Run as Service or Daemon

Run Radar Agent as a Linux daemon or Windows service, including using nohup, GNU Screen, systemd, and NSSM utility for service management.

**Use when**: Running Radar Agent as a Linux daemon or Windows service or using nohup, GNU Screen, systemd, and NSSM utility for service management.

### Service Management

- **Linux**: Use nohup, GNU Screen, or systemd
- **Windows**: Use NSSM utility
- **Service Configuration**: Configure service settings

---

## Harbor ID and Ship ID

Locate Harbor ID (Private Location ID) and Ship ID (Agent ID) in BlazeMeter settings for use in API calls and configuration.

**Use when**: Locating Harbor ID and Ship ID in BlazeMeter settings or obtaining Private Location ID and Agent ID for use in API calls and configuration.

### Finding IDs

- **Harbor ID**: Private Location ID
- **Ship ID**: Agent ID
- **Location**: Find in BlazeMeter settings
- **Usage**: Use in API calls and configuration

---

## Manual Update of Images

Manually update Docker images for private locations when auto-update is disabled, including checking versions, pulling images, and installing with proper tags.

**Use when**: Manually updating Docker images for private locations or when auto-update is disabled and checking versions, pulling images, and installing with proper tags.

### Update Process

1. **Check Versions**: Verify current and available versions
2. **Pull Images**: Pull updated images
3. **Install**: Install with proper tags

---

## RSS Subscription for Image Updates

Subscribe to RSS feeds for private location image updates, including generating API tokens, accessing RSS feeds, and including browser images in feeds.

**Use when**: Subscribing to RSS feeds for private location image updates or generating API tokens, accessing RSS feeds, and including browser images in feeds.

### RSS Setup

- **API Tokens**: Generate API tokens
- **RSS Feeds**: Access RSS feeds
- **Browser Images**: Include browser images in feeds

---

## Documentation References

For detailed information about Radar Agent, use the BlazeMeter MCP help tools:

**Radar Agent**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `private-locations-radar-agent-overview` (overview)
  - `private-locations-radar-agent-changelog` (changelog)
  - `private-locations-radar-agent-connection-errors` (connection errors)
  - `private-locations-radar-agent-sso-login-error` (SSO login)
  - `private-locations-radar-agent-http-https-proxy-setup` (proxy setup)
  - `private-locations-radar-agent-high-availability-failover-capability` (HA/failover)
  - `private-locations-handle-radar-agent-availability-issues` (availability)
  - `private-locations-remote-agent-expired` (expired)
  - `private-locations-auto-restart-radar-agent-on-linux` (auto-restart)
  - `private-locations-radar-agent-support-for-https-common-name-in-x509-certificates` (HTTPS certificates)
  - `private-locations-radar-agent-certificates.htm` (certificates)
  - `private-locations-improve-timeout-handling.htm` (timeout handling)
  - `private-locations-run-radar-agent-as-container` (container)
  - `private-locations-run-radar-agent-as-service-or-daemon` (service/daemon)
  - `private-locations-manual-update-of-images` (manual update)
  - `private-locations-enable-rss-subscription-for-image-updates` (RSS subscription)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["private-locations-radar-agent-overview", "private-locations-radar-agent-changelog", "private-locations-radar-agent-connection-errors", "private-locations-radar-agent-sso-login-error", "private-locations-radar-agent-http-https-proxy-setup", "private-locations-radar-agent-high-availability-failover-capability", "private-locations-handle-radar-agent-availability-issues", "private-locations-remote-agent-expired", "private-locations-auto-restart-radar-agent-on-linux", "private-locations-radar-agent-support-for-https-common-name-in-x509-certificates", "private-locations-radar-agent-certificates.htm", "private-locations-improve-timeout-handling.htm", "private-locations-run-radar-agent-as-container", "private-locations-run-radar-agent-as-service-or-daemon", "private-locations-manual-update-of-images", "private-locations-enable-rss-subscription-for-image-updates"]}`

