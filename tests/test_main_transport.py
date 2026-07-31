import pytest

import main


class _DummyFastMCP:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.run_calls = []

    def run(self, transport="stdio", mount_path=None):
        self.run_calls.append({"transport": transport, "mount_path": mount_path})


def _patch_runtime_dependencies(monkeypatch):
    monkeypatch.setattr(main, "init_telemetry", lambda *a, **k: None)
    monkeypatch.setattr(main, "get_token", lambda: object())
    monkeypatch.setattr(main, "register_confirm_mode", lambda *a, **k: None)
    monkeypatch.setattr(main, "register_tools", lambda *a, **k: None)
    monkeypatch.setattr(main, "FastMCP", _DummyFastMCP)


class TestResolveMcpTransport:
    def test_precedence_cli_then_env_then_default(self, monkeypatch):
        monkeypatch.delenv("BZM_MCP_TRANSPORT", raising=False)
        assert main.resolve_mcp_transport("") == "stdio"

        monkeypatch.setenv("BZM_MCP_TRANSPORT", "http")
        assert main.resolve_mcp_transport("") == "http"

        # CLI value must override environment fallback.
        assert main.resolve_mcp_transport("docker") == "docker"

    def test_invalid_transport_raises_clear_error(self, monkeypatch):
        monkeypatch.delenv("BZM_MCP_TRANSPORT", raising=False)

        with pytest.raises(ValueError, match="Invalid MCP transport"):
            main.resolve_mcp_transport("banana")


class TestBuildRuntimeHttp:
    def test_http_runtime_uses_env_settings_and_stateful_http(self, monkeypatch):
        _patch_runtime_dependencies(monkeypatch)
        monkeypatch.setenv("FASTMCP_HOST", "0.0.0.0")
        monkeypatch.setenv("FASTMCP_PORT", "8012")
        monkeypatch.setenv("FASTMCP_STREAMABLE_HTTP_PATH", "/custom-mcp")

        mcp, runtime_transport = main.build_runtime(transport="http")

        assert runtime_transport == "streamable-http"
        assert isinstance(mcp, _DummyFastMCP)
        assert mcp.kwargs["host"] == "0.0.0.0"
        assert mcp.kwargs["port"] == 8012
        assert mcp.kwargs["streamable_http_path"] == "/custom-mcp"
        assert mcp.kwargs["stateless_http"] is False


class TestBuildRuntimeTransportMapping:
    def test_transport_mapping_keeps_docker_stdio_and_http_streamable(self, monkeypatch):
        _patch_runtime_dependencies(monkeypatch)

        _mcp_http, runtime_transport_http = main.build_runtime(transport="http")
        _mcp_docker, runtime_transport_docker = main.build_runtime(transport="docker")
        _mcp_stdio, runtime_transport_stdio = main.build_runtime(transport="stdio")

        assert runtime_transport_http == "streamable-http"
        assert runtime_transport_docker == "stdio"
        assert runtime_transport_stdio == "stdio"
