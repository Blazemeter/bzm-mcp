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
from mcp.server.fastmcp import Context

from config.token import BzmToken
from models.result import BaseResult


# NOTE: Imports are performed locally in each method to avoid cyclical import problems.
# This file acts as a bridge between different managers to access specific methods.

async def count_project_tests(token: BzmToken, ctx: Context, project_id: int) -> int:
    from tools.test_manager import TestManager
    return (
        await TestManager(token, ctx).list(project_id=project_id, limit=1, offset=0)).total


async def read_account(token: BzmToken, ctx: Context, account_id: int) -> BaseResult:
    from tools.account_manager import AccountManager
    return await AccountManager(token, ctx).read(account_id)


async def read_execution(token: BzmToken, ctx: Context, execution_id: int) -> BaseResult:
    from tools.execution_manager import ExecutionManager
    return await ExecutionManager(token, ctx).read(execution_id)
