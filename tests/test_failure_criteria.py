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

import pytest

from config.blazemeter import TOOLS_PREFIX
from formatters.failure_criteria_labels import (
    FAILURE_CRITERIA_GENERAL_FIELDS,
    failure_criteria_meta_payload,
    format_failure_criteria_for_tool,
)
from formatters.test import format_failure_criteria, format_tests
from models.failure_criteria import (
    FailureCriteriaConfig,
    FailureCriterionRule,
    failure_criteria_from_configure_args,
    merge_failure_criteria_into_configuration_dict,
    rule_to_api_dict,
)
from tools.test_manager import register as register_tests_tool


class TestFormatFailureCriteria:
    def test_empty_configuration(self):
        fc = format_failure_criteria({})
        assert fc.enabled is False
        assert fc.rules == []
        assert fc.sliding_window_for_all is False

    def test_parses_rules_and_enabled(self):
        cfg = {
            "enableFailureCriteria": True,
            "plugins": {
                "thresholds": {
                    "thresholds": [
                        {
                            "field": "errors.rate",
                            "label": "ALL",
                            "op": "gte",
                            "value": "1",
                            "offsetPercentage": "0.0",
                            "isEmpty": False,
                            "stopTestOnViolation": False,
                            "ignoreRampup": False,
                            "slidingWindow": True,
                        }
                    ],
                    "ignoreRampup": True,
                    "fromTaurus": False,
                    "isOverriddenByUi": True,
                },
                "jmeter": {"version": "stable"},
            },
        }
        fc = format_failure_criteria(cfg)
        assert fc.enabled is True
        assert len(fc.rules) == 1
        assert fc.rules[0].kpi == "errors.rate"
        assert fc.rules[0].sliding_window is True
        assert fc.ignore_rampup is True
        assert fc.sliding_window_for_all is True

    def test_sliding_window_for_all_false_when_one_rule_off(self):
        cfg = {
            "enableFailureCriteria": True,
            "plugins": {
                "thresholds": {
                    "thresholds": [
                        {"field": "a", "slidingWindow": True},
                        {"field": "b", "slidingWindow": False},
                    ]
                }
            },
        }
        fc = format_failure_criteria(cfg)
        assert fc.sliding_window_for_all is False


class TestFormatFailureCriteriaForTool:
    def test_mcp_keys_match_tool_args(self):
        fc = FailureCriteriaConfig(
            enabled=True,
            ignore_rampup=True,
            rules=[
                FailureCriterionRule(
                    kpi="errors.percent",
                    label="ALL",
                    condition="gte",
                    value="5",
                    offset_percent="0.0",
                    stop_test_on_violation=True,
                    sliding_window=True,
                )
            ],
        )
        out = format_failure_criteria_for_tool(fc)
        assert out["enabled"] is True
        assert out["ignore_rampup"] is True
        assert out["sliding_window_for_all"] is True
        assert out["meta"]["kpi_labels"]["errors.percent"] == "Error Percentage"
        assert out["meta"]["condition_labels"]["gte"] == "Greater than or equal to"
        row = out["rules"][0]
        assert row["kpi"] == "errors.percent"
        assert row["condition"] == "gte"
        assert row["value"] == "5"
        assert row["offset_percent"] == "0.0"
        assert row["stop_test_on_violation"] is True
        assert row["sliding_window"] is True

    def test_meta_uses_empty_string_key_for_null_condition(self):
        fc = FailureCriteriaConfig(
            enabled=True,
            rules=[FailureCriterionRule(kpi="errors.rate", condition=None, value="")],
        )
        out = format_failure_criteria_for_tool(fc)
        assert out["meta"]["condition_labels"][""] == "No condition selected"
        assert out["rules"][0]["condition"] is None

    def test_meta_structure_when_no_rules(self):
        out = format_failure_criteria_for_tool(FailureCriteriaConfig(enabled=False, rules=[]))
        assert out["meta"]["kpi_labels"] == {}
        assert out["meta"]["condition_labels"] == {}
        assert len(out["meta"]["general"]) == len(FAILURE_CRITERIA_GENERAL_FIELDS)
        assert out["meta"]["general"][0]["key"] == "enabled"
        assert out["meta"]["general_labels"]["enabled"] == "Failure Criteria section on or off for the test"
        assert "stop_test_on_violation" in out["meta"]["rule_field_labels"]

    def test_format_tests_failure_criteria_shape(self):
        tests = format_tests(
            [
                {
                    "id": 1,
                    "name": "t",
                    "description": "",
                    "projectId": 9,
                    "configuration": {
                        "enableFailureCriteria": True,
                        "plugins": {
                            "thresholds": {
                                "thresholds": [
                                    {
                                        "field": "hits.rate",
                                        "label": "ALL",
                                        "op": "lt",
                                        "value": "10",
                                        "offsetPercentage": "0.0",
                                        "isEmpty": False,
                                        "stopTestOnViolation": False,
                                        "slidingWindow": False,
                                    }
                                ],
                                "ignoreRampup": False,
                            }
                        },
                    },
                    "overrideExecutions": [],
                }
            ]
        )
        fc = tests[0].failure_criteria
        assert fc["enabled"] is True
        assert fc["meta"]["kpi_labels"]["hits.rate"] == "Avg. Hits/s"
        assert fc["meta"]["condition_labels"]["lt"] == "Less than"


class TestSerializeAndMerge:
    def test_rule_to_api_dict(self):
        r = FailureCriterionRule(
            kpi="responseTime.avg",
            label="ALL",
            condition="gt",
            value="500",
            offset_percent="0.0",
            stop_test_on_violation=True,
            sliding_window=True,
            ignore_rampup=True,
        )
        d = rule_to_api_dict(r)
        assert d["field"] == "responseTime.avg"
        assert d["slidingWindow"] is True
        assert d["stopTestOnViolation"] is True
        assert d["ignoreRampup"] is True

    def test_merge_preserves_jmeter(self):
        existing = {
            "type": "taurus",
            "plugins": {
                "jmeter": {"version": "stable", "consoleArgs": ""},
                "thresholds": {
                    "thresholds": [],
                    "ignoreRampup": False,
                    "fromTaurus": False,
                    "isOverriddenByUi": False,
                },
            },
        }
        fc = FailureCriteriaConfig(
            enabled=True,
            rules=[
                FailureCriterionRule(
                    kpi="errors.rate",
                    condition="gte",
                    value="5",
                    sliding_window=False,
                )
            ],
        )
        merged = merge_failure_criteria_into_configuration_dict(existing, fc)
        assert merged["plugins"]["jmeter"]["version"] == "stable"
        assert len(merged["plugins"]["thresholds"]["thresholds"]) == 1
        assert merged["plugins"]["thresholds"]["thresholds"][0]["field"] == "errors.rate"
        assert merged["enableFailureCriteria"] is True


class TestFailureCriteriaFromConfigureArgs:
    def test_sliding_window_for_all_overrides_each_rule(self):
        fc = failure_criteria_from_configure_args(
            {
                "enabled": True,
                "rules": [
                    {"kpi": "a", "sliding_window": False},
                    {"kpi": "b", "sliding_window": False},
                ],
                "sliding_window_for_all": True,
            }
        )
        assert all(r.sliding_window for r in fc.rules)
        assert fc.sliding_window_for_all is True

    def test_requires_enabled_and_rules(self):
        with pytest.raises(ValueError, match="enabled"):
            failure_criteria_from_configure_args({"rules": []})
        with pytest.raises(ValueError, match="rules"):
            failure_criteria_from_configure_args({"enabled": True})


class _FakeMcpForTests:
    def __init__(self):
        self.tools = {}

    def tool(self, name, description):
        def decorator(func):
            self.tools[name] = func
            return func

        return decorator


class TestFailureCriteriaMetaPayload:
    def test_contains_catalog(self):
        p = failure_criteria_meta_payload()
        assert "layers" in p
        assert "top_level_tool_args" in p and "rule_fields" in p
        assert "general" in p and "kpis" in p and "conditions" in p
        assert len(p["general"]) == len(FAILURE_CRITERIA_GENERAL_FIELDS)
        assert any(x["key"] == "test_id" for x in p["top_level_tool_args"])
        assert any(x["key"] == "kpi" for x in p["rule_fields"])
        assert p["general_labels"]["ignore_rampup"]
        assert "value" in p["rule_field_labels"]


class TestFailureCriteriaMetaAction:
    def test_tool_returns_catalog_without_api(self):
        mcp = _FakeMcpForTests()
        register_tests_tool(mcp, token=None)
        tool = mcp.tools[f"{TOOLS_PREFIX}_tests"]
        result = asyncio.run(tool("failure_criteria_meta", {}, ctx=None))
        assert result.error is None
        payload = result.result[0]
        assert "top_level_tool_args" in payload
        assert "general" in payload and "kpis" in payload and "conditions" in payload
        assert "general_labels" in payload
