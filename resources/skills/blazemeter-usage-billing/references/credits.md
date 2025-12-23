# BlazeMeter Credits and Billing

## Credit Types and Charging

Understand BlazeMeter credit types (VU, VUH, Tests), how credits are charged for different test types, and calculate credit consumption for performance, functional, API monitoring, and service virtualization tests.

**Use when**: Understanding BlazeMeter credit types and charging, calculating credit consumption for different test types, or optimizing credit usage.

## Credit Types

Your billing plan is based on one of three credit types: **Variable Unit (VU)**, **Variable Unit Hours (VUH)**, or **Tests**.

BlazeMeter uses three main credit types:

### VU (Variable Unit)
- **Used for**: All capabilities across the entire BlazeMeter platform
- **Description**: A Variable Unit (VU) is a metric that measures usage of all capabilities across the entire BlazeMeter platform. A VU ceiling signifies the maximum concurrency that you can leverage across the platform as a whole at any time, taking into account various usage metrics such as the number of virtual users, browser session executions, running virtual services, virtual service transactions, test data usage, and running tests
- **Calculation**: Concurrent VUs translate as follows to the individual parts of the BlazeMeter Continuous Testing Platform:
  - **Performance Testing**: 1 Variable Unit Hour (VUH) equals 1 VU, except for [Browser Performance Test Consumption](https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html#Browser)
  - **GUI Functional Testing**: 1 Browser session execution equals 100 VU
  - **Service Virtualization**: Each running virtual service equals 100 VU. Each 2,500 transactions equal 5 VU that is reserved until midnight (local time) while the virtual service is running
  - **API Monitoring** (also replaces **API Functional Testing**): 1,000 API calls equal 5 VU (increments of 5 VU are reserved for 24 hours)
  - **Test Data**: See [BlazeMeter Test Data Consumption](https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html#h_01FW7ASC4ECQ3M36G0ZTCNNBXD) below

### VUH (Variable Unit Hours)
- **Used for**: Performance testing and GUI Functional testing
- **Description**: A Variable Unit Hour, formerly known as Virtual User Hour, is used to measure Performance testing and GUI Functional testing usage. When using VUH as credit, consumption will be deducted from your VUH credit balance

**BlazeMeter calculates VUH as follows:**

- **Calculation**: 
  - **Performance testing**: `Length of test in hours (rounded up to the next hour) * Max Users`
    - **Example**: If a Performance test runs for 90 minutes with 60 virtual users, 2 * 60 = 120 VUH will be billed
    - Note that a test's consumption of VUH is based on the actual max concurrency and duration of the test. If you configured a one-hour test ramping up to 20,000 virtual users, but stopped it when it reached 10,000 virtual users, the test would only consume 10,000 VUH. If the test was configured for 3 hours but you stopped it after 2 hours, it would consume the max concurrency reached times 2 (hours)
  - **GUI Functional testing**: `Sum of each browser session in a GUI Functional test: Length of a browser session in hours (rounded up to the next hour) * 100 VUH`
    - **Example**: A GUI Functional test has 2 browsers and 2 iterations with different sets of test data (each iteration runs in a separate browser session for isolation purposes). Each browser session runs for ~5 minutes. `Credits used = 2 (browsers) * 2 (iterations) * 100 (VUH per browser session in 1 hour) = 400 VUH`
    - Note that a test's consumption of VUH is based on the actual max concurrency and duration of the test

### Tests
- **Used for**: All test types (Performance, Functional, API Monitoring, Service Virtualization)
- **Description**: With this credit type, you will be charged for every test that you run, except for Debug tests that run for 10 users and up to 5 minutes maximum
- **Calculation**: One credit per test run, regardless of duration or complexity
- **Examples**:
  - A test runs for 1 minute and generates 10 virtual users/threads. No test credit is billed
  - A test runs for 10 minutes and generates 10 virtual users/threads. 1 test credit will be billed
  - A test runs for 50 minutes and generates 500 virtual users/threads. 1 test credit will be billed

## Charging Models by Test Type

### Performance Tests
- **Credit Type**: VU or VUH
- **Charging Model**: Based on concurrent users and test duration
- **VUH Calculation**: `Length of test in hours (rounded up to the next hour) * Max Users`
- **Factors**:
  - Peak concurrent virtual users (actual max concurrency reached)
  - Test execution duration (actual duration, not configured duration)
  - Number of scenarios
  - Load distribution across locations
- **Note**: Consumption is based on actual max concurrency and duration. If you stop a test early, only the actual consumption is billed

### Browser Performance Tests
- **Credit Type**: VU or VUH
- **Charging Model**: 100 times more VU or VUH than regular performance tests
- **Calculation**: `Number of virtual users * 100 VUH`
- **Examples**:
  - A test with **10 virtual users** would consume **1,000 VUH** (10 users × 100 VUH each)
  - A test with **25 virtual users** would consume **2,500 VUH** (25 users × 100 VUH each)
- **Note**: Usage is calculated per virtual user, making it easy to estimate costs based on your testing needs

**Note**: When running [browser performance tests](https://help.blazemeter.com/docs/guide/performance-create-browser-test.html) in BlazeMeter, you will consume 100 time more VU or VUH.

### GUI Functional Tests
- **Credit Type**: VUH (when using VUH plan) or Tests (when using Tests plan)
- **Charging Model**: 
  - **VUH**: Based on browser session length (rounded up to next hour) * 100 VUH per session
  - **Tests**: One credit per test run
- **Factors**:
  - Number of browsers
  - Number of iterations
  - Length of each browser session
  - Each iteration runs in a separate browser session for isolation purposes

### API Monitoring Tests
- **Credit Type**: VU (when using VU plan) or Tests (when using Tests plan)
- **Charging Model**: 
  - **VU**: 1,000 API calls equal 5 VU (increments of 5 VU are reserved for 24 hours)
  - **Tests**: One credit per test run
- **Factors**:
  - Number of API calls (for VU plan)
  - One credit per test run (for Tests plan)
  - Independent of number of steps or assertions
  - Includes scheduled and on-demand test runs

### Service Virtualization Tests
- **Credit Type**: VU (when using VU plan) or Tests (when using Tests plan)
- **Charging Model**: 
  - **VU**: Each running virtual service equals 100 VU. Each 2,500 transactions equal 5 VU that is reserved until midnight (local time) while the virtual service is running
  - **Tests**: One credit per test run
- **Factors**:
  - Number of running virtual services (100 VU each)
  - Number of transactions (5 VU per 2,500 transactions)
  - One credit per test run (for Tests plan)

## BlazeMeter Test Data Consumption

When you use [BlazeMeter Test Data](https://help.blazemeter.com/docs/guide/test-data-how-to-use.html) features as part of a test execution, you will consume 50% more VU or VUH. You can find the maximum number of test data rows that can be generated for your plan in the [plan comparison table](https://www.blazemeter.com/pricing).

**Example 1:**
A Performance test with 1,000 virtual users consumes 1,000 VUH. When you add BlazeMeter Test Data to that test, you incur 50% more in usage, amounting to 1,500 VUH.

**Example 2:**
A stand-alone virtual service processes 5,000 transactions, therefore consuming 110 VU (100 VU is consumed for running the service. Every 2,500 transactions consumes 5 VU more.) If you add BlazeMeter Test Data to it, you will consume 110 VU, plus 50% for transactions (55 VU), plus 1 for each virtual service, that is, 110+55+1=166 VU.

## Credit Calculation

### Understanding Credit Consumption

1. **Performance Tests (VUH)**:
   - Calculate based on actual peak concurrent users reached (not configured)
   - Multiply by actual test duration in hours (rounded up to next hour)
   - Consider load distribution across multiple locations
   - **Note**: If you stop a test early, only actual consumption is billed

2. **Browser Performance Tests (VUH)**:
   - Calculate: `Number of virtual users * 100 VUH`
   - Much higher consumption than regular performance tests

3. **GUI Functional Tests (VUH)**:
   - Calculate: `Sum of each browser session: Length in hours (rounded up) * 100 VUH`
   - Each iteration runs in a separate browser session

4. **API Monitoring Tests (VU)**:
   - Calculate: `1,000 API calls = 5 VU` (increments of 5 VU reserved for 24 hours)

5. **Service Virtualization (VU)**:
   - Calculate: `100 VU per running virtual service + 5 VU per 2,500 transactions`
   - Transactions VU reserved until midnight (local time)

6. **Tests Credit Type**:
   - Count total number of test executions
   - Each execution consumes one credit (except Debug tests: 10 users, up to 5 minutes)
   - No additional factors affect credit consumption
   - If a test failed to run or failed to generate a report (tests need to run for at least 2 minutes), the test will not be deducted from your test credits

### How Many Credits Will My Test Use?

If your billing is based on tests, credits are counted per test, not by duration or number of virtual users or threads. Each test takes a couple of minutes to start up and spin down. An hour-long test runs approximately 55 minutes long, plus time to start up and shut down.

If for whatever reason a test failed to run (for example, an error in a user uploaded script) or failed to generate a report (tests need to run for at least 2 minutes to generate a report), the test will not be deducted from your test credits.

### Where Can I See My Credit Type?

Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. You can check your maximum concurrency and remaining credits, as well as your credit type under **Settings > Accounts > Billing**.

**Note**: The billing page shows your credit type, maximum concurrency, and remaining credits. You can also check your maximum concurrency and remaining credits in the workspace settings.

### Optimizing Credit Usage

- **Performance Tests**:
  - Optimize concurrent user counts
  - Use appropriate test durations
  - Consider load distribution strategies
  - Use Private Locations for cost optimization
  - Stop tests early if goals are met (only actual consumption is billed)

- **Browser Performance Tests**:
  - Be aware of 100x multiplier
  - Use only when necessary
  - Consider regular performance tests for most scenarios

- **GUI Functional Tests**:
  - Optimize number of browsers and iterations
  - Minimize browser session duration
  - Use test scheduling efficiently

- **API Monitoring Tests**:
  - Optimize number of API calls
  - Use test scheduling efficiently
  - Remove unnecessary test runs

- **Service Virtualization**:
  - Optimize number of virtual services
  - Minimize transaction counts
  - Stop services when not in use

- **Test Data**:
  - Be aware of 50% additional consumption
  - Use only when necessary
  - Check plan limits for maximum test data rows

## Using MCP Tools

While there are no specific MCP tools for credit management, you can use workspace tools to access billing information:

**Get Workspace Billing Information**:
- Tool: `blazemeter_workspaces`
- Action: `read`
- Required args: `workspace_id` (integer)
- Returns: Workspace details including billing usage information

**Example Workflow**:
1. Use `blazemeter_workspaces` with action `read` to get workspace details
2. Check billing usage information in the workspace response
3. Monitor credit consumption patterns

## Viewing Usage Reports

BlazeMeter Usage Reports provide metrics about the utilization of BlazeMeter in your organization. These metrics include high-level utilization data that is available either in graphs or JSON payloads, aggregated daily. You can also download detailed (per-test) utilization data in CSV format.

### How to Access Usage Reports

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
2. Select the level, either **Account** or **Workspace**
3. Select **Usage Reports**

Alternatively you can also [automate report gathering by making calls to the BlazeMeter API](https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html#retrieving), as described below.

### Filter Usage Reports By Type and Time Period

BlazeMeter aggregates usage report on a daily basis. These aggregated reports provide quick, high-level usage information. Usage reports display information based on the type of plan they have.

You can filter the usage reports by the following criteria:
- **Start Date**
- **End Date**
- **Group by**: In certain reports, the totals can be grouped by either test type or user:
  - Test Type (only for Number of Tests, Variable Unit Hours, and Max Number of Variable Units)
  - User (only for Variable Unit Hours)
  - None (default)
- **Select Report Type**:
  - Number of Tests
  - API Functional Tests - Number of API Calls
  - Number of Server Hours
  - Variable Unit Hours
  - Max Number of Variable Units
  - Virtual Services Transactions
  - Virtual Services Concurrent Usage
  - GUI Functional Tests - Number of Browser sessions

On the far right, the usage report also indicates the total - either the total number of tests, of calls, of hours, of transactions, or of users, respectively.

**Note**: For more specific information about **Virtual Services Transactions** and **Virtual Services Concurrent Usage** metrics, see [Virtual Services Analytics](https://help.blazemeter.com/docs/guide/mock-service-transactional-analytics.html).

### How to Download Detailed Usage Reports

If you need more details about test names, project-level utilization, test size and duration, and much more, download the Detailed Usage Report CSV file.

The detailed report includes the following information:
- **Date**: Displays Date and time the test ran
- **Workspace Id**: Unique identifier of the workspace in an account
- **Workspace Name**: Name of the workspace
- **Test Name**: Name of the test configuration
- **Link to Test**: URL to your test in the workspace (requires workspace permissions to view)
- **Report Name**: Name of the report for the test run (defaults to Test Name but can be edited)
- **Link to Report**: URL for viewing the report in the workspace (requires workspace permissions to view)
- **Max Users**: Max number of virtual users reached during the test
- **Duration (m)**: Duration of the test run (actual run time if stopped early)
- **Number of Virtual Users**: Number of configured virtual users
- **Number Of Servers**: Number of provisioned engines or instances in a test
- **Server Hours**: Number of server hours consumed by provisioned engines or instances
- **Variable Unit Hours**: Number of Variable Unit Hours consumed in a test
- **Functional Test API calls**: Applies only to Functional API tests - The number of calls made in your test scenario
- **Locations**: Geolocation of the load generators. For more information, see [Load Distribution](https://help.blazemeter.com/docs/guide/performance-load-distribution.html)
- **Test Type**: Displays as: JMeter, Taurus, FunctionalGui, FunctionalAPI, or URL
- **Execution Client Id**: Type of client that launched the test (Examples: GUI, API, Taurus, BE_CHROME (Chrome Extension), etc.)
- **Is Free Test**: Confirms whether credits were consumed
- **Credits Type**: Identifies the credit option for a test
- **Credits Used**: Number of consumed credits for a test
- **Plan Name**: Assigned name of the provisioned plan to your account
- **Project Id**: Unique identifier of the project in a workspace
- **Project Name**: Assigned name of project
- **User Id**: Unique identifier of User
- **User Email**: Email from User in the account or workspace
- **First Name**: First name of the user
- **Last Name**: Last name of user
- **Report Notes**: Notes and comments about the results
- **First Sample**: Date and time of first sent sample
- **Last Sample**: Date and time of last sent sample
- **Parallel tests in account**: Number of tests running concurrently in the entire account
- **Parallel tests in workspace**: Number of tests running concurrently in the workspace this test belongs to
- **End user experience test used**: Number of end-user experience monitoring test credits consumed

### Usage Report Scope and Access Permissions

**Account Level Usage Report:**
- Covers usage from all workspaces
- Can be accessed by users with the following roles:
  - Owner
  - Admin
  - Billing
- Access: **Settings > Account > Usage Report**

**Workspace Level Usage Report:**
- Covers only a single workspace
- Can be accessed by Account-level roles (Owner, Admin, Billing) as well as:
  - (Workspace) Manager
- Access: **Settings > Workspace > Usage Report**

You can check membership under **Settings > Workspaces > Members**.

### Retrieve Usage Report Data with the BlazeMeter API

Using API calls is useful if you want to automate downloading reports. For more information on how to handle the required authentication of your API calls, see [Authorization](https://help.blazemeter.com/docs/guide/api-authorization.html).

**Aggregated Usage Data in JSON Format:**
- Account level: `https://a.blazemeter.com/api/v4/accounts/{account_id}/reports/usage/tests/credits?daysInterval=1&toDate={timestamp}&fromDate={timestamp}`
- Workspace level: `https://a.blazemeter.com/api/v4/workspaces/{workspace_id}/reports/usage/tests/credits?daysInterval=1&toDate={timestamp}&fromDate={timestamp}`

**Detailed Usage Data in CSV Format:**
- Account level: `https://a.blazemeter.com/api/v4/accounts/{account_id}/reports/usage/tests/credits?daysInterval=1&toDate={timestamp}&fromDate={timestamp}&download=true`
- Workspace level: `https://a.blazemeter.com/api/v4/workspaces/{workspace_id}/reports/usage/tests/credits?daysInterval=1&toDate={timestamp}&fromDate={timestamp}&download=true`

---

## Annual vs Monthly Subscription

BlazeMeter offers both annual and monthly subscription options. Understanding the differences helps you choose the best plan for your needs.

**Use when**: Choosing between annual and monthly subscription plans or understanding subscription options.

### Annual Subscription

- Based on the plan that you select, you are eligible for the features included in that plan.
- The annual subscription is cheaper than the monthly subscription.
- Annual subscriptions can be cancelled at any time before the renewal date. For more information about how to cancel the subscription within the platform, see [Canceling a Subscription](#canceling-a-subscription). You continue to have access to the service until the last day of your billing period.
- Annual plans that are cancelled before the end date of the subscription are not renewed and your account automatically returns to a free subscription.
- Your account automatically renews at the end of the year unless you change your subscription.

### Monthly Subscription

- Based on the plan that you select, you are eligible for the features included in that plan.
- The monthly subscription is more costly compared to annual subscription.
- You can cancel the service, or downgrade, or upgrade your plan service without penalty.
- Your account automatically renews each month unless you change your subscription.

### Pricing Page

For more information regarding the pricing of the subscriptions, see [our pricing page](https://blazemeter.com/pricing).

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Annual vs Monthly Subscription**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-annual-vs-monthly-subscription`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-annual-vs-monthly-subscription"]}`

---

## Canceling a Subscription

Canceling a paid subscription reverts your account back to the Free tier after the end of the billing cycle. Canceling the current subscription is also a prerequisite to [downgrade a subscription](#upgrade-and-downgrade).

**Use when**: Canceling a paid subscription or downgrading your plan.

### Steps to Cancel

1. Log in to BlazeMeter as Account Admin.
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**.
3. In the **Account** section, click **Billing**.
4. In **Billing**, scroll all the way down to the end of the billing history panel. Click **Cancel Subscription** at the bottom left corner of the page.

### The Remainder of the Plan

After canceling your subscription, you will still be able to use your plan until the end of your current billing cycle. Example: If you are billed on the 20th of every month and you cancel on March 10th, you can still use your plan until March 20th.

Once your account is canceled and after the billing period has ended (e.g. the end of the month), all data and reports are removed from storage. If you do not want the data to be removed, contact [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com) and inform us not to remove the data. Be sure to include your username.

### Confirm Cancellation

You can verify that your plan has been canceled. Review the **Payment Method** section in the **Billing** page. If there is no message for "NEXT PAYMENT DUE" next to your Credit Card information, this means that you have successfully canceled your subscription.

### Annual Subscription Cancellation Fee

We don't believe in Fees. If you cancel an annual plan before the end of the contract period, you *do not* need to pay a cancellation fee. You cancel and your subscription won't renew.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Canceling a Subscription**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-cancelling-a-subscription`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-cancelling-a-subscription"]}`

---

## Credit Balance

At any point of time if you would like to check your credit balance (credit usage), follow these steps:

**Use when**: Checking your credit balance, monitoring credit usage, or reviewing subscription details and remaining credits.

### View Credit Balance

Follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**.
2. Go to **Account > Billing**.
3. Notice the **Subscription** panel. You are presented with the following balances per month/billing cycle:
   - **Max Concurrency Load Engines**
   - **Test Duration**
   - **Total Tests**
   - **Remaining Tests**
   - **Report Retention**
   - **Max Total Parallel VUs**
   - **Parallel Runs**

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Credit Balance**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-credit-balance`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-credit-balance"]}`

---

## Getting Invoices and Receipts

**If you've purchased one of our plans, you can access the subscription dashboard after logging into your account.**

**Use when**: Accessing invoices and receipts, downloading billing documents, or reviewing payment history for BlazeMeter subscriptions and purchases.

### Access Invoices and Receipts

Follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**.
2. Navigate to the **Account** section then click **Billing**.
3. View the **Billing Details** section. Scroll down to find your invoices.

### Users Without Subscriptions

If you don't have a monthly subscription with BlazeMeter, the following page will appear when you click the "Invoice, Payments & Subscription" link.

For users without subscriptions, you may need to contact BlazeMeter support or your account manager to access billing information.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Getting Invoices and Receipts**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-getting-invoices-and-receipts`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-getting-invoices-and-receipts"]}`

---

## How Many Credits Will My Test Use?

Credits are counted per test, not per minute, hour, or engines. Each test takes a couple of minutes to start up and spin down. An hour long test runs approximately 55 minutes long, plus time to start up and shut down.

**Use when**: Understanding credit consumption for test runs, calculating expected credit usage, or optimizing test configurations to minimize credit consumption.

### Credit Deduction Rules

**1 test credit will be deducted from your test credit balance once the test is completed. For multi tests, 1 credit will be deducted as well.**

### When Credits Are NOT Deducted

If for whatever reason a test failed to run (for example, an error in a user uploaded script) or failed to generate a report (tests need to run for at least 2 minutes to generate a report), the test will not be deducted from your test credits.

### Important Notes

- Credits are counted **per test**, not per minute, hour, or engines
- Each test takes a couple of minutes to start up and spin down
- An hour long test runs approximately 55 minutes long, plus time to start up and shut down
- Multi-tests consume 1 credit total, not 1 credit per sub-test
- Failed tests or tests that don't generate reports (less than 2 minutes) don't consume credits

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**How Many Credits Will My Test Use**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-how-many-credits-will-my-test-use`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-how-many-credits-will-my-test-use"]}`

---

## Purchasing Additional Credits

As an account owner, you can easily refill your credit balance when your team's credits are running low. This means that you don't have to stop testing if you run out of credits before the end of the billing cycle.

Applies to Basic Monthly, Basic Annual, and Pro Monthly accounts.

**Use when**: Refilling credit balance when credits are running low or purchasing additional credits before the end of the billing cycle.

### How do I know when it's time to renew?

BlazeMeter automatically triggers alerts if the number of remaining credits goes below 10% of the total number of credits included in your current plan. There are two types of alerts:

- Email notifications
- On-screen messages

You can renew your subscription before your colleagues try to run tests with an insufficient number of credits.

Once you refill your credit, any remaining credits in your previous plan are rolled over to your new plan (up to 10%). Any unused credits at the end of the current billing cycle are rolled over automatically to the credit balance of the next billing cycle.

**Example:** You have a Basic Monthly plan which lets you run up to 15 tests a month. 3 weeks into the billing cycle, you see an on-screen message indicating you are almost out of test credits. This message indicates that you have used up 14 tests out of the 15 tests included in your current plan, and you are only allowed to run one more test. To continue testing, you decide to refill your credit balance.

### How do I purchase additional credits?

Perform one of the following actions to upgrade or renew your plan:

- In an email notification, click **Upgrade your plan**
- In an on-screen message, click **upgrade your plan**
- In BlazeMeter, **renew or upgrade your plan**. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. Under **Account**, click **Billing:** The **Subscription** page displays: Click **Renew** to purchase the same plan again or click **Upgrade** to purchase a better plan.

**Result:** An additional number of credits (either test credits or VUHs) is added to your account. A pop-up displays with a summary of the number of credits you're buying and how much you'll be charged. When you confirm, the credits are available for immediate use.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Purchasing Additional Credits**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-purchasing-additional-credits`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-purchasing-additional-credits"]}`

---

## Purchasing Process for API Monitoring

After your account has been set up, a Free plan is active by default. For a Free plan, no billing information is required. For customers who want to upgrade from the Free plan to a Basic or Pro plan, the process is straightforward. All you have to do is choose a subscription plan and complete the purchasing process.

**Use when**: Upgrading from Free plan to Basic or Pro plan for API Monitoring or completing the purchasing process for API Monitoring subscriptions.

### Navigating to the Billing Screen

To reach the Billing screen, click the **Subscriptions** button next to your Profile. The Plans menu appears.

### Choosing a Subscription

1. On the Billing screen, select the plan to upgrade to. Alternatively, you can select **Contact Sales** for the Unleashed plan.
2. Enter the details of the customer making the purchase, including name and address, and click **Next**.
3. Enter a valid credit card number, the expiration date of the card, and the security code on the back of the card., then click **Next**.
4. Check that the entered information is correct, then click **Upgrade**. The purchasing process is complete.

### Updating the Billing Details

If there are changes in the billing details of an existing plan, follow the steps outlined in [Purchasing Process for BlazeMeter Digital Plans](#purchasing-process-for-blazemeter-digital-plans).

### Summary

Your billing details are not visible to any other users. Even Admin users cannot see this information. In case there are any changes in the Billing Details or Payment information, you can always go back and edit them.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Subscription Process for API Monitoring**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-purchasing-process-for-api-monitoring`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-purchasing-process-for-api-monitoring"]}`

---

## Purchasing Process for BlazeMeter Digital Plans

After your account has been set up, a Free plan is active by default. For a Free plan, no billing information is required. For customers who want to upgrade from the Free plan to a Basic or Pro plan, the process is straightforward. All you have to do is chose a plan and complete the purchasing process.

You complete the purchase in three steps:

1. Choose the desired plan and payment frequency
2. Provide information on the purchaser, and
3. Enter credit card details.

Typically, the person making the purchase handles billing for the company. In some cases, a third party service provider purchases the plan for the company. In the following instructions, we will explain the differences between these two types of purchasers.

**Use when**: Upgrading from Free plan to Basic or Pro plan for BlazeMeter Digital Plans or completing the purchasing process for BlazeMeter Digital Plans subscriptions.

### Navigating to the Billing Screen

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. Click **Account Settings > Billing** on the left-hand side of the screen.
2. Under the Account tab, click Billing. The Billing screen opens in the main area of the screen.

### Updating the Current Plan

Whether you are starting out with the Free plan or perhaps have the Basic plan, you upgrade the plan in the same way. For customers who have the Basic plan and are upgrading to the Pro plan, the cost of the new plan is prorated based on the time left in the previous plan.

1. Click on the Upgrade button in the upper right hand corner of the Billing screen: In the top section of the screen will appear the upgrade options.
2. Choose your payment frequency. You have a choice between annual and monthly payment plans. As you can see, the Annual plan gives you a discount. The decision is yours!
3. If you currently have the Free plan, you'll have a choice between the Basic and Pro plans. For convenience, the cost (per month) and plan details are displayed. If you choose the annual plan, you'll see: And for the monthly plan, you'll see:
4. Click the **Upgrade** button corresponding to the plan you choose.

### Filling out the Payment Information for Plan Upgrades

The next stage after choosing the type of upgrade (Basic or Pro) from the Free plan, is to enter the billing information. If you are upgrading from a Basic plan to the Pro plan, then there is no need to enter billing information since it has already been filled out. In case there is a change in those details, see the section below on how to edit them.

This is an example of what you would see if you upgraded to the Basic plan.

After clicking **Upgrade**, the following wizard opens:

1. Enter the details of the customer making the purchase, including name and address, and click **Next**. The following page displays:
2. Enter a valid credit card number, the expiration date of the card, and the security code on the back of the card., then click **Next**. The following page displays:
3. Check that the entered information is correct, then click **Upgrade**. The following page displays:

The purchasing process is complete.

### Updating the Billing Details

If there are changes in the billing details of an existing plan, follow these steps.

1. Open the **Billing** page:
2. Click the **Edit** button on the right of the **Billing Details** section.
3. Fill in the fields including the name of the person making the purchase, the company name, and address details. If you are a third party making this purchase for another company, put in your name and your company information here. This is because the information you enter will also appear on the invoices. The email field is automatically filled with the email of the person who set up the account.
4. When you are done, click **Save Changes**. Otherwise, if you do not want to save the information that was entered, click **Close** to discard the form.

### Updating the Payment Information

The payment method is always credit card.

1. Open the Billing page:
2. Click the **Edit** button on the right of the **Payment Method** section.
3. Fill in the fields including the name of the person making the purchase, the company name, and address details, the click **Next**.
4. Enter a valid credit card number, the expiration date of the card, and the security code on the back of the card, the click **Next**.
5. Review the payment method details, then click **Confirm**.

### Summary

Your billing details are not visible to any other users. Even Admin users cannot see this information. In case there are any changes in the Billing Details or Payment information, you can always go back and edit them.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Purchasing Process for BlazeMeter Digital Plans**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-purchasing-process-for-blazemeter-digital-plans`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-purchasing-process-for-blazemeter-digital-plans"]}`

---

## Refunds

If you have questions regarding Refunds, [contact Support](https://help.blazemeter.com/docs/answers/support-ticket.html) with the relevant Invoice number.

**Use when**: Requesting refunds for credits or understanding refund policies.

### Frequently Asked Questions

- See [BlazeMeter Credit Types and How They are Charged](#credit-types-and-charging).
- If for whatever reason a test failed to run (for example, an error in a user uploaded script) or generate a report (tests need to run for at least 2 minutes to generate a report) the test will not be deducted from your test credits.
- If the test is mistakenly counted against your test credits, [contact Support](https://help.blazemeter.com/docs/answers/support-ticket.html) and we will refund your credits.
- Credits do not carry over from one billing cycle to the other.
- If you are mid way through your monthly cycle and need an immediate capacity upgrade, then you will be upgraded and charged for the new plan mid cycle but the credits from your original tier will NOT be carried over or refunded.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Refunds**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-refunds`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-refunds"]}`

---

## Upgrade and Downgrade

You can upgrade, downgrade, or change plans at any time.

For example, if you are on the Basic plan but need higher capacity, you can opt to upgrade to our Pro plan. If you were on the Pro plan but your project has ended and you need less capacity, cancel the Pro plan and then upgrade to the Basic plan.

**Use when**: Upgrading or downgrading your subscription plan or changing plans.

### What happens to my credits?

If you are in the middle of your monthly cycle and need an immediate capacity upgrade, then you will be upgraded and charged for the new plan mid-cycle. *The credits from your original tier will not be carried over.* You cannot have 2 simultaneous subscriptions or varying levels of credit capacity.

### How do I downgrade?

To downgrade a paid subscription, first [cancel your current subscription](#canceling-a-subscription), then upgrade it.

### How do I upgrade?

1. Log in to your account.
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**.
3. Click **Settings** > **Account** > **Billing**.

On the Billing screen, you will see your subscription details.

To upgrade, click the yellow **Upgrade** button in the top right, and select the new plan that you want.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Upgrade and Downgrade**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-upgrade-downgrade`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-upgrade-downgrade"]}`

---

## Why is BlazeMeter Billing VAT Based

VAT: As BlazeMeter is a product that is ONLY electronically delivered, VAT is collected when selling to European customers. Based on the new tax regulations, all products which are ONLY electronically delivered will be subject to VAT.

You must fill in your company name and VAT ID upon payment.

**Use when**: Understanding VAT billing for European customers or filling in VAT information during payment.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Why is BlazeMeter Billing VAT Based**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-why-is-blazemeter-billing-vat-based`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-why-is-blazemeter-billing-vat-based"]}`

---

## Usage Reports

BlazeMeter Usage Reports provide metrics about the utilization of BlazeMeter in your organization. These metrics include high-level utilization data that is available either in graphs or JSON payloads, aggregated daily. You can also download detailed (per-test) utilization data in CSV format.

**Use when**: Viewing usage reports, analyzing credit consumption, filtering usage data, or downloading detailed usage reports.

### Access Usage Reports

Follow these steps:

1. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**.
2. Select the level, either **Account** or **Workspace**.
3. Select **Usage Reports**.

Alternatively you can also [automate report gathering by making calls to the BlazeMeter API](#retrieve-usage-report-data-with-the-blazemeter-api), as described below.

### Filter Usage Reports By Type and Time Period

BlazeMeter aggregates usage report on a daily basis. These aggregated reports provide quick, high-level usage information. Usage reports display information based on the type of plan they have.

You can filter the usage reports by the following criteria:

- **Start Date**: Select the start date for the report period
- **End Date**: Select the end date for the report period
- **Group by**: In certain reports, the totals can be grouped by either test type or user.
  - **Test Type** (only for Number of Tests, Variable Unit Hours, and Max Number of Variable Units)
  - **User** (only for Variable Unit Hours)
  - **None** (default)
- **Select Report Type**:
  - Number of Tests
  - API Functional Tests - Number of API Calls
  - Number of Server Hours
  - Variable Unit Hours
  - Max Number of Variable Units
  - Virtual Services Transactions
  - Virtual Services Concurrent Usage
  - GUI Functional Tests - Number of Browser sessions

On the far right, the usage report also indicates the total - either the total number of tests, of calls, of hours, of transactions, or of users, respectively.

For more specific information about **Virtual Services Transactions** and **Virtual Services Concurrent Usage** metrics, see [Virtual Services Analytics](skill-blazemeter-service-virtualization://references/analytics.md).

### How to Download Detailed Usage Reports

If you need more details about test names, project-level utilization, test size and duration, and much more, download the Detailed Usage Report CSV file.

In the detailed report you will find the following information:

- **Date**: Displays Date and time the test ran
- **Workspace Id**: Displays a Unique identifier of the workspace in an account
- **Workspace Name**: Displays name of the workspace
- **Test Name**: Displays name of the test configuration
- **Link to Test**: Identifies the URL to your test in the workspace. Requires workspace permissions to view
- **Report Name**: Displays name of the report for the test run. Defaults to Test Name but can be edited to reflect build number or other useful information
- **Link to Report**: Displays URL for viewing the report in the workspace. Requires workspace permissions to view
- **Max Users**: Displays the max number of virtual users reached during the test
- **Duration (m)**: Displays the duration of the test run. A test stopped prior to configured duration will show actual run time
- **Number of Virtual Users**: Displays number of configured virtual users
- **Number Of Servers**: Displays the number of provisioned engines or instances in a test
- **Server Hours**: Displays the number of server hours consumed by provisioned engines or instances in a test
- **Variable Unit Hours**: Displays the number of Variable Unit Hours consumed in a test
- **Functional Test API calls**: Applies only to Functional API tests: The number of calls made in your test scenario
- **Locations**: Indicates the geolocation of the load generators. For more information about locations, see [Load Distribution](skill-blazemeter-performance-testing://references/load-configuration.md)
- **Test Type**: Displays as: JMeter, Taurus, FunctionalGui, FunctionalAPI, or URL
- **Execution Client Id**: Describes type of client that launched the test. Examples: GUI, API, Taurus, BE_CHROME (Chrome Extension), etc.
- **Is Free Test**: Confirms whether credits were consumed
- **Credits Type**: Identifies the credit option for a test
- **Credits Used**: Identifies the number of consumed credits for a test
- **Plan Name**: Indicates the assigned name of the provisioned plan to your account
- **Project Id**: Displays a Unique identifier of the project in a workspace
- **Project Name**: Displays the assigned name of project
- **User Id**: Displays a Unique identifier of User
- **User Email**: Displays the email from User in the account or workspace
- **First Name**: Displays the first name of the user
- **Last Name**: Displays the last name of user
- **Report Notes**: Allows user to enter notes and comments about the results
- **First Sample**: Displays Date and time of first sent sample
- **Last Sample**: Displays Date and time of last sent sample
- **Parallel tests in account**: Indicates the number of tests running concurrently in the entire account
- **Parallel tests in workspace**: Indicates the number of tests running concurrently in the workspace this test belongs to
- **End user experience test used**: Indicates the number of end-user experience monitoring test credits consumed

### Usage Report Scope and Access Permissions

#### Account Level Usage Report

Account-level Usage Reports cover usage from all workspaces. They can be accessed by users with the following roles:

- Owner
- Admin
- Billing

Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. To access the Account-level Usage Report, choose **Settings > Account > Usage Report.**

#### Workspace Level Usage Report

Workspace-level Usage Reports cover only a single workspace. They can be accessed by any of the above Account-level roles, as well as the following Workspace-level role.

- (Workspace) Manager

Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. To access the Workspace level Usage Report, choose **Settings > Workspace > Usage Report.**

You can check membership under **Settings > Workspaces > Members**.

### Retrieve Usage Report Data with the BlazeMeter API

Using API calls is useful if you want to automate downloading reports. For more information on how to handle the required authentication of your API calls, see [Authorization](skill-blazemeter-api-reference://references/authentication.md).

To fetch aggregate usage report data in JSON, or detailed Usage Report in CSV format through our API, make calls modeled after the following examples.

#### Aggregated Usage Data in JSON Format:

- Example API call to pull aggregated data in JSON format at an Account level: `https://a.blazemeter.com/api/v4/accounts/84084/reports/usage/tests/credits?daysInterval=1&toDate=1537253999&fromDate=1534489200`
- Example API Call to pull aggregated data in JSON format at a Workspace level: `https://a.blazemeter.com/api/v4/workspaces/75969/reports/usage/tests/credits?daysInterval=1&toDate=1537253999&fromDate=1534489200`

#### Detailed Usage Data in CSV Format:

- Example API call to pull a detailed CSV at an Account level: `https://a.blazemeter.com/api/v4/accounts/84084/reports/usage/tests/credits?daysInterval=1&toDate=1537253999&fromDate=1534489200&download=true`
- Example API Call to pull a detailed CSV at a Workspace level: `https://a.blazemeter.com/api/v4/workspaces/75969/reports/usage/tests/credits?daysInterval=1&toDate=1537253999&fromDate=1534489200&download=true`

### Documentation References

For detailed information about usage reports, use the BlazeMeter MCP help tools:

**Usage Reports**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-how-do-i-view-my-usage-reports`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-how-do-i-view-my-usage-reports"]}`

---

## Documentation References

For detailed information about BlazeMeter credits and billing, use the BlazeMeter MCP help tools:

**Credit Types and Charging**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-blazemeter-credit-types-and-how-they-are-charged`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-blazemeter-credit-types-and-how-they-are-charged"]}`

**Usage Reports**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `usage-billing-how-do-i-view-my-usage-reports`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["usage-billing-how-do-i-view-my-usage-reports"]}`

