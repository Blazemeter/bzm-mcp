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
from formatters.execution import (
    format_summary_report,
    format_request_stats,
    format_error_report,
    format_anomalies_stats,
)
from models.manager import Manager
from models.result import BaseResult
from tools import bridge
from tools.utils import api_request

EXECUTION_ARCHIVED_MSG = ("Execution report is archived. It is not possible to read execution "
                          "information from an archived execution.")


class ReportManager(Manager):

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    def _extract_execution_name(self, execution_result: BaseResult) -> Optional[str]:
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
        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        # Extract execution name from execution result if available
        execution_name = self._extract_execution_name(execution_result)

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

    async def read_error(self, master_id: Optional[int]):
        """
        Get error report for a given master_id with formatted, AI-friendly structure.
        Includes execution metadata and explanatory context about error metrics.
        """
        if not isinstance(master_id, int) or master_id < 1:
            return BaseResult(error="Missing or invalid required argument 'execution_id'. Expected integer.")

        # Check if it's valid or allowed
        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        execution_name = self._extract_execution_name(execution_result)
        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/reports/errorsreport/data",
            result_formatter=format_error_report,
            result_formatter_params={
                "execution_id": master_id,
                "execution_name": execution_name
            }
        )

    async def read_request_stats(self, master_id: Optional[int]):
        """
        Get request statistics report for a given master_id with formatted, AI-friendly structure.
        Includes execution metadata and explanatory context about metrics per endpoint.
        """
        if not isinstance(master_id, int) or master_id < 1:
            return BaseResult(error="Missing or invalid required argument 'execution_id'. Expected integer.")

        # Check if it's valid or allowed
        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        execution_name = self._extract_execution_name(execution_result)
        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

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

    async def read_anomalies_stats(self, master_id: Optional[int]):
        """
        Get anomaly statistics for a given master_id (test execution).

        Returns a structured report: no anomalies, full per-anomaly details when permitted, or
        statistics_unavailable when the API returns no stats (e.g. account without anomaly access).
        """
        if not isinstance(master_id, int) or master_id < 1:
            return BaseResult(error="Missing or invalid required argument 'execution_id'. Expected integer.")

        execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        execution_name = self._extract_execution_name(execution_result)

        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/anomalies/stats",
            result_formatter=format_anomalies_stats,
            result_formatter_params={
                "execution_id": master_id,
                "execution_name": execution_name,
            },
        )
