"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    10|Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from tools.actions.spec import ALL, HTTP, STDIO, ActionSpec

HEADER = "Operations on tests."

HINTS = (
    "- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.",
    "- To search test runs/reports (executions), use the execution tool search action instead of tests search.",
    "- Before configure_failure_criteria, prefer failure_criteria_meta for kpi/condition codes and labels, then read if you must merge with existing rules.",
    "- For configure_failure_criteria, call read first and merge client-side if you must keep existing rules; providing rules replaces all criteria rows for that test.",
)

ACTIONS: tuple[ActionSpec, ...] = (
    ActionSpec(
        name="read",
        transports=ALL,
        required_args=("test_id",),
        body="""Read a test. Get the detailed information of a test.
    args(dict): Dictionary with the following required parameters:
        test_id (int): The only required parameter. The id of the test to read.
    When presenting failure_criteria to the user, use meta.general_labels, meta.rule_field_labels, meta.kpi_labels, and meta.condition_labels for readable text; avoid leading with raw kpi ids or op codes.""",
    ),
    ActionSpec(
        name="create",
        transports=ALL,
        required_args=("test_name", "project_id"),
        body="""Create a new test. Do not create a test if the user has not confirmed the location for validation of workspace, project and account.
    args(dict): Dictionary with the following required parameters:
        test_name (str): The required name of the test to create.
        project_id (int): The id of the project to list tests from.""",
    ),
    ActionSpec(
        name="delete",
        transports=ALL,
        required_args=("test_id",),
        body="""Delete a test.
    args(dict): Dictionary with the following required parameters:
        test_id (int): The only required parameter. The id of the test to be deleted.""",
    ),
    ActionSpec(
        name="list",
        transports=ALL,
        required_args=("project_id",),
        body="""List all tests.
    args(dict): Dictionary with the following required parameters:
        project_id (int): The id of the project to list tests from.
        limit (int, default=10, valid=[1 to 50]): The number of tests to list.
        offset (int, default=0): Number of tests to skip.
    Each listed test may include failure_criteria; when describing it to the user, use meta labels like read (see read action).""",
    ),
    ActionSpec(
        name="search",
        transports=ALL,
        required_args=("account_id",),
        body="""Search tests across an account
    args(dict): Dictionary with the following optional filter parameters:
        account_id (int, mandatory): The id of the account to use.
        test_name (str): Case- and diacritic-insensitive (ilike) match on test name.
        workspace_id_list (list[int], values= use search_filter_values with 'workspace_id_list'): Workspace IDs to filter test results.
        time_frame (str, default='latest', values=['latest','last24','lastWeek','lastMonth','custom']):
            Filter by test create date. latest=Today, last24=Last 24 hours, lastWeek=Last 7 days,
            lastMonth=Last 30 days, custom=use start_time and end_time.
        start_time (str): Start of create-date range in ISO format (only when time_frame is 'custom').
        end_time (str): End of create-date range in ISO format (only when time_frame is 'custom').
        cloud_provider_name_list (list[str], values= use search_filter_values with 'cloud_provider_name_list'): Cloud provider names.
        created_by_id_list (list[int], values= use search_filter_values with 'created_by_id_list'): Owner user IDs (test creator, not execution runner).
        locations_id_list (list[str], values= use search_filter_values with 'locations_id_list'): Location IDs configured on the test.
        project_id_list (list[int], values= use search_filter_values with 'project_id_list'): Project IDs.
        duration_list (list[dict], values= use search_filter_values with 'duration_list'): Duration in seconds. Example: [{">=": 5}].
        number_of_engines_list (list[dict], values= use search_filter_values with 'number_of_engines_list'): Engine count. Example: [{">=": 2}].
        virtual_users_list (list[dict], values= use search_filter_values with 'virtual_users_list'): Virtual user count. Example: [{">=": 10}].
        page_index (int, default=1): Page number. If has_more is true, ask the user before fetching the next page.
    Returns test_id, test_name, test_url, project/workspace info, configuration summary, and timestamps (created, updated).""",
    ),
    ActionSpec(
        name="search_filter_values",
        transports=ALL,
        required_args=("account_id", "filter_names"),
        body="""List allowed values for test search filters.
    args(dict): Dictionary with the following required filter parameters:
        account_id (int, mandatory): The id of the account to use.
        filter_names (list[str], values=['workspace_id_list', 'cloud_provider_name_list', 'created_by_id_list', 'locations_id_list', 'project_id_list', 'tag_id_list', 'duration_list', 'number_of_engines_list', 'virtual_users_list']): Filter names to resolve.""",
    ),
    ActionSpec(
        name="configure_load",
        transports=ALL,
        required_args=("test_id",),
        body="""Configure the load of a test for the given test id. The test id is the only required parameter.
             The test will be configured based on the following parameters only if user confirms the configuration:
    args(dict): Dictionary with the following parameters:
        test_id (int): The only required parameter. The id of the test to configure.
        iterations (int, default=1, infinite=-1): The number of iterations to run the test with. Don't use if hold-for is provided.
        hold-for (str, default=1m): The length of time the test will run at the peak concurrency. Values can be provided in m (minutes) only. Don't use if iterations is provided.
        concurrency (int, default=20, disable=0, max=500000): The number of concurrent virtual users simulated to run. For example, 20 will set the test to run with 20 concurrent users. To disable it set to 0.
        ramp-up (str, disable=""): The length of time the test will take to ramp-up to full concurrency. Values can be provided in m (minutes) only. Can be empty.
        steps (int, default=1, disable=-1): The number of ramp-up steps. Can be empty.
        executor (str, default=jmeter): The script type you are running. Includes the following options: (gatling,grinder,jmeter,locust,pbench,selenium,siege).""",
    ),
    ActionSpec(
        name="configure_locations",
        transports=ALL,
        required_args=("test_id",),
        body="""Configure the distribution of a test for given test id. The test id is the only required parameter.
             The test will be configured based on the following parameters only if user confirms the configuration:
    args(dict): Dictionary with the following parameters:
        test_id (int): The only required parameter. The id of the test to configure.
        locations (list[str]): List of all locations with their percentage distribution of user load in a key value format "location_id=percent_value". Example: ["us-east4-a=25", "us-east1-b=25", "us-west1-a=25", "us-central1-a=25"]""",
    ),
    ActionSpec(
        name="upload_assets",
        transports=frozenset({STDIO}),
        required_args=("test_id", "file_paths"),
        body="""Upload main script test as well as multiple related assets to a test. Supports .zip, .csv, .jmx, .yaml and other file types.
    args(dict): Dictionary with the following required parameters:
        test_id (int): The id of the test to upload assets to.
        file_paths (list): List of full file paths to upload.
        main_script (str, optional): Path to the main script file. If provided, will update test configuration to use this script.""",
    ),
    ActionSpec(
        name="upload_assets",
        transports=frozenset({HTTP}),
        required_args=("test_id", "filename", "declared_size", "encoding", "sha256"),
        body="""Prepare a one-shot upload URL for a single test asset. MCP does not accept file bytes, paths, or base64. You POST the file yourself.
    args(dict): Dictionary with the following required parameters:
        test_id (int): The id of the test to upload to. Authorized before mint.
        filename (str): ASCII letters, digits, underscore, hyphen, plus a required extension, length 3-255. Example: Retail-Demo.jmx
        declared_size (int): Uncompressed size in bytes, greater than 0. Hard ceiling is 100 MiB.
        encoding (str, values=['identity','gzip']): Transport encoding you will send on the POST. Hash the uncompressed file first; gzip only after hashing.
        sha256 (str): 64 hex characters of the uncompressed asset.
    Returns immediately: method POST, url, authorization (the upload capability, once), headers (Authorization, X-Upload-Filename, X-Content-SHA256, Content-Encoding), size_ceiling, redeem_deadline, upload_deadline, one_file_per_url, success_status 201.
    POST exactly one raw asset as the body (not multipart). 201 means the file landed. After real bytes the URL is spent; call upload_assets again. Empty body is 422 and the ticket stays reusable. If the POST returns 503 after bytes were sent, GET /api/v4/tests/{test_id}/files before retrying so a lost 201 does not become a duplicate.
    Example:
      curl -X POST "$URL" -H "Authorization: Bearer $TOKEN" -H "X-Upload-Filename: Retail-Demo.jmx" -H "X-Content-SHA256: $SHA" -H "Content-Encoding: identity" --data-binary @Retail-Demo.jmx""",
    ),
    ActionSpec(
        name="failure_criteria_meta",
        transports=ALL,
        body="""Read-only catalog: overview (layers), top_level_tool_args, rule_fields, general, general_labels, rule_field_labels, kpis, conditions. Field names align with reading and configuring tests. No BlazeMeter API call.
    args(dict): Optional; may be empty {}. Unknown keys are ignored.""",
    ),
    ActionSpec(
        name="configure_failure_criteria",
        transports=ALL,
        required_args=("test_id", "enabled", "rules"),
        body="""Set failure criteria (BlazeMeter configuration.enableFailureCriteria and configuration.plugins.thresholds). Replaces the full rules list for the test.
    args(dict): Dictionary with the following parameters:
        test_id (int): Required. The test id.
        enabled (bool): Required. Master switch for the Failure Criteria section (API enableFailureCriteria).
        rules (list): Required. List of rule objects; use an empty list to clear all rules. Each object may include:
            kpi (str): Required per rule. API metric field name (`field`). Documented values (product may offer more):
                responseTime.avg, responseTime.min, responseTime.max, responseTime.std,
                responseTime.percentile.0, responseTime.percentile.50, responseTime.percentile.90,
                responseTime.percentile.95, responseTime.percentile.99,
                latency.avg, connectTime.avg, size.count, size.avg, size.rate,
                hits.count, hits.avg, hits.rate, duration.count,
                errors.count, errors.percent, errors.rate
            label (str, default=ALL): Label scope for the metric (default ALL labels).
            condition (str or null): API operator (`op`). Allowed string values:
                lt (Less than), gt (Greater than), eq (Equal to), ne (Not equal to),
                lte (Less than or equal to), gte (Greater than or equal to).
                Omit the key or use JSON null for no operator (incomplete / initial state).
            value (str): Threshold as string (numeric text, e.g. "500", "1"; may be empty until set).
            offset_percent (str, default=0.0): Baseline offset percentage string (API offsetPercentage).
            stop_test_on_violation (bool, default=false): Stop Test on violation (API stopTestOnViolation); product expects 1-min slide window when used.
            sliding_window (bool, default=false): 1-min slide window eval for this rule (API slidingWindow). Per-row "1-min slide window eval"; bulk "Enable 1-min slide window eval for all" means every rule has sliding_window true.
            ignore_rampup (bool, optional): Per-rule ignore ramp-up when the API includes it on the item.
            is_empty (bool, default=false): Incomplete row flag (API isEmpty).
        ignore_rampup (bool, optional): Container-level "Ignore failure criteria during ramp-up" (advanced); omit to keep existing value on merge.
        sliding_window_for_all (bool, optional): If set, sets every rule's sliding_window to this value after parsing rules (bulk convenience).
        from_taurus (bool, optional): plugins.thresholds.fromTaurus; omit to preserve existing.
        criteria_overridden_in_interface (bool, optional): Threshold-block metadata (maps to plugins.thresholds when merging); omit to preserve existing.
    Reading a test and configuring failure criteria use the same field names; BlazeMeter’s REST JSON is only used in HTTP calls inside the server.""",
    ),
)
