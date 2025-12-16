# API Monitoring Troubleshooting

## Radar Agent Auth Fail

Troubleshoot and resolve authentication failures when installing on-premise API Monitoring Radar Agent, including creating Runscope API tokens and configuring agent authentication.

**Use when**: Troubleshooting authentication failures when installing on-premise API Monitoring Radar Agent, creating Runscope API tokens, or configuring agent authentication.

### Symptom

When installing an on-premise API Monitoring Radar Agent, you may encounter an "invalid username/password" error message.

### Reason

The Radar Agent requires a **Runscope API token** in order to authenticate.

### Solution

Run the agent program with the API token via the `--token` argument, then save the agent's configuration to a file.

### Creating Runscope API Tokens

To create the required API token, follow these steps:

1. **Log into API Monitoring**
2. **Click your API Monitoring icon** in the upper-right below your name, then select **Personal Information**
3. **On the left side click Applications**. The [https://www.runscope.com/applications](https://www.runscope.com/applications) page opens
4. **Click Create Application**. All fields are required
5. **Provide any Name** for the app that reflects its purpose (for example, "API Monitoring Agent Token")
6. **Provide any Website URL and Callback URL**. It can be completely imaginary, so long as it "looks like" a URL to satisfy the parser on that page. Normally this application creation process is used to set up an [application for use with an OAuth flow with a third-party app](https://www.runscope.com/docs/api/authentication), so that app can access API Monitoring. But in this case, you use it to generate a Runscope API token for [general Runscope API usage](https://www.runscope.com/docs/api), and the URLs are ignored
7. **Click the Create Application button**
8. **On the next page, scroll down** until you see the **Personal Access Token**. This is the UUID that is your API token which you'll use with the agent

### Launching the Agent

Now that you have your token, launch your agent like this:
```
/path/to/runscope-radar --token=whatever-your-token-is
```

If you are on multiple API Monitoring "Teams", you are prompted to choose which "Team" to associate the agent with. If you are on only one Team, no such prompt will occur.

Save the agent's configuration to a file:
```
/path/to/runscope-radar -f /path/to/radar.conf
```

**Note**: The agent configuration file contains various parameters, including the API token (which you provided) as well as a unique agent ID that was generated, and the Team ID that the agent is associated with. You can read more about the agent and its options here: [https://www.runscope.com/docs/api-testing/agent/](https://www.runscope.com/docs/api-testing/agent/)

You can now execute your API Monitoring test.

---

## SSL Certificate

Diagnose and resolve SSL certificate errors in API Monitoring tests, including issues with unsupported CAs, incomplete certificate chains, and SSL verification configuration.

**Use when**: Diagnosing and resolving SSL certificate errors in API Monitoring tests, troubleshooting unsupported CAs, incomplete certificate chains, or SSL verification issues.

### Symptom

You see the following SSL error when running an [API Monitoring](https://help.blazemeter.com/docs/guide/api-monitoring-create-your-first-api-monitoring-test.html) test:

```
Failed: Error contacting host SSL: certificate signed by unknown authority
```

### Solution

To help debug this issue, we recommend using [SSLLabs SSL Server Test](https://www.ssllabs.com/ssltest/index.html) tool. Open the tool in a new tab, add your hostname, hit *Submit*, and check the results of the test for any warnings and errors.

The two most common causes you're seeing the error, and how to fix them, are:

The two most common causes you're seeing the error, and how to fix them, are:

#### Certificate From Unsupported CA

The certificate is signed by an authority not supported by API Monitoring. Check our [Supported SSL CA Certificates for Radar Agent](https://help.blazemeter.com/docs/guide/private-locations-supported-ssl-ca-certificates-for-radar-agent.html) article for more information. If your certificate authority is not on that list, you can fix the issue by:

- **If you control the server**: You can get a new certificate with one of the supported authorities in our list and update your server
- **If you're using a 3rd-party API**: You can reach out to your provider to see if they can change the certificate or offer an alternative solution
- **If the test is for functionality of the API, and not security**: You can disable SSL verification in your test by going to your API Monitoring environment -> Behaviors -> Validate SSL, or for all tests in your bucket by going to Bucket Settings -> Traffic Inspector -> Verify SSL Certificates

#### Incomplete Certificate Chain

The server has an **incomplete certificate chain**. That means the server is not providing the necessary intermediate certificates. Browsers and some clients will automatically download them, but many API/HTTP clients won't. You can fix this issue by:

- **If you have control of the server**: You'll need to bundle the missing certificates. You can find instructions on how to do that by searching: "(name of your certificate issuer) bundle intermediate certificates" ([Example](https://www.google.com/search?q=godaddy+intermediate+certificate+bundle))
- **If you're using a 3rd-party API**: You can reach out to your provider to see if they can change the certificate or offer an alternative solution
- **If the test is for functionality of the API, and not security**: You can disable SSL verification in your test by going to your API Monitoring environment -> Behaviors -> Validate SSL, or for all tests in your bucket by going to Bucket Settings -> Traffic Inspector -> Verify SSL Certificates


### Best Practices

- **Use Valid Certificates**: Always use valid SSL certificates from trusted CAs
- **Complete Certificate Chains**: Ensure all intermediate certificates are included
- **Regular Certificate Updates**: Monitor certificate expiration and renew timely
- **Production Security**: Never disable SSL verification in production tests

---

## Debug Test

Debug why a test worked previously but fails now, including checking logs, static data issues, site status, protocol changes, network connectivity, CSV data usage, and regular expression matching.

**Use when**: Debugging why a test worked previously but fails now, checking logs, investigating static data issues, site status, protocol changes, network connectivity, CSV data usage, or regular expression matching problems.

### Overview

When a previously working API Monitoring test starts failing, systematic debugging is required to identify the root cause. Common causes include changes to the API, test data issues, network problems, or configuration changes.

### Debugging Checklist

#### 1. Check Test Logs
- **Browse to the specific Test Reports -> Logs -> jmeter-console0.log Tab** and click **Download**
- Check for warning and error type messages
- Resolve the errors based on details mentioned in log file

**Note**: The log file is the first place to look when debugging why a test that worked previously is now failing. It contains detailed information about what happened during test execution.

#### 2. Review Static Data
- **Do you have static data in your request body that refers to time beyond 24 hours or calendar days?** Then parametrize the script using [synthetic test data](https://help.blazemeter.com/docs/guide/test-data-generate-synthetic.html)

#### 3. Verify Site Status
- **Is your target site temporarily down?** Check site status before running the test

#### 4. Check Protocol Changes
- **Was there a change in protocol or URL of your target site from that recorded in your script?** Check the protocol in the script and change it to a working one if required

#### 5. Test Network Connectivity
- **Low or no network connectivity?** Check your internet connectivity, direct or proxy connections

#### 6. Review CSV Data Usage
- **Was the data in the CSV file for one-time use and has already been used?** Change the CSV file with a fresh working data set or edit your script to use [synthetic](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html) functions to generate data in the required format

#### 7. Verify Regular Expression Matching
- **Are regular expressions not matching due to changes in site code?** Debug your script in JMeter, use the Regular Expression tester from the 'view result tree' listener and update the regular expressions where required


### Best Practices

- **Regular Test Maintenance**: Review and update tests regularly
- **Monitor API Changes**: Stay informed about API changes
- **Version Control**: Keep test configurations in version control
- **Documentation**: Document test dependencies and requirements

---

## Documentation References

For detailed information about API Monitoring troubleshooting, use the BlazeMeter MCP help tools:

**Radar Agent Authentication**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-api-monitoring-radar-agent-auth-fail`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-api-monitoring-radar-agent-auth-fail"]}`

**SSL Certificate Issues**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-api-monitoring-ssl-certificate`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-api-monitoring-ssl-certificate"]}`

**Debug Test**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-debug-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-debug-test"]}`

