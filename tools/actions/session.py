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

from tools.actions.spec import ALL, ActionSpec

HEADER = (
    "Chat session for this conversation. Call it ONCE at the start of the conversation, "
    "before any other BlazeMeter tool, and keep the returned session_id in context."
)

HINTS = (
    "- **CRITICAL**: Pass the returned `session_id` in every call to every other BlazeMeter tool "
    "of this conversation (top-level or inside args). Do not call 'get' again while it keeps working.",
    "- **CRITICAL**: Never reuse a session_id from another conversation: tasks and dataframes are "
    "isolated per session.",
    "- Only call 'get' again when a tool returns error_code SESSION_REQUIRED, SESSION_INVALID or "
    "SESSION_EXPIRED; then use the new session_id and re-run the calls whose tasks or dataframes "
    "you still need.",
)

ACTIONS: tuple[ActionSpec, ...] = (
    ActionSpec(
        name="get",
        transports=ALL,
        body="""Start a new chat session and return its session_id.
    args(dict): No arguments.""",
    ),
)
