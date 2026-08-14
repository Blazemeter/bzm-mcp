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
from mcp.server.fastmcp import Context

from config.auth import BZM_TOKEN_STATE_ATTR, BZM_USER_CONFIG_STATE_ATTR

class Manager:
    def __init__(
        self,
        ctx: Context,
    ):
        self.ctx = ctx
        # depending on the transport, I can get the token from the request context or request state inside ctx
        request_context = getattr(ctx, "request_context", None)
        request_state = getattr(getattr(request_context, "request", None), "state", None)

        request_context_config = getattr(request_context, BZM_USER_CONFIG_STATE_ATTR, None)
        request_state_config = getattr(request_state, BZM_USER_CONFIG_STATE_ATTR, None)

        if isinstance(request_context_config, dict):
            user_config = request_context_config
        elif isinstance(request_state_config, dict):
            user_config = request_state_config
        else:
            user_config = {}

        request_state_token = getattr(request_state, BZM_TOKEN_STATE_ATTR, None)
        self.token = user_config.get("token") or request_state_token
