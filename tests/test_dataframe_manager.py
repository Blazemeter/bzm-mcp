import asyncio

import polars as pl

from models.result import BaseResult
from tools.dataframe_manager import (
    auto_flatten_wide,
    build_dataframe_from_result,
    clear_dataframes,
    get_dataframe_metadata,
    group_dataframe_schemas,
    list_dataframes_metadata,
    materialize_large_result_if_needed,
    query_dataframes,
    register_dataframe,
    serialize_result_to_compact_json,
)
from tools.async_task_manager import get_task_record, submit_task
from tools.utils import tool_result


def _clear_all():
    asyncio.run(clear_dataframes())


def test_register_list_get_remove_clear_lifecycle():
    _clear_all()
    metadata = asyncio.run(
        register_dataframe(
            result=[{"id": 1, "name": "alpha"}, {"id": 2, "name": "beta"}],
            origin_manager="tests",
            origin_action="seed",
            json_size_chars=9001,
        )
    )

    assert metadata["rows"] == 2
    assert metadata["columns"] == 2

    listed = asyncio.run(list_dataframes_metadata())
    assert len(listed) == 1
    assert listed[0]["dataframe_id"] == metadata["dataframe_id"]
    assert "schema" not in listed[0]
    assert "schema_hash" in listed[0]

    fetched = asyncio.run(get_dataframe_metadata(metadata["dataframe_id"]))
    assert fetched is not None
    assert fetched["table_name"] == metadata["table_name"]

    removed = asyncio.run(clear_dataframes())
    assert removed == 1
    assert asyncio.run(list_dataframes_metadata()) == []


def test_query_supports_join_and_union():
    _clear_all()
    left = asyncio.run(
        register_dataframe(
            result=[{"id": 1, "v": "a"}, {"id": 2, "v": "b"}],
            origin_manager="tests",
            origin_action="left",
            json_size_chars=9001,
        )
    )
    right = asyncio.run(
        register_dataframe(
            result=[{"id": 1, "w": "x"}, {"id": 3, "w": "y"}],
            origin_manager="tests",
            origin_action="right",
            json_size_chars=9001,
        )
    )

    join_sql = (
        f"SELECT l.id, l.v, r.w FROM {left['table_name']} l "
        f"JOIN {right['table_name']} r ON l.id = r.id ORDER BY l.id LIMIT 100 OFFSET 0"
    )
    join_response = query_dataframes(join_sql)
    assert "error" not in join_response
    assert join_response["rows"] == 1
    assert join_response["result"][0]["columns"] == ["id", "v", "w"]
    assert join_response["result"][0]["rows"][0][0] == 1

    union_sql = (
        f"SELECT id FROM {left['table_name']} "
        f"UNION SELECT id FROM {right['table_name']} ORDER BY id LIMIT 100 OFFSET 0"
    )
    union_response = query_dataframes(union_sql)
    assert "error" not in union_response
    id_idx = union_response["result"][0]["columns"].index("id")
    assert sorted([row[id_idx] for row in union_response["result"][0]["rows"]]) == [1, 2, 3]


def test_group_dataframe_schemas_hierarchical_top_level_and_column_variants():
    _clear_all()
    # Use flatten=False to preserve nested schema for grouping logic (configuration struct)
    first = asyncio.run(
        register_dataframe(
            result=[{"id": 1, "configuration": {"threads": 10}}],
            origin_manager="tests",
            origin_action="a",
            json_size_chars=9001,
            flatten=False,
        )
    )
    second = asyncio.run(
        register_dataframe(
            result=[{"id": 2, "configuration": {"threads": "10"}}],
            origin_manager="tests",
            origin_action="b",
            json_size_chars=9001,
            flatten=False,
        )
    )
    third = asyncio.run(
        register_dataframe(
            result=[{"id": 3, "value": 10}],
            origin_manager="tests",
            origin_action="c",
            json_size_chars=9001,
            flatten=False,
        )
    )

    grouped = asyncio.run(group_dataframe_schemas())
    assert "groups" in grouped
    assert len(grouped["groups"]) == 2

    filtered = asyncio.run(group_dataframe_schemas([first["dataframe_id"], second["dataframe_id"], "missing-id"]))
    assert len(filtered["groups"]) == 1
    assert filtered["missing_df_ids"] == "missing-id"
    assert "df_sets" in filtered
    group = filtered["groups"][0]
    assert "varying_columns" in group
    assert "configuration" in group["varying_columns"].split(",")
    group_ids = set(filtered["df_sets"][group["df_ref"]].split(","))
    assert group_ids == {first["dataframe_id"], second["dataframe_id"]}
    assert third["dataframe_id"] not in group_ids
    configuration_column = next(col for col in group["columns"] if col["name"] == "configuration")
    assert "dtype" not in configuration_column
    assert len(configuration_column["variations"]) == 2
    for version in configuration_column["variations"]:
        assert "hash" not in version
        assert "column_schema" in version
        assert isinstance(version["column_schema"], str)
        assert "df_ref" in version
        assert all(isinstance(df_id, str) for df_id in filtered["df_sets"][version["df_ref"]].split(","))


def test_query_blocks_non_read_only_sql():
    _clear_all()
    response = query_dataframes("DELETE FROM some_table")
    assert "error" in response
    assert "read-only sql is allowed" in response["error"].lower()


def test_query_allows_literals_with_blocked_keywords():
    _clear_all()
    response = query_dataframes("SELECT 'delete' AS word ORDER BY word LIMIT 1 OFFSET 0")
    assert "error" not in response
    assert response["result"][0]["columns"] == ["word"]
    assert response["result"][0]["rows"][0][0] == "delete"


def test_query_requires_order_by_limit_offset():
    _clear_all()
    no_order = query_dataframes("SELECT 1 AS value LIMIT 1 OFFSET 0")
    assert "error" in no_order
    assert "order by is mandatory" in no_order["error"].lower()

    no_limit = query_dataframes("SELECT 1 AS value ORDER BY value OFFSET 0")
    assert "error" in no_limit
    assert "limit is mandatory" in no_limit["error"].lower()

    no_offset = query_dataframes("SELECT 1 AS value ORDER BY value LIMIT 1")
    assert "error" in no_offset
    assert "offset is mandatory" in no_offset["error"].lower()


def test_tool_result_threshold_keeps_small_payload():
    _clear_all()

    @tool_result()
    async def tool_handler(action: str) -> BaseResult:
        return BaseResult(result=[{"value": "ok"}])

    response = asyncio.run(tool_handler("read"))
    assert response.result == [{"value": "ok"}]
    assert asyncio.run(list_dataframes_metadata()) == []


def test_tool_result_threshold_boundary_8000():
    _clear_all()
    payload_size = 1
    while True:
        candidate = [{"payload": "x" * payload_size}]
        serialized_len = len(serialize_result_to_compact_json(candidate))
        if serialized_len >= 8000:
            break
        payload_size += 1
    if serialized_len > 8000:
        payload_size -= 1
        candidate = [{"payload": "x" * payload_size}]
        serialized_len = len(serialize_result_to_compact_json(candidate))

    assert serialized_len <= 8000

    @tool_result()
    async def tool_handler(action: str) -> BaseResult:
        return BaseResult(result=candidate)

    response = asyncio.run(tool_handler("read"))
    assert response.result == candidate
    assert asyncio.run(list_dataframes_metadata()) == []


def test_tool_result_threshold_materializes_large_payload():
    _clear_all()
    large_value = "x" * 8100

    @tool_result()
    async def tool_handler(action: str) -> BaseResult:
        return BaseResult(result=[{"id": 1, "payload": large_value}])

    response = asyncio.run(tool_handler("read"))
    assert response.result is not None
    assert response.result[0]["stored_as_dataframe"] is True
    assert response.result[0]["json_size_chars"] > 8000
    assert len(asyncio.run(list_dataframes_metadata())) == 1


def test_tool_result_forces_dataframe_when_requested():
    _clear_all()

    @tool_result()
    async def tool_handler(action: str, args: dict) -> BaseResult:
        return BaseResult(result=[{"value": "small"}])

    response = asyncio.run(tool_handler("read", {"result_format": "dataframe"}))
    assert response.result is not None
    assert response.result[0]["stored_as_dataframe"] is True
    assert len(asyncio.run(list_dataframes_metadata())) == 1


def test_tool_result_force_dataframe_skips_empty_result():
    _clear_all()

    @tool_result()
    async def tool_handler(action: str, args: dict) -> BaseResult:
        return BaseResult(result=[])

    response = asyncio.run(tool_handler("read", {"result_format": "dataframe"}))
    assert response.result == []
    assert response.info is not None
    assert any("contains no rows" in msg for msg in response.info)
    assert asyncio.run(list_dataframes_metadata()) == []


def test_tool_result_raw_skips_dataframe_even_if_large():
    _clear_all()
    large_value = "x" * 9000

    @tool_result()
    async def tool_handler(action: str, args: dict) -> BaseResult:
        return BaseResult(result=[{"payload": large_value}])

    response = asyncio.run(tool_handler("read", {"result_format": "raw"}))
    assert response.result is not None
    assert isinstance(response.result[0], dict)
    assert response.result[0].get("stored_as_dataframe") is not True
    assert asyncio.run(list_dataframes_metadata()) == []


def test_materialize_large_result_if_needed_for_task_result():
    _clear_all()

    async def scenario():
        async def action():
            return BaseResult(result=[{"payload": "x" * 8200}])

        task_id = submit_task(
            action={"manager": "TestManager", "method": "slow_action"},
            coro_factory=action,
        )
        while True:
            record = get_task_record(task_id)
            if record and record.status in {"completed", "failed", "cancelled"}:
                return record
            await asyncio.sleep(0.01)

    record = asyncio.run(scenario())
    assert record.result is not None
    assert record.result.result is not None
    assert record.result.result[0]["stored_as_dataframe"] is True
    assert len(asyncio.run(list_dataframes_metadata())) == 1


def test_materialize_helper_keeps_small_result_unchanged():
    _clear_all()

    async def _run():
        original = BaseResult(result=[{"ok": True}])
        return await materialize_large_result_if_needed(
            base_result=original,
            origin_manager="demo",
            origin_action="read",
        )

    result = asyncio.run(_run())
    assert result.result == [{"ok": True}]
    assert asyncio.run(list_dataframes_metadata()) == []


def test_auto_flatten_wide_expands_structs_and_flattens_lists():
    """auto_flatten_wide expands nested structs and flattens list columns to scalar."""
    # Struct column: configuration.threads
    df = pl.DataFrame([
        {"id": 1, "configuration": {"threads": 10, "ramp_up": 60}},
        {"id": 2, "configuration": {"threads": 20, "ramp_up": 120}},
    ])
    flattened = auto_flatten_wide(df)
    assert flattened.width >= 3  # id + configuration__threads + configuration__ramp_up
    assert flattened.height == 2
    assert not any(isinstance(dt, pl.Struct) for dt in flattened.schema.values())
    # Path format preserves nesting in column names
    assert "configuration__threads" in flattened.schema.names()

    # List of scalars: take first element
    df_list = pl.DataFrame([
        {"id": 1, "tags": ["a", "b", "c"]},
        {"id": 2, "tags": ["x", "y"]},
    ])
    flattened_list = auto_flatten_wide(df_list)
    assert not any(isinstance(dt, pl.List) for dt in flattened_list.schema.values())
    assert flattened_list.height == 2

    # Deeply nested struct: path accumulates (config__inner__b)
    df_nested = pl.DataFrame([
        {"id": 1, "config": {"a": 1, "inner": {"b": 2, "c": 3}}},
    ])
    flattened_nested = auto_flatten_wide(df_nested)
    assert "config__a" in flattened_nested.schema.names()
    assert "config__inner__b" in flattened_nested.schema.names()
    assert "config__inner__c" in flattened_nested.schema.names()


def test_register_dataframe_flattens_by_default_and_is_queryable():
    """Registration with flatten=True (default) produces path-style flat columns queryable via SQL."""
    _clear_all()
    metadata = asyncio.run(
        register_dataframe(
            result=[
                {"id": 1, "configuration": {"threads": 10}},
                {"id": 2, "configuration": {"threads": 20}},
            ],
            origin_manager="tests",
            origin_action="flatten_check",
            json_size_chars=9001,
        )
    )
    table = metadata["table_name"]
    # Flattened schema uses path format: configuration__threads (preserves nesting in name)
    response = query_dataframes(
        f'SELECT id, "configuration__threads" FROM {table} ORDER BY id LIMIT 10 OFFSET 0'
    )
    assert "error" not in response
    assert response["rows"] == 2
