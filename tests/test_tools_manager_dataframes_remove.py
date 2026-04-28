import asyncio

from tools.dataframe_manager import clear_dataframes, register_dataframe, get_dataframe_metadata
from tools.tools_manager import ToolsManager


def _clear_dataframes():
    asyncio.run(clear_dataframes())


def test_dataframes_remove_supports_list_of_ids():
    _clear_dataframes()
    first = asyncio.run(
        register_dataframe(
            result=[{"id": 1, "name": "a"}],
            origin_manager="tests",
            origin_action="seed1",
            json_size_chars=9001,
        )
    )
    second = asyncio.run(
        register_dataframe(
            result=[{"id": 2, "name": "b"}],
            origin_manager="tests",
            origin_action="seed2",
            json_size_chars=9001,
        )
    )

    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(
        manager.dataframes_remove(dataframe_id_list=[first["dataframe_id"], second["dataframe_id"]])
    )

    assert response.error is None
    assert response.result is not None
    assert len(response.result) == 2
    assert all(item["removed"] is True for item in response.result)
    assert asyncio.run(get_dataframe_metadata(first["dataframe_id"])) is None
    assert asyncio.run(get_dataframe_metadata(second["dataframe_id"])) is None


def test_dataframes_remove_requires_non_empty_list():
    _clear_dataframes()
    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(manager.dataframes_remove(dataframe_id_list=[]))
    assert response.error is not None
    assert "dataframe_id_list" in response.error
