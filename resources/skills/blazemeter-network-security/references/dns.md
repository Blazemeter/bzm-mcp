# DNS Configuration

## Disable DNS Caching

Configure JMeter properties to disable DNS caching in BlazeMeter tests, ensuring fresh DNS lookups for each request.

**Use when**: DNS changes need to be reflected immediately in tests, testing DNS failover scenarios, or when you need dynamic DNS resolution for each request.

### Overview

By default, JMeter caches DNS lookups to improve performance. However, in some scenarios, you need fresh DNS lookups for each request to test DNS failover, reflect immediate DNS changes, or handle dynamic DNS resolution.

### Configuration

#### JMeter Properties

Once an application has gained network access (that is, a URL connection, parsing of XML document with external references, and so on), the DNS settings are cached, so any subsequent operation will use the old settings even if the real settings have changed.

To reset everything, do one of the following:
- Restart the server since the default JVM setting is to cache forever
- You can change this behavior by adding the `sun.net.inetaddr.ttl=0` command to the Engines via JMeter properties
- In your Test configuration page, enter the JMeter property `sun.net.inetaddr.ttl=0`

**Note**: The default JVM setting caches DNS lookups forever, which means DNS changes won't be reflected until the server is restarted. Setting `sun.net.inetaddr.ttl=0` disables DNS caching, ensuring fresh DNS lookups for each request.

**Property**: `sun.net.inetaddr.ttl`
- **Value**: `0` (to disable DNS caching)
- **Description**: Sets the time-to-live for DNS lookups to 0 seconds, ensuring fresh DNS lookups for each request

#### Configuration Methods

**Method 1: JMeter Properties in BlazeMeter (Recommended)**
1. In BlazeMeter test configuration, go to "Advanced Configuration" or "JMeter Properties" section
2. Add the following property:
   - `sun.net.inetaddr.ttl=0`
3. Run your test as planned

**Method 2: User Properties File**
1. Create or edit `user.properties` file in your JMeter script
2. Add the following property:
   ```
   sun.net.inetaddr.ttl=0
   ```

**Method 3: System Properties in Script**
Add to your JMeter script using JSR223 Sampler or BeanShell:
```java
System.setProperty("sun.net.inetaddr.ttl", "0");
```

### Use Cases

#### Testing DNS Failover
- **Scenario**: Testing failover between primary and secondary DNS servers
- **Requirement**: Fresh DNS lookups to detect DNS changes immediately
- **Benefit**: Tests can verify DNS failover behavior in real-time

#### Immediate DNS Changes
- **Scenario**: DNS records updated and need immediate reflection in tests
- **Requirement**: No DNS caching to see changes immediately
- **Benefit**: Tests reflect DNS changes without waiting for cache expiration

#### Dynamic DNS Resolution
- **Scenario**: Using dynamic DNS services or load balancers with changing IPs
- **Requirement**: Fresh DNS lookups for each request
- **Benefit**: Tests work correctly with dynamic DNS configurations

### Performance Considerations

**Impact of Disabling DNS Caching**:
- **Increased DNS Lookups**: Each request performs a DNS lookup
- **Potential Performance Impact**: May increase test execution time
- **Network Load**: More DNS queries to DNS servers

**When to Enable DNS Caching**:
- Stable DNS configurations
- Performance-critical tests
- High-volume test scenarios
- When DNS changes are not expected during test execution

### Best Practices

- **Use Selectively**: Only disable DNS caching when necessary
- **Monitor Performance**: Track test execution time impact
- **Test Configuration**: Verify DNS caching settings work as expected
- **Document Changes**: Keep track of DNS caching configuration in test documentation

---

## Documentation References

For detailed information about DNS configuration in BlazeMeter, use the BlazeMeter MCP help tools:

**Disable DNS Caching**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-disable-dns-caching`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-disable-dns-caching"]}`

