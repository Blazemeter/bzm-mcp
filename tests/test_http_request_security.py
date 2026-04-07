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

import httpx

from config.security import validate_http_request_endpoint
from tools.utils import http_request


class FakeHttpResponse:
    def __init__(self, text: str = "ok"):
        self.text = text
        self.headers = {"content-type": "text/plain"}

    def raise_for_status(self):
        return None


class TestHttpEndpointAllowlistValidation:
    def test_allows_blazemeter_help_domain(self):
        assert validate_http_request_endpoint("https://help.blazemeter.com/docs/index.html") is None

    def test_rejects_http_even_for_allowlisted_domain(self):
        error = validate_http_request_endpoint("http://help.blazemeter.com/docs/index.html")
        assert error is not None
        assert "Only https URLs are allowed" in error

    def test_rejects_non_allowlisted_domain(self):
        error = validate_http_request_endpoint("https://evil.example.com/steal")
        assert error is not None
        assert "not allowed" in error

    def test_rejects_aws_metadata_endpoint(self):
        error = validate_http_request_endpoint("http://169.254.169.254/latest/meta-data")
        assert error is not None
        assert "Only https URLs are allowed" in error

    def test_rejects_non_absolute_endpoint(self):
        error = validate_http_request_endpoint("/docs/index.html")
        assert error is not None
        assert "Invalid endpoint scheme" in error

    def test_allows_uppercase_allowlisted_hostname(self):
        error = validate_http_request_endpoint("https://HELP.BLAZEMETER.COM/docs/index.html")
        assert error is None

    def test_rejects_hostname_with_trailing_dot(self):
        error = validate_http_request_endpoint("https://help.blazemeter.com./docs/index.html")
        assert error is not None
        assert "not allowed" in error

    def test_rejects_userinfo_host_confusion(self):
        error = validate_http_request_endpoint("https://help.blazemeter.com@evil.example.com/docs")
        assert error is not None
        assert "not allowed" in error

    def test_rejects_lookalike_subdomain_suffix(self):
        error = validate_http_request_endpoint("https://help.blazemeter.com.evil.example.com/docs")
        assert error is not None
        assert "not allowed" in error

    def test_rejects_ip_literal_even_with_https(self):
        error = validate_http_request_endpoint("https://169.254.169.254/latest/meta-data")
        assert error is not None
        assert "not allowed" in error

    def test_allows_explicit_allowlisted_port(self):
        error = validate_http_request_endpoint("https://help.blazemeter.com:443/docs/index.html")
        assert error is None


class TestHttpRequestSsrfProtection:
    def test_http_request_blocks_disallowed_host_without_network_call(self, monkeypatch):
        called = {"value": False}

        async def fake_request(self, method, endpoint, headers=None, **kwargs):  # pragma: no cover
            called["value"] = True
            return FakeHttpResponse()

        monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)

        result = asyncio.run(http_request("GET", "https://internal.example.local/secret"))

        assert result.error is not None
        assert "not allowed" in result.error
        assert called["value"] is False

    def test_http_request_allows_allowlisted_host(self, monkeypatch):
        async def fake_request(self, method, endpoint, headers=None, **kwargs):
            assert endpoint == "https://help.blazemeter.com/docs"
            return FakeHttpResponse(text="help-content")

        monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)

        result = asyncio.run(http_request("GET", "https://help.blazemeter.com/docs"))

        assert result.error is None
        assert result.result == "help-content"
