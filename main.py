import os
from server import register_tools
from mcp.server.fastmcp import FastMCP
from config.token import BzmToken, BzmTokenError

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')

def run():
    token = None
    
    if BLAZEMETER_API_KEY_FILE_PATH:
        try:
            token = BzmToken.from_file(BLAZEMETER_API_KEY_FILE_PATH)
        except BzmTokenError as e:
            # Token file exists but is invalid - this will be handled by individual tools
            pass
        except Exception as e:
            # Other errors (file not found, permissions, etc.) - also handled by tools
            pass
    
    mcp = FastMCP("bzm-mcp")
    register_tools(mcp, token)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run()
