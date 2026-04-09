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

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

from models.failure_criteria import FailureCriteriaConfig, FailureCriterionRule

KPI_FIELD_PRODUCT_LABEL_EN: Dict[str, str] = {
    "responseTime.avg": "Avg. Response Time",
    "responseTime.min": "Min response time",
    "responseTime.max": "Max response time",
    "responseTime.std": "Response time standard deviation",
    "responseTime.percentile.0": "Percentile 0",
    "responseTime.percentile.50": "Median / 50th percentile",
    "responseTime.percentile.90": "90th percentile (P90)",
    "responseTime.percentile.95": "95th percentile (P95)",
    "responseTime.percentile.99": "99th percentile (P99)",
    "latency.avg": "Average latency",
    "connectTime.avg": "Average connect time",
    "size.count": "Size count",
    "size.avg": "Average size",
    "size.rate": "Size rate",
    "hits.count": "Hits count",
    "hits.avg": "Average hits",
    "hits.rate": "Avg. Hits/s",
    "duration.count": "Duration count",
    "errors.count": "Error count",
    "errors.percent": "Error Percentage",
    "errors.rate": "Error rate",
}

CONDITION_OP_PRODUCT_LABEL_EN: Dict[Optional[str], str] = {
    None: "No condition selected",
    "lt": "Less than",
    "gt": "Greater than",
    "eq": "Equal to",
    "ne": "Not equal to",
    "lte": "Less than or equal to",
    "gte": "Greater than or equal to",
}

FAILURE_CRITERIA_GENERAL_FIELDS: List[Dict[str, str]] = [
    {"key": "enabled", "label": "Failure Criteria section on or off for the test"},
    {"key": "ignore_rampup", "label": "Ignore failure criteria during ramp-up (advanced configuration)"},
    {"key": "sliding_window_for_all", "label": "Whether every rule uses 1-min slide window"},
    {"key": "from_taurus", "label": "Failure criteria imported from Taurus script"},
    {"key": "criteria_overridden_in_interface", "label": "Failure criteria overridden in product vs script"},
]

FAILURE_CRITERIA_TOP_LEVEL_TOOL_ARGS: List[Dict[str, Any]] = [
    {
        "key": "test_id",
        "required": True,
        "label": "BlazeMeter test id",
    },
    {"key": "enabled", "required": True, "label": "Turn Failure Criteria on or off for this test"},
    {
        "key": "rules",
        "required": True,
        "label": "Full list of criterion rows; replaces all existing rows for the test",
    },
    {
        "key": "ignore_rampup",
        "required": False,
        "label": "Container-level ignore during ramp-up",
    },
    {
        "key": "sliding_window_for_all",
        "required": False,
        "label": "If set, applies the same sliding_window boolean to every rule after parse",
    },
    {
        "key": "from_taurus",
        "required": False,
        "label": "Threshold block fromTaurus",
    },
    {
        "key": "criteria_overridden_in_interface",
        "required": False,
        "label": "Threshold block override flag",
    },
]

FAILURE_CRITERIA_RULE_FIELDS: List[Dict[str, str]] = [
    {"key": "kpi", "label": "Metric id"},
    {"key": "label", "label": "Scope label for the metric (default ALL)"},
    {"key": "condition", "label": "Operator code"},
    {"key": "value", "label": "Threshold as string"},
    {"key": "offset_percent", "label": "Baseline percentage offset string"},
    {"key": "stop_test_on_violation", "label": "Stop the test when this criterion is violated"},
    {"key": "sliding_window", "label": "1-min slide window eval for this row"},
    {"key": "ignore_rampup", "label": "Per-row ignore ramp-up"},
    {"key": "is_empty", "label": "Incomplete row"},
]


def _general_labels_dict() -> Dict[str, str]:
    return {row["key"]: row["label"] for row in FAILURE_CRITERIA_GENERAL_FIELDS}


def _rule_field_labels_dict() -> Dict[str, str]:
    return {row["key"]: row["label"] for row in FAILURE_CRITERIA_RULE_FIELDS}


def _condition_dict_key(op: Optional[str]) -> str:
    """JSON-friendly key for condition_labels (null op maps to empty string)."""
    return "" if op is None else str(op)


def _label_for_condition(op: Optional[str]) -> str:
    if op in CONDITION_OP_PRODUCT_LABEL_EN:
        return CONDITION_OP_PRODUCT_LABEL_EN[op]
    return op if op else CONDITION_OP_PRODUCT_LABEL_EN[None]


def _collect_kpi_and_condition_labels(
        rules: List[FailureCriterionRule],
) -> tuple[Dict[str, str], Dict[str, str]]:
    kpi_labels: Dict[str, str] = {}
    condition_labels: Dict[str, str] = {}
    for r in rules:
        kid = r.kpi
        if kid and kid not in kpi_labels:
            kpi_labels[kid] = KPI_FIELD_PRODUCT_LABEL_EN.get(kid, kid)
        ck = _condition_dict_key(r.condition)
        if ck not in condition_labels:
            condition_labels[ck] = _label_for_condition(r.condition)
    return kpi_labels, condition_labels


def build_failure_criteria_meta(rules: List[FailureCriterionRule]) -> Dict[str, Any]:
    """
    Per-test meta: static field definitions, label maps keyed like response fields, dynamic kpi/condition maps.
    """
    kpi_labels, condition_labels = _collect_kpi_and_condition_labels(rules)
    return {
        "general": copy.deepcopy(FAILURE_CRITERIA_GENERAL_FIELDS),
        "general_labels": _general_labels_dict(),
        "rule_fields": copy.deepcopy(FAILURE_CRITERIA_RULE_FIELDS),
        "rule_field_labels": _rule_field_labels_dict(),
        "kpi_labels": kpi_labels,
        "condition_labels": condition_labels,
    }


def _format_rule_for_tool(rule: FailureCriterionRule) -> Dict[str, Any]:
    """One rule: same keys as configure_failure_criteria rules[]."""
    row: Dict[str, Any] = {
        "kpi": rule.kpi,
        "label": rule.label,
        "condition": rule.condition,
        "value": rule.value,
        "offset_percent": rule.offset_percent,
        "stop_test_on_violation": rule.stop_test_on_violation,
        "sliding_window": rule.sliding_window,
        "is_empty": rule.is_empty,
    }
    if rule.ignore_rampup is not None:
        row["ignore_rampup"] = rule.ignore_rampup
    return row


def format_failure_criteria_for_tool(fc: FailureCriteriaConfig) -> Dict[str, Any]:
    """failure_criteria on Test: same field names as configure_failure_criteria (plus meta)."""
    out: Dict[str, Any] = {
        "enabled": fc.enabled,
        "ignore_rampup": fc.ignore_rampup,
        "sliding_window_for_all": fc.sliding_window_for_all,
        "meta": build_failure_criteria_meta(fc.rules),
        "rules": [_format_rule_for_tool(r) for r in fc.rules],
    }
    if fc.from_taurus is not None:
        out["from_taurus"] = fc.from_taurus
    if fc.criteria_overridden_in_interface is not None:
        out["criteria_overridden_in_interface"] = fc.criteria_overridden_in_interface
    return out


def failure_criteria_meta_payload() -> Dict[str, Any]:
    """Catalog: parameters, field labels, KPI and condition value lists."""
    kpis = [{"kpi": kid, "label": lbl} for kid, lbl in sorted(KPI_FIELD_PRODUCT_LABEL_EN.items())]
    cond_items = list(CONDITION_OP_PRODUCT_LABEL_EN.items())
    cond_items.sort(key=lambda x: ("\x00" if x[0] is None else str(x[0]),))
    conditions = [{"op": op, "label": lbl} for op, lbl in cond_items]
    return {
        "layers": "Reading a test and configuring failure criteria use the same field names in tool data.",
        "top_level_tool_args": copy.deepcopy(FAILURE_CRITERIA_TOP_LEVEL_TOOL_ARGS),
        "rule_fields": copy.deepcopy(FAILURE_CRITERIA_RULE_FIELDS),
        "general": copy.deepcopy(FAILURE_CRITERIA_GENERAL_FIELDS),
        "general_labels": _general_labels_dict(),
        "rule_field_labels": _rule_field_labels_dict(),
        "kpis": kpis,
        "conditions": conditions,
    }
