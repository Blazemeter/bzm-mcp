# Chrome Extension Recorder

## The BlazeMeter Chrome Extension

The [BlazeMeter Chrome Extension](https://chrome.google.com/webstore/detail/blazemeter-the-continuous/mbopgmdnpcbohhpnfglgohlbhfongabi) is a free tool that enables you to **Record**, **Upload**, and **Run** test scripts for your web applications. The Chrome Extension supports recording JMX, JSON or YML files, for running in [JMeter](https://www.blazemeter.com/solutions/jmeter), [Taurus](https://gettaurus.org/), or [BlazeMeter](https://www.blazemeter.com/signup), as well as both JMeter and [Selenium](https://www.selenium.dev/) scripts, automatically and simultaneously.

**Use when**: Recording performance and functional tests using the BlazeMeter Chrome Extension, creating JMeter and Selenium scripts automatically, or running tests without installing JMeter or Selenium locally.

### Overview

The BlazeMeter Chrome extension records all HTTP/S requests that your browser sends while you interact with your web application. From the recording, it creates a JMeter or Selenium script and uploads it to BlazeMeter, where you can browse scripts and execute them with a single click.

Using the BlazeMeter extension means you can run JMeter and Selenium scripts without even having these tools installed! No need to install JMeter or Selenium to record or run a performance test, the BlazeMeter Chrome extension creates the script on its own.

### Running Your Scripts in BlazeMeter

The BlazeMeter Chrome extension records all HTTP/S requests that your browser sends while you interact with your web application. From the recording, it creates a JMeter or Selenium script and uploads it to BlazeMeter, where you can browse scripts and execute them with a single click.

### Running Your Scripts Locally

Alternatively, if you have JMeter installed, you can always convert your recording into a JMeter JMX file or Taurus YAML file, then edit or run it via your browser or on your local computer.

**Note**: The extension needs to be able to communicate with blazemeter.com in order for the recording to be converted into a script.

### Key Features

- **Record Performance Tests**: Create JMeter scripts by recording browser interactions
- **Record Functional Tests**: Create Selenium scripts automatically
- **Synchronized Recording**: Record both JMeter and Selenium scripts simultaneously
- **No Installation Required**: Run tests without installing JMeter or Selenium locally
- **Multiple Export Formats**: Export as JMX, JSON, or YAML files
- **Direct Upload**: Upload and run tests directly in BlazeMeter
- **Script Editing**: Edit scripts before uploading or running

### Installation

1. Install the [BlazeMeter Chrome Extension](https://chrome.google.com/webstore/detail/blazemeter-the-continuous/mbopgmdnpcbohhpnfglgohlbhfongabi)
2. Record your actions, then play them back as a script
3. For more information, see [Chrome Extension - Record](#record)

### FAQ

**Q: Do I need to pay to use the extension?**  
**A:** The BlazeMeter Chrome Extension is free to use for as long as you like.

**Q: Do I need a BlazeMeter account to use the extension?**  
**A:** A BlazeMeter account is required to convert the recording into a JMeter script (.jmx) file because this process is performed on the server side. Any BlazeMeter account (free or paid) will suffice. [Signing up for BlazeMeter](https://www.blazemeter.com/signup) is super fast and doesn't require any sort of commitment or credit card.

**Q: How does the recorded script handle cookies?**  
**A:** The script will use cookie values from the original recording, though any new cookie values passed back by the server will override the values used in the original recording. (You can disable this behavior in the advanced settings.)

**Q: What is the minimum version of Chrome that is required?**  
**A:** Version 58 if you want to use all the features (e.g. recording transactions)

**Q: How does the recorder handle Web Components, such as Salesforce Lightning Web Components?**  
**A:** The BlazeMeter Chrome Extension supports recording web applications that contain Web Components. Shadow Roots encapsulate the internals of your Web Components out of reach of standard JavaScript selectors. However, the Chrome Recorder's ShadowRoot selector type is able to find elements inside Web Components, and the Recorder can detect and record [test actions](https://help.blazemeter.com/docs/guide/functional-taurus-actions-scriptless.html) (such as `type` or `click`) across Shadow Root boundaries. Note: When you are recording a Salesforce Lightning app with synthetic Shadow DOMs, slots are not supported; the Recorder records and replays the test normally, but replay fails later in Taurus.

### Documentation References

For detailed information about the BlazeMeter Chrome Extension, use the BlazeMeter MCP help tools:

**The BlazeMeter Chrome Extension**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `recorders-blazemeter-chrome-extension`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-blazemeter-chrome-extension"]}`

---

## Record

Record performance and functional tests using the BlazeMeter Chrome Extension, including advanced options, multi-tab recording, and script editing.

**Use when**: Recording performance and functional tests using the BlazeMeter Chrome Extension or using advanced options, multi-tab recording, and script editing.

### Overview

The [BlazeMeter Chrome Extension](https://help.blazemeter.com/docs/guide/recorders-blazemeter-chrome-extension.html) allows you to test your web application without prior scripting knowledge, by recording user actions and HTTP requests to create a unique test artifact that runs both JMeter and Selenium tests.

Recording a test with the Chrome extension is one way to create Objects for the [Test Action Library](https://help.blazemeter.com/docs/guide/functional-test-action-library.html) when you [Create Scriptless GUI Functional Tests](https://help.blazemeter.com/docs/guide/functional-create-scriptless-test.html).

**This article covers the following topics:**
- [Record Mode](skill-blazemeter-recorders://references/chrome-extension.md) [Advanced Options](skill-blazemeter-recorders://references/chrome-extension.md)
- [How to Record a Test](skill-blazemeter-recorders://references/chrome-extension.md) [How multi tab recording for Selenium scripts works](skill-blazemeter-recorders://references/chrome-extension.md)
- [BlazeMeter Script Editor](skill-blazemeter-recorders://references/chrome-extension.md)
- [How to Download the Recording](skill-blazemeter-recorders://references/chrome-extension.md)

The extension supports:
- Browser-based test recording
- Multi-tab recording
- Advanced recording options
- Script editing and refinement
- Recording both performance and functional tests in parallel

### Record Mode

This mode automatically records performance and functional tests in parallel, and creates both JMeter and Selenium scripts that run locally or directly on BlazeMeter.

First, let's review the recording options available when you open the extension:

- **ENTER THE NAME OF THE TEST** - Type the desired name of your test in this required field.
- **Start recording** - Starts recording both HTTP(s) requests and Selenium actions for the test
- **Stop recording** - Stops recording the test
- **Reset all options** - Resets everything, discarding any recording and settings, and reverting the menu to its default state as it was when you first opened it
- **Run** - This button is first disabled and is enabled after you have stopped the recording. Click it to choose how to upload and run the script on BlazeMeter:
  - Performance Test
  - API Functional Test
  - GUI Functional Test
  - End User Experience Monitoring
- **Edit** - This button is first disabled and is enabled after you have stopped the recording. Use the JMeter Editor in case you need make small fixes before uploading the script
- **Save...** - This button is first disabled and is enabled after you have stopped the recording. Choose as what type of script you want to download the recording:
  - Taurus YAML of JMeter & Selenium - for Load tests and UX tests combined
  - Selenium only - for UX tests only
  - JMX - for Load tests only
- **Save in Project...** - Before you run or save the recording, select the BlazeMeter account, project, and workspace, where you want to save the test

### Installation

1. **Install Extension**: Install BlazeMeter Chrome Extension from Chrome Web Store
2. **Sign In**: Sign in to your BlazeMeter account (verify that you see the "Hi [username]" greeting in the upper right-hand corner)
3. **Configure Settings**: Configure extension settings as needed
4. **Start Recording**: Begin recording browser sessions

### How To Record a Test

By default, every test step you perform is being recorded to a "Test Case", and it will be a monolithic script with a sequence of actions. On the JMX level, this will simply create a thread group consisting of these actions. The recorder, in fact, treats each step as a single transaction controller, so if you prefer, you may rename the label, and add additional labels to group subsequent actions under their own transaction controllers.

**Steps:**
1. Click the BlazeMeter icon in your Chrome browser toolbar
2. Log in to your BlazeMeter account if you haven't already. Verify that you see the "Hi [username]" greeting in the upper right-hand corner to confirm that the plugin is logged in
3. Give your test a name
4. (Optional) Expand and configure advanced options, or use the defaults
5. Click the **Start recording** button. The UI will change to show your yet-to-be-performed first steps. Note that on the right-hand side, there is a UI column that starts counting at 2, and a JMX column that starts counting at 0
6. Perform the actions in your application that you wish to simulate in your test. For example, browse to a site, click on a selection, fill out a form, submit the form. Note that as you do so, the UI count increases to reflect UI actions that you performed on a user-level. The JMX count increases to reflect how many items are created within the performance script to do the same
7. (Optional) Rename a segment by clicking the label. Or type in a name, then click **Save** to create a new label under which to group sets of subsequent actions for readability later
8. Use the **Pause recording** button at any time you need to pause the recording. The button will change to **Record** so that clicking it a second time will unpause, resuming the recording
9. While the recording is paused, you can select and right-click any element on your webpage to add assertions as test steps. When you add an assertion, the UI count increments by one. Only add assertions while the test is paused, else the recorder will also record the clicks you have performed to open the context menu
10. When finished, click the **Stop recording** button
11. Download, edit, or run the test in the cloud

**Note:** The UI count and JMX count will often not match. This is because what might take a human multiple mouse-clicks (go to URL, expand the menu, selection option, click submit button) may translate into fewer, simpler actions to the machine (a GET followed by a POST), or the opposite, where just one user-action can cause multiple requests.

**Note**: By default, every test step you perform is being recorded to a "Test Case", and it will be a monolithic script with a sequence of actions. On the JMX level, this will simply create a thread group consisting of these actions. The recorder, in fact, treats each step as a single transaction controller, so if you prefer, you may rename the label, and add additional labels to group subsequent actions under their own transaction controllers.

### How Multi-Tab Recording for Selenium Scripts Works

When recording a Selenium scenario, the BlazeMeter Chrome extension takes into account the following scenarios:

- **When you open a new tab**: The Chrome Extension adds an "openWindow" action to your script recording with the default new tab URL of Chrome. The Chrome Extension remembers this tab and the focus of recording switches to this tab using the "selectWindow" command
- **When you switch to an existing tab**: The "openWindow" action is recorded together with the current URL of that tab. The Chrome Extension remembers this tab and the focus of recording switches to this tab using the "selectWindow" action
- **When you close a tab**: The "close" action is recorded, then the browser automatically switches to another existing tab. Then it follows the described behavior for switching to existing tabs
- **When you switch between tabs** that have already been part of the recording: The Chrome Extension does not add another "openWindow" action because it recognizes the tab. Instead, only the "selectWindow" action is added to the recording

### Advanced Options

These Advanced Options are specific to HTTP(S) calls. Scroll down to view all options in this section.

- **User Agent** - Select your preferred User Agent, meaning, which device or browser your users are using. This selection adds a "User-Agent" header to the requests, and it allows you to emulate various situations, such as a user browsing via a mobile device
- **Filter Pattern** - By default, requests are not filtered (the asterisk include all domains and paths). By modifying the [match pattern](https://developer.chrome.com/docs/extensions/mv3/match_patterns/) in this field you can change which requests your recording includes. For example, you likely do not wish to record your Gmail, Facebook, or even BlazeMeter traffic. Typically you use this option to restrict requests to only one domain. You'll be presented with the option to select which domains to include and exclude before the test actually runs. Default: `http://*/*, https://*/*`. Format: Refer to [Google's guide on creating match patterns](https://developer.chrome.com/docs/extensions/mv3/match_patterns/)
- **Disable Browser Cache** - Disables the browser cache during the recording. This option is important since cached objects are not recorded
- **Wipe Service Workers** - Removes the service workers of the page every time you navigate to another page while recording
- **Record AJAX Requests** - Enable this option if the site uses AJAX which needs to be included in the recording
- **Update Settings Before Running Test** - Enable this option to change test settings before running. Through the BlazeMeter interface, you can control properties such as ramp-up time, test duration, load distribution between engines, and much more
- **Randomize recorded think times** - Enable this option to use a uniform random timer to simulate the expected delayed response time of a real service or human user
- **Requests to Record** - Lets you control how BlazeMeter handles embedded objects on the page, such as images, CSS, and JavaScript files:
  - **Only Top-Level Requests** - If selected, the recorded script will not include requests for referenced objects. When the JMeter script is executed, it will parse the HTML file and send requests for all referenced objects
  - **Parallel Number of Downloads** - For each browser, enter a number of downloads that are allowed to run in parallel
  - **Top Level Requests and the Following** - This option offers a selection of objects that can be included. The recorded JMeter script will include requests for referenced objects. When executed, the script does not parse the HTML file and likewise does not send requests for referenced objects
- **GUI Functional Test Options**:
  - **Export ID Locators** - If the identifiers in your user interface are static, enable this option. This is the default. Examples of such locators of DOM elements are "ID a1234567" or "Xpath div[id=a1234567]". If identifiers in your user interface may be regenerated and are not uniquely reliable for use in test scripts, disable this option. Disabling this option excludes ID locators from the recording. The option is applied as long as you enable it before you export and run the script in BlazeMeter, meaning, you can still enable it after recording
  - **Allow Context Clicks to be recorded** - By default, this option is disabled and the recording does not contain right mouse button clicks right before assertions; this is to exclude clicks where the tester is using the Chrome extension's context menu to add an assertion. If you want these right clicks to be recorded, enable this option

### BlazeMeter Script Editor

Instead of downloading the recording as-is, you may wish to further edit your script. You have the following options:
- Load Testing: Edit your script for JMeter
- Functional Test: Edit your script for Selenium

**Load Testing: Edit your script for JMeter:**
Click this option and you'll see a new tab open to display the JMeter script editor.

- Use the topmost three buttons to select in which format to export your script:
  - Taurus YAML file
  - Taurus JSON file
  - JMeter JMX file
- Use the buttons in the red bar to perform the following tasks:
  - Expand all fields or collapse all fields
  - Sort the contents
  - Filter the contents (In the filter, enter a JMESPath query to filter, sort, or transform the JSON data, and preview it)
  - Undo a change or redo a change
- To the left of each item is a handle button that you can click and drag to move the item up or down in the script
- Next to the handle is a button that opens a menu for customizing your script
- Lastly, use the play button in the upper-right corner to run your edited script in BlazeMeter

### How To Download the Recording

After your script is recorded, you can choose to click **Save...** in the Chrome extension to download a copy of the recording.

You will be prompted to select the desired type of the exported recording:
- A Taurus YAML script containing both, JMeter and Selenium tests
- A Taurus YAML script consisting of only a Selenium test
- A JMeter-only JMX script

If you selected additional options for **Requests to Record** earlier, you will be prompted to select additional options pertaining to which domains to include in the exported script.

### Best Practices

- Clear browser cache before recording
- Use incognito mode for cleaner recordings
- Filter out unnecessary requests
- Review and edit scripts after recording
- Test recorded scripts before production use

---

## Changelog

Track changes and updates to the BlazeMeter Chrome Extension, including new features, bug fixes, and version history.

**Use when**: Tracking changes and updates to the BlazeMeter Chrome Extension or reviewing new features, bug fixes, and version history.

### Overview

The Chrome Extension changelog documents all updates, improvements, and fixes to the extension. It helps you:
- Stay informed about new features
- Understand bug fixes and improvements
- Track version history
- Plan for updates

### Recent Versions

**Latest Version: 6.6.0 (2024-09-02)**
- Added an option for Browser Performance Tests, enabling users to run tests directly

**Version 6.5.9 (2024-09-17)**
- Removed the contextClick action before registering any assertions

**Version 6.5.8 (2024-09-12)**
- Refined XPath locators for improved reliability

**Version 6.5.7 (2024-09-06)**
- Removed all Mixpanel API code and updated internal packages

**Version 6.5.6 (2024-08-30)**
- Fixed glitches that prevented the extension from remaining active during installation
- Resolved an issue where the Chrome Plugin crashed due to inactivity or while recording operations with long fetch times

**Version 6.5.5 (2024-08-23)**
- Fixed an issue where certain network requests were not recorded

**Version 6.5.2 (2024-07-20)**
- Resolved an issue where the Chrome plugin would latch onto the webpage after rapid reloading

**Version 6.5.0 (2024-07-09)**
- Fixed an issue causing the Chrome plugin to crash after a few minutes of inactivity
- Addressed a problem with recording duplicate network requests

### Key Features by Version

**Version 6.0.0 (2023-07-14)**
- Fix: Object Picker Issue
- Remove: Selenium option from Edit button dropdown
- Upgrade: from manifest 2.0 to manifest 3.0

**Version 5.0.0 (2021-11-26)**
- Change: Perforce rebranding
- Fix: iframes order when recording
- Fix: same-origin errors when handling iframe locators

**Version 4.9.0 (2020-04-23)**
- Add: remote debugging experience
- Add: new commands support (WaitFor, StoreEval, AssertEval, AnswerDialog, AssertDialog)
- Add: "if/then/else" control block
- Add: "for" loop support
- Add: "foreach" loop support

**Version 4.0 (2018-06-18)**
- Functional test case record and playback capabilities
- Unification of single recording using both approaches, where test case can be downloaded as Selenium and/or JMeter
- Added merged (2 in one) YAML scenarios enabling to run in parallel both Selenium and JMeter scripts

### Accessing Changelog

- **Extension Settings**: View changelog in extension settings
- **Release Notes**: Check BlazeMeter release notes
- **Version History**: Review version history for changes
- **Help Documentation**: Access changelog from help.blazemeter.com

### Version Information

- **Current Version**: Check current extension version
- **Update Notifications**: Receive notifications for updates
- **Compatibility**: Verify compatibility with BlazeMeter platform

### Best Practices

- Regularly check for extension updates
- Review changelog before updating
- Test extension after updates
- Report issues or feedback

---

## Documentation References

For detailed information about Chrome Extension recorder, use the BlazeMeter MCP help tools:

**Chrome Extension Record**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `recorders-chrome-extension-record`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-chrome-extension-record"]}`

**Chrome Extension Changelog**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `recorders-chrome-extension-changelog`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["recorders-chrome-extension-changelog"]}`

