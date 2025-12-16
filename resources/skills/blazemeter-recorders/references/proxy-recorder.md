# Proxy Recorder

## Creating the Proxy Recorder

With BlazeMeter's Proxy Recorder technology, you can easily record and create JMeter performance test scenarios for your mobile or web app, even when using a secure connection. The proxy recorder works with both web, mobile browsers and native mobile apps.

In addition, you don't need to install any additional software on your phone or computer.

**Use when**: Creating a proxy recorder for recording performance test scenarios or configuring proxy types, port configuration, and private location setup.

### Overview

With BlazeMeter's Proxy Recorder technology, you can easily record and create JMeter performance test scenarios for your mobile or web app, even when using a secure connection. The proxy recorder works with both web, mobile browsers and native mobile apps.

In addition, you don't need to install any additional software on your phone or computer.

**Before using the Proxy Recorder**, please verify that the computer running the proxy has port 80 open for proxies created in the cloud, or allowing traffic from the Private Location you are using.

**Known Limitations:**
- The Proxy Recorder rewrites the packets since it must decipher the incoming and outgoing packets using its own certificate. Thus, this recording solution **will not work** when the tested application/server uses [Certificate pinning](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning#How_It_Works)
- If the machine you're recording from is on an internal network which is behind its own proxy, then the Proxy Recorder **will not work**. This is because it is not possible to run one proxy from behind another proxy (at least within the context of the recorder)

The Proxy Recorder captures HTTP/HTTPS traffic between your application and the internet, allowing you to record test scenarios for mobile apps, web apps, and APIs. It supports:
- Mobile app recording
- Web app recording
- API recording
- Multiple proxy types

### How To Create a Proxy

1. Log in to your BlazeMeter account
2. Go to the Performance tab
3. Go to mobile recorder URL: [https://a.blazemeter.com/app/recorder/#/](https://a.blazemeter.com/app/recorder/#/) or click the Recorder button in the Create Test screen under the Performance tab
4. You will see the proxy recorder screen
5. Choose what type of proxy you wish to create:
   - A proxy with random IP over port 80
   - A proxy with a random IP over a random port which is not 80
6. For iOS devices, enable "Launch proxy recorder with random port"
7. If your network is not open to external networks, generate the proxy recorder in a [private location](skill-blazemeter-private-locations://references/introduction.md). To do so, open the location drop-down and chose the private location you wish to use. The proxy recorder will be generated on the first available load generator in the chosen location. If needed, [set the port range for your ships](skill-blazemeter-recorders://references/proxy-recorder.md) now

Before you can start recording, you must configure you device or browser to use the proxy recorder:
- [Configure Android Devices for Proxy Recording](skill-blazemeter-recorders://references/proxy-recorder.md)
- [Configure Apple Devices for Proxy Recording](skill-blazemeter-recorders://references/proxy-recorder.md)
- [Configure Firefox for Proxy Recording](skill-blazemeter-recorders://references/proxy-recorder.md)
- [Configure Chrome for Proxy Recording](skill-blazemeter-recorders://references/proxy-recorder.md)

### Proxy Types

- **Cloud Proxy**: Use BlazeMeter cloud infrastructure (port 80 or random port)
- **Private Location Proxy**: Use Private Location for on-premise recording
- **Random Port**: For iOS devices, enable "Launch proxy recorder with random port"

### Configuration Steps

1. **Select Proxy Type**: Choose cloud, private location, or random port
2. **Configure Port**: Set proxy port (default 80, or random port for iOS)
3. **Set Up Private Location** (if needed): Configure Private Location for on-premise recording
4. **Create Proxy**: Create proxy recorder instance
5. **Get Proxy Details**: Obtain proxy URL and port for device/browser configuration (shown in left panel)

### Best Practices

- Use cloud proxy for quick setup
- Use private location proxy for on-premise apps
- Configure appropriate port ranges
- Document proxy configuration
- Verify port 80 is open for cloud proxies
- Note: Certificate pinning and nested proxies are not supported

---

## Recording Your Session

After you have created a [Proxy Recorder](skill-blazemeter-recorders://references/proxy-recorder.md), and configured your mobile device or browser, you are now ready to record your session for the performance test.

**Use when**: Recording performance test sessions using the proxy recorder or capturing requests, pausing/stopping recording, exporting as JMX/JSON/URL list/Smart JMX, and shutting down the proxy.

### Capture Requests

Go back to your Browser window/tab, and start accessing your web app, or browse the URLs you want to test. The Recorder starts showing all the captured requests.

Once you've recorded the requests, press "Pause".

When you're 100% finished, click the "Stop" button on the left panel.

### Recording Process

1. **Start Proxy**: Start proxy recorder (after creating it)
2. **Configure Device/Browser**: Configure device or browser to use proxy (see configuration sections below)
3. **Start Recording**: Begin recording session (click the big red button at the bottom of the screen)
4. **Interact with App**: Use your application normally - browse URLs, interact with your web app
5. **View Requests**: The Recorder shows all the captured requests in real-time
6. **Pause Recording**: Press "Pause" when needed
7. **Stop Recording**: Click the "Stop" button on the left panel when finished

### Export the Recording as Performance Test

Now you have your performance test recording. Next, you need to decide what to do with it. You have the following options:

1. **Export it as a JMeter .jmx file**. Edit if necessary and run your load test.
2. **Export it as a JSON file**. Again, you can edit it before running your test.
3. **Export it as a URL list** to instantly create a URL test. Just export it, go to the BlazeMeter app and start running your test.
4. **Export it as a "Smart JMX"**.

### Export Formats

- **JMX**: Export as JMeter script (JMX format)
- **JSON**: Export as JSON format
- **URL List**: Export as list of URLs (instantly create a URL test)
- **Smart JMX**: Export as optimized JMeter script

### Recording Controls

- **Start/Stop**: Control recording start and stop (big red button at bottom of screen)
- **Pause/Resume**: Pause and resume recording
- **View Requests**: View captured requests in real-time in the recorder interface

### Shut Down the Proxy

Don't forget to disable the Proxy after running your test.

1. Return to your Network settings.
2. Uncheck the Proxy option to turn it off.
3. Click "Apply" to save the changes.
4. Go to your Recorder page, and click the "TERMINATE PROXY" button at the bottom of the left panel.

If you have any questions, e-mail us at: [support-blazemeter@perforce.com](mailto:support-blazemeter@perforce.com?subject=Proxy Recorder).

### Best Practices

- Clear app cache before recording
- Record complete user workflows
- Review captured requests before export
- Test exported scripts before production use

---

## Configure Chrome for Proxy Recording

Configure Chrome browser to use BlazeMeter Proxy Recorder for recording web application traffic.

**Use when**: Configuring Chrome browser for proxy recording or setting up Chrome to route traffic through BlazeMeter Proxy Recorder.

### Recording Using Chrome (Mac)

On the left panel of the proxy recorder, you should be able to see all your proxy settings that you will need to enter in the following steps:

1. Open your Chrome Preferences by accessing the Chrome Menu, and selecting "Preferences..." from the menu. The "Settings" tab opens
2. In the top right Search box, enter "proxy". Search results are displayed
3. Click "Open Proxy Settings". A separate window opens for 'Network' settings and the 'Proxy' section (or Proxies, depending on your OS)
4. Check the option "Web Proxy", and fill out the fields for "Web Proxy Server" and port:
   - Enable the "Proxy server requires password" checkbox
   - Enter the username and password from your proxy recorder settings
   - Enter the web proxy server name from your proxy recorder settings. Don't include the port number at the end and don't include the "http://" prefix
   - Enter the port from your proxy recorder settings
5. Click OK
6. In next window, click "Apply" to apply this change
7. In your Chrome browser, enter the following URL: **http://mitm.it**. You'll see various OS options, including Windows, Apple on this page
8. Select the Apple version. If you have an issue with the Apple or Windows certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html) here
9. Return to your Recorder window/tab, and click that big red button at the bottom of your screen

Now you are ready start [recording your session](https://help.blazemeter.com/docs/guide/recorders-recording-your-session.html) in Mac Chrome.

### Recording Using Chrome (Windows)

On the left panel of the proxy recorder, you should be able to see all your proxy settings that you will need to enter in the following steps:

1. Access the main Chrome Menu, and select the "Settings" menu item. The "Settings" tab opens
2. In the top Search box, enter "proxy". Search results are displayed
3. Click "Open proxy settings". A separate "Internet Properties" window opens
4. Click the "LAN settings" button
5. Check the option "Use a proxy server...", and fill out the fields:
   - Enter the IP from your proxy recorder settings under Address. NOTE: don't include the port number at the end and don't include the "http://" prefix
   - Enter the port from your proxy recorder settings
   - Note down the username and password for later. There is no section that has a place to store the username and password. You will be prompted to enter these credentials in the browser when trying to access sites
6. Click OK
7. In next window, click "Apply" and then "OK", to apply this change
8. In your Chrome browser, enter the following URL: **http://mitm.it**. You'll see various OS options, including Windows, Apple on this page
9. Select the Windows version. If you have an issue with the Apple or Windows certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html) here
10. Return to your Recorder window/tab, and click that big red button at the bottom of your screen

Now you are ready to start [recording your session](https://help.blazemeter.com/docs/guide/recorders-recording-your-session.html) in Windows Chrome.

### Certificate Installation

- **Download Certificate**: Navigate to http://mitm.it in Chrome and select your OS version (Apple for Mac, Windows for Windows)
- **Install Certificate**: Install certificate in Chrome
- **Trust Certificate**: Trust certificate for HTTPS traffic
- **Alternative**: If you have an issue with the OS-specific certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html)

### Best Practices

- Use separate Chrome profile for recording
- Clear browser cache before recording
- Verify certificate installation
- Test proxy connection before recording

---

## Configure Firefox for Proxy Recording

Configure Firefox browser to use BlazeMeter Proxy Recorder for recording web application traffic.

**Use when**: Configuring Firefox browser for proxy recording or setting up Firefox to route traffic through BlazeMeter Proxy Recorder.

### Configuration Steps

On the left panel of the proxy recorder, you should be able to see all your proxy settings that you will need to enter in the following steps:

1. Enter the 'Preferences' section in your browser. The following sample screenshot shows the respective menu on macOS
2. Select the section 'General', go to the 'Network Proxy' section, and click the 'Settings' button. The Connection Settings window opens
3. Select the option 'Manual Proxy configuration'. Enter the proxy details from the proxy recorder settings shown above, and press the 'OK' button. Don't include the colon and port number at the end and don't include the "http://" prefix
4. In your Firefox browser, enter the following URL: **http://mitm.it**. You'll see various OS options, including Windows, Apple
5. Select the one that you're using. If you have an issue with the Windows or Apple certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html) here as well. A new window opens and prompts you to examine and trust the certificate
6. Choose and install the certificate
7. When prompted, enter a username and a password to authenticate to the recorder proxy. Find the username and password in the proxy settings shown in the beginning of this article
8. Return to your Recorder window/tab, and click that big red button at the bottom of your screen

Now you are ready to start [recording your session](https://help.blazemeter.com/docs/guide/recorders-recording-your-session.html).

### Certificate Installation

- **Download Certificate**: Navigate to http://mitm.it in Firefox and select your OS version
- **Install Certificate**: A new window opens and prompts you to examine and trust the certificate. Choose and install the certificate
- **Authenticate**: When prompted, enter a username and a password to authenticate to the recorder proxy (find these in the proxy settings)
- **Alternative**: If you have an issue with the OS-specific certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html)

### Best Practices

- Use separate Firefox profile for recording
- Clear browser cache before recording
- Verify certificate installation
- Test proxy connection before recording

---

## Configure Apple Devices for Proxy Recording

Configure Apple iOS devices for proxy recording, including WiFi proxy settings, certificate installation, and trust configuration for BlazeMeter proxy recorder.

**Use when**: Configuring Apple iOS devices for proxy recording or setting up WiFi proxy settings, certificate installation, and trust configuration.

### Configuration Steps

On the left panel of the Proxy recorder, you should be able to see all your proxy settings:

1. Go to your device's 'Settings', go to 'WIFI' and click on your local WIFI network
2. Click 'Configure Proxy' and got to the 'Configure Proxy' settings page. By default this option is Off. Select the Manual option to enable the proxy
3. Enter data for the server and the port. Look at the proxy settings we provided earlier:
   - For the server, enter the text displayed in the current proxy field. Don't include the colon and port number at the end and don't include the "http://" prefix
   - Enter the port number in the 'port' field
   - Set the Authentication to "disabled"
4. Open your mobile browser and enter the following URL: **http://mitm.it**. You should see various devices, including Android and Apple, on your screen. Select the Apple version for this case
   - **NOTE:** If you have an issue with the Apple certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html) here as well
5. **IMPORTANT**: For **Apple/iOS** devices, perform the following:
   - Download the BZ certificate as instructed to your device
   - In your Apple device, go to: **Settings > General > About > Certificate Trust Settings**
   - Under "Enable full trust for root certificates," turn on trust for the certificate
6. Next, go back to your Recorder window/tab, and click that big red button at the bottom of your screen

Now you are ready to start [recording your session](https://help.blazemeter.com/docs/guide/recorders-recording-your-session.html).

### WiFi Proxy Settings

- **Manual Proxy**: Configure manual proxy settings (select Manual option)
- **Server Address**: Enter proxy server address (from proxy settings, without http:// prefix and without port)
- **Port**: Enter proxy port number
- **Authentication**: Set to "disabled"

### Certificate Installation

- **Download Certificate**: Navigate to http://mitm.it in mobile browser and select Apple version
- **Install Certificate**: Download the BZ certificate to your device
- **Trust Certificate**: **IMPORTANT** - In your Apple device, go to: **Settings > General > About > Certificate Trust Settings**. Under "Enable full trust for root certificates," turn on trust for the certificate
- **Alternative**: If you have an issue with the Apple certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html)

### Best Practices

- Use device and computer on same network
- Verify WiFi proxy settings are correct
- Ensure certificate is fully trusted
- Test connection before recording

---

## Configure Android Devices for Proxy Recording

Configure Android devices for proxy recording, including WiFi proxy settings, certificate installation, and trust configuration for BlazeMeter proxy recorder.

**Use when**: Configuring Android devices for proxy recording or setting up WiFi proxy settings, certificate installation, and trust configuration.

### Enable Debug Mode

First, ensure your Android app has the following permissions to allow for the proxy recorder to record traffic on it while in debug mode:

1. Ensure the application has the following permissions:
   ```xml
   <uses-permission android:name="android.permission.INTERNET"/>
   <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
   <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
   ```
2. In the application tag, include the following attribute:
   ```xml
   android:networkSecurityConfig="@xml/network_security_config"
   ```
3. Create the XML directory in base/src/{packageMain}/res and add the following XML content to the file network_security_config.xml:
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <network-security-config>
     <debug-overrides>
       <trust-anchors>
         <!-- Trust user added CAs while debuggable only -->
         <certificates src="user" />
       </trust-anchors>
     </debug-overrides>
   </network-security-config>
   ```
4. Run your app in debug mode

For more information on this procedure, see [the official Android Developers documentation](https://developer.android.com/privacy-and-security/security-config#network-security-config).

### Configure the Device to Record Traffic

Once the above is done, follow the below steps to record traffic from your app or mobile browser:

On the left panel of the Proxy Recorder, you should be able to see all your proxy settings that you will need to enter in the following steps:

It's now time to configure your Android device. Ensure your Wi-Fi connection is turned on.

1. Go to your device's "Settings", go to Connections, then "Wi-Fi", and hold selection on your local Wi-Fi network
2. Select the "Manage network settings" option and select "Show advanced options"
3. Tap the Proxy dropdown and select "Manual" for the proxy setup. You'll now be asked to enter data for the server and the port
4. Look at the proxy settings we provided earlier. For the server, enter the text displayed in the current proxy field. Don't include the colon and port number at the end and don't include the "http://" prefix. Enter the port number in the 'port' field
5. Activate the "Authenticate server" option and enter the authentication username and password that are provided in the proxy setup
6. You may be prompted for the username and password when accessing the browser, so be prepared to enter this information again
7. Tap the "Save" button to save your changes
8. Open your mobile browser and enter the following URL: **http://mitm.it**. You should see various devices, including Android and Apple, on your screen
9. Select Android. If you have an issue with the Android certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html)
10. Tap the Android option and download the certificate
11. When prompted, enter a name for the certificate (doesn't matter what the name is) and set the "Used for" to "VPN and Apps", and tap "OK"
12. Turn off the Wi-Fi on your device, then turn it back on. This step recycles the connection to use the certificate
13. Next, go back to your Recorder window/tab, and click that big red button at the bottom of your screen

Now you are ready to start [recording your session](https://help.blazemeter.com/docs/guide/recorders-recording-your-session.html).

### WiFi Proxy Settings

- **Manual Proxy**: Configure manual proxy settings (select "Manual" from Proxy dropdown)
- **Proxy Hostname**: Enter proxy server address (from proxy settings, without http:// prefix and without port)
- **Proxy Port**: Enter proxy port number
- **Authenticate server**: Activate this option and enter the authentication username and password from proxy settings

### Certificate Installation

- **Download Certificate**: Navigate to http://mitm.it in mobile browser and select Android version
- **Install Certificate**: Tap the Android option and download the certificate
- **Set Certificate Name**: When prompted, enter a name for the certificate (doesn't matter what the name is) and set the "Used for" to "VPN and Apps", and tap "OK"
- **Recycle Connection**: Turn off the Wi-Fi on your device, then turn it back on. This step recycles the connection to use the certificate
- **Alternative**: If you have an issue with the Android certificate, you can also use the [Other certificate](https://help.blazemeter.com/docs/guide/recorders-using-the-other-certificate.html)

### Best Practices

- Use device and computer on same network
- Verify WiFi proxy settings are correct
- Ensure certificate is installed and trusted
- Test connection before recording

---

## Using the Other Certificate

Use the universal "Other" certificate for proxy recording when device-specific certificates fail, providing a fallback option for all environments.

**Use when**: Device-specific certificates fail for proxy recording or using the universal "Other" certificate as a fallback option for all environments.

### Overview

When using the [Proxy Recorder](https://help.blazemeter.com/docs/guide/recorders-creating-the-proxy-recorder.html), if there is ever an issue with the certificate used for an Apple, Android, or Windows device, then the "Other" certificate is an all-around certificate that will work on any environment.

The process for installing is the same as for the device specific certificates, but this default certificate will work on all environments and is a way to get your recording done, in case an issue with one of the device-specific certificates is found.

The "Other" certificate is a universal certificate that works across all devices and browsers when device-specific certificates fail. It provides:
- Universal compatibility
- Fallback option
- Simplified certificate management

### When to Use

- **Device-Specific Certificate Fails**: When device-specific certificate doesn't work
- **Multiple Devices**: When recording from multiple device types
- **Quick Setup**: When you need quick certificate setup
- **Compatibility Issues**: When experiencing certificate compatibility issues

### Installation

In the following procedures, you can replace the certificate download step for each of the device specific steps with the download of the "Other" certificate:

- [Configure Android Devices for Proxy Recording](https://help.blazemeter.com/docs/guide/recorders-configure-android-devices-for-proxy-recording.html)
- [Configure Apple Devices for Proxy Recording](https://help.blazemeter.com/docs/guide/recorders-configure-apple-devices-for-proxy-recorder.html)
- [Configure Firefox for Proxy Recording](https://help.blazemeter.com/docs/guide/recorders-configure-firefox-for-proxy-recording.html)
- [Configure Chrome for Proxy Recording](https://help.blazemeter.com/docs/guide/recorders-configure-chrome-for-proxy-recording.html)

**Steps:**
1. **Download "Other" Certificate**: Navigate to http://mitm.it and select "Other" instead of the device-specific option
2. **Install on Device/Browser**: Install certificate on target device or browser (same process as device-specific certificates)
3. **Trust Certificate**: Trust certificate in device/browser settings (follow device-specific trust procedures)
4. **Test Connection**: Verify proxy connection works

### Best Practices

- Try device-specific certificates first
- Use "Other" certificate as fallback when device-specific certificates fail
- Ensure certificate is fully trusted
- Test connection after installation
- The installation process is the same as device-specific certificates, just select "Other" from http://mitm.it

---

## Setting Port Range on Your Agent

Set custom port ranges for proxy recorder and service virtualization on private locations, including static endpoints, API configuration, and port range limitations.

**Use when**: Setting custom port ranges for proxy recorder and service virtualization on private locations or configuring static endpoints, API configuration, and port range limitations.

### Overview

When using Service Virtualization or the proxy recorder on a Private Location, sometimes limiting the port range that is open to the virtual service or proxy recorder is necessary. Every virtual service uses its own port, so consider that defining a port range limits the number of virtual services that you can create and run on a particular agent.

Port range configuration allows you to:
- Set custom port ranges for proxy recorder
- Configure static endpoints
- Manage port allocation
- Optimize resource usage
- Limit the number of virtual services that can run on an agent

### Static Endpoints for Service Virtualization

This behavior only applies to transaction based virtual services on Docker-based agents.

If a transactional virtual service is stopped and re-deployed on a Docker Private Location, the same port number will be reused when possible. If the port is not available and taken by another process on the Agent host, the virtual service finds a new port from the allowed port range of the Agent and uses that. In this case, the notification message indicates that the end point has changed.

### Set a Custom Port Range

The following API lets you to limit the range of ports available on a specific agent:

**URL:**
```
https://a.blazemeter.com/api/v4/private-locations/<LOCATION_ID>/ships/<AGENT_ID>
```

**Request Parameters:**

| Parameter | Description |
|-----------|-------------|
| API Key | [Identifies the user (--user 'id:secret' ). How to get the API Key?](https://help.blazemeter.com/docs/guide/administration-api-keys.html) |
| Patch Body | "portRange" is the only parameter needed |
| LOCATION_ID | The ID of the Private Location. [How to get I get the Harbor ID?](https://help.blazemeter.com/docs/guide/private-locations-harbor-id-and-ship-id.html) |
| AGENT_ID | The ID of the agent within the Private Location. [How to get the Ship ID?](https://help.blazemeter.com/docs/guide/private-locations-harbor-id-and-ship-id.html) |

**cURL Example:**
```bash
curl -X PATCH https://a.blazemeter.com/api/v4/private-locations/<LOCATION_ID>/ships/<AGENT_ID> \
  -H "Content-Type: application/json" \
  --user 'id:secret' \
  -d '{"portRange":"2000-2500"}'
```

**Example PATCH Body:**
```json
{
  "portRange": "2000-2500"
}
```

### Configuration Steps

1. **Get Location and Agent IDs**: Obtain LOCATION_ID (Harbor ID) and AGENT_ID (Ship ID) from your Private Location
2. **Get API Key**: Obtain your BlazeMeter API key (id:secret format)
3. **Set Port Range**: Use the PATCH API to set the port range (e.g., "2000-2500")
4. **Verify Configuration**: Check the response to confirm the port range was set

### Port Range Considerations

- **Range Size**: Set appropriate port range size (e.g., "2000-2500" provides 500 ports)
- **Port Conflicts**: Avoid port conflicts with other services
- **Static Endpoints**: Configure static endpoints for specific services (transactional virtual services on Docker-based agents)
- **Limitations**: Be aware that defining a port range limits the number of virtual services that can run on an agent
- **Reuse**: Transactional virtual services will reuse the same port when possible

### Best Practices

- Use appropriate port ranges (consider how many virtual services you need)
- Avoid conflicts with system ports (use ports above 1024)
- Document port range configuration
- Test port range settings
- Consider that each virtual service uses its own port

---

## Documentation References

For detailed information about Proxy Recorder, use the BlazeMeter MCP help tools:

**Creating Proxy Recorder**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `recorders-creating-the-proxy-recorder`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-creating-the-proxy-recorder"]}`

**Recording Session**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `recorders-recording-your-session`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-recording-your-session"]}`

**Device Configuration**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**:
  - `recorders-configure-chrome-for-proxy-recording` (Chrome)
  - `recorders-configure-firefox-for-proxy-recording` (Firefox)
  - `recorders-configure-apple-devices-for-proxy-recorder` (Apple)
  - `recorders-configure-android-devices-for-proxy-recording` (Android)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-configure-chrome-for-proxy-recording", "recorders-configure-firefox-for-proxy-recording", "recorders-configure-apple-devices-for-proxy-recorder", "recorders-configure-android-devices-for-proxy-recording"]}`

**Using the Other Certificate**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `recorders-using-the-other-certificate`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-using-the-other-certificate"]}`

**Setting Port Range**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `recorders-setting-port-range-on-your-agent`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-setting-port-range-on-your-agent"]}`

