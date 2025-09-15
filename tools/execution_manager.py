import traceback
from typing import Optional, Dict, Any, List, Union

from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX, EXECUTIONS_ENDPOINT
from config.token import BzmToken
from formatters.execution import format_executions, format_executions_detailed, format_executions_status
from models.execution import TestExecutionDetailed
from models.result import BaseResult
from tools.report_manager import ReportManager
from tools.utils import api_request


class ExecutionResult(BaseResult):
    result: Optional[List[Union[TestExecutionDetailed]]] = Field(description="Test Executions Status List",
                                                                 default=None)


class ExecutionManager:

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx

    async def start(self, test_id: int, delayed_start_ready: bool = True,
                    is_debug_run: bool = False) -> BaseResult:
        parameters = {
            "delayedStart": delayed_start_ready
        }
        start_body = {
            "isDebugRun": is_debug_run,
        }
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

        # Get status information and append that to execution element
        # https://help.blazemeter.com/apidocs/performance/masters_tracking_test_status.htm
        parameters = {
            "level ": 200,  # INFO
            "events": False  # Evaluate the use in the future
        }
        status_response = await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{execution_id}/status",
            result_formatter=format_executions_status,
            params=parameters
        )

        if status_response.error:
            return status_response

        # Append the status information
        execution_element.execution_status_detailed = status_response.result[0]

        return BaseResult(
            result=[execution_element]
        )

    async def list(self, test_id: int, limit: int = 50, offset: int = 0) -> BaseResult:
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
                    return BaseResult(
                        result=await report_manager.read_error(args["execution_id"])
                    )
                case "read_request_stats":
                    return BaseResult(
                        result=await report_manager.read_request_stats(args["execution_id"])
                    )
                case "read_all_reports":
                    return BaseResult(
                        result=[{
                            "summary": await report_manager.read_summary(args["execution_id"]),
                            "error": await report_manager.read_error(args["execution_id"]),
                            "request_stats": await report_manager.read_request_stats(args["execution_id"])
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
