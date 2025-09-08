from typing import Optional

from config.token import BzmToken
from .base import api_request


class ReportManager:

    def __init__(self, token: Optional[BzmToken]):
        self.reports = []
        self.token = token

    def _apply_paging(self, all_data: list, limit: int, offset: int, master_id: int, report_type: str):
        total = len(all_data)

        start_idx = offset
        end_idx = offset + limit
        paged_data = all_data[start_idx:end_idx]
        has_more = end_idx < total

        return {
            "execution_id": master_id,
            "report_type": report_type,
            "raw_data": paged_data,
            "has_more": has_more,
            "total": total,
            "page_info": {
                "offset": offset,
                "limit": limit,
                "returned_count": len(paged_data)
            }
        }

    async def get_summary_report(self, master_id: int):
        endpoint = f"/masters/{master_id}/reports/default/summary"

        report_response = await api_request(self.token, "GET", endpoint)

        if "error" in report_response and report_response["error"]:
            return {
                "error": report_response.get("error")
            }

        report_data = report_response.get("result", {})

        return {
            "master_id": master_id,
            "report_type": "summary",
            "raw_data": report_data
        }

    async def get_error_report(self, master_id: int, limit: int = 10, offset: int = 0):
        """
        Get error report for a given master_id with client-side paging.
        Always returns paged results for AI efficiency.
        """
        endpoint = f"/masters/{master_id}/reports/errorsreport/data"

        report_response = await api_request(self.token, "GET", endpoint)

        if "error" in report_response and report_response["error"]:
            return {
                "master_id": master_id,
                "report_type": "errors",
                "error": report_response.get("error"),
                "raw_data": [],
                "has_more": False,
                "total": 0
            }

        all_data = report_response.get("result", [])
        return self._apply_paging(all_data, limit, offset, master_id, "errors")

    async def get_request_stats_report(self, master_id: int, limit: int = 10, offset: int = 0):
        """
        Get request statistics report for a given master_id with client-side paging.
        Always returns paged results for AI efficiency.
        """
        endpoint = f"/masters/{master_id}/reports/aggregatereport/data"

        report_response = await api_request(self.token, "GET", endpoint)

        if "error" in report_response and report_response["error"]:
            return {
                "master_id": master_id,
                "report_type": "request_stats",
                "error": report_response.get("error"),
                "raw_data": [],
                "has_more": False,
                "total": 0
            }

        all_data = report_response.get("result", [])
        return self._apply_paging(all_data, limit, offset, master_id, "request_stats")
