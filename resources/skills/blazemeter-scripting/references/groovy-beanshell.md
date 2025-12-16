# Groovy/Beanshell Scripting

## File Writing

Write files in Groovy/Beanshell scripts during BlazeMeter performance tests, using the /tmp/artifacts/ directory for output files.

**Use when**: Scripts need to write output files during test execution or when generating test artifacts for analysis.

### Overview

When running your Performance Tests in BlazeMeter, using JSR223 Pre/Post processors is a common practice to extract desired data from a response to a file. This applies to .txt and .csv files.

When writing a file using this element, include the following path to ensure the file gets written to the correct folder:
```
/tmp/artifacts/<YourFilename.txt>
```

For example, instead of `Results.txt`, write `/tmp/artifacts/Results.txt`.

You can also exclude the path and only specify `<YourFilename.txt>` in your script and the file will automatically be created in the `/tmp/artifacts` folder.

As a result, you'll find the output file in the "artifacts.zip" file of your Test results.

**Note**: This is useful for extracting test data, generating debug logs, or creating custom reports during test execution.

### Directory Structure

- **Output Directory**: `/tmp/artifacts/`
- **File Persistence**: Files in this directory are preserved after test execution
- **File Download**: Files can be downloaded from test artifacts (in artifacts.zip file)
- **Automatic Path**: You can specify just the filename and it will automatically be created in `/tmp/artifacts/`

### Writing Files

#### Groovy Example
```groovy
// Write text file (full path)
def file = new File('/tmp/artifacts/output.txt')
file.write('Test output data')

// Write text file (automatic path - just filename)
def file2 = new File('output.txt')  // Automatically created in /tmp/artifacts/
file2.write('Test output data')

// Write CSV file
def csvFile = new File('/tmp/artifacts/results.csv')
csvFile.write('Header1,Header2\nValue1,Value2\n')
```

#### Beanshell Example
```beanshell
// Write text file (full path)
import java.io.*;
FileWriter fw = new FileWriter("/tmp/artifacts/output.txt");
fw.write("Test output data");
fw.close();

// Write text file (automatic path - just filename)
FileWriter fw2 = new FileWriter("output.txt");  // Automatically created in /tmp/artifacts/
fw2.write("Test output data");
fw2.close();
```

### Use Cases

- **Test Artifacts**: Generate test artifacts for analysis
- **Debug Information**: Write debug information to files
- **Data Export**: Export test data to files
- **Log Files**: Create custom log files

### Best Practices

- Always use `/tmp/artifacts/` directory for output files
- Use appropriate file names and extensions
- Clean up temporary files if needed
- Document file structure and content

---

## Documentation References

For detailed information about Groovy/Beanshell file writing, use the BlazeMeter MCP help tools:

**Groovy/Beanshell File Writing**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-groovy-beanshell`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-groovy-beanshell"]}`

