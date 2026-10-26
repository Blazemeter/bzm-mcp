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
import asyncio
from types import SimpleNamespace

import pytest

from config.token import BzmToken
from models.result import BaseResult
from tests.conftest import make_ctx
from tools import report_manager as report_manager_module
from tools.execution_manager import ExecutionManager
from tools.report_manager import EXECUTION_ARCHIVED_MSG, ReportManager


@pytest.fixture
def fake_api(monkeypatch):
    """Counts execution reads and records the report endpoints requested."""
    state = {"execution_reads": 0, "reports": [], "archived": False}

    async def read_execution(self, execution_id):
        state["execution_reads"] += 1
        return BaseResult(result=[{"result": SimpleNamespace(archived=state["archived"]), "context": ""}])

    async def api_request(token, method, endpoint, result_formatter=None, result_formatter_params=None, **kwargs):
        state["reports"].append(endpoint)
        return BaseResult(result=[{"endpoint": endpoint}])

    monkeypatch.setattr(ExecutionManager, "read", read_execution)
    monkeypatch.setattr(report_manager_module, "api_request", api_request)
    return state


def _ctx():
    return make_ctx(BzmToken("user-1", "secret"), "sess-a")


def test_all_reports_read_the_execution_once(fake_api):
    result = asyncio.run(ExecutionManager(_ctx()).read_all_reports(7))
    assert result.error == ""
    assert fake_api["execution_reads"] == 1
    assert fake_api["reports"] == [
        "/masters/7/reports/default/summary",
        "/masters/7/reports/errorsreport/data",
        "/masters/7/reports/aggregatereport/data",
    ]


def test_all_reports_of_an_archived_execution_read_no_report(fake_api):
    fake_api["archived"] = True
    result = asyncio.run(ExecutionManager(_ctx()).read_all_reports(7))
    assert result.error == EXECUTION_ARCHIVED_MSG
    assert fake_api["execution_reads"] == 1
    assert fake_api["reports"] == []


@pytest.mark.parametrize(
    "action, endpoint",
    [
        ("read_summary", "/masters/7/reports/default/summary"),
        ("read_error", "/masters/7/reports/errorsreport/data"),
        ("read_request_stats", "/masters/7/reports/aggregatereport/data"),
        ("read_anomalies_stats", "/masters/7/anomalies/stats"),
    ],
)
def test_each_report_action_still_checks_its_execution(fake_api, action, endpoint):
    result = asyncio.run(getattr(ReportManager(_ctx()), action)(7))
    assert result.error is None
    assert fake_api["execution_reads"] == 1
    assert fake_api["reports"] == [endpoint]
