# Supported Browsers

## Supported Browsers

Understand browser support for GUI Functional Testing, including version groups (actual, deprecated, unsupported), browser selection, and Safari WebKit engine support.

**Use when**: Understanding browser support for GUI Functional Testing or selecting browsers and understanding version groups and Safari WebKit engine support.

### Overview

In BlazeMeter, we support the last six versions of Firefox, Chrome, Microsoft Edge, and [Safari](https://help.blazemeter.com/docs/guide/functional-supported-browsers.html#h_01FPDNF45QZBK7GTD42KC17Z3Z) browsers.

### Browser Selection in Test Creation

When you create a GUI Functional test, in the "Browser Selection" section you may select the browsers and versions you need.

The best practice is to select the default browser version. In such case, you will not need to update the browser version each time we add a new version. As soon as we add a new version, your GUI Functional test will run on the latest available browser version in BlazeMeter.

By default, and if no location is selected, the test runs in the latest Chrome browser.

### Browser Selection in Private Location

If you using a Private Location, you'll need to enable the browsers at the *Functionalities* tab in the settings of your Location by selecting either the default browsers option, or by selecting specific browsers after choosing "Select version" option.

Even when you use a [Private Location with disabled AUTO_UPDATE](https://help.blazemeter.com/docs/guide/private-locations-how-to-enable-auto-upgrade-for-running-containers.html), selecting the default browser version for a test is still the best option - on test start we will use the latest available browser version you have installed on your Private Location.

**Note**: Private Locations are run behind your corporate firewall and assigned to Workspaces. BlazeMeter's default behavior is to run a test against an execution engine in the cloud, unless you configure the test explicitly to run on a Private Location.

### Browser Versions Groups

We have three groups of browser versions:
- actual
- deprecated
- unsupported

### Actual

The last 3 versions of browsers.

Although we encourage you to always use the default browser version, you may have a specific use case with a requirement to have some exact browser version selected for your GUI Functional test.

### Deprecated

The last 4-6 versions of browsers.

If you have such a version selected for your GUI Functional test, we will show deprecation warnings both inside the GUI Functional test and inside the Test Report.

You will still be able to run the test but be prepared to upgrade the browser to a more recent version before the browsers becomes outdated and unsupported.

### Unsupported

All the versions below the last six versions.

In case you have an unsupported version selected in a GUI Functional test, you won't be able to run such a test until you have the browser version updated to a more recent one.

### Note on Safari Browser Support

Safari browser can run only in the Apple ecosystem. BlazeMeter uses custom Linux images with lightweight WebKit engine installed to enable GUI functional testing with Safari browser. From web applications functional testing perspective, the only difference with the real Safari browser is that fonts might differ.

| Browser | WebKit engine version |
|---------|----------------------|
| Safari 14 | 610.4.3.1.7 |
| Safari 15 | 613.1.6.1 |

---

## Documentation References

For detailed information about supported browsers, use the BlazeMeter MCP help tools:

**Supported Browsers**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-supported-browsers`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-supported-browsers"]}`

