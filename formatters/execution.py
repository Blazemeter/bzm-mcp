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
from typing import Any, List, Optional

from config.blazemeter import BZM_BASE_URL
from models.execution import (
    TestExecution, TestExecutionDetailed, TestExecutionStatus, TestExecutionStatuses,
    SummaryReport, SummaryReportMetrics,
    RequestStatsReport, RequestStatMetrics,
    ErrorReport, LabelErrors, HttpError, AssertionError, FailedEmbeddedResource, FailedUrl,
    AffectedKpi,
    AffectedLabel,
    AnomalyDetail,
    AnomalyDetectionReport,
)
from tools.utils import get_date_time_iso


def _build_execution_url(execution_id: Optional[int]) -> str:
    """Build execution URL from execution ID."""
    return f"{BZM_BASE_URL}/app/#/masters/{execution_id}" if execution_id else ""


def _calculate_error_rate(errors_count: int, total_count: int, existing_rate: float = 0.0) -> float:
    """Calculate error rate percentage if not already provided."""
    if existing_rate and existing_rate > 0:
        return existing_rate
    if total_count and total_count > 0 and errors_count > 0:
        return (errors_count / total_count) * 100
    return 0.0


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
                archived=execution.get("dumped", False),
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
        error_rate = _calculate_error_rate(failed, hits)

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
            execution_url=_build_execution_url(execution_id),
            overall_metrics=metrics,
            context=_get_summary_context()
        )

        formatted_reports.append(report)

    return formatted_reports


def _get_common_metrics_explanation() -> str:
    """Common metrics explanation shared across report types."""
    return (
        "- avg_response_time_ms: Mean response time across all requests\n"
        "- percentile_90_ms: 90% of requests completed faster than this time (important for SLA monitoring)\n"
        "- percentile_95_ms: 95% of requests completed faster than this time\n"
        "- percentile_99_ms: 99% of requests completed faster than this time (catches outliers)\n"
        "- median_response_time_ms: Middle value when all response times are sorted (less affected by outliers than average)\n"
        "- min_response_time_ms: Fastest response time\n"
        "- max_response_time_ms: Slowest response time\n"
        "- avg_throughput_per_second: Average requests per second (indicates system capacity)\n"
        "- errors_count: Total number of failed requests\n"
        "- errors_rate_percent: Percentage of requests that failed\n"
    )


def _get_common_interpretation_guidance() -> str:
    """Common interpretation guidance shared across report types."""
    return (
        "- Compare percentiles to average: Large gaps indicate inconsistent performance\n"
        "- High errors_rate_percent (>1%) suggests system issues or misconfiguration\n"
        "- Response times should be consistent across percentiles for stable systems\n"
        "- Throughput indicates system capacity under load\n"
        "- Compare percentile_99_ms to avg_response_time_ms to identify outliers\n"
    )


def _get_summary_context() -> str:
    """Provide context about summary report metrics for AI interpretation."""
    return (
            "SUMMARY REPORT METRICS EXPLANATION:\n"
            "This summary report provides overall performance metrics for a test execution.\n\n"
            "KEY METRICS:\n"
            "- total_requests: Total number of HTTP requests executed\n"
            "- total_errors: Number of requests that failed (non-2xx/3xx responses or timeouts)\n"
            "- error_rate_percent: Percentage of failed requests (total_errors / total_requests * 100)\n"
            + _get_common_metrics_explanation() +
            "- total_duration_seconds: How long the test ran\n"
            "- max_concurrent_users: Peak number of simultaneous virtual users\n"
            "- average_bytes_per_request: Average response size in bytes\n"
            "- total_bytes: Total bytes transferred\n\n"
            "INTERPRETATION GUIDANCE:\n"
            + _get_common_interpretation_guidance() +
            "- Use request_stats for per-endpoint breakdown (available via read_request_stats action)\n\n"
            "For more details about the summary report, consult the BlazeMeter skill blazemeter-performance-testing and read the related reporting resource\n"
            "**CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.\n"
    )


def format_request_stats(request_stats_data: List[Any], params: Optional[dict] = None) -> List[RequestStatsReport]:
    """
    Format request statistics data from BlazeMeter API into a structured, AI-friendly format.
    
    The API returns request stats as a list of objects, one per endpoint/label.
    This function normalizes field names and adds context for AI interpretation.
    """
    formatted_reports = []
    execution_id = params.get("execution_id") if params else None
    execution_name = params.get("execution_name") if params else None

    # Handle case where data might be nested
    stats_list = request_stats_data
    if request_stats_data and isinstance(request_stats_data[0], list):
        stats_list = request_stats_data[0]

    formatted_stats = []
    for stat_item in stats_list:
        if not isinstance(stat_item, dict):
            continue

        # Calculate error rate if not provided
        samples = stat_item.get("samples", 0)
        errors_count = stat_item.get("errorsCount", 0)
        errors_rate = _calculate_error_rate(errors_count, samples, stat_item.get("errorsRate", 0))

        metrics = RequestStatMetrics(
            label_id=stat_item.get("labelId", ""),
            label_name=stat_item.get("labelName", "Unknown"),
            samples=samples,
            avg_response_time_ms=round(stat_item.get("avgResponseTime", 0), 2),
            percentile_90_ms=stat_item.get("90line", 0),
            percentile_95_ms=stat_item.get("95line", 0),
            percentile_99_ms=stat_item.get("99line", 0),
            min_response_time_ms=stat_item.get("minResponseTime", 0),
            max_response_time_ms=stat_item.get("maxResponseTime", 0),
            avg_latency_ms=round(stat_item.get("avgLatency", 0), 2),
            standard_deviation_ms=round(stat_item.get("stDev", 0), 2),
            duration_seconds=stat_item.get("duration", 0),
            avg_bytes=round(stat_item.get("avgBytes", 0), 2),
            avg_throughput_per_second=round(stat_item.get("avgThroughput", 0), 2),
            median_response_time_ms=stat_item.get("medianResponseTime", 0),
            geometric_mean_response_time_ms=round(stat_item.get("geoMeanResponseTime"), 2) if stat_item.get(
                "geoMeanResponseTime") is not None else None,
            errors_count=errors_count,
            errors_rate_percent=round(errors_rate, 2),
            concurrency=stat_item.get("concurrency", 0),
            has_label_passed_thresholds=stat_item.get("hasLabelPassedThresholds")
        )

        formatted_stats.append(metrics)

    # Create report with all stats and context
    report = RequestStatsReport(
        execution_id=execution_id or 0,
        execution_name=execution_name,
        execution_url=_build_execution_url(execution_id),
        request_stats=formatted_stats,
        context=_get_request_stats_context()
    )

    formatted_reports.append(report)
    return formatted_reports


def _get_request_stats_context() -> str:
    """Provide context about request stats report metrics for AI interpretation."""
    return (
            "REQUEST STATS REPORT METRICS EXPLANATION:\n"
            "This report provides performance metrics for each request label/endpoint in the test execution.\n\n"
            "KEY METRICS PER ENDPOINT:\n"
            "- label_id: Unique identifier for the request label\n"
            "- label_name: Name of the endpoint/request (e.g., 'Login', 'Homepage', 'View Product')\n"
            "- samples: Total number of requests executed for this endpoint\n"
            + _get_common_metrics_explanation() +
            "- avg_latency_ms: Average network latency (time to first byte) for this endpoint\n"
            "- standard_deviation_ms: Measure of response time variability (higher = more inconsistent)\n"
            "- duration_seconds: Duration of the test period for this endpoint\n"
            "- avg_bytes: Average response size in bytes for this endpoint\n"
            "- geometric_mean_response_time_ms: Geometric mean response time (less affected by outliers than arithmetic mean, useful for skewed distributions)\n"
            "- concurrency: Number of concurrent users hitting this endpoint\n"
            "- has_label_passed_thresholds: Indicates whether this endpoint passed configured performance thresholds (null if thresholds not configured)\n\n"
            "INTERPRETATION GUIDANCE:\n"
            "- Compare avg_response_time_ms across endpoints to identify slow endpoints\n"
            + _get_common_interpretation_guidance() +
            "- Standard deviation indicates consistency: lower = more consistent, higher = more variable\n"
            "- Use this report to drill down into specific endpoint performance issues\n"
            "- The 'ALL' label (if present) shows aggregated metrics across all endpoints\n"
            "**CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.\n"
    )


def format_error_report(error_data: List[Any], params: Optional[dict] = None) -> List[ErrorReport]:
    """
    Format error report data from BlazeMeter API into a structured, AI-friendly format.
    
    The API returns error data as a list of label objects, each containing arrays of:
    - errors: HTTP errors with response codes and messages
    - assertions: Assertion failures
    - failedEmbeddedResources: Failed CSS/JS/images
    - urls: Failed URLs
    This function normalizes field names and adds context for AI interpretation.
    """
    formatted_reports = []
    execution_id = params.get("execution_id") if params else None
    execution_name = params.get("execution_name") if params else None

    label_list = error_data
    if error_data and isinstance(error_data[0], list):
        label_list = error_data[0]

    formatted_label_errors = []
    total_errors = 0

    for label_item in label_list:
        if not isinstance(label_item, dict):
            continue

        label_id = label_item.get("labelId", "")
        label_name = label_item.get("name", label_item.get("_id", "Unknown"))

        # Process HTTP errors
        http_errors = []
        errors_array = label_item.get("errors", [])
        for error_obj in errors_array:
            if isinstance(error_obj, dict):
                http_errors.append(HttpError(
                    response_code=error_obj.get("rc") if error_obj.get("rc") else None,
                    response_message=error_obj.get("m", ""),
                    error_count=error_obj.get("count", 0)
                ))
                total_errors += error_obj.get("count", 0)

        # Process assertion errors
        assertion_errors = []
        assertions_array = label_item.get("assertions", [])
        for assertion_obj in assertions_array:
            if isinstance(assertion_obj, dict):
                failures = assertion_obj.get("failures", 0)
                assertion_errors.append(AssertionError(
                    assertion_name=assertion_obj.get("name", ""),
                    failure_message=assertion_obj.get("failureMessage", ""),
                    failures=failures
                ))
                total_errors += failures

        # Process failed embedded resources
        failed_resources = []
        failed_embedded_array = label_item.get("failedEmbeddedResources", [])
        for resource_obj in failed_embedded_array:
            if isinstance(resource_obj, dict):
                resource_count = resource_obj.get("count", 0)
                failed_resources.append(FailedEmbeddedResource(
                    response_code=resource_obj.get("rc", ""),
                    response_message=resource_obj.get("rm", ""),
                    resource_count=resource_count
                ))
                total_errors += resource_count

        # Process failed URLs
        failed_urls = []
        urls_array = label_item.get("urls", [])
        for url_obj in urls_array:
            if isinstance(url_obj, dict):
                url_count = url_obj.get("count", 0)
                failed_urls.append(FailedUrl(
                    url=url_obj.get("url", ""),
                    failure_count=url_count
                ))
                total_errors += url_count

        # Calculate total errors for this label
        label_total = sum(e.error_count for e in http_errors) + \
                      sum(a.failures for a in assertion_errors) + \
                      sum(r.resource_count for r in failed_resources) + \
                      sum(u.failure_count for u in failed_urls)

        label_error = LabelErrors(
            label_id=label_id,
            label_name=label_name,
            http_errors=http_errors,
            assertion_errors=assertion_errors,
            failed_embedded_resources=failed_resources,
            failed_urls=failed_urls,
            total_errors_for_label=label_total
        )

        formatted_label_errors.append(label_error)

    # Create report with all label errors and context
    report = ErrorReport(
        execution_id=execution_id or 0,
        execution_name=execution_name,
        execution_url=_build_execution_url(execution_id),
        label_errors=formatted_label_errors,
        total_errors=total_errors,
        context=_get_error_report_context()
    )

    formatted_reports.append(report)
    return formatted_reports


def _get_error_report_context() -> str:
    """Provide context about error report metrics for AI interpretation."""
    return (
        "ERROR REPORT METRICS EXPLANATION:\n"
        "This report lists errors that occurred during test execution, grouped by endpoint/label.\n\n"

        "STRUCTURE:\n"
        "The report contains label_errors entries. Each entry represents errors for a specific endpoint and includes four arrays:\n"
        "1. http_errors – HTTP response code errors\n"
        "2. assertion_errors – Custom assertion failures\n"
        "3. failed_embedded_resources – Failed CSS, JavaScript, or image resources\n"
        "4. failed_urls – Failed URL requests\n\n"

        "KEY METRICS PER LABEL:\n"
        "- label_id: request label/endpoint\n"
        "- label_name: Endpoint/request name\n"
        "- total_errors_for_label: Total errors for this label (HTTP + assertions + embedded resources + URLs)\n\n"

        "HTTP ERRORS:\n"
        "- response_code: HTTP status code (e.g., '404', '500', '401'; empty string may indicate transaction/connection errors)\n"
        "- response_message: Server error message\n"
        "- error_count: Number of occurrences\n\n"

        "ASSERTION ERRORS:\n"
        "- assertion_name: Failed assertion name\n"
        "- failure_message: Reason for the failure\n"
        "- failures: Number of occurrences\n\n"

        "FAILED EMBEDDED RESOURCES:\n"
        "- response_code: HTTP status code\n"
        "- response_message: Error message\n"
        "- resource_count: Number of failed loads\n\n"

        "FAILED URLS:\n"
        "- url: Failed URL\n"
        "- failure_count: Number of failures\n\n"

        "OVERALL METRIC:\n"
        "- total_errors: Sum of all errors across labels and types\n\n"

        "INTERPRETATION GUIDANCE:\n"
        "- 'ALL' label aggregates errors across endpoints for overall analysis\n"
        "- Group by response_code to identify HTTP patterns (4xx client errors, 5xx server errors)\n"
        "- Group by label_name to identify endpoints with the most failures\n"
        "- Empty response_code often indicates transaction or connection issues\n"
        "- High counts suggest systemic problems rather than isolated failures\n"
        "- Failed embedded resources may cause UI issues but not necessarily functional failures\n"
        "- Assertion errors indicate validation failures; review failure_message for expected conditions\n"
        "- Compare total_errors with total_requests from the summary report to calculate error rate\n"
        "- Same response_code across labels suggests widespread issues; different codes in one label may indicate intermittent problems\n\n"

        "SKILL CATEGORIES FOR RESOLVING ERRORS:\n"
        "- blazemeter-performance-testing: Analyze error patterns and assertion failures\n"
        "- blazemeter-integrations: Troubleshoot scripts, authentication errors (401), and integrations\n"
        "- blazemeter-api-reference: Understand API error codes and response formats\n\n"

        "For deeper troubleshooting, consult the BlazeMeter skill blazemeter-performance-testing and related reporting resources.\n"
        "**CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.\n"
    )


KPI_CODE_TO_DISPLAY_NAME = {
    "avg_rt": "Average response time",
    "pec50_rt": "50th percentile response time",
    "pec90_rt": "90th percentile response time",
    "pec95_rt": "95th percentile response time",
    "pec99_rt": "99th percentile response time",
}


def _kpi_code_to_display_name(kpi_code: str) -> str:
    """Map BlazeMeter anomaly KPI codes to short display names for the LLM."""
    return KPI_CODE_TO_DISPLAY_NAME.get(kpi_code, kpi_code)


def _parse_anomalies_dict(
    rows: dict[str, Any],
    affected_names: List[str],
) -> tuple[List[AffectedLabel], List[AffectedKpi], List[AnomalyDetail]]:
    """
    Build labels_affected, kpi_affected, and per-row details from anomaly rows.

    This parser is intentionally label_id-first: dedupe, ref assignment, and detail linking
    are all keyed by label_id. affected_names is accepted for interface compatibility but
    does not drive ordering or filtering.
    """
    _ = affected_names

    kpi_affected: List[AffectedKpi] = []
    seen_kpi: set[str] = set()
    kpi_lookup: dict[str, int] = {}

    labels_affected: List[AffectedLabel] = []
    ref_lookup: dict[str, int] = {}
    seen_lids: set[str] = set()

    details: List[AnomalyDetail] = []

    def anomaly_detail(lid: str, kpi: str, st: Any, en: Any, spike: float) -> AnomalyDetail:
        return AnomalyDetail(
            ref_id=ref_lookup.get(lid, 0),
            kpi_ref_id=kpi_lookup.get(kpi) or 0,
            start_time=get_date_time_iso(int(st)) if st is not None else None,
            end_time=get_date_time_iso(int(en)) if en is not None else None,
            max_spike_height=spike,
        )

    for row in rows.values():
        if not isinstance(row, dict):
            continue

        lid = str(row.get("labelId", ""))
        lname = str(row.get("labelName", ""))

        if lid and lid not in seen_lids:
            seen_lids.add(lid)
            ref = len(labels_affected) + 1
            labels_affected.append(AffectedLabel(ref_id=ref, label_id=lid, label_name=lname))
            ref_lookup[lid] = ref

        kpi = str(row.get("kpi") or "")
        if kpi and kpi not in seen_kpi:
            seen_kpi.add(kpi)
            kpi_ref = len(kpi_affected) + 1
            kpi_affected.append(
                AffectedKpi(
                    kpi_ref_id=kpi_ref,
                    kpi_id=kpi,
                    kpi_name=_kpi_code_to_display_name(kpi),
                )
            )
            kpi_lookup[kpi] = kpi_ref

        st = row.get("startTime")
        en = row.get("endTime")
        spike = float(row.get("maxSpikeHeight", 0) or 0)
        details.append(anomaly_detail(lid, kpi, st, en, spike))

    return labels_affected, kpi_affected, details


def _get_anomalies_detection_context() -> str:
    """Context for interpreting anomaly stats and routing the LLM to skills."""
    return (
        "ANOMALY DETECTION RESPONSE — FIELD DEFINITIONS FOR THE LLM:\n"
        "- anomaly_detection_status: "
        "'no_anomalies' = API returned counts and anomaly_count is 0. "
        "'anomalies_with_details' = API returned counts and a list of anomalies with KPIs and time windows. "
        "'statistics_unavailable' = API returned no stats object (empty result); this token/account cannot retrieve "
        "anomaly statistics (e.g. free tier or anomaly detection not enabled). Do not invent counts.\n"
        "- anomaly_count: Total anomalies when statistics are available; 0 means none detected. "
        "Null only when statistics_unavailable (unknown to this tool).\n"
        "- labels_affected: Distinct labels with ref_id, label_id and label_name that had at least one anomaly.\n"
        "- kpi_affected: Distinct KPIs with kpi_ref_id, kpi_id (API key) and kpi_name (human-readable).\n"
        "- anomalies: Each row is one anomaly: ref_id (label), kpi_ref_id (KPI), start_time/end_time (ISO 8601), "
        "max_spike_height (spike severity for that KPI in that window).\n"
        "- statistics_unavailable_reason: Human-readable explanation when details cannot be shown.\n\n"
        "INTERPRETATION:\n"
        "- Prefer Timeline report in BlazeMeter UI to see anomalies visually; correlate with errors and KPIs.\n"
        "- Multiple rows per ref_id are normal (one per KPI).\n"
        "- When statistics_unavailable: state clearly that anomaly details are not available for this account/session; "
        "suggest checking workspace/plan or help on anomaly detection.\n\n"
        "SKILL ROUTING:\n"
        "- blazemeter-performance-testing: reporting.md (Timeline, anomaly testing), interpreting KPIs and next steps.\n"
        "- blazemeter-administration: workspaces-projects.md (who can enable anomaly detection).\n\n"
        "**CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.\n"
    )


def format_anomalies_stats(raw: List[Any], params: Optional[dict] = None) -> List[AnomalyDetectionReport]:
    """
    Normalize /anomalies/stats API payloads into a single structured report.

    The API may return:
    - An empty list when anomaly statistics are not available for the account.
    - A dict with anomalyCount, affectedLabel, and anomalies (object map or empty list when count is 0).
    """
    execution_id = params.get("execution_id") if params else None
    execution_name = params.get("execution_name") if params else None
    eid = execution_id or 0

    if not raw:
        return [
            AnomalyDetectionReport(
                execution_id=eid,
                execution_name=execution_name,
                execution_url=_build_execution_url(execution_id),
                anomaly_detection_status="statistics_unavailable",
                anomaly_count=None,
                labels_affected=[],
                kpi_affected=[],
                anomalies=[],
                statistics_unavailable_reason=(
                    "BlazeMeter returned no anomaly statistics for this execution. "
                    "This usually means anomaly detection is not available for your account or workspace "
                    "(for example a limited plan), or the feature is disabled. Per-anomaly details cannot be shown."
                ),
                context=_get_anomalies_detection_context(),
            )
        ]

    payload = raw[0]
    if not isinstance(payload, dict):
        return [
            AnomalyDetectionReport(
                execution_id=eid,
                execution_name=execution_name,
                execution_url=_build_execution_url(execution_id),
                anomaly_detection_status="statistics_unavailable",
                anomaly_count=None,
                labels_affected=[],
                kpi_affected=[],
                anomalies=[],
                statistics_unavailable_reason=(
                    "Unexpected anomaly statistics payload; could not parse structured anomaly data."
                ),
                context=_get_anomalies_detection_context(),
            )
        ]

    count = int(payload.get("anomalyCount", 0))
    affected = payload.get("affectedLabel") or []
    if not isinstance(affected, list):
        affected = []

    anomalies_raw = payload.get("anomalies")
    affected_names = [str(x) for x in affected]
    rows = anomalies_raw if isinstance(anomalies_raw, dict) else {}
    labels_affected, kpi_affected, details = _parse_anomalies_dict(rows, affected_names)

    if count == 0 and not details:
        status = "no_anomalies"
    elif details or count > 0:
        status = "anomalies_with_details"
    else:
        status = "no_anomalies"

    return [
        AnomalyDetectionReport(
            execution_id=eid,
            execution_name=execution_name,
            execution_url=_build_execution_url(execution_id),
            anomaly_detection_status=status,
            anomaly_count=count,
            labels_affected=labels_affected,
            kpi_affected=kpi_affected,
            anomalies=details,
            statistics_unavailable_reason=None,
            context=_get_anomalies_detection_context(),
        )
    ]


def format_request_stats(request_stats_data: List[Any], params: Optional[dict] = None) -> List[RequestStatsReport]:
    """
    Format request statistics data from BlazeMeter API into a structured, AI-friendly format.
    
    The API returns request stats as a list of objects, one per endpoint/label.
    This function normalizes field names and adds context for AI interpretation.
    """
    formatted_reports = []
    execution_id = params.get("execution_id") if params else None
    execution_name = params.get("execution_name") if params else None

    # Handle case where data might be nested
    stats_list = request_stats_data
    if request_stats_data and isinstance(request_stats_data[0], list):
        stats_list = request_stats_data[0]

    formatted_stats = []
    for stat_item in stats_list:
        if not isinstance(stat_item, dict):
            continue

        # Calculate error rate if not provided
        samples = stat_item.get("samples", 0)
        errors_count = stat_item.get("errorsCount", 0)
        errors_rate = _calculate_error_rate(errors_count, samples, stat_item.get("errorsRate", 0))

        metrics = RequestStatMetrics(
            label_id=stat_item.get("labelId", ""),
            label_name=stat_item.get("labelName", "Unknown"),
            samples=samples,
            avg_response_time_ms=round(stat_item.get("avgResponseTime", 0), 2),
            percentile_90_ms=stat_item.get("90line", 0),
            percentile_95_ms=stat_item.get("95line", 0),
            percentile_99_ms=stat_item.get("99line", 0),
            min_response_time_ms=stat_item.get("minResponseTime", 0),
            max_response_time_ms=stat_item.get("maxResponseTime", 0),
            avg_latency_ms=round(stat_item.get("avgLatency", 0), 2),
            standard_deviation_ms=round(stat_item.get("stDev", 0), 2),
            duration_seconds=stat_item.get("duration", 0),
            avg_bytes=round(stat_item.get("avgBytes", 0), 2),
            avg_throughput_per_second=round(stat_item.get("avgThroughput", 0), 2),
            median_response_time_ms=stat_item.get("medianResponseTime", 0),
            geometric_mean_response_time_ms=round(stat_item.get("geoMeanResponseTime"), 2) if stat_item.get(
                "geoMeanResponseTime") is not None else None,
            errors_count=errors_count,
            errors_rate_percent=round(errors_rate, 2),
            concurrency=stat_item.get("concurrency", 0),
            has_label_passed_thresholds=stat_item.get("hasLabelPassedThresholds")
        )

        formatted_stats.append(metrics)

    # Create report with all stats and context
    report = RequestStatsReport(
        execution_id=execution_id or 0,
        execution_name=execution_name,
        execution_url=_build_execution_url(execution_id),
        request_stats=formatted_stats,
        context=_get_request_stats_context()
    )
    formatted_reports.append(report)
    return formatted_reports


def _get_request_stats_context() -> str:
    """Provide context about request stats report metrics for AI interpretation."""
    return (
            "REQUEST STATS REPORT METRICS EXPLANATION:\n"
            "This report provides performance metrics for each request label/endpoint in the test execution.\n\n"
            "KEY METRICS PER ENDPOINT:\n"
            "- label_id: Unique identifier for the request label\n"
            "- label_name: Name of the endpoint/request (e.g., 'Login', 'Homepage', 'View Product')\n"
            "- samples: Total number of requests executed for this endpoint\n"
            + _get_common_metrics_explanation() +
            "- avg_latency_ms: Average network latency (time to first byte) for this endpoint\n"
            "- standard_deviation_ms: Measure of response time variability (higher = more inconsistent)\n"
            "- duration_seconds: Duration of the test period for this endpoint\n"
            "- avg_bytes: Average response size in bytes for this endpoint\n"
            "- geometric_mean_response_time_ms: Geometric mean response time (less affected by outliers than arithmetic mean, useful for skewed distributions)\n"
            "- concurrency: Number of concurrent users hitting this endpoint\n"
            "- has_label_passed_thresholds: Indicates whether this endpoint passed configured performance thresholds (null if thresholds not configured)\n\n"
            "INTERPRETATION GUIDANCE:\n"
            "- Compare avg_response_time_ms across endpoints to identify slow endpoints\n"
            + _get_common_interpretation_guidance() +
            "- Standard deviation indicates consistency: lower = more consistent, higher = more variable\n"
            "- Use this report to drill down into specific endpoint performance issues\n"
            "- The 'ALL' label (if present) shows aggregated metrics across all endpoints\n"
            "**CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.\n"
    )
