from typing import Optional

from mcp.server.fastmcp import Context

from config.blazemeter import EXECUTIONS_ENDPOINT
from config.token import BzmToken
from tools.utils import api_request


class ReportManager:

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx

    async def read_summary(self, master_id: int):
        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/reports/default/summary")

    async def read_error(self, master_id: int):
        """
        Get error report for a given master_id with client-side paging.
        Always returns paged results for AI efficiency.
        """
        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/reports/errorsreport/data"
        )

    async def read_request_stats(self, master_id: int):
        """
        Get request statistics report for a given master_id with client-side paging.
        Always returns paged results for AI efficiency.
        """
        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/reports/aggregatereport/data"
        )
