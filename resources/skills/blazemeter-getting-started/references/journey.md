# Continuous Testing Journey

Understand the continuous testing journey in BlazeMeter, including best practices, workflows, and strategies for implementing continuous testing.

**Use when**: Understanding the continuous testing journey, implementing continuous testing strategies, or learning best practices for continuous testing workflows.

### Overview

In the app economy, the ability to release new functionality for your product with volume, velocity, and quality is imperative to competitive advantage, but quality can be difficult to achieve while doing so. Tools are difficult to integrate, and a tool preferred by developers may not be the tool preferred by testers. The end result? A large, disparate, loosely integrated tool chain that is a resource-intensive monster. We've all been there!

BlazeMeter solves this problem by providing all the components needed for the entire continuous testing process in one deeply integrated, intuitive workflow. This guide will walk you through this continuous testing journey, from beginning to end.

Your continuous testing journey can ultimately look like this, shifting left and shifting right to fit your needs. But for now, let's focus on starting the journey from square one.

**Note**: The continuous testing journey is designed to help you understand how different testing phases work together to create a comprehensive testing strategy. Each phase builds upon the previous one, creating a complete testing workflow.

### Phase 1: Functional Testing

Before you create your first performance tests, you want to ensure that all of your application server's required functions are up and running and available, and you want to ensure that the user interface (UI) is behaving as expected.

Start by recording GUI Functional Tests to test the user's experience with the UI in an actual web browser.

### Phase 2: Service Virtualization

After verifying your application server is functioning as expected, you're ready to move on to simulating some tests. BlazeMeter's Service Virtualization allow you to test even when you don't have access to a full test environment.

You can run a virtual service to deploy transactions, which are typically a subset of transactions in a particular service. Once a virtual service is created and running, you can associate it with your test, embed it in your test scripts, or provide it during test execution.

### Phase 3: Performance Testing

You've verified your application server is functioning as expected, and you've virtualized some tests to get an idea of what deploying transactions against your services will look like. Now it's time to jump into real Performance Testing!

Performance Testing via the BlazeMeter cloud is how you ensure that your application server will be able to handle the full load of users performing various actions all at once as soon as your application goes live. The Performance tab will provide you with a wide range of options for testing, starting with either running a single performance test or a combination of a multiple performance tests executed simultaneously, which we refer to as a Multi-Test.

Cloud testing leverages cloud computing resources and models to enable all aspects of load testing in a highly cost-effective manner. With cloud testing, you have unlimited resources at your disposal. You can perform all Performance Testing activities in the cloud with features such as real-time reporting.

### Phase 4: API Monitoring

You've verified that your application is both functioning properly and ready to perform well under load, so going forward, you'll want to keep an ever-watchful eye on your application server so as to avoid any surprise outages in the future.

Downtime can have a far-reaching impact on any business. Without proper visibility into the traffic running through your apps and infrastructure, diagnosing and solving the problem means using up valuable time and resources. BlazeMeter's API Monitoring surfaces issues directly from the internal and third-party APIs that power your apps and infrastructure.

It works by running API monitors -- either from around the globe or from within your infrastructure -- on a continuous schedule to give you visibility into API problems so you can prevent, identify and solve them fast -- before your customers notice.

### Now Start Your Journey!

If you're ready to begin your testing with BlazeMeter, then start with one of the following guides, depending on what type of user you are:

- [I'm an entirely new user!](https://help.blazemeter.com/docs/guide/getting-started.html)
- [I'm an existing BlazeMeter user!](https://help.blazemeter.com/docs/guide/getting-started-bzm-updates-for-bzm-users.html)
- [I'm a Runscope user!](https://help.blazemeter.com/docs/guide/getting-started-blazemeter-for-runscope-users.html)

---

## Documentation References

For detailed information about the continuous testing journey, use the BlazeMeter MCP help tools:

**Continuous Testing Journey**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `getting-started-continuous-testing-journey`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["getting-started-continuous-testing-journey"]}`

