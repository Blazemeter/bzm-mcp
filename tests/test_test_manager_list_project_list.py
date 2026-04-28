import asyncio

from models.result import BaseResult
from tools.test_manager import TestManager


def test_list_merges_multiple_projects(monkeypatch):
    async def fake_read_project(token, ctx, project_id):
        return BaseResult(result=[{"project_id": project_id}])

    async def fake_api_request(token, method, endpoint, result_formatter=None, params=None, **kwargs):
        project_id = params.get("projectId")
        return BaseResult(
            result=[{"test_id": project_id * 100, "project_id": project_id}],
            total=1,
            has_more=False,
        )

    monkeypatch.setattr("tools.test_manager.bridge.read_project", fake_read_project)
    monkeypatch.setattr("tools.test_manager.api_request", fake_api_request)

    manager = TestManager(token=None, ctx=None)
    response = asyncio.run(manager.list(project_id_list=[10, 20], limit=5, offset=0))

    assert response.error is None
    assert response.result is not None
    assert len(response.result) == 2
    assert {item["project_id"] for item in response.result} == {10, 20}
    assert response.total == 2
    assert response.info is not None
    assert "Merged tests list from 2 projects" in response.info[0]


def test_list_requires_project_id_list():
    manager = TestManager(token=None, ctx=None)
    response = asyncio.run(manager.list(project_id_list=[]))
    assert response.error is not None
    assert "project_id_list" in response.error
