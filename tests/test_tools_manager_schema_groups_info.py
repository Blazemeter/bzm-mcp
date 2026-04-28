import asyncio

from tools.dataframe_manager import clear_dataframes, register_dataframe
from tools.tools_manager import ToolsManager


def _clear_dataframes():
    asyncio.run(clear_dataframes())


def test_schema_groups_info_adds_critical_hint_when_variations_exist():
    _clear_dataframes()
    # Use flatten=False to preserve nested schema for variation detection (configuration struct)
    asyncio.run(
        register_dataframe(
            result=[{"id": 1, "configuration": {"threads": 10}}],
            origin_manager="tests",
            origin_action="seed1",
            json_size_chars=9001,
            flatten=False,
        )
    )
    asyncio.run(
        register_dataframe(
            result=[{"id": 2, "configuration": {"threads": "10"}}],
            origin_manager="tests",
            origin_action="seed2",
            json_size_chars=9001,
            flatten=False,
        )
    )

    manager = ToolsManager(token=None, ctx=None)
    response = asyncio.run(manager.dataframes_schema_groups())

    assert response.info is not None
    assert any("Column variations were detected" in msg for msg in response.info)
