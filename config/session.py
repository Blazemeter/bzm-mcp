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

import asyncio
import hashlib
import hmac
import logging
import re
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Callable, Optional
from urllib.parse import quote

import httpx

from config.env import env_float, env_int
from config.http_clients import SharedAsyncClient
from config.ids import SIMPLE_ID_ALPHABET, random_id
from config.service_auth import service_headers

logger = logging.getLogger(__name__)

# "bzs_" + 32 chars from the simple-id alphabet (160 random bits). The storage-api
# mints hosted session ids in the same format.
SESSION_ID_PREFIX = "bzs_"
SESSION_ID_LENGTH = 32
SESSION_ID_RE = re.compile(rf"^{SESSION_ID_PREFIX}[{SIMPLE_ID_ALPHABET}]{{{SESSION_ID_LENGTH}}}$")
SESSION_TOOL_NAME = "blazemeter_session"

SESSION_STORAGE_TIMEOUT_SECONDS = env_float("SESSION_STORAGE_TIMEOUT_SECONDS", 15.0, minimum=0.1)
# stdio lifecycle; the same rules and defaults as the storage-api sweeper.
SESSION_IDLE_TIMEOUT_SECONDS = env_int("SESSION_IDLE_TIMEOUT_SECONDS", 7 * 24 * 3600, minimum=1)
SESSION_PURGE_GRACE_SECONDS = env_int("SESSION_PURGE_GRACE_SECONDS", 3600, minimum=0)
SESSION_SWEEP_INTERVAL_SECONDS = env_int("SESSION_SWEEP_INTERVAL_SECONDS", 60, minimum=1)


def generate_session_id() -> str:
    return f"{SESSION_ID_PREFIX}{random_id(SESSION_ID_LENGTH)}"


def is_valid_session_id(value: Any) -> bool:
    return isinstance(value, str) and bool(SESSION_ID_RE.fullmatch(value))


class SessionState(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True)
class ChatSession:
    """One conversation's workspace for tasks and dataframes. Expired, then purged."""

    session_id: str
    owner_id: str
    state: SessionState
    created_at: datetime
    last_seen_at: datetime
    expired_at: Optional[datetime] = None


class SessionErrorCode(str, Enum):
    REQUIRED = "SESSION_REQUIRED"
    INVALID = "SESSION_INVALID"
    EXPIRED = "SESSION_EXPIRED"
    UNAVAILABLE = "SESSION_UNAVAILABLE"
    SERVICE_ERROR = "SESSION_SERVICE_ERROR"


_RECOVERY_HINT = (
    f"Call {SESSION_TOOL_NAME} with action 'get' to obtain a new session_id, use it in every "
    "following tool call, and re-run the tool calls that produced any task or dataframe you "
    "still need: ids from a previous session are not available in the new one."
)

SESSION_ERROR_MESSAGES = {
    SessionErrorCode.REQUIRED: (
        f"'session_id' is a required argument. Call {SESSION_TOOL_NAME} with action 'get' once "
        "at the start of this conversation and pass the returned session_id in every tool call."
    ),
    SessionErrorCode.INVALID: f"Invalid session_id. {_RECOVERY_HINT}",
    SessionErrorCode.EXPIRED: f"This session expired. {_RECOVERY_HINT}",
    # Transient: the session (if any) is still valid, so no renegotiation.
    SessionErrorCode.UNAVAILABLE: "The session service is unavailable right now. Retry the same call in a moment.",
    # Not transient: the service rejected this MCP server's request (configuration).
    SessionErrorCode.SERVICE_ERROR: (
        "The session service rejected this server's request. This is a server configuration "
        "problem and retrying will not help; report it to the server administrator."
    ),
}


class SessionError(Exception):
    def __init__(self, code: SessionErrorCode):
        super().__init__(SESSION_ERROR_MESSAGES[code])
        self.code = code
        self.message = SESSION_ERROR_MESSAGES[code]


class SessionPort(ABC):
    """
    Chat-session registry. Lookups are scoped to the owner and to the credential
    the session was created with (opaque, e.g. the BlazeMeter Authorization value):
    a session owned by someone else, or used with another credential, is reported
    exactly like an unknown one (INVALID). Failures are SessionError, with
    UNAVAILABLE when the registry cannot answer.
    """

    @abstractmethod
    async def open(self, owner_id: str, credential: str) -> ChatSession:
        raise NotImplementedError

    @abstractmethod
    async def touch(self, session_id: str, owner_id: str, credential: str) -> ChatSession:
        """Validate an ACTIVE session of ``owner_id`` + ``credential`` and record the keep-alive."""
        raise NotImplementedError


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class _Entry:
    session: ChatSession
    # HMAC of the creating credential (process-local key; the credential is never kept).
    credential_hash: bytes
    # First "expired, renegotiate" answer: the purge grace starts here.
    expired_notified_at: Optional[datetime] = None

    def purgeable(self, now: datetime, grace: timedelta) -> bool:
        since = self.expired_notified_at or self.session.expired_at
        return since is not None and now - since >= grace


class InMemorySessionProvider(SessionPort):
    """
    stdio: the storage-api lifecycle, in process. ACTIVE → EXPIRED after the idle
    timeout → purged once the grace has passed since the first "expired" answer
    (or since expiry if nobody asked). ``on_purge(owner_id, session_id)`` releases
    what the session held (its partition). Sweeps run on open/touch, at most once
    per sweep interval: a stdio process has no background service to run them.
    """

    def __init__(
            self,
            idle_timeout_seconds: float = SESSION_IDLE_TIMEOUT_SECONDS,
            purge_grace_seconds: float = SESSION_PURGE_GRACE_SECONDS,
            sweep_interval_seconds: float = SESSION_SWEEP_INTERVAL_SECONDS,
            on_purge: Optional[Callable[[str, str], None]] = None,
            clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        self._entries: dict[str, _Entry] = {}
        self._hash_key = secrets.token_bytes(32)
        self._lock = asyncio.Lock()
        self._idle_timeout = timedelta(seconds=idle_timeout_seconds)
        self._purge_grace = timedelta(seconds=purge_grace_seconds)
        self._sweep_interval = timedelta(seconds=sweep_interval_seconds)
        self._on_purge = on_purge
        self._clock = clock
        self._last_sweep: Optional[datetime] = None

    def _credential_hash(self, credential: str) -> bytes:
        return hmac.new(self._hash_key, credential.encode("utf-8"), hashlib.sha256).digest()

    def _expire_if_idle(self, entry: _Entry, now: datetime) -> None:
        session = entry.session
        if session.state is SessionState.ACTIVE and now - session.last_seen_at >= self._idle_timeout:
            entry.session = replace(session, state=SessionState.EXPIRED, expired_at=now)

    def _sweep(self, now: datetime) -> None:
        if self._last_sweep is not None and now - self._last_sweep < self._sweep_interval:
            return
        self._last_sweep = now
        for session_id, entry in list(self._entries.items()):
            self._expire_if_idle(entry, now)
            if entry.session.state is SessionState.EXPIRED and entry.purgeable(now, self._purge_grace):
                del self._entries[session_id]
                if self._on_purge is not None:
                    self._on_purge(entry.session.owner_id, session_id)

    async def open(self, owner_id: str, credential: str) -> ChatSession:
        async with self._lock:
            now = self._clock()
            self._sweep(now)
            session_id = generate_session_id()
            while session_id in self._entries:
                session_id = generate_session_id()
            session = ChatSession(
                session_id=session_id,
                owner_id=owner_id,
                state=SessionState.ACTIVE,
                created_at=now,
                last_seen_at=now,
            )
            self._entries[session_id] = _Entry(session, self._credential_hash(credential))
            return session

    async def touch(self, session_id: str, owner_id: str, credential: str) -> ChatSession:
        async with self._lock:
            now = self._clock()
            self._sweep(now)
            entry = self._entries.get(session_id)
            if (
                entry is None
                or entry.session.owner_id != owner_id
                or not hmac.compare_digest(entry.credential_hash, self._credential_hash(credential))
            ):
                raise SessionError(SessionErrorCode.INVALID)
            self._expire_if_idle(entry, now)
            if entry.session.state is SessionState.EXPIRED:
                if entry.expired_notified_at is None:
                    entry.expired_notified_at = now
                raise SessionError(SessionErrorCode.EXPIRED)
            entry.session = replace(entry.session, last_seen_at=now)
            return entry.session


_TRANSIENT_STATUSES = frozenset({408, 429})


class HttpSessionProvider(SessionPort):
    """Hosted: the storage-api owns the session registry (``/sessions``)."""

    def __init__(
            self,
            base_url: str,
            caller_token: str,
            timeout_seconds: float = SESSION_STORAGE_TIMEOUT_SECONDS,
            transport: Optional[httpx.AsyncBaseTransport] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._caller_token = caller_token
        # Shared client: touch runs on every tool call.
        if transport is not None:
            self._http = SharedAsyncClient(
                lambda: httpx.AsyncClient(transport=transport, timeout=timeout_seconds)
            )
        else:
            self._http = SharedAsyncClient(
                lambda: httpx.AsyncClient(http2=True, timeout=timeout_seconds)
            )

    def _headers(self, credential: str) -> dict[str, str]:
        # Explicit credential: open/touch run before the session is bound to the context.
        return service_headers(self._caller_token, credential)

    async def _post(self, path: str, owner_id: str, credential: str) -> httpx.Response:
        try:
            return await self._http.get().post(
                f"{self._base_url}{path}",
                headers=self._headers(credential),
                json={"owner_id": owner_id},
            )
        except httpx.HTTPError as exc:
            logger.warning("session storage %s unreachable: %s", path, type(exc).__name__)
            raise SessionError(SessionErrorCode.UNAVAILABLE) from exc

    @staticmethod
    def _session_or_unavailable(response: httpx.Response) -> ChatSession:
        status_code = response.status_code
        if status_code in _TRANSIENT_STATUSES or status_code >= 500:
            logger.warning("session storage answered %s", status_code)
            raise SessionError(SessionErrorCode.UNAVAILABLE)
        if status_code >= 400:
            # 401/403: caller token or credential header; 4xx: contract mismatch.
            logger.error("session storage rejected the MCP request with %s", status_code)
            raise SessionError(SessionErrorCode.SERVICE_ERROR)
        try:
            return _session_from_payload(response.json())
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            logger.warning("session storage returned an invalid session payload")
            raise SessionError(SessionErrorCode.UNAVAILABLE) from exc

    async def open(self, owner_id: str, credential: str) -> ChatSession:
        response = await self._post("/sessions", owner_id, credential)
        return self._session_or_unavailable(response)

    async def touch(self, session_id: str, owner_id: str, credential: str) -> ChatSession:
        response = await self._post(
            f"/sessions/{quote(session_id, safe='')}/touch", owner_id, credential
        )
        if response.status_code == 404:
            raise SessionError(SessionErrorCode.INVALID)
        if response.status_code == 410:
            raise SessionError(SessionErrorCode.EXPIRED)
        return self._session_or_unavailable(response)


def _session_from_payload(payload: dict[str, Any]) -> ChatSession:
    expired_at = payload.get("expired_at")
    return ChatSession(
        session_id=str(payload["id"]),
        owner_id=str(payload["owner_id"]),
        state=SessionState(payload["state"]),
        created_at=datetime.fromisoformat(payload["created_at"]),
        last_seen_at=datetime.fromisoformat(payload["last_seen_at"]),
        expired_at=datetime.fromisoformat(expired_at) if expired_at else None,
    )
