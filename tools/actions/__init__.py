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
"""
Action catalogs for MCP tools.

Convention for adding or migrating a tool:
1. One catalog module per MCP tool: ``tools/actions/<domain>.py``.
2. Export ``HEADER``, ``HINTS``, and ``ACTIONS``.
3. ``body`` is LLM prose without a ``- name:`` prefix. ``render_description``
   always emits ``- {name}: {body}``.
4. ``required_args`` is the source of truth for presence checks. Manager
   methods keep type and range checks.
5. The same action name may appear twice only when ``transports`` are disjoint
   (stdio vs HTTP). Always ``filter_actions`` before ``action_by_name``.
6. Do not add unused fields.
7. Register with ``register_managed_tool(..., actions=, header=, hints=)``.
   Do not pass a parallel description string.
8. Dispatch with a handler map keyed by action name, not a growing match/case
   plus a name set.
"""

from tools.actions.spec import (
    ALL,
    HTTP,
    STDIO,
    ActionSpec,
    action_by_name,
    filter_actions,
    render_description,
)

__all__ = [
    "ALL",
    "HTTP",
    "STDIO",
    "ActionSpec",
    "action_by_name",
    "filter_actions",
    "render_description",
]
