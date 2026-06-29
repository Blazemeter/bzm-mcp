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
import logging
import os
import time
from typing import Any, Awaitable, Callable

import httpx

logger = logging.getLogger(__name__)

try:
    from opentelemetry import metrics, trace  # noqa: F401 — must be module-level for patching
    _OTEL_API_AVAILABLE = True
except ImportError:
    trace = None  # type: ignore[assignment]
    metrics = None  # type: ignore[assignment]
    _OTEL_API_AVAILABLE = False

_call_counter = None
_duration_histogram = None

DEFAULT_OTLP_ENDPOINT = "https://grpc.public.prd.shared.perforce.com"
DEFAULT_OTLP_PROTOCOL = "grpc"


def _get_otlp_protocol() -> str:
    return os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL", DEFAULT_OTLP_PROTOCOL)


def _create_trace_exporter():
    if _get_otlp_protocol() == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    else:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    return OTLPSpanExporter()


def _create_metric_exporter():
    if _get_otlp_protocol() == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    else:
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    return OTLPMetricExporter()


def init_telemetry(service_name: str, service_version: str) -> None:
    global _call_counter, _duration_histogram

    if not _OTEL_API_AVAILABLE:
        return
    if os.getenv("OTEL_SDK_DISABLED", "").lower() == "true":
        return
    try:
        # Lazy SDK imports: defer heavy setup until init_telemetry() and tolerate a
        # missing SDK (ImportError) without breaking module import or startup.
        from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        resource = Resource.create({
            SERVICE_NAME: service_name,
            SERVICE_VERSION: service_version,
        })
        provider = TracerProvider(resource=resource)

        # Default export destination/protocol for shipped releases (gRPC + Perforce
        # collector). PAG or local dev may override via OTEL_EXPORTER_OTLP_ENDPOINT
        # and OTEL_EXPORTER_OTLP_PROTOCOL; OTEL_SDK_DISABLED=true disables telemetry.
        if not os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = DEFAULT_OTLP_ENDPOINT

        try:
            provider.add_span_processor(BatchSpanProcessor(_create_trace_exporter()))
        except Exception:
            logger.debug("OTLP trace exporter setup failed", exc_info=True)

        trace.set_tracer_provider(provider)
        logger.debug("OTel TracerProvider initialised (service=%s, version=%s)", service_name, service_version)

        try:
            from opentelemetry.sdk.metrics import MeterProvider
            from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

            readers = []
            try:
                readers.append(PeriodicExportingMetricReader(_create_metric_exporter()))
            except Exception:
                logger.debug("OTLP metric exporter setup failed", exc_info=True)

            meter_provider = MeterProvider(resource=resource, metric_readers=readers)
            metrics.set_meter_provider(meter_provider)

            meter = metrics.get_meter("bzm-mcp")
            _call_counter = meter.create_counter(
                "mcp.tool.calls",
                unit="{call}",
                description="Number of MCP tool calls",
            )
            _duration_histogram = meter.create_histogram(
                "mcp.tool.duration",
                unit="s",
                description="MCP tool call duration in seconds",
            )
            logger.debug("OTel MeterProvider initialised")
        except ImportError:
            pass
        except Exception:
            logger.debug("OTel metrics init failed", exc_info=True)

    except ImportError:
        pass
    except Exception:
        logger.debug("OTel init failed; continuing without tracing", exc_info=True)


def _get_meta(ctx: Any) -> dict:
    try:
        return ctx.request_context.request.params.meta or {}
    except Exception:
        return {}


def _extract_trace_context(meta: dict):
    if not meta:
        return None
    try:
        from opentelemetry.propagate import extract
        carrier = {}
        if "traceparent" in meta:
            carrier["traceparent"] = meta["traceparent"]
        if "tracestate" in meta:
            carrier["tracestate"] = meta["tracestate"]
        return extract(carrier) if carrier else None
    except Exception:
        return None


def _get_client_info(ctx: Any):
    try:
        info = ctx.request_context.session.client_params.clientInfo
        return info.name, info.version
    except Exception:
        return None, None


def _get_session_id(ctx: Any) -> str | None:
    try:
        session_id = ctx.session_id
        return str(session_id) if session_id is not None else None
    except Exception:
        return None


def _record_span_error(span: Any, error_type: str) -> None:
    try:
        span.set_attribute("error.type", error_type)
    except Exception:
        pass
    try:
        from opentelemetry.trace import Status, StatusCode
        span.set_status(Status(StatusCode.ERROR))
    except Exception:
        pass


def _http_status_to_error_type(status_code: int) -> str:
    if status_code in (401, 403):
        return "auth_failed"
    if status_code == 404:
        return "not_found"
    if status_code == 429:
        return "rate_limited"
    if status_code >= 500:
        return "server_error"
    return f"http_{status_code}"


def _record_metrics(tool_name: str, action: str, elapsed: float, error_type: str | None) -> None:
    attrs: dict[str, str] = {"gen_ai.tool.name": tool_name, "mcp.tool.action": action}
    if error_type is not None:
        attrs["error.type"] = error_type
    try:
        if _call_counter is not None:
            _call_counter.add(1, attrs)
        if _duration_histogram is not None:
            _duration_histogram.record(elapsed, attrs)
    except Exception:
        pass


async def run_tool(
    tool_name: str,
    action: str,
    ctx: Any,
    dispatch: Callable[[], Awaitable[Any]],
) -> Any:
    if trace is None:
        return await dispatch()

    try:
        meta = _get_meta(ctx)
        parent_ctx = _extract_trace_context(meta)
        tracer = trace.get_tracer("bzm-mcp")
        span_cm = tracer.start_as_current_span(
            f"tools/call {tool_name}",
            context=parent_ctx,
            kind=trace.SpanKind.SERVER,
            record_exception=False,
            set_status_on_exception=False,
        )
    except Exception:
        return await dispatch()

    with span_cm as span:
        try:
            span.set_attribute("mcp.method.name", "tools/call")
            span.set_attribute("gen_ai.tool.name", tool_name)
            span.set_attribute("gen_ai.operation.name", "execute_tool")
            span.set_attribute("mcp.tool.action", action)
            client_name, client_version = _get_client_info(ctx)
            if client_name is not None:
                span.set_attribute("user_agent.name", client_name)
            if client_version is not None:
                span.set_attribute("user_agent.version", client_version)
            session_id = _get_session_id(ctx)
            if session_id is not None:
                span.set_attribute("mcp.session.id", session_id)
        except Exception:
            pass

        start = time.perf_counter()
        error_type: str | None = None
        result = None
        try:
            result = await dispatch()
        except httpx.TimeoutException:
            error_type = "timeout"
            _record_span_error(span, error_type)
            raise
        except httpx.HTTPStatusError as e:
            error_type = _http_status_to_error_type(e.response.status_code)
            _record_span_error(span, error_type)
            raise
        except Exception:
            error_type = "tool_error"
            _record_span_error(span, error_type)
            raise
        finally:
            elapsed = time.perf_counter() - start
            metric_error_type = error_type or (
                "api_error" if result is not None and getattr(result, "error", None) else None
            )
            _record_metrics(tool_name, action, elapsed, metric_error_type)

        if result is not None and getattr(result, "error", None):
            _record_span_error(span, "api_error")
        return result
