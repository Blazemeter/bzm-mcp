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

from formatters.execution import (
    format_request_stats,
    format_summary_report,
    format_error_report,
    format_anomalies_stats,
)


class TestFormatRequestStats:

    def test_format_request_stats_basic(self):
        api_data = [
            {
                "labelId": "test-label-id-123",
                "labelName": "Test Endpoint",
                "samples": 1000,
                "avgResponseTime": 150.5,
                "90line": 200,
                "95line": 250,
                "99line": 300,
                "minResponseTime": 50,
                "maxResponseTime": 500,
                "avgLatency": 10.2,
                "stDev": 25.5,
                "duration": 60,
                "avgBytes": 1024.5,
                "avgThroughput": 16.67,
                "medianResponseTime": 145,
                "errorsCount": 5,
                "errorsRate": 0.5,
                "concurrency": 20,
                "geoMeanResponseTime": 148.3,
                "hasLabelPassedThresholds": True
            }
        ]

        result = format_request_stats(api_data, {
            "execution_id": 12345,
            "execution_name": "Test Execution"
        })

        assert len(result) == 1
        report = result[0]
        assert report.execution_id == 12345
        assert report.execution_name == "Test Execution"
        assert report.context is not None
        assert len(report.context) > 0
        assert "REQUEST STATS REPORT METRICS EXPLANATION" in report.context
        assert len(report.request_stats) == 1

        stats = report.request_stats[0]
        assert stats.label_id == "test-label-id-123"
        assert stats.label_name == "Test Endpoint"
        assert stats.samples == 1000
        assert stats.avg_response_time_ms == 150.5
        assert stats.percentile_90_ms == 200
        assert stats.percentile_95_ms == 250
        assert stats.percentile_99_ms == 300
        assert stats.min_response_time_ms == 50
        assert stats.max_response_time_ms == 500
        assert stats.avg_latency_ms == 10.2
        assert stats.standard_deviation_ms == 25.5
        assert stats.duration_seconds == 60
        assert stats.avg_bytes == 1024.5
        assert stats.avg_throughput_per_second == 16.67
        assert stats.median_response_time_ms == 145
        assert stats.errors_count == 5
        assert stats.errors_rate_percent == 0.5
        assert stats.concurrency == 20
        assert stats.geometric_mean_response_time_ms == 148.3
        assert stats.has_label_passed_thresholds is True

    def test_format_request_stats_empty_data(self):
        result = format_request_stats([])

        assert len(result) == 1
        assert len(result[0].request_stats) == 0
        assert result[0].execution_id == 0


class TestFormatSummaryReport:

    def test_format_summary_report_basic(self):
        api_data = [[
            {
                "summary": [
                    {
                        "id": "ALL",
                        "hits": 5000,
                        "failed": 25,
                        "avg": 120.5,
                        "min": 50,
                        "max": 500,
                        "tp90": 200,
                        "tp95": 250,
                        "tp99": 300,
                        "median": 115,
                        "hits_avg": 83.33,
                        "duration": 60,
                        "size_avg": 1024.5,
                        "bytes": 5122500,
                        "maxUsers": 50
                    }
                ]
            }
        ]]

        result = format_summary_report(api_data, {
            "execution_id": 12345,
            "execution_name": "Test Summary Execution"
        })

        assert len(result) == 1
        report = result[0]
        assert report.execution_id == 12345
        assert report.execution_name == "Test Summary Execution"
        assert report.context is not None
        assert len(report.context) > 0
        assert "SUMMARY REPORT METRICS EXPLANATION" in report.context

        metrics = report.overall_metrics
        assert metrics.total_requests == 5000
        assert metrics.total_errors == 25
        assert metrics.error_rate_percent == 0.5
        assert metrics.average_response_time_ms == 120.5
        assert metrics.min_response_time_ms == 50
        assert metrics.max_response_time_ms == 500
        assert metrics.percentile_90_ms == 200
        assert metrics.percentile_95_ms == 250
        assert metrics.percentile_99_ms == 300
        assert metrics.median_response_time_ms == 115
        assert metrics.average_throughput_per_second == 83.33
        assert metrics.total_duration_seconds == 60
        assert metrics.average_bytes_per_request == 1024.5
        assert metrics.total_bytes == 5122500
        assert metrics.max_concurrent_users == 50

class TestFormatErrorReport:

    def test_format_error_report_basic(self):
        api_data = [
            {
                "labelId": "login-label",
                "name": "Login",
                "errors": [
                    {"rc": "500", "m": "Internal Server Error", "count": 3},
                ],
                "assertions": [
                    {
                        "name": "Response contains success",
                        "failureMessage": "Text 'success' not found",
                        "failures": 2,
                    }
                ],
                "failedEmbeddedResources": [
                    {
                        "rc": "404",
                        "rm": "Not Found",
                        "count": 1,
                    }
                ],
                "urls": [
                    {
                        "url": "https://example.com/login",
                        "count": 4,
                    }
                ],
            }
        ]

        result = format_error_report(
            api_data,
            {
                "execution_id": 999,
                "execution_name": "Error Report Execution",
            },
        )

        # One report with correct metadata and context
        assert len(result) == 1
        report = result[0]
        assert report.execution_id == 999
        assert report.execution_name == "Error Report Execution"
        assert report.context is not None
        assert len(report.context) > 0
        assert "ERROR REPORT METRICS EXPLANATION" in report.context

        # Label errors structure
        assert len(report.label_errors) == 1
        label = report.label_errors[0]
        assert label.label_id == "login-label"
        assert label.label_name == "Login"

        # HTTP errors
        assert len(label.http_errors) == 1
        http_error = label.http_errors[0]
        assert http_error.response_code == "500"
        assert http_error.response_message == "Internal Server Error"
        assert http_error.error_count == 3

        # Assertion errors
        assert len(label.assertion_errors) == 1
        assertion = label.assertion_errors[0]
        assert assertion.assertion_name == "Response contains success"
        assert assertion.failure_message == "Text 'success' not found"
        assert assertion.failures == 2

        # Failed embedded resources
        assert len(label.failed_embedded_resources) == 1
        resource = label.failed_embedded_resources[0]
        assert resource.response_code == "404"
        assert resource.response_message == "Not Found"
        assert resource.resource_count == 1

        # Failed URLs
        assert len(label.failed_urls) == 1
        failed_url = label.failed_urls[0]
        assert failed_url.url == "https://example.com/login"
        assert failed_url.failure_count == 4

        # Totals
        assert label.total_errors_for_label == 3 + 2 + 1 + 4
        assert report.total_errors == 3 + 2 + 1 + 4


class TestFormatAnomaliesStats:

    def test_statistics_unavailable_empty_api_result(self):
        result = format_anomalies_stats([], {"execution_id": 123, "execution_name": "Test"})

        assert len(result) == 1
        report = result[0]
        expected_report_subset = {
            "anomaly_detection_status": "statistics_unavailable",
            "anomaly_count": None,
            "anomalies": [],
        }
        assert report.model_dump(
            include={
                "anomaly_detection_status": True,
                "anomaly_count": True,
                "anomalies": True,
            }
        ) == expected_report_subset
        assert report.statistics_unavailable_reason is not None
        assert "ANOMALY DETECTION RESPONSE" in report.context

    def test_no_anomalies(self):
        api = [
            {
                "anomalyCount": 0,
                "affectedLabel": [],
                "anomalies": [],
            }
        ]
        result = format_anomalies_stats(api, {"execution_id": 456, "execution_name": "No anomalies run"})

        assert len(result) == 1
        report = result[0]
        expected_report_subset = {
            "anomaly_detection_status": "no_anomalies",
            "anomaly_count": 0,
            "labels_affected": [],
            "anomalies": [],
            "statistics_unavailable_reason": None,
        }
        assert report.model_dump(
            include={
                "anomaly_detection_status": True,
                "anomaly_count": True,
                "labels_affected": True,
                "anomalies": True,
                "statistics_unavailable_reason": True,
            }
        ) == expected_report_subset

    def test_anomalies_with_details(self):
        api = [
            {
                "anomalyCount": 2,
                "affectedLabel": ["Login Page"],
                "anomalies": {
                    "id1": {
                        "anomalyId": "id1",
                        "masterId": "81627918",
                        "labelId": "lbl1",
                        "created": 1774026305007,
                        "kpi": "avg_rt",
                        "startTime": 1774026170,
                        "endTime": 1774026324,
                        "maxSpikeHeight": 5112.42,
                        "labelName": "Login Page",
                    },
                    "id2": {
                        "anomalyId": "id2",
                        "masterId": "81627918",
                        "labelId": "lbl1",
                        "created": 1774026305007,
                        "kpi": "pec99_rt",
                        "startTime": 1774026170,
                        "endTime": 1774026322,
                        "maxSpikeHeight": 5447.52,
                        "labelName": "Login Page",
                    },
                },
            }
        ]
        result = format_anomalies_stats(api, {"execution_id": 81627918, "execution_name": "With anomalies"})
        report = result[0]

        expected_report_subset = {
            "anomaly_detection_status": "anomalies_with_details",
            "anomaly_count": 2,
            "labels_affected": [
                {"ref_id": 1, "label_id": "lbl1", "label_name": "Login Page"},
            ],
            "kpi_affected": [
                {"kpi_ref_id": 1, "kpi_id": "avg_rt", "kpi_name": "Average response time"},
                {"kpi_ref_id": 2, "kpi_id": "pec99_rt", "kpi_name": "99th percentile response time"},
            ],
            "anomalies": [
                {"ref_id": 1, "kpi_ref_id": 1, "max_spike_height": 5112.42},
                {"ref_id": 1, "kpi_ref_id": 2, "max_spike_height": 5447.52},
            ],
        }
        assert report.model_dump(
            include={
                "anomaly_detection_status": True,
                "anomaly_count": True,
                "labels_affected": {"__all__": {"ref_id", "label_id", "label_name"}},
                "kpi_affected": {"__all__": {"kpi_ref_id", "kpi_id", "kpi_name"}},
                "anomalies": {"__all__": {"ref_id", "kpi_ref_id", "max_spike_height"}},
            }
        ) == expected_report_subset
