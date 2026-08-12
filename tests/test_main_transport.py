import pytest

import main
from config.auth import HttpAuthProvider, StdioAuthProvider
from config.runtime import AppRuntime
from config.storage import HttpStorageClient, LocalStorageClient


class _DummyFastMCP:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.run_calls = []

    def run(self, transport="stdio", mount_path=None):
        self.run_calls.append({"transport": transport, "mount_path": mount_path})


def _patch_mcp_server_dependencies(monkeypatch):
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


class TestToWireTransport:
    def test_maps_logical_transports(self):
        assert main.to_wire_transport("http") == "streamable-http"
        assert main.to_wire_transport("stdio") == "stdio"
        assert main.to_wire_transport("docker") == "stdio"


class TestBuildMcpServerHttp:
    def test_http_uses_env_settings_and_stateful_http(self, monkeypatch):
        _patch_mcp_server_dependencies(monkeypatch)
        monkeypatch.setenv("FASTMCP_HOST", "0.0.0.0")
        monkeypatch.setenv("FASTMCP_PORT", "8012")
        monkeypatch.setenv("FASTMCP_STREAMABLE_HTTP_PATH", "/custom-mcp")

        mcp, runtime_transport = main.build_mcp_server(transport="http")

        assert runtime_transport == "streamable-http"
        assert isinstance(mcp, _DummyFastMCP)
        assert mcp.kwargs["host"] == "0.0.0.0"
        assert mcp.kwargs["port"] == 8012
        assert mcp.kwargs["streamable_http_path"] == "/custom-mcp"
        assert mcp.kwargs["stateless_http"] is False

    def test_http_falls_back_to_cloud_run_port(self, monkeypatch):
        _patch_mcp_server_dependencies(monkeypatch)
        monkeypatch.delenv("FASTMCP_PORT", raising=False)
        monkeypatch.setenv("PORT", "8080")
        monkeypatch.setenv("FASTMCP_HOST", "0.0.0.0")

        mcp, _ = main.build_mcp_server(transport="http")

        assert mcp.kwargs["port"] == 8080


class TestBuildMcpServerTransportMapping:
    def test_transport_mapping_keeps_docker_stdio_and_http_streamable(self, monkeypatch):
        _patch_mcp_server_dependencies(monkeypatch)

        _mcp_http, runtime_transport_http = main.build_mcp_server(transport="http")
        _mcp_docker, runtime_transport_docker = main.build_mcp_server(transport="docker")
        _mcp_stdio, runtime_transport_stdio = main.build_mcp_server(transport="stdio")

        assert runtime_transport_http == "streamable-http"
        assert runtime_transport_docker == "stdio"
        assert runtime_transport_stdio == "stdio"


class TestBuildMcpServerAuthWiring:
    def test_http_registers_http_auth_provider(self, monkeypatch):
        captured = {}

        def capture_register(mcp, runtime):
            captured["runtime"] = runtime

        _patch_mcp_server_dependencies(monkeypatch)
        monkeypatch.setattr(main, "register_tools", capture_register)

        main.build_mcp_server(transport="http")

        runtime = captured["runtime"]
        assert isinstance(runtime, AppRuntime)
        assert runtime.transport == "streamable-http"
        assert isinstance(runtime.auth, HttpAuthProvider)
        assert isinstance(runtime.storage, HttpStorageClient)

    def test_stdio_and_docker_register_stdio_auth_provider(self, monkeypatch):
        captured = {}

        def capture_register(mcp, runtime):
            captured.setdefault("runtimes", []).append(runtime)

        token = object()
        _patch_mcp_server_dependencies(monkeypatch)
        monkeypatch.setattr(main, "get_token", lambda: token)
        monkeypatch.setattr(main, "register_tools", capture_register)
        monkeypatch.delenv("MCP_DOCKER", raising=False)
        monkeypatch.delenv("BZM_STORAGE_BACKEND", raising=False)

        main.build_mcp_server(transport="stdio")
        main.build_mcp_server(transport="docker")

        assert len(captured["runtimes"]) == 2
        for runtime in captured["runtimes"]:
            assert isinstance(runtime.auth, StdioAuthProvider)
            assert runtime.auth.get_token(ctx=None) is token
            assert isinstance(runtime.storage, LocalStorageClient)


class TestRunTransportDispatch:
    def test_http_uses_bearer_middleware_server(self, monkeypatch):
        calls = {"stdio": 0, "http": 0}

        class _Mcp:
            def run(self, transport="stdio", mount_path=None):
                calls["stdio"] += 1

        _patch_mcp_server_dependencies(monkeypatch)
        monkeypatch.setattr(main, "build_mcp_server", lambda **k: (_Mcp(), "streamable-http"))
        monkeypatch.setattr(
            main,
            "run_streamable_http",
            lambda mcp: calls.__setitem__("http", calls["http"] + 1),
        )

        main.run(transport="http")

        assert calls["http"] == 1
        assert calls["stdio"] == 0

    def test_stdio_uses_mcp_run(self, monkeypatch):
        calls = {"stdio": 0, "http": 0}

        class _Mcp:
            def run(self, transport="stdio", mount_path=None):
                calls["stdio"] += 1
                assert transport == "stdio"

        _patch_mcp_server_dependencies(monkeypatch)
        monkeypatch.setattr(main, "build_mcp_server", lambda **k: (_Mcp(), "stdio"))
        monkeypatch.setattr(
            main,
            "run_streamable_http",
            lambda mcp: calls.__setitem__("http", calls["http"] + 1),
        )

        main.run(transport="stdio")

        assert calls["stdio"] == 1
        assert calls["http"] == 0
