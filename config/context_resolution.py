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
from typing import Any

from config.auth import BZM_TOKEN_STATE_ATTR, BZM_USER_CONFIG_STATE_ATTR


def get_request_context(ctx: Any) -> Any:
    return getattr(ctx, "request_context", None)


def get_request_state(ctx: Any) -> Any:
    request_context = get_request_context(ctx)
    request = getattr(request_context, "request", None)
    return getattr(request, "state", None)


def resolve_ctx_user_config(ctx: Any) -> dict[str, Any]:
    request_context = get_request_context(ctx)
    request_state = get_request_state(ctx)

    request_context_config = getattr(request_context, BZM_USER_CONFIG_STATE_ATTR, None)
    if isinstance(request_context_config, dict):
        return request_context_config

    request_state_config = getattr(request_state, BZM_USER_CONFIG_STATE_ATTR, None)
    if isinstance(request_state_config, dict):
        return request_state_config

    return {}


def resolve_ctx_token(ctx: Any) -> Any:
    user_config = resolve_ctx_user_config(ctx)
    request_state = get_request_state(ctx)
    request_state_token = getattr(request_state, BZM_TOKEN_STATE_ATTR, None)
    return user_config.get("token") or request_state_token
