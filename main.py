import os
import sys
import logging
from server import register_tools
from mcp.server.fastmcp import FastMCP
from config.token import BzmToken, BzmTokenError

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')
logging.basicConfig(level=logging.ERROR)

def run():
    try:
        token = BzmToken.from_file(BLAZEMETER_API_KEY_FILE_PATH)
    except BzmTokenError as e:
        logging.error(f"Error loading BlazeMeter token: {e}")
        raise SystemExit(1)

    mcp = FastMCP("bzm-mcp")
    register_tools(mcp, token)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run()
