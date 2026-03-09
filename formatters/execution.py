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
from typing import Any, List, Optional, Dict

from config.blazemeter import BZM_BASE_URL
from models.execution import (
    TestExecution, TestExecutionDetailed, TestExecutionStatus, TestExecutionStatuses,
    SummaryReport, SummaryReportMetrics
)
from tools.utils import get_date_time_iso


def format_executions(executions: List[Any], params: Optional[dict] = None) -> List[TestExecution]:
    formatted_executions = []
    for execution in executions:
        execution_id = execution.get("id")
        execution_name = execution.get("name")
        project_id = execution.get("projectId")
        formatted_executions.append(
            TestExecution(
                execution_id=execution_id,
                execution_name=execution_name,
                project_id=project_id,
                execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}"
            )
        )
    return formatted_executions


def format_executions_detailed(executions: List[Any], params: Optional[dict] = None) -> List[TestExecutionDetailed]:
    formatted_executions = []
    for execution in executions:
        execution_id = execution.get("id")
        formatted_executions.append(
            TestExecutionDetailed(
                execution_id=execution_id,
                execution_name=execution.get("name"),
                execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}",
                created=get_date_time_iso(execution.get("created")),
                updated=get_date_time_iso(execution.get("updated")),
                ended=get_date_time_iso(execution.get("ended")),
                project_id=execution.get("projectId"),
                execution_status=execution.get("reportStatus", "unset"),
                execution_status_detailed=None
            )
        )
    return formatted_executions


def format_executions_status(statuses: List[Any], params: Optional[dict] = None) -> List[TestExecutionStatus]:
    formatted_statuses = []
    for status_element in statuses:
        execution_step = status_element.get("executionStep", "Unknown")
        status = status_element.get("statuses")
        formatted_statuses.append(
            TestExecutionStatus(
                progress_percent=status.get("ended", 0),
                execution_step=execution_step,
                execution_statuses=TestExecutionStatuses(
                    pending_percent=status.get("pending", 0),
                    booting_percent=status.get("booting", 0),
                    downloading_percent=status.get("downloading", 0),
                    ready_percent=status.get("ready", 0),
                    ended_percent=status.get("ended", 0),
                )
            )
        )
    return formatted_statuses


def format_summary_report(summary_data: List[Any], params: Optional[dict] = None) -> List[SummaryReport]:
    """
    Format summary report data from BlazeMeter API into a structured, AI-friendly format.
    
    The API returns summary data in a nested structure: [[{summary_data}]]
    This function extracts and normalizes the data, adding context and clear field names.
    """
    formatted_reports = []
    execution_id = params.get("execution_id") if params else None
    execution_name = params.get("execution_name") if params else None
    
    # Handle nested structure: summary_data is typically [[{...}]]
    summary_list = summary_data
    if summary_data and isinstance(summary_data[0], list):
        summary_list = summary_data[0]
    
    for summary_item in summary_list:
        if not isinstance(summary_item, dict):
            continue
            
        # Extract the actual summary data (usually nested in 'summary' array)
        summary_array = summary_item.get("summary", [])
        if not summary_array:
            continue
            
        # Get the overall metrics (usually the first item with id="ALL" or the first item)
        overall_data = None
        for item in summary_array:
            if isinstance(item, dict):
                if item.get("id") == "ALL" or item.get("lb") == "ALL":
                    overall_data = item
                    break
        
        # Fallback to first item if no "ALL" found
        if not overall_data and summary_array:
            overall_data = summary_array[0] if isinstance(summary_array[0], dict) else None
        
        if not overall_data:
            continue
        
        # Extract metrics with safe defaults
        hits = overall_data.get("hits", 0)
        failed = overall_data.get("failed", 0)
        error_rate = (failed / hits * 100) if hits > 0 else 0.0
        
        metrics = SummaryReportMetrics(
            total_requests=hits,
            total_errors=failed,
            error_rate_percent=round(error_rate, 2),
            average_response_time_ms=round(overall_data.get("avg", 0), 2),
            min_response_time_ms=overall_data.get("min", 0),
            max_response_time_ms=overall_data.get("max", 0),
            percentile_90_ms=overall_data.get("tp90", 0),
            percentile_95_ms=overall_data.get("tp95", overall_data.get("tp90", 0)),  # Fallback if tp95 not available
            percentile_99_ms=overall_data.get("tp99", overall_data.get("tp90", 0)),  # Fallback if tp99 not available
            median_response_time_ms=overall_data.get("median", overall_data.get("avg", 0)),
            average_throughput_per_second=round(overall_data.get("hits_avg", 0), 2),
            total_duration_seconds=overall_data.get("duration", 0),
            average_bytes_per_request=round(overall_data.get("size_avg", 0), 2),
            total_bytes=overall_data.get("bytes", 0),
            max_concurrent_users=overall_data.get("maxUsers", overall_data.get("concurrency", 0))
        )
        
        report = SummaryReport(
            execution_id=execution_id or 0,
            execution_name=execution_name,
            execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}" if execution_id else "",
            overall_metrics=metrics,
            context=_get_summary_context()
        )
        
        formatted_reports.append(report)
    
    return formatted_reports


def _get_summary_context() -> str:
    """Provide context about summary report metrics for AI interpretation."""
    return (
        "SUMMARY REPORT METRICS EXPLANATION:\n"
        "This summary report provides overall performance metrics for a test execution.\n\n"
        "KEY METRICS:\n"
        "- total_requests: Total number of HTTP requests executed\n"
        "- total_errors: Number of requests that failed (non-2xx/3xx responses or timeouts)\n"
        "- error_rate_percent: Percentage of failed requests (total_errors / total_requests * 100)\n"
        "- average_response_time_ms: Mean response time across all requests\n"
        "- percentile_90_ms: 90% of requests completed faster than this time (important for SLA monitoring)\n"
        "- percentile_95_ms: 95% of requests completed faster than this time\n"
        "- percentile_99_ms: 99% of requests completed faster than this time (catches outliers)\n"
        "- median_response_time_ms: Middle value when all response times are sorted (less affected by outliers than average)\n"
        "- average_throughput_per_second: Average requests per second (indicates system capacity)\n"
        "- total_duration_seconds: How long the test ran\n"
        "- max_concurrent_users: Peak number of simultaneous virtual users\n\n"
        "INTERPRETATION GUIDANCE:\n"
        "- Compare percentiles to average: Large gaps indicate inconsistent performance\n"
        "- High error_rate_percent (>1%) suggests system issues or misconfiguration\n"
        "- Response times should be consistent across percentiles for stable systems\n"
        "- Throughput indicates system capacity under load\n"
        "- Use request_stats for per-endpoint breakdown (available via read_request_stats action)\n\n"
        "For more details about the summary report, consult the BlazeMeter skill blazemeter-performance-testing and read the related reporting resource\n"
    )
