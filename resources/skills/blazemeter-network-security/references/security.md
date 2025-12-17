# API Monitoring Security

## API Monitoring Security

Implement security best practices for API Monitoring, including HTTPS enforcement, authentication tokens, and secure data handling.

**Use when**: Implementing security best practices for API Monitoring tests, handling sensitive data in API tests, or when configuring secure API test execution.

### Overview

API Monitoring tests often interact with production or sensitive APIs. Implementing security best practices ensures that sensitive data is protected, authentication is secure, and API tests follow security guidelines.

**Security is our top priority. If you think you've found a vulnerability in any BlazeMeter API Monitoring service, please contact us.**

### How We Keep You Safe

BlazeMeter uses best practices for Internet security. This helps ensure that your data is safe, secure, and available only to authorized users. Your data will be completely inaccessible to anyone else, unless you explicitly choose to share that data with the public.

**HTTPS Enforcement:**
- BlazeMeter API Monitoring enforces secure HTTPS for our entire website, including the public (unauthenticated) parts of the site
- All communications with the API Monitoring API are also protected with SSL
- We also use HTTP Strict Transport Security to ensure your web browser never interacts with BlazeMeter over insecure HTTP

**User Authentication:**
- BlazeMeter API Monitoring provides each user in your organization with a unique user name and password
- These credentials must be entered to access your organization's data

### Security Best Practices

#### HTTPS Enforcement

**Always Use HTTPS**:
- Configure all API calls to use HTTPS (port 443)
- Avoid HTTP (port 80) for sensitive endpoints
- Verify SSL/TLS certificates are valid

**For this reason, we recommend that you use HTTPS whenever possible.** If an API gives you the choice, you should always use HTTPS.

**Important Note:**
BlazeMeter can be used to inspect traffic to APIs that communicate via plain-text HTTP or encrypted HTTPS. When you use API Monitoring with a plain-text HTTP API, all network traffic between your server and BlazeMeter will be sent in plain text, as will all network traffic between BlazeMeter and your API provider.

**Note**: This is an important security consideration. Always use HTTPS when possible to protect sensitive data in transit.

**SSL Certificate Validation**:
- Enable SSL certificate validation in API Monitoring tests
- Use valid SSL certificates for test endpoints
- Handle certificate errors appropriately

#### Authentication Tokens

**Secure Token Storage**:
- Use BlazeMeter Secrets Management for storing authentication tokens
- Never hardcode tokens in test scripts
- Rotate tokens regularly

**Token Types**:
- API keys
- OAuth tokens
- Bearer tokens
- JWT tokens

**Token Usage**:
- Include tokens in request headers
- Use appropriate authentication methods
- Handle token expiration gracefully

#### Secure Data Handling

**Sensitive Data Protection**:
- Use Secrets Management for sensitive data (passwords, API keys, tokens)
- Avoid logging sensitive data in test results
- Mask sensitive data in reports

**Data Encryption**:
- Encrypt sensitive data in transit (HTTPS)
- Use secure data storage for test data
- Implement data encryption at rest when applicable

#### Request and Response Security

**Secure Headers**:
- Use appropriate security headers in requests
- Validate security headers in responses
- Implement CORS policies correctly

**Input Validation**:
- Validate input data in API tests
- Sanitize user inputs
- Prevent injection attacks

### Implementation

#### Configure HTTPS for All API Calls

1. **Update Test Steps**: Change HTTP URLs to HTTPS
2. **Verify Certificates**: Ensure SSL certificates are valid
3. **Handle Redirects**: Configure HTTPS redirect handling
4. **Test Connectivity**: Verify HTTPS connections work correctly

#### Use Authentication Tokens Securely

1. **Store in Secrets**: Use BlazeMeter Secrets Management
2. **Reference in Tests**: Reference secrets in test steps
3. **Rotate Regularly**: Update tokens periodically
4. **Monitor Usage**: Track token usage and expiration

#### Handle Sensitive Data Appropriately

1. **Identify Sensitive Data**: Determine what data is sensitive
2. **Use Secrets Management**: Store sensitive data securely
3. **Mask in Reports**: Configure data masking in test results
4. **Limit Access**: Restrict access to sensitive test data

#### Follow Security Guidelines

1. **Review Security Policies**: Understand organizational security requirements
2. **Implement Best Practices**: Follow industry security standards
3. **Regular Audits**: Review security configurations periodically
4. **Update Practices**: Keep security practices current

### Secrets Management

Use Secrets Management to manage values that are encrypted and hidden from users, but can still be read and used by API Monitoring test scripts. The Secrets Management feature for API Monitoring Tests requires a qualifying plan; check your plan or [contact Sales to get started](mailto:sales-blazemeter@perforce.com).

#### How Secret Management Works

The Secrets feature allows API Monitoring **team owners** and administrators to create and manage variables with a key/value pair, where the value is encrypted and **hidden**, and allows all team members to use the variables in their tests with the new built-in function `{{get_secret(key)}}`.

In the same way you might have a `.env` or `config` file in your app that includes sensitive variables you don't want to be checked in to your project's version control repository. The Secrets feature can help you keep sensitive information secure.

**Examples of Common Use Cases:**
- You might have an API key or access token that you do not wish to be visible in your tests for security reasons
- You are working with an API that requires authentication credentials that you don't want exposed
- You don't want to send certain information to third-party integrations

#### Manage Secrets

As a team owner or admin, you can manage secrets at the team level and at the bucket level. Secrets created at the team level can be used by all tests in all buckets. Secrets created at the bucket level can be used only by tests within that bucket.

**Secrets have a 4096-character limit.**

#### Create Secrets at the Team Level

As an API Monitoring team owner or admin, you can create secrets at the team level.

**Steps:**
1. Go to the **API Monitoring** tab
2. Click your profile on the top-right and select **Secrets** from the dropdown list
3. On the **Secrets** page, click **Add Secret**. A new secret key/value pair is created
4. Enter the name that will be used to access the secret throughout your tests
5. Enter the value
6. Click **Save Changes**

#### Edit and Delete Secrets at the Team Level

**To edit an existing secret:**
- Go to the **Secrets** page and click **Edit** next to the secret you wish to change the value for
- Enter the new value and click **Save Changes**

**To delete a secret:**
- Go to the **Secrets** page and click the **x** next to the secret that you wish to delete

#### Create Secrets at the Bucket Level

You can create secrets at the bucket level if you have appropriate RBAC privileges. If you don't have permission to create secrets, contact your team owner or administrator.

**Steps:**
1. In **API Monitoring**, click **Bucket Settings** in the top right corner. The **Bucket Settings** page opens
2. Scroll down to the **Bucket Secrets** section
3. Click **Add Secret**. Secrets on a bucket level can't have the same name as secrets on the team level
4. Enter the **Name** and **Value**. **Description** is optional
5. Click **Save Changes**

#### Edit and Delete Secrets at the Bucket Level

**To edit an existing secret:**
- Go to the **Bucket Settings** page and scroll down to the **Bucket Secrets** section
- Click **Edit** next to the secret that you wish to change the value for
- Enter the new value, and click **Save Changes**

**To delete a secret:**
- Click the **x** next to the secret that you wish to delete

Team owners and admins can create roles with various permissions, for example, the View or Manage Bucket Permissions, and assign the roles to team members. For more information, see [Role-Based Access Control](https://help.blazemeter.com/docs/guide/api-monitoring-role-based-access-control.html).

#### Use Secrets in Tests

To use secrets in your tests, you'll have to use a built-in function:

| Variable/Function | Description |
|-------------------|-------------|
| `{{get_secret(key)}}` | Retrieves the secret value for the `key` name |

To see what team level secrets are available in your BlazeMeter API Monitoring account, you'll need to check with your team owner which can be found in the [Team Members](https://www.runscope.com/teams) page. To see what secrets are available at the bucket level, go to the Bucket Settings page.

This built-in function can be used just like any other BlazeMeter API Monitoring built-in functions, which means you can add it to your environment settings, initial variables, pre-request/post-response scripts, etc. To use it in scripts, make sure you're calling the function as `get_secret(key)` without the parenthesis:

```javascript
// Example pre-request / post-response script
request.params.push({name:"api_key", value: get_secret("secret_key")});
```

**Important Security Feature:**
Whenever you have a step in your API tests that's using the `get_secret` function or is referencing a variable that was set using this function, **the results for that step will omit any information that might contain the value for that secret**, including the headers and body for both request and response. This also applies to any step that has a pre-request script or post-response script as it might reveal the value of the secret value.

**Note**: This automatic masking ensures that secret values are never exposed in test results, even if they're used in scripts or variables. This is a critical security feature that protects sensitive credentials.

#### Bucket Authentication

API Monitoring buckets are writable given that you know the randomly generated bucket key; however, data can only be viewed by the bucket owner. You may optionally enable secondary authentication for a bucket. Authenticated buckets require an additional secret token to be supplied in either an HTTP header or query string parameter to write to a bucket. If you would like to enable authentication tokens for your buckets, you may do so by enabling them in the Bucket Settings page on your dashboard.

### Data Masking

#### Configure Data Masking

**Mask Sensitive Data in Reports**:
1. Identify sensitive data fields
2. Configure masking rules
3. Apply masking to test results
4. Verify masking works correctly

**Masked Data Types**:
- Authentication tokens
- Passwords
- Credit card numbers
- Personal information

### Contacting BlazeMeter Support

If you have found a security vulnerability in a BlazeMeter web site or service, or if you have further questions about your data's security, send an email to [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com?subject=security vulnerability in BlazeMeter API Monitoring) or contact the Account Team.

Your email will be reviewed promptly. We request that you not publicly disclose the issue until it has been addressed by BlazeMeter.

### Security Checklist

- [ ] All API calls use HTTPS
- [ ] SSL certificates are validated
- [ ] Authentication tokens stored in Secrets Management
- [ ] Sensitive data is masked in reports
- [ ] Security headers are configured correctly
- [ ] Input validation is implemented
- [ ] Access to sensitive data is restricted
- [ ] Security practices are documented
- [ ] Bucket authentication enabled if needed
- [ ] Secrets are managed at appropriate level (team or bucket)

---

## API Monitoring IP Addresses and Allowlisting

Due to the elastic nature of the BlazeMeter API Monitoring infrastructure, we do not publish lists of IP addresses for allowlists. Between the [regions](skill-blazemeter-api-monitoring://references/configuration.md) that we use and depending on the load, you could see a wide variety of source IPs at any given time.

**Use when**: Configuring allowlists for API Monitoring tests, understanding IP address ranges, or using Radar Agent for known source IP addresses.

### Overview

You can get a known source IP address for requests in your tests by using the [Radar Agent](skill-blazemeter-private-locations://references/radar-agent.md) on a host you control. The agent also allows you to send test requests from within your own infrastructure. Once running the agent acts just like any of the cloud locations and can be enabled within a test or shared [environment](skill-blazemeter-api-monitoring://references/configuration.md).

### Additional Resources

- [Allowlisting BlazeMeter](skill-blazemeter-network-security://references/allowlisting.md)
- [Radar Agent Documentation](skill-blazemeter-private-locations://references/radar-agent.md)

### Documentation References

For detailed information about API Monitoring IP addresses and allowlisting, use the BlazeMeter MCP help tools:

**API Monitoring IP Addresses and Allowlisting**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-ip-addresses-allowlisting`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-ip-addresses-allowlisting"]}`

---

## Documentation References

For detailed information about API Monitoring security, use the BlazeMeter MCP help tools:

**API Monitoring Security**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-security`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-security"]}`

**Secrets Management**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-monitoring-secrets-management` (for API Monitoring) or `administration-secrets.htm` (for general administration)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-monitoring-secrets-management"]}`

