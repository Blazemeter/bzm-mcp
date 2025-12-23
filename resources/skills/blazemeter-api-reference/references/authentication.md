# Authentication

## API Authorization

Understand API authorization methods in BlazeMeter, including API key authentication using Basic Auth and cookie authentication.

**Use when**: Understanding API authorization methods in BlazeMeter or configuring API key authentication using Basic Auth and cookie authentication.

### API Key Authentication Using Basic Auth

To use BlazeMeter API without any dependence on a cookie or a token, be sure to pass [your API Key](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html) as Basic Auth credentials. Our API key contains an ID (highlighted in green) and a Secret (highlighted in orange), for example:

```
id:secret
f817e22f1526b048799f75da:7641251982b983cfd92b5a25fa97cd3ee9e21920f21d8b14cd705831826935723f3033f0
```

Use them as Type Basic Auth in the corresponding fields:
- **id** → **username**
- **secret** → **password**

**Note**: For more information about how to find your API key, see the [BlazeMeter API keys](https://help.blazemeter.com/docs/guide/api-blazemeter-api-keys.html) article.

**cURL Example:**
```bash
curl -X POST https://a.blazemeter.com:443/api/v4/tests/testID/start \
  -H "Content-Type: application/json" \
  --user 'f817e22f1526b048799f75da:7641251982b983cfd92b5a25fa97cd3ee9e21920f21d8b14cd705831826935723f3033f0'
```

Examples of using the API Key can be seen in any API request example in cURL and Python. Here's what it will look like in Postman when using Basic Auth.

### Cookie Authentication

Cookie authentication is the basic authentication method with BlazeMeter. Authentication cookies are commonly used by web servers to know whether the user is logged in or not, and with which account they are logged in. When you log in to your BlazeMeter account, a cookie will be generated exclusively for your session. When BlazeMeter recognizes a valid session key in a subsequent request, it will authorize the user according to this existing session key without requesting the password again.

---

## API Keys

To use the BlazeMeter API, you will need your API key, which can also be used for certain integrations like BlazeMeter's Jenkins plugin or BlazeMeter MCP.

**Use when**: Generating, regenerating, and managing BlazeMeter API keys, setting expiration periods, or using API keys for integrations.

### Generate a New API Key

Follow these steps:

1. Go to the user drop-down menu at the top right corner of the screen, then click on 'Settings'. You will be transferred to the 'Settings' Panel
2. Go to the 'API keys' option under the 'Personal' settings on the left of the screen
3. There, click on the '+' icon to create a new API key
4. Give your API key a relevant name that is useful for your reference, and set its expiration period
5. Click the "Generate" button. Your new API Key ID and API Key Secret is displayed

**IMPORTANT**: Your API Key Secret ("secret key") **will only be shown this one time and can never be retrieved again**. Make sure to copy the secret key before closing the window. **If the secret key is lost, it must be regenerated.**

You've now successfully created a new API key!

**Note**: Your API key can also be used for certain integrations like [BlazeMeter's Jenkins plugin](https://help.blazemeter.com/docs/guide/integrations-blazemeter-jenkins-plugin-guide.html) or [BlazeMeter MCP](https://help.blazemeter.com/docs/guide/integrations-blazemeter-mcp-server.html).

### Regenerate a New 'Secret' API Key for Your API Key

Every API key has a 'Secret' API key that is visible only to you when you initially create a new API key. In case you forgot your 'Secret' or you simply wish to regenerate it:

1. Go to your API keys section
2. Hover over the relevant API key
3. You will now see a **Regenerate** button on the right of the API key
4. Click the button to regenerate a new 'Secret API key' (and not a new API key)

**Note**: This regenerates only the secret portion of the API key, not the entire API key. The API Key ID remains the same.

### Limit the Expiration for All API Keys Under Your Account

The Account's owner or admin can limit the maximum expiration date for all the API keys of all the users of the Account. That is very useful in case an Account has to take strict security measures.

1. Go to the user settings drop down menu at the top right corner of the screen
2. Click on it and then click 'Settings'. You will be transferred to the 'Settings' Panel
3. Go to the 'General Settings' option under the 'Account' settings on the left of the screen
4. Use the 'API Keys Expiration Period' panel's drop-down menu to select the maximum expiration period for the account's API keys

### Best Practices

- **Secure Storage**: Store API keys securely
- **Expiration**: Set appropriate expiration periods
- **Key Rotation**: Regularly rotate API keys
- **Access Control**: Limit key access

---

## Documentation References

For detailed information about API authentication, use the BlazeMeter MCP help tools:

**API Authorization**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-authorization`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-authorization"]}`

**BlazeMeter API Keys**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `api-blazemeter-api-keys`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["api-blazemeter-api-keys"]}`

