import traceback
from datetime import datetime
from typing import Optional, Dict, Any, List, Union

from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import BZM_BASE_URL
from config.token import BzmToken
from models.execution import TestExecution, TestExecutionDetailed, TestExecutionStatuses, TestExecutionStatus
from models.result import BaseResult
from tools.base import api_request, get_date_time_iso, TOOLS_PREFIX
from tools.report_manager import ReportManager


class TestExecutionBasicResult(BaseResult):
    result: Optional[List[Union[TestExecution]]] = Field(description="Test Executions List", default=None)


class TestExecutionResult(BaseResult):
    result: Optional[List[Union[TestExecutionDetailed]]] = Field(description="Test Executions Status List",
                                                                 default=None)


class TestExecutionManager:

    def __init__(self, token: Optional[BzmToken]):
        self.token = token

    async def start(self, test_id: int, delayed_start_ready: bool = True,
                    is_debug_run: bool = False) -> TestExecutionBasicResult:
        parameters = {
            "delayedStart": delayed_start_ready
        }
        start_body = {
            "isDebugRun": is_debug_run,
        }
        start_response = await api_request(self.token, "POST", f"/tests/{test_id}/start", params=parameters,
                                           json=start_body)

        result = start_response.get("result", {})

        if "id" in result:
            execution_id = result.get("id")
            execution_name = result.get("name")
            return TestExecutionBasicResult(
                result=[
                    TestExecution(
                        test_id=test_id,
                        execution_id=execution_id,
                        execution_name=execution_name,
                        execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}"
                    )
                ]
            )
        else:
            return TestExecutionBasicResult(
                error=start_response.get("error")
            )

    async def read(self, execution_id: int) -> TestExecutionResult:

        execution_response = await api_request(self.token, "GET", f"/masters/{execution_id}")

        if "error" in execution_response and execution_response["error"]:
            return TestExecutionResult(
                error=execution_response.get("error")
            )

        execution_result = execution_response.get("result", {})

        execution_id = execution_result.get("id")
        execution_name = execution_result.get("name")

        created = get_date_time_iso(execution_result.get("created"))
        updated = get_date_time_iso(execution_result.get("updated"))
        ended = execution_result.get("ended")
        if ended is not None:
            ended = get_date_time_iso(ended)

        execution_status = execution_result.get("reportStatus")

        # Status information
        # https://help.blazemeter.com/apidocs/performance/masters_tracking_test_status.htm
        parameters = {
            "level ": 200,  # INFO
            "events": False  # Evaluate the use in the future
        }
        status_response = await api_request(self.token, "GET", f"/masters/{execution_id}/status", params=parameters)

        if "error" in status_response and status_response["error"]:
            return TestExecutionResult(
                error=status_response.get("error")
            )

        status_result = status_response.get("result", {})
        statuses = status_result.get("statuses", {})

        execution_statuses = TestExecutionStatuses(
            pending_percent=statuses.get("pending", 0),
            booting_percent=statuses.get("booting", 0),
            downloading_percent=statuses.get("downloading", 0),
            ready_percent=statuses.get("ready", 0),
            ended_percent=statuses.get("ended", 0),
        )

        progress_percent = execution_statuses.ended_percent
        if progress_percent is None:
            progress_percent = 0

        return TestExecutionResult(
            result=[
                TestExecutionDetailed(
                    test_id=execution_result.get("testId", 0),
                    execution_id=execution_id,
                    execution_name=execution_name,
                    execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}",
                    created=created,
                    updated=updated,
                    ended=ended,
                    execution_status=execution_status,
                    execution_status_detailed=TestExecutionStatus(
                        progress_percent=progress_percent,
                        execution_step=status_result.get("execution_step", "Unknown"),
                        execution_statuses=execution_statuses
                    ),
                )
            ],
            error=status_response.get("error")
        )

    async def list(self, test_id: int, limit: int = 50, offset: int = 0) -> TestExecutionBasicResult:
        parameters = {
            "testId": test_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        execution_response = await api_request(self.token, "GET", "/masters", params=parameters)

        if "error" in execution_response and execution_response["error"]:
            return TestExecutionBasicResult(
                error=execution_response.get("error")
            )

        executions = execution_response.get("result", [])
        has_more = execution_response.get("total", 0) - (offset + limit) > 0
        results = []
        for execution in executions:
            execution_id = execution.get("id")
            execution_name = execution.get("name")
            execution = TestExecution(
                test_id=test_id,
                execution_id=execution_id,
                execution_name=execution_name,
                execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}"
            )
            results.append(execution)

        return TestExecutionBasicResult(
            result=results,
            has_more=has_more
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_test_execution",
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
                limit (int, default=50): The number of test executions to list.
                offset (int, default=0): Number of test executions to skip.       
        - get_summary_report: get the summary report for a given execution ID.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get the summary report for.
        - get_error_report: get the error report for a given execution ID with optional paging.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get the error report for.
                limit (int, optional): Maximum number of error entries to return (default: all).
                offset (int, optional): Number of error entries to skip (default: 0).
        - get_request_stats_report: get the request statistics report for a given execution ID with optional paging.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get the request statistics report for.
                limit (int, optional): Maximum number of request stats entries to return (default: all).
                offset (int, optional): Number of request stats entries to skip (default: 0).
        - get_all_reports: get all reports (summary, error, and request statistics) for a given execution ID.
            args(dict): Dictionary with the following required parameters:
                execution_id (int): The execution ID to get all reports for.
        """
    )
    async def test_execution(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        test_manager = TestExecutionManager(token)
        report_manager = ReportManager(token)

        try:
            match action:
                case "start":
                    return await test_manager.start(args["test_id"])
                case "read":
                    return await test_manager.read(args["execution_id"])
                case "list":
                    return await test_manager.list(args["test_id"])
                case "get_summary_report":
                    return await report_manager.get_summary_report(args["execution_id"])
                case "get_error_report":
                    limit = args.get("limit", 10)
                    offset = args.get("offset", 0)
                    return BaseResult(
                        result=await report_manager.get_error_report(args["execution_id"], limit, offset)
                    )
                case "get_request_stats_report":
                    limit = args.get("limit", 10)
                    offset = args.get("offset", 0)
                    return BaseResult(
                        result=await report_manager.get_request_stats_report(args["execution_id"], limit, offset)
                    )
                case "get_all_reports":
                    return BaseResult(
                        result=[{
                            "summary_report": await report_manager.get_summary_report(args["execution_id"]),
                            "error_report": await report_manager.get_error_report(args["execution_id"]),
                            "request_stats_report": await report_manager.get_request_stats_report(args["execution_id"])
                        }]
                    )
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in test execution manager tool"
                    )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
