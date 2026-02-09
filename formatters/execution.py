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
from typing import Any, List, Optional

from config.blazemeter import BZM_BASE_URL
from models.execution import TestExecution, TestExecutionDetailed, TestExecutionStatus, TestExecutionStatuses
from tools.utils import get_date_time_iso


def format_executions(executions: List[Any], params: Optional[dict] = None) -> List[TestExecution]:
    formatted_executions = []
    for execution in executions:
        execution_id = execution.get("id")
        execution_name = execution.get("name")
        project_id = execution.get("projectId")
        formatted_executions.append(
            TestExecution(
                execution_id=execution_id,
                execution_name=execution_name,
                project_id=project_id,
                execution_url=f"{BZM_BASE_URL}/app/#/masters/{execution_id}"
            )
        )
    return formatted_executions


def format_executions_detailed(executions: List[Any], params: Optional[dict] = None) -> List[TestExecutionDetailed]:
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
                project_id=execution.get("projectId"),
                execution_status=execution.get("reportStatus", "unset"),
                execution_status_detailed=None
            )
        )
    return formatted_executions


def format_executions_status(statuses: List[Any], params: Optional[dict] = None) -> List[TestExecutionStatus]:
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
