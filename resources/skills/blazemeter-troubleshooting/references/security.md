# Security Troubleshooting

## Apache Log4j2 Vulnerability

Understand and mitigate Apache Log4j2 vulnerabilities in BlazeMeter, including updating OPL components, JMeter versions, and security patches.

**Use when**: Understanding and mitigating Apache Log4j2 vulnerabilities in BlazeMeter, updating OPL components, JMeter versions, or applying security patches.

### Context

**Last time this page was updated: 12/21/2021 3:43am PST** As new information becomes available, we will keep updating this page.

This page contains information about BlazeMeter's response to the Apache Log4j2 Remote Code Execution (RCE) Vulnerability - CVE-2021-44228 and the following. The information here also covers the second identified vulnerability, CVE-2021-45046: Apache Log4j2 Thread Context Message Pattern and Context Lookup Pattern vulnerable to a denial of service attack.

Our engineering and product teams are aware of these vulnerabilities and provided patches (see below) to prevent any impact to BlazeMeter. Updated information will be provided continuously on this page as it becomes available.

For more information about this vulnerability please see:
- https://lists.apache.org/thread/83y7dx5xvn3h5290q1twn16tltolv88f

### Summary

Log4J Vulnerability impact to BlazeMeter: Only services which are written in Java were exposed to the log4j vulnerability. The majority of BlazeMeter is not written in Java and therefore our product is largely unexposed to this vulnerability.

We've released patches to services which were exposed to the log4j vulnerabilities (CVE-2021-44228, CVE-2021-45046, CVE-2021-45105) and will keep updating components as needed.

We will continue to work with all our external service providers to verify they are not exposed to that risk as well, as a second level risk mitigation.

### Details

On Dec 9th, 2021, we were first notified of the initial log4j security vulnerability. We immediately started the security investigation process of all systems to understand our exposure. Through our exhaustive search we discovered two affected areas, Service Virtualization and JMeter.

We found no evidence of any attack on our systems and all customer data/information is secure. Please also see [Perforce' security announcement page](https://www.perforce.com/support/log4j).

### Mitigation & Required Actions by BlazeMeter Users

The following BlazeMeter agent (OPL) components must be updated to the new version containing the patch:

- **The OPLs need to be updated** (if auto update is disabled, the update has to be conducted manually by the customer) & restarted. Please update any OPLs to the latest images. The versions that contain the fixes are:
  - `blazemeter/taurus-cloud` (1.20.261)
  - `blazemeter/service-mock` (5.0.11)
  - `blazemeter/blazevse` (5.0.11)
  - `blazemeter/sv-bridge` (5.0.11)

- **If you are using the Private Cloud deployment model**, please also update: `blazemeter/mock-pc-service` (5.0.11)

#### JMeter in BlazeMeter's cloud agents and OPLs (on-premise agents)

JMeter is not openly exposed and only conforms to the testing script provided by the user, thus remaining isolated from the outer world even when vulnerable. We released a new version of our cloud agents and OPL image with log4j 2.17 (see above for details under taurus cloud) and are continuously assessing the situation and will take further actions as applicable/needed. The solution was to replace the old log4j-*.jar files. This means you will see the jar names of older versions, however these jar files contain the content of log4j 2.17. JMeter itself is Open Source and not part of the BlazeMeter product, therefore we are not able to provide any patches for standalone versions of JMeter.


### Best Practices

- **Stay Informed**: Monitor security advisories regularly
- **Update Promptly**: Apply security patches as soon as available
- **Test Updates**: Always test after applying updates
- **Document Changes**: Keep track of security updates applied

### Additional Resources

For more information about this vulnerability please see:
- https://lists.apache.org/thread/83y7dx5xvn3h5290q1twn16tltolv88f
- [Perforce' security announcement page](https://www.perforce.com/support/log4j)

---

## Documentation References

For detailed information about Apache Log4j2 vulnerability mitigation, use the BlazeMeter MCP help tools:

**Apache Log4j2 Vulnerability**:
- **Category**: `root_category`
- **Subcategory**: `answers`
- **Help ID**: `answers-security-apache-log4j2`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "answers", "help_id_list": ["answers-security-apache-log4j2"]}`

