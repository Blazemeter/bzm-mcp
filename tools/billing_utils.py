"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, List


class AllowanceType(Enum):
    CREDITS = "credits"
    ACTUAL_THREADS = "actualThreads"
    VIRTUAL_USER_HOURS = "virtualUserHours"
    SERVER_HOURS = "serverHours"
    FUNCTIONAL_REQUESTS = "functionalRequests"


class TestType(Enum):
    PERFORMANCE = "performance"
    BROWSER_PERFORMANCE = "browser_performance"
    GUI_FUNCTIONAL = "gui_functional"
    API_MONITORING = "api_monitoring"
    SERVICE_VIRTUALIZATION = "service_virtualization"


@dataclass
class TestConfiguration:
    concurrency: int  # Max concurrent virtual users
    duration_minutes: Optional[float] = None  # Test duration in minutes
    iterations: Optional[int] = None  # Number of iterations (alternative to duration)
    locations: Optional[List[str]] = None  # List of location IDs
    test_type: TestType = TestType.PERFORMANCE
    browser_sessions: Optional[int] = None  # For GUI Functional tests
    api_calls: Optional[int] = None  # For API Monitoring tests
    virtual_services: Optional[int] = None  # For Service Virtualization
    transactions: Optional[int] = None  # For Service Virtualization
    uses_test_data: bool = False  # Whether test uses BlazeMeter Test Data
    number_of_servers: Optional[int] = None  # Number of engines/servers (for serverHours calculation)


@dataclass
class CostResult:
    cost: float
    cost_type: str
    calculation_details: Dict
    test_configuration: TestConfiguration


class BlazeMeterCostCalculator:
    # Based on BlazeMeter documentation:
    # https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html

    def __init__(self, allowance_type: str, allowance_amount: Optional[float] = None):
        self.allowance_type = AllowanceType(allowance_type)
        self.allowance_amount = allowance_amount

    def calculate_cost(
            self,
            test_config: Optional[TestConfiguration] = None
    ) -> CostResult:

        # If test_id is provided, fetch test configuration
        if not test_config:
            raise ValueError("test_config must be provided")

        # Calculate cost based on allowance type
        if self.allowance_type == AllowanceType.VIRTUAL_USER_HOURS:
            return self._calculate_vuh_cost(test_config)
        elif self.allowance_type == AllowanceType.CREDITS:
            # Credits can be VU or Tests - we'll calculate both and return the appropriate one
            # In practice, you'd need to know which plan type (VU or Tests) the user has
            # For now, we'll calculate VU cost as default
            return self._calculate_vu_cost(test_config)
        elif self.allowance_type == AllowanceType.ACTUAL_THREADS:
            return self._calculate_threads_cost(test_config)
        elif self.allowance_type == AllowanceType.SERVER_HOURS:
            return self._calculate_server_hours_cost(test_config)
        elif self.allowance_type == AllowanceType.FUNCTIONAL_REQUESTS:
            return self._calculate_functional_requests_cost(test_config)
        else:
            raise ValueError(f"Unsupported allowance type: {self.allowance_type}")

    def _calculate_vuh_cost(self, config: TestConfiguration) -> CostResult:
        """
        Calculate cost in Variable Unit Hours (VUH).

        Documentation References:
        - Skill: blazemeter-usage-billing
        - Help: usage-billing-blazemeter-credit-types-and-how-they-are-charged
        - URL: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html

        Performance testing: Length of test in hours (rounded up) * Max Users
        Browser Performance: Number of virtual users * 100 VUH
        GUI Functional: Length of browser session in hours (rounded up) * 100 VUH per session

        Source: BlazeMeter Credit Types and How They are Charged documentation,
        section "Variable Unit Hours (VUH) as Credit"
        """

        if config.test_type == TestType.BROWSER_PERFORMANCE:
            # Browser Performance: 100x multiplier
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "When running browser performance tests in BlazeMeter, you will consume 100 time more VU or VUH."
            cost = config.concurrency * 100
            details = {
                "formula": "concurrency * 100",
                "concurrency": config.concurrency,
                "multiplier": 100,
                "note": "Browser performance tests consume 100x more VUH than regular performance tests",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"
            }

        elif config.test_type == TestType.GUI_FUNCTIONAL:
            # GUI Functional: Sum of each browser session
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "In GUI Functional testing, VUH is determined by the length of your browser session.
            #  Sum of each browser session in a GUI Functional test:
            #  Length of a browser session in hours (rounded up to the next hour) * 100 VUH"
            if not config.browser_sessions:
                raise ValueError("browser_sessions required for GUI Functional tests")

            # Calculate duration in hours (rounded up)
            if config.duration_minutes:
                duration_hours = math.ceil(config.duration_minutes / 60)
            elif config.iterations:
                # Estimate: assume each iteration takes some time
                # This is a simplification - actual duration depends on test execution
                duration_hours = 1  # Default to 1 hour if iterations provided
            else:
                raise ValueError("duration_minutes or iterations required for GUI Functional tests")

            cost = config.browser_sessions * duration_hours * 100
            details = {
                "formula": "browser_sessions * duration_hours * 100",
                "browser_sessions": config.browser_sessions,
                "duration_hours": duration_hours,
                "multiplier_per_session": 100,
                "note": "Each browser session consumes 100 VUH per hour (rounded up)",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"
            }

        else:
            # Performance testing: Length of test in hours (rounded up) * Max Users
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "In Performance testing, VUH is: Length of test in hours (rounded up to the next hour) * Max Users"
            if not config.duration_minutes:
                raise ValueError("duration_minutes required for Performance tests")

            duration_hours = math.ceil(config.duration_minutes / 60)
            cost = duration_hours * config.concurrency

            details = {
                "formula": "duration_hours (rounded up) * concurrency",
                "duration_minutes": config.duration_minutes,
                "duration_hours": duration_hours,
                "concurrency": config.concurrency,
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"
            }

        # Apply Test Data multiplier if applicable
        # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
        # "When you use BlazeMeter Test Data features as part of a test execution, you will consume 50% more VU or VUH."
        if config.uses_test_data:
            original_cost = cost
            cost = cost * 1.5  # 50% more
            details["test_data_multiplier"] = 1.5
            details["cost_without_test_data"] = original_cost
            details["cost_with_test_data"] = cost
            details[
                "test_data_documentation"] = "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"

        return CostResult(
            cost=cost,
            cost_type="VUH",
            calculation_details=details,
            test_configuration=config
        )

    def _calculate_vu_cost(self, config: TestConfiguration) -> CostResult:
        """
        Calculate cost in Variable Units (VU).

        Documentation References:
        - Skill: blazemeter-usage-billing
        - Help: usage-billing-blazemeter-credit-types-and-how-they-are-charged
        - URL: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html

        Performance Testing: 1 VUH = 1 VU (except browser performance)
        Browser Performance: 100x multiplier
        GUI Functional: 1 browser session = 100 VU
        API Monitoring: 1,000 API calls = 5 VU
        Service Virtualization: 100 VU per service + 5 VU per 2,500 transactions

        Source: BlazeMeter Credit Types and How They are Charged documentation,
        section "Variable Unit (VU) as Credit"
        """
        details = {}

        if config.test_type == TestType.API_MONITORING:
            if not config.api_calls:
                raise ValueError("api_calls required for API Monitoring tests")

            # 1,000 API calls = 5 VU (increments of 5 VU reserved for 24 hours)
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "API Monitoring (also replaces API Functional Testing): 1,000 API calls equal 5 VU
            #  (increments of 5 VU are reserved for 24 hours)."
            cost = math.ceil(config.api_calls / 1000) * 5
            details = {
                "formula": "ceil(api_calls / 1000) * 5",
                "api_calls": config.api_calls,
                "vu_per_1000_calls": 5,
                "note": "VU increments of 5 are reserved for 24 hours",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"
            }

        elif config.test_type == TestType.SERVICE_VIRTUALIZATION:
            if not config.virtual_services:
                raise ValueError("virtual_services required for Service Virtualization")

            # 100 VU per running virtual service
            # Plus 5 VU per 2,500 transactions
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "Service Virtualization: Each running virtual service equals 100 VU.
            #  Each 2,500 transactions equal 5 VU that is reserved until midnight (local time)
            #  while the virtual service is running."
            cost = config.virtual_services * 100

            if config.transactions:
                transaction_vu = math.ceil(config.transactions / 2500) * 5
                cost += transaction_vu
                details["transactions"] = config.transactions
                details["transaction_vu"] = transaction_vu
                details["note"] = "100 VU per service + 5 VU per 2,500 transactions (reserved until midnight)"
            else:
                details["note"] = "100 VU per running virtual service"

            details["virtual_services"] = config.virtual_services
            details["base_vu_per_service"] = 100
            details[
                "documentation"] = "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"

        elif config.test_type == TestType.GUI_FUNCTIONAL:
            # 1 browser session = 100 VU
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "GUI Functional Testing: 1 Browser session execution equals 100 VU."
            if not config.browser_sessions:
                raise ValueError("browser_sessions required for GUI Functional tests")

            cost = config.browser_sessions * 100
            details = {
                "formula": "browser_sessions * 100",
                "browser_sessions": config.browser_sessions,
                "vu_per_session": 100,
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"
            }

        elif config.test_type == TestType.BROWSER_PERFORMANCE:
            # Browser Performance: 100x multiplier (same as VUH calculation)
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "When running browser performance tests in BlazeMeter, you will consume 100 time more VU or VUH."
            cost = config.concurrency * 100
            details = {
                "formula": "concurrency * 100",
                "concurrency": config.concurrency,
                "multiplier": 100,
                "note": "Browser performance tests consume 100x more VU than regular performance tests",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"
            }

        else:
            # Performance Testing: 1 VUH = 1 VU
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
            # "Performance Testing: 1 Variable Unit Hour (VUH) equals 1 VU, except for Browser Performance Test Consumption"
            if not config.duration_minutes:
                raise ValueError("duration_minutes required for Performance tests")

            duration_hours = math.ceil(config.duration_minutes / 60)
            cost = duration_hours * config.concurrency
            details = {
                "formula": "duration_hours (rounded up) * concurrency",
                "duration_minutes": config.duration_minutes,
                "duration_hours": duration_hours,
                "concurrency": config.concurrency,
                "note": "1 VUH = 1 VU for Performance tests",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"
            }

        # Apply Test Data multiplier if applicable
        # Reference: https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html
        # "When you use BlazeMeter Test Data features as part of a test execution, you will consume 50% more VU or VUH."
        if config.uses_test_data:
            original_cost = cost
            cost = cost * 1.5  # 50% more
            details["test_data_multiplier"] = 1.5
            details["cost_without_test_data"] = original_cost
            details["cost_with_test_data"] = cost
            details[
                "test_data_documentation"] = "https://help.blazemeter.com/docs/guide/usage-billing-blazemeter-credit-types-and-how-they-are-charged.html"

        return CostResult(
            cost=cost,
            cost_type="VU",
            calculation_details=details,
            test_configuration=config
        )

    def _calculate_threads_cost(self, config: TestConfiguration) -> CostResult:
        """
        Calculate cost based on actual threads (Max Number of Variable Units).

        Documentation References:
        - Skill: blazemeter-usage-billing
        - Help: usage-billing-how-do-i-view-my-usage-reports
        - URL: https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html

        Based on Usage Reports documentation:
        - "Max Number of Variable Units" represents the maximum concurrent threads/users
        - This is the peak concurrency reached during the test execution
        - Found in Usage Reports under "Select Report Type" -> "Max Number of Variable Units"

        For different test types:
        - Performance tests: Maximum concurrent virtual users/threads
        - Browser Performance: Same as performance (threads = virtual users)
        - GUI Functional: Number of concurrent browser sessions
        - API Monitoring: Not typically measured in threads
        - Service Virtualization: Number of concurrent virtual services

        Source: BlazeMeter Usage Reports documentation, section "Filter Usage Reports By Type and Time Period"
        """
        if config.test_type == TestType.GUI_FUNCTIONAL:
            if not config.browser_sessions:
                raise ValueError("browser_sessions required for GUI Functional tests with actualThreads")
            cost = config.browser_sessions
            details = {
                "formula": "browser_sessions",
                "browser_sessions": config.browser_sessions,
                "note": "For GUI Functional tests, actualThreads equals the number of concurrent browser sessions"
            }
        elif config.test_type == TestType.SERVICE_VIRTUALIZATION:
            if not config.virtual_services:
                raise ValueError("virtual_services required for Service Virtualization tests with actualThreads")
            cost = config.virtual_services
            details = {
                "formula": "virtual_services",
                "virtual_services": config.virtual_services,
                "note": "For Service Virtualization, actualThreads equals the number of concurrent virtual services"
            }
        elif config.test_type == TestType.API_MONITORING:
            # API Monitoring doesn't typically use threads in the same way
            # Use concurrency if available, otherwise default to 1
            cost = config.concurrency if config.concurrency > 0 else 1
            details = {
                "formula": "concurrency (or 1 if not specified)",
                "concurrency": config.concurrency,
                "note": "For API Monitoring, actualThreads may represent concurrent test executions"
            }
        else:
            # Performance and Browser Performance tests
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html
            # Usage Reports include "Max Number of Variable Units" which represents peak concurrency
            cost = config.concurrency
            details = {
                "formula": "max_concurrent_threads",
                "concurrency": config.concurrency,
                "note": "Cost equals the maximum concurrent threads/users reached during test execution. "
                        "This represents the peak concurrency, not the configured concurrency.",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html"
            }

        return CostResult(
            cost=cost,
            cost_type="actualThreads",
            calculation_details=details,
            test_configuration=config
        )

    def _calculate_server_hours_cost(self, config: TestConfiguration) -> CostResult:
        """
        Calculate cost in server hours.

        Documentation References:
        - Skill: blazemeter-usage-billing
        - Help: usage-billing-how-do-i-view-my-usage-reports
        - URL: https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html

        Based on Usage Reports documentation:
        - "Number of Server Hours" = Number of provisioned engines/instances * test duration in hours
        - Server hours represent the compute resources consumed by the test
        - Found in Usage Reports under "Select Report Type" -> "Number of Server Hours"
        - Detailed report includes: "Server Hours: Number of server hours consumed by provisioned engines or instances"

        Formula: Number of Servers * Duration in hours

        Engine estimation:
        - BlazeMeter typically provisions 1 engine per ~1000-2000 concurrent users
        - Minimum 1 engine is always provisioned
        - Actual engine count may vary based on load distribution and locations

        Source: BlazeMeter Usage Reports documentation, sections:
        - "Filter Usage Reports By Type and Time Period" (report type: "Number of Server Hours")
        - "How to Download Detailed Usage Reports" (field: "Server Hours")
        """
        if not config.duration_minutes:
            raise ValueError("duration_minutes required for server hours calculation")

        estimated_engines = 1
        location_multiplier = 1
        # Use provided number_of_servers if available, otherwise estimate
        if config.number_of_servers is not None and config.number_of_servers > 0:
            # User provided the exact number of servers
            total_engines = config.number_of_servers
            engine_source = "user_provided"
        else:
            # Estimate number of engines/instances based on concurrency
            # BlazeMeter typically provisions engines based on load requirements
            # General rule: ~1000-2000 users per engine, but this can vary
            # We use a conservative estimate of 1000 users per engine
            if config.concurrency > 0:
                estimated_engines = max(1, math.ceil(config.concurrency / 1000))
            else:
                # If no concurrency specified, assume minimum 1 engine
                estimated_engines = 1

            # Consider multiple locations - each location may require engines
            location_multiplier = len(config.locations) if config.locations else 1
            total_engines = estimated_engines * location_multiplier
            engine_source = "estimated"

        # Duration in hours (not rounded up for server hours - use actual duration)
        duration_hours = config.duration_minutes / 60

        cost = total_engines * duration_hours

        details = {
            "formula": "number_of_engines * duration_hours",
            "total_engines": total_engines,
            "engine_source": engine_source,
            "duration_minutes": config.duration_minutes,
            "duration_hours": duration_hours,
        }

        if engine_source == "estimated":
            details.update({
                "estimated_engines_per_location": estimated_engines if config.concurrency > 0 else 1,
                "number_of_locations": location_multiplier,
                "note": "Engine count is estimated based on concurrency (~1000 users per engine). "
                        "Actual engine count may vary based on load distribution, locations, "
                        "and BlazeMeter's provisioning algorithm. Server hours use actual duration, "
                        "not rounded up. To provide exact engine count, use number_of_servers parameter."
            })
        else:
            details.update({
                "note": "Engine count provided by user. Server hours use actual duration, not rounded up.",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html"
            })

        return CostResult(
            cost=cost,
            cost_type="serverHours",
            calculation_details=details,
            test_configuration=config
        )

    def _calculate_functional_requests_cost(self, config: TestConfiguration) -> CostResult:
        """
        Calculate cost for functional requests.

        Documentation References:
        - Skill: blazemeter-usage-billing
        - Help: usage-billing-how-do-i-view-my-usage-reports
        - URL: https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html

        Based on Usage Reports documentation:
        - "API Functional Tests - Number of API Calls" represents functional requests
        - This applies to Functional API tests (now part of API Monitoring)
        - Each API call in a functional test counts as a functional request
        - Found in Usage Reports under "Select Report Type" -> "API Functional Tests - Number of API Calls"
        - Detailed report includes: "Functional Test API calls: Applies only to Functional API tests -
          The number of calls made in your test scenario"

        For different test types:
        - API Monitoring/Functional API: Number of API calls made
        - GUI Functional: Number of browser sessions (each session may make multiple requests)
        - Other test types: Typically 1 request per test execution

        Source: BlazeMeter Usage Reports documentation, sections:
        - "Filter Usage Reports By Type and Time Period" (report type: "API Functional Tests - Number of API Calls")
        - "How to Download Detailed Usage Reports" (field: "Functional Test API calls")
        """
        if config.test_type == TestType.API_MONITORING:
            if not config.api_calls:
                raise ValueError("api_calls required for API Monitoring tests with functionalRequests")
            # Reference: https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html
            # Usage Reports show "API Functional Tests - Number of API Calls" which represents functional requests
            cost = config.api_calls
            details = {
                "formula": "api_calls",
                "api_calls": config.api_calls,
                "note": "For API Monitoring/Functional API tests, functionalRequests equals "
                        "the number of API calls made in the test scenario. "
                        "This includes all API calls across all test steps and iterations.",
                "documentation": "https://help.blazemeter.com/docs/guide/usage-billing-how-do-i-view-my-usage-reports.html"
            }
        elif config.test_type == TestType.GUI_FUNCTIONAL:
            if not config.browser_sessions:
                raise ValueError("browser_sessions required for GUI Functional tests")
            # For GUI Functional, each browser session may make multiple requests
            # We use browser_sessions as a proxy, but actual requests may be higher
            cost = config.browser_sessions
            details = {
                "formula": "browser_sessions (approximation)",
                "browser_sessions": config.browser_sessions,
                "note": "For GUI Functional tests, functionalRequests is approximated by "
                        "browser sessions. Each session may make multiple HTTP requests. "
                        "Actual request count depends on test steps and page interactions."
            }
        else:
            # For other test types (Performance, Service Virtualization, etc.)
            # Typically, 1 request per test execution
            cost = 1
            details = {
                "formula": "1 request per test execution",
                "note": "For non-functional test types, each test execution consumes "
                        "1 functional request credit. This metric primarily applies to "
                        "Functional API and GUI Functional tests."
            }

        return CostResult(
            cost=cost,
            cost_type="functionalRequests",
            calculation_details=details,
            test_configuration=config
        )


def calculate_test_cost(
        config_dict: Dict
) -> Dict:
    """
    Convenience function to calculate test cost.

    Args:
        config_dict: A dictionary containing the configuration parameters.
            Possible keys:
            - 'allowance_type': Type of allowance (credits, virtualUserHours, etc.) (required)
            - 'concurrency': Maximum concurrent virtual users
            - 'duration_minutes': Test duration in minutes
            - 'iterations': Number of iterations (alternative to duration)
            - 'locations': List of location IDs
            - 'test_type': Type of test (performance, browser_performance, gui_functional, etc.)
            - 'browser_sessions': Number of browser sessions (for GUI Functional)
            - 'api_calls': Number of API calls (for API Monitoring)
            - 'virtual_services': Number of virtual services (for Service Virtualization)
            - 'transactions': Number of transactions (for Service Virtualization)
            - 'uses_test_data': Whether test uses BlazeMeter Test Data
            - 'number_of_servers': Number of servers (for server hours calculation)

    Returns:
        Dictionary with cost calculation results
    """
    # Extract values from the dictionary
    allowance_type = config_dict.get('allowance_type')
    if not allowance_type:
        raise ValueError("allowance_type is required in config_dict")

    concurrency = config_dict.get('concurrency')
    duration_minutes = config_dict.get('duration_minutes')
    iterations = config_dict.get('iterations')
    locations = config_dict.get('locations')
    test_type = config_dict.get('test_type', "performance")
    browser_sessions = config_dict.get('browser_sessions')
    api_calls = config_dict.get('api_calls')
    virtual_services = config_dict.get('virtual_services')
    transactions = config_dict.get('transactions')
    uses_test_data = config_dict.get('uses_test_data', False)
    number_of_servers = config_dict.get('number_of_servers')

    calculator = BlazeMeterCostCalculator(allowance_type)

    # Create test configuration if not using test_id
    test_config = TestConfiguration(
        concurrency=concurrency or 0,
        duration_minutes=duration_minutes,
        iterations=iterations,
        locations=locations,
        test_type=TestType(test_type),
        browser_sessions=browser_sessions,
        api_calls=api_calls,
        virtual_services=virtual_services,
        transactions=transactions,
        uses_test_data=uses_test_data,
        number_of_servers=number_of_servers
    )

    result = calculator.calculate_cost(
        test_config=test_config
    )

    return {
        "cost": result.cost,
        "cost_type": result.cost_type,
        "calculation_details": result.calculation_details,
        "skill": "blazemeter-usage-billing",
        "test_configuration": {
            "concurrency": result.test_configuration.concurrency,
            "duration_minutes": result.test_configuration.duration_minutes,
            "test_type": result.test_configuration.test_type.value
        }
    }
