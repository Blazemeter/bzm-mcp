# Configuration

## Environment Variables

Configure environment variables for private location agents, including agent settings, proxy configuration, and custom parameters.

**Use when**: Configuring environment variables for private location agents or setting up agent settings, proxy configuration, and custom parameters.

### Overview

This section contains a full list of supported environment variables for your Docker and Kubernetes agent installations.

Default environment variables are included and prefilled in the auto-generated command created when you add an agent for your private location. For Docker agent installation, the command can be used as is. For Kubernetes agent installation, you'll need to replace and update some of the variables with your own configuration.

Optional environment variables enable you to further configure your instance for specific use cases, for example, when your private location is hidden behind a corporate proxy, or if you want to use CA certificates for agent installation.

### Docker Environment Variables

Key environment variables include:

- **AUTH_TOKEN** (String) - The agent auth token
- **AUTO_UPDATE** (Boolean) - Whether new (Dockerized) auto-updates should be enabled. Default: true
- **AWS_CA_BUNDLE** (String) - This value is always /etc/ssl/certs/ca-certificates.crt. Denotes the location of the certificate bundle
- **CONTAINER_MANAGER_TYPE** (String) - Valid values: DOCKER, KUBERNETES. Default: DOCKER
- **DOCKER_REGISTRY** (String) - The address of your private Docker registry. For example: localhost:5000
- **DOCKER_REGISTRY_EMAIL** (String) - The user name of your private Docker registry
- **DOCKER_REGISTRY_PASSWORD** (String) - The password of your private Docker registry
- **DOCKER_REGISTRY_USERNAME** (String) - The user name of your private Docker registry
- **DODUO_PORT** (String) - The user-defined port where to run Doduo (BlazeMeter Grid Proxy). By default, Doduo listens on port 8000
- **HARBOR_ID** (String) - The ID of the private location with which the agent is associated
- **HOSTNAME_OVERRIDE** (String) - The hostname you are going to use for transactional virtual services created on the agent
- **HTTPS_PROXY** (String) - URL of HTTPS proxy server to be used for all HTTPS requests sent by agent to a.blazemeter.com. Also passed to the other components
- **HTTP_PROXY** (String) - URL of the HTTP proxy server to be used for all HTTP requests sent by the agent to a.blazemeter.com. Also passed to other components
- **INHERIT_RUNNING_USER_AND_GROUP** (Boolean) - If true, it indicates that containers launched should use the same UID:GID as the Crane itself. Default: false
- **NO_PROXY** (String) - URL that should be excluded from proxying (on servers that should be contacted directly)
- **PREFERRED_INTERFACE** (String) - Uses a specific network interface to gather the machine's IP address. If the interface is unavailable, it falls back to use the first available interface (not in the denylist, see default). Default: none; Uses first interface available not in list: docker0, lo
- **REQUESTS_CA_BUNDLE** (String) - This value is always /etc/ssl/certs/ca-certificates.crt. Denotes the location of the certificate bundle
- **SHIP_ID** (String) - The ID of the Agent
- **TLS_CERT** (String) - The public certificate for the domain used in HOSTNAME_OVERRIDE
- **TLS_CERT_GRID** (String) - The public certificate for the domain used to run the BlazeMeter Grid proxy over HTTPS
- **TLS_KEY** (String) - The private key for the domain used in HOSTNAME_OVERRIDE
- **TLS_KEY_GRID** (String) - The private key for the domain used to run the BlazeMeter Grid proxy over HTTPS
- **VERIFY_SSL** (Boolean) - If set to false, will send insecure requests to HTTPS addresses. If true a CA bundle may be required if something other than BlazeMeter requires HTTPS connections. Default: true

### Kubernetes Environment Variables

Key environment variables include:

- **AUTH_TOKEN** (String) - The agent auth token
- **AUTO_KUBERNETES_UPDATE** (Boolean) - If true, activate Kubernetes auto updater. Default: false
- **AWS_CA_BUNDLE** (String) - This value is always /etc/ssl/certs/ca-certificates.crt. Denotes the location of the certificate bundle
- **CONTAINER_MANAGER_TYPE** (String) - Valid values: DOCKER, KUBERNETES. Default: DOCKER
- **DOCKER_REGISTRY** (String) - The address of your private Kubernetes registry. It uses the same variable as Docker
- **DODUO_PORT** (String) - The user-defined port where to run Doduo (BlazeMeter Grid Proxy). By default, Doduo listens on port 8000
- **HARBOR_ID** (String) - The ID of the private location with which the agent is associated
- **HTTPS_PROXY** (String) - URL of HTTPS proxy server to be used for all HTTPS requests sent by agent to a.blazemeter.com. Also passed to the other components
- **HTTP_PROXY** (String) - URL of the HTTP proxy server to be used for all HTTP requests sent by the agent to a.blazemeter.com. Also passed to other components
- **IMAGE_OVERRIDES** (JSON Encoded String) - Allows the override of the default image received from BZA for the container to run. Set the key to the original value (Example: `apm-image:latest`). Set the value to the new repository name with a tag. Extract the appropriate version number from 'admin/ship-stats'. Must be JSON encoded. Must follow the following regular expression format: `{"path/<image_name:latest>":"path/<image_name:version_number>"}`. Example: `{"blazemeter/crane:latest":"gcr.io/verdant-bulwark-278/blazemeter/crane:3.6.47"}`
- **INHERIT_RUNNING_USER_AND_GROUP** (Boolean) - If true, it indicates that containers launched should use the same UID:GID as the Crane itself. Default: false
- **KUBERNETES_CUSTOM_ANNOTATIONS_JSON** (JSON Encoded String) - JSON-encoded string of annotations to be added to all pods created by Crane. Safe-to-evict is always set to false in addition to whatever is defined using this environment variable. Example: `{ "customAnnotation": "customValue" }`
- **KUBERNETES_ISTIO_GATEWAY_NAME** (String) - This value denotes the name of the Istio Gateway to be used. If left empty or not present, an Istio Gateway will be created by default (if KUBERNETES_WEB_EXPOSE_TYPE is set to ISTIO)
- **KUBERNETES_LIMITS_EPHEMERAL_STORAGE** (Integer) - Integer value in megabytes. Set to control the ephemeral storage limits of the Taurus pod (optional). Default: None. Example: `name: KUBERNETES_LIMITS_EPHEMERAL_STORAGE value: '8192'`
- **KUBERNETES_REQUESTS_EPHEMERAL_STORAGE** (Integer) - Integer value in megabytes. Set to control the ephemeral storage requests of the Taurus pod (optional). Default: 100 (Mi). Example: `name: KUBERNETES_REQUESTS_EPHEMERAL_STORAGE value: '100'`
- **KUBERNETES_SERVICES_BLOCKING_GET** (Boolean) - This needs to be set to true when creating numerous transactional virtual services to avoid potential issues with K8S provisioning of pods. Default: false
- **KUBERNETES_USE_APIPA** (Boolean) - Crane uses kubernetes node information to discover the IP Address of the endpoint. By default, this is disabled and "127.0.0.1" is used as the Automatic Private IP Address (APIPA) for all endpoints. To use kubernetes node IP address then set this flag to False. Default: true
- **KUBERNETES_USE_PRE_PULLING** (Boolean) - Allows the K8S cluster to pre-pull images when updates occur to BlazeMeter components. Default: false
- **KUBERNETES_WEB_EXPOSE_SUB_DOMAIN** (String) - The subdomain to be used when creating transactional virtual services. Example Value: example.user.net
- **KUBERNETES_WEB_EXPOSE_TLS_SECRET_NAME** (String) - The TLS secret name that contains the TLS key and TLS secret for the domain provided in KUBERNETES_WEB_EXPOSE_SUB_DOMAIN
- **KUBERNETES_WEB_EXPOSE_TYPE** (String) - This indicates the type of web interface to be used. The values can be INGRESS or CONTOUR or ISTIO
- **KUBERNETES_LABELS** (JSON) - Labels to add to resources created by agent. Must be in JSON format. Syntax: `{"label_1": "label_1_value", "label_2": "label_2_value"}`
- **KUBERNETES_NODE_SELECTOR_JSON** (JSON) - Used to configure the k8s nodeSelector field to match specific node labels for the Crane engine deployment. Must be in JSON format. Syntax: `{"label_1": "label_1_value", "label_2": "label_2_value"}`
- **KUBERNETES_RESOURCES_LIMITS_CPU** (String) - CPU limits for resources created by agent
- **KUBERNETES_RESOURCES_LIMITS_MEMORY** (String) - Memory limits for resources created by agent
- **KUBERNETES_SERVICE_USE_TYPE** (String) - Allows the K8S cluster to use ClusterIP services over the default NodePort service for virtual services. Can be NODEPORT or CLUSTERIP. Default: NODEPORT
- **KUBERNETES_TOLERATIONS_JSON** (Array) - Set to specify that the crane container passes tolerations and node selector elements to child containers. Syntax: `'[{ "effect": "NoSchedule", "key": "lifecycle", "operator": "Equal", "value": "spot" }]'`
- **KUBERNETES_WEB_EXPOSE_SHORT_URL** (Boolean) - When enabled, generate shorter ingress URLs by omitting namespace name and container port. WARNING: Limits port exposing to only 1 port per container due to missing port number in URL! Default: false
- **NO_PROXY** (String) - URL that should be excluded from proxying (on servers that should be contacted directly)
- **PREFERRED_INTERFACE** (String) - Uses a specific network interface to gather the machine's IP address. If the interface is unavailable, it falls back to use the first available interface (not in the denylist, see default). Default: none; Uses first interface available not in list: docker0, lo
- **REQUESTS_CA_BUNDLE** (String) - This value is always /etc/ssl/certs/ca-certificates.crt. Denotes the location of the certificate bundle
- **SHIP_ID** (String) - The ID of the agent
- **TLS_CERT_GRID** (String) - The public certificate for the domain used to run the BlazeMeter Grid proxy over HTTPS
- **TLS_KEY_GRID** (String) - The private key for the domain used to run the BlazeMeter Grid proxy over HTTPS
- **VERIFY_SSL** (Boolean) - If set to false, will send insecure requests to HTTPS addresses. If true a CA bundle may be required if something other than BlazeMeter requires HTTPS connections. Default: true

---

## Enable Auto-Update for Running Containers

Configure automatic updates for running containers in private locations, including AUTO_UPDATE, AUTO_KUBERNETES_UPDATE, and AUTO_UPDATE_CONTAINERS_WHILE_RUNNING environment variables.

**Use when**: Configuring automatic updates for running containers in private locations or setting up AUTO_UPDATE, AUTO_KUBERNETES_UPDATE, and AUTO_UPDATE_CONTAINERS_WHILE_RUNNING environment variables.

### Enable Auto-Update for Running Containers

To configure your running containers to upgrade themselves automatically, set the following environment variables to true:

- **AUTO_UPDATE** Controls auto update of Crane itself on Docker, default: true
- **AUTO_KUBERNETES_UPDATE** Controls auto update of Crane itself on Kubernetes, default: false
- **AUTO_UPDATE_CONTAINERS_WHILE_RUNNING** Controls auto update of components, default false. Also, either AUTO_UPDATE or AUTO_KUBERNETES_UPDATE must be *true* for this option to work, depending on the platform Crane is running on

When auto-upgrade is enabled, the agent checks periodically whether there is a new version of the Crane agent component images. The first check is right after starting, and from then on, once per hour. As soon a newer image is found, the running container is replaced by the new one, and it will use the newer image.

### What are the benefits of auto-upgrade?

- You do not need to check versions manually and restart running services manually to have the latest images
- On Kubernetes, there is no outage of the running crane components

### What are the drawbacks of auto-upgrade?

- You will lose the virtual services' state
- Once the running virtual services are replaced, all logs are lost
- On Docker, there will be a short outage for any running virtual services. A new instance needs to download transactions using the Service Virtualization API and reconfigure itself. This outage length depends on network speed and the number of transactions within the virtual services

---

## Configure Agents to Use Corporate Proxy

Configure private location agents to connect through corporate proxy servers for Docker and Kubernetes installations, including HTTP_PROXY, HTTPS_PROXY, and NO_PROXY settings.

**Use when**: Configuring private location agents to connect through corporate proxy servers or setting up HTTP_PROXY, HTTPS_PROXY, and NO_PROXY settings for Docker and Kubernetes installations.

### Proxy Configuration

- **HTTP_PROXY**: Set HTTP proxy server
- **HTTPS_PROXY**: Set HTTPS proxy server
- **NO_PROXY**: Configure proxy bypass list
- **Authentication**: Set proxy authentication if needed

---

## Configure Docker Installation to Use CA Bundle

Configure Docker installations to use custom CA certificate bundles, including creating CA bundles, mounting certificates, and configuring for Grid Proxy.

**Use when**: Configuring Docker installations to use custom CA certificate bundles or creating CA bundles, mounting certificates, and configuring for Grid Proxy.

### CA Bundle Configuration

1. **Create CA Bundle**: Create certificate bundle file
2. **Mount Certificates**: Mount certificates in container
3. **Configure Grid Proxy**: Set up Grid Proxy configuration

---

## Configure Kubernetes Agent to Use CA Bundle

Configure Kubernetes installations to use CA certificates via ConfigMaps, including creating ConfigMaps, mounting volumes, and configuring for Grid Proxy.

**Use when**: Configuring Kubernetes installations to use CA certificates via ConfigMaps or creating ConfigMaps, mounting volumes, and configuring for Grid Proxy.

### Kubernetes CA Configuration

1. **Create ConfigMap**: Create ConfigMap with CA certificates
2. **Mount Volumes**: Mount certificate volumes
3. **Configure Grid Proxy**: Set up Grid Proxy configuration

---

## Bring Your Own Certificate Mock Services

Configure custom SSL/TLS certificates for Service Virtualization on Docker and Kubernetes agents, including certificate requirements, hostname validation, and Ingress controller setup.

**Use when**: Configuring custom SSL/TLS certificates for Service Virtualization on Docker and Kubernetes agents or setting up certificate requirements, hostname validation, and Ingress controller configuration.

### Certificate Configuration

- **Certificate Requirements**: Understand certificate requirements
- **Hostname Validation**: Configure hostname validation
- **Ingress Controller**: Set up Ingress controller
- **Certificate Installation**: Install custom certificates

---

## OpenShift Support

Set up Service Virtualization on OpenShift Container Platform, including creating projects, roles, deploying agents, and using HAProxy for ingress. The Service Virtualization component of BlazeMeter supports the OpenShift Container Platform web console. You can create a new project, create a role for an agent, and deploy the agent using OpenShift. You can then deploy virtual services to your Private Location as usual.

The BlazeMeter Agent and containers officially support OpenShift for virtual services when using HAProxy only. Support for Contour or Istio on OpenShift is experimental at this time. OpenShift Support for other components has not been tested.

**Use when**: Setting up Service Virtualization on OpenShift Container Platform or creating projects, roles, deploying agents, and using HAProxy for ingress.

### Set Up Service Virtualization on the OpenShift Platform

The setup consists of two sections:
1. An administrator creates a new project and a role for the agent
2. A developer (or any non-admin role) deploys the agent

### Create a New Project and a Role for the Agent

OpenShift admin needs to perform these steps as a prerequisite before a developer can set up Service Virtualization.

Follow these steps:

1. Create a new project with name blazemeter:
   ```bash
   oc new-project blazemeter
   ```

2. Create Role for the agent. Apply the YAML file:
   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     name: role-crane
     namespace: blazemeter
   rules:
   - apiGroups:
     - ""
     resources:
     - pods
     - pods/log
     verbs:
     - get
     - list
   - apiGroups:
     - ""
     - extensions
     - apps
     resources:
     - pods
     - services
     - endpoints
     - daemonsets
     - pods/*
     - pods/exec
     - deployments
     - replicasets
     - deployments/scale
     verbs:
     - get
     - list
     - watch
     - create
     - update
     - patch
     - delete
     - deletecollection
     - createcollection
   - apiGroups:
     - route.openshift.io
     resources:
     - routes
     - routes/custom-host
     verbs:
     - get
     - list
     - create
     - update
     - patch
     - delete
   ```
   Run the following command:
   ```bash
   oc apply -f ./role-crane.yaml
   ```

3. Create Role binding for the agent to default service account in the blazemeter project. Apply the YAML file:
   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: role-binding-crane
     namespace: blazemeter
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: Role
     name: role-crane
   subjects:
   - kind: ServiceAccount
     name: default
     namespace: blazemeter
   ```
   Run the following command:
   ```bash
   oc apply -f ./rolebinding-crane.yaml
   ```

4. Provide editing permissions to a developer (or any non-admin user) who will be deploying the agent:
   ```bash
   oc adm policy add-role-to-user edit developer
   ```

### Deploy the Agent

**Prerequisite:** OpenShift admin needs to create a new project and a role for the agent.

Follow these steps:

1. Log in as a developer:
   ```bash
   oc login -u developer -p developer https://api.crc.testing:6443
   ```

2. Create a configmap required for the agent app. Edit the agent config map template with the name 'crane-cm-template.yaml' to update the AUTH_TOKEN, HARBOR_ID, SHIP_ID. You can get these values by creating a new private location in BlazeMeter. Update the KUBERNETES_WEB_EXPOSE_SUB_DOMAIN with the sub domain of the route host name. (Optional) Update the DOCKER_REGISTRY if you are using the images from your own Docker registry instead of gcr.io.

   Use the following YAML file for reference:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: crane-cm
     namespace: blazemeter
   data:
     AUTH_TOKEN: <AUTH_TOKEN>
     CONTAINER_MANAGER_TYPE: KUBERNETES
     DOCKER_REGISTRY: gcr.io/verdant-bulwark-278
     HARBOR_ID: <HARBOR_ID>
     INHERIT_RUNNING_USER_AND_GROUP: "true"
     KUBERNETES_SERVICE_USE_TYPE: CLUSTERIP
     KUBERNETES_SERVICES_BLOCKING_GET: "true"
     KUBERNETES_WEB_EXPOSE_SUB_DOMAIN: apps-crc.testing
     KUBERNETES_WEB_EXPOSE_TYPE: OPENSHIFT
     SHIP_ID: <SHIP_ID>
   ```
   Run the following command:
   ```bash
   oc apply -f ./crane-cm.yaml
   ```

3. Deploy the agent. Use the following YAML file for reference:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: crane
     labels:
       role: role-crane
   spec:
     selector:
       matchLabels:
         role: role-crane
     replicas: 1
     strategy:
       type: Recreate
     template:
       metadata:
         labels:
           role: role-crane
       spec:
         restartPolicy: Always
         terminationGracePeriodSeconds: 30
         containers:
         - envFrom:
           - configMapRef:
               name: crane-cm
           name: bzm-crane
           image: gcr.io/verdant-bulwark-278/blazemeter/crane:3.5.159
           imagePullPolicy: Always
   ```
   Run the following command:
   ```bash
   oc apply -f ./deployment-crane.yaml
   ```

4. Verify the agent status in BlazeMeter. Go to **Settings**, **Workspace**, **Private Locations**

Once the agent is deployed, you can deploy the virtual services to your Private location as usual.

To check the deployments, log in to the OpenShift console:
```bash
crc console
```

---

## Supported SSL CA Certificates

Understand supported SSL CA certificates for Radar Agent, including the Mozilla Included CA Certificate List reference. The Radar agent supports certificates from the following authority list: [Mozilla Included CA Certificate List](https://ccadb-public.secure.force.com/mozilla/IncludedCACertificateReport).

**Use when**: Understanding supported SSL CA certificates for Radar Agent or referencing the Mozilla Included CA Certificate List for certificate validation.

### Certificate Support

- **Mozilla CA List**: Reference Mozilla Included CA Certificate List for all supported certificate authorities
- **Certificate Validation**: The Radar agent validates certificates against the Mozilla Included CA Certificate List
- **Supported Certificates**: All certificates from the Mozilla Included CA Certificate List are supported

For more information on configuring certificates, see [Configuring Radar Agent Certificates](skill-blazemeter-private-locations://references/radar-agent.md) in the Radar Agent documentation.

---

## Internal Repository

Configure private locations to use internal Docker registries and JMeter plugin repositories, including DOCKER_REGISTRY environment variable and plugin manager configuration.

**Use when**: Configuring private locations to use internal Docker registries and JMeter plugin repositories or setting up DOCKER_REGISTRY environment variable and plugin manager configuration.

### Internal Repository Setup

- **DOCKER_REGISTRY**: Configure internal Docker registry
- **Plugin Manager**: Set up plugin repository
- **Repository Configuration**: Configure repository settings

---

## Configure Crane Agent to Ensure Mock Service Deployed is Reachable

Configure Crane agent to ensure virtual services deployed on private locations are reachable, including identifying network interfaces and setting PREFERRED_INTERFACE environment variable.

**Use when**: Configuring Crane agent to ensure virtual services deployed on private locations are reachable or identifying network interfaces and setting PREFERRED_INTERFACE environment variable.

### Network Interface Configuration

- **Identify Interfaces**: Identify available network interfaces
- **PREFERRED_INTERFACE**: Set preferred interface variable
- **Reachability**: Ensure services are reachable

---

## Documentation References

For detailed information about Private Location configuration, use the BlazeMeter MCP help tools:

**Configuration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `private-locations-blazemeter-agent-environment-variables` (environment variables), `private-locations-how-to-enable-auto-upgrade-for-running-containers` (auto-update), `private-locations-optional-installation-step-configure-agents-to-use-corporate-proxy` (corporate proxy), `private-locations-optional-installation-step-configure-docker-installation-to-use-ca-bundle` (Docker CA bundle), `private-locations-optional-installation-step-configure-kubernetes-agent-to-use-ca-bundle` (Kubernetes CA bundle), `private-locations-optional-installation-step-bring-your-own-certificate-mock-services` (BYO certificate), `private-locations-openshift-support-for-blazemeter-agent-for-kubernetes` (OpenShift), `private-locations-supported-ssl-ca-certificates-for-radar-agent` (SSL CA certificates), `private-location-internal-repository` (internal repository), `private-locations-configure-crane-agent-to-ensure-mock-service-deployed-is-reachable` (Crane agent)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["private-locations-blazemeter-agent-environment-variables", "private-locations-how-to-enable-auto-upgrade-for-running-containers", "private-locations-optional-installation-step-configure-agents-to-use-corporate-proxy", "private-locations-optional-installation-step-configure-docker-installation-to-use-ca-bundle", "private-locations-optional-installation-step-configure-kubernetes-agent-to-use-ca-bundle", "private-locations-optional-installation-step-bring-your-own-certificate-mock-services", "private-locations-openshift-support-for-blazemeter-agent-for-kubernetes", "private-locations-supported-ssl-ca-certificates-for-radar-agent", "private-location-internal-repository", "private-locations-configure-crane-agent-to-ensure-mock-service-deployed-is-reachable"]}`

