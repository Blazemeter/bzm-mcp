import traceback
from typing import Optional, Dict, Any

from mcp.server.fastmcp import Context

from config.token import BzmToken
from models.result import BaseResult
from .base import api_request, TOOLS_PREFIX, get_date_time_iso

ACCOUNTS_ENDPOINT = "/accounts"


class AccountManager:
    def __init__(self, token: Optional[BzmToken]):
        self.token = token

    async def read(self, account_id: int) -> BaseResult:
        account_response = await api_request(self.token, "GET", f"{ACCOUNTS_ENDPOINT}/{account_id}")

        if "error" in account_response and account_response["error"]:
            return BaseResult(
                error=account_response.get("error")
            )

        accounts = [account_response.get("result", None)]
        return BaseResult(
            result=self.normalize_accounts(accounts),
            has_more=False
        )

    async def list(self, limit: int = 50, offset: int = 0) -> BaseResult:
        parameters = {
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        accounts_response = await api_request(self.token, "GET", f"{ACCOUNTS_ENDPOINT}", params=parameters)

        if "error" in accounts_response and accounts_response["error"]:
            return BaseResult(
                error=accounts_response.get("error")
            )

        accounts = accounts_response.get("result", [])
        has_more = accounts_response.get("total", 0) - (offset + limit) > 0

        return BaseResult(
            result=self.normalize_accounts(accounts),
            has_more=has_more
        )

    @staticmethod
    def normalize_accounts(accounts):
        formatted_accounts = []
        for account in accounts:
            formatted_account = {
                "account_id": account.get("id"),
                "account_name": account.get("name", "Unknown"),
                "description": account.get("description", ""),
                "created": get_date_time_iso(account.get("created")),
                "updated": get_date_time_iso(account.get("updated")),
            }
            formatted_accounts.append(formatted_account)
        return formatted_accounts

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
                    limit (int, default=50): The number of tests to list.
                    offset (int, default=0): Number of tests to skip.
        """
    )
    async def account(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        account_manager = AccountManager(token)
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
