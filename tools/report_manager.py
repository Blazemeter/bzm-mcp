import traceback
from .base import api_request
from typing import Optional
from config.token import BzmToken
from typing import Any, Dict

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

