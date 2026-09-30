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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from config.blazemeter import USER_ENDPOINT
from config.env import env_int
from config.token import BzmToken

# How long a successful verification may be reused once the cache is integrated.
IDENTITY_CACHE_TTL_SECONDS = env_int("IDENTITY_CACHE_TTL_SECONDS", 300, minimum=0)


@dataclass(frozen=True)
class Identity:
    """Caller verified against BlazeMeter; ``user_id`` owns sessions and partitions."""

    user_id: str


class IdentityError(Exception):
    code = "AUTH_INVALID"
    public_detail = "Invalid credentials."

    def __init__(self, detail: Optional[str] = None):
        super().__init__(detail or self.public_detail)
        self.detail = detail or self.public_detail


class InvalidCredentials(IdentityError):
    """No token, or BlazeMeter rejected it (401/403)."""


class IdentityUnavailable(IdentityError):
    """BlazeMeter could not be reached; never cached, the next call retries."""

    code = "AUTH_UNAVAILABLE"
    public_detail = "Could not verify credentials with BlazeMeter. Try again."


class IdentityPort(ABC):
    @abstractmethod
    async def verify(self, token: Optional[BzmToken]) -> Identity:
        raise NotImplementedError


class BlazeMeterIdentityVerifier(IdentityPort):
    """Resolve the BlazeMeter user behind a token with ``GET /user`` on every call."""

    async def verify(self, token: Optional[BzmToken]) -> Identity:
        # TODO(cache): once CachePort (CACHE_METHOD) is integrated, reuse successful
        # verifications for IDENTITY_CACHE_TTL_SECONDS. Key on the whole token
        # credential (id:secret), never on the token id alone: a key without the
        # secret would let a forged "id:anything" token inherit a cached identity.
        # Do not cache failures from IdentityUnavailable.
        from tools.utils import api_request

        if token is None:
            raise InvalidCredentials(
                "No API token. Set BLAZEMETER_API_KEY env var with file path or API_KEY_ID and "
                "API_KEY_SECRET secrets in docker catalog configuration."
            )
        try:
            response = await api_request(token, "GET", USER_ENDPOINT)
        except Exception as exc:
            raise IdentityUnavailable() from exc
        if response.error:
            raise InvalidCredentials(str(response.error))
        user = response.result[0] if response.result else None
        user_id = user.get("id") if isinstance(user, dict) else None
        if user_id is None or not str(user_id).strip():
            raise InvalidCredentials()
        return Identity(user_id=str(user_id).strip())
