# Load Configuration

## Load Configuration

Configure load settings for performance tests, including users, duration, iterations, ramp-up, RPS limits, and dynamic user changes. BlazeMeter allows you to control frequently changed parameters from the UI or API by overriding existing values, eliminating the need to edit hard-coded values in scripts and re-upload them between tests.

**Use when**: Configuring load settings for performance tests, setting up users, duration, iterations, ramp-up, or RPS limits, or overriding script values without re-uploading scripts.

### Override Settings

In the **Load Configuration** section, you can control the number of users, test duration, and ramp-up options by overriding existing settings:

1. On the **Performance** tab, open a test or create a test
2. On the **Configuration** tab, scroll down to the **Load Configuration** section
3. Specify appropriate values in the **Total Users**, **Duration**, and **Ramp Up Time** fields
4. (Optional) Specify additional options:
   - To limit the number of requests per second (RPS), click a preconfigured value in the **Limit RPS** list
   - To limit the number of ramp up steps, click a preconfigured value in the **Ramp Up Steps** list

In a multi-test scenario, you can also set overrides for individual tests that run as part of the multi-test. However, if overrides are disabled in a multi-test, the values will be taken from the original script of each single test.

### Disable Overrides

If you do not want to use any overrides, instead relying on the configuration in your original script, you can disable any and all overrides:

1. In the **Performance** tab, open a test or create a new test
2. In the **Configuration** tab, scroll down to the **Load Configuration** section
3. Click the toggle icon for each override you want to disable. Toggled right (and blue) is enabled. Toggled left (and gray) is disabled. When an override is disabled, the slider bar and number field is gray and will not be applied

To disable all overrides, ensure all toggles are set to the left (gray).

**Conditions for disabling overrides:**

Overrides can only be disabled under the following conditions:
- You have a paid BlazeMeter account
- Your script is a [JMeter](skill-blazemeter-performance-testing://references/advanced-features.md) script
- If your script is not a JMeter script, overrides will be disabled only if you upload a [Taurus](skill-blazemeter-performance-testing://references/taurus.md) YAML configuration file with your script and set the YAML file as the main test file, which will automatically disable UI overrides

### Select Total Users

Select the number of users you want deployed at the peak of your test. BlazeMeter will divide this user population across the number of test engines deployed.

**Multiple Thread Groups:**

If your script uses multiple thread groups, the following will apply:

- **If each thread group in the script is configured for 1 user** (the default setting) in the **Number of Threads (users)** field, BlazeMeter will divide the total number of users evenly across the thread groups, rounding up and down as needed.

  **Examples:**
  - If you specify 10 users for 2 thread groups, each thread group will run 5 users
  - If you specify 6 users for 3 thread groups, each will run 2
  - If you specify 11 users for 3 thread groups, BlazeMeter will round up (from 3.66) and each will run 4
  - If you specify 7 users for 3 thread groups, BlazeMeter will round down (from 2.33) and each will run 2

- **If you specify different user numbers for each of your multiple thread groups**, BlazeMeter will maintain the ratio of threads between the thread groups in the JMX script to achieve the total users you specify here.

  **Example**: If your JMX script has 3 thread groups and the **Number of Threads (users)** field in each of them is set to 5, 3, and 2 respectively, then a test with 1000 users specified in the Load Configuration section will run 500, 300, and 200 threads through those thread groups.

### Configure Duration or Iterations

You can configure your test to run either for a specified duration or for a specified number of iterations:

1. On the **Performance** tab, click **Create Test** and **Performance Test**
2. Scroll down to the **Load Configuration** section
3. In the **Duration / Iterations** section, turn on one of the following options:
   - **Duration**: Set the duration for the entire test, in minutes. The test will run infinite iterations until the duration is met
   - **Iterations**: Set the number of iterations instead. The test will run long enough to complete all iterations

### Limitations

When you specify iterations, be aware of the following limitations:

- You cannot run a test with a duration longer than your plan limit
- If you configure a **high-iteration test** using the overrides, *BlazeMeter will apply a default duration of approximately 1 hour and 10 minutes*. This safeguard is to prevent infinite tests, which can place an undue burden on system resources. If you must run a high-iterations test that will exceed an hour in duration, you can disable overrides and set values directly in your script, in which case the test can run through all iterations to completion
- If you disable overrides and have infinite iterations (loops) set in your script, specify a duration in your script. **Example**: If you configure a JMeter test to run infinite loops with no duration, BlazeMeter will apply a 10-second duration. This safeguard helps to prevent an undue burden on the system caused by infinite tests
- You cannot configure duration and iterations at the same time when you specify overrides, but if you disable *all* overrides, you can configure duration and iterations in the script (for example, in a JMeter script). If you configure both, the test will run until whichever limit (iterations or duration) is met first

**Note**: If you find that your test ended before running its full duration, review the preceding list of limitations for the possible cause.

**For JMeter Tests**: You can download the *artifacts.zip* file from the [Logs Report](https://help.blazemeter.com/docs/guide/performance-logs-report.html). Inside is a *modified_{your_script_name}.jmx* file. If you open that modified JMX file in your local JMeter, you can see any thread group overrides that BlazeMeter might have applied to your script.

### Configure Ramp Up Time and Steps

You can select how fast you want the test to ramp up. This is the elapsed time in minutes from the test start until all users are running. You can also select the number of steps for the ramp-up of your test.

**To configure ramp-up time, follow these steps:**

1. On the **Performance** tab, click **Create Test** and **Performance Test**
2. Scroll down to the **Load Configuration** section
3. Move the **Ramp Up Time** slider or enter the number of minutes in the box

**To configure ramp-up steps, follow these steps:**

1. Go to the **Load Configuration** section
2. In the **Ramp Up Steps** box, enter the value or expand the drop-down menu to select a value

**Ramp Up Steps:**

- The default value is 0, which delivers a linear ramp-up from test start until the end of ramp up time:

- A value of 5 delivers 20% of the peak users at the start and reaches 100% at the start of the 5th step:

### Limit Requests per Second (RPS)

With the RPS setting, you can specify the maximum number of requests per second (RPS).

To configure the RPS setting, follow these steps:

1. Go to the **Load Configuration** section
2. In the **Limit RPS** box, type or select a value

When you use this setting, you will see a **Change RPS** button on your live test reports and can make changes during the test.

### Change RPS Limits During a Test

To see how the number of requests per second affects system performance, you can change RPS limits during a test:

1. Start a test
2. At the top right corner of the reports section, click **Run Time Control**
3. Click **Change RPS**
4. To submit the new value to the test engines, in the box, set the RPS value and click **Apply**

### Change the Number of Users During a Test

You can change the number of concurrent virtual users during load testing to enhance the quality of performance insights. This feature provides an enhanced view of an application's behavior under various conditions, aids in uncovering latent issues, and can contribute to robust application performance optimization. Testers and developers alike can use this technique to fine-tune their applications with the goal of efficient operations even during periods of high user demand.

**This feature provides:**

- **Dynamic User Patterns**: During normal operations, the number of users engaging with an application varies. By altering the number of concurrent virtual users in real time, you can replicate the dynamic user patterns observed in real-world scenarios, providing a more accurate representation of application performance
- **Scalability Testing**: Adjusting the virtual user count allows you to determine an application's scalability limits. Identifying the point at which performance starts to degrade or become unstable aids in making informed decisions about resource allocation and infrastructure requirements
- **Bottleneck Detection**: Monitoring performance metrics as the virtual user count changes helps you detect performance bottlenecks, memory leaks, or other issues that might not be apparent under consistent conditions
- **Stress Testing**: By gradually increasing the number of virtual users, you can stress the application to its limits, uncovering how it behaves under extreme conditions. In this way, you can gauge the potential impact of sudden spikes in user traffic or unexpected surges
- **Load Balancing Validation**: By varying the number of users, you can validate load-balancing algorithms and configurations
- **Capacity Planning**: Dynamic concurrent user testing is critical for capacity planning

**To change the number of users during load testing:**

1. On the main menu, click the **Performance** tab
2. Click **Create Test** and **Performance Test**
3. On the **Test Configuration** page, turn on the **Change the number of users at run time** toggle

   **Important Notes:**
   - If a test only has a multi-thread group JMX script uploaded, the **Change the number of users at run time** toggle does not appear in the **LOAD CONFIGURATION** section
   - If multiple JMX scripts are uploaded (for example, one with a single thread group and one with multi-thread groups), the **Change the number of users at runtime** toggle behaves differently. This toggle is disabled when the multi-thread group script is the active test but enabled when the single-thread group script is the active script

4. Start a test
5. In **Reports**, click **Run Time Control**. This button is visible only after the test starts to run
6. Click **Change Number of Users**. A dialog box appears where you can change the number of users, ramp up time, and number of steps

   **Example**: In this example, the number of users is changed from 100 to 200 and the ramp-up time is set to 2 minutes. When updating these settings, you cannot exceed your plan limits

7. Set new values and click **Apply**. The **Summary** (or **Request Stats**) report displays the time and details of the changes
8. To see more details of the property changes, click the purple circle icon

---

## Load Distribution

BlazeMeter is a cloud-based service which lets you [choose the geographical location](skill-blazemeter-performance-testing://references/load-configuration.md) that you wish to run the load from.

When you think of load testing, it is understood that you would have more than one user hitting the website. To get the best realistic results from your load test, you should mimic the actual real time environment where the end users would be using your website. Typically, your users are located throughout the world. You can load test your application in the same way.

BlazeMeter provides you with the infrastructure and ability to select your desired multiple geographical location from where you would like the load to be generated while you are performing load test against your application.

You can run the test from one location or distribute the load across multiple locations. This selection can be modified before each run. This means that you can run the same test several times and choose a different location each time.

You can also change the default ratio of users to engines or set the engine count manually in cases where you are not using the Total Users setting.

**Use when**: Configuring load distribution across multiple geographic locations, setting up traffic weighting and engine-to-user ratios, or testing from specific geographic regions to simulate real-world user patterns.

- [Select a Location](skill-blazemeter-performance-testing://references/load-configuration.md)
- [Select Multiple Locations](skill-blazemeter-performance-testing://references/load-configuration.md)
- [Advantages of Generating Load from Multiple Geographic Locations](skill-blazemeter-performance-testing://references/load-configuration.md)
- [How the Engine to Users Ratio Works](skill-blazemeter-performance-testing://references/load-configuration.md) [Change the Ratio of Users to Engines](skill-blazemeter-performance-testing://references/load-configuration.md) [Set the Number of Engines When Total Users is Toggled Off](skill-blazemeter-performance-testing://references/load-configuration.md)
- [How to Set a Load Origin Location in your BlazeMeter Load Test](skill-blazemeter-performance-testing://references/load-configuration.md) [Best Practice for Selecting Load Origin Location in your BlazeMeter Tests](skill-blazemeter-performance-testing://references/load-configuration.md)
- [Locations You Can Generate Load From](skill-blazemeter-performance-testing://references/load-configuration.md)

### Select a Location

Follow these steps:

1. In the **Performance** tab, open a test or create a new test.
2. In the **Configuration**tab, scroll down to the**Load Distribution**section.
3. In the **Locations** column, expand the drop-down menu to display the list of locations and make your selection.Start entering a location name to filter the list:

### Select Multiple Locations

You can distribute your test Virtual Users load to multiple cloud locations. By default, the locations will be equally weighted.

Follow these steps:

1. To add another location, click the **+ Add Location** button. To delete a location, click the bin icon. Each time you click the **+ Add Location** button, a new line will be added and the % of traffic will be re-calculated to evenly distribute the users. There is a limit of ten locations per single test. After adding a 10th engine, the **+ Add Location** button will be grayed out. If your test requires more than ten locations, consider setting up a [multi-test](skill-blazemeter-performance-testing://references/scenarios.md) instead.
2. (Optional) To use multiple locations with a custom-weighted (unequal) distribution, make your edits in the **% of Traffic** field. While you are editing, a message will display that reminds you that your numbers must add up to 100%. To go back to equal distribution, click **evenly divide the traffic**.

### Advantages of Generating Load from Multiple Geographic Locations

Here are some of the advantages of generating load from multiple geo-locations:

- Mimic Actual End user usage pattern
- Ability to generate unique data stream to effectively test Load Balancer or other components
- Ability to hit the server with unique request and test its processing power
- Ability to check the effective usage of application code for features like concurrency, caching, cookie, session etc.
- Ability to check the Memory leakage issues
- Ability to check the effective configuration of the Database server to handle an incoming request, process it, and send the correct response
- Maximum coverage of website usage with respect to different client network parameters
- Ability to check the fail-over capability of the server
- Ability to check the proper working of network architecture
- Ability to check for requirements for scalability of existing hardware resources in different geographical locations.

### How the Engine to Users Ratio Works

BlazeMeter automatically calculates the number of engines you will need based on your entry in the Total Users field. The default ratio between users and engines is configured as part of your plan. In most cases, you do not need to alter this setting.

If your test is particularly resource intensive or you are running a JMeter test with multiple thread groups, you may want to change the ratio of users to engines.

### Change the Ratio of Users to Engines

Follow these steps:

1. In the **Performance** tab, open a test or create a new test.
2. In the **Configuration** tab, scroll down to the**Load Distribution**section.
3. Click the number to the left of **Max Users Per an Engine** and enter a new value or drag the slider. BlazeMeter will automatically adjust the number of required engines.

### Set the Number of Engines When Total Users is Toggled Off

If you have **Total Users** toggled off in your [Load Configuration](skill-blazemeter-performance-testing://references/load-configuration.md), you will need to set the number of engines for BlazeMeter to run your test on. The default is one but you can increase the number to the maximum allowed by your plan.

Follow these steps:

1. In the **Performance** tab, open a test or create a new test.
2. In the **Configuration** tab, scroll down to the**Load Distribution**section.
3. Click the number of **Total Engines** and enter a new value or drag the slider. BlazeMeter will automatically adjust the number of required engines. Use care with this setting, as the number of users your test creates will equal [users defined in your script] * [number of engines].

If this happens, go back and check the **Total Engines** slider. For example, you may have intended to run a 1-engine test, but the **Total Engines** setting may have accidentally been set to 2, especially if you are running a larger number of users (over 500).

To change your plan limit, click **Get More** to be taken to your Account Billing screen where you can see your plan, compare plans, or contact sales.

### How to Set a Load Origin Location in your BlazeMeter Load Test

You can choose the specific geographic location from which you wish to run your load. This selection can be modified before each run, that way you can run the same test several times and each time choose a different location in the world. For more information, see [Locations You Can Generate Load From](skill-blazemeter-performance-testing://references/load-configuration.md).

### Best Practice for Selecting Load Origin Location in your BlazeMeter Tests

- First, you should start with testing with the nearest location from the load locations available. Once you have run sufficient load tests and the results are in an acceptable range, select the farthest server and run the same test. Check the response times, see the network latency and perform any optimization required and rerun to verify the results.
- You can run load from multiple locations simultaneously by creating multiple tests with different load origin locations and then scheduling these tests to run at a predefined time to check the load on the test servers.
- You can use the **Multi Test** feature to monitor and view the results from different geographic locations in one aggregated report.
- You can run load from multiple locations with multiple tests with different network emulation values for maximum coverage.

### Locations You Can Generate Load From

We currently provide the following locations:

**Amazon Web Services (AWS) Locations:**
- US East (Virginia)
- US East (Ohio)
- US West (North California)
- US West (Oregon)
- Canada (Central)
- EU West (Ireland)
- EU West (London)
- EU West (Paris)
- EU Central (Frankfurt)
- Asia Pacific (Tokyo)
- Asia Pacific (Mumbai)
- Asia Pacific (Seoul)
- Asia Pacific (Singapore)
- Asia Pacific (Sydney)
- South America (Sao Paulo)

**Google Cloud Platform Locations:**
- US East (Virginia)
- US East (South Carolina)
- US West (Oregon)
- US West (California)
- US Central (Iowa)
- Canada East (Montreal)
- EU West (London)
- EU West (Frankfurt)
- EU West (Belgium)
- EU West (Netherlands)
- Asia East (Taiwan)
- Asia Northeast (Japan)
- Asia Southeast (Singapore)
- Asia South (Mumbai)
- Australia (Sydney)
- Brazil (Sao Paulo)
- Japan (Osaka)

**Microsoft Azure Locations:**
- US East (Virginia)
- US East 2 (Virginia)
- US West (California)
- US West 2 (US West 2)
- US West Central (US West Central)
- US Central (Iowa)
- US North Central (Illinois)
- US South Central (Texas)
- Canada East (Quebec City)
- Canada Central (Toronto)
- EU West (Netherlands)
- EU North (Ireland)
- UK West (Cardiff)
- UK South (London)
- Japan East (Tokyo, Saitama)
- Japan West (Osaka)
- Korea Central (Seoul)
- Korea South (Busan)
- East Asia (Hong Kong)
- Southeast Asia (Singapore)
- Central India (Pune)
- West India (Mumbai)
- South India (Chennai)
- Australia East (New South Wales)
- Australia Southeast (Victoria)
- Brazil South (Sao Paulo)

**Jump to next section:**
- [Failure Criteria](skill-blazemeter-performance-testing://references/advanced-features.md)

---

## Documentation References

For detailed information about load configuration, use the BlazeMeter MCP help tools:

**Load Configuration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-load-configuration` (load configuration), `performance-load-distribution` (load distribution)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-load-configuration", "performance-load-distribution"]}`

