# Migration Guides

## BlazeMeter for Runscope Users

Guide for Runscope users transitioning to BlazeMeter, including login process, understanding BlazeMeter features, locating Runscope functionality, and understanding teams vs workspaces.

**Use when**: Transitioning from Runscope to BlazeMeter or understanding BlazeMeter features, locating Runscope functionality, and understanding teams vs workspaces.

### Overview

Runscope users, welcome to BlazeMeter! Runscope has been merged with BlazeMeter, but all the functionality you're already familiar with remains intact—we've only added new features and functionality by merging our two tools. This guide will help you make sense of the changes so you can continue using Runscope features with minimal interruption.

### Logging into BlazeMeter as a Runscope User

This section only pertains to the **first time you log in** to BlazeMeter as a Runscope user.

1. **Log in to Runscope normally**. As soon as you do so, you will automatically be directed to your new BlazeMeter login screen
2. **Reset your password**. At the BlazeMeter login screen, you will be prompted to reset your existing Runscope password. This will only happen the first time you log in
3. **You're ready to go!** Your existing Runscope login is now your BlazeMeter login

### What is BlazeMeter?

BlazeMeter is a commercial self-service load testing platform-as-a-service (PaaS) which is fully compatible with various popular testing tools, such as Apache JMeter, Selenium, K6 for example. BlazeMeter has now expanded to be able to accommodate your entire [Continuous Testing Journey](https://help.blazemeter.com/docs/guide/getting-started-continuous-testing-journey.html).

Whereas Runscope helps you test the correctness of an API, BlazeMeter can help you load-test the API by simulating countless numbers of virtual users simultaneously from multiple locations around the world.

### Where is Runscope?

Once you setup your BlazeMeter account and login, you'll find the Runscope you're familiar with under the **API Monitoring tab**:

From there, everything underneath the tab should look quite familiar. All of Runscope lives under the API Monitoring tab within BlazeMeter. Simply continue using it as you always have—but now you can enjoy the new features added by BlazeMeter.

**Note**: The API Monitoring tab provides all the functionality you're familiar with from Runscope, including API test creation, monitoring, and reporting. The interface should be familiar, with additional BlazeMeter features integrated seamlessly.

### Runscope Teams vs BlazeMeter Workspaces

As a result of Runscope merging with BlazeMeter into one combined tool, there is now a wider range of team and workspace memberships you can be granted. You can work within Runscope teams just as you always have, but you can now additionally and optionally join BlazeMeter testing workspaces. Teams and workspaces are wholly apart from each other and do not share any permissions.

**Important details**:

- **Some settings specific to Runscope are in a separate menu apart from other BlazeMeter settings**. After clicking the API Monitoring tab, look for a face icon under your name
- **BlazeMeter testing workspace membership is wholly separate from API Monitoring team membership**. In other words, you are likely already familiar with how Runscope team membership works, as accessed via the familiar menu. Now you can additionally join performance and functional testing workspaces, which are used from within their respective tabs
- The important detail to remember is that BlazeMeter [workspaces](https://help.blazemeter.com/docs/guide/administration-workspaces-and-projects.html) are wholly apart from [API Monitoring teams](https://help.blazemeter.com/docs/guide/administration-api-monitoring-teams.html) and are accessed via their own menu

*We certainly understand that this division of user roles and permissions as presented here can take some getting used to. We're working on simplifying this functionality in future releases.*

---

## BlazeMeter for People Who Know JMeter

Guide for JMeter users using BlazeMeter, including compatibility, scalability, recording, script maintenance, multi-location testing, APM integrations, and network emulation.

**Use when**: Getting started with BlazeMeter as a JMeter user or understanding compatibility, scalability, recording, script maintenance, multi-location testing, APM integrations, and network emulation.

### Overview

People familiar with JMeter know that it's one of the best open source performance testing tools available on today's market. But no tool is foolproof and there are always pros and cons to be found with each one.

BlazeMeter is 'JMeter in the cloud'. This means it's not only 100% compatible with JMeter - but it also addresses its limitations like scalability, stability and reporting.

### Key Features for JMeter Users

With BlazeMeter, you can get:

- **'On-the-fly' script recording** with the BlazeMeter Chrome Extension
- **A simple way to maintain and execute JMeter scripts** from one location
- **The ability to generate up to 1,000,000 (or even more!) virtual users** - no need to worry about infrastructure cost and setup
- **Real time monitoring and reporting**
- **Easy access to historical reports** for comparison
- **The ability to test from multiple geo-locations** - no need to worry about test and report synchronization
- **The option to extend your test data further** with top-tier APM solution integrations like AppDynamics, Dynatrace, CA APM, New Relic and CloudWatch
- **End-to-end visibility** of your server, app (web and mobile), and end user experience
- **Ability to customize your script** by modifying [JMeter properties](https://help.blazemeter.com/docs/guide/performance-jmeter-properties.html) directly via BlazeMeter
- **Network emulation** for running with different bandwidth and latency configurations, useful for mobile testing

### Getting Started

With BlazeMeter, all you need is to directly upload your JMeter scripts, choose the number of load engines you wish to run on and run the test. BlazeMeter takes care of everything else! You'll have an unlimited number of pre-configured load engines available at your convenience. Detailed graphical reports are also generated during the load.

To get started, you can upload your JMeter script via the [Performance Test Screen](https://help.blazemeter.com/docs/guide/performance-create-test.html).

Want to learn more about running JMeter tests from BlazeMeter? Watch our on-demand recording, [How to Make JMeter Highly Scalable and More Collaborative With BlazeMeter](https://www.blazemeter.com/webinars/JMeter-Performance-Testing-Simple?utm_source=BM&utm_medium=kb&utm_campaign=blazemeter-for-people-who-know-jmeter).

**Note**: BlazeMeter is 100% compatible with JMeter, so you can use your existing JMeter scripts without modification. The platform addresses JMeter's limitations like scalability, stability, and reporting while maintaining full compatibility.

---

## BlazeMeter Updates for BlazeMeter Users

Guide for existing BlazeMeter users to understand platform updates, new features, and changes.

**Use when**: Understanding BlazeMeter platform updates, new features, or changes to existing functionality.

### Overview

Over time, BlazeMeter's functionality has been expanded to accommodate you throughout the whole [Continuous Testing Journey](https://help.blazemeter.com/docs/guide/getting-started-continuous-testing-journey.html).

### Functional & Performance Tests

The user interface distinguishes between Functional and Performance categories. This is simply to help with organization.

- When the Functional tab is active, only items relating to functional tests are shown
- When the Performance tab is active, only items relating to performance tests are shown. Examples of Performance tests are JMeter tests, URL/API Performance Tests, and Multi-Tests

### Service Virtualization

The [Service Virtualization](https://help.blazemeter.com/docs/guide/mock-service-introduction.html) tab lets you create "stand-in" services for real live services that you have no control over, or that are not ready to use yet. Virtual services can be stateless or stateful. Substituting services can be a powerful tool for testing purposes.

[Click here to learn how create your first test leveraging virtual services!](https://help.blazemeter.com/docs/guide/mock-service-create-first.html)

### Test Data

The test data integration spans across all components: Functional tests, Performance tests, API monitoring tests, as well as virtual services can load synthetically generated test data and custom CSV files.

The Test Data subtabs are where you define and store account-wide shared data entities that provide consistent values for all test types and for all team members.

### API Monitoring

The [API Monitoring](https://help.blazemeter.com/docs/guide/api-monitoring-create-your-first-api-monitoring-test.html) tab helps you monitor public, private, and third-party APIs in seconds, as well as evaluate the uptime, performance and correctness of an API.

As an existing BlazeMeter user, you are likely already familiar with BlazeMeter's features for performing functional or performance API tests. API Monitoring brings additional layers of API-related functionality. For example, once you've verified your APIs are working via functional tests, API Monitoring will help you ensure they remain functioning going forward.

For BlazeMeter users not already familiar with Runscope, there are some settings and permissions specific to API Monitoring that you'll want to be aware of:

- **Some settings specific to API Monitoring are in a separate menu apart from other BlazeMeter settings**. On the API Monitoring tab, look for a face icon under your name. Clicking the face icon opens a drop-down menu
- **BlazeMeter testing workspace membership is wholly separate from API Monitoring team membership**. In other words, you are likely already familiar with how [workspace](https://help.blazemeter.com/docs/guide/administration-workspaces-and-projects.html) membership works, as can be seen from your main BlazeMeter settings. The important detail to remember is that [API Monitoring teams](https://help.blazemeter.com/docs/guide/administration-api-monitoring-teams.html) are wholly apart from [workspaces](https://help.blazemeter.com/docs/guide/administration-workspaces-and-projects.html) and are accessed via their own menu

*We certainly understand that this division of user roles and permissions as presented here can take some getting used to. We're working on simplifying this functionality in future releases.*

### Ready to Learn More?

First, you can revisit our [Getting Started](https://help.blazemeter.com/docs/guide/getting-started.html) guide if you're like to review some of the functionality you're likely already familiar with. Even so, you may find that the recent updates to the guide make it worth a second look, and the guide includes many links to other various features, new and old alike.

Make sure to learn about [The Continuous Journey](https://help.blazemeter.com/docs/guide/getting-started-continuous-testing-journey.html), if you haven't already, for an overview of the big picture.

To learn how to make the most of any of the above tools, sign up for free courses at [BlazeMeter University](https://www.blazemeter.com/university)!

**Note**: BlazeMeter University provides free courses to help you learn how to use all the features of the platform. The courses cover everything from getting started to advanced topics.

---

## Documentation References

For detailed information about migration guides, use the BlazeMeter MCP help tools:

**Migration Guides**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `getting-started-blazemeter-for-runscope-users` (Runscope), `getting-started-bzm-for-people-who-know-jmeter` (JMeter), `getting-started-bzm-updates-for-bzm-users` (BlazeMeter updates)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["getting-started-blazemeter-for-runscope-users", "getting-started-bzm-for-people-who-know-jmeter", "getting-started-bzm-updates-for-bzm-users"]}`

