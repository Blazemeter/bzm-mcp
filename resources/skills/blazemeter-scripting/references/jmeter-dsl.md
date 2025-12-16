# JMeter DSL

## JMeter DSL

Use JMeter DSL (Domain-Specific Language) for creating JMeter tests as code in Java, providing Git-friendly and IDE-friendly test development.

**Use when**: Creating JMeter tests as code in Java for Git-friendly and IDE-friendly development or when managing JMeter tests in version control systems.

### Overview

JMeter DSL is an open source initiative that provides JMeter-as-Code in Java.

There are two important limitations of vanilla JMeter:
- Not Git friendly due to its XML nature
- For Groovy scripting, no autocomplete or debugging features

JMeter DSL solves the above problems, and provides more features such as CI/CD integration, Git and IDE friendly, extends the JMeter ecosystem and makes it more pluggable, and more.

**Note**: JMeter DSL is an open source initiative that provides JMeter-as-Code in Java, making it easier to create, maintain, and version control JMeter tests.

JMeter DSL allows you to create JMeter tests programmatically using Java code instead of JMX files. This approach provides:
- Version control friendly (Git)
- IDE support and autocomplete
- Code reusability
- Programmatic test generation
- CI/CD integration
- Extensible and pluggable ecosystem

### Benefits

- **Version Control**: Tests are code files, easy to version control
- **IDE Support**: Full IDE support with autocomplete and debugging
- **Code Reusability**: Reuse test components as code
- **Dynamic Generation**: Generate tests programmatically
- **Git Friendly**: Tests are code files, not XML, making them Git-friendly
- **CI/CD Integration**: Easy integration with CI/CD pipelines

### Creating Tests with JMeter DSL

#### Basic Example
```java
import us.abstracta.jmeter.javadsl.core.TestPlanStats;
import static us.abstracta.jmeter.javadsl.JmeterDsl.*;

TestPlanStats stats = testPlan(
    threadGroup(2, 10,
        httpSampler("http://example.com")
    )
).run();
```

### Learning Resources

To learn more about JMeter DSL, see:
- [User guide | jmeter-java-dsl (abstracta.github.io)](https://abstracta.github.io/jmeter-java-dsl/guide/)
- [GitHub - abstracta/jmeter-java-dsl: Simple JMeter performance tests API](https://github.com/abstracta/jmeter-java-dsl)

### Integration with BlazeMeter

1. **Create Test with DSL**: Write JMeter test using DSL
2. **Compile to JMX**: Convert DSL code to JMX file
3. **Upload to BlazeMeter**: Upload JMX file to BlazeMeter
4. **Execute Test**: Run test in BlazeMeter

**Note**: Since JMeter DSL compiles to standard JMX files, the resulting tests are fully compatible with BlazeMeter and can be used just like any other JMeter test.

### Best Practices

- Use DSL for complex or dynamic test generation
- Leverage IDE features for development
- Version control test code
- Document test structure and logic

---

## Documentation References

For detailed information about JMeter DSL, use the BlazeMeter MCP help tools:

**JMeter DSL**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `performance-jmeter-dsl`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["performance-jmeter-dsl"]}`

