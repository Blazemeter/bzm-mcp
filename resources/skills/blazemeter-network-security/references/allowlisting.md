# Allowlisting BlazeMeter Infrastructure

## Allowlisting BlazeMeter Engines

Configure allowlists for BlazeMeter cloud engines to communicate with application servers, including IP ranges for Debug Test Engines, AWS, GCE, Azure, and Functional GUI Testing locations.

**Use when**: Configuring firewall rules for BlazeMeter cloud engines, working from behind corporate firewalls, or when application servers need to allow incoming connections from BlazeMeter test engines.

### Overview

BlazeMeter cloud engines require network access to your application servers. Configure firewall rules to allow traffic from BlazeMeter IP ranges based on the cloud provider and location where tests are executed.

**Note**: To ensure BlazeMeter's cloud engines can communicate with your application server, you may need to allowlist the relevant IP ranges. Here you'll find the available CIDRs (Classless Inter-Domain Routing) for the IPs used by BlazeMeter cloud engines.

### IP Ranges by Location Type

To ensure BlazeMeter's cloud engines can communicate with your application server, you may need to allowlist the relevant IP ranges. Here you'll find the available CIDRs (Classless Inter-Domain Routing) for the IPs used by BlazeMeter cloud engines.

#### Debug Test Engines

IP addresses for debug test execution. Used for troubleshooting and debugging tests. These are specific IP addresses that need to be allowlisted:

- 35.245.251.194, 35.245.232.79
- 35.245.160.5, 34.64.185.248
- 35.194.77.139, 35.198.210.225
- 35.194.88.224, 35.244.89.90
- 35.245.24.75, 35.203.78.93
- 35.221.19.213, 35.234.97.23
- 35.245.0.140, 34.76.64.195
- 35.245.200.243, 35.246.9.61
- 35.245.217.101, 35.231.2.168
- 35.245.242.163, 35.236.93.4
- 34.86.94.3, 34.82.42.213
- 35.245.162.86, 34.86.129.102
- 34.86.55.231, 34.86.129.100
- 34.86.18.245, 34.86.129.101
- 34.86.167.17
- 35.199.23.208

#### AWS Locations

Amazon Web Services cloud locations. Multiple regions available (us-east, us-west, eu-west, etc.). IP ranges vary by region and availability zone.

**Getting AWS IP Ranges:**
- [Downloadable list of AWS Engines in JSON format](https://ip-ranges.amazonaws.com/ip-ranges.json)
- Find the [AWS EC2 Region code<>Name mapping chart](https://docs.aws.amazon.com/general/latest/gr/rande.html) here

#### GCE (Google Cloud Engine) Locations

Google Cloud Platform locations. Multiple regions available. IP ranges for Google Cloud infrastructure.

**Getting GCE IP Ranges:**
- [Downloadable list of GCE Engines in JSON format](https://www.gstatic.com/ipranges/cloud.json)
- For more information, see [Where can I find Compute Engine IP ranges? (in the Google Cloud documentation)](https://cloud.google.com/compute/docs/faq#find_ip_range)
- Find the [Google Cloud Region code<>Name mapping chart](https://cloud.google.com/about/locations/) here

#### Azure Locations

Microsoft Azure cloud locations. Multiple regions available. IP ranges for Azure infrastructure.

**Getting Azure IP Ranges:**
- Downloadable list [via this link (XML format)](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519)
- Find the [Azure Region code<>Name mapping chart](https://azure.microsoft.com/en-us/regions/) here

#### Functional GUI Testing Locations

Locations dedicated to functional GUI testing. Separate IP ranges from performance testing engines. Used for Selenium-based functional tests.

**US East (Virginia) - Default Location:**
- CIDR: 34.86.129.64/26

**US West (Oregon):**
- 34.82.137.166
- 35.247.48.254
- 35.197.44.138
- 34.83.234.170
- 34.82.232.108
- 35.185.206.63
- 34.83.173.62
- 34.83.79.24

**EU West (London):**
- 35.189.104.226
- 35.242.133.63
- 35.246.94.188
- 35.230.145.198
- 35.234.150.228
- 35.234.156.180
- 35.234.138.9
- 35.242.129.55

### Configuration Steps

1. **Identify Test Locations**: Determine which cloud providers and regions your tests will use
2. **Obtain IP Ranges**: Get current IP ranges for selected locations
3. **Configure Firewall Rules**: Add IP ranges to firewall allowlists
4. **Test Connectivity**: Verify that BlazeMeter engines can reach your application servers
5. **Monitor Changes**: IP ranges may change; monitor for updates

### Best Practices

- **Use Specific IP Ranges**: Allowlist only the IP ranges you need for your test locations
- **Regular Updates**: IP ranges may change; review and update allowlists periodically
- **Document Changes**: Keep track of IP range changes and firewall rule updates
- **Test After Changes**: Verify connectivity after any firewall rule modifications

---

## Allowlisting BlazeMeter Behind Firewall

Master guide for allowlisting BlazeMeter URLs, engines, API Monitoring infrastructure, and Private Locations to work from behind corporate firewalls.

**Use when**: Working from behind corporate firewalls, configuring network security policies for BlazeMeter access, or when corporate network policies require explicit allowlisting of external services.

### Overview

When working from behind corporate firewalls, you need to allowlist multiple BlazeMeter components to ensure proper functionality. This includes web URLs, API endpoints, test engines, and infrastructure components.

### Components to Allowlist

In order to fully utilize BlazeMeter from behind your firewall, you may need to allowlist some addresses in order to prevent connection issues. What you need to allowlist depends on what you're trying to do.

#### BlazeMeter URLs

BlazeMeter's own URLs are not associated with static IP addresses; rather, our IPs change periodically. That means if you need to allowlist our URLs, you must allowlist by URL instead of by IP address.

**Our URLs include:**
- `a.blazemeter.com`
- `data.blazemeter.com`
- `mock.blazemeter.com`
- `bard.blazemeter.com`
- `auth.blazemeter.com`

#### BlazeMeter Engines

BlazeMeter cloud engines can be allowlisted using the IP ranges of our engine providers. Check out our guide [Allowlisting BlazeMeter Engines](https://help.blazemeter.com/docs/answers/answers-allowlist-blazemeter-engines.html) for full details.

If you'd like an alternative to allowlisting the IP ranges of our public engines, then check out our blog article [Top 3 Options for Running Performance Tests Behind Your Corporate Firewall](https://www.blazemeter.com/blog/top-three-options-running-performance-tests-behind-your-corporate-firewall/).

#### BlazeMeter API Monitoring URLs

Due to the elastic nature of BlazeMeter API Monitoring infrastructure, we do not publish lists of IP addresses for allowlists. However, between the [regions](https://help.blazemeter.com/docs/guide/api-monitoring-global-locations.html) used and depending on the load, you could see a wide variety of source IPs at any given time. Also see [API Monitoring: IP Addresses & Allowlisting](https://help.blazemeter.com/docs/guide/api-monitoring-ip-addresses-allowlisting.html) for more information.

#### Private Locations

If you elect to setup your own Private Locations -- what we call on-premise agents or engines that you setup yourself -- you'll need to know everything that must be allowlisted to allow Private Locations to function, all of which is detailed in our [Private Locations System Requirements](https://help.blazemeter.com/docs/guide/private-locations-system-requirements.html) guide.

### Network Requirements

#### Outbound Connections
- HTTPS (port 443) to BlazeMeter domains
- WebSocket connections for real-time features
- API communication endpoints

#### Inbound Connections (if using Private Locations)
- Agent registration and heartbeat endpoints
- Test execution coordination endpoints

### Configuration Steps

1. **Identify Required URLs**: List all BlazeMeter URLs your organization needs
2. **Configure Firewall Rules**: Add URLs and IP ranges to firewall allowlists
3. **Test Connectivity**: Verify access to BlazeMeter web application and API
4. **Configure Proxy (if needed)**: Set up proxy settings if required by corporate policy
5. **Document Configuration**: Keep track of firewall rules and proxy settings

### Best Practices

- **Use Wildcard Domains**: Allowlist `*.blazemeter.com` for easier management
- **Monitor Access**: Track firewall logs for blocked connections
- **Coordinate with IT**: Work with network security team for proper configuration
- **Test Regularly**: Verify connectivity after network changes

---

## API Monitoring IP Addresses Allowlisting

Understand IP address requirements for API Monitoring tests and configure allowlists using Radar Agent for known source IPs.

**Use when**: Configuring firewall rules for API Monitoring tests, using Radar Agent with known source IP addresses, or when your API endpoints require IP-based allowlisting.

### Overview

Due to the elastic nature of the BlazeMeter API Monitoring infrastructure, we do not publish lists of IP addresses for allowlists. Between the [regions](https://help.blazemeter.com/docs/guide/api-monitoring-global-locations.html) that we use and depending on the load, you could see a wide variety of source IPs at any given time.

### IP Address Requirements

#### Cloud-Based API Monitoring
- IP ranges vary by execution location
- Dynamic IP addresses from BlazeMeter cloud infrastructure
- May require broader IP range allowlisting
- IP addresses change dynamically based on load and regions

#### Radar Agent (Private Locations)

You can get a known source IP address for requests in your tests by using the [Radar Agent](https://help.blazemeter.com/docs/guide/private-locations-radar-agent-overview.html) on a host you control. The agent also allows you to send test requests from within your own infrastructure. Once running the agent acts just like any of the cloud locations and can be enabled within a test or shared [environment](https://help.blazemeter.com/docs/guide/api-monitoring-managing-configuration-with-environments.html).

**Benefits of Using Radar Agent:**
- **Known Source IP Addresses**: Get predictable IP addresses from your Private Location
- **Static or Predictable IPs**: Easier to configure firewall rules
- **Better Security**: Narrower allowlist reduces attack surface
- **Easier Troubleshooting**: Known source IPs simplify network debugging
- **Infrastructure Control**: Send test requests from within your own infrastructure

### Configuration with Radar Agent

#### Setting Up Radar Agent for Known Source IPs
1. **Set Up Radar Agent**: Install and configure Radar Agent on a host you control
2. **Identify Private Location IP**: Get the public IP address of your Private Location
3. **Configure Firewall**: Allowlist the known source IP addresses
4. **Enable in Test or Environment**: Enable Radar Agent within a test or shared environment
5. **Test Connectivity**: Verify API Monitoring tests can reach your endpoints

### Firewall Rule Setup

1. **Identify Source IPs**: Determine IP addresses used by API Monitoring tests
2. **Configure Allowlist**: Add IP addresses to firewall allowlists
3. **Set Port Rules**: Allow HTTPS (443) and HTTP (80) as needed
4. **Test Access**: Verify API Monitoring tests can reach your endpoints
5. **Monitor Logs**: Check firewall logs for blocked connections

### Best Practices

- **Use Private Locations**: Private Locations provide known source IPs for easier firewall configuration
- **Document IP Changes**: Keep track of IP address changes
- **Regular Testing**: Verify firewall rules work correctly after changes
- **Coordinate with Security**: Work with security team for proper configuration

---

## Documentation References

For detailed information about allowlisting BlazeMeter infrastructure, use the BlazeMeter MCP help tools:

**Allowlisting BlazeMeter Engines**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-allowlist-blazemeter-engines`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-allowlist-blazemeter-engines"]}`

**Allowlisting BlazeMeter Behind Firewall**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-allowlisting-blazemeter`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-allowlisting-blazemeter"]}`

**API Monitoring IP Addresses**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-ip-addresses-allowlisting`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-ip-addresses-allowlisting"]}`

