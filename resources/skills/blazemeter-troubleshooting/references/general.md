# General Troubleshooting

## Debug Test

Debug why a test worked previously but fails now, including checking logs, static data issues, site status, protocol changes, network connectivity, CSV data usage, and regular expression matching.

**Use when**: Debugging why a test worked previously but fails now, checking logs, investigating static data issues, site status, protocol changes, network connectivity, CSV data usage, or regular expression matching problems.

### Symptom

Your BlazeMeter script worked fine yesterday but today, when you tried to run it again, it failed.

### Solution

Follow these troubleshooting steps to identify and resolve the issue:

1. **Check the jmeter-console0.log file**:
   - Browse to the specific Test Reports -> Logs -> jmeter-console0.log Tab and click **Download**
   - Check for warning and error type messages and resolve the errors based on details mentioned in log file

2. **Review static data in your request body**:
   - Do you have static data in your request body that refers to time beyond 24 hours or calendar days? Then parametrize the script using [synthetic test data](https://help.blazemeter.com/docs/guide/test-data-generate-synthetic.html)

3. **Verify site status**:
   - Is your target site temporarily down? Check site status before running the test

4. **Check protocol or URL changes**:
   - Was there a change in protocol or URL of your target site from that recorded in your script? Check the protocol in the script and change it to a working one if required

5. **Test network connectivity**:
   - Low or no network connectivity? Check your internet connectivity, direct or proxy connections

6. **Review CSV data usage**:
   - Was the data in the CSV file for one-time use and has already been used? Change the CSV file with a fresh working data set or edit your script to use [synthetic](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html) functions to generate data in the required format

7. **Verify regular expression matching**:
   - Are regular expressions not matching due to changes in site code? Debug your script in JMeter, use the Regular Expression tester from the 'view result tree' listener and update the regular expressions where required

---

## Delete Non-Empty Project

Resolve "Cannot delete non-empty project" errors by identifying and deleting associated test reports, including using API for verification and force deletion.

**Use when**: Resolving "Cannot delete non-empty project" errors or when identifying and deleting associated test reports using API for verification and force deletion.

### Reason

If a test was deleted without also deleting test reports associated with it, then even though the reports are no longer visible in the UI, the existence of these reports means the project remains non-empty. In other words, delete all tests and test reports before the project they belong to is considered empty.

**Note**: This is a common issue when tests are deleted but their associated reports remain in the system. The project cannot be deleted until all associated reports are removed.

### Solution Steps

1. **Verify if any test reports still exist under the project**:
   - Execute the following API request:
     ```
     GET https://a.blazemeter.com/api/v4/masters?projectId=<project_id>
     ```
     (Replace <project_id> with your project's ID.)
   - If there are any reports under the project, they will be listed within the response message

2. **Force-delete the project via the API**:
   - If all tests have been deleted and all that remain are test reports that are no longer needed, you can force-delete the project via the API
   - To perform the forced deletion, execute the following API request:
     ```
     DELETE https://a.blazemeter.com/api/v4/projects/{project_id}?force=true
     ```
     (Replace <project_id> with your project's ID.)

---

## Forbidden Domains

Understand which domains are forbidden to test using BlazeMeter, including the comprehensive list of restricted domains and authorization requirements.

**Use when**: Understanding which domains are forbidden to test using BlazeMeter or when checking the comprehensive list of restricted domains and authorization requirements.

### Restricted Domains

Users are permitted to test domains for which they have authorization. For more information, see the [license agreement](https://www.perforce.com/license-agreements) and [terms of use](https://www.perforce.com/terms-use).

There are multiple domains which you are expressly forbidden to test at any time—unless specifically authorized to do so in writing from support-blazemeter@perforce.com. Any domain listed in the help documentation may *NOT* be tested for load at any time, and if they are, the test will result in an automatic error, and credits used for these activities will NOT be refunded.

**Note**: The complete list of forbidden domains is extensive and includes major websites such as google.com, facebook.com, youtube.com, amazon.com, microsoft.com, and many others. For the complete list, refer to the help documentation using the help_id below.

**Important**: Any domain listed in the help documentation may *NOT* be tested for load at any time, and if they are, the test will result in an automatic error, and credits used for these activities will NOT be refunded. If you need to test a forbidden domain, you must obtain written authorization from support-blazemeter@perforce.com.

---

## High Response Time

Diagnose and resolve high response time issues in BlazeMeter tests, including understanding why response times differ between local and cloud tests, different tests, different runs, and different locations.

**Use when**: Diagnosing high response time issues, understanding why response times differ between local and cloud tests, different tests, different runs, or different locations.

### Symptom

My average response time for a test is higher than what was expected or desired.

**Examples:**
- A BlazeMeter test has a higher average response time than the same test run locally
- Two different BlazeMeter tests show different average response times
- Two runs of the same BlazeMeter test show different average response times
- Tests run from different locations or engine providers show different average response times

### Reason

The last section of this article will touch on each of the above scenarios, but first, let's explore an overall explanation of where BlazeMeter fits into the picture.

#### BlazeMeter is Merely the Messenger

BlazeMeter only reports these metrics as observed by the engine from the location or provider you selected. BlazeMeter does not in any way impact or interfere with these metrics; it only reports them. BlazeMeter has no control over response time, nor does BlazeMeter affect actual response times. (Service Virtualization can [Simulate Irregular Response Latencies](https://help.blazemeter.com/docs/guide/mock-service-think-time-irregular-response-latency.html) *in addition* to the response time.)

#### Waiting for a Call Back

When you run a test from BlazeMeter, the system can only know how long it took your application server to respond; it doesn't know why it took as long as it did.

### Solution

To find out why your application server took as long to respond to the test engines as it did, investigate your own server and network internally with the appropriate teams that can help you troubleshoot. Here are some pointers to help you get started.

#### (1) A BlazeMeter test has a higher average response time than the same test run locally

BlazeMeter's engines are in different geographical locations and on different networks than your local machine, so response times are not comparable between the two. If your local machine is on the same network as your application server, data has less distance to travel. There will always be a difference between the routes from each engine to your server compared to from your local machine to your server.

To test locally, set up a [Private Location](https://help.blazemeter.com/docs/guide/private-locations-intro.html): your own BlazeMeter engine which you install within your own network.

#### (2) Two different BlazeMeter tests show different average response times

There are many reasons why response times may differ between two different tests. For example, expect a multi-test to experience higher response times than a single test. A more complex script puts a heavier strain on your application server or your network, resulting in bottlenecks that affect response time. Keep in mind that no two test scripts are alike, so some differences are inevitable.

#### (3) Two runs of the same BlazeMeter test show different average response times

It's not uncommon for two runs of the same test to have considerably different average response times. If this happens, work with your application server and network teams to investigate what conditions differed between the time frames of the two runs. It's possible an internal server or network issue caused a momentary delay in getting responses out to BlazeMeter's engines.

#### (4) Tests run from different locations or engine providers show different average response times

Variances in response times are to be expected, because (a) data sent to engines in two different geographic locations travels different routes and (b) different providers (Google, AWS, Azure) provide different machines, and though they are comparable, they are not exactly the same.

In case of the former, if the difference in response times is severe, you may need to work with your network team internally to identify bottlenecks in sending data to some locations versus other locations.

---

## Chrome Extension Export JMX Failed

Resolve export to JMX failures in BlazeMeter Chrome Extension caused by network or firewall blocking of the converter URL.

**Use when**: Resolving export to JMX failures in BlazeMeter Chrome Extension or when troubleshooting network or firewall blocking of the converter URL.

### Reason

This means that something on your network (typically your firewall) is blocking the connection needed for the recorder to complete the export. When you select the option to export your recording to JMX, the extension actually converts the recording into JMeter's JMX format. This conversion is not performed with the app itself, but rather through BlazeMeter's own converter located at [https://converter.blazemeter.com](https://converter.blazemeter.com). If the converter URL is blocked or otherwise unreachable from within your own network for any reason, the conversion will not be possible to perform, and thus the error above will occur.

### Solution

To resolve the issue, check with your internal network or security team to ensure that the converter URL can be reached from the machine you are recording from.

**Note**: The converter URL is [https://converter.blazemeter.com](https://converter.blazemeter.com). This URL must be accessible from your network for the JMX export to work. If your firewall blocks this URL, you'll need to whitelist it or configure your network to allow access.

---

## Support Feature Requests Submit

Submit feature requests (ideas) to BlazeMeter, including describing business problems, voting on existing ideas, and following progress.

**Use when**: Submitting feature requests to BlazeMeter or when describing business problems, voting on existing ideas, and following progress.

### Process

Please read these two short tips for success before you start:

1. **Describe the business problem you want to solve**. Instead of just describing a feature, please explain the challenges you face today and the "better way" you would like to be able to get your job done. We want to focus on solving the problem, not just adding a feature out of context.

2. **Vote and add comments to other people's requests if their idea would impact you**. Our goal is to prioritize to build the most impactful features first and to make sure they deliver the benefits you are hoping for. Votes and comments speed the process along.

### Accessing the Ideas Portal

Start by clicking on the HELP CENTER tab and then clicking the **Feature Requests** button. If you have a paid account with us, you'll be automatically signed in to our ideas portal where you can **add a new idea**, **vote** or **comment on an existing idea** and **subscribe to track the progress of any idea** as it makes its way through our roadmap. Free-tier users will see a simpler, "submit-only" interface.

### Making Your Voice Heard

To get started, click the "Add a New Idea" button and start typing a summary of your idea. The portal will look for similar ideas and present them to you to vote and add comments to, or you can create your own if there isn't a match.

If you find an existing idea you can boost with a vote and a comment about your usage patterns and needs, please do so! This is why we chose this venue: it allows ideas to grow richer and more refined by allowing you to prioritize them and to paint a picture explaining how and why a change would impact your day-to-day work.

### Following The Progress of Ideas

If you find an idea that interests you, whether or not you have commented on it, you can easily **Subscribe** to it. Think of this as "following" an idea as it's impacted by other customers, PM team comments and changes in status as it moves from idea to backlog to shipped feature. When you subscribe you'll get **email notifications whenever someone else comments or the status changes**.

### Prioritize The Features You Care About Most

We're starting the Ideas Portal out with 12 votes per user. You can use up to three of those votes on any one idea. When an idea is implemented, we'll put the votes back in your account. You can also remove a vote from an idea if you would rather allocate it to another. You can comment on and subscribe to an unlimited number of ideas.

---

## Support Feature Requests Track

Track feature request statuses (Future consideration, Likely to implement, Planning to implement, Shipped, etc.) and understand how to influence outcomes.

**Use when**: Tracking feature request statuses or when understanding how to influence outcomes and following feature request progress.

### Status Types

When a Feature Request (Idea) is submitted it starts out without a status. To view these Ideas: click on the "Recent" tab at the top of the Ideas Portal. If you aren't already in the Ideas Portal, please log into BlazeMeter and click the "Feature Requests" button in the HELP CENTER.

Several times a week, we review new Ideas and move them to one of the states below. When we do, the submitter, voters, commenters and anyone who has manually "Subscribed" to updates will get an email.

#### Future consideration
The Idea has been reviewed, checked for categorization and we have asked some initial questions to be sure we get the essential core of the idea. We may edit to the title or description to ensure others can find it. If someone has already made a similar request, we'll merge the new idea with the existing one and let the submitter and any subscribers know. → Vote or comment to help this one along!

#### Likely to implement
Same as above, except that we have weighed in early to say the idea is a likely candidate for implementation if it gets sufficient interest. Consider this a "like" on our part, but not a commitment to implement. → Vote or comment to help this one along!

#### Unlikely to implement
Same as "Future consideration," except that we have weighed in with a comment to say why the idea is *not* a likely candidate for implementation. → If you feel strongly that we should think again about this one, let us know with a comment!

#### Planning to implement
The idea has been selected for implementation. Work should start in the next sprint or two. It's on the way!

#### Shipped
The feature has been released. → Enjoy!

#### Already exists
The feature already exists, but was probably too hard to find! → Tell us how we could have made this one more easily discovered!

#### Will not implement
This one is a definite "no" and we will be sure to explain why.

---

## Support Ticket Management

Open support tickets in BlazeMeter, including email support, community forums, and best practices for providing detailed issue descriptions.

**Use when**: Opening support tickets in BlazeMeter or when accessing email support, community forums, and following best practices for providing detailed issue descriptions.

### Support Channels

BlazeMeter support hours are 6 AM - 5 PM PST, Monday - Friday. If you open your ticket outside of these hours, then we will get to it at the first opportunity. BlazeMeter provides multiple ways to get in touch with our support professionals and receive the help you need.

#### Open a Support Ticket

By submitting a support ticket, you can provide a detailed description of your issue or question. If you're referring to a specific test, report, or session, it's best to open the ticket from within BlazeMeter while viewing that page. The full URL is then automatically included in the ticket.

1. In BlazeMeter, click the **Help Center** tab on the right-hand side of the screen
2. Click the **Support Tickets** button
3. Enter the **Subject** and a **Description** of your issue
4. Click **Continue** to view the top Knowledge Base articles which you might find helpful regarding your query
5. Either click **Continue** to send the ticket. Or click **This resolved my issue** to cancel

Support receives the URL of the BlazeMeter page you were on when opening this ticket. Your name and email address are automatically included.

#### Email BlazeMeter Support

If you cannot log on to the support portal or BlazeMeter, send an email to [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com). Describe your query or issue in detail. Make sure to include relevant information such as your account details, project information, test or report URL, screenshots, and any error messages you have encountered.

- For a specific BlazeMeter test, include the Test URL or [Report URL](https://help.blazemeter.com/docs/guide/performance-share-reports.html)
- For a specific API Monitoring Test, include an [API Monitoring test result](https://help.blazemeter.com/docs/guide/api-monitoring-sharing-test-results.html)

To ensure the best quality of service, open support tickets using the email address that is associated with the BlazeMeter account that experienced the issue, if possible. This will allow us to see vital information associated with your account that can speed up the time to resolution for your issue.

#### Explore Community Forums

- [BlazeMeter Forum](https://groups.google.com/g/blazemeter-forum)
- [JMeter Forum](https://groups.google.com/g/ptgram24)
- [jMeter-Plugins Forum](http://groups.google.com/group/jmeter-plugins)
- [Taurus GitHub Issues](https://github.com/Blazemeter/taurus/issues)

### Best Practices

- Ensure your test can run locally, for example, through a local Taurus or JMeter installation
- If your test works locally but fails on BlazeMeter, or if it fails to start or hangs indefinitely, search the [Support knowledgebase](https://portal.perforce.com/s/topic/0TOPA0000001YNp4AM/blazemeter) before opening a ticket
- For problems with Taurus, jMeter, or jMeter Plugins, contact their community forums

**Note**: When opening a support ticket, it's best to open it from within BlazeMeter while viewing the specific test, report, or session page. The full URL is then automatically included in the ticket, which helps support understand the context of your issue.

---

## Documentation References

For detailed information about general troubleshooting, use the BlazeMeter MCP help tools:

**Debug Test**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-debug-test`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-debug-test"]}`

**Delete Non-Empty Project**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-delete-non-empty-project`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-delete-non-empty-project"]}`

**High Response Time**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-high-response-time`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-high-response-time"]}`

**Forbidden Domains**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-forbidden-domains`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-forbidden-domains"]}`

**Chrome Extension Export JMX Failed**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-chrome-extension-export-jmx-failed`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-chrome-extension-export-jmx-failed"]}`

**Support Feature Requests Submit**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `support-ideas-submit`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["support-ideas-submit"]}`

**Support Feature Requests Track**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `support-ideas-track`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["support-ideas-track"]}`

**Support Ticket Management**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `support-ticket`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["support-ticket"]}`

