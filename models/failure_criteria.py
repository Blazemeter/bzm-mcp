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
# HTTP JSON uses BlazeMeter camelCase (enableFailureCriteria, stopTestOnViolation, …).
# Domain models here match the field names used in tool read/configure responses and arguments.

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class FailureCriterionRule(BaseModel):
    """One failure criterion row (domain naming; API uses plugins.thresholds.thresholds[])."""

    model_config = ConfigDict(extra="ignore")

    kpi: str = Field(description="API field name for the KPI, e.g. responseTime.avg, errors.rate")
    label: str = Field(default="ALL", description="Label scope; default ALL")
    condition: Optional[str] = Field(
        default=None,
        description="Comparison operator: lt, gt, eq, ne, lte, gte; None matches API null",
    )
    value: str = Field(default="", description="Threshold as string, same as API")
    offset_percent: str = Field(default="0.0", description="Baseline offset percentage string")
    stop_test_on_violation: bool = Field(
        default=False,
        description="Stop Test (API stopTestOnViolation); typically used with 1-min slide window",
    )
    sliding_window: bool = Field(
        default=False,
        description="1-min slide window eval for this rule (API slidingWindow)",
    )
    ignore_rampup: Optional[bool] = Field(
        default=None,
        description="Per-rule ignore ramp-up when API sends it; None omits key on write",
    )
    is_empty: bool = Field(
        default=False,
        description="Incomplete row flag from API (isEmpty)",
    )


class FailureCriteriaConfig(BaseModel):
    """Failure criteria section (domain model)."""

    model_config = ConfigDict(extra="ignore")

    enabled: bool = Field(
        description="Section master switch (API configuration.enableFailureCriteria)",
    )
    rules: List[FailureCriterionRule] = Field(default_factory=list)
    ignore_rampup: Optional[bool] = Field(
        default=None,
        description="Container-level ignore ramp-up; None preserves existing on merge",
    )
    from_taurus: Optional[bool] = Field(
        default=None,
        description="fromTaurus; None preserves existing on merge",
    )
    criteria_overridden_in_interface: Optional[bool] = Field(
        default=None,
        description="Threshold-block flag from the API; None preserves existing on merge",
    )

    @computed_field
    @property
    def sliding_window_for_all(self) -> bool:
        """
        True when at least one rule exists and every rule has sliding_window enabled
        (same idea as bulk 'Enable 1-min slide window eval for all' in the product).
        """
        if not self.rules:
            return False
        return all(r.sliding_window for r in self.rules)


def rule_to_api_dict(rule: FailureCriterionRule) -> Dict[str, Any]:
    """Serialize one rule to API item shape (camelCase keys)."""
    out: Dict[str, Any] = {
        "field": rule.kpi,
        "label": rule.label,
        "op": rule.condition,
        "value": rule.value,
        "offsetPercentage": rule.offset_percent,
        "isEmpty": rule.is_empty,
        "stopTestOnViolation": rule.stop_test_on_violation,
        "slidingWindow": rule.sliding_window,
    }
    if rule.ignore_rampup is not None:
        out["ignoreRampup"] = rule.ignore_rampup
    return out


def merge_failure_criteria_into_configuration_dict(
        existing_configuration: Dict[str, Any],
        fc: FailureCriteriaConfig,
) -> Dict[str, Any]:
    """
    Return a full configuration dict with failure criteria applied.
    Preserves plugins.jmeter and other configuration keys; merges plugins.thresholds metadata.
    """
    out = copy.deepcopy(existing_configuration) if isinstance(existing_configuration, dict) else {}
    if not isinstance(out, dict):
        out = {}

    plugins = out.setdefault("plugins", {})
    if not isinstance(plugins, dict):
        plugins = {}
        out["plugins"] = plugins

    jmeter = plugins.get("jmeter")
    prev_th = plugins.get("thresholds")
    prev_dict: Dict[str, Any] = dict(prev_th) if isinstance(prev_th, dict) else {}

    new_th: Dict[str, Any] = {**prev_dict}
    new_th["thresholds"] = [rule_to_api_dict(r) for r in fc.rules]

    def _merge_meta(key: str, fc_val: Optional[bool], default: bool) -> None:
        if fc_val is not None:
            new_th[key] = fc_val
        elif key in prev_dict:
            new_th[key] = prev_dict[key]
        else:
            new_th[key] = default

    _merge_meta("ignoreRampup", fc.ignore_rampup, False)
    _merge_meta("fromTaurus", fc.from_taurus, False)
    _merge_meta("isOverriddenByUi", fc.criteria_overridden_in_interface, True)

    plugins["thresholds"] = new_th
    if jmeter is not None:
        plugins["jmeter"] = jmeter

    out["enableFailureCriteria"] = fc.enabled
    return out


def _require_bool(value: Any, message: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(message)
    return value


def _optional_bool_arg(value: Any, arg_name: str) -> Optional[bool]:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"Invalid argument '{arg_name}'. Expected boolean or omit.")
    return value


def _parse_configure_rule(raw: Any, index: int) -> FailureCriterionRule:
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid rules[{index}]: expected an object.")
    kpi = raw.get("kpi")
    if not isinstance(kpi, str) or not kpi.strip():
        raise ValueError(f"Invalid rules[{index}].kpi: required non-empty string.")
    cond = raw.get("condition")
    if cond is not None and not isinstance(cond, str):
        raise ValueError(f"Invalid rules[{index}].condition: expected string or null.")
    ir = raw.get("ignore_rampup")
    if ir is not None and not isinstance(ir, bool):
        raise ValueError(f"Invalid rules[{index}].ignore_rampup: expected boolean or omit.")
    label = raw["label"] if isinstance(raw.get("label"), str) else "ALL"
    return FailureCriterionRule(
        kpi=kpi.strip(),
        label=label,
        condition=cond,
        value=str(raw.get("value", "")),
        offset_percent=str(raw.get("offset_percent", "0.0")),
        stop_test_on_violation=bool(raw.get("stop_test_on_violation", False)),
        sliding_window=bool(raw.get("sliding_window", False)),
        ignore_rampup=ir,
        is_empty=bool(raw.get("is_empty", False)),
    )


def _rules_from_configure_args(rules_raw: Any) -> List[FailureCriterionRule]:
    if rules_raw is None:
        raise ValueError(
            "Missing required argument 'rules'. Expected a list (use empty list to clear rules)."
        )
    if not isinstance(rules_raw, list):
        raise ValueError("Invalid argument 'rules'. Expected a list.")
    return [_parse_configure_rule(raw, i) for i, raw in enumerate(rules_raw)]


def _apply_sliding_window_for_all(
        rules: List[FailureCriterionRule], value: Optional[bool]
) -> List[FailureCriterionRule]:
    if value is None:
        return rules
    return [r.model_copy(update={"sliding_window": value}) for r in rules]


def failure_criteria_from_configure_args(args: Dict[str, Any]) -> FailureCriteriaConfig:
    """
    Validate blazemeter_tests configure_failure_criteria args and build FailureCriteriaConfig.
    Raises ValueError with a message suitable for BaseResult.error.
    """
    enabled = _require_bool(
        args.get("enabled"),
        "Missing or invalid required argument 'enabled'. Expected boolean.",
    )
    rules = _rules_from_configure_args(args.get("rules"))
    sw_all = _optional_bool_arg(args.get("sliding_window_for_all"), "sliding_window_for_all")
    rules = _apply_sliding_window_for_all(rules, sw_all)

    return FailureCriteriaConfig(
        enabled=enabled,
        rules=rules,
        ignore_rampup=_optional_bool_arg(args.get("ignore_rampup"), "ignore_rampup"),
        from_taurus=_optional_bool_arg(args.get("from_taurus"), "from_taurus"),
        criteria_overridden_in_interface=_optional_bool_arg(
            args.get("criteria_overridden_in_interface"),
            "criteria_overridden_in_interface",
        ),
    )
