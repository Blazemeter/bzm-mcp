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
from typing import Any, Optional

import httpx

from config.blazemeter import BZM_API_BASE_URL, NO_API_TOKEN_MESSAGE, USER_ENDPOINT
from config.env import env_float, env_int
from config.http_clients import SharedAsyncClient
from config.token import BzmToken

# How long a successful verification may be reused once the cache is integrated.
IDENTITY_CACHE_TTL_SECONDS = env_int("IDENTITY_CACHE_TTL_SECONDS", 300, minimum=0)
# Every tool call waits for this check, so it gets its own short budget
# instead of the general API timeout.
IDENTITY_TIMEOUT_SECONDS = env_float("IDENTITY_TIMEOUT_SECONDS", 10.0, minimum=0.1)


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
    """Identity could not be confirmed (outage, unexpected status or body); never cached."""

    code = "AUTH_UNAVAILABLE"
    public_detail = "Could not verify credentials with BlazeMeter. Try again."


class IdentityPort(ABC):
    @abstractmethod
    async def verify(self, token: Optional[BzmToken]) -> Identity:
        raise NotImplementedError


class BlazeMeterIdentityVerifier(IdentityPort):
    """
    Resolve the BlazeMeter user behind a token with ``GET /user`` on every call.

    Classified by the real HTTP status (``api_request`` folds every failure into
    one error string): only 401/403 mean the credentials are invalid. Anything
    else (404, 5xx, network, an unexpected body) is IdentityUnavailable, so an
    outage is never reported to the agent as a bad API key.
    """

    def __init__(
            self,
            transport: Optional[httpx.AsyncBaseTransport] = None,
            timeout_seconds: float = IDENTITY_TIMEOUT_SECONDS,
    ) -> None:
        options: dict[str, Any] = {"base_url": BZM_API_BASE_URL, "timeout": timeout_seconds}
        if transport is not None:
            options["transport"] = transport
        else:
            options["http2"] = True
        # Shared: this runs before every tool call.
        self._http = SharedAsyncClient(lambda: httpx.AsyncClient(**options))

    async def verify(self, token: Optional[BzmToken]) -> Identity:
        # TODO(cache): once CachePort (CACHE_METHOD) is integrated, reuse successful
        # verifications for IDENTITY_CACHE_TTL_SECONDS. Key on the whole token
        # credential (id:secret), never on the token id alone: a key without the
        # secret would let a forged "id:anything" token inherit a cached identity.
        # Do not cache failures from IdentityUnavailable.
        if token is None:
            raise InvalidCredentials(NO_API_TOKEN_MESSAGE)
        from tools.utils.common import user_agent

        try:
            response = await self._http.get().get(
                USER_ENDPOINT,
                headers={"Authorization": token.as_basic_auth(), "User-Agent": user_agent},
            )
        except httpx.HTTPError as exc:
            raise IdentityUnavailable() from exc

        if response.status_code in (401, 403):
            raise InvalidCredentials(_error_message(response))
        if response.status_code != 200:
            raise IdentityUnavailable()
        try:
            result = response.json().get("result")
        except (ValueError, AttributeError) as exc:
            raise IdentityUnavailable() from exc
        user = result[0] if isinstance(result, list) and result else result
        user_id = user.get("id") if isinstance(user, dict) else None
        if user_id is None or not str(user_id).strip():
            raise IdentityUnavailable()  # 200 without a user: BlazeMeter's problem, not the key's
        return Identity(user_id=str(user_id).strip())


def _error_message(response: httpx.Response) -> Optional[str]:
    """BlazeMeter's reason for a rejection (``error.message`` or ``message``), if any."""
    try:
        payload = response.json()
    except ValueError:
        return None
    if not isinstance(payload, dict):
        return None
    error = payload.get("error")
    message = error.get("message") if isinstance(error, dict) else error
    message = message or payload.get("message")
    if not isinstance(message, str) or not message.strip():
        return None
    return f"{InvalidCredentials.public_detail} BlazeMeter: {message.strip()[:200]}"
