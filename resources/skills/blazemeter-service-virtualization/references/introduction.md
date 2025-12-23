# Service Virtualization Introduction

## Introduction

Introduction to Service Virtualization concepts, including terminology (transactions, services, virtual services, templates, tags), configurations tab, and the Start Virtualizing Now wizard.

**Use when**: Getting started with Service Virtualization or understanding terminology, configurations tab, and the Start Virtualizing Now wizard.

### Overview

Service Virtualization emulates the behavior of web services to remove dependencies during development and testing.

### Key Terminology

#### Transaction

A Transaction is a request/response pair that is associated with a given Service. For example, in the Swagger Petstore, GET /pet/{petId} and its associated response is a Transaction. The request in a Transaction can be a single request, or it can represent multiple potential requests using regular expressions.

#### Service

Within BlazeMeter, a Service is a logical grouping of Transactions. These Transactions can be anything, but typically, a Service is a grouping of Transactions that are related to a specific live service. Anytime you upload Transactions from a supported file type, you are prompted to either assign those Transactions to a Service or create a new Service.

The [Transactions](https://help.blazemeter.com/docs/guide/mock-service-transaction-repository-transaction-types.html) section lists all of the Transactions that are available to you. You can filter the list of Transactions by Service name to make it easier to find the specific Transaction that you are looking for.

When you are creating a virtual service, you are required to associate the virtual service with a Service. The Transactions that are available for your virtual service are determined by the Service that you select. You can either choose from existing Transactions in the service, or you can upload a Swagger, HAR, or WSDL file that has the Transactions that you need. To learn more about file formats, see [Adding Transactions](https://help.blazemeter.com/docs/guide/mock-service-add-transactions.html).

#### Virtual Service

A virtual service can stand in for the live service for testing purposes. A **Transaction-Based virtual service** is filled with a collection of Transactions, typically a subset of the Transactions in a Service. You run a virtual service to deploy those Transactions. Once a virtual service is created and running, you can associate it with your test, embed it in your test scripts, or provide it during test execution.

#### Virtual Service Template

A template is a common collection of Transactions that you can use to generate a virtual service for those transactions anytime you need one. Templates are persistent objects that can either directly create virtual services or load transactions into a running virtual service when you associate it with a test.

#### Tags

In context of Transactions, a tag is a custom identifier that makes it easier to find the Transactions that you are looking for. In addition to filtering by service name, you can also search for transactions by their tags. Virtual services get predefined tags assigned automatically, so you recognize the virtual services that have optional settings enabled. These tags are "[Think Time](https://help.blazemeter.com/docs/guide/mock-service-think-time-irregular-response-latency.html)", "[Redirect to Live](https://help.blazemeter.com/docs/guide/mock-service-add-transactions.html#h_01F8XBM7A57RC0A59107YGA0PN)", or "[Stateful](https://help.blazemeter.com/docs/guide/mock-service-add-processing-actions.html)".

### The Configurations Tab

Rather than hard-coding recurring configuration values in a virtual service, transaction, or processing action, you can define environment variables for virtual services to use at runtime. Use the **Configurations** tab to create custom name-value pairs and refer to these properties in `${config.name}` format. To learn more, see [Virtual Services Configuration](https://help.blazemeter.com/docs/guide/mock-service-configurations.html).

**Note**: Configurations allow you to avoid hard-coding values and make your virtual services more flexible and reusable across different environments.

### The Learn More Tab

The **Learn More** tab lets you create a virtual service by uploading Transactions from a supported file type, such as Swagger or HAR. From the Virtual Services tab, you can also create a virtual service from an existing Service or a Template. If you want to add more Transactions to the Service, you can upload additional Transactions without having to switch tabs. As you create your virtual service, you can select the specific Transactions that you want to include and then run the virtual service to make them available for tests.

### The Start Virtualizing Now Wizard

To make onboarding of Service Virtualization users as easy as possible, use the "Start Virtualizing Now!" wizard. It is an interactive and guided step-by-step journey of how to create virtual services. In five steps, you can create ready-to-use virtual services with all necessary artifacts and settings.

Follow these steps:

1. Log in to BlazeMeter and click the **Service Virtualization** tab.
2. Click the **Start Virtualizing Now** button.
3. Follow the instructions in 5 steps to create the service, define the service, and configure it.
4. Click **Run Virtual Service**. BlazeMeter will set up the virtual service endpoint according your choices and run it.

Your virtual service is running. Copy the provided **Example Request URL** to your browser to review the response.

To use the virtual service, copy the provided **Endpoint** and use it in the place of the real service endpoint.

**Note**: The "Start Virtualizing Now!" wizard is an interactive and guided step-by-step journey that makes onboarding of Service Virtualization users as easy as possible. In five steps, you can create ready-to-use virtual services with all necessary artifacts and settings.

---

## The Role of Services

A Service is an entity for categorizing Transactions and virtual services into a logical grouping. When you create a virtual service, you can only add Transactions that are a part of the same service. Therefore, it is important that you associate your Transactions with a service name that is meaningful.

To learn more about Service Virtualization, Services, virtual services, and other key concepts, see:
- [Introduction to Service Virtualization](skill-blazemeter-service-virtualization://references/introduction.md)
- Managing services covers tasks such as [upgrading](skill-blazemeter-service-virtualization://references/management.md), [renaming or deleting](skill-blazemeter-service-virtualization://references/management.md), [cloning](skill-blazemeter-service-virtualization://references/management.md), and [importing and exporting](skill-blazemeter-service-virtualization://references/management.md) services.

---

## Use Cases and Capabilities

Integrating Service Virtualization with BlazeMeter tests helps remove common testing constraints in a way that makes it easier to associate the virtual service with your tests. Virtual services in BlazeMeter also empower your ecosystem of developers and testers to collaborate and reuse assets.

### Performance Testing with Service Virtualization

Service Virtualization helps you handle situations where a piece of your application might not be available for testing when you need it. When combined with BlazeMeter performance testing functionality, Service Virtualization can make performance testing easier and more powerful.

The following scenarios are examples where Service Virtualization is needed for performance testing:

- **Component-level isolation**: You can load test the whole system, but it can be difficult to discern what might be slowing things down at the component level. You also want to test specific services in isolation to see how they perform under load.

- **Early testing**: You want to start performance testing early, but some services are still in development and not completely ready to be included.

- **Third-party API testing**: You need to run performance tests against third party APIs but cannot do so without affecting the live service. It's possible that the third-party API provides a sandbox environment for performance testing, but using these environments can incur costs that you would rather avoid.

In each of these scenarios, the ability to virtualize the service in question removes the constraint and enables timely and fast performance testing.

Service Virtualization also supports functional testing in BlazeMeter.

### Empower Developers to Test with Virtual Services

The simplicity of Service Virtualization and its availability as an integrated part of BlazeMeter turns virtualization from what used to be either individualized in-code work at the developer level, or centrally managed COE work at the QA level, into a highly collaborative exercise that works for any organizational paradigm.

Consider the following examples of how you can collaborate across roles with Service Virtualization:

- **Open-source integration**: Developers who prefer to build their virtual services in open-source tools like Wiremock can export those definitions into BlazeMeter for broader usage.

- **Reusability**: Virtual services created on demand by developers and testers are available for other team members to reuse, or leverage to create similar services. As the team builds a library of Transactions for a given service, team members who need to test will increasingly find that the needed Transactions already exist, and spinning up a virtual service is as simple as selecting those Transactions.

- **QA COE enhancement**: A QA COE can improve, augment, and organize Transactions contributed by the whole team in a way that makes them more powerful and easier to find.

All of these scenarios ultimately empower developers to test with Service Virtualization in a more convenient and accessible manner.

### Self-defining Test Assets

Testing has historically required the creation of various assets required to complete the tests (like virtual services) in different tools without any unifying platform. Service Virtualization takes BlazeMeter in a direction where tests start to become self-defining assets.

In BlazeMeter, with Service Virtualization fully integrated, you can now associate your test with virtual service data during test creation. You can also manage virtual services as a test dependency directly in your test scripts.

The more information you can build into the test itself about what it needs to run, the more efficient and self-defining your tests become.

---

## Service Virtualization Use Cases and Capabilities

Integrating Service Virtualization with BlazeMeter tests helps remove common testing constraints in a way that makes it easier to associate the virtual service with your tests. Virtual services in BlazeMeter also empower your ecosystem of developers and testers to collaborate and reuse assets.

**Use when**: Understanding Service Virtualization use cases, capabilities, or integrating virtual services with BlazeMeter tests.

### Performance Testing with Service Virtualization

Service Virtualization helps you handle situations where a piece of your application might not be available for testing when you need it. When combined with BlazeMeter performance testing functionality, Service Virtualization can make performance testing easier and more powerful.

The following scenarios are examples where Service Virtualization is needed for performance testing:

- You can load test the whole system, but it can be difficult to discern what might be slowing things down at the component level. You also want to test specific services in isolation to see how they perform under load.
- You want to start performance testing early, but some services are still in development and not completely ready to be included.
- You need to run performance tests against third party APIs but cannot do so without affecting the live service. It's possible that the third-party API provides a sandbox environment for performance testing, but using these environments can incur costs that you would rather avoid.

In each of these scenarios, the ability to virtualize the service in question removes the constraint and enables timely and fast performance testing.

Service Virtualization also supports functional testing in BlazeMeter.

### Empower Developers to Test with Virtual Services

The simplicity of Service Virtualization and its availability as an integrated part of BlazeMeter turns virtualization from what used to be either individualized in-code work at the developer level, or centrally managed COE work at the QA level, into a highly collaborative exercise that works for any organizational paradigm.

Consider the following examples of how you can collaborate across roles with Service Virtualization:

- Developers who prefer to build their virtual services in open-source tools like Wiremock can export those definitions into BlazeMeter for broader usage.
- Virtual services created on demand by developers and testers are available for other team members to reuse, or leverage to create similar services. As the team builds a library of Transactions for a given service, team members who need to test will increasingly find that the needed Transactions already exist, and spinning up a virtual service is as simple as selecting those Transactions.
- A QA COE can improve, augment, and organize Transactions contributed by the whole team in a way that makes them more powerful and easier to find.

All of these scenarios ultimately empower developers to test with Service Virtualization in a more convenient and accessible manner.

### Documentation References

For detailed information about Service Virtualization use cases and capabilities, use the BlazeMeter MCP help tools:

**Service Virtualization Use Cases and Capabilities**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-use-cases-and-capabilities`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-use-cases-and-capabilities"]}`

---

## The Role of Services in Service Virtualization

A Service is an entity for categorizing Transactions and virtual services into a logical grouping. When you create a virtual service, you can only add Transactions that are a part of the same service. Therefore, it is important that you associate your Transactions with a service name that is meaningful.

**Use when**: Understanding the role of Services in Service Virtualization, categorizing Transactions, or creating logical groupings for virtual services.

### Overview

To learn more about Service Virtualization, Services, virtual services, and other key concepts, see:

- [Introduction to Service Virtualization](skill-blazemeter-service-virtualization://references/introduction.md)
- Managing services covers tasks such as [upgrading](skill-blazemeter-service-virtualization://references/management.md), [renaming or deleting](skill-blazemeter-service-virtualization://references/management.md), [cloning](skill-blazemeter-service-virtualization://references/management.md), and [importing and exporting](skill-blazemeter-service-virtualization://references/management.md) services.

### Documentation References

For detailed information about the role of Services in Service Virtualization, use the BlazeMeter MCP help tools:

**The Role of Services**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-the-role-of-services`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-the-role-of-services"]}`

### Capabilities

- **Request Matching**: Match requests based on various criteria (URL, headers, query parameters, cookies, credentials, body)
- **Dynamic Responses**: Generate responses dynamically using templates and helpers
- **State Management**: Manage stateful service interactions through State Update processing actions
- **Processing Actions**: Execute webhooks, HTTP calls, and state updates
- **Live System Integration**: Redirect unmatched requests to live systems
- **Test Data Integration**: Use BlazeMeter Test Data for dynamic responses

---

## Documentation References

For detailed information about Service Virtualization introduction, use the BlazeMeter MCP help tools:

**Service Virtualization Introduction**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-introduction`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-introduction"]}`

