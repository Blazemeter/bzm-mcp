import traceback
from typing import Optional, Dict, Any

from config.blazemeter import BZM_BASE_URL
from config.token import BzmToken
from tools.base import api_request
from tools.report_manager import ReportManager


class TestExecutionManager:

    def __init__(self, token: Optional[BzmToken]):
        self.token = token

    async def start(self, test_id: int, delayed_start_ready: bool = True, is_debug_run: bool = False) -> dict[str, any]:
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
            master_id = result.get("id")
            return {
                "master_id": master_id,
                "execution_url": f"{BZM_BASE_URL}/app/#/masters/{master_id}"
            }
        else:
            return {"error": start_response.get("error")}


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name="bzm_mcp_test_execution_tool",
        description="""
        Operations on tests and reports.
        Actions:
        - start: start a preconfigured load test, you need to know the testId of a created and configured test.
            args(dict): Dictionary with the following required parameters:
                test_id (int): The test Id that should be started.
        - get_summary_report: get the summary report for a given master ID.
            args(dict): Dictionary with the following required parameters:
                master_id (int): The master ID to get the summary report for.
        - get_error_report: get the error report for a given master ID with optional paging.
            args(dict): Dictionary with the following required parameters:
                master_id (int): The master ID to get the error report for.
                limit (int, optional): Maximum number of error entries to return (default: all).
                offset (int, optional): Number of error entries to skip (default: 0).
        - get_request_stats_report: get the request statistics report for a given master ID with optional paging.
            args(dict): Dictionary with the following required parameters:
                master_id (int): The master ID to get the request statistics report for.
                limit (int, optional): Maximum number of request stats entries to return (default: all).
                offset (int, optional): Number of request stats entries to skip (default: 0).
        - get_all_reports: get all reports (summary, error, and request statistics) for a given master ID.
            args(dict): Dictionary with the following required parameters:
                master_id (int): The master ID to get all reports for.
        """
    )
    async def bzm_mcp_test_execution_tool(action: str, args: Dict[str, Any]) -> Dict[str, Any]:
        test_manager = TestExecutionManager(token)
        report_manager = ReportManager(token)
        
        try:
            match action:
                case "start":
                    return {"result": await test_manager.start(args["test_id"])}
                case "get_summary_report":
                    return {"result": await report_manager.get_summary_report(args["master_id"])}
                case "get_error_report":
                    limit = args.get("limit", 10)
                    offset = args.get("offset", 0)
                    return {"result": await report_manager.get_error_report(args["master_id"], limit, offset)}
                case "get_request_stats_report":
                    limit = args.get("limit", 10)
                    offset = args.get("offset", 0)
                    return {"result": await report_manager.get_request_stats_report(args["master_id"], limit, offset)}
                case "get_all_reports":
                    return {"result": {
                        "summary_report": await report_manager.get_summary_report(args["master_id"]),
                        "error_report": await report_manager.get_error_report(args["master_id"]),
                        "request_stats_report": await report_manager.get_request_stats_report(args["master_id"])
                    }}
                case _:
                    return {"result": f"Action {action} not found in test execution manager tool"}
        except Exception as e:
            return {"result": f"Error: {traceback.format_exc()}"}
