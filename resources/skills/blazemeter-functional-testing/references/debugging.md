# Debugging Functional Tests

## Debug Best Practices

Debug scriptless GUI Functional Tests using best practices, including local debugger, breakpoints, Chrome DevTools, error analysis, and common troubleshooting scenarios.

**Use when**: Debugging scriptless GUI Functional Tests or using local debugger, breakpoints, Chrome DevTools, and error analysis.

### Introduction

The aim of this guide is to provide guidance on how to debug errors encountered during testing with BlazeMeter Scriptless. The Scriptless editor lets you easily create and execute GUI Functional tests without coding. You can record tests using the BlazeMeter Chrome Extension, or create them directly on the BlazeMeter Cloud platform.

There are several ways to debug tests within BlazeMeter, through the BlazeMeter Recorder Chrome Extension, through the debugger built into the BlazeMeter platform, and through the test execution report results. We will go through each of these in this guide.

Common errors in BlazeMeter tests can be in the following categories:

1. **Errors with test execution** - The test doesn't execute at all, no results are returned (empty report), unavailable infrastructure to run the tests
2. **Issues with locating elements** - An Object (a.k.a. element) cannot be found on a page, locators are incorrectly defined
3. **Errors with test data** - Problems with the CSV file structure or definition, data not comma-separated, data cells containing commas not in quotation marks, csv file does not have the csv suffix, data referenced but not properly defined, variables not properly being referenced (variable syntax)
4. **Errors due to test definition** - Issues executing custom code which is malformed, issues interacting with a dialog window that hasn't appeared yet, etc.
5. **Assertions/Test Failures** - Assertions fail because the application is not working as it should (this means, the test discovered a bug!)

### Errors With Test Execution

BlazeMeter uses container-based test execution engines to run the tests. These executors are spun up at the execution of each test, and destroyed upon completion. This means that every test runs on a clean browser image - there is nothing in the browser cache at the start of each test. It also means that the test execution engines will not have any remembered (cached) login information, nor is the execution engine running as a logged-in user on a network.

For instance, if NTLM authentication is used (which relies on a user being logged in to Windows as an AD user), an alternative authentication mechanism is needed, since the OPLs from where your tests run are *not* on a Windows machine logged-in as a specific AD user.

Test executions can be either cloud based, [Private Location](https://help.blazemeter.com/docs/guide/private-locations-use.html) based, or locally executed. Private Locations are run behind your corporate firewall and assigned to Workspaces. BlazeMeter's default behavior is to run a test against an execution engine in the cloud, unless you configure the test explicitly to run on a Private Location. Regardless of the Location defined in the test (cloud or Private Location), you can always use the built-in test *debugger* to locally run the test on your machine for a quick feedback loop and the ability to step through your test with breakpoints, etc.

If your test failed to run:

1. Ensure you are in the correct BlazeMeter Account and Workspace
2. If your application under test is behind the corporate firewall, make sure the test is configured to run on a Private Location which can access your application. If the cloud engines have been allowlisted by your organization, then they may be able to access your application - verify this with your sys admins.
3. Before running a test, ensure you have set the test execution Location in the test Configuration (located below the test steps editor)
4. Verify that you have selected the appropriate browsers and versions for the test execution in the test Configuration. You can define multiple entries for the same browser with different versions
5. Verify the status of the Private Location, if you are using one.
6. Verify network connectivity, if you are executing tests in the public cloud.

If the application instance which you are trying to test is not accessible outside your company network (intranet only), the cloud engines cannot reach your application.

- Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**.
- To view the status of your Private Location, expand the Workspaces section in the left side menu, click Private Locations, and choose your Private Location. The "Agents" section displays the running engines which are being used for current test executions, allowing you to determine if all engines are busy or not.

You can determine the number of running sessions on a given Private Location, for a given Agent, by using the following Blaze API call:
```
GET /private-locations/${lcoationId}/servers/${agentId}
```

In the result, get the length of the `result.containerStatuses` attribute to obtain the number of running sessions. You could aggregate the results of all Agents (if there are more than one) under a given Private Location (harbor) to get the full count for a given Private Location.

## Debugging Scriptless GUI Functional Tests

The Scriptless editor has a built-in local debugger, separate from the GUI Functional Test Debugger. Developers use debuggers to step through and troubleshoot broken tests.

**Use when**: Debugging scriptless GUI Functional Tests interactively, stepping through test scenarios, troubleshooting broken tests, or using breakpoints to pause execution.

### How to Interactively Debug a Scriptless Scenario Locally

1. Go to the Functional Tab, open the broken Test and go to its Configuration tab
2. Turn the local debugger on. Now the **Play** button is enabled
3. (Optional) Click **Toggle Breakpoint** on steps where you want to pause execution to troubleshoot
4. Click the **Play** button to start the debugger. The Play button turns into a **Pause** button
5. Wait for the debugger to open in a new browser window
6. Resize or move the BlazeMeter window and the Debugger window, so you can see both
7. Watch how BlazeMeter executes the test scenario and color-codes the debug results:
   - A green checkbox marks a step that has been executed
   - A yellow edge marks a step that is being executed
   - A green edge marks a step that has completed
   - A red edge and red exclamation mark marks a step that has failed
   - The colored marks are reset when you click Play or Stop
   - Hover over Info symbols to read warnings and informational messages, for example, if the first locator was not found, and secondary etc. locator was used instead
8. Click **Stop** to close the debugger

### How to Use Breakpoints

If you have set a breakpoint on a step, it means that execution pauses there, so you can investigate.

In your investigation, you can modify steps while the debugger is running. When you reach a breakpoint, you can modify the executed step, or any step after it. You can also modify steps before the breakpoint, but that won't affect this run of the debugger.

Click **Play** anytime to continue execution after pausing at a breakpoint; or click **Stop** to close the debugger.

Additionally, you have the following options when pausing at groups, loops, and if/else blocks:
- **Step In** - Step into the group, loop, or if/else block, and pause again
- **Step Over** - Execute the group, loop, or if/else block, and pause again
- **Step Out** - Step out of the current group, loop, or if/else block, and pause again

### Interactive Variable Editing

You can interactively edit variable values while the local debugger is running. Left-click the blue highlighted variable name to open the inline editor.

---

### Debugging Using the Local Debug Option on the BlazeMeter Platform

For the official documentation of this feature, see [Debugging Scriptless GUI Functional Tests](skill-blazemeter-functional-testing://references/debugging.md).

The local debugger is a great option for debugging a test on the BlazeMeter platform. It will run the Scriptless test locally on your machine. Once you have a test created or imported, the Debug option is available. Toggle the Debug switch at the top of the test Configuration page to turn on the debugger.

**Note**: Regardless of the Location defined in the test (cloud or Private Location), you can always use the built-in test *debugger* to locally run the test on your machine for a quick feedback loop and the ability to step through your test with breakpoints, etc.

The local debugger allows you to Play, Stop, Step Into, Step Over, and Step Out.

- **Play** - Start or Resume the test
- **Stop** - Halt the test execution
- **Step In** - Step into the group, loop, or if/else block, and pause again, OR if the next step is a normal test step, this will simply execute the next step and pause again
- **Step Over** - Execute the group, loop, or if/else block, and pause again
- **Step Out** - Step out of the current group, loop, or if/else block, and pause again

Each individual test step has debugging options specific to that particular step. Toggle Breakpoint, Execute Step and Disable Scenario Step are available as far as step-level debugging options, and these will be displayed when you have Debug mode enabled (otherwise, you won't see them) and are hovering over an individual step.

- **Disable Scenario Step** - Can be used to skip over test steps that are working correctly and are not required for the execution of the failed test step.
- **Toggle Breakpoint** - Can be used to mark a given step such that during Local Debug execution it will pause once it gets to that step until you manually resume the test (by pressing Play).
- **Execute Step** - Will immediately execute the selected step. This allows you to move the current execution ahead of where it currently is (thus skipping steps) which can be very useful. Once you use this option to execute a given step, you can then press the Play button at the top and the test will resume executing right after the step you just manually executed.

When Local Debug is enabled, test steps now have the additional context options described above.

To start debugging, simply hit the Play button once you have enabled the Debug toggle. After enabling the Debug toggle, you can first set breakpoints at individual test steps where you want the execution to pause. Once you have set the breakpoints you want, simply hit the Play button. The debugger will pause on the first breakpoint it gets to, and wait until you resume playback (again, via the Play button).

Local Debug execution currently paused on a breakpoint: Notice the black arrow on the right of the test step, which denotes the debug execution is currently paused on that step. To resume, you can simply press play - or you can use any of the "Step..." buttons (for example, Step Over).

A useful workflow for debugging a wide variety of issues is to set breakpoints at points in the test where it may be useful to examine the state of the page via Chrome Dev Tools. When the debugger is paused on your breakpoint, you are free to switch to the window where the test is being executed, press F12 to open dev tools, and then inspect the HTML on the Elements tab, and utilize the Console to execute Javascript commands. The former is a good way to debug issues with element locators, and the latter is a good way to validate custom code snippets work as intended in the exact place where they would be executed during the test (see "Debugging Custom Code Snippets" section for details).

**Note**: Notice the black arrow on the right of the test step, which denotes the debug execution is currently paused on that step. To resume, you can simply press play - or you can use any of the "Step..." buttons (for example, Step Over).

### Debugging Failed Reports on BlazeMeter

When a test is executed on the BlazeMeter platform, a report is created that indicates the results of the test execution. The results will show whether the test passed or failed. They can also show broken or undefined, if there was an issue running the test itself. For more details on the test status, see [Test Result Meanings](https://docs.google.com/document/d/1NB4NcQW-7h08NCnBbfezI5n8mcfdq1JQsc7awSmPBCM/edit#heading=h.2b4czxur5xw).

To find out why a test failed, click on the details tab. The right hand pane shows the steps executed for the test. The failure reason will be flagged in a banner at the top.

Clicking on the error moves to the step where the error failed, and moves the test video to the location of the error. This lets you see what is happening on the application at the moment of the error. You can verify whether all of the expected elements are loaded and available on the page.

Sometimes there will not be enough information to know why the test failed. In this case, it is helpful to check the available logs. Go to the Advanced Logs section by performing the following steps:

1. Go to your test execution result/report missing data or with an error. You must be on the report page of a test or you will not have the option to view these advanced logs!
2. Open the Reports dropdown (top menu bar) and choose Show all reports.
3. In the left bottom corner under Sessions, select the session listed for your report (it will be the one with your test name).
4. Switch to Logs tab.
5. Select bzt.log from the Log dropdown.
6. Search for errors.

You can use Ctrl+F and search for "error", or manually scroll through the log, or download the artifacts.zip and view the aperitif.out log file.

If nothing is shown there, check the other files' logs next - switch to the Selenium session logs and view the driver logs.

Sometimes these errors will reveal an issue in the definition of your test. If it still seems like the issue is platform-related then it may be time to submit a support request. When reporting an issue, including any errors from these logs is imperative. You can download the entire log files and submit as an attachment to the ticket.

### Debugging Custom Code Snippets

1. Always author custom code snippets in an IDE like VSCode.
2. Once the snippet is to your liking, try running it in the Chrome DevTools console by pressing F12, going to Console tab, and then entering your code line by line and executing it against the live page to ensure it works as intended. For in depth tutorial on this, refer to: [https://developers.google.com/web/tools/chrome-devtools/javascript](https://developers.google.com/web/tools/chrome-devtools/javascript).
3. Once it works as intended, paste it into a custom code action (Script Eval, Store Eval, or Assert Eval) in your test on BlazeMeter.

### Cached Login Credentials Resulting in Inconsistent Executions

Local browser caching can result in login steps not being required during subsequent local debug executions since the authorization credentials are stored in your browser cache after the first login. This can adversely affect test executions because the test will try to perform the Login steps, but if the application skips the login page because credentials are cached, then the test will fail because it cannot perform the login steps (since a login page never showed up).

Also when you record the test locally, you may already be logged in to an application so it doesn't prompt you to login. Then when you run that test on a Private Location, it will fail because the first thing that happens is the remote executor is prompted with a login page, but there were no login steps recorded when you recorded locally so it will fail at this point.

Below are the best practices for solving this particular issue:

- **Always log out** first before recording locally **so that your login steps are also recorded**.
- **Work around playback issues with login/auth caching during Local Debug:** When the login steps fail because BlazeMeter is trying to log in during local execution, but the application skips the login page entirely, because your login credentials/authorization are cached, press "Execute step" (Play icon button) on the first step after the login steps. Then press the Play button at the top next to the "Debug" label, and the debugger will resume playback at that point. Alternatively you can mark the Login steps as "Disable Step" so that those steps do not execute during local debug playback. This way the test is still defined with the login steps, which would be required every time during Private Location/Cloud (non-local-debug) execution, and you can simply skip them during the Local Debug playback
- **An even more elegant solution which requires no manual intervention** would be to make a Group which has an If/Else Action that handles both scenarios: [if] you were already logged in, do nothing, *or* [else] you were not logged in, so enter credentials and submit login form.

### SwitchFrame Parameters

SwitchFrame command is used to switch between different frames (for example, iframes) on a given page. Nested frames can be complex to navigate from a test automation perspective, and in some cases it may be necessary to define the switching of frames yourself by making use of the different parameters you can provide to the SwitchFrame command, as described below:

- **"relative=top"** - Switches Webdriver context to the main page. This is usually performed when you're done with actions inside the frame and you need to switch back to the root page (which is sometimes called "default content").
- **"relative=parent"** - Switches 1 level up, either from nested frame to parent frame, or from frame to root page ("default content")
- **"index=0"** - Switches to the first frame from the context you are currently in. For example, if the page has 3 frames, you'll be switched to the first one. Or if you are already in frame, then you'll be switched to the first frame inside this frame (which would be a *nested* frame)
- **"index=n"** - Switches to *n*th frame

It may be useful to record a test with the recorder, debug the test via the recorder, and ensure the frame traversal is occurring properly. In some cases, there can be issues related to actions being performed too quickly in the test which can confuse the application under test and result in frames not being traversed to when they should be.

In these cases, you may need to introduce Pause actions for a few seconds between the triggering action (which causes frame to open and be traversed to) and the SwitchFrame action. Additionally, in some rare cases you may need to alter the SwitchFrame parameters (from what the recorder generated) in order to effect the desired frame traversal behavior in your test - although this is very rare as the recorder almost always captures the SwitchFrame parameters accurately.

### Test Result Meanings

Once finished executing, tests will have one of the following four statuses indicating the result of the test:

**Pass:**
The test executed to completion with no issues, and all Assertions (if any were defined) passed.

**Broken:**
This status is received when an exception occurs during the test execution. For example, NoSuchElement is an example of a common exception and the first course of action should be to validate that the element's locators are valid and that the element is in fact present on the page at this point in the test. Other exception types should also be investigated.

**Fail:**
When an Assertion within a test has failed. Usually indicates that the application under test may have an issue, or that the Assertion was improperly defined.

**Undefined:**
This status occurs when a test didn't (or couldn't) report its status. For example, the error occurred before the test has started (CSV parsing, and so on). Or the Private Location image with browser driver shut down unexpectedly. There are a wide variety of potential causes for Undefined status, but many of them stem from causes not related to the way the test is configured - but rather due to execution engine issues.

### Important Considerations

- The Debugger uses native JavaScript executed against the browser as its mechanism for page interaction, while the Private Location executors are using actual Selenium - this may result in some differences or inconsistencies between debugger/Private Location/cloud execution.
- As the Test Report becomes more closely aligned to the Scriptless Actions of your test, it will become even more important to have important/critical steps labeled with a description, Objects named properly, and test steps organized via Scenario Sections with descriptive names.

**Resources:**
- Scriptless Test Creation Basics: [Creating Scriptless Functional Tests](https://help.blazemeter.com/docs/guide/functional-create-scriptless-test.html)
- Scriptless Action Descriptions: [Taurus Actions for GUI Functional Testing](https://help.blazemeter.com/docs/guide/functional-taurus-actions-scriptless.html)
- Test Action Library: [Test Action Library](https://help.blazemeter.com/docs/guide/functional-test-action-library.html)
- GUI Functional Test Report: [GUI Functional Test Report](https://help.blazemeter.com/docs/guide/functional-gui-test-report.html)
- Blaze University: [https://university.blazemeter.com/dashboard](https://university.blazemeter.com/dashboard)

---

## Documentation References

For detailed information about debugging Functional Tests, use the BlazeMeter MCP help tools:

**Debugging Scriptless GUI Functional Tests**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-test-debug`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-test-debug"]}`

**Debug Best Practices**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-test-debug-best-practices`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-test-debug-best-practices"]}`

