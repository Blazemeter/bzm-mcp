"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    10|Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from mcp.server.fastmcp import Context

from config.blazemeter import SUPPORT_MESSAGE, TESTS_ENDPOINT, TOOLS_PREFIX
from config.file_access import FileAccessPort
from config.runtime import AppRuntime
from config.storage import SessionScopeResolverPort
from config.tickets import TicketPort
from formatters.failure_criteria_labels import failure_criteria_meta_payload
from formatters.test import format_tests
from models.failure_criteria import (
    failure_criteria_from_configure_args,
    merge_failure_criteria_into_configuration_dict,
)
from models.manager import Manager
from models.performance_test import PerformanceTestObject
from models.result import BaseResult
from tools import bridge
from tools.actions import STDIO
from tools.actions.tests import ACTIONS, HEADER, HINTS
from tools.mcp_entrypoint import register_managed_tool
from tools.utils import (
    Operations,
    api_request,
    search,
    require_confirmation,
    run_as_task,
)
from tools.utils.uploads import HttpAssetMinter, StdioAssetUploader

ActionHandler = Callable[[dict[str, Any]], Awaitable[BaseResult]]


class TestManager(Manager):
    __test__ = False

    def __init__(
        self,
        ctx: Context,
        file_access: FileAccessPort | None = None,
        scope_resolver: SessionScopeResolverPort | None = None,
        tickets: TicketPort | None = None,
    ):
        super().__init__(ctx)
        self.file_access = file_access
        self.scope_resolver = scope_resolver
        self.tickets = tickets

    @run_as_task()
    async def read(self, test_id: int | None) -> BaseResult:
        if not isinstance(test_id, int) or test_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'test_id'. Expected integer."
            )

        test_result = await api_request(
            self.token,
            "GET",
            f"{TESTS_ENDPOINT}/{test_id}",
            result_formatter=format_tests,
        )
        if test_result.error:
            return test_result
        project_result = await bridge.read_project(
            self.token, self.ctx, test_result.result[0].project_id
        )
        if project_result.error:
            return project_result
        return test_result

    @require_confirmation(operation=Operations.CREATE)
    @run_as_task()
    async def create(self, test_name: str | None, project_id: int | None) -> BaseResult:
        if not isinstance(test_name, str) or not test_name.strip():
            return BaseResult(
                error="Missing or invalid required argument 'test_name'. Expected non-empty string."
            )
        if not isinstance(project_id, int) or project_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'project_id'. Expected integer."
            )

        project_result = await bridge.read_project(self.token, self.ctx, project_id)
        if project_result.error:
            return project_result

        test_body = {
            "name": test_name,
            "projectId": project_id,
            "configuration": {
                "type": "taurus",
                "filename": "DemoTest.jmx",
                "testMode": "script",
                "scriptType": "jmeter",
            },
        }
        return await api_request(
            self.token,
            "POST",
            f"{TESTS_ENDPOINT}",
            result_formatter=format_tests,
            json=test_body,
        )

    @require_confirmation(operation=Operations.DELETE)
    @run_as_task()
    async def delete(self, test_id: int | None) -> BaseResult:
        if not isinstance(test_id, int) or test_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'test_id'. Expected integer."
            )

        test_result = await self.read(test_id)
        if test_result.error:
            return test_result
        test_deleted_result = await api_request(
            self.token, "DELETE", f"{TESTS_ENDPOINT}/{test_id}"
        )
        if test_deleted_result.error:
            return test_deleted_result
        test_deleted_result.result = [f"Test {test_id} Deleted Successfully"]
        return test_deleted_result

    @require_confirmation(operation=Operations.CREATE)
    @run_as_task()
    async def upload_assets(
        self,
        test_id: int | None,
        file_paths: list[str] | None,
        main_script: str | None = None,
    ) -> BaseResult:
        return await StdioAssetUploader(self.file_access, self.scope_resolver).upload(
            self.token,
            self.ctx,
            test_id,
            file_paths,
            main_script,
            self.read,
        )

    @require_confirmation(operation=Operations.CREATE)
    @run_as_task()
    async def upload_assets_remote(self, args: dict[str, Any]) -> BaseResult:
        return await HttpAssetMinter(self.tickets, self.scope_resolver).mint(
            self.token,
            self.ctx,
            args,
            self.read,
        )

    @run_as_task()
    async def list(
        self,
        project_id: int | None,
        limit: int = 50,
        offset: int = 0,
        control_ai_consent: bool = True,
    ) -> BaseResult:
        if not isinstance(project_id, int) or project_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'project_id'. Expected integer."
            )
        if not isinstance(limit, int) or not isinstance(offset, int):
            return BaseResult(
                error="Invalid arguments 'limit'/'offset'. Expected integers."
            )

        if control_ai_consent:
            project_result = await bridge.read_project(self.token, self.ctx, project_id)
            if project_result.error:
                return project_result

        parameters = {
            "projectId": project_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated",
        }

        return await api_request(
            self.token,
            "GET",
            f"{TESTS_ENDPOINT}",
            result_formatter=format_tests,
            params=parameters,
        )

    @run_as_task()
    async def search(self, args: dict[str, Any]) -> BaseResult:
        account_id = args.get("account_id")
        if not isinstance(account_id, int) or account_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'account_id'. Expected integer."
            )
        account_data = await bridge.read_account(self.token, self.ctx, account_id)
        if account_data.error:
            return account_data

        return await search.test_execution_search(
            "test-union", self.token, account_id, args
        )

    @run_as_task()
    async def search_filter_values(
        self, account_id: int, filter_names: list[str]
    ) -> BaseResult:
        account_data = await bridge.read_account(self.token, self.ctx, account_id)
        if account_data.error:
            return account_data

        return await search.test_execution_search_filter_values(
            "test-union", account_id, self.token, filter_names
        )

    @staticmethod
    def _normalize_configuration_override(
        configuration: dict, test_data_override: dict
    ) -> dict:
        if (
            configuration.get("holdFor") is not None
            and test_data_override.get("iterations") is not None
        ):
            del test_data_override["iterations"]

        if (
            configuration.get("iterations") is not None
            and test_data_override.get("holdFor") is not None
        ):
            del test_data_override["holdFor"]

        concurrency = test_data_override.get("concurrency")
        if concurrency is not None and concurrency < 1:
            del test_data_override["concurrency"]

        steps = test_data_override.get("steps")
        if steps is not None and steps < 0:
            del test_data_override["steps"]

        ramp_up = test_data_override.get("rampUp")
        if ramp_up is not None and ramp_up == "":
            del test_data_override["rampUp"]

        concurrency = test_data_override.get("concurrency", 1)
        locations_concurrency = {}
        if "locationsPercents" in test_data_override:
            for location, percent in test_data_override["locationsPercents"].items():
                locations_concurrency[location] = int(percent * concurrency / 100)

            first_location = next(iter(locations_concurrency), None)
            if (
                first_location is not None
                and locations_concurrency[first_location] == 0
            ):
                locations_concurrency[first_location] = 1

            test_data_override["locations"] = locations_concurrency

        return test_data_override

    @require_confirmation(operation=Operations.UPDATE)
    @run_as_task()
    async def configure(self, performance_test: PerformanceTestObject) -> BaseResult:
        if not performance_test.is_valid():
            raise ValueError("PerformanceTestObject must have a valid test_id")

        test_data = await self.read(performance_test.test_id)
        if test_data.error:
            return test_data

        test_override_executions = test_data.result[0].override_executions
        test_data_override = {}
        for override in test_override_executions:
            test_data_override.update(override)
        configuration = performance_test.get_configuration()
        test_data_override.update(configuration)

        test_data_override = self._normalize_configuration_override(
            test_data_override, test_data_override
        )

        override_executions = [test_data_override] if test_data_override else None
        configuration_body = {"overrideExecutions": override_executions}

        return await api_request(
            self.token,
            "PATCH",
            f"{TESTS_ENDPOINT}/{performance_test.test_id}",
            result_formatter=format_tests,
            json=configuration_body,
        )

    @require_confirmation(operation=Operations.UPDATE)
    @run_as_task()
    async def configure_failure_criteria(self, args: dict[str, Any]) -> BaseResult:
        test_id = args.get("test_id")
        if not isinstance(test_id, int) or test_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'test_id'. Expected integer."
            )
        try:
            fc = failure_criteria_from_configure_args(args)
        except ValueError as e:
            return BaseResult(error=str(e))

        test_data = await self.read(test_id)
        if test_data.error:
            return test_data

        configuration = test_data.result[0].configuration
        if not isinstance(configuration, dict):
            configuration = {}
        merged_configuration = merge_failure_criteria_into_configuration_dict(
            configuration, fc
        )
        return await api_request(
            self.token,
            "PATCH",
            f"{TESTS_ENDPOINT}/{test_id}",
            result_formatter=format_tests,
            json={"configuration": merged_configuration},
        )

    @run_as_task()
    async def failure_criteria_meta(self, args: dict[str, Any]) -> BaseResult:
        return BaseResult(result=[failure_criteria_meta_payload()])


def build_test_handlers(manager: TestManager, transport: str) -> dict[str, ActionHandler]:
    async def upload_assets(args: dict[str, Any]) -> BaseResult:
        if transport == STDIO:
            return await manager.upload_assets(
                args.get("test_id"),
                args.get("file_paths"),
                args.get("main_script"),
            )
        return await manager.upload_assets_remote(args)

    return {
        "read": lambda args: manager.read(args.get("test_id")),
        "create": lambda args: manager.create(
            args.get("test_name"), args.get("project_id")
        ),
        "delete": lambda args: manager.delete(args.get("test_id")),
        "list": lambda args: manager.list(
            args.get("project_id"),
            args.get("limit", 50),
            args.get("offset", 0),
        ),
        "search": manager.search,
        "search_filter_values": lambda args: manager.search_filter_values(
            args.get("account_id"), args.get("filter_names", [])
        ),
        "configure_load": lambda args: manager.configure(
            PerformanceTestObject.from_args(args)
        ),
        "configure_locations": lambda args: manager.configure(
            PerformanceTestObject.from_args(args)
        ),
        "upload_assets": upload_assets,
        "configure_failure_criteria": manager.configure_failure_criteria,
        "failure_criteria_meta": manager.failure_criteria_meta,
    }


def register(mcp, runtime: AppRuntime):
    async def _dispatch(action, args, token, ctx):
        test_manager = TestManager(
            ctx,
            runtime.file_access,
            runtime.scope_resolver,
            runtime.tickets,
        )
        handler = build_test_handlers(test_manager, runtime.transport).get(action)
        if handler is None:
            return BaseResult(
                error=f"Action {action} not found in tests manager tool"
            )
        return await handler(args)

    register_managed_tool(
        mcp,
        runtime,
        name=f"{TOOLS_PREFIX}_tests",
        actions=ACTIONS,
        header=HEADER,
        hints=HINTS,
        dispatch=_dispatch,
        support_message=SUPPORT_MESSAGE,
    )
