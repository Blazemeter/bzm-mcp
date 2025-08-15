import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("bzm-mcp")

BLAZEMETER_API_KEY_FILE_PATH = os.getenv('BLAZEMETER_API_KEY')
