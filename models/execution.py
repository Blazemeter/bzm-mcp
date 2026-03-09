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
from typing import Optional

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


class SummaryReportMetrics(BaseModel):
    """Performance metrics for a test execution summary."""
    total_requests: int = Field(description="Total number of requests (hits) executed during the test")
    total_errors: int = Field(description="Total number of failed requests")
    error_rate_percent: float = Field(description="Percentage of requests that failed")
    average_response_time_ms: float = Field(description="Average response time in milliseconds")
    min_response_time_ms: int = Field(description="Minimum response time in milliseconds")
    max_response_time_ms: int = Field(description="Maximum response time in milliseconds")
    percentile_90_ms: float = Field(description="90th percentile response time in milliseconds (90% of requests were faster)")
    percentile_95_ms: float = Field(description="95th percentile response time in milliseconds (95% of requests were faster)")
    percentile_99_ms: float = Field(description="99th percentile response time in milliseconds (99% of requests were faster)")
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
    overall_metrics: SummaryReportMetrics = Field(description="Overall performance metrics aggregated across all requests")
    context: str = Field(description="Explanatory context about the summary report format and metrics")
