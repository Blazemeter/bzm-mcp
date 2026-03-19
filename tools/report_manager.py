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
from typing import Optional

from mcp.server.fastmcp import Context

from config.blazemeter import EXECUTIONS_ENDPOINT
from config.token import BzmToken
from formatters.execution import format_summary_report, format_request_stats
from models.manager import Manager
from models.result import BaseResult
from tools import bridge
from tools.utils import api_request

EXECUTION_ARCHIVED_MSG = ("Execution report is archived. It is not possible to read execution "
                          "information from an archived execution.")


class ReportManager(Manager):

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    @staticmethod
    def _extract_execution_name(execution_result: BaseResult) -> Optional[str]:
        """Extract execution name from execution result if available."""
        if execution_result.result and len(execution_result.result) > 0:
            exec_data = execution_result.result[0]
            if isinstance(exec_data, dict):
                return exec_data.get("execution_name") or exec_data.get("name")
        return None

    @staticmethod
    def _evaluate_archived(execution_result: BaseResult) -> bool:
        return (execution_result.result and len(execution_result.result) > 0 and
                execution_result.result[0].get("result").archived)

    async def read_summary(self, master_id: int):
        # Check if it's valid or allowed
        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        # Extract execution name from execution result if available
        execution_name = self._extract_execution_name(execution_result)

        # Get summary data from API with formatter
        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/reports/default/summary",
            result_formatter=format_summary_report,
            result_formatter_params={
                "execution_id": master_id,
                "execution_name": execution_name
            }
        )

    async def read_error(self, master_id: int):
        """
        Get error report for a given master_id with client-side paging.
        Always returns paged results for AI efficiency.
        """
        # Check if it's valid or allowed
        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/reports/errorsreport/data"
        )

    async def read_request_stats(self, master_id: int):
        """
        Get request statistics report for a given master_id with formatted, AI-friendly structure.
        Includes execution metadata and explanatory context about metrics per endpoint.
        """
        # Check if it's valid or allowed
        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        # Extract execution name from execution result if available
        execution_name = self._extract_execution_name(execution_result)

        # Get request stats data from API with formatter
        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/reports/aggregatereport/data",
            result_formatter=format_request_stats,
            result_formatter_params={
                "execution_id": master_id,
                "execution_name": execution_name
            }
        )

    async def read_anomalies_stats(self, master_id: int):
        """
        Get anomaly statistics for a given master_id (test execution).
        Returns anomaly count, affected labels, and per-anomaly details (KPI, time range, max spike).
        """
        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/anomalies/stats",
        )
