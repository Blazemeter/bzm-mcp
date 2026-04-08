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
from typing import Any, Dict, List, Optional

from formatters.failure_criteria_labels import format_failure_criteria_for_tool
from models.failure_criteria import FailureCriteriaConfig, FailureCriterionRule
from models.test import Test
from tools.utils import get_date_time_iso


def _get_failure_criterion_rule_from_api_item(item: Dict[str, Any]) -> FailureCriterionRule:
    return FailureCriterionRule(
        kpi=(item.get("field") or "")
        if isinstance(item.get("field"), str)
        else str(item.get("field") or ""),
        label=item.get("label") if isinstance(item.get("label"), str) else "ALL",
        condition=item.get("op"),
        value=str(item.get("value", "")),
        offset_percent=str(item.get("offsetPercentage", "0.0")),
        stop_test_on_violation=bool(item.get("stopTestOnViolation", False)),
        sliding_window=bool(item.get("slidingWindow", False)),
        ignore_rampup=item.get("ignoreRampup") if isinstance(item.get("ignoreRampup"), bool) else None,
        is_empty=bool(item.get("isEmpty", False)),
    )


def format_failure_criteria(configuration: Dict[str, Any]) -> FailureCriteriaConfig:
    """Map BlazeMeter test configuration JSON to the failure_criteria domain model (read path)."""
    if not isinstance(configuration, dict):
        return FailureCriteriaConfig(enabled=False, rules=[])

    enabled = bool(configuration.get("enableFailureCriteria", False))
    plugins = configuration.get("plugins")
    if not isinstance(plugins, dict):
        return FailureCriteriaConfig(enabled=enabled, rules=[])

    th = plugins.get("thresholds")
    if not isinstance(th, dict):
        return FailureCriteriaConfig(enabled=enabled, rules=[])

    raw_rules = th.get("thresholds")
    rules: List[FailureCriterionRule] = []
    if isinstance(raw_rules, list):
        for item in raw_rules:
            if isinstance(item, dict):
                rules.append(_get_failure_criterion_rule_from_api_item(item))

    def _optional_bool(key: str) -> Optional[bool]:
        v = th.get(key)
        return v if isinstance(v, bool) else None

    return FailureCriteriaConfig(
        enabled=enabled,
        rules=rules,
        ignore_rampup=_optional_bool("ignoreRampup"),
        from_taurus=_optional_bool("fromTaurus"),
        criteria_overridden_in_interface=_optional_bool("isOverriddenByUi"),
    )


def format_tests(tests: List[Any], params: Optional[dict] = None) -> List[Test]:
    formatted_tests = []
    for test in tests:
        configuration = test.get("configuration", {})
        if not isinstance(configuration, dict):
            configuration = {}
        formatted_tests.append(
            Test(
                test_id=test.get("id"),
                test_name=test.get("name", "Unknown"),
                description=test.get("description", ""),
                created=get_date_time_iso(test.get("created")),
                updated=get_date_time_iso(test.get("updated")),
                project_id=test.get("projectId"),
                configuration=configuration,
                override_executions=test.get("overrideExecutions", []),
                failure_criteria=format_failure_criteria_for_tool(
                    format_failure_criteria(configuration)
                ),
            )
        )
    return formatted_tests
