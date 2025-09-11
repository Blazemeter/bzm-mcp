from typing import Any, List

from config.blazemeter import BZM_BASE_URL
from models.execution import TestExecution, TestExecutionDetailed, TestExecutionStatus, TestExecutionStatuses
from tools.utils import get_date_time_iso


def format_executions(executions: List[Any]) -> List[TestExecution]:
    formatted_executions = []
    for execution in executions:
        execution_id = execution.get("id")
        execution_name = execution.get("name")
        formatted_executions.append(
            TestExecution(
                execution_id=execution_id,
                execution_name=execution_name,
                execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}"
            )
        )
    return formatted_executions


def format_executions_detailed(executions: List[Any]) -> List[TestExecutionDetailed]:
    formatted_executions = []
    for execution in executions:
        execution_id = execution.get("id")
        formatted_executions.append(
            TestExecutionDetailed(
                execution_id=execution_id,
                execution_name=execution.get("name"),
                execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}",
                created=get_date_time_iso(execution.get("created")),
                updated=get_date_time_iso(execution.get("updated")),
                ended=get_date_time_iso(execution.get("ended")),
                execution_status=execution.get("reportStatus", "unset"),
                execution_status_detailed=None
            )
        )
    return formatted_executions


def format_executions_status(statuses: List[Any]) -> List[TestExecutionStatus]:
    formatted_statuses = []
    for status_element in statuses:
        execution_step = status_element.get("executionStep", "Unknown")
        status = status_element.get("statuses")
        formatted_statuses.append(
            TestExecutionStatus(
                progress_percent=status.get("ended", 0),
                execution_step=execution_step,
                execution_statuses=TestExecutionStatuses(
                    pending_percent=status.get("pending", 0),
                    booting_percent=status.get("booting", 0),
                    downloading_percent=status.get("downloading", 0),
                    ready_percent=status.get("ready", 0),
                    ended_percent=status.get("ended", 0),
                )
            )
        )
    return formatted_statuses
