from typing import Optional

from mcp.server.fastmcp import Context

from config.token import BzmToken


class Manager:
    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx
