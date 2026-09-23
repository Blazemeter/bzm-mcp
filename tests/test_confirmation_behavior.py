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
from types import SimpleNamespace

from config.auth import BZM_USER_CONFIG_STATE_ATTR
from models.result import BaseResult
from tools.utils import Operations, require_confirmation


class _ManagerWithConfirmation:
    def __init__(self, ctx, confirmation_mode: str = "DELETE"):
        request_state = SimpleNamespace(**{BZM_USER_CONFIG_STATE_ATTR: {"confirmation_mode": confirmation_mode}})
        request = SimpleNamespace(state=request_state)
        setattr(ctx, "request_context", SimpleNamespace(request=request))
        self.ctx = ctx

    @require_confirmation(operation=Operations.CREATE)
    async def do_create(self):
        return BaseResult(result=["created"])


class _NoElicitContext:
    async def elicit(self, message, schema):
        raise RuntimeError("elicit not supported")


class _AcceptContext:
    async def elicit(self, message, schema):
        return SimpleNamespace(action="accept", data=True)


class _RejectContext:
    async def elicit(self, message, schema):
        return SimpleNamespace(action="decline", data=False)


class TestConfirmationBehavior:
    def test_blocks_when_confirmation_required_and_elicit_unsupported(self):
        manager = _ManagerWithConfirmation(_NoElicitContext(), confirmation_mode="CUD")

        result = asyncio.run(manager.do_create())

        assert result.error is not None
        assert "confirmation is required" in result.error.lower()
        assert result.result is None

    def test_allows_when_confirmation_required_and_user_accepts(self):
        manager = _ManagerWithConfirmation(_AcceptContext(), confirmation_mode="CUD")

        result = asyncio.run(manager.do_create())

        assert result.error is None
        assert result.result == ["created"]

    def test_returns_cancelled_when_confirmation_required_and_user_declines(self):
        manager = _ManagerWithConfirmation(_RejectContext(), confirmation_mode="CUD")

        result = asyncio.run(manager.do_create())

        assert result.error is None
        assert result.result == ["Action manually cancelled by the user."]

    def test_allows_when_confirmation_not_required_even_without_elicit(self):
        manager = _ManagerWithConfirmation(_NoElicitContext(), confirmation_mode="DISABLE")

        result = asyncio.run(manager.do_create())

        assert result.error is None
        assert result.result == ["created"]
