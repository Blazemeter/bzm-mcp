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
from typing import List, Optional

from pydantic import BaseModel, Field


class TestExecution(BaseModel):
    """Test execution basic information structure."""
    execution_id: int = Field(
        description="The unique identifier of the execution. This is known as the masterId or test execution id")
    execution_name: str = Field(description="The test execution report name")
    project_id: int = Field(description="The project id of the test execution")
    execution_url: str = Field(description="The test execution report URL")


class TestExecutionStatuses(BaseModel):
    pending_percent: int = Field("Percent of machines that are still being provisioned")
    booting_percent: int = Field("Percent of machines that are booting")
    downloading_percent: int = Field("Percent of machines that are downloading necessary files")
    ready_percent: int = Field("Percent of machines that are ready to start")
    ended_percent: int = Field("Percent of machines that have finished running")


class TestExecutionStatus(BaseModel):
    progress_percent: int = Field("The current progress percent of the execution. Range from 0 to 100.")
    execution_step: str = Field("The current status step of this execution.")
    execution_statuses: TestExecutionStatuses = Field(
        "A percentage breakdown of all the session status for this execution")


class TestExecutionDetailed(TestExecution):
    created: Optional[str] = Field(description="The datetime that the test execution was started.", default=None)
    updated: Optional[str] = Field(description="The datetime that the test execution was updated", default=None)
    ended: Optional[str] = Field(description="The datetime that the test execution was ended.", default=None)
    execution_status: str = Field(
        description="Indicates the ending status of the test execution. Value can be pass, fail, unset, error, abort, or noData")
    execution_status_detailed: Optional[TestExecutionStatus] = Field(
        "Indicates the current status of the test execution.")
    archived: Optional[bool] = Field(description="If the execution report was archived", default=None)


class SummaryReportMetrics(BaseModel):
    """Performance metrics for a test execution summary."""
    total_requests: int = Field(description="Total number of requests (hits) executed during the test")
    total_errors: int = Field(description="Total number of failed requests")
    error_rate_percent: float = Field(description="Percentage of requests that failed")
    average_response_time_ms: float = Field(description="Average response time in milliseconds")
    min_response_time_ms: int = Field(description="Minimum response time in milliseconds")
    max_response_time_ms: int = Field(description="Maximum response time in milliseconds")
    percentile_90_ms: float = Field(
        description="90th percentile response time in milliseconds (90% of requests were faster)")
    percentile_95_ms: float = Field(
        description="95th percentile response time in milliseconds (95% of requests were faster)")
    percentile_99_ms: float = Field(
        description="99th percentile response time in milliseconds (99% of requests were faster)")
    median_response_time_ms: float = Field(description="Median (50th percentile) response time in milliseconds")
    average_throughput_per_second: float = Field(description="Average number of requests per second")
    total_duration_seconds: int = Field(description="Total test duration in seconds")
    average_bytes_per_request: float = Field(description="Average response size in bytes")
    total_bytes: int = Field(description="Total bytes transferred")
    max_concurrent_users: int = Field(description="Maximum number of concurrent virtual users")


class SummaryReport(BaseModel):
    """Formatted summary report for a test execution."""
    execution_id: int = Field(description="The execution ID this summary belongs to")
    execution_name: Optional[str] = Field(description="The execution name", default=None)
    execution_url: str = Field(description="URL to view this execution in BlazeMeter")
    overall_metrics: SummaryReportMetrics = Field(
        description="Overall performance metrics aggregated across all requests")
    context: str = Field(description="Explanatory context about the summary report format and metrics")


class RequestStatMetrics(BaseModel):
    """Performance metrics for a specific request label/endpoint."""
    label_id: str = Field(description="Unique identifier for the request label")
    label_name: str = Field(description="Name of the request label (endpoint name)")
    samples: int = Field(description="Total number of requests executed for this label")
    avg_response_time_ms: float = Field(description="Average response time in milliseconds")
    percentile_90_ms: float = Field(description="90th percentile response time in milliseconds")
    percentile_95_ms: float = Field(description="95th percentile response time in milliseconds")
    percentile_99_ms: float = Field(description="99th percentile response time in milliseconds")
    min_response_time_ms: int = Field(description="Minimum response time in milliseconds")
    max_response_time_ms: int = Field(description="Maximum response time in milliseconds")
    avg_latency_ms: float = Field(description="Average latency in milliseconds")
    standard_deviation_ms: float = Field(description="Standard deviation of response times")
    duration_seconds: int = Field(description="Duration of the test period for this label")
    avg_bytes: float = Field(description="Average response size in bytes")
    avg_throughput_per_second: float = Field(description="Average requests per second for this label")
    median_response_time_ms: float = Field(description="Median (50th percentile) response time in milliseconds")
    geometric_mean_response_time_ms: Optional[float] = Field(
        description="Geometric mean response time in milliseconds (less affected by outliers than arithmetic mean)",
        default=None)
    errors_count: int = Field(description="Total number of errors for this label")
    errors_rate_percent: float = Field(description="Percentage of requests that failed for this label")
    concurrency: int = Field(description="Number of concurrent users for this label")
    has_label_passed_thresholds: Optional[bool] = Field(
        description="Indicates whether this label passed the configured performance thresholds", default=None)


class RequestStatsReport(BaseModel):
    """Formatted request statistics report for a test execution."""
    execution_id: int = Field(description="The execution ID this report belongs to")
    execution_name: Optional[str] = Field(description="The execution name", default=None)
    execution_url: str = Field(description="URL to view this execution in BlazeMeter")
    request_stats: List[RequestStatMetrics] = Field(description="Performance metrics for each request label/endpoint")
    context: str = Field(description="Explanatory context about the request stats report format and metrics")


class HttpError(BaseModel):
    """HTTP error information."""
    response_code: Optional[str] = Field(
        description="HTTP response code of the error (e.g., '404', '500', empty string for transaction errors)",
        default=None)
    response_message: str = Field(description="Error message or description")
    error_count: int = Field(description="Number of times this specific HTTP error occurred")


class AssertionError(BaseModel):
    """Assertion failure information."""
    assertion_name: str = Field(description="Name of the assertion that failed")
    failure_message: str = Field(description="Message describing why the assertion failed")
    failures: int = Field(description="Number of times this assertion failed")


class FailedEmbeddedResource(BaseModel):
    """Failed embedded resource information (e.g., CSS, JS, images)."""
    response_code: str = Field(description="HTTP response code of the failed resource")
    response_message: str = Field(description="Error message for the failed resource")
    resource_count: int = Field(description="Number of times this resource failed to load")


class FailedUrl(BaseModel):
    """Failed URL information."""
    url: str = Field(description="URL that failed to load")
    failure_count: int = Field(description="Number of times this URL failed")


class LabelErrors(BaseModel):
    """Error information for a specific label/endpoint."""
    label_id: str = Field(description="Unique identifier for the request label")
    label_name: str = Field(description="Name of the endpoint/label (e.g., 'Login', 'Homepage', 'ALL')")
    http_errors: List[HttpError] = Field(description="List of HTTP errors (response codes) for this label",
                                         default_factory=list)
    assertion_errors: List[AssertionError] = Field(description="List of assertion failures for this label",
                                                   default_factory=list)
    failed_embedded_resources: List[FailedEmbeddedResource] = Field(
        description="List of failed embedded resources (CSS, JS, images) for this label", default_factory=list)
    failed_urls: List[FailedUrl] = Field(description="List of failed URLs for this label", default_factory=list)
    total_errors_for_label: int = Field(
        description="Total number of errors (HTTP + assertions + embedded resources) for this label")


class ErrorReport(BaseModel):
    """Formatted error report for a test execution."""
    execution_id: int = Field(description="The execution ID this error report belongs to")
    execution_name: Optional[str] = Field(description="The execution name", default=None)
    execution_url: str = Field(description="URL to view this execution in BlazeMeter")
    label_errors: List[LabelErrors] = Field(description="List of errors grouped by label/endpoint")
    total_errors: int = Field(description="Total number of errors across all labels and error types")
    context: str = Field(description="Explanatory context about the error report format and metrics")
