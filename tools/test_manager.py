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

import asyncio
import builtins
import logging
import re
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import Context

from config.blazemeter import SUPPORT_MESSAGE, TESTS_ENDPOINT, TOOLS_PREFIX
from config.file_access import FileAccessPort
from config.runtime import AppRuntime
from config.security import detect_sensitive_upload_path_reason
from config.storage import HOSTED_FILE_ACCESS_MESSAGE, SessionScopeResolverPort
from config.tickets import TicketClientError, TicketPort
from formatters.failure_criteria_labels import failure_criteria_meta_payload
from formatters.test import format_tests
from models.failure_criteria import (
    failure_criteria_from_configure_args,
    merge_failure_criteria_into_configuration_dict,
)
from models.manager import Manager
from models.performance_test import PerformanceTestObject
from models.result import BaseResult
from tools import bridge, search_utils
from tools.action_spec import STDIO, action_by_name, filter_actions
from tools.mcp_entrypoint import register_managed_tool
from tools.test_actions import TEST_ACTIONS, TEST_HINTS, TEST_TOOL_HEADER
from tools.utils import (
    Operations,
    api_request,
    format_sanitized_traceback,
    require_confirmation,
    run_as_task,
    validate_required_args,
)

logger = logging.getLogger(__name__)

TEST_DISPATCH_ACTIONS = frozenset(
    {
        "read",
        "create",
        "delete",
        "list",
        "search",
        "search_filter_values",
        "configure_load",
        "configure_locations",
        "upload_assets",
        "configure_failure_criteria",
        "failure_criteria_meta",
    }
)
_FILENAME_RE = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9]+$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_ALLOWED_ENCODINGS = frozenset({"identity", "gzip"})
_FORBIDDEN_UPLOAD_KEYS = frozenset(
    {"file", "file_paths", "content", "bytes", "base64", "main_script"}
)


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

    def _current_scope(self):
        return self.scope_resolver.resolve(self.ctx, self.token)

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
        else:
            # Check if it's valid or allowed
            project_result = await bridge.read_project(
                self.token, self.ctx, test_result.result[0].project_id
            )
            if project_result.error:
                return project_result
            else:
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

        # Check if it's valid or allowed
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
        else:
            test_deleted_result = await api_request(
                self.token, "DELETE", f"{TESTS_ENDPOINT}/{test_id}"
            )
            if test_deleted_result.error:
                return test_deleted_result
            else:
                # The Delete operation returns null content
                # Text is incorporated to give context to the AI of the successful operation.
                test_deleted_result.result = [f"Test {test_id} Deleted Successfully"]
                return test_deleted_result

    @classmethod
    def _detect_sensitive_path_reason(cls, file_path: str) -> str | None:
        return detect_sensitive_upload_path_reason(file_path)

    def _validate_files(
        self,
        file_paths: list[str],
        valid_files: list[str],
        invalid_files: list[str],
        blocked_files: list[dict[str, str]],
        file_access: FileAccessPort | None = None,
        scope=None,
    ):
        # Security design note:
        # Uploads are intentionally allowed from any user working location (not restricted to one workspace root),
        # because users may execute tests from different local projects or folders.
        # The destination is BlazeMeter-managed infrastructure, and sensitive-origin filtering is enforced by
        # detect_sensitive_upload_path_reason() to prevent accidental leakage of system/secret files.
        # UNC paths are intentionally supported by design. Any sensitive data exposed through shared UNC
        # locations is an administrative responsibility of the UNC share owners/administrators.
        for file_path in file_paths:
            logger.debug(f"Checking file: {file_path}")
            sensitive_reason = self._detect_sensitive_path_reason(file_path)
            if sensitive_reason:
                logger.warning(
                    f"Blocked sensitive file path: {file_path} ({sensitive_reason})"
                )
                blocked_files.append(
                    {
                        "file": file_path,
                        "reason": sensitive_reason,
                    }
                )
                continue
            exists = (
                file_access.exists(file_path, scope=scope) if file_access else False
            )
            is_file = (
                file_access.is_file(file_path, scope=scope) if file_access else False
            )
            if exists and is_file:
                logger.debug(f"File exists: {file_path}")
                valid_files.append(file_path)
            else:
                logger.debug(f"File does not exist: {file_path}")
                invalid_files.append(file_path)

    @staticmethod
    def _process_upload_results(
        upload_results: list[dict[str, Any]],
        valid_files: list[str],
        successful_uploads: list[dict[str, Any]],
        failed_uploads: list[dict[str, Any]],
    ):
        for i, result in enumerate(upload_results):
            if isinstance(result, Exception):
                logger.error(f"Upload failed for {valid_files[i]}: {result}")
                failed_uploads.append({"file": valid_files[i], "error": str(result)})
            else:
                logger.debug(f"Upload successful for {valid_files[i]}: {result}")
                successful_uploads.append({"file": valid_files[i], "result": result})

    @require_confirmation(operation=Operations.CREATE)
    @run_as_task()
    async def upload_assets(
        self,
        test_id: int | None,
        file_paths: list[str] | None,
        main_script: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(test_id, int) or test_id < 1:
            return {
                "error": "Missing or invalid required argument 'test_id'. Expected integer."
            }
        if not isinstance(file_paths, list) or not file_paths:
            return {
                "error": "Missing or invalid required argument 'file_paths'. Expected non-empty list."
            }
        if self.file_access is None or self.scope_resolver is None:
            return {"error": HOSTED_FILE_ACCESS_MESSAGE}

        # Check if it's valid or allowed
        test_data = await self.read(test_id)
        if test_data.error:
            return {"error": test_data.error}

        logger.debug(f"Starting upload_assets for test_id: {test_id}")
        logger.debug(f"Original file paths: {file_paths}")
        logger.debug(f"Main script: {main_script}")
        scope = self._current_scope()

        mapped_file_paths = self.file_access.map_paths(file_paths, scope=scope)
        logger.debug(f"Mapped file paths: {mapped_file_paths}")

        mapped_main_script = None
        if main_script:
            mapped_main_script_list = self.file_access.map_paths(
                [main_script], scope=scope
            )
            mapped_main_script = (
                mapped_main_script_list[0] if mapped_main_script_list else None
            )
            logger.debug(f"Mapped main script: {mapped_main_script}")

        valid_files = []
        invalid_files = []
        blocked_files = []

        self._validate_files(
            mapped_file_paths,
            valid_files,
            invalid_files,
            blocked_files,
            file_access=self.file_access,
            scope=scope,
        )

        logger.debug(f"Valid files: {valid_files}")
        logger.debug(f"Invalid files: {invalid_files}")
        logger.debug(f"Blocked files: {blocked_files}")

        if not valid_files:
            logger.error("No valid files found to upload")
            return {
                "error": "No valid files found to upload",
                "invalid_files": invalid_files,
                "blocked_files": blocked_files,
            }

        logger.debug("Starting concurrent uploads")
        upload_tasks = [
            self._upload_single_file(test_id, file_path, scope)
            for file_path in valid_files
        ]
        upload_results = await asyncio.gather(*upload_tasks, return_exceptions=True)

        logger.debug(f"Upload results: {upload_results}")

        successful_uploads = []
        failed_uploads = []

        self._process_upload_results(
            upload_results, valid_files, successful_uploads, failed_uploads
        )

        config_update_result = None
        if mapped_main_script and mapped_main_script in valid_files:
            logger.debug(
                f"Updating test configuration with main script: {mapped_main_script}"
            )
            config_update_result = await self._update_test_configuration(
                test_id, mapped_main_script
            )

        return {
            "test_id": test_id,
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads,
            "invalid_files": invalid_files,
            "blocked_files": blocked_files,
            "config_update": config_update_result,
        }

    @require_confirmation(operation=Operations.CREATE)
    @run_as_task()
    async def upload_assets_remote(self, args: dict[str, Any]) -> dict[str, Any]:
        forbidden = sorted(_FORBIDDEN_UPLOAD_KEYS.intersection(args))
        if forbidden:
            return {
                "error": (
                    "HTTP upload_assets does not accept file bytes, paths, or main_script. "
                    f"Remove: {', '.join(forbidden)}."
                )
            }
        if self.tickets is None or self.scope_resolver is None:
            return {"error": "Upload tickets are not configured for this runtime."}
        if self.token is None:
            return {"error": "Missing BlazeMeter credentials for this request."}

        test_id = args.get("test_id")
        filename = args.get("filename")
        declared_size = args.get("declared_size")
        encoding = args.get("encoding")
        sha256 = args.get("sha256")

        if not isinstance(test_id, int) or isinstance(test_id, bool) or test_id < 1:
            return {
                "error": "Missing or invalid required argument 'test_id'. Expected integer."
            }
        if (
            not isinstance(filename, str)
            or not (3 <= len(filename) <= 255)
            or not _FILENAME_RE.fullmatch(filename)
        ):
            return {
                "error": (
                    "Invalid filename. Use ASCII letters, digits, underscore, hyphen, "
                    "and a required extension (length 3-255)."
                )
            }
        if (
            not isinstance(declared_size, int)
            or isinstance(declared_size, bool)
            or declared_size <= 0
        ):
            return {
                "error": "Invalid declared_size. Expected an integer greater than 0."
            }
        if encoding not in _ALLOWED_ENCODINGS:
            return {"error": "Invalid encoding. Expected 'identity' or 'gzip'."}
        if not isinstance(sha256, str) or not _SHA256_RE.fullmatch(sha256):
            return {"error": "Invalid sha256. Expected 64 hexadecimal characters."}
        sha256 = sha256.lower()

        test_data = await self.read(test_id)
        if test_data.error:
            return {"error": test_data.error}

        scope = self._current_scope()
        try:
            await self.tickets.put_credential(
                scope.user_id, scope.mcp_session_id, self.token.as_basic_auth()
            )
            minted = await self.tickets.mint(
                scope.user_id,
                scope.mcp_session_id,
                test_id,
                filename,
                declared_size,
                encoding,
                sha256,
            )
        except TicketClientError as exc:
            return {"error": str(exc)}

        logger.info("minted upload ticket %s for test %s", minted.id, test_id)
        return {
            "method": "POST",
            "url": self.tickets.public_upload_url(minted.id),
            "authorization": f"Bearer {minted.token}",
            "headers": {
                "Authorization": f"Bearer {minted.token}",
                "X-Upload-Filename": filename,
                "X-Content-SHA256": sha256,
                "Content-Encoding": encoding,
            },
            "size_ceiling": minted.size_ceiling,
            "redeem_deadline": minted.redeem_deadline,
            "upload_deadline": minted.upload_deadline,
            "one_file_per_url": True,
            "success_status": 201,
            "test_id": test_id,
            "filename": filename,
        }

    async def _upload_single_file(
        self, test_id: int, file_path: str, scope
    ) -> BaseResult:
        logger.debug(f"Uploading single file: {file_path} to test: {test_id}")
        try:
            file_name = Path(file_path).name

            logger.debug(f"File name: {file_name}")

            file_content = self.file_access.read_bytes(file_path, scope=scope)

            logger.debug(f"File size: {len(file_content)} bytes")

            files = {"file": (file_name, file_content, self._get_mime_type(file_path))}

            endpoint = f"{TESTS_ENDPOINT}/{test_id}/files"
            logger.debug(f"Uploading to endpoint: {endpoint}")

            result = await api_request(self.token, "POST", endpoint, files=files)

            logger.debug(f"Upload result: {result}")

            return result

        except Exception as e:
            logger.error(f"Exception in _upload_single_file: {e}")
            logger.error(f"Traceback: {format_sanitized_traceback(e)}")
            raise Exception(f"Failed to upload {file_path}: {e!s}")

    async def _update_test_configuration(
        self, test_id: int, main_script_path: str
    ) -> BaseResult:
        try:
            file_name = Path(main_script_path).name
            config_update = {
                "configuration": {
                    "filename": file_name,
                    "scriptType": self._get_script_type(file_name),
                }
            }

            return await api_request(
                self.token, "PATCH", f"{TESTS_ENDPOINT}/{test_id}", json=config_update
            )

        except Exception as e:
            raise Exception(f"Failed to update test configuration: {e!s}")

    @staticmethod
    def _get_mime_type(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        mime_types = {
            ".jmx": "application/xml",
            ".yaml": "text/yaml",
            ".yml": "text/yaml",
            ".csv": "text/csv",
            ".zip": "application/zip",
            ".jar": "application/java-archive",
            ".properties": "text/plain",
            ".xml": "application/xml",
        }

        return mime_types.get(extension, "application/octet-stream")

    @staticmethod
    def _get_script_type(file_name: str) -> str:
        extension = Path(file_name).suffix.lower()

        script_types = {
            ".jmx": "jmeter",
            ".yaml": "taurus",
            ".yml": "taurus",
            ".py": "python",
            ".js": "javascript",
        }

        return script_types.get(extension, "unknown")

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
            # Check if it's valid or allowed
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
        # Check if it's valid or allowed
        account_id = args.get("account_id")
        if not isinstance(account_id, int) or account_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'account_id'. Expected integer."
            )
        account_data = await bridge.read_account(self.token, self.ctx, account_id)
        if account_data.error:
            return account_data

        return await search_utils.test_execution_search(
            "test-union", self.token, account_id, args
        )

    @run_as_task()
    async def search_filter_values(
        self, account_id: int, filter_names: builtins.list[str]
    ) -> BaseResult:
        # Check if it's valid or allowed
        account_data = await bridge.read_account(self.token, self.ctx, account_id)
        if account_data.error:
            return account_data

        return await search_utils.test_execution_search_filter_values(
            "test-union", account_id, self.token, filter_names
        )

    @staticmethod
    def _normalize_configuration_override(
        configuration: dict, test_data_override: dict
    ) -> dict:
        # Switch between iteration and duration
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

        # Remove concurrency if value it's zero
        concurrency = test_data_override.get("concurrency")
        if concurrency is not None and concurrency < 1:
            del test_data_override["concurrency"]

        # Remove ramp up steps if value it's -1
        steps = test_data_override.get("steps")
        if steps is not None and steps < 0:
            del test_data_override["steps"]

        # Remove ramp up if it's empty
        ramp_up = test_data_override.get("rampUp")
        if ramp_up is not None and ramp_up == "":
            del test_data_override["rampUp"]

        # Recalculate location concurrency
        concurrency = test_data_override.get("concurrency", 1)
        locations_concurrency = {}
        if "locationsPercents" in test_data_override:
            for location, percent in test_data_override["locationsPercents"].items():
                locations_concurrency[location] = int(percent * concurrency / 100)

            # Fallback behavior: int(percent * concurrency / 100) can truncate to 0 for low loads.
            # To avoid ending with all locations at 0 users, we guarantee at least 1 user only on
            # the first location when that first computed value is 0.
            first_location = next(iter(locations_concurrency), None)
            if (
                first_location is not None
                and locations_concurrency[first_location] == 0
            ):
                locations_concurrency[first_location] = (
                    1  # Default behaviour on BlazeMeter
                )

            test_data_override["locations"] = locations_concurrency

        return test_data_override

    @require_confirmation(operation=Operations.UPDATE)
    @run_as_task()
    async def configure(self, performance_test: PerformanceTestObject) -> BaseResult:
        if not performance_test.is_valid():
            raise ValueError("PerformanceTestObject must have a valid test_id")

        # Check if it's valid or allowed
        test_data = await self.read(performance_test.test_id)
        if test_data.error:
            return test_data

        test_override_executions = test_data.result[0].override_executions
        test_data_override = {}
        # Flat the overrides if more then one exists
        for override in test_override_executions:
            test_data_override.update(override)
        configuration = performance_test.get_configuration()
        test_data_override.update(configuration)

        # Normalize Override
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
        """Replace failure criteria for a test via PATCH configuration (preserves plugins.jmeter)."""
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
        """Return the full KPI and condition catalog for building configure_failure_criteria rules (no API call)."""
        return BaseResult(result=[failure_criteria_meta_payload()])


def _unwrap_upload_result(upload_result: Any) -> BaseResult:
    if isinstance(upload_result, BaseResult):
        if upload_result.error:
            return upload_result
        inner = (
            upload_result.result[0]
            if upload_result.result and len(upload_result.result) == 1
            else None
        )
        if isinstance(inner, dict) and inner.get("error"):
            return BaseResult(error=str(inner["error"]))
        return upload_result
    if isinstance(upload_result, dict) and upload_result.get("error"):
        return BaseResult(error=upload_result["error"])
    return BaseResult(result=[upload_result])


def register(mcp, runtime: AppRuntime):
    visible = filter_actions(runtime.transport, TEST_ACTIONS)

    async def _dispatch(action, args, token, ctx):
        test_manager = TestManager(
            ctx,
            runtime.file_access,
            runtime.scope_resolver,
            runtime.tickets,
        )
        match action:
            case "read":
                return await test_manager.read(args.get("test_id"))
            case "create":
                return await test_manager.create(
                    args.get("test_name"), args.get("project_id")
                )
            case "delete":
                return await test_manager.delete(args.get("test_id"))
            case "list":
                return await test_manager.list(
                    args.get("project_id"),
                    args.get("limit", 50),
                    args.get("offset", 0),
                )
            case "search":
                return await test_manager.search(args)
            case "search_filter_values":
                return await test_manager.search_filter_values(
                    args.get("account_id"), args.get("filter_names", [])
                )
            case "configure_load":
                performance_test = PerformanceTestObject.from_args(args)
                return await test_manager.configure(performance_test)
            case "configure_locations":
                performance_test = PerformanceTestObject.from_args(args)
                return await test_manager.configure(performance_test)
            case "upload_assets":
                spec = action_by_name(visible, "upload_assets")
                if spec is None:
                    return BaseResult(
                        error=f"Action upload_assets is not available on {runtime.transport}."
                    )
                if validation_error := validate_required_args(
                    action, args, list(spec.required_args)
                ):
                    return validation_error
                if runtime.transport == STDIO:
                    upload_result = await test_manager.upload_assets(
                        args.get("test_id"),
                        args.get("file_paths"),
                        args.get("main_script"),
                    )
                else:
                    upload_result = await test_manager.upload_assets_remote(args)
                return _unwrap_upload_result(upload_result)
            case "configure_failure_criteria":
                if validation_error := validate_required_args(
                    action, args, ["test_id", "enabled", "rules"]
                ):
                    return validation_error
                return await test_manager.configure_failure_criteria(args)
            case "failure_criteria_meta":
                return await test_manager.failure_criteria_meta(args)
            case _:
                return BaseResult(
                    error=f"Action {action} not found in tests manager tool"
                )

    register_managed_tool(
        mcp,
        runtime,
        name=f"{TOOLS_PREFIX}_tests",
        actions=TEST_ACTIONS,
        header=TEST_TOOL_HEADER,
        hints=TEST_HINTS,
        dispatch=_dispatch,
        support_message=SUPPORT_MESSAGE,
    )
