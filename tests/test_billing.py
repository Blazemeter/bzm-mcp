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
import pytest

from tools.billing_utils import (
    BlazeMeterCostCalculator,
    TestConfiguration as BillingTestConfiguration,
    TestType as BillingTestType,
    AllowanceType,
    calculate_test_cost
)


class TestPerformanceTestsVUH:
    """Tests for Performance tests using VUH allowance type"""

    def test_performance_test_vuh_basic(self):
        """Test basic performance test with VUH"""
        result = calculate_test_cost({
            'allowance_type': "virtualUserHours",
            'concurrency': 100,
            'duration_minutes': 90,
            'test_type': "performance"
        })

        # 90 minutes = 2 hours (rounded up) * 100 users = 200 VUH
        assert result['cost'] == 200
        assert result['cost_type'] == "VUH"
        assert result['calculation_details']['duration_hours'] == 2
        assert result['calculation_details']['concurrency'] == 100

    def test_performance_test_vuh_exact_hour(self):
        """Test performance test with exact hour duration"""
        result = calculate_test_cost({
            'allowance_type': "virtualUserHours",
            'concurrency': 50,
            'duration_minutes': 60,
            'test_type': "performance"
        })

        # 60 minutes = 1 hour * 50 users = 50 VUH
        assert result['cost'] == 50
        assert result['cost_type'] == "VUH"

    def test_performance_test_vuh_with_test_data(self):
        """Test performance test with Test Data (50% increase)"""
        result = calculate_test_cost({
            'allowance_type': "virtualUserHours",
            'concurrency': 100,
            'duration_minutes': 60,
            'test_type': "performance",
            'uses_test_data': True
        })

        # 60 minutes = 1 hour * 100 users = 100 VUH * 1.5 = 150 VUH
        assert result['cost'] == 150
        assert result['calculation_details']['test_data_multiplier'] == 1.5
        assert result['calculation_details']['cost_without_test_data'] == 100


class TestBrowserPerformanceTests:
    """Tests for Browser Performance tests"""

    def test_browser_performance_vuh(self):
        """Test browser performance test with VUH (100x multiplier)"""
        result = calculate_test_cost({
            'allowance_type': "virtualUserHours",
            'concurrency': 10,
            'duration_minutes': 60,
            'test_type': "browser_performance"
        })

        # 10 users * 100 = 1000 VUH
        assert result['cost'] == 1000
        assert result['cost_type'] == "VUH"
        assert result['calculation_details']['multiplier'] == 100

    def test_browser_performance_vu(self):
        """Test browser performance test with VU (100x multiplier)"""
        result = calculate_test_cost({
            'allowance_type': "credits",
            'concurrency': 5,
            'duration_minutes': 30,
            'test_type': "browser_performance"
        })

        # 5 users * 100 = 500 VU
        assert result['cost'] == 500
        assert result['cost_type'] == "VU"


class TestGUIFunctionalTests:
    """Tests for GUI Functional tests"""

    def test_gui_functional_vuh(self):
        """Test GUI functional test with VUH"""
        result = calculate_test_cost({
            'allowance_type': "virtualUserHours",
            'browser_sessions': 4,
            'duration_minutes': 30,
            'test_type': "gui_functional"
        })

        # 4 sessions * 1 hour (30 min rounded up) * 100 = 400 VUH
        assert result['cost'] == 400
        assert result['cost_type'] == "VUH"
        assert result['calculation_details']['browser_sessions'] == 4
        assert result['calculation_details']['duration_hours'] == 1
        assert result['calculation_details']['multiplier_per_session'] == 100

    def test_gui_functional_vu(self):
        """Test GUI functional test with VU"""
        result = calculate_test_cost({
            'allowance_type': "credits",
            'browser_sessions': 3,
            'test_type': "gui_functional"
        })

        # 3 sessions * 100 = 300 VU
        assert result['cost'] == 300
        assert result['cost_type'] == "VU"

    def test_gui_functional_missing_browser_sessions(self):
        """Test that GUI functional test requires browser_sessions"""
        with pytest.raises(ValueError, match="browser_sessions required"):
            calculate_test_cost({
                'allowance_type': "credits",
                'test_type': "gui_functional"
            })


class TestAPIMonitoringTests:
    """Tests for API Monitoring tests"""

    def test_api_monitoring_vu(self):
        """Test API monitoring test with VU"""
        result = calculate_test_cost({
            'allowance_type': "credits",
            'api_calls': 5000,
            'test_type': "api_monitoring"
        })

        # 5000 calls / 1000 = 5 * 5 = 25 VU
        assert result['cost'] == 25
        assert result['cost_type'] == "VU"
        assert result['calculation_details']['api_calls'] == 5000

    def test_api_monitoring_partial_thousand(self):
        """Test API monitoring with calls not divisible by 1000"""
        result = calculate_test_cost({
            'allowance_type': "credits",
            'api_calls': 3500,
            'test_type': "api_monitoring"
        })

        # 3500 calls / 1000 = 3.5, rounded up to 4 * 5 = 20 VU
        assert result['cost'] == 20
        assert result['cost_type'] == "VU"

    def test_api_monitoring_functional_requests(self):
        """Test API monitoring with functional requests"""
        result = calculate_test_cost({
            'allowance_type': "functionalRequests",
            'api_calls': 1000,
            'test_type': "api_monitoring"
        })

        assert result['cost'] == 1000
        assert result['cost_type'] == "functionalRequests"


class TestServiceVirtualizationTests:
    """Tests for Service Virtualization tests"""

    def test_service_virtualization_basic(self):
        """Test service virtualization without transactions"""
        result = calculate_test_cost({
            'allowance_type': "credits",
            'virtual_services': 2,
            'test_type': "service_virtualization"
        })

        # 2 services * 100 = 200 VU
        assert result['cost'] == 200
        assert result['cost_type'] == "VU"

    def test_service_virtualization_with_transactions(self):
        """Test service virtualization with transactions"""
        result = calculate_test_cost({
            'allowance_type': "credits",
            'virtual_services': 1,
            'transactions': 5000,
            'test_type': "service_virtualization"
        })

        # 1 service * 100 = 100 VU
        # 5000 transactions / 2500 = 2 * 5 = 10 VU
        # Total = 110 VU
        assert result['cost'] == 110
        assert result['cost_type'] == "VU"


class TestActualThreadsAllowance:
    """Tests for actualThreads allowance type"""

    def test_actual_threads_performance(self):
        """Test actual threads for performance test"""
        result = calculate_test_cost({
            'allowance_type': "actualThreads",
            'concurrency': 250,
            'duration_minutes': 30,
            'test_type': "performance"
        })

        assert result['cost'] == 250
        assert result['cost_type'] == "actualThreads"

    def test_actual_threads_gui_functional(self):
        """Test actual threads for GUI functional test"""
        result = calculate_test_cost({
            'allowance_type': "actualThreads",
            'browser_sessions': 5,
            'test_type': "gui_functional"
        })

        assert result['cost'] == 5
        assert result['cost_type'] == "actualThreads"


class TestServerHoursAllowance:
    """Tests for serverHours allowance type"""

    def test_server_hours_provided(self):
        """Test server hours with provided number of servers"""
        result = calculate_test_cost({
            'allowance_type': "serverHours",
            'concurrency': 1000,
            'duration_minutes': 120,
            'number_of_servers': 2,
            'test_type': "performance"
        })

        # 2 servers * 2 hours = 4 server hours
        assert result['cost'] == 4.0
        assert result['cost_type'] == "serverHours"
        assert result['calculation_details']['total_engines'] == 2
        assert result['calculation_details']['engine_source'] == "user_provided"

    def test_server_hours_estimated(self):
        """Test server hours with estimated engines"""
        result = calculate_test_cost({
            'allowance_type': "serverHours",
            'concurrency': 2500,
            'duration_minutes': 60,
            'test_type': "performance"
        })

        # 2500 users / 1000 = 3 engines (rounded up)
        # 3 engines * 1 hour = 3 server hours
        assert result['cost'] == 3.0
        assert result['cost_type'] == "serverHours"
        assert result['calculation_details']['engine_source'] == "estimated"

    def test_server_hours_with_multiple_locations(self):
        """Test server hours with multiple locations"""
        result = calculate_test_cost({
            'allowance_type': "serverHours",
            'concurrency': 1000,
            'duration_minutes': 60,
            'locations': ["us-west-1", "eu-central-1", "ap-southeast-1"],
            'test_type': "performance"
        })

        # 1 engine per location * 3 locations * 1 hour = 3 server hours
        assert result['cost'] == 3.0
        assert result['calculation_details']['number_of_locations'] == 3


class TestErrorHandling:
    """Tests for error handling and validation"""

    def test_missing_allowance_type(self):
        """Test that allowance_type is required"""
        with pytest.raises(ValueError, match="allowance_type is required"):
            calculate_test_cost({
                'concurrency': 100,
                'duration_minutes': 60
            })

    def test_missing_duration_for_performance(self):
        """Test that duration is required for performance tests"""
        with pytest.raises(ValueError, match="duration_minutes required"):
            calculate_test_cost({
                'allowance_type': "virtualUserHours",
                'concurrency': 100,
                'test_type': "performance"
            })

    def test_missing_api_calls_for_monitoring(self):
        """Test that api_calls is required for API monitoring with VU"""
        with pytest.raises(ValueError, match="api_calls required"):
            calculate_test_cost({
                'allowance_type': "credits",
                'test_type': "api_monitoring"
            })

    def test_missing_virtual_services(self):
        """Test that virtual_services is required for service virtualization"""
        with pytest.raises(ValueError, match="virtual_services required"):
            calculate_test_cost({
                'allowance_type': "credits",
                'test_type': "service_virtualization"
            })


class TestCalculatorClass:
    """Tests using the BlazeMeterCostCalculator class directly"""

    def test_calculator_initialization(self):
        """Test calculator initialization"""
        calculator = BlazeMeterCostCalculator("virtualUserHours")
        assert calculator.allowance_type == AllowanceType.VIRTUAL_USER_HOURS

    def test_calculator_with_test_config(self):
        """Test calculator with TestConfiguration object"""
        calculator = BlazeMeterCostCalculator("credits")

        config = BillingTestConfiguration(
            concurrency=100,
            duration_minutes=60,
            test_type=BillingTestType.PERFORMANCE
        )

        result = calculator.calculate_cost(test_config=config)

        assert result.cost == 100
        assert result.cost_type == "VU"
        assert result.test_configuration.concurrency == 100

    def test_calculator_no_config_raises_error(self):
        """Test that calculator requires configuration"""
        calculator = BlazeMeterCostCalculator("credits")

        with pytest.raises(ValueError, match="test_config must be provided"):
            calculator.calculate_cost()


@pytest.fixture
def sample_performance_config():
    """Fixture providing a sample performance test configuration"""
    return {
        'allowance_type': "virtualUserHours",
        'concurrency': 100,
        'duration_minutes': 60,
        'test_type': "performance"
    }


class TestFixtures:
    """Tests using pytest fixtures"""

    def test_with_fixture(self, sample_performance_config):
        """Test using the sample configuration fixture"""
        result = calculate_test_cost(sample_performance_config)

        assert result['cost'] == 100
        assert result['cost_type'] == "VUH"

    def test_fixture_modification(self, sample_performance_config):
        """Test modifying fixture data"""
        sample_performance_config['concurrency'] = 200
        result = calculate_test_cost(sample_performance_config)

        assert result['cost'] == 200
