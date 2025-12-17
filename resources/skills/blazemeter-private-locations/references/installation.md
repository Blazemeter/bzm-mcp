# Installation

## Installing the Agent

Install, uninstall, and regenerate BlazeMeter's on-premise agent on your server/instance behind your firewall.

**Use when**: Installing, uninstalling, or regenerating BlazeMeter's on-premise agent on your server/instance behind your firewall.

### Overview

First, make sure your server/instance meets the minimum requirements as described in [Private Location System Requirements](skill-blazemeter-private-locations://references/installation.md).

Continue with one of the following options:
- [Installing a BlazeMeter Agent for Docker](skill-blazemeter-private-locations://references/installation.md)
- [Installing a BlazeMeter Agent for Kubernetes](skill-blazemeter-private-locations://references/installation.md)
- [Installing a BlazeMeter Agent using Helm Charts](skill-blazemeter-private-locations://references/installation.md)

---

## Install Agent for Docker

Install BlazeMeter agents for Docker installations, including pulling images, configuring containers, and setting up Docker-based private locations.

**Use when**: Installing BlazeMeter agents for Docker installations or setting up Docker-based private locations.

### Installation Steps

**Prerequisites:** Before proceeding with installation, ensure that your server/instance meets the minimum requirements. For more information, see [Private Location System Requirements](skill-blazemeter-private-locations://references/installation.md).

1. Log into your BlazeMeter account and click Settings in the top right corner.
2. Go to **Workspaces**, **Private Locations** and choose the Private Location where you want to create the Agent.
3. Click **Add agent**.
4. Enter a new agent name that helps your team members recognize what to use this location for.
5. (Optional) Enter the IP address of the machine.
6. Click **Create Agent**.
7. BlazeMeter generates a Docker installation command in the **Docker Command** tab.
8. Copy the command, add environment variables as per details of your Docker instance, then run the updated command on your private engine. For more information, see [BlazeMeter Agent Environment Variables](https://help.blazemeter.com/docs/guide/private-locations-blazemeter-agent-environment-variables.html). Installing the agent inside Docker requires sufficient permissions (root access required). When [using Docker for Mac 4.3.0](https://github.com/docker/for-mac/issues/6073) or above, add the following parameter to the command: `--privileged -v /sys/fs/cgroup:/sys/fs/cgroup:rw`. When installing an agent behind a corporate proxy, follow [these additional steps](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-agents-to-use-corporate-proxy.html). When installing an agent that uses a CA certificate, follow [these additional steps.](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-docker-installation-to-use-ca-bundle.html) When installing an agent on a host with multiple network interfaces, follow [these additional steps.](https://help.blazemeter.com/docs/guide/private-locations-configure-crane-agent-to-ensure-mock-service-deployed-is-reachable.html) If your application requires a custom certificate to be able to communicate over HTTPS, see [Optional Installation Step: Bring Your Own Certificate – Service Virtualization.](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-bring-your-own-certificate-mock-services.html#h_d92217cb-0390-4982-8546-eca1efdc4c05)

After the command has finished running, a container is created (called **bzm-crane-<agentId>**) and the images required for the installation begin to [download](https://help.blazemeter.com/docs/guide/private-locations-create.html#h_90be5918-c6e8-4d3f-b221-77de81efa276). Downloads can take up to 30 minutes (depending on the network speed on the machine). During this time, the new agent is listed in the **Private Location** section, and it indicates its status as '**Downloading**'.

After the download has finished, the agent indicates to be in an '**Idle**' status and is available for use. For more information about how to use your new private location, see [Using Private Locations](https://help.blazemeter.com/docs/guide/private-locations-use.html).

**Important**: When using Docker for Mac 4.3.0 or above, add the following parameter to the command: `--privileged -v /sys/fs/cgroup:/sys/fs/cgroup:rw`. Installing the agent inside Docker requires sufficient permissions (root access required).

To check the downloaded docker images, use the following command:
```
$ sudo docker images
```

You should see something similar to the following depending on what functionalities you selected (both tags **MUST** be present for proper functionality) when creating the private location:

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
blazemeter/service-mock       0.2.4-11         df8d54721102   3 days ago     165MB
blazemeter/service-mock       latest           df8d54721102   3 days ago     165MB
blazemeter/charmander/firefox_65.0.2  2.1.0-266  681cf263e9d1  8 hours ago   1.45GB
blazemeter/charmander/firefox_65.0.2  latest     681cf263e9d1  8 hours ago   1.45GB
blazemeter/charmander/chrome_69.0.3497.92  2.1.0-266  89fb01cb9950  8 hours ago  1.47GB
blazemeter/charmander/chrome_69.0.3497.92  latest     89fb01cb9950  8 hours ago  1.47GB
```

---

## Install Agent for Kubernetes

Install BlazeMeter agents for Kubernetes installations, including deployment configuration, RBAC setup, and Kubernetes-based private locations.

**Use when**: Installing BlazeMeter agents for Kubernetes installations or setting up Kubernetes-based private locations.

### Installation Steps

You want to install a BlazeMeter on-premise agent for Kubernetes on a server/instance behind your firewall. BlazeMeter supports the two Ingress controllers for Kubernetes: Contour and Istio. The same installation instructions apply for a variety of Kubernetes clusters, for example, EKS, GKE, AKS.

When adding an on-premise agent for a [Private Location](https://help.blazemeter.com/docs/guide/private-locations-create.html), you will come across commands for Docker and Kubernetes installations, which you copy and run on your machine to install the agent. Ensure that you update all [environment variables](https://help.blazemeter.com/docs/guide/private-locations-blazemeter-agent-environment-variables.html) according to your Kubernetes instance.

### Contour Configuration

BlazeMeter provides two methods for installing a Kubernetes agent with Contour:
- **Automatic**: Involves copying a BlazeMeter auto-generated command, then replacing environment variables with your own, and possibly adding new ones. This is a straightforward method recommended for most use cases.
- **Manual**: Involves creating separate YAML files, filling them with your environment variables, and executing them individually. This method is recommended for special use cases, for example, if you need to use CA certificates with your agent.

### Install Kubernetes Agent (Automatic)

The following steps walk you through the **automatic** method. For the manual method, see [Optional Installation Step: Manual Kubernetes Agent Installation](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-manual-kubernetes-agent-installation.html).

**Follow these steps:**

1. Verify that your server/instance [meets the minimum requirements](skill-blazemeter-private-locations://references/installation.md)
2. Log into your BlazeMeter account and click **Settings** in the top right corner.
3. To choose to the Private Location where you want to create the Agent, go to **Workspaces**, **Private Locations**.
4. For our Kubernetes implementation, ensure that your Private Location support a *Shared* Run Type instead of *Dedicated*. See [Creating a Private Location](https://help.blazemeter.com/docs/guide/private-locations-create.html) for details.
5. Click **Add agent**.
6. Enter the agent name.
7. (Optional) Enter the IP address of the machine.
8. Click **Create Agent**. A Kubernetes installation command and configuration is generated on the **Kubernetes Configuration** tab.
9. Copy the command, then update and/or add to the environment variables as per details of your Kubernetes instance. For details, see the following section [Using the Kubernetes Auto-Generated Command](https://help.blazemeter.com/docs/guide/private-locations-install-blazemeter-agent-for-kubernetes.html#h_01EY6NN2BBNQPHTRBKEKMP6GD4), and also the article [BlazeMeter Agent Environment Variables](https://help.blazemeter.com/docs/guide/private-locations-blazemeter-agent-environment-variables.html). When installing an agent behind a corporate proxy, follow [these additional steps](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-configure-agents-to-use-corporate-proxy.html). When installing an agent on a host with multiple network interfaces, follow [these additional steps.](https://help.blazemeter.com/docs/guide/private-locations-configure-crane-agent-to-ensure-mock-service-deployed-is-reachable.html) If your application requires a custom certificate to be able to communicate over HTTPS, see [Optional Installation Step: Bring Your Own Certificate – Service Virtualization](https://help.blazemeter.com/docs/guide/private-locations-optional-installation-step-bring-your-own-certificate-mock-services.html#h_d92217cb-0390-4982-8546-eca1efdc4c05).
10. Run the updated command on your private engine.
11. Use the following command to check on the status of the pod launch for the crane deployment: `kubectl get pods`
12. After the Kubernetes pod shows as 'Running', the agent indicates to be in an '**Idle**' status and is available for use. For more information what you can do with your new private location, see [Using Private Locations](https://help.blazemeter.com/docs/guide/private-locations-use.html).

### Using the Kubernetes Auto-Generated Command (Manual)

When adding an on-premise agent for a [Private Location](https://help.blazemeter.com/docs/guide/private-locations-create.html), you will come across commands for Docker and Kubernetes installations, which you copy and run on your machine to install the agent.

The Kubernetes auto-generated command allows you to consolidate all configuration and deployment variables for a simpler execution.

**Prerequisites for using the auto-generated command**

- Verify that you have a cluster admin access to execute the command.
- Replace all instances of `namespace` with your assigned namespace. For best practices for a namespace, see the [Kubernetes documentation](https://kubernetes.io/docs/tasks/administer-cluster/namespaces-walkthrough/). Use the following yaml to create a namespace if required:
  ```yaml
  apiVersion: v1
  kind: Namespace
  metadata:
    name: BLAZEMETER
  ```
- You can also add and replace other environment variables as required by your instance. See the complete list of [BlazeMeter Agent Environment Variables](https://help.blazemeter.com/docs/guide/private-locations-blazemeter-agent-environment-variables.html) for details.

The auto-generated command includes:
- Role and RoleBinding for RBAC
- ClusterRole and ClusterRoleBinding
- Deployment configuration with environment variables
- Optional Contour access configuration (commented out)

---

## Install Agent for Kubernetes for Mock Services

Install BlazeMeter agents for Kubernetes specifically for Service Virtualization, including Istio setup, gateway configuration, secret creation, agent deployment, and DNS configuration. This article details how to install a BlazeMeter on-premise agent for Kubernetes on a server/instance behind your firewall with the goal of running Service Virtualization. BlazeMeter supports Contour as well as Istio for defining Ingress traffic. The procedure described here relies on Istio.

Service Virtualization is a use case where the Private Location needs an outbound and an inbound connection, while Private Locations for other test types need only an outbound connection. Service Virtualization uses either Istio or Contour to help route Ingress traffic into the desired pod in containers and the cluster. With Istio, you can also use the same Private Location for both Service Virtualization and Performance tests.

**Use when**: Installing BlazeMeter agent for Kubernetes specifically for Service Virtualization or setting up Istio, gateway configuration, secret creation, agent deployment, and DNS configuration.

### Istio Overview

Virtual services can use Istio to help route Ingress traffic into the desired pod in containers and the cluster.

**Gateway**: The Gateway serves as a load balancer configuration and as an entry point into your cluster. In the gateway, you can define ports that you want to expose and you can list different hosts (domain names) that each of the ports should handle.

**Virtual Services**: Istio handles traffic through the gateway. You can create resources called virtual services that serve as a bridge between the gateway and the actual services that are running on your Kubernetes cluster. For incoming traffic that is targeting a given host name (example: `mydomain1-9090-<YOURNAMESPACE>.mocks.yoursite.com`), a virtual service forwards traffic to a specific service which then forwards it to the pod and the containers within your cluster.

**Sidecar Injection**: Additionally, for any pod that you create in your cluster, Istio will inject a container that helps enforce mutual TLS traffic for anything that is going in and out of your pods.

### Set Up Istio

Follow these steps:

1. Download the binary by executing the following shell script:
   ```bash
   curl -L https://istio.io/downloadIstio | sh -
   ```
2. Ensure that the cluster is clean. Run the following command:
   ```bash
   kubectl get all
   ```
3. Delete the **projectcontour** namespace if it is present. Run the following command:
   ```bash
   kubectl delete ns projectcontour
   ```
4. Install and set up a profile. Run the following command:
   ```bash
   ./istioctl install --set profile=demo -y
   ```
5. Enable the istio-injection for the namespace. In this example we are running on the `<YOURNAMESPACE>` namespace. Run the following command:
   ```bash
   kubectl label namespace <YOURNAMESPACE> istio-injection=enabled
   ```

### Create a Secret

Follow these steps:

1. Generate a wildcard cert using openssl:
   ```bash
   openssl genrsa -out mydomain.local.key 2048
   openssl req -new -key mydomain.local.key -out mydomain.local.csr
   openssl x509 -req -days 3650 -in mydomain.local.csr -signkey mydomain.local.key -out mydomain.local.crt
   rm mydomain.local.csr
   ```
2. Create a secret in the `istio-system` namespace called `wildcard-credential`:
   ```bash
   kubectl create -n istio-system secret tls wildcard-credential --key=mydomain.local.key --cert=mydomain.local.crt
   ```

### Deploy the Gateway

Here is a sample of the gateway file contents. To set the istio selector in the spec, make sure it matches your ingress gateway pod labels. If you installed Istio using Helm following the standard documentation, this would be `istio:ingress`. Replace `<YOURNAMESPACE>` by your namespace.

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: bzm-gateway
  namespace: <YOURNAMESPACE>
spec:
  selector:
    istio: ingressgateway # Set this to your istio default controller!
  servers:
  - port:
      number: 80
      name: http-80
      protocol: HTTP
    hosts:
    - "*"
  - port:
      number: 443
      name: https-443
      protocol: HTTPS
    hosts:
    - "*"
    tls:
      mode: SIMPLE
      # This must be located in the "istio-system" namespace
      credentialName: wildcard-credential
  - port:
      number: 15443
      name: https-15443
      protocol: HTTPS
    hosts:
    - "*"
    tls:
      mode: PASSTHROUGH
```

Run the following command to deploy the gateway:
```bash
kubectl apply -f <path to yaml>/bzm_gateway.yaml -n <YOURNAMESPACE>
```

### Deploy an Agent

Follow these steps:

1. Create an agent in the BlazeMeter Private Location section and copy the Kubernetes configuration
2. Copy the Kubernetes Configuration agent creation command and update it or add the following:
   - Enter the namespace where you want to deploy crane, in this example, `<YOURNAMESPACE>`
   - Update imagePullPolicy value: `imagePullPolicy: Always`
   - Add the below properties under spec of kind Deployment:
     - `KUBERNETES_WEB_EXPOSE_TYPE: ISTIO`
     - `KUBERNETES_WEB_EXPOSE_SUB_DOMAIN: mydomain.local`
     - `KUBERNETES_WEB_EXPOSE_TLS_SECRET_NAME: wildcard-credential`
     - `KUBERNETES_SERVICE_USE_TYPE: CLUSTERIP`
     - `KUBERNETES_USE_PRE_PULLING: 'true'`
     - `KUBERNETES_SERVICES_BLOCKING_GET: 'true'`
     - `KUBERNETES_ISTIO_GATEWAY_NAME: bzm-gateway` (optional)
   - Add `"networking.istio.io"` as part of the roles.rules.apiGroups
   - Add `"ingresses", "gateways", "virtualservices"` as part of roles.rules.resources

3. Apply the manifest to deploy this agent:
   ```bash
   kubectl apply -f deployment-crane.yaml -n <YOURNAMESPACE>
   ```
4. Verify the pods and other resources within your cluster namespace to ensure that the agent is running:
   ```bash
   kubectl get all -n <YOURNAMESPACE>
   ```
5. Verify the resources within the istio-system namespace:
   ```bash
   kubectl get svc -n istio-system
   kubectl get secret -n istio-system
   ```
   Make sure we have the loadbalancer service running with an active external IP. Verify that the secret named wildcard-credential is set up.
6. To verify Istio deployments within your active namespace, run the following command:
   ```bash
   kubectl get gw -n <YOURNAMESPACE>
   ```
   Verify that the bzm-gateway is deployed within your namespace (same namespace as that of crane)

After all resources within your cluster are set up, you can start deploying virtual services.

### Deploy an HTTP or HTTPS based Virtual Service

The virtual service creates an Istio virtual service in the namespace. You can verify the virtual service in your namespace by using the following command:
```bash
kubectl get virtualservices -n <YOURNAMESPACE>
```

**Note**: Stopping or deleting a virtual service deletes the Istio virtual service.

1. Navigate to the **Virtual Service** tab in the BlazeMeter UI
2. Create a virtual service with a set of transactions, and select the Kubernetes private location agent (the agent we created with this configuration) in the Private Location
3. After the virtual service is created, click on the save and start button to run the virtual service
4. The endpoint should be visible in the UI with the FQDN ending the subdomain. In this example, it is: "Mydomain.local"
5. The format of your virtual service endpoint should look like this: `mockserviceName&ID.namespaceName.mydomain.local`

### Configure the DNS

If you cannot connect to the virtual service endpoint, it is likely due to failing DNS resolution. The DNS resolution for the generated virtual services URLs/endpoint is not anything that Service Virtualization or Crane can set up automatically.

The missing piece is that the systems from which you are running HTTP/S requests don't have any DNS records that map traffic of the generated subdomains. You resolve this issue by adding the DNS entry of the external IP of the loadbalancer to the hosts file of the system which is used for hitting the virtual service endpoint.

For example, let's say the generated URL is `mockservice232297-8080-<YOURNAMESPACE>.mydomain.local` and the external IP of the loadbalancer is `34.72.180.232`, then add the following to your `/etc/hosts` file:
```
34.72.180.232 mockservice232297-8080-<YOURNAMESPACE>.mydomain.local
```

You can now reach the virtual service endpoint at `mockservice232297-8080-<YOURNAMESPACE>.mydomain.local`

Now that you have an Agent installed, continue reading how you [use your new Private Location](skill-blazemeter-private-locations://references/management.md).

---

## Install Agent Helm Chart

Install BlazeMeter agents using Helm Chart, including chart installation, configuration, and Helm-based deployment. This article shows you how to deploy a BlazeMeter Private Location to your Kubernetes cluster using Helm, the package manager for Kubernetes. This procedure uses a Helm chart which enables you to make advanced configurations to your BlazeMeter Private Location deployment.

**Use when**: Installing BlazeMeter agents using Helm Chart or setting up Helm-based deployment.

### Prerequisites

- A BlazeMeter account
- A Kubernetes cluster. The same installation instructions apply for a variety of clusters, for example, EKS, GKE, AKS
- Latest [Helm](https://helm.sh/) installed
- Before proceeding with the installation, ensure that your Kubernetes cluster meets the minimum requirements. For more information, see [Private Location System Requirements](skill-blazemeter-private-locations://references/installation.md)

### Obtain Location ID, Agent ID, and Auth Token from BlazeMeter

For this installation, identify your Private Location ID (formerly Harbour_ID), BlazeMeter Agent ID (formerly Ship_ID), and your BlazeMeter API Auth_token, and store them in a text file in a safe location.

**Get through BlazeMeter web UI:**

1. Log in to BlazeMeter with Workspace Admin permissions
2. [Create a Private Location](skill-blazemeter-private-locations://references/management.md)
3. After the Private Location has been created in BlazeMeter, copy the Private Location ID
4. Start following the procedure how to [Create an Agent](skill-blazemeter-private-locations://references/installation.md). Give the agent a name. (Optional) Enter the IP address of the agent. Click **Create**. Go to the **Helm chart** tab. *Do not run* any generated dock command. Instead, copy the following values into a text file:
   - HARBOR_ID — your Private Location ID
   - SHIP_ID — your Agent ID
   - AUTH_TOKEN — your API authentication token

**Get through BlazeMeter API:**

1. Create a Private Location using an [API call](https://api.blazemeter.com/performance/#create-a-private-location)
2. Copy the Private Location ID (Harbour ID) from the response
3. Create an Agent using [an API call](https://help.blazemeter.com/apidocs/performance/private_locations_create_an_agent.htm)
4. Copy the Agent ID (Ship_ID) from the response
5. Generate the docker command using [an API call](https://help.blazemeter.com/apidocs/performance/private_locations_docker_command.htm)
6. Copy the Auth_token from the response

*Do not run* the generated command.

### Download the Helm Chart

1. [Download the latest Helm chart](https://github.com/Blazemeter/helm-crane/releases/) TAR file from the GitHub repository
2. Unpack the chart with the given *version* using the following command:
   ```bash
   tar -xvf helm-crane-*version*.tgz
   ```

### Configure the Helm Chart Values

The `values.yaml` file contains the default values for your chart. Customize it now for your requirements.

**Setting up the minimum required:**

Before installing the chart, provide your BlazeMeter harbour_id, ship_id, and authtoken in the values.yaml file. These values are required for the Crane deployment to register and authenticate with BlazeMeter.

1. Open the `values.yaml` file in a text editor of your choice
2. Add your Location ID, Agent ID, and Auth Token, in quotation marks, to the `env:` section, using the following format:
   ```yaml
   env:
     authtoken: "*your BlazeMeter API Auth token*"
     harbour_id: "*your Private Location ID*"
     ship_id: "*your Agent ID*"
   ```
3. Replace the example values above with your actual credentials

**Using Kubernetes Secrets or External Secret Managers:**

To keep your Crane credentials secure and not store them directly in the values.yaml file, use one of the following integrations:
- SecretProviderClass (CSI Driver)
- ExternalSecrets Operator

When you enable either of these integrations, the `env.authtoken, env.harbour_id` and `env.ship_id` values in `values.yaml` are ignored, and the credentials are sourced from your external secret store.

**Configure optional settings:**

The Helm chart supports many optional configurations including:
- Proxy configuration
- CA certificates
- Grid Proxy configuration
- Non-privilege container deployment
- Service Virtualization support
- Custom labels
- Tolerations
- Node selectors
- Resource limits and requests
- Pod Disruption Budget
- SecretProviderClass
- ExternalSecrets Operator

For detailed configuration options, see the [Helm Chart documentation](https://help.blazemeter.com/docs/guide/private-locations-install-blazemeter-agent-helm-chart.html).

### Verify the Helm Chart

After you have configured the values, run the following command to verify if the values are correctly used in the Helm chart:
```bash
helm lint <path-to-chart>
helm template <path-to-chart>
```

The command prints the template that Helm will use to install this chart. Check the values and if something is missing, edit the values.yaml file again according to your requirements.

### Install the Helm Chart

To install the BlazeMeter Agent through the Helm chart, use the following command:
```bash
helm install crane /path/to/chart --namespace <your-namepace-name>
```

### Verify Helm Chart Installation

After installing the chart, you can verify both the deployment and the underlying Kubernetes infrastructure using Helm's built-in test hooks. This chart includes a test pod that checks for essential connectivity and configuration, ensuring your environment is ready for BlazeMeter workloads.

**Run the Helm test:**
```bash
helm test <release-name> -n <namespace>
```

Replace `<release-name>` with the name you used for your Helm release (e.g., crane). Replace `<namespace>` with the namespace where you installed the chart.

**What does the test do?**

The test pod will:
- Validate that the Cluster resources are suitable to run Crane and child deployment
- Check for required roles and mappings
- Verify network connectivity and DNS resolution from within the cluster
- Validate if the required kubernetes resources are deployed to support crane and its functionalities

**Interpreting validation results:**

- **Success**: If the test passes, your chart and infrastructure are ready
- **Failure**: If the test fails, review the logs for details. Common issues include missing secrets, network restrictions, or misconfigured values or specs. Address any reported issues and re-run the test

You can add the `--logs` flag to helm test to automatically print the test pod logs:
```bash
helm test <release-name> --logs
```

### Upgrade an Existing Helm Chart

To upgrade your existing Helm release to a new version of the chart, use the helm upgrade command:
```bash
helm upgrade <release-name> /path/to/newchart -n <namespace>
```

If you have a custom values.yaml file, specify it with the -f flag:
```bash
helm upgrade <release-name> /path/to/newchart -n <namespace> -f /path/to/values.yaml
```

Before upgrading, preview the changes using the helm-diff plugin:
```bash
helm diff upgrade <release-name> /path/to/newchart -n <namespace> -f /path/to/values.yaml
```

### Uninstall the Helm Chart

To uninstall the Helm chart, run:
```bash
helm uninstall <release-name> -n <your-namepace-name>
```

---

## System Requirements

Understand system requirements for Private Location installations, including OS versions, hardware, software, and network requirements for Docker and Kubernetes.

**Use when**: Understanding system requirements for Private Location installations or planning Docker and Kubernetes deployments.

### Requirements

- **OS Versions**: Supported operating system versions
- **Hardware**: Minimum hardware requirements
- **Software**: Required software dependencies
- **Network**: Network connectivity requirements

---

## Manual Kubernetes Agent Installation

Perform manual Kubernetes agent installation for Private Locations, including YAML file creation, RBAC configuration, and deployment setup.

**Use when**: Performing manual Kubernetes agent installation for Private Locations or customizing YAML files, RBAC configuration, and deployment setup.

### Manual Installation

1. **YAML Files**: Create Kubernetes YAML files
2. **RBAC Configuration**: Set up RBAC resources
3. **Deployment Setup**: Configure deployment
4. **Apply Configuration**: Apply YAML files to cluster

---

## Upgrade from Legacy Supervisor Ship

Upgrade from legacy BlazeMeter Supervisor agents to new Dockerized agents, including uninstallation and installation procedures.

**Use when**: Upgrading from legacy BlazeMeter Supervisor agents to new Dockerized agents or performing uninstallation and installation procedures.

### Upgrade Process

1. **Uninstall Legacy**: Remove legacy Supervisor agents
2. **Install New**: Install Dockerized agents
3. **Migrate Configuration**: Migrate configuration settings
4. **Verify Upgrade**: Verify successful upgrade

---

## Documentation References

For detailed information about Private Location installation, use the BlazeMeter MCP help tools:

**Installation**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `private-locations-install-blazemeter-agent-for-docker` (Docker)
  - `private-locations-install-blazemeter-agent-for-kubernetes` (Kubernetes)
  - `private-locations-install-blazemeter-agent-for-kubernetes-for-mock-services` (Kubernetes Mock Services)
  - `private-locations-install-blazemeter-agent-helm-chart` (Helm Chart)
  - `private-locations-system-requirements` (system requirements)
  - `private-locations-optional-installation-step-manual-kubernetes-agent-installation` (manual Kubernetes)
  - `private-locations-upgrade-from-legacy-blazemeter-supervisor-ship-to-new-dockerized-agent` (upgrade from legacy)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["private-locations-install-blazemeter-agent-for-docker", "private-locations-install-blazemeter-agent-for-kubernetes", "private-locations-install-blazemeter-agent-for-kubernetes-for-mock-services", "private-locations-install-blazemeter-agent-helm-chart", "private-locations-system-requirements", "private-locations-optional-installation-step-manual-kubernetes-agent-installation", "private-locations-upgrade-from-legacy-blazemeter-supervisor-ship-to-new-dockerized-agent"]}`

