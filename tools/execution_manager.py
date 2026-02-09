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
import traceback
from typing import Optional, Dict, Any

import httpx
from mcp.server.fastmcp import Context

from config.blazemeter import TOOLS_PREFIX, EXECUTIONS_ENDPOINT, SUPPORT_MESSAGE
from config.token import BzmToken
from formatters.execution import format_executions, format_executions_detailed, format_executions_status
from models.manager import Manager
from models.result import BaseResult
from tools import bridge
from tools.report_manager import ReportManager
from tools.utils import api_request, timeout, user_agent


class ExecutionManager(Manager):

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    async def _request_log_analyzer_api(self, method: str, execution_id: int, json_body: Optional[Dict[str, Any]] = None) -> BaseResult:
        if not self.token:
            return BaseResult(
                error="No API token. Set BLAZEMETER_API_KEY env var with file path or API_KEY_ID and API_KEY_SECRET secrets."
            )
        
        url = f"https://log-analyzer.blazemeter.com/analyzer/{execution_id}"
        headers = {
            "Authorization": self.token.as_basic_auth(),
            "User-Agent": user_agent,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(http2=True, timeout=timeout) as client:
                resp = await self._make_analyzer_http_request(client, method, url, headers, json_body)
                resp.raise_for_status()
                return self._parse_analyzer_response(resp)
        except httpx.HTTPStatusError as e:
            return self._handle_analyzer_http_error(e, execution_id)
        except Exception as e:
            return BaseResult(error=f"Error calling Log Analyzer API: {str(e)}")

    async def _make_analyzer_http_request(self, client: httpx.AsyncClient, method: str, url: str, headers: Dict[str, str], json_body: Optional[Dict[str, Any]]) -> httpx.Response:
        if method == "GET":
            return await client.get(url, headers=headers)
        if method == "POST":
            return await client.post(url, headers=headers, json=json_body or {})
        return await client.request(method, url, headers=headers, json=json_body)

    def _parse_analyzer_response(self, resp: httpx.Response) -> BaseResult:
        content_type = resp.headers.get("content-type", "")
        
        if "application/json" not in content_type.lower():
            return BaseResult(result=[resp.text], error=None)
        
        response_dict = resp.json()
        if not isinstance(response_dict, dict):
            return BaseResult(result=[response_dict], error=None)
        
        analyzer_data = response_dict.get("data", response_dict)
        error = analyzer_data.get("error") if isinstance(analyzer_data, dict) else None
        return BaseResult(result=[analyzer_data], error=error)

    def _handle_analyzer_http_error(self, e: httpx.HTTPStatusError, execution_id: int) -> BaseResult:
        status_code = e.response.status_code
        if status_code == 401:
            return BaseResult(error="Unauthorized: Invalid API credentials for Log Analyzer API.")
        elif status_code == 403:
            return BaseResult(error="Forbidden: Access denied to Log Analyzer API.")
        elif status_code == 404:
            return BaseResult(error=f"Not Found: Analysis for execution {execution_id} not found.")
        else:
            try:
                error_body = e.response.json()
                error_msg = error_body.get("error", {}).get("message", str(e))
                return BaseResult(error=f"HTTP {status_code}: {error_msg}")
            except:
                return BaseResult(error=f"HTTP {status_code}: {e.response.text[:200]}")

    async def start(self, test_id: int, delayed_start_ready: bool = True,
                    is_debug_run: bool = False) -> BaseResult:
        # Check if it's valid or allowed
        test_result = await bridge.read_test(self.token, self.ctx, test_id)
        if test_result.error:
            return test_result

        parameters = {"delayedStart": delayed_start_ready}
        start_body = {"isDebugRun": is_debug_run}
        return await api_request(
            self.token,
            "POST",
            f"/tests/{test_id}/start",
            result_formatter=format_executions,
            params=parameters,
            json=start_body
        )

    async def read(self, execution_id: int) -> BaseResult:
        execution_response = await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{execution_id}",
            result_formatter=format_executions_detailed,
        )

        if execution_response.error:
            return execution_response

        execution_element = execution_response.result[0]

        project_result = await bridge.read_project(self.token, self.ctx, execution_element.project_id)
        if project_result.error:
            return project_result

        status_response = await self._fetch_execution_status(execution_id)
        if status_response.error:
            return status_response

        execution_element.execution_status_detailed = status_response.result[0]

        result = {
            "result": execution_element,
            "context": self._get_execution_status_context()
        }

        return BaseResult(result=[result])

    async def _fetch_execution_status(self, execution_id: int) -> BaseResult:
        parameters = {"level ": 200, "events": False}
        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{execution_id}/status",
            result_formatter=format_executions_status,
            params=parameters
        )

    @staticmethod
    def _get_execution_status_context() -> str:
        return (
            "The execution_status is main attribute that indicates if the test passed or failed.\n"
            "The possible values are:\n"
            "pass: Passed - A test is deemed to pass if none of the Failure Criteria defined for the test are met.\n"
            "fail: Failed - A test is deemed to fail if one or more of the Failure Criteria defined for the test are met.\n"
            "unset: Not Set - A test that has no Failure Criteria defined. IMPORTANT - The test outcome is indeterminate because no pass/fail criteria are defined, so it must be reported as unset.\n"
            "abort: Aborted - A test that is terminated using the Abort Test command available during the booting phase.\n"
            "error: Error - A test with one or more execution errors that causes the test to end with no data.\n"
            "noData: No Data - deprecated. Legacy reports with execution errors that ended with no data will remain in No Data status.\n"
            "\n"
            "IMPORTANT - Detecting Test Completion:\n"
            "To determine if a test execution has completed, check the 'ended' field in the execution response:\n"
            "- If 'ended' is null: The test is still running or has not finished.\n"
            "- If 'ended' is not null: The test has completed (has a timestamp indicating when it finished).\n"
            "\n"
            "Always verify that the 'ended' field is not null before retrieving final reports to ensure the test has fully completed and all data is available.\n"
        )

    async def list(self, test_id: int, limit: int = 50, offset: int = 0) -> BaseResult:
        test_result = await bridge.read_test(self.token, self.ctx, test_id)
        if test_result.error:
            return test_result

        parameters = {
            "testId": test_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}",
            result_formatter=format_executions,
            params=parameters
        )

    async def ai_analysis(self, execution_id: int) -> BaseResult:
        execution_response = await self.read(execution_id)
        if execution_response.error:
            return execution_response

        execution_element = self._extract_execution_element(execution_response, execution_id)
        if isinstance(execution_element, BaseResult):
            return execution_element

        if not self._is_execution_started(execution_element):
            return BaseResult(
                error=f"Execution {execution_id} has not been started yet. Please start the execution first before requesting AI analysis."
            )

        analyzer_response = await self._get_or_trigger_analysis(execution_id)
        if analyzer_response.error:
            return analyzer_response

        analysis_state = self._parse_analysis_state(analyzer_response)
        if isinstance(analysis_state, BaseResult):
            return analysis_state

        return self._build_analysis_result(execution_id, analysis_state)

    def _extract_execution_element(self, execution_response: BaseResult, execution_id: int):
        if not execution_response.result:
            return self._execution_not_found_error(execution_id)
        
        result_dict = execution_response.result[0]
        execution_element = result_dict.get("result")
        if not execution_element:
            return self._execution_not_found_error(execution_id)
        
        return execution_element

    @staticmethod
    def _execution_not_found_error(execution_id: int) -> BaseResult:
        return BaseResult(error=f"Execution {execution_id} not found")

    @staticmethod
    def _is_execution_started(execution_element) -> bool:
        return execution_element.created is not None

    async def _get_or_trigger_analysis(self, execution_id: int) -> BaseResult:
        analyzer_response = await self._request_log_analyzer_api("GET", execution_id)
        
        if self._should_trigger_new_analysis(analyzer_response):
            post_response = await self._request_log_analyzer_api("POST", execution_id)
            if post_response.error:
                return post_response
            return post_response

        return analyzer_response

    @staticmethod
    def _should_trigger_new_analysis(analyzer_response: BaseResult) -> bool:
        if analyzer_response.error:
            return True
        
        if not analyzer_response.result:
            return False
        
        analyzer_data = analyzer_response.result[0]
        return isinstance(analyzer_data, dict) and analyzer_data.get("status") == "not_started"

    def _parse_analysis_state(self, analyzer_response: BaseResult):
        analyzer_data = self._extract_analyzer_data(analyzer_response)
        
        if not analyzer_data:
            return {
                "is_ready": False,
                "status_message": "Analysis status is not available yet",
                "analysis_results": None
            }

        error = analyzer_data.get("error")
        if error:
            return BaseResult(error=f"Analysis error: {error}")

        readiness = self._determine_analysis_readiness(analyzer_data)
        
        if not readiness.get("status_message") or not readiness["status_message"].strip():
            readiness["status_message"] = "Analysis status unknown"
        
        return readiness

    @staticmethod
    def _extract_analyzer_data(analyzer_response: BaseResult) -> Optional[Dict[str, Any]]:
        if not analyzer_response.result:
            return None
        
        analyzer_data = analyzer_response.result[0]
        if not isinstance(analyzer_data, dict):
            return None
        
        return analyzer_data

    @staticmethod
    def _normalize_results(results: Any) -> list:
        if results is None:
            return []
        if isinstance(results, list):
            return results
        return [results] if results else []

    @staticmethod
    def _build_analysis_response(is_ready: bool, status_message: str, analysis_results: Any) -> Dict[str, Any]:
        return {
            "is_ready": is_ready,
            "status_message": status_message,
            "analysis_results": analysis_results
        }

    @staticmethod
    def _determine_analysis_readiness(analyzer_data: Dict[str, Any]) -> Dict[str, Any]:
        status = analyzer_data.get("status", "").strip().lower()
        progress = analyzer_data.get("progress", 0)
        
        result_field = analyzer_data.get("result")
        results = ExecutionManager._normalize_results(result_field)
        
        if status == "finished":
            if results:
                return ExecutionManager._build_analysis_response(
                    True, f"Analysis complete with {len(results)} result(s)", results
                )
            return ExecutionManager._build_analysis_response(
                True, "Analysis complete with no issues found", []
            )
        
        if status in ["not_started", "running"]:
            progress_str = f" ({progress}%)" if progress else ""
            return ExecutionManager._build_analysis_response(
                False, f"Analysis {status}{progress_str}", None
            )
        
        if not status:
            return ExecutionManager._build_analysis_response(
                True, "Analysis complete", results
            )
        
        return ExecutionManager._build_analysis_response(
            True, f"Analysis {status}", results
        )

    def _build_analysis_result(self, execution_id: int, analysis_state: Dict[str, Any]) -> BaseResult:
        is_ready = analysis_state["is_ready"]
        result = {
            "result": {
                "execution_id": execution_id,
                "analysis_status": "ready" if is_ready else "processing",
                "analysis_message": analysis_state["status_message"],
                "analysis_results": analysis_state["analysis_results"]
            },
            "context": self._get_analysis_context_message(is_ready, analysis_state["status_message"])
        }
        return BaseResult(result=[result])

    @staticmethod
    def _get_analysis_context_message(is_ready: bool, status_message: str) -> str:
        if is_ready:
            return (
                "AI analysis is ready. The analysis results are available above.\n"
                "You can now proceed with reviewing the analysis results.\n"
                "If you need to check the execution status or reports, use the 'read' action."
            )
        else:
            return (
                "AI analysis is currently being processed and is not ready yet.\n"
                f"Status: {status_message}\n"
                "Please wait a moment and check again using the 'ai_analysis' action.\n"
                "The analysis will be available once processing is complete."
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_execution",
        description="""
        Operations on tests executions and results reports.
        Actions:
        - start: start a preconfigured load test, you need to know the test_id of a created and configured test.
            args(dict): Dictionary with the following required parameters:
                test_id (int): The test Id that should be started.
        - read: Read a Test Execution. Get the information and status of a test execution.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get the information.
        - list: List all executions for a test ID. 
            args(dict): Dictionary with the following required parameters:
                test_id (int): The id of the test to list the execution from
                limit (int, default=10, valid=[1 to 50]): The number of test executions to list.
                offset (int, default=0): Number of test executions to skip.       
        - read_summary: get the summary report for a given execution ID.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get the summary report for.
        - read_errors: get the error report for a given execution ID.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get the error report for.
        - read_request_stats: get the request statistics report for a given execution ID.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get the request statistics report for.
        - read_all_reports: get all reports (summary, error, and request statistics) for a given execution ID.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get all reports for.
        - read_anomalies_stats: get anomaly statistics for a test execution (count, affected labels, per-anomaly KPI/time/spike details).
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution (master) ID to get anomaly stats for.
        - ai_analysis: Trigger AI analysis for an execution and get dynamic responses based on polling results.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID (masterId) to trigger AI analysis for.
            The action will check if the execution is running or finished, then either retrieve existing analysis status
            or create a new analysis entry. It provides dynamic responses indicating whether the analysis is ready or still processing.
        """
    )
    async def execution(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        test_manager = ExecutionManager(token, ctx)
        report_manager = ReportManager(token, ctx)

        try:
            match action:
                case "start":
                    return await test_manager.start(args["test_id"])
                case "read":
                    return await test_manager.read(args["execution_id"])
                case "list":
                    return await test_manager.list(args["test_id"])
                case "read_summary":
                    return await report_manager.read_summary(args["execution_id"])
                case "read_errors":
                    return await report_manager.read_error(args["execution_id"])
                case "read_request_stats":
                    return await report_manager.read_request_stats(args["execution_id"])
                case "read_all_reports":
                    summary_result = await report_manager.read_summary(args["execution_id"])
                    error_result = await report_manager.read_error(args["execution_id"])
                    stats_result = await report_manager.read_request_stats(args["execution_id"])
                    return BaseResult(
                        result=[{
                            "summary": summary_result.result or None,
                            "error": error_result.result or None,
                            "request_stats": stats_result.result or None
                        }]
                    )
                case "read_anomalies_stats":
                    return await report_manager.read_anomalies_stats(args["execution_id"])
                case "ai_analysis":
                    return await test_manager.ai_analysis(args["execution_id"])
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in test execution manager tool"
                    )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}\n{SUPPORT_MESSAGE}"
            )
