"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import traceback
from typing import Optional, Dict, Any
import httpx
from mcp.server.fastmcp import Context

from config.blazemeter import ACCOUNTS_ENDPOINT, TOOLS_PREFIX, SUPPORT_MESSAGE
from config.token import BzmToken
from formatters.account import format_accounts
from models.manager import Manager
from models.result import BaseResult
from tools.utils import api_request


class AccountManager(Manager):

    # Note: It's allowed to list all the user account without AI consent
    # the format_accounts only expose minimum information to user
    # The read operation verify permissions and don't allow to share if don't have permissions.

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    async def read(self, account_id: int) -> BaseResult:
        account_result = await api_request(
            self.token,
            "GET",
            f"{ACCOUNTS_ENDPOINT}/{account_id}",
            result_formatter=format_accounts
        )
        if account_result.error:
            return account_result
        else:
            ai_consent = account_result.result[0].ai_consent
            if ai_consent is not True:
                return BaseResult(
                    error=f"The Account ID {account_id} does not have AI consent. Contact your account manager for more information."
                )
            else:
                return account_result

    async def list(self, limit: int = 50, offset: int = 0) -> BaseResult:

        # Note: Not it's needed to control AI consent at this level

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
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}\n{SUPPORT_MESSAGE}"
            )
