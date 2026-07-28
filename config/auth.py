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

from typing import Optional, Protocol, runtime_checkable

from mcp.server.fastmcp import Context, FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from config.token import BzmToken, BzmTokenError

BZM_TOKEN_STATE_ATTR = "token"


class AuthError(Exception):
    """Raised when Authorization cannot be parsed into credentials."""


@runtime_checkable
class AuthPort(Protocol):
    """Resolves the BlazeMeter API token for the current tool invocation."""

    def get_token(self, ctx: Context) -> Optional[BzmToken]:
        ...


class StdioAuthProvider:
    """Process-lifetime token from env / api-key.json / Docker secrets."""

    def __init__(self, token: Optional[BzmToken]):
        self._token = token

    def get_token(self, ctx: Context) -> Optional[BzmToken]:
        return self._token


class HttpAuthProvider:
    """Per-request token attached by Bearer auth middleware to request.state."""

    def get_token(self, ctx: Context) -> Optional[BzmToken]:
        request = ctx.request_context.request
        if request is None:
            return None
        return getattr(request.state, BZM_TOKEN_STATE_ATTR, None)


def parse_authorization_header(value: Optional[str]) -> BzmToken:
    """
    Parse ``Authorization: Bearer <credentials>`` into a BzmToken.

    Credentials may be ``id:secret`` or base64(``id:secret``). Does not call
    the BlazeMeter API — parse only.
    """
    if not value or not value.strip():
        raise AuthError("Missing Authorization header")

    scheme, _, credentials = value.strip().partition(" ")
    if scheme.lower() != "bearer" or not credentials.strip():
        raise AuthError("Authorization header must use Bearer scheme")

    try:
        return BzmToken.from_bearer_credentials(credentials.strip())
    except BzmTokenError as exc:
        raise AuthError("Unparseable Bearer credentials") from exc


class BearerAuthMiddleware:
    """
    HTTP gate: require a parseable Bearer token on every request.

    Attaches BzmToken to ``request.state``; does not validate against BlazeMeter.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        if scope.get("method") == "OPTIONS":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        try:
            token = parse_authorization_header(request.headers.get("authorization"))
        except AuthError:
            response = JSONResponse(
                {"error": "Unauthorized"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return

        setattr(request.state, BZM_TOKEN_STATE_ATTR, token)
        await self.app(scope, receive, send)


def run_streamable_http(mcp: FastMCP) -> None:
    """Serve FastMCP over streamable HTTP with Bearer auth middleware."""
    import anyio
    import uvicorn

    async def _serve() -> None:
        app = BearerAuthMiddleware(mcp.streamable_http_app())
        config = uvicorn.Config(
            app,
            host=mcp.settings.host,
            port=mcp.settings.port,
            log_level=mcp.settings.log_level.lower(),
        )
        await uvicorn.Server(config).serve()

    anyio.run(_serve)
