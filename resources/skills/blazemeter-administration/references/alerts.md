# Workspace Alerts

## Administration Creating Workspace Alerts

When managing your tests in a BlazeMeter Workspace, you may want notifications when a considerably large test (above your normal requirements) is launched or generated. Workspace Alerts make it easy to generate an e-mail or Slack notification when a member of your workspace performs such an action.

If you want to publish all test activity regardless of test size or duration, that's an option too.

**Note**: You will require to have 'Admin' user role in the account, or 'Manager' role in the workspace to enter or edit these Alerts.

**Use when**: Creating workspace alerts for email and Slack notifications or when configuring test alerts, agent alerts, and webhook notifications for large tests.

### Create an Alert

Follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Expand the **Workspace** section in the desired workspace, and click **Alerts**
3. Click the '+' button. A new window opens
4. Fill out the criteria. If you want to post alerts to Slack, see the Slack Webhook Tips below
5. The alert will be sent out if either the Test Duration OR the Test Concurrency are met or exceeded
6. To save the settings, click **Create alert**
7. Your alert appears under the **Alerts** section
8. Use the **Validate** option to confirm that the new alert works as intended. This action will send a notification to the email address and/or Slack Webhook URL you have entered above

You have set up an Alert.

**Note**: If you want to publish all test activity regardless of test size or duration, that's an option too. You can create multiple alert configurations and separate webhooks (each with their own name, icon and channel destination), consider having one alert that publishes all "BlazeMeter Activity" and another that alerts when a "BlazeMeter Large Test" is created or run.

### Configure Alerts for Agents

Admins or workspace managers can configure agent alerts so that users can be notified when the free disk space on any agent goes below a defined value.

Follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Expand the **Workspace** section in the desired workspace, and click **Alerts**
3. Click the '+' button. You have an option to add a **Test Alert** or an **Agent Alert**
4. Select Agent Alert. A new window **Create an Agent Alert** opens

**Note**: For the Agent Alert option, at least one private location has to be defined in the workspace.

5. Fill out the criteria:
   - By default, the alert will be sent in case free disk space goes below 30.00 GB, but the threshold can be changed
   - Select a notification channel for the alert: email, Slack or both
6. Click **Create alert**
7. Your alert appears under the **Alerts** section
8. Use the **Validate** option to confirm that the new alert works as intended. This action will send a notification to the email address and/or Slack Webhook URL you have entered above

You have set up an Alert.

### Slack WebHook URL Tips

1. For information on how to set up a Slack Webhook URL, please refer to [this Slack doc](https://api.slack.com/messaging/webhooks)
2. Be sure to give your webhook a meaningful name and icon when creating the Webhook URL in Slack. You can do this in the "Customize Name" and "Customize Icon" fields in the Slack Incoming Webhooks configuration screen. The default name is "Incoming Webhook," but "BlazeMeter Activity" or the like would be better. The default icon looks like this, but the BlazeMeter icon will be easier to spot
3. Prefer Slack and no emails? Be sure to clear the Email address field above before saving
4. Since you can create multiple alert configurations and separate webhooks (each with their own name, icon and channel destination), consider having one alert that publishes all "BlazeMeter Activity" and another that alerts when a "BlazeMeter Large Test" is created or run

**Note**: The Validate option sends a test notification to confirm that the alert configuration works correctly. This is useful for testing webhook URLs and email addresses before relying on them for production alerts.

### Alert Types

- **Test Alerts**: Notifications when tests are launched or completed (based on Test Duration OR Test Concurrency)
- **Agent Alerts**: Notifications for agent status changes (free disk space below threshold)

### Notification Channels

- **Email**: Send alerts to email addresses
- **Slack**: Send alerts to Slack channels via webhooks
- **Both**: Send alerts to both email and Slack

### Best Practices

- Set appropriate thresholds to avoid alert fatigue
- Use different channels for different alert severities
- Test webhook configurations before production use using the Validate option
- Monitor alert delivery to ensure reliability
- Consider creating separate alerts for different purposes (all activity vs. large tests)

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Creating Workspace Alerts**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-creating-workspace-alerts`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-creating-workspace-alerts"]}`

