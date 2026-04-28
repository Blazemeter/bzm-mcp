import asyncio

from tools.tools_manager import ToolsManager


def test_dataframes_query_uses_requested_output_format_by_default(monkeypatch):
    captured = {}

    def fake_query_dataframes(sql: str, output_format: str = "matrix"):
        captured["sql"] = sql
        captured["output_format"] = output_format
        return {
            "result": [{"id": 1}],
            "rows": 1,
            "columns": 1,
            "schema": [{"name": "id", "dtype": "Int64"}],
            "output_format": output_format,
        }

    monkeypatch.setattr("tools.tools_manager.query_dataframes", fake_query_dataframes)

    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(
        manager.dataframes_query(
            sql="SELECT 1 AS id ORDER BY id LIMIT 1 OFFSET 0",
            output_format="matrix",
            result_format="auto",
        )
    )

    assert response.error is None
    assert captured["output_format"] == "matrix"


def test_dataframes_query_forces_records_when_result_format_dataframe(monkeypatch):
    captured = {}

    def fake_query_dataframes(sql: str, output_format: str = "matrix"):
        captured["sql"] = sql
        captured["output_format"] = output_format
        return {
            "result": [{"id": 1}],
            "rows": 1,
            "columns": 1,
            "schema": [{"name": "id", "dtype": "Int64"}],
            "output_format": output_format,
        }

    monkeypatch.setattr("tools.tools_manager.query_dataframes", fake_query_dataframes)

    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(
        manager.dataframes_query(
            sql="SELECT 1 AS id ORDER BY id LIMIT 1 OFFSET 0",
            output_format="matrix",
            result_format="dataframe",
        )
    )

    assert response.error is None
    assert captured["output_format"] == "records"
    assert response.info is not None
    assert any(
        "dataframes_query uses records internally for dataframe storage" in message
        for message in response.info
    )
