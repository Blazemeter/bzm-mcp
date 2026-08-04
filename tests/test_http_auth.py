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
import base64
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from config.auth import (
    AuthError,
    BZM_TOKEN_STATE_ATTR,
    BearerAuthMiddleware,
    HttpAuthProvider,
    StdioAuthProvider,
    parse_authorization_header,
)
from config.runtime import build_runtime
from config.token import BzmToken, BzmTokenError


class TestBearerCredentialParsing:
    def test_plaintext_id_secret(self):
        token = BzmToken.from_bearer_credentials("key-id:key-secret")
        assert token.id == "key-id"
        assert token.secret == "key-secret"

    def test_base64_id_secret(self):
        raw = base64.b64encode(b"key-id:key-secret").decode()
        token = BzmToken.from_bearer_credentials(raw)
        assert token.id == "key-id"
        assert token.secret == "key-secret"

    def test_empty_raises(self):
        with pytest.raises(BzmTokenError):
            BzmToken.from_bearer_credentials("  ")

    def test_unparseable_raises(self):
        with pytest.raises(BzmTokenError):
            BzmToken.from_bearer_credentials(base64.b64encode(b"no-colon").decode())


class TestAuthorizationHeaderParsing:
    def test_bearer_plaintext(self):
        token = parse_authorization_header("Bearer key-id:key-secret")
        assert token.id == "key-id"
        assert token.secret == "key-secret"

    def test_bearer_base64(self):
        raw = base64.b64encode(b"key-id:key-secret").decode()
        token = parse_authorization_header(f"Bearer {raw}")
        assert token.id == "key-id"
        assert token.secret == "key-secret"

    def test_missing_header(self):
        with pytest.raises(AuthError):
            parse_authorization_header(None)

    def test_wrong_scheme(self):
        with pytest.raises(AuthError):
            parse_authorization_header("Basic abc")


class TestAuthProviders:
    def test_stdio_returns_startup_token(self):
        token = BzmToken("id", "secret")
        provider = StdioAuthProvider(token)
        assert provider.get_token(ctx=None) is token

    def test_stdio_allows_none(self):
        assert StdioAuthProvider(None).get_token(ctx=None) is None

    def test_http_reads_request_state(self):
        token_a = BzmToken("a-id", "a-secret")
        token_b = BzmToken("b-id", "b-secret")
        provider = HttpAuthProvider()

        def ctx_with(token: BzmToken):
            request = SimpleNamespace(state=SimpleNamespace(**{BZM_TOKEN_STATE_ATTR: token}))
            request_context = SimpleNamespace(request=request)
            return SimpleNamespace(request_context=request_context)

        assert provider.get_token(ctx_with(token_a)).id == "a-id"
        assert provider.get_token(ctx_with(token_b)).id == "b-id"

    def test_http_concurrent_tokens_are_isolated(self):
        """Two contexts with different Bearer-derived tokens resolve independently."""
        provider = HttpAuthProvider()
        token_a = BzmToken("account-a", "secret-a")
        token_b = BzmToken("account-b", "secret-b")

        def make_ctx(token: BzmToken):
            request = MagicMock()
            setattr(request.state, BZM_TOKEN_STATE_ATTR, token)
            ctx = MagicMock()
            ctx.request_context.request = request
            return ctx

        assert provider.get_token(make_ctx(token_a)).id == "account-a"
        assert provider.get_token(make_ctx(token_b)).id == "account-b"


class TestBearerAuthMiddleware:
    def _app(self):
        async def ok(request: Request):
            token = getattr(request.state, BZM_TOKEN_STATE_ATTR, None)
            return JSONResponse({"id": token.id if token else None})

        return BearerAuthMiddleware(Starlette(routes=[Route("/mcp", endpoint=ok, methods=["POST"])]))

    def test_missing_authorization_returns_401(self):
        client = TestClient(self._app())
        response = client.post("/mcp")
        assert response.status_code == 401
        assert response.json()["error"] == "Unauthorized"

    def test_invalid_bearer_returns_401(self):
        client = TestClient(self._app())
        response = client.post("/mcp", headers={"Authorization": "Bearer not-valid"})
        assert response.status_code == 401

    def test_valid_bearer_attaches_token(self):
        client = TestClient(self._app())
        response = client.post(
            "/mcp",
            headers={"Authorization": "Bearer key-id:key-secret"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == "key-id"

    def test_options_bypasses_auth(self):
        async def ok(_request: Request):
            return JSONResponse({"ok": True})

        app = BearerAuthMiddleware(Starlette(routes=[Route("/mcp", endpoint=ok, methods=["OPTIONS"])]))
        client = TestClient(app)
        assert client.options("/mcp").status_code == 200


class TestBuildRuntime:
    def test_build_runtime_stdio_and_http(self):
        stdio = build_runtime("stdio")
        assert stdio.transport == "stdio"
        assert isinstance(stdio.auth, StdioAuthProvider)

        http = build_runtime("streamable-http")
        assert http.transport == "streamable-http"
        assert isinstance(http.auth, HttpAuthProvider)
