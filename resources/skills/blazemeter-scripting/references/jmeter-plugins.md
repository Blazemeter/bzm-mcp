# JMeter Plugins

## Random CSV Data Set Config Plugin

Include non-standard JMeter plugins like Random CSV Data Set Config in BlazeMeter tests by uploading plugin JAR files.

**Use when**: Needing non-standard JMeter plugins in BlazeMeter tests or using custom JMeter plugins not included by default.

### Overview

BlazeMeter supports custom JMeter plugins that are not included by default. You can upload plugin JAR files to extend JMeter functionality in your tests.

While BlazeMeter automatically includes standard plugins that are typically available through JMeter's Plugin Manager, you must upload a few non-standard plugins with your test in order to run.

### Symptom: Plugin Not Found Error

If your JMeter script makes use of the Random CSV Data Set Config Plugin, you may find your test will fail to start when uploaded to BlazeMeter.

**Error Message:**
Download the logs from the **Logs** tab of your failed test report. View the jmeter-console.log and look for the following error:

**Note**: This error means that the JMeter instance install on the BlazeMeter test engine does not include the Random CSV Data Set Config plugin. While BlazeMeter automatically includes standard plugins that are typically available through JMeter's Plugin Manager, you must upload a few non-standard plugins with your test in order to run.

```
2019-01-23 18:00:46,298 ERROR o.a.j.JMeter: Error in NonGUIDriver
java.lang.IllegalArgumentException: Problem loading XML from:'/home/jmeter/Withdrawal_requests.jmx',
missing class com.thoughtworks.xstream.converters.ConversionException:
---- Debugging information ----
cause-exception : com.thoughtworks.xstream.converters.ConversionException
cause-message :
first-jmeter-class : org.apache.jmeter.save.converters.HashTreeConverter.unmarshal(HashTreeConverter.java:67)
class : org.apache.jmeter.save.ScriptWrapper
required-type : org.apache.jorphan.collections.ListedHashTree
converter-type : org.apache.jmeter.save.ScriptWrapperConverter
path : /jmeterTestPlan/hashTree/hashTree/hashTree/com.blazemeter.jmeter.RandomCSVDataSetConfig
line number : 58
version : 4.0 r1823414
-------------------------------
```

This error means that the JMeter instance install on the BlazeMeter test engine does not include the Random CSV Data Set Config plugin.

### Solution

In order to correct the error, upload the plugin JAR file along with your test, as you would any other test file, per the instructions found in [Uploading Files](https://help.blazemeter.com/docs/guide/performance-upload-files.html) and [Shared Folders](https://help.blazemeter.com/docs/guide/performance-shared-folders.html).

**Steps:**
1. **Get Plugin JAR**: Download or obtain the Random CSV Data Set Config plugin JAR file
2. **Upload to Test**: Upload JAR file to test configuration (as you would any other test file)
3. **Configure Plugin**: Configure plugin settings in test
4. **Test Plugin**: Verify plugin works correctly

### Random CSV Data Set Config Plugin

The Random CSV Data Set Config plugin allows you to:
- Randomly select rows from CSV files
- Use random data distribution
- Configure random selection parameters

### Configuration Steps

1. **Upload Plugin JAR**: Upload Random CSV Data Set Config plugin JAR file to your test
2. **Add Plugin Element**: Add plugin element to JMeter test
3. **Configure CSV File**: Set CSV file path
4. **Configure Random Selection**: Set random selection parameters
5. **Test Configuration**: Verify plugin configuration works

### Best Practices

- Use only trusted plugin sources
- Test plugins thoroughly before production use
- Document plugin usage and configuration
- Keep plugin versions updated

---

## Documentation References

For detailed information about JMeter plugins, use the BlazeMeter MCP help tools:

**Random CSV Data Set Config Plugin**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-jmeter-random-csv-data-set-config-plugin`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-jmeter-random-csv-data-set-config-plugin"]}`

