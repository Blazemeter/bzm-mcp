import os
from server import register_tools
from mcp.server.fastmcp import FastMCP
from config.token import BzmToken, BzmTokenError

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')

def run():
    token = None
    try:
        token = BzmToken.from_file(BLAZEMETER_API_KEY_FILE_PATH)
    except BzmTokenError as e:
        pass

    mcp = FastMCP("bzm-mcp")
    register_tools(mcp, token)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run()
