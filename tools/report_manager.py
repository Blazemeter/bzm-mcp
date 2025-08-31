import traceback
from .base import api_request
from typing import Optional
from config.token import BzmToken
from typing import Any, Dict
import logging

class ReportManager:

    def __init__(self, token: Optional[BzmToken]):
        self.reports = []
        self.token = token

    async def get_master_id(self, test_id: int):
        """Get the masterId for a given testId from the /masters endpoint"""
        endpoint = f"/masters?testId={test_id}"
        
        masters_response = await api_request(self.token, "GET", endpoint)
        
        if "error" in masters_response and masters_response["error"]:
            return {
                "error": masters_response.get("error"),
                "master_id": None
            }
        
        masters = masters_response.get("result", [])
        
        if not masters:
            return {
                "error": f"No masters found for testId {test_id}",
                "master_id": None
            }
        
        # Get the most recent master (first in the list)
        master_id = masters[0].get("id")
        return {
            "master_id": master_id,
            "error": None
        }

    async def get_summary_report(self, master_id: int):
        endpoint = f"/masters/{master_id}/reports/default/summary"
        
        report_response = await api_request(self.token, "GET", endpoint)
        
        if "error" in report_response and report_response["error"]:
            return {
                "master_id": master_id,
                "report_type": "summary",
                "error": report_response.get("error"),
                "raw_data": {}
            }
        
        report_data = report_response.get("result", {})
        
        return {
            "master_id": master_id,
            "report_type": "summary",
            "raw_data": report_data
        }

    async def get_error_report(self, master_id: int):
        endpoint = f"/masters/{master_id}/reports/errorsreport/data"
        
        report_response = await api_request(self.token, "GET", endpoint)
        
        if "error" in report_response and report_response["error"]:
            return {
                "master_id": master_id,
                "report_type": "errors",
                "error": report_response.get("error"),
                "raw_data": {}
            }
        
        report_data = report_response.get("result", {})
        
        return {
            "master_id": master_id,
            "report_type": "errors",
            "raw_data": report_data
        }

    async def get_request_stats_report(self, master_id: int):
        endpoint = f"/masters/{master_id}/reports/aggregatereport/data"
        
        report_response = await api_request(self.token, "GET", endpoint)
        
        if "error" in report_response and report_response["error"]:
            return {
                "master_id": master_id,
                "report_type": "request_stats",
                "error": report_response.get("error"),
                "raw_data": {}
            }
        
        report_data = report_response.get("result", {})
        
        return {
            "master_id": master_id,
            "report_type": "request_stats",
            "raw_data": report_data
        }


def register(mcp, token: Optional[BzmToken]):

    @mcp.tool(
        name="bzm_mcp_reports_tool",
        description="""
        Retrieves multiple types of reports (summary, error, and request statistics) for a given test from the Blazemeter MCP.
        This tool allows you to fetch detailed information about a test's execution, including overall results, encountered errors, and request-level statistics.
        Provide the test ID to obtain the relevant reports.
        Arguments:
        - test_id (int): The id of the test to get reports for.
        Returns:
        - summary_report (dict): The summary report for the test.
        - error_report (dict): The error report for the test.
        - request_stats_report (dict): The request statistics report for the test.
        """
    )
    async def bzm_mcp_reports_tool(args: Dict[str, Any]) -> Dict[str, Any]:
        report_manager = ReportManager(token)
        try:
            master_result = await report_manager.get_master_id(args["test_id"])
            
            if master_result.get("error"):
                return {
                    "result": {
                        "error": master_result["error"],
                        "summary_report": {},
                        "error_report": {},
                        "request_stats_report": {}
                    }
                }
            
            master_id = master_result["master_id"]
            
            return { 
                "result": { 
                    "summary_report": await report_manager.get_summary_report(master_id),
                    "error_report": await report_manager.get_error_report(master_id),
                    "request_stats_report": await report_manager.get_request_stats_report(master_id)
                }
            }
        except Exception as e:
            return {"result": f"Error: {traceback.format_exc()}"}
