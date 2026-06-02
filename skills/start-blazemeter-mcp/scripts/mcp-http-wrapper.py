#!/usr/bin/env python3
"""
HTTP/SSE wrapper for BlazeMeter MCP binary.
Starts the MCP binary as a subprocess and exposes it via HTTP/SSE on configured port.
"""

import os
import sys
import subprocess
import threading
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Configuration
WORKSPACE_ROOT = "/Users/wguerrero/blazemeterMCP"
MCP_BIN = f"{WORKSPACE_ROOT}/bzm-mcp-arm64.app/Contents/MacOS/bzm-mcp"
API_KEYS_FILE = f"{WORKSPACE_ROOT}/api-key.json"
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8000

# Setup logging
LOG_DIR = f"{WORKSPACE_ROOT}/.github/skills/start-blazemeter-mcp/logs"
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
LOG_FILE = f"{LOG_DIR}/mcp-http-wrapper.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global MCP process
mcp_process = None


def start_mcp_process():
    """Start the MCP binary as a subprocess."""
    global mcp_process
    
    env = os.environ.copy()
    env['API_KEYS_FILE'] = API_KEYS_FILE
    
    logger.info(f"Starting MCP binary: {MCP_BIN}")
    try:
        mcp_process = subprocess.Popen(
            [MCP_BIN, "--mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
        logger.info(f"MCP process started with PID {mcp_process.pid}")
        return True
    except Exception as e:
        logger.error(f"Failed to start MCP: {e}")
        return False


class MCPHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler for MCP requests."""
    
    def do_GET(self):
        """Handle GET requests."""
        logger.info(f"GET {self.path}")
        
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "healthy",
                "port": HTTP_PORT,
                "mcp_pid": mcp_process.pid if mcp_process else None
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/sse":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            
            # Stream from MCP process
            if mcp_process and mcp_process.stdout:
                try:
                    while True:
                        line = mcp_process.stdout.readline()
                        if line:
                            self.wfile.write(f"data: {line}".encode())
                            self.wfile.flush()
                        else:
                            break
                except Exception as e:
                    logger.error(f"SSE streaming error: {e}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging."""
        logger.debug(format % args)


def run_http_server():
    """Run the HTTP server."""
    server = HTTPServer((HTTP_HOST, HTTP_PORT), MCPHTTPHandler)
    logger.info(f"HTTP server listening on {HTTP_HOST}:{HTTP_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("HTTP server stopped")
        if mcp_process:
            mcp_process.terminate()
            mcp_process.wait()


def main():
    """Main entry point."""
    # Validate prerequisites
    if not os.path.isfile(MCP_BIN):
        logger.error(f"MCP binary not found: {MCP_BIN}")
        sys.exit(1)
    
    if not os.path.isfile(API_KEYS_FILE):
        logger.error(f"API key file not found: {API_KEYS_FILE}")
        sys.exit(1)
    
    if not os.access(MCP_BIN, os.X_OK):
        logger.error(f"MCP binary is not executable: {MCP_BIN}")
        sys.exit(1)
    
    logger.info(f"BlazeMeter MCP HTTP Wrapper starting")
    logger.info(f"Workspace: {WORKSPACE_ROOT}")
    logger.info(f"HTTP: {HTTP_HOST}:{HTTP_PORT}")
    
    # Start MCP process
    if not start_mcp_process():
        sys.exit(1)
    
    # Start HTTP server
    try:
        run_http_server()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        if mcp_process:
            mcp_process.terminate()


if __name__ == "__main__":
    main()
