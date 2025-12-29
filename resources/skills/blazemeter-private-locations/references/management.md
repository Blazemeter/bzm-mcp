# Management

## Create

Create a Private Location in BlazeMeter, including setting up basic configuration, advanced configuration (engine hardware consumption, performance testing configuration), and functionalities (Performance, API Testing, Proxy Recorder, Service Virtualization, GUI Functional, Data Orchestration, Delphix Integration).

**Use when**: Creating a Private Location in BlazeMeter or setting up basic configuration, advanced configuration, and functionalities.

### Create a Private Location

A Private Location (formerly known as a harbor) is a logical container on the BlazeMeter end. A private location contains one or more agents (formerly known as ships). Private locations are servers with our agent installed on your end. You can have multiple private locations in your account; each will define a unique "location" to choose when running tests and deploying virtual services. You need to be a workspace manager to create Private Locations.

**Steps:**

1. Log into your BlazeMeter account as a workspace manager
2. Navigate to **Settings > Workspace > Private Locations**
3. Click + to add a new private location. The **Create a private location** window opens
4. Fill out the **Setup** section:
   - **Location name** - Give your private location a meaningful name that helps you team members choose the most appropriate location in the Location list when configuring tests
   - **Parallel engine runs** - Enter the number of separate parallel tests each agent is allowed to run in this private location. If using Kubernetes to create agents, enter a value greater than 1
5. (Optional) Toggle the **Agent Log**. When creating a new private location, the Agent Log is ON by default. To investigate agent failure or diagnose any agent connectivity issues, enable the agent log. You can view the logs and debug issues in real time. For more information, see [Enabling and Downloading Agent Log](skill-blazemeter-private-locations://references/management.md)
6. (Optional) Toggle the Advanced slider. For more information, see [Set Up the Advanced Configuration](skill-blazemeter-private-locations://references/management.md)
7. Click **Next**
8. Select at least one functionality that you would like this private location to install on the agents that are added. For more information, see [Set Up the Functionalities](skill-blazemeter-private-locations://references/management.md)
9. Click **Create**

You have created a Private location. The **Private Location** page opens and you can continue with the installation process for installing an agent. For more information, see the following installation procedures:
- Either [Installing a BlazeMeter Agent for Kubernetes](skill-blazemeter-private-locations://references/installation.md)
- or [Installing a BlazeMeter Agent for Docker](skill-blazemeter-private-locations://references/installation.md)

Verify that you see your Private Location in your Private Locations list, which is found in the **Settings > Workspace > Private Locations** section.

### Set Up the Advanced Configuration

#### Engine Hardware Consumption

- **Override number of CPUs** - This will override the default number of CPUs to the **whole number** value of CPUs you want the engines to run with (i.e. 2 for 2 CPUs)
- **Override memory (MB)** - This will override the default memory use for each engine in MB (i.e. for 8 GB of memory, set the number to 8192)

By default, containers created by the agent use the Docker Memory and CPU settings. These settings override the Docker maximum settings. If you enter a value greater than the maximum Docker settings, the agent uses the maximum settings instead. This option is available to help ensure that large containers designed for performance testing or Service Virtualization can later be reduced for less demanding tests or virtual services.

#### Performance Testing Configuration

- **Users per engine** - The number of virtual users that can be run on each individual test/engine
- **JVM Parameters XMX** - XMX specifies the maximum memory allocation pool for the Java Virtual Machine (JVM)
- **JVM Parameters XMS** - XMS specifies the initial memory allocation pool for the Java Virtual Machine (JVM)

By default, the virtual service container will have an initial Java heap size (XMS) of 16 GB and a maximum Java heap size (XMX) of 3 GB.

**GUI Functional Testing Requirements:**
- The current suggested configuration for this test type is 1 CPU and 2048 MB RAM per selected browser
- For running several browsers in parallel your machine should have ~(N+ceiling[N/20]) CPUs (where N - is the number of browsers, and ceiling[N/20] is the number of Taurus engines, with 1 Taurus engine per 20 browsers)
- For calculating the memory please, use the formula ((N+ceiling[N/20])*2048)

**Example:** If your test uses 2 browsers (Chrome and Firefox), the calculations will be the following:
- **CPUs**: (2+ceiling[2/20]) = 2+1 = 3
- **RAM**: (2+ceiling[2/20])*2048 = (2+1)*2048 = 6144

Thus the machine should have at least **3 CPUs** and **6144 MB** of RAM.

**Storage Recommendations:**
- We recommend using SSD storage on the machine as it will speed up GUI test execution
- For more than 8 parallel browsers, it's mandatory to have SSD storage

### Set Up the Functionalities

- **Performance** - Downloads all the images related to running Performance tests from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `taurus-cloud`, `apm-image`, `blazemeter/crane`, and `blazemeter` (Legacy JMeter users **ONLY**) images
- **API Testing** - Downloads all the images related to running API Functional tests from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `taurus-cloud`, `apm-image`, and `blazemeter/crane` images. **Note**: Starting February 2022, the API Functional testing feature has been deprecated. Depending on your subscription plan, you may still be able to run existing tests but can no longer create new ones. **Please use BlazeMeter API Monitoring to create and run your API Functional Tests going forward**
- **Proxy Recorder** - Downloads all the images related to creating and running the proxy recorder from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `blazemeter/proxy-recorder` and `blazemeter/crane` images
- **Service Virtualization** - Downloads all the images related to creating and running Service Virtualization from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `blazemeter/service-mock` and `blazemeter/crane` images
- **GUI Functional** (**Shared** run type only) - Downloads all the images related to GUI Functional test from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `taurus-cloud`, `apm-image`, `blazemeter/crane`, `blazemeter/charmander/firefox`, and `blazemeter/charmander/chrome`. The following options are available for the GUI Functional options:
  - **Default Firefox, Chrome, Microsoft Edge and Safari** - Installs the latest Firefox, Chrome, Microsoft Edge and Safari versions on the agent
  - **Select Version** - Gives you the choice of the currently supported Chrome, Firefox, Microsoft Edge, and Safari versions:
    - Chrome (latest 6 versions)
    - Firefox (latest 6 versions)
    - Microsoft Edge (latest 6 versions)
    - Safari (latest 6 versions)
  - **All Firefox, Chrome, Microsoft Edge and Safari** - Installs all Firefox, Chrome, Microsoft Edge and Safari versions on the agent
- **Data Orchestration**
- **Delphix Integration** - Downloads all the images related to the [Delphix integration](https://help.blazemeter.com/docs/guide/integrations-integrate-with-delphix.html) from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278))

---

## VS Cloud

Understand differences between cloud testing and private location testing, including target audience, prerequisites, processes, and recommendations for each approach.

**Use when**: Understanding differences between cloud testing and private location testing or deciding which approach to use based on target audience, prerequisites, and processes.

## Cloud vs Private Location

BlazeMeter is a commercial, self-service performance testing platform-as-a-service (PaaS), which is fully compatible with open-source [Apache JMeter](skill-blazemeter-performance-testing://references/scenarios.md) and [Taurus](skill-blazemeter-performance-testing://references/taurus.md). You can perform tests both off and on your premises.

**Use when**: Deciding between cloud and private location testing, understanding the differences between cloud and private location options, or determining which testing approach is best for your application.

### Cloud Testing with BlazeMeter

**Target Audience:**

This option is open to all who wish to perform load or functional testing on their website/application.

**Prerequisites:**

- BlazeMeter Account
- Application accessible outside your company firewall for testing, or ability to open the firewall to inbound traffic

**Process:**

- BlazeMeter creates instances on a public cloud using Amazon, Azure, or Google Compute Cloud which hold the JMeter or Taurus setup and will create load on your hosted app. These cloud instances record the app's performance and then send these reports back to BlazeMeter in real-time for your viewing pleasure.
- When using [JMeter Tests (Legacy)](skill-blazemeter-performance-testing://references/scenarios.md), the load is generated by a distributed JMeter architecture. A JMeter console is used to control the test. You need to choose the number of JMeter Engine(s) that will participate in the test.
- When using [Performance test](skill-blazemeter-performance-testing://references/scenarios.md) (Current) to execute the test with Taurus, JMeter, Gatling or other support technologies, you simply need to choose the number of engine(s) that will participate in the test.
- Each engine will simulate the number of threads/virtual users specified in the script you provide.

**Examples:**

- 20 engines and a script with 100 threads will generate 2,000 simultaneous users traffic.
- Imagine a cluster of 100 dedicated JMeter engines, all preconfigured, available in any of 51 geographical locations and ready to run 24/7 with no setup at all. No more than 5 minutes is needed to set up and run a test.

### Private Location Testing with BlazeMeter

**Target Audience:**

For developers who need to test apps behind a firewall and do not want to allow inbound connections through firewall rules, the cloud solution will not work. You need private location (or On-premise) testing.

**Prerequisites:**

- BlazeMeter Account
- Port 80 and 443 open for outgoing connections.
- Constant connectivity to the internet.
- On-premise server should run on a Linux OS that can run Docker. They must have a dual-core processor, at least 8 GB RAM, and at least 60 GB hard-disk space free. See [our private location requirements](skill-blazemeter-private-locations://references/installation.md) for the full requirements.

**Process:**

Using our private location service, no incoming requests need to be made, so do the following:

- Simply install our agent on your on-premise servers. This agent will give your servers a "heartbeat" by sending outgoing requests to BlazeMeter to check if any tests have been started, and if so, BlazeMeter will respond with instructions for these servers.
- They (your warm-blooded servers) will then create the load for your application while sending data back to BlazeMeter, so you have full access to our real-time reporting.

### Recommendations

- We recommend running up to 1,000 Threads/Virtual Users per one Engine if you are using HTTP/S protocol.
- The number of supported Threads depends on your script intensity and available resources. The more intense your script – the fewer threads a single Engine can support.
- For example, a test with 10 Engines, each running 300 threads, simulates a total of 3,000 users.

---

## Where to Find Harbor ID and Ship ID

Harbor is the legacy name for a Private Location, your on-premise environment. Ship is the legacy name for the BlazeMeter Agent, any server on which you install our agent for load generation.

**Use when**: Finding the Harbor ID (Private Location ID) or Ship ID (Agent ID) for configuration, API calls, or troubleshooting.

### Finding the IDs

The Harbor ID and Ship ID can be found in the BlazeMeter Settings -> Workspaces -> Private Locations -> **<Your Private Location>**. You will see a screen similar to the below:

**Harbor ID:** Your Private Location ID is located under **Private Location Details**, under the **Id** column (indicated by the red arrow).

**Ship ID:** Your Agent ID is located under **Agents** section, under the **Id** column (indicated by the blue arrow).

### Cloud vs Private Locations

BlazeMeter is a commercial, self-service performance testing platform-as-a-service (PaaS), which is fully compatible with open-source [Apache JMeter](https://jmeter.apache.org/) and [Taurus](https://gettaurus.org/). You can perform tests both off and on your premises.

### Cloud Testing with BlazeMeter

**Target Audience:**
This option is open to all who wish to perform load or functional testing on their website/application.

**Prerequisites:**
- BlazeMeter Account
- Application accessible outside your company firewall for testing, or ability to open the firewall to inbound traffic

**Process:**
- BlazeMeter creates instances on a public cloud using Amazon, Azure, or Google Compute Cloud which hold the JMeter or Taurus setup and will create load on your hosted app. These cloud instances record the app's performance and then send these reports back to BlazeMeter in real-time for your viewing pleasure.
- When using [JMeter Tests (Legacy)](https://help.blazemeter.com/docs/guide/performance-create-jmeter-test.html), the load is generated by a distributed JMeter architecture. A JMeter console is used to control the test. You need to choose the number of JMeter Engine(s) that will participate in the test.
- When using [Performance test](https://help.blazemeter.com/docs/guide/performance-create-test.html) (Current) to execute the test with Taurus, JMeter, Gatling or other support technologies, you simply need to choose the number of engine(s) that will participate in the test.
- Each engine will simulate the number of threads/virtual users specified in the script you provide.

**Examples:**
- 20 engines and a script with 100 threads will generate 2,000 simultaneous users traffic.
- Imagine a cluster of 100 dedicated JMeter engines, all preconfigured, available in any of 51 geographical locations and ready to run 24/7 with no setup at all. No more than 5 minutes is needed to set up and run a test.

### Private Location Testing with BlazeMeter

**Target Audience:**
For developers who need to test apps behind a firewall and do not want to allow inbound connections through firewall rules, the cloud solution will not work. You need private location (or On-premise) testing.

**Prerequisites:**
- BlazeMeter Account
- Port 80 and 443 open for outgoing connections.
- Constant connectivity to the internet.
- On-premise server should run on a Linux OS that can run Docker. They must have a dual-core processor, at least 8 GB RAM, and at least 60 GB hard-disk space free. See [our private location requirements](https://help.blazemeter.com/docs/guide/private-locations-system-requirements.html) for the full requirements.

**Process:**
Using our private location service, no incoming requests need to be made, so do the following:
- Simply install our agent on your on-premise servers. This agent will give your servers a "heartbeat" by sending outgoing requests to BlazeMeter to check if any tests have been started, and if so, BlazeMeter will respond with instructions for these servers.
- They (your warm-blooded servers) will then create the load for your application while sending data back to BlazeMeter, so you have full access to our real-time reporting.

### Recommendations

- We recommend running up to 1,000 Threads/Virtual Users per one Engine if you are using HTTP/S protocol
- The number of supported Threads depends on your script intensity and available resources. The more intense your script – the fewer threads a single Engine can support
- For example, a test with 10 Engines, each running 300 threads, simulates a total of 3,000 users

---

## Where to Find Harbor ID and Ship ID

Harbor is the legacy name for a Private Location, your on-premise environment. Ship is the legacy name for the BlazeMeter Agent, any server on which you install our agent for load generation.

**Use when**: Finding the Harbor ID (Private Location ID) or Ship ID (Agent ID) for configuration, API calls, or troubleshooting.

### Finding the IDs

The Harbor ID and Ship ID can be found in the BlazeMeter Settings -> Workspaces -> Private Locations -> **<Your Private Location>**. You will see a screen similar to the below:

**Harbor ID:** Your Private Location ID is located under **Private Location Details**, under the **Id** column (indicated by the red arrow).

**Ship ID:** Your Agent ID is located under **Agents** section, under the **Id** column (indicated by the blue arrow).

**Note**: When using [JMeter Tests (Legacy)](https://help.blazemeter.com/docs/guide/performance-create-jmeter-test.html), the load is generated by a distributed JMeter architecture. A JMeter console is used to control the test. You need to choose the number of JMeter Engine(s) that will participate in the test. When using [Performance test](https://help.blazemeter.com/docs/guide/performance-create-test.html) (Current) to execute the test with Taurus, JMeter, Gatling or other support technologies, you simply need to choose the number of engine(s) that will participate in the test. Each engine will simulate the number of threads/virtual users specified in the script you provide.

---

## Create

Create private locations in BlazeMeter, including location configuration, parallel engine runs, agent log settings, advanced configuration, and functionality selection.

**Use when**: Creating private locations in BlazeMeter or configuring location settings, parallel engine runs, agent log settings, and advanced configuration.

### Create a Private Location

A Private Location (formerly known as a harbor) is a logical container on the BlazeMeter end. A private location contains one or more agents (formerly known as ships). Private locations are servers with our agent installed on your end. You can have multiple private locations in your account; each will define a unique "location" to choose when running tests and deploying virtual services. You need to be a workspace manager to create Private Locations.

**Follow these steps:**

1. Log into your BlazeMeter account as a workspace manager.
2. Navigate to **Settings > Workspace > Private Locations**.
3. Click + to add a new private location. The **Create a private location** window opens.
4. Fill out the **Setup** section:
   - **Location name** - Give your private location a meaningful name that helps you team members choose the most appropriate location in the Location list when configuring tests.
   - **Parallel engine runs** - Enter the number of separate parallel tests each agent is allowed to run in this private location. If using Kubernetes to create agents, enter a value greater than 1.
5. (Optional) Toggle the **Agent Log**. When creating a new private location, the Agent Log is ON by default. To investigate agent failure or diagnose any agent connectivity issues, enable the agent log. You can view the logs and debug issues in real time. For more information, see [Enabling and Downloading Agent Log](https://help.blazemeter.com/docs/guide/private-locations-enable-download-agent-log.html).
6. (Optional) Toggle the Advanced slider. For more information, see [Set Up the Advanced Configuration](https://help.blazemeter.com/docs/guide/private-locations-create.html#h_01FD8GXEN0WKK7491WSRYMTA6K).
7. Click **Next**.
8. Select at least one functionality that you would like this private location to install on the agents that are added. For more information, see [Set Up the Functionalities](https://help.blazemeter.com/docs/guide/private-locations-create.html#h_90be5918-c6e8-4d3f-b221-77de81efa276).
9. Click **Create**.

You have created a Private location. The **Private Location** page opens and you can continue with the installation process for installing an agent. For more information, see the following installation procedures:
- Either [Installing a BlazeMeter Agent for Kubernetes](https://help.blazemeter.com/docs/guide/private-locations-install-blazemeter-agent-for-kubernetes.html)
- or [Installing a BlazeMeter Agent for Docker](https://help.blazemeter.com/docs/guide/private-locations-install-blazemeter-agent-for-docker.html)

Verify that you see your Private Location in your Private Locations list, which is found in the **Settings > Workspace > Private Locations** section.

### Set Up the Advanced Configuration

#### Engine Hardware Consumption

- **Override number of CPUs** This will override the default number of CPUs to the **whole number** value of CPUs you want the engines to run with (i.e. 2 for 2 CPUs).
- **Override memory (MB)** This will override the default memory use for each engine in MB (i.e. for 8 GB of memory, set the number to 8192).

By default, containers created by the agent use the Docker Memory and CPU settings. These settings override the Docker maximum settings. If you enter a value greater than the maximum Docker settings, the agent uses the maximum settings instead. This option is available to help ensure that large containers designed for performance testing or Service Virtualization can later be reduced for less demanding tests or virtual services.

#### Performance Testing Configuration

- **Users per engine** The number of virtual users that can be run on each individual test/engine.
- **JVM Parameters XMX** XMX specifies the maximum memory allocation pool for the Java Virtual Machine (JVM).
- **JVM Parameters XMS** XMS specifies the initial memory allocation pool for the Java Virtual Machine (JVM).

By default, the virtual service container will have an initial Java heap size (XMS) of 16 GB and a maximum Java heap size (XMX) of 3 GB.

- The current suggested configuration for this test type is 1 CPU and 2048 MB RAM per selected browser. For running several browsers in parallel your machine should have ~(N+ceiling[N/20]) CPUs (where N - is the number of browsers, and ceiling[N/20] is the number of Taurus engines, with 1 Taurus engine per 20 browsers). For calculating the memory please, use the formula ((N+ceiling[N/20])*2048).
- For example, if your test uses 2 browsers (Chrome and Firefox), the calculations will be the following: **CPUs**: (2+ceiling[2/20]) = 2+1 = 3 **RAM**: (2+ceiling[2/20])*2048 = (2+1)*2048 = 6144. Thus the machine should have at least **3 CPUs** and **6144 MB** of RAM.
- We recommend using SSD storage on the machine as it will speed up GUI test execution.
- For more than 8 parallel browsers, it's mandatory to have SSD storage.

### Set Up the Functionalities

- **Performance** Downloads all the images related to running Performance tests from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `taurus-cloud`, `apm-image`, `blazemeter/crane`, and `blazemeter` (Legacy JMeter users **ONLY**) images
- **API Testing** Downloads all the images related to running API Functional tests from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `taurus-cloud`, `apm-image`, and `blazemeter/crane` images. Starting February 2022, the API Functional testing feature has been deprecated. Depending on your subscription plan, you may still be able to run existing tests but can no longer create new ones. **Please use BlazeMeter API Monitoring to create and run your API Functional Tests going forward**
- **Proxy Recorder** Downloads all the images related to creating and running the proxy recorder from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `blazemeter/proxy-recorder` and `blazemeter/crane` images
- **Service Virtualization** Downloads all the images related to creating and running Service Virtualization from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `blazemeter/service-mock` and `blazemeter/crane` images
- **GUI Functional** (**Shared** run type only) Downloads all the images related to GUI Functional test from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278)). This list includes `taurus-cloud`, `apm-image`, `blazemeter/crane`, `blazemeter/charmander/firefox`, and `blazemeter/charmander/chrome`. The following options are available for the GUI Functional options:
  - **Default Firefox, Chrome, Microsoft Edge and Safari** - Installs the latest Firefox, Chrome, Microsoft Edge and Safari versions on the agent
  - **Select Version** - Gives you the choice of the currently supported Chrome, Firefox, Microsoft Edge, and Safari versions:
    - Chrome (latest 6 versions)
    - Firefox (latest 6 versions)
    - Microsoft Edge (latest 6 versions)
    - Safari (latest 6 versions)
  - **All Firefox, Chrome, Microsoft Edge and Safari** - Installs all Firefox, Chrome, Microsoft Edge and Safari versions on the agent
- **Data Orchestration** - Enables Test Data Orchestration functionality for preparing test environments
- **Delphix Integration** - Downloads all the images related to the [Delphix integration](https://help.blazemeter.com/docs/guide/integrations-integrate-with-delphix.html) from BlazeMeter (using our docker registry, [https://gcr.io/verdant-bulwark-278](https://gcr.io/verdant-bulwark-278))

---

## Use

Use and manage private locations, including agent management, status monitoring, test execution, location editing, and agent actions (edit, reset, regenerate, disable, delete).

**Use when**: Using and managing private locations or performing agent management, status monitoring, test execution, location editing, and agent actions.

### Overview

Be sure to [calibrate your test](skill-blazemeter-performance-testing://references/jmeter-configuration.md) before running full-scale tests.

You have successfully installed a private location in your workspace. The following information explains how to use your new private location.

### Manage Private Locations

Workspace managers and testers can manage private locations. To manage private location details:

1. In your BlazeMeter account, go to **Settings**, **Workspace**, **Private Locations**. You see a list of all private locations in your workspace. You can search or filter your private locations by name, and sort the list of private locations either by name, type, or date created.
2. Click a private location to see the details and a list of agents which are the on-premise servers that have the BlazeMeter agent installed.

Every private location contains the following details:

- **Enable or Disable Private Location** Enable or disable the private location using the toggle. This is useful for when you are handling maintenance on the agents in the private location and do not want users running tests on this location during that period.
- **Refresh Private Location** Clicking this button will refresh the private location page, giving you the latest status of the agents within the private location.
- **Edit Private Location** This button opens up the **Edit private location** window. The same Setup and Functionalities options from the [Create a private location](https://help.blazemeter.com/docs/guide/private-locations-create.html) dialogs are available here. Apply your changes and click the **Apply** to save. You need to be workspace manager to make changes.
- **Unshare Private Location** To unshare a Shared private location, in the **Edit private location** window, click the **Unshare location** button that appears at the bottom left-hand corner. This action is a prerequisite for deleting a Shared location. If the selected shared private location is assigned to tests configured in the associated Workspaces, the following message displays: Before you can unshare, you first need to reconfigure the tests assigned to the selected Private Location to run in alternative locations. Click **Show me a list of tests that are using this OPL**. The **Advanced Search** page opens with a list of tests that are using the selected Private Location: Click the names of the relevant tests and scroll down to **Locations**: Change the location(s) as needed. **Result:** The selected Private Location reappears on the **Private Locations** page as an Unshared Private Location.
- **Delete Private Location** The Delete location option will appear at the bottom left-hand corner of the window and will **PERMANENTLY** delete the private location after accepting the prompt. This action does not delete the installed agent. To manually delete the agent, see [Removing an Agent](https://help.blazemeter.com/docs/guide/private-locations-remove-agent.html). If the selected private location is assigned to tests configured in the selected workspaces, the following message displays: Before you can delete, you first need to reconfigure the tests assigned to the selected Private Location to run in alternative locations. Click **Show me a list of tests that are using this OPL**. The **Advanced Search** page opens with a list of tests that are using the selected Private Location: Click the name of the relevant test(s) and scroll down to **Locations**: Change the location(s) as needed.
- **Id** - The [ID of the private location](https://help.blazemeter.com/docs/guide/private-locations-where-to-find-harbor-id-and-ship-id.html) (formerly known as harbor)
- **Type** - The private location type (Shared or Unshared)
- **Engines per agent** - The number of engines/tests that can run on one agent
- **Max threads per engine** - The maximum number of users that can run per test/engine
- **Console** - JVM XMS and XMX settings for each test/engine
- **Agents** - Gives a count of all agents in the private location and a count of their statuses
- **+ Add Agent** - Used to add an agent to the private location

### View Agent Options and Details

To view agent details, follow these steps:

1. Log into your BlazeMeter account.
2. Navigate to **Settings**, **Workspace**, **Private Locations**. You should see a list of all your private locations.
3. Click a private location to see its details and a list of its agents which are the on-premise servers that have our agent installed on them.

Each agent will have the following information that you can view:

- **Name** - Name of the agent
- **Id** - [The Agent ID](https://help.blazemeter.com/docs/guide/private-locations-where-to-find-harbor-id-and-ship-id.html) (formerly known as Ship)
- **Created** - Date the agent was created
- **Address** - IP addresses of the agent
- **Status** - The status of the agent:
  - **Idle** - It looks good and is ready to be used.
  - **Running** - A test is currently using this Agent as a load engine.
  - **Error** - The Agent is not sending a heartbeat and there is probably something wrong with the server.
  - **Downloading** - The Agent is in the process of downloading and updating images used for the Private location installation.
  - **Detached** - The Agent has not sent a heartbeat in more than 3 months.
- **Last Heartbeat** - Last time a heartbeat was sent to BlazeMeter
- **Description** - Contains the details on any currently running tests or processes on this agent
- **Actions** - The actions you can use on an agent. See below for the list of actions:
  - **Edit** - Change the agent's name or IP address.
  - **Reset** - Stop any running tests on the machine and bring the agent to an Idle status. Be careful when using this as it will not stop the report if it is still showing as running.
  - **Regenerate** - Regenerate the agent. Use for re-installations. For more information, see [Installing a BlazeMeter Agent for Docker](https://help.blazemeter.com/docs/guide/private-locations-install-blazemeter-agent-for-docker.html) or [Installing a BlazeMeter Agent for Kubernetes](https://help.blazemeter.com/docs/guide/private-locations-install-blazemeter-agent-for-kubernetes.html).
  - **Disable** - Disable the ability to run tests on a specific agent. For example, you may want to do this if you have an unstable server that you'd rather not use.
  - **Delete** - Remove a specific agent from your private location as long as it is not in Running status.

### Run Private Location Tests

Follow these steps:

1. [Create a new test](https://help.blazemeter.com/docs/guide/performance-create-test.html) or go to an existing test saved in your BlazeMeter Workspace
2. In the test configuration page, you will find your private location listed under **Location(s)**

Once the test is running, you will be able to see the agent(s) that are currently running the test and information about this session in your private location settings.

Be sure to [calibrate your test](https://help.blazemeter.com/docs/guide/performance-jmeter-calibration.html) before running full-scale tests.

**Note**: When using a Private Location, you can monitor the status of agents in real-time. The agent status will show as "Running" when a test is currently using the agent as a load engine. You can view detailed information about running tests in the agent's Description field.

---

## Install Agent

Install, uninstall, and regenerate BlazeMeter on-premise agents, including Docker, Kubernetes, and Helm Chart installation options.

**Use when**: Installing, uninstalling, or regenerating BlazeMeter on-premise agents or using Docker, Kubernetes, or Helm Chart installation options.

### Agent Operations

- **Install**: Install agents using various methods
- **Uninstall**: Remove agents from infrastructure
- **Regenerate**: Regenerate agent credentials

---

## Regenerate Agent

Regenerate private location agents for Docker and Kubernetes installations when issues occur, including obtaining new commands and updating configurations. Sometimes, you will need to regenerate an agent if something goes wrong with the install.

**Use when**: Regenerating private location agents for Docker and Kubernetes installations or when issues occur and obtaining new commands and updating configurations.

### Regenerate an Agent in Docker Installation

Follow these steps:

1. Log into your BlazeMeter account
2. Navigate to **Settings**, **Workspace**, **Private Locations**
3. Click a private location to see its details and a list of its agents
4. In the **Actions** column for the agent that you want to regenerate, click **Regenerate**
5. Click **OK**
6. You will see a Docker run command, similar to the one below
7. Copy this command and save in a safe place for later. Installing the agent inside Docker requires sufficient permissions (root access required)
   - When installing an agent behind a corporate proxy, follow [these additional steps](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-agents-to-use-corporate-proxy.html)
   - When installing an agent that uses a CA certificate, follow [these additional steps](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-docker-installation-to-use-ca-bundle.html)
   - When installing an agent on a host with multiple network interfaces, follow [these additional steps](https://help.blazemeter.com/docs/guide/private-locations-configure-crane-agent-to-ensure-mock-service-deployed-is-reachable.html)
8. Remove the currently running blazemeter/crane container with the following command: `sudo docker rm -f $(sudo docker ps -q -f ancestor=blazemeter/crane)`
9. Take the Docker run command (with any extra pieces needed for a proxy and/or certificate bundle setup) and run the command with root access (use sudo). You have successfully regenerated the machine

### Regenerate an Agent in Kubernetes Installation

Follow these steps:

1. Log into your BlazeMeter account
2. Navigate to **Settings**, **Workspace**, **Private Locations**
3. Click a private location to see its details and a list of its agents
4. In the **Actions** column for the agent that you want to regenerate, click **Regenerate**
5. Click **OK**
6. You will then see a Docker run command, similar to the one below
7. Copy this command and save in a safe place for later
   - When installing an agent behind a corporate proxy, follow [these additional steps](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-agents-to-use-corporate-proxy.html)
   - When installing an agent on a host with multiple network interfaces, follow [these additional steps](https://help.blazemeter.com/docs/guide/private-locations-configure-crane-agent-to-ensure-mock-service-deployed-is-reachable.html)
8. Use one of the following to update your agent deployment file:
   - **Edit the deployment file directly**: Replace the value attached to the `AUTH_TOKEN` environment variable:
     - `kubectl get deployments` (to get the crane deployment name)
     - `kubectl edit deployment <crane deployment name>` - This will open the deployment configuration file in a `vi` window which will allow you to edit the `AUTH_TOKEN`. Once you have finished editing, you can type `:wq` to save your changes
   - **Or edit the deployment file you created for the installation**: In a text editor, replace the `AUTH_TOKEN` environment variable value with the new one and save it. Move the file to your Kubernetes instance and use the following command to apply the changes: `kubectl apply -f <filename of configuration file>`

You have successfully regenerated the machine

---

## Remove Agent

Remove private location agents from Docker and Kubernetes installations, including stopping containers, removing images, and deleting agents from BlazeMeter. This article explains how to remove an agent installation from your local machine.

**Use when**: Removing private location agents from Docker and Kubernetes installations or stopping containers, removing images, and deleting agents from BlazeMeter.

### Remove an Agent in Docker Installation

Follow these steps:

1. Log in to the machine containing the agent you want to uninstall/remove, and run the following command to list all the containers:
   ```
   $ sudo docker ps -a
   ```
   You will see a response similar to the one below:
   ```
   CONTAINER ID   IMAGE              COMMAND   CREATED       STATUS       PORTS   NAMES
   54c0b773a855   blazemeter/crane   "bash"    2 days ago    Up 2 days           blazemeter-crane
   ```

2. Remove the `bzm-crane-[<agentId>]` container with the following command:
   ```
   $ sudo docker rm -f <Container_ID>
   ```
   You need the container ID from the previous step to run this command

3. To remove all the images for the BlazeMeter install, list out all the images on the machine using the following command:
   ```
   $ sudo docker images
   ```
   You will see something like the following:
   ```
   REPOSITORY                    TAG              IMAGE ID       CREATED        SIZE
   taurus-cloud                  1.13.0-975       5df8fa4f6613   11 days ago    3.76GB
   taurus-cloud                  latest           5df8fa4f6613   11 days ago    3.76GB
   apm-image                     1.3.0-826        58c5cfab39a2   2 weeks ago    281MB
   apm-image                     latest           58c5cfab39a2   2 weeks ago    281MB
   blazemeter/crane              3.1.1-1425       7e1c470769df   5 weeks ago    700MB
   blazemeter/crane              latest           7e1c470769df   5 weeks ago    700MB
   blazemeter/proxy-recorder     1.9.0-833        cb9cdf0c1067   3 weeks ago    1.13GB
   blazemeter/proxy-recorder     latest           cb9cdf0c1067   3 weeks ago    1.13GB
   ```

4. To remove all the images, use one of the following commands:
   - **Remove all images**: `$ sudo docker rmi $(docker images -a -q)`
   - **Force delete if there are issues**: `$ sudo docker rmi -f $(docker images -a -q)`
   - **Remove only BlazeMeter images** (if you have other images on your Docker instance): `$ sudo docker rmi <Image ID of apm-image> <Image ID of blazemeter/proxy-recorder> <Image ID of taurus-cloud> <Image ID of blazemeter/crane> <Image ID of service-mock> <Image ID(s) of charmander-chrome> <Image ID(s) of charmander-firefox>`

5. Go to the Private Location containing this Agent and click **Delete**. To complete the action, click **OK**

### Remove an Agent in Kubernetes Installation

Follow these steps:

1. Log in to the Kubernetes instance where the agent is located
2. Use the following command to get the deployment name for the crane:
   ```
   kubectl get deployments
   ```
3. Use the following command to delete the deployment configuration file from your Kubernetes instance:
   ```
   kubectl delete deployment <crane deployment name>
   ```
4. Go to the Private Location containing this Agent and click **Delete**. To complete the action, click **OK**

---

## Enable Download Agent Log

Enable downloading agent logs for troubleshooting, including log access, download options, and log analysis. To investigate agent failure or diagnose any agent connectivity issues, enable the agent log. You can view the logs and debug issues in real time.

**Use when**: Enabling downloading agent logs for troubleshooting or accessing logs, downloading logs, and analyzing log data.

### Agent Log when Creating a New Private Location

When you create a new private location, the Agent Log is **ON** by default. For more information, see [Creating a Private Location](skill-blazemeter-private-locations://references/management.md).

For any of your existing private locations, the Agent Log is **OFF** by default.

### Enable the Agent Log for an Existing Private Location

Follow these steps:

1. Navigate to **Settings**, **Workspace**, **Private Locations**
2. Click the name of your existing location to open the details page
3. Click the **Edit** icon
4. The Agent log is off by default. To enable the Agent log, toggle the slider ON. This will enable the Agent log for any new agents that you add to this Private location
5. (Optional) If you want to enable the Agent log to your existing agents, check the box for **Also apply Agent log writing state to X existing Agents**. The checkbox refers to the number of existing agents within that private location
6. Click **Apply**

### Enable the Agent Log per Agent

You can allow the agent log for specific agents.

Follow these steps:

1. Navigate to **Settings**, **Workspace**, **Private Locations**
2. Click the name of your existing location to open the details page
3. In the **Actions** column, click the **Agent log** icon for the agent that you want to enable the log for. An Agent log section opens at the bottom
4. Toggle the **Agent Log writing is enabled** slider to ON

### Download the Agent Log

You can download the agent log file for up to last two weeks.

Follow these steps:

1. Navigate to **Settings**, **Workspace**, **Private Locations**
2. Click the name of your existing location to open the details page
3. In the agents section, click the **Actions** button. An Agent log section opens at the bottom. The **Agent Log writing is enabled** slider should be ON. For more information, see [Enable the Agent Log per Agent](#enable-the-agent-log-per-agent) in this article
4. Click **Downloads**
5. Select the time range for the Agent log. The logs file for the agent is generated and ready for download. The file will be available for 24 hours. An error message is displayed if no logs are available. In this case, select a different time range. If file size limit is exceeded, consider downloading in steps
6. Click **Download**

---

## Manage Private Locations (Account Admin)

Manage private locations across workspaces as an account admin, including sharing, unsharing, and deleting private locations, with validation for tests using those locations. As an Account Admin, you can manage all the Private Locations in your BlazeMeter account. Viewing all your Private Locations in one place allows you to optimize the use of your resources, by sharing and unsharing Private Locations across Workspaces. Additionally, you can permanently delete Private Locations within your account.

**Use when**: Managing private locations across workspaces as an account admin or sharing, unsharing, and deleting private locations with validation for tests using those locations.

### Access Account-Level Private Location Management

Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. To view the details of private locations in your account, navigate to **Settings > Account > Locations Manager > Private Locations**.

### Share Private Locations

To share a Private Location with other workspaces within your account, follow these steps:

1. Log into your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account > Locations Manager**. A list of all Private Locations in your account appears. You can search and filter Private Locations by name
4. Select a Private Location, then click the share icon. A list of available workspaces displays
5. Select one or more workspaces, then click **Share with (n) Workspaces** (where n = number of workspaces selected)

All the existing shared Workspaces will be marked in the table as Shared. In addition, the calculation of n includes all Workspaces that will be shared. If a Workspace is already shared, it cannot be selected but it will be included in the total number of shared workspaces (n).

**Result:** The selected workspaces are added to the selected Private Location on the **Private Locations** page.

### Unshare Private Locations

To unshare a Private Location from Workspaces, follow these steps:

1. Log into your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account > Private Locations**. A list of all Private Locations in your account appears. You can search or filter Private Locations by name. By default, the **Private Location** page displays up to five Workspace names in a private location table row. If more than five Workspaces are shared with a Private Location, a link appears on the right indicating the number of shared workspaces that are hidden (not shown)
4. To unshare, do one of the following:
   - Click the X icon next to a Workspace name
   - Click either an **(n) more** link (where n = number of hidden workspaces) or an **Unshare** button. A list of all the shared Workspaces displays. Select one or more Workspaces, then click **Remove share from (n) Workspaces** (where n = number of workspaces selected)

If the selected private locations are assigned to tests configured in one or more of the selected Workspaces, the following message displays:

*Before you can unshare, you first need to reconfigure the tests assigned to the selected Private Location to run in alternative locations.*

To do that, follow these steps:

1. Click **Show me a list of tests that are using this Private Location**. The **Advanced Search** page opens with a list of tests that are using the selected Private Location
2. Click the name of the relevant test(s) and scroll down to **Locations**
3. Change the location(s) as needed
4. Return to the Private Location page and repeat step 3

**Result:** The selected workspaces are unshared from the selected Private Location on the **Private Locations** page.

### Delete Private Locations

You can delete Private Locations whether they are shared or unshared.

To delete a private location, follow these steps:

1. Log into your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account > Private Locations**. A list of all Private Locations in your account appears. You can search or filter private locations by name
4. Select a private location row
5. Click the trash can icon on the right of the selected private location row. A popup displays
6. Click **Delete**. The selected private location is permanently deleted

If the selected private locations are assigned to tests configured in the selected workspaces, the following message displays:

*Before you can delete, you first need to reconfigure the tests assigned to the selected Private Location to run in alternative locations.*

1. Click **Show me a list of tests that are using this Private Location**. The **Advanced Search** page opens with a list of tests that are using the selected Private Location
2. Click the name of the relevant test(s) and scroll down to **Locations**
3. Change the location(s) as needed
4. Return to the Private Location page and click Delete

**Important:** This action *does not* delete an installed agent. To manually delete an agent, see [Removing an Agent](skill-blazemeter-private-locations://references/management.md).

---

## Documentation References

For detailed information about Private Location management, use the BlazeMeter MCP help tools:

**Cloud vs Private Location**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `private-locations-vs-cloud`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["private-locations-vs-cloud"]}`

**Management**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `private-locations-vs-cloud` (cloud vs private location)
  - `private-locations-create` (create)
  - `private-locations-use` (use, includes unshare/delete for workspace managers)
  - `administration-manage-private-locations` (share/unshare/delete for account admins)
  - `private-locations-install-agent` (install agent)
  - `private-locations-regenerate-agent` (regenerate)
  - `private-locations-remove-agent` (remove)
  - `private-locations-enable-download-agent-log` (download logs)
  - `private-locations-where-to-find-agent-logs` (find logs)
  - `private-locations-where-to-find-harbor-id-and-ship-id` (Harbor/Ship ID)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["private-locations-vs-cloud", "private-locations-create", "private-locations-use", "administration-manage-private-locations", "private-locations-install-agent", "private-locations-regenerate-agent", "private-locations-remove-agent", "private-locations-enable-download-agent-log", "private-locations-where-to-find-agent-logs", "private-locations-where-to-find-harbor-id-and-ship-id"]}`

**Installation**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `private-locations-install-agent` (installing the agent)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["private-locations-install-agent"]}`

