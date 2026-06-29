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
import os
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from models.result import BaseResult
from telemetry import (
    DEFAULT_OTLP_ENDPOINT,
    DEFAULT_OTLP_PROTOCOL,
    _create_metric_exporter,
    _create_trace_exporter,
    _get_otlp_protocol,
    _record_metrics,
    init_telemetry,
    run_tool,
)


def _make_ctx(meta=None):
    ctx = MagicMock()
    ctx.request_context.request.params.meta = meta or {}
    ctx.request_context.session.client_params = None
    ctx.session_id = None
    return ctx


def _make_ctx_with_client(name="claude-code", version="1.2.3"):
    ctx = MagicMock()
    ctx.request_context.request.params.meta = {}
    ctx.request_context.session.client_params.clientInfo.name = name
    ctx.request_context.session.client_params.clientInfo.version = version
    ctx.session_id = "session-abc"
    return ctx


def _make_tracer_and_span():
    span = MagicMock()
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=span)
    cm.__exit__ = MagicMock(return_value=False)
    tracer = MagicMock()
    tracer.start_as_current_span.return_value = cm
    return tracer, span


class TestRecordMetrics:
    def test_omits_error_type_on_success(self):
        counter = MagicMock()
        histogram = MagicMock()
        with patch("telemetry._call_counter", counter), patch("telemetry._duration_histogram", histogram):
            _record_metrics("blazemeter_user", "read", 0.5, None)
        expected = {"gen_ai.tool.name": "blazemeter_user", "mcp.tool.action": "read"}
        counter.add.assert_called_once_with(1, expected)
        histogram.record.assert_called_once_with(0.5, expected)

    def test_includes_error_type_on_failure(self):
        counter = MagicMock()
        histogram = MagicMock()
        with patch("telemetry._call_counter", counter), patch("telemetry._duration_histogram", histogram):
            _record_metrics("blazemeter_user", "read", 0.5, "timeout")
        expected = {
            "gen_ai.tool.name": "blazemeter_user",
            "mcp.tool.action": "read",
            "error.type": "timeout",
        }
        counter.add.assert_called_once_with(1, expected)
        histogram.record.assert_called_once_with(0.5, expected)


class TestRunTool:
    def test_returns_dispatch_result(self):
        ctx = _make_ctx()
        tracer, _ = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            result = BaseResult(result=[{"id": 1}])
            returned = asyncio.run(run_tool("blazemeter_user", "read", ctx, AsyncMock(return_value=result)))
            assert returned is result

    def test_sets_span_attributes(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            asyncio.run(run_tool("blazemeter_user", "read", ctx, AsyncMock(return_value=BaseResult())))
            span.set_attribute.assert_any_call("gen_ai.tool.name", "blazemeter_user")
            span.set_attribute.assert_any_call("mcp.tool.action", "read")
            span.set_attribute.assert_any_call("mcp.method.name", "tools/call")
            span.set_attribute.assert_any_call("gen_ai.operation.name", "execute_tool")

    def test_sets_client_info_attributes(self):
        ctx = _make_ctx_with_client("claude-code", "1.2.3")
        tracer, span = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            asyncio.run(run_tool("blazemeter_user", "read", ctx, AsyncMock(return_value=BaseResult())))
            span.set_attribute.assert_any_call("user_agent.name", "claude-code")
            span.set_attribute.assert_any_call("user_agent.version", "1.2.3")
            span.set_attribute.assert_any_call("mcp.session.id", "session-abc")

    def test_span_kind_server(self):
        ctx = _make_ctx()
        tracer, _ = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            asyncio.run(run_tool("blazemeter_user", "read", ctx, AsyncMock(return_value=BaseResult())))
            _, kwargs = tracer.start_as_current_span.call_args
            assert kwargs.get("kind") == t.SpanKind.SERVER

    def test_reraises_httpx_401(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        response = MagicMock()
        response.status_code = 401
        err = httpx.HTTPStatusError("unauthorized", request=MagicMock(), response=response)
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            with pytest.raises(httpx.HTTPStatusError):
                asyncio.run(run_tool("t", "a", ctx, AsyncMock(side_effect=err)))
            span.set_attribute.assert_any_call("error.type", "auth_failed")

    def test_reraises_httpx_404(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        response = MagicMock()
        response.status_code = 404
        err = httpx.HTTPStatusError("not found", request=MagicMock(), response=response)
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            with pytest.raises(httpx.HTTPStatusError):
                asyncio.run(run_tool("t", "a", ctx, AsyncMock(side_effect=err)))
            span.set_attribute.assert_any_call("error.type", "not_found")

    def test_reraises_httpx_500(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        response = MagicMock()
        response.status_code = 500
        err = httpx.HTTPStatusError("server error", request=MagicMock(), response=response)
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            with pytest.raises(httpx.HTTPStatusError):
                asyncio.run(run_tool("t", "a", ctx, AsyncMock(side_effect=err)))
            span.set_attribute.assert_any_call("error.type", "server_error")

    def test_reraises_httpx_timeout(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        err = httpx.TimeoutException("timed out")
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            with pytest.raises(httpx.TimeoutException):
                asyncio.run(run_tool("t", "a", ctx, AsyncMock(side_effect=err)))
            span.set_attribute.assert_any_call("error.type", "timeout")

    def test_reraises_generic_exception(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            with pytest.raises(ValueError):
                asyncio.run(run_tool("t", "a", ctx, AsyncMock(side_effect=ValueError("boom"))))
            span.set_attribute.assert_any_call("error.type", "tool_error")

    def test_marks_span_failed_on_result_error(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            result = BaseResult(error="api returned error")
            returned = asyncio.run(run_tool("t", "a", ctx, AsyncMock(return_value=result)))
            assert returned is result
            span.set_attribute.assert_any_call("error.type", "api_error")

    def test_survives_span_setup_failure(self):
        ctx = _make_ctx()
        with patch("telemetry.trace") as t:
            t.get_tracer.side_effect = RuntimeError("otel broken")
            result = BaseResult(result=[{"id": 1}])
            returned = asyncio.run(run_tool("t", "a", ctx, AsyncMock(return_value=result)))
            assert returned is result

    def test_survives_broken_ctx(self):
        ctx = _make_ctx(meta=None)
        tracer, _ = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            result = BaseResult(result=[])
            returned = asyncio.run(run_tool("t", "a", ctx, AsyncMock(return_value=result)))
            assert returned is result

    def test_omits_client_info_when_absent(self):
        ctx = _make_ctx()
        tracer, span = _make_tracer_and_span()
        with patch("telemetry.trace") as t:
            t.get_tracer.return_value = tracer
            asyncio.run(run_tool("blazemeter_user", "read", ctx, AsyncMock(return_value=BaseResult())))
            attribute_names = [c[0][0] for c in span.set_attribute.call_args_list]
            assert "user_agent.name" not in attribute_names
            assert "user_agent.version" not in attribute_names


class TestInitTelemetry:
    def test_does_not_raise_without_sdk(self):
        init_telemetry("bzm-mcp", "1.0.0")

    def test_does_not_raise_with_disabled_flag(self, monkeypatch):
        monkeypatch.setenv("OTEL_SDK_DISABLED", "true")
        init_telemetry("bzm-mcp", "1.0.0")

    def test_does_not_raise_with_endpoint_set(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
        init_telemetry("bzm-mcp", "1.0.0")

    def test_defaults_endpoint_to_perforce_grpc(self, monkeypatch):
        monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
        monkeypatch.delenv("OTEL_SDK_DISABLED", raising=False)
        init_telemetry("bzm-mcp", "1.0.0")
        assert os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] == DEFAULT_OTLP_ENDPOINT
        assert DEFAULT_OTLP_ENDPOINT == "https://grpc.public.prd.shared.perforce.com"

    def test_explicit_endpoint_not_overridden(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
        monkeypatch.delenv("OTEL_SDK_DISABLED", raising=False)
        init_telemetry("bzm-mcp", "1.0.0")
        assert os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] == "http://localhost:4317"

    def test_defaults_protocol_to_grpc(self, monkeypatch):
        monkeypatch.delenv("OTEL_EXPORTER_OTLP_PROTOCOL", raising=False)
        assert _get_otlp_protocol() == DEFAULT_OTLP_PROTOCOL
        assert DEFAULT_OTLP_PROTOCOL == "grpc"

    def test_http_protocol_env(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
        assert _get_otlp_protocol() == "http/protobuf"

    def test_does_not_raise_with_http_protocol(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
        init_telemetry("bzm-mcp", "1.0.0")

    def test_grpc_trace_exporter_selected(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
        with patch(
            "opentelemetry.exporter.otlp.proto.grpc.trace_exporter.OTLPSpanExporter",
            return_value=MagicMock(),
        ) as grpc_exporter:
            _create_trace_exporter()
        grpc_exporter.assert_called_once()

    def test_http_trace_exporter_selected(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
        with patch(
            "opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter",
            return_value=MagicMock(),
        ) as http_exporter:
            _create_trace_exporter()
        http_exporter.assert_called_once()

    def test_grpc_metric_exporter_selected(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
        with patch(
            "opentelemetry.exporter.otlp.proto.grpc.metric_exporter.OTLPMetricExporter",
            return_value=MagicMock(),
        ) as grpc_exporter:
            _create_metric_exporter()
        grpc_exporter.assert_called_once()

    def test_http_metric_exporter_selected(self, monkeypatch):
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_PROTOCOL", "http/json")
        with patch(
            "opentelemetry.exporter.otlp.proto.http.metric_exporter.OTLPMetricExporter",
            return_value=MagicMock(),
        ) as http_exporter:
            _create_metric_exporter()
        http_exporter.assert_called_once()
