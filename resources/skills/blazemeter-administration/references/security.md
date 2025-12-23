# Security Settings

## Managing Account Security

As the initial account Owner, you are the Admin and control security settings, such as the session and API key expiration timeouts, according to your companies requirements.

**Use when**: Managing account security settings as an Admin, configuring API keys expiration period, or setting session timeout settings for idle user logout.

### Admin Account

When you create a BlazeMeter Account, you have specified an email address and password to sign in to [BlazeMeter](https://a.blazemeter.com/). When you sign in using these credentials, you are accessing your BlazeMeter site as an Admin. Your Admin account has access to all services, settings, and resources in your account.

### API Keys Expiration Period

As Admin, define the maximum expiration date of all API Keys created in this account.

1. Log in to your BlazeMeter Account. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Click **Account > Security**
3. In the **API Keys Expiration Period** section, select an **Expiry** time period:
   - 1 Month
   - 3 Months
   - 6 Months
   - 1 Year
   - 10 Years
4. Click **Set** to save

**Note**: The default is 10 years.

### Session Timeout

As Admin, set a session timeout after which idle users are logged out.

1. Log in to your BlazeMeter Account. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Click **Account > Security**
3. Enable the **Session Timeout** section
4. Select a time unit: Either **Minutes**, **Hours**, or **Days**
5. Enter an idle timeout as a number
6. Click **Set** to save

**Note**: The default is 30 days.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Security**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `administration-security` (account security)
  - `integrations-saml-sso-integration` (SAML SSO Integration)
  - `administration-changing-your-email-address` (change email)
  - `administration-changing-your-password` (change password)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-security", "administration-changing-your-email-address", "administration-changing-your-password"]}`

**Administration Secrets**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-secrets.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-secrets.htm"]}`

**SAML SSO Integration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-saml-sso-integration`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-saml-sso-integration"]}`

---

## SAML SSO Integration

BlazeMeter supports integration with Security Assertion Markup Language 2.0 (SAML 2.0), an XML-based protocol used by web browsers to allow for Single Sign-On (SSO), which enables a user to securely log in to multiple systems via a single portal and a single internal organization account.

**Use when**: Setting up Single Sign-On (SSO) for your organization, enabling users to log in to BlazeMeter using their organization's internal account, or managing user access through SAML SSO.

### Overview

A key advantage of SAML SSO is that users do not need to register new BlazeMeter accounts -- That's one less login to remember! It also ensures that all members of your organization will be able to utilize BlazeMeter while your organization's own internal admin will manage who may log into it.

### Setup Process

To integrate SAML SSO with BlazeMeter, either [open a support ticket](https://portal.perforce.com/s/contactsupport) with BlazeMeter Support or email us directly at [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com?subject=SSO), requesting SSO integration. BlazeMeter Support will send you the required metadata and instructions based on your unique environment.

### Benefits

- **Single Sign-On**: Users can log in to BlazeMeter using their organization's internal account
- **Centralized Management**: Organization admins manage user access through their internal systems
- **No Additional Accounts**: Users don't need to create separate BlazeMeter accounts
- **Enhanced Security**: Leverage your organization's existing security policies and authentication mechanisms

### Documentation References

For detailed information about SAML SSO integration, use the BlazeMeter MCP help tools:

**SAML SSO Integration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `integrations-saml-sso-integration`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["integrations-saml-sso-integration"]}`

---

### Security Settings

- **API Keys Expiration**: Configure expiration period for API keys
- **Session Timeout**: Set idle user logout timeout
- **Security Policies**: Manage account-level security policies

### API Key Management

- Generate new API keys
- Configure expiration periods
- Regenerate existing keys
- Revoke compromised keys

### Session Management

- Configure session timeout duration
- Enable automatic logout for idle users
- Manage active sessions

---

## Administration Changing Your Email Address

To change the email address associated with your account, contact [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com?subject=Change email address associated with my account) and request the email address change.

State the current email address associated with your account, and the new one.

**Use when**: Changing the email address associated with your BlazeMeter account.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Changing Your Email Address**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-changing-your-email-address`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-changing-your-email-address"]}`

---

## Administration Changing Your Password

You can change your password in two ways:
- Inside the app through [Personal Settings](#inside-the-app-personal-settings)
- Outside the app through [Forgot Password](#outside-the-app-forgot-password)

**Use when**: Changing your BlazeMeter account password or recovering access to your account.

### Inside the app: Personal Settings

1. Log in to your account with your registered email address and password.
2. Click the dropdown in the top right corner of the screen.
3. Click on **Personal Settings**.
4. Select **Password** tab.
5. Enter and confirm your new password. Passwords must contain at least one special character.

### Outside the app: 'Forgot Password'

If you find yourself locked out of your account, please use this link to get access back:

1. Open the login page and click the "Forgot your Password" link, or open the link [https://a.blazemeter.com/user/password](https://a.blazemeter.com/user/password) in any modern browser.
2. Enter your registered email address.
3. Click the "Reset Password" button.
4. A new password is emailed to the registered email address. Use that password to log in to your account.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Changing Your Password**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-changing-your-password`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-changing-your-password"]}`

---

## Administration Create and Manage Secrets

Secrets are objects that contain sensitive data, such as passwords, tokens, credit card numbers, or any other data that shouldn't be exposed. By using secrets, you do not have to hard code any sensitive data into your test scripts. When you run a test, whenever an enabled secret appears in reports or logs during and after run time, the value of the secret is replaced with asterisks (*).

Once you create your secrets, you can use them in your Performance tests. For more information on adding secrets to your test scripts, see [Secrets](skill-blazemeter-performance-testing://references/advanced-features.md) in Advanced Test Options.

**Use when**: Creating and managing secrets for storing sensitive data securely, or when you need to avoid hard-coding passwords, tokens, or other sensitive information in test scripts.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Secrets**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-secrets.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-secrets.htm"]}`

### Feature Availability

Secrets is a feature that is limited to Enterprise customers. To enable secrets, contact [BlazeMeter Support](mailto:support-blazemeter@perforce.com?subject=Enable Private Locations) or your account manager.

### Security Best Practices

When using secrets, ensure that:
- Only production and non-sensitive secrets are used
- All secrets are strictly limited in scope and privilege, and access only test-specific resources or data
- Secrets should be temporary and rotated regularly
- You avoid the use of secrets that provide access to productions environments or sensitive customer data

### Secrets Page

You can create and manage secrets on the **Secrets** page in your Workspace settings. All workspace members can view all secrets configured in the workspace. All roles except Viewer can create secrets. Once the secret is created, no one can see the value, protecting the sensitive data.

### Permissions

The following are permissions for secrets:

- **Create a secret**: All roles except viewer
- **Edit a secret**: Account admins, Workspace managers, the member who created the secret
- **Delete a secret**: Account admins, Workspace managers, the member who created the secret

### Create a Secret

In order to use secrets in your Performance tests, you need to create them.

**To create a secret:**

1. Log in to your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings** > **Workspace** > **Secrets**
4. Click the **+ Add Secret** button
5. Enter the following:
   - **Secret name**: Can be any name you choose. You can only use lowercase letters, numbers, underscores, and hyphens
   - **Secret value**: Enter the value you want for your secret. Secret values must have a minimum of five characters
   - **Description**: (Optional) Enter a description of your secret
6. Click **Create Secret**

### Edit or Delete a Secret

Workspace members with the correct permissions can edit or delete a secret by clicking the **Edit** or **Delete** icon in the **Action** column.

**When editing a secret:**
- You can only edit the **Description**
- The **Secret value** cannot be viewed, but can be overridden by entering another value
- To change the **Secret name**, you need to delete the secret and create another one with the new name

### Use Secrets in Your Tests and Virtual Services

Now that you have configured your secrets, you can create Performance tests, GUI Functional tests, and use secrets with your virtual services. For more information on using secrets:

- **For Performance tests**: See [Manage Secrets for Performance Tests](skill-blazemeter-performance-testing://references/advanced-features.md)
- **For GUI Functional tests**: See [Manage Secrets for GUI Functional Tests](skill-blazemeter-functional-testing://references/gui-tests.md)
- **For Service Virtualization**: See [Manage Secrets for Service Virtualization](skill-blazemeter-service-virtualization://references/virtual-services.md)

---

## Administration Two-Factor Authentication

BlazeMeter supports two-factor authentication (2FA) to add an additional layer of security for user logins. There are two ways to add it to a user account:
- You will be prompted to setup 2FA when creating a new account or resetting your password
- For existing accounts, the option to setup 2FA may be found within Personal Settings

Setup is easy!

**Use when**: Configuring and managing two-factor authentication for BlazeMeter user accounts or when installing authenticator apps, configuring 2FA, and removing 2FA.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Two-Factor Authentication**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-two-factor-authentication`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-two-factor-authentication"]}`

### Install a Supported Authenticator App

Two-factor authentication relies on receiving a temporary security code from an authenticator application installed on another machine (typically a mobile device). BlazeMeter supports the following authenticator apps:

- **FreeOTP**
- **Google Authenticator**

Once you have installed and configured the app on your device, you're ready to setup 2FA.

### Configure BlazeMeter 2FA

While creating a new account or resetting your password, you'll be prompted to setup 2FA; otherwise, you can set it up via these steps:

1. Navigate to your Personal Settings by clicking your name in the upper-left corner of the UI, then clicking "Personal Settings"
2. On the next screen, in the left-hand menu, click "Authenticator"
3. As instructed on-screen, open your authenticator app, then scan the provided barcode
4. After scanning the barcode successfully, the authenticator app will provide you with a one-time security code. Enter it in the "One-time code" field
5. Click the Save button

Your newly configured authenticator will now be listed.

### Remove BlazeMeter 2FA

If you need to disable two-factor authentication, simply follow these steps:

1. Navigate to your Personal Settings by clicking your name in the upper-left corner of the UI, then clicking "Personal Settings"
2. On the next screen, in the left-hand menu, click "Authenticator"
3. Click the trash bin icon to delete your 2FA configuration

### Security Best Practices

- Always enable 2FA for administrative accounts
- Use authenticator apps (FreeOTP, Google Authenticator) for better security
- Regularly review active sessions

**Note**: 2FA adds an additional layer of security by requiring a temporary security code from an authenticator app in addition to your password. This significantly reduces the risk of unauthorized access even if your password is compromised.

---

## Changing Your Email Address

Change the email address associated with your BlazeMeter account.

**Use when**: Updating your account email address or when you need to change the email associated with your BlazeMeter account.

### Change Your Email Address

To change the email address associated with your account, contact [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com?subject=Change email address associated with my account) and request the email address change.

**Important**: State the current email address associated with your account, and the new one.

---

## Changing Your Password

You can change your password in two ways:
- Inside the app through Personal Settings
- Outside the app through Forgot Password

**Use when**: Changing your BlazeMeter account password, resetting a forgotten password, or recovering access to your account.

### Inside the app: Personal Settings

1. Log in to your account with your registered email address and password
2. Click the dropdown in the top right corner of the screen
3. Click on **Personal Settings**
4. Select **Password** tab
5. Enter and confirm your new password. Passwords must contain at least one special character

### Outside the app: Forgot Password

If you find yourself locked out of your account, please use this link to get access back:

1. Open the login page and click the "Forgot your Password" link, or open the link [https://a.blazemeter.com/user/password](https://a.blazemeter.com/user/password) in any modern browser
2. Enter your registered email address
3. Click the "Reset Password" button
4. A new password is emailed to the registered email address. Use that password to log in to your account

### Best Practices

- Use strong passwords with at least one special character
- Change passwords regularly for security
- Keep your password secure and don't share it
- Use the Forgot Password feature if you're locked out

### Overview

You can change your password in two ways:
- **Inside the app**: Through Personal Settings
- **Outside the app**: Through Forgot Password

### Inside the App: Personal Settings

Follow these steps:

1. Log in to your account with your registered email address and password
2. Click the dropdown in the top right corner of the screen
3. Click on **Personal Settings**
4. Select **Password** tab
5. Enter and confirm your new password. Passwords must contain at least one special character
6. Save your changes

### Outside the App: Forgot Password

If you find yourself locked out of your account, use the Forgot Password feature:

1. Open the login page and click the "Forgot your Password" link, or open the link [https://a.blazemeter.com/user/password](https://a.blazemeter.com/user/password) in any modern browser
2. Enter your registered email address
3. Click the "Reset Password" button
4. A new password is emailed to the registered email address. Use that password to log in to your account

**Note**: After logging in with the temporary password, consider changing it to a new password of your choice through Personal Settings.

