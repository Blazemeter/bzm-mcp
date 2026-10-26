"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    10|Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

STDIO = "stdio"
HTTP = "streamable-http"
ALL = frozenset({STDIO, HTTP})


@dataclass(frozen=True)
class ActionSpec:
    """Policy of one tool action: transports, required args, and LLM prose."""

    name: str
    transports: frozenset[str]
    body: str
    required_args: tuple[str, ...] = ()


def filter_actions(transport: str, specs: Sequence[ActionSpec]) -> tuple[ActionSpec, ...]:
    visible = tuple(spec for spec in specs if transport in spec.transports)
    names = [spec.name for spec in visible]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate action names for {transport}: {duplicates}")
    return visible


def action_by_name(actions: Sequence[ActionSpec], name: str) -> ActionSpec | None:
    for spec in actions:
        if spec.name == name:
            return spec
    return None


def render_description(
    header: str,
    actions: Sequence[ActionSpec],
    hints: Sequence[str] = (),
) -> str:
    parts: list[str] = []
    if header.strip():
        parts.append(header.strip())
    parts.append("Actions:")
    for spec in actions:
        body = spec.body.strip()
        parts.append(f"- {spec.name}: {body}")
    if hints:
        parts.append("Hints:")
        parts.extend(hint.rstrip() for hint in hints)
    return "\n".join(parts) + "\n"
