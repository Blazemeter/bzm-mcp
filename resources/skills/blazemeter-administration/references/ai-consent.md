# AI Consent Management

## Administration AI Consent Management

BlazeMeter's AI-assisted features require explicit consent from the account owner before team members can use them. By default, AI features are disabled.

**Use when**: Managing AI consent settings for BlazeMeter AI-assisted features or when enabling/disabling AI features and understanding data privacy policies.

### Which services does BlazeMeter use?

BlazeMeter uses Microsoft Cognitive Services running in the Microsoft Azure cloud within an instance that is dedicated solely to BlazeMeter purposes, adhering to all relevant data protection laws and regulations.

For more information, see [Data, privacy, and security for Azure OpenAI Service (microsoft.com)](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy).

**Note**: For more information specifically on Test Data AI features, see [Test Data Pro AI FAQ](https://help.blazemeter.com/docs/guide/test-data-pro-faq.html). For more information specifically on API Monitoring, see [Manage AI Consent in API Monitoring](https://help.blazemeter.com/docs/guide/api-monitoring-ai-consent.html).

### Does my Account have access to the AI features?

The AI features are exclusively available for BlazeMeter Enterprise plans ("Unleashed"). Free, Basic, and Pro accounts do not have access to these features. Your BlazeMeter account administrator needs to manually enable and approve the utilization of AI functionality for the account.

### Who can manage AI Consent?

In the Account Settings, your BlazeMeter account admins control the availability of AI features account wide.

### Will AI automatically access my data?

No, the AI features are not activated by default. In the absence of consent, AI features remain inactive. For more information, see our [Generative AI Policy](https://www.perforce.com/generative-ai-policy).

### How to enable or disable AI features?

To enable or disable AI features:

1. Log in as account administrator
2. Go to **Account Settings > Environment > Account AI Consent**
3. Enable or disable AI features by choosing **Agree** or **Disagree**
4. The settings are saved automatically

### Does the utilization of AI features result in higher resource demands?

No, utilizing AI features doesn't incur any additional resource consumption. They also do not affect resource consumption on the private location side.

### Are there any additional costs for using these features?

There are no additional fees or "token" usage associated with utilizing the AI features. The AI features are exclusively available for Enterprise plans ("Unleashed"). Free, Basic, and Pro accounts do not have access to these features.

### Will AI use my data to be trained for use cases outside of BlazeMeter?

No, BlazeMeter does not utilize any private or sensitive customer data to train the model used in our product.

We employ Microsoft Cognitive Services. Within BlazeMeter's paid service account, Microsoft does not utilize any data for machine learning purposes, and this data is not employed beyond the BlazeMeter environment. For more information, see our [Generative AI Policy](https://www.perforce.com/generative-ai-policy).

### Will other customers be able to generate output based on data other customers have used?

No, BlazeMeter does not utilize any private or sensitive customer data to train the model used in our product.

We employ Microsoft Cognitive Services. Within BlazeMeter's paid service account, Microsoft does not utilize any data for machine learning purposes, and this data is not employed beyond the BlazeMeter environment.

### Do all BlazeMeter features now utilize AI?

No, AI is only integrated into specific components. Other functionalities remain unaffected.

For example, when you initiate the Data Creation Wizard for the first time, a dialog will notify you whether your account administrator has enabled the AI features in the Data Profiler or not. For more information on Test Data AI features, see [Test Data Pro AI FAQ](https://help.blazemeter.com/docs/guide/test-data-pro-faq.html).

### What if the AI service is unavailable?

In the event of AI unavailability or an AI error, we handle it in a standard manner and provide an appropriate error message to the user.

**Note**: Will a test with AI-driven test data fail? In the event of AI unavailability or an AI error, we handle it in a standard manner and provide an appropriate error message to the user.

### What happens when we choose to opt out?

Consent settings apply at the workspace level and affect all users in the workspace.

- When AI features are disabled, team members will not be able to access the generators anymore
- Changes to AI Consent take effect immediately upon saving

For more details on AI policies, refer to the Perforce [Generative AI Policy](https://www.perforce.com/generative-ai-policy).

### Data Privacy

- **Data Usage**: Understand how data is used for AI features
- **Data Storage**: Review data storage and retention policies
- **Opt-Out**: Ability to opt out of AI features
- **Data Security**: AI features use encrypted data transmission

### AI Consent Settings

- **Enable AI Features**: Allow use of AI-assisted features
- **Disable AI Features**: Opt out of all AI features
- **Selective Consent**: Enable specific AI features while disabling others

### Using MCP Tools

To check AI consent status at account level:

**Read account AI consent**:
- Tool: `blazemeter_account`
- Action: `read`
- Required args: `account_id` (integer)
- Returns: Account details including AI Consent information in the response

The account response includes AI consent settings that can be checked programmatically.

### Best Practices

- Review AI consent policies before enabling
- Understand data usage and privacy implications
- Configure consent at appropriate level (account, workspace, or team)
- Regularly review consent settings
- Communicate consent decisions to team members

### Privacy Considerations

- AI features may process test data and scripts
- Data is used to improve AI model performance
- Users can opt out at any time
- Data is handled according to privacy policies

### Feature-Specific Consent

Some AI features may have separate consent settings:
- **AI Script Assistant**: Consent for script generation
- **Test Data Pro AI**: Consent for data generation and profiling
- **AI Log Analysis**: Consent for log processing

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration AI Consent Management**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `administration-ai-consent`
  - `api-monitoring-ai-consent`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-ai-consent", "api-monitoring-ai-consent"]}`
- **Account AI Consent**: Use MCP tool `blazemeter_account` with action `read` to check AI consent settings programmatically
