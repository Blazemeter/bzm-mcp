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
# This file currently acts as a bridge between different managers to access specific methods,
# primarily for validation of reference elements.

async def read_account(token: BzmToken, ctx: Context, account_id: int) -> BaseResult:
    from tools.account_manager import AccountManager
    return await AccountManager(token, ctx).read(account_id)


async def read_project(token: BzmToken, ctx: Context, project_id: int) -> BaseResult:
    from tools.project_manager import ProjectManager
    return await ProjectManager(token, ctx).read(project_id)


async def read_workspace(token: BzmToken, ctx: Context, workspace_id: int) -> BaseResult:
    from tools.workspace_manager import WorkspaceManager
    return await WorkspaceManager(token, ctx).read(workspace_id)


async def read_test(token: BzmToken, ctx: Context, test_id: int) -> BaseResult:
    from tools.test_manager import TestManager
    return await TestManager(token, ctx).read(test_id)


async def count_project_tests(token: BzmToken, ctx: Context, project_id: int) -> int:
    from tools.test_manager import TestManager
    return (
        await TestManager(token, ctx).list(project_id=project_id, limit=1, offset=0, control_ai_consent=False)).total


async def read_execution(token: BzmToken, ctx: Context, execution_id: int) -> BaseResult:
    from tools.execution_manager import ExecutionManager
    return await ExecutionManager(token, ctx).read(execution_id)
