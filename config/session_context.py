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

import contextvars
from contextlib import contextmanager
from typing import Iterator, Optional

from config.identity import Identity
from config.session import ChatSession

# Request-scoped and set only by the tool entrypoint after validation: the identity
# once BlazeMeter accepted the token, the session once it is ACTIVE and owned by it,
# and the credential the call runs with (sessions are bound to it; the storage API
# re-checks it on every session-scoped request).
_current_identity: contextvars.ContextVar[Optional[Identity]] = contextvars.ContextVar(
    "bzm_current_identity", default=None
)
_current_session: contextvars.ContextVar[Optional[ChatSession]] = contextvars.ContextVar(
    "bzm_current_session", default=None
)
_current_credential: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "bzm_current_credential", default=None
)


class SessionContextMissing(RuntimeError):
    """Session-scoped state was used outside a validated tool call."""


def current_identity() -> Optional[Identity]:
    return _current_identity.get()


def current_session() -> Optional[ChatSession]:
    return _current_session.get()


def current_credential() -> Optional[str]:
    return _current_credential.get()


@contextmanager
def bind_session_context(
        identity: Identity,
        session: Optional[ChatSession] = None,
        credential: Optional[str] = None,
) -> Iterator[None]:
    """Bind a validated identity (and session/credential) for the duration of one tool call."""
    identity_token = _current_identity.set(identity)
    session_token = _current_session.set(session)
    credential_token = _current_credential.set(credential)
    try:
        yield
    finally:
        _current_credential.reset(credential_token)
        _current_session.reset(session_token)
        _current_identity.reset(identity_token)
