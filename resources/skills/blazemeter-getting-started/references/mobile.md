# Mobile Testing

## Testing Mobile Sites and Apps

Guide for testing mobile sites and apps with BlazeMeter, including mobile-specific configurations, testing strategies, and best practices.

**Use when**: Testing mobile sites and apps, configuring mobile-specific test settings, or implementing mobile testing strategies.

### Overview

Irrespective of the mobile OS (Android or iOS) or app type (native, web, or hybrid), BlazeMeter is the tool for performance and functional testing.

You have two options, you can use BlazeMeter's network emulation for performance tests, or Codeless Automation integration for functional tests of mobile apps.

### Test Mobile Performance

BlazeMeter provides real world performance testing of mobile web sites and mobile apps:

1. **Record your mobile scenario** using BlazeMeter's [Chrome Extension](https://help.blazemeter.com/docs/guide/recorders-blazemeter-chrome-extension.html) or [Proxy Recorder](https://help.blazemeter.com/docs/guide/recorders-creating-the-proxy-recorder.html)
2. **[Upload](https://help.blazemeter.com/docs/guide/performance-scenario-definition.html) the recorded script** to BlazeMeter when you are done
3. **Enable the [Network Emulation](https://help.blazemeter.com/docs/guide/performance-network-emulation.html) feature** and either select the network type to emulate, or set your own parameters
4. **Run the performance test**
5. **Perform result analysis** using the BlazeMeter test report, beginning with the [Summary Report](https://help.blazemeter.com/docs/guide/performance-summary-report.html)

**Note**: Network emulation allows you to simulate different network conditions (bandwidth, latency) that mobile users might experience, making your performance tests more realistic.

### Test Mobile Functionality

To test mobile web sites, use BlazeMeter [GUI Functional Tests](https://help.blazemeter.com/docs/guide/functional-create-scriptless-test.html).

To test mobile apps, run your tests on real or virtual devices such as [Perfecto Android emulators and iOS simulators](https://www.perfecto.io/platform/mobile-emulators-simulators). For more information on mobile app testing, see [Perfecto 101 on Perforce Education](https://training.perfecto.io/learn/courses/518/perfecto-101).

**Note**: BlazeMeter supports testing of mobile apps regardless of the mobile OS (Android or iOS) or app type (native, web, or hybrid). You can use network emulation for performance tests or Codeless Automation integration for functional tests of mobile apps.

---

## Documentation References

For detailed information about mobile testing, use the BlazeMeter MCP help tools:

**Testing Mobile Sites and Apps**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `getting-started-testing-mobile-sites-and-apps`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["getting-started-testing-mobile-sites-and-apps"]}`

