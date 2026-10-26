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
from typing import Any, Optional

from mcp.server.fastmcp import Context

from config.blazemeter import EXECUTIONS_ENDPOINT
from formatters.execution import (
    format_summary_report,
    format_request_stats,
    format_error_report,
    format_anomalies_stats,
)
from models.manager import Manager
from models.result import BaseResult
from tools import bridge
from tools.utils import api_request, run_as_task

EXECUTION_ARCHIVED_MSG = ("Execution report is archived. It is not possible to read execution "
                          "information from an archived execution.")
# Report name -> (path under the execution, formatter).
_REPORTS = {
    "summary": ("reports/default/summary", format_summary_report),
    "errors": ("reports/errorsreport/data", format_error_report),
    "request_stats": ("reports/aggregatereport/data", format_request_stats),
    "anomalies_stats": ("anomalies/stats", format_anomalies_stats),
}


class ReportManager(Manager):

    def __init__(
        self,
        ctx: Context,
    ):
        super().__init__(ctx)

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

    async def read_report(
            self,
            master_id: int,
            report: str,
            execution_result: Optional[BaseResult] = None,
    ) -> BaseResult:
        """
        One report of an execution. A caller reading several reports of the same
        execution passes ``execution_result`` (access and archival check) to read it once.
        """
        if execution_result is None:
            # Check if it's valid or allowed
            execution_result = await bridge.read_execution(self.token, self.ctx, master_id)
        if execution_result.error:
            return execution_result

        if self._evaluate_archived(execution_result):
            return BaseResult(
                error=EXECUTION_ARCHIVED_MSG,
            )

        path, formatter = _REPORTS[report]
        return await api_request(
            self.token,
            "GET",
            f"{EXECUTIONS_ENDPOINT}/{master_id}/{path}",
            result_formatter=formatter,
            result_formatter_params={
                "execution_id": master_id,
                "execution_name": self._extract_execution_name(execution_result),
            },
        )

    @run_as_task()
    async def read_summary(self, master_id: int):
        return await self.read_report(master_id, "summary")

    @run_as_task()
    async def read_error(self, master_id: Optional[int]):
        """
        Get error report for a given master_id with formatted, AI-friendly structure.
        Includes execution metadata and explanatory context about error metrics.
        """
        if not isinstance(master_id, int) or master_id < 1:
            return BaseResult(error="Missing or invalid required argument 'execution_id'. Expected integer.")
        return await self.read_report(master_id, "errors")

    @run_as_task()
    async def read_request_stats(self, master_id: Optional[int]):
        """
        Get request statistics report for a given master_id with formatted, AI-friendly structure.
        Includes execution metadata and explanatory context about metrics per endpoint.
        """
        if not isinstance(master_id, int) or master_id < 1:
            return BaseResult(error="Missing or invalid required argument 'execution_id'. Expected integer.")
        return await self.read_report(master_id, "request_stats")

    @run_as_task()
    async def read_anomalies_stats(self, master_id: Optional[int]):
        """
        Get anomaly statistics for a given master_id (test execution).

        Returns a structured report: no anomalies, full per-anomaly details when permitted, or
        statistics_unavailable when the API returns no stats (e.g. account without anomaly access).
        """
        if not isinstance(master_id, int) or master_id < 1:
            return BaseResult(error="Missing or invalid required argument 'execution_id'. Expected integer.")
        return await self.read_report(master_id, "anomalies_stats")
