from formatters.test import format_tests_minimal


def test_format_tests_minimal_drops_heavy_configuration_fields():
    raw = [
        {
            "id": 1,
            "name": "T1",
            "description": "desc",
            "created": 0,
            "updated": 0,
            "projectId": 10,
            "configuration": {"huge": {"nested": [1, 2, 3]}},
            "overrideExecutions": [{"k": "v"}],
        }
    ]

    formatted = format_tests_minimal(raw)
    assert len(formatted) == 1
    assert formatted[0]["test_id"] == 1
    assert formatted[0]["project_id"] == 10
    assert "configuration" not in formatted[0]
    assert "override_executions" not in formatted[0]
