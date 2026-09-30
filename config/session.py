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
import re
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from urllib.parse import quote

import httpx

from config.env import env_float

# "bzs_" + 32 chars from the simple-id alphabet (160 random bits). The storage-api
# mints hosted session ids in the same format.
SESSION_ID_PREFIX = "bzs_"
SESSION_ID_ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
SESSION_ID_LENGTH = 32
SESSION_ID_RE = re.compile(r"^bzs_[0-9a-hjkmnp-tv-z]{32}$")
SESSION_TOOL_NAME = "blazemeter_session"
# End-user credential the call runs with, sent to the storage API on every
# session-scoped request (sessions are bound to it; the API keeps only its HMAC).
CREDENTIAL_HEADER = "X-Bzm-Credential"

SESSION_STORAGE_TIMEOUT_SECONDS = env_float("SESSION_STORAGE_TIMEOUT_SECONDS", 15.0, minimum=0.1)


def generate_session_id() -> str:
    body = "".join(secrets.choice(SESSION_ID_ALPHABET) for _ in range(SESSION_ID_LENGTH))
    return f"{SESSION_ID_PREFIX}{body}"


def is_valid_session_id(value: Any) -> bool:
    return isinstance(value, str) and bool(SESSION_ID_RE.fullmatch(value))


class SessionState(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True)
class ChatSession:
    """One conversation's workspace for tasks and dataframes. Never deleted, only expired."""

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
    exactly like an unknown one (INVALID).
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


class InMemorySessionProvider(SessionPort):
    """stdio: sessions live as long as the process and never expire on their own."""

    def __init__(self) -> None:
        self._sessions: dict[str, ChatSession] = {}
        # HMAC of the creating credential per session (process-local key; the
        # credential itself is never kept).
        self._credential_hashes: dict[str, bytes] = {}
        self._hash_key = secrets.token_bytes(32)
        self._lock = asyncio.Lock()

    def _credential_hash(self, credential: str) -> bytes:
        return hmac.new(self._hash_key, credential.encode("utf-8"), hashlib.sha256).digest()

    async def open(self, owner_id: str, credential: str) -> ChatSession:
        async with self._lock:
            session_id = generate_session_id()
            while session_id in self._sessions:
                session_id = generate_session_id()
            now = _utc_now()
            session = ChatSession(
                session_id=session_id,
                owner_id=owner_id,
                state=SessionState.ACTIVE,
                created_at=now,
                last_seen_at=now,
            )
            self._sessions[session_id] = session
            self._credential_hashes[session_id] = self._credential_hash(credential)
            return session

    async def touch(self, session_id: str, owner_id: str, credential: str) -> ChatSession:
        async with self._lock:
            session = self._sessions.get(session_id)
            expected = self._credential_hashes.get(session_id, b"")
            if (
                session is None
                or session.owner_id != owner_id
                or not hmac.compare_digest(expected, self._credential_hash(credential))
            ):
                raise SessionError(SessionErrorCode.INVALID)
            if session.state is SessionState.EXPIRED:
                raise SessionError(SessionErrorCode.EXPIRED)
            touched = replace(session, last_seen_at=_utc_now())
            self._sessions[session_id] = touched
            return touched


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
        self._timeout = timeout_seconds
        self._transport = transport

    def _headers(self, credential: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._caller_token}", CREDENTIAL_HEADER: credential}

    def _client(self) -> httpx.AsyncClient:
        if self._transport is not None:
            return httpx.AsyncClient(transport=self._transport, timeout=self._timeout)
        return httpx.AsyncClient(http2=True, timeout=self._timeout)

    async def open(self, owner_id: str, credential: str) -> ChatSession:
        async with self._client() as client:
            response = await client.post(
                f"{self._base_url}/sessions",
                headers=self._headers(credential),
                json={"owner_id": owner_id},
            )
        response.raise_for_status()
        return _session_from_payload(response.json())

    async def touch(self, session_id: str, owner_id: str, credential: str) -> ChatSession:
        async with self._client() as client:
            response = await client.post(
                f"{self._base_url}/sessions/{quote(session_id, safe='')}/touch",
                headers=self._headers(credential),
                json={"owner_id": owner_id},
            )
        if response.status_code == 404:
            raise SessionError(SessionErrorCode.INVALID)
        if response.status_code == 410:
            raise SessionError(SessionErrorCode.EXPIRED)
        response.raise_for_status()
        return _session_from_payload(response.json())


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
