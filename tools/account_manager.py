import traceback
from typing import Optional, Dict, Any

from mcp.server.fastmcp import Context

from config.blazemeter import ACCOUNTS_ENDPOINT, TOOLS_PREFIX
from config.token import BzmToken
from formatters.account import format_accounts
from models.result import BaseResult
from tools.utils import api_request


class AccountManager:
    def __init__(self, token: Optional[BzmToken], ctx: Context):
        self.token = token
        self.ctx = ctx

    async def read(self, account_id: int) -> BaseResult:
        return await api_request(
            self.token,
            "GET",
            f"{ACCOUNTS_ENDPOINT}/{account_id}",
            result_formatter=format_accounts
        )

    async def list(self, limit: int = 50, offset: int = 0) -> BaseResult:
        parameters = {
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        return await api_request(
            self.token,
            "GET",
            f"{ACCOUNTS_ENDPOINT}",
            result_formatter=format_accounts,
            params=parameters
        )


def register(mcp, token: Optional[BzmToken]) -> None:
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_account",
        description="""
        Operations on account users. 
        Use this when a user needs to select a account.
        Actions:
        - read: Read a Account. Get the information of a account.
            args(dict): Dictionary with the following required parameters:
                account_id (int): The id of the account to get information.
        - list: List all accounts. 
            args(dict): Dictionary with the following required parameters:
                limit (int, default=10, valid=[1 to 50]): The number of tests to list.
                offset (int, default=0): Number of tests to skip.
        Hints:
        - If you need to get the default account, use the project id to get the workspace and with that the account.
        - Use the read operation if AI consent information is needed. The AI Consent it's located at account level.
    """
    )
    async def account(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        account_manager = AccountManager(token, ctx)
        try:
            match action:
                case "read":
                    return await account_manager.read(args["account_id"])
                case "list":
                    return await account_manager.list(args.get("limit", 50), args.get("offset", 0))
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in account manager tool"
                    )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
