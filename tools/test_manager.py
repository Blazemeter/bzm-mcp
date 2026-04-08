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
import logging
import os
from pathlib import Path
from typing import Any, Dict
from typing import Optional, List

import httpx
from mcp.server.fastmcp import Context

from config.blazemeter import TESTS_ENDPOINT, TOOLS_PREFIX
from config.path_mapper import PathMapperFactory
from config.security import detect_sensitive_upload_path_reason
from config.token import BzmToken
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
from tools.utils import api_request, require_confirmation, Operations, format_sanitized_traceback

logger = logging.getLogger(__name__)


class TestManager(Manager):
    __test__ = False

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)
        self.path_mapper = PathMapperFactory.create_strategy()

    async def read(self, test_id: Optional[int]) -> BaseResult:
        if not isinstance(test_id, int) or test_id < 1:
            return BaseResult(error="Missing or invalid required argument 'test_id'. Expected integer.")

        test_result = await api_request(
            self.token,
            "GET",
            f"{TESTS_ENDPOINT}/{test_id}",
            result_formatter=format_tests
        )
        if test_result.error:
            return test_result
        else:
            # Check if it's valid or allowed
            project_result = await bridge.read_project(self.token, self.ctx, test_result.result[0].project_id)
            if project_result.error:
                return project_result
            else:
                return test_result

    @require_confirmation(operation=Operations.CREATE)
    async def create(self, test_name: Optional[str], project_id: Optional[int]) -> BaseResult:
        if not isinstance(test_name, str) or not test_name.strip():
            return BaseResult(error="Missing or invalid required argument 'test_name'. Expected non-empty string.")
        if not isinstance(project_id, int) or project_id < 1:
            return BaseResult(error="Missing or invalid required argument 'project_id'. Expected integer.")

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
                "scriptType": "jmeter"
            }
        }
        return await api_request(
            self.token,
            "POST",
            f"{TESTS_ENDPOINT}",
            result_formatter=format_tests,
            json=test_body
        )

    @require_confirmation(operation=Operations.DELETE)
    async def delete(self, test_id: Optional[int]) -> BaseResult:
        if not isinstance(test_id, int) or test_id < 1:
            return BaseResult(error="Missing or invalid required argument 'test_id'. Expected integer.")

        test_result = await self.read(test_id)
        if test_result.error:
            return test_result
        else:
            test_deleted_result = await api_request(
                self.token,
                "DELETE",
                f"{TESTS_ENDPOINT}/{test_id}"
            )
            if test_deleted_result.error:
                return test_deleted_result
            else:
                # The Delete operation returns null content
                # Text is incorporated to give context to the AI of the successful operation.
                test_deleted_result.result = [f"Test {test_id} Deleted Successfully"]
                return test_deleted_result

    @classmethod
    def _detect_sensitive_path_reason(cls, file_path: str) -> Optional[str]:
        return detect_sensitive_upload_path_reason(file_path)

    @classmethod
    def _validate_files(cls, file_paths: List[str], valid_files: List[str], invalid_files: List[str],
                        blocked_files: List[Dict[str, str]]):
        # Security design note:
        # Uploads are intentionally allowed from any user working location (not restricted to one workspace root),
        # because users may execute tests from different local projects or folders.
        # The destination is BlazeMeter-managed infrastructure, and sensitive-origin filtering is enforced by
        # detect_sensitive_upload_path_reason() to prevent accidental leakage of system/secret files.
        # UNC paths are intentionally supported by design. Any sensitive data exposed through shared UNC
        # locations is an administrative responsibility of the UNC share owners/administrators.
        for file_path in file_paths:
            logger.debug(f"Checking file: {file_path}")
            sensitive_reason = cls._detect_sensitive_path_reason(file_path)
            if sensitive_reason:
                logger.warning(f"Blocked sensitive file path: {file_path} ({sensitive_reason})")
                blocked_files.append({
                    "file": file_path,
                    "reason": sensitive_reason,
                })
                continue
            if os.path.exists(file_path) and os.path.isfile(file_path):
                logger.debug(f"File exists: {file_path}")
                valid_files.append(file_path)
            else:
                logger.debug(f"File does not exist: {file_path}")
                invalid_files.append(file_path)

    @staticmethod
    def _process_upload_results(upload_results: List[Dict[str, Any]], valid_files: List[str],
                                successful_uploads: List[Dict[str, Any]], failed_uploads: List[Dict[str, Any]]):
        for i, result in enumerate(upload_results):
            if isinstance(result, Exception):
                logger.error(f"Upload failed for {valid_files[i]}: {result}")
                failed_uploads.append({
                    "file": valid_files[i],
                    "error": str(result)
                })
            else:
                logger.debug(f"Upload successful for {valid_files[i]}: {result}")
                successful_uploads.append({
                    "file": valid_files[i],
                    "result": result
                })

    @require_confirmation(operation=Operations.CREATE)
    async def upload_assets(self, test_id: Optional[int], file_paths: Optional[List[str]],
                            main_script: Optional[str] = None) -> Dict[
        str, Any]:
        if not isinstance(test_id, int) or test_id < 1:
            return {"error": "Missing or invalid required argument 'test_id'. Expected integer."}
        if not isinstance(file_paths, list) or not file_paths:
            return {"error": "Missing or invalid required argument 'file_paths'. Expected non-empty list."}

        # Check if it's valid or allowed
        test_data = await self.read(test_id)
        if test_data.error:
            return {"error": test_data.error}

        logger.debug(f"Starting upload_assets for test_id: {test_id}")
        logger.debug(f"Original file paths: {file_paths}")
        logger.debug(f"Main script: {main_script}")

        mapped_file_paths = self.path_mapper.map_paths(file_paths)
        logger.debug(f"Mapped file paths: {mapped_file_paths}")

        mapped_main_script = None
        if main_script:
            mapped_main_script_list = self.path_mapper.map_paths([main_script])
            mapped_main_script = mapped_main_script_list[0] if mapped_main_script_list else None
            logger.debug(f"Mapped main script: {mapped_main_script}")

        valid_files = []
        invalid_files = []
        blocked_files = []

        self._validate_files(mapped_file_paths, valid_files, invalid_files, blocked_files)

        logger.debug(f"Valid files: {valid_files}")
        logger.debug(f"Invalid files: {invalid_files}")
        logger.debug(f"Blocked files: {blocked_files}")

        if not valid_files:
            logger.error("No valid files found to upload")
            return {
                "error": "No valid files found to upload",
                "invalid_files": invalid_files,
                "blocked_files": blocked_files
            }

        logger.debug("Starting concurrent uploads")
        upload_tasks = [self._upload_single_file(test_id, file_path) for file_path in valid_files]
        upload_results = await asyncio.gather(*upload_tasks, return_exceptions=True)

        logger.debug(f"Upload results: {upload_results}")

        successful_uploads = []
        failed_uploads = []

        self._process_upload_results(upload_results, valid_files, successful_uploads, failed_uploads)

        config_update_result = None
        if mapped_main_script and mapped_main_script in valid_files:
            logger.debug(f"Updating test configuration with main script: {mapped_main_script}")
            config_update_result = await self._update_test_configuration(test_id, mapped_main_script)

        return {
            "test_id": test_id,
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads,
            "invalid_files": invalid_files,
            "blocked_files": blocked_files,
            "config_update": config_update_result
        }

    async def _upload_single_file(self, test_id: int, file_path: str) -> BaseResult:
        logger.debug(f"Uploading single file: {file_path} to test: {test_id}")
        try:
            file_path_obj = Path(file_path)
            file_name = file_path_obj.name

            logger.debug(f"File name: {file_name}")

            with open(file_path, 'rb') as file:
                file_content = file.read()

            logger.debug(f"File size: {len(file_content)} bytes")

            files = {
                'file': (file_name, file_content, self._get_mime_type(file_path))
            }

            endpoint = f"{TESTS_ENDPOINT}/{test_id}/files"
            logger.debug(f"Uploading to endpoint: {endpoint}")

            result = await api_request(
                self.token,
                "POST",
                endpoint,
                files=files)

            logger.debug(f"Upload result: {result}")

            return result

        except Exception as e:
            logger.error(f"Exception in _upload_single_file: {e}")
            logger.error(f"Traceback: {format_sanitized_traceback(e)}")
            raise Exception(f"Failed to upload {file_path}: {str(e)}")

    async def _update_test_configuration(self, test_id: int, main_script_path: str) -> BaseResult:
        try:
            file_name = Path(main_script_path).name
            config_update = {
                "configuration": {
                    "filename": file_name,
                    "scriptType": self._get_script_type(file_name)
                }
            }

            return await api_request(
                self.token,
                "PATCH",
                f"{TESTS_ENDPOINT}/{test_id}",
                json=config_update
            )

        except Exception as e:
            raise Exception(f"Failed to update test configuration: {str(e)}")

    @staticmethod
    def _get_mime_type(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        mime_types = {
            '.jmx': 'application/xml',
            '.yaml': 'text/yaml',
            '.yml': 'text/yaml',
            '.csv': 'text/csv',
            '.zip': 'application/zip',
            '.jar': 'application/java-archive',
            '.properties': 'text/plain',
            '.xml': 'application/xml'
        }

        return mime_types.get(extension, 'application/octet-stream')

    @staticmethod
    def _get_script_type(file_name: str) -> str:
        extension = Path(file_name).suffix.lower()

        script_types = {
            '.jmx': 'jmeter',
            '.yaml': 'taurus',
            '.yml': 'taurus',
            '.py': 'python',
            '.js': 'javascript'
        }

        return script_types.get(extension, 'unknown')

    async def list(self, project_id: Optional[int], limit: int = 50,
                   offset: int = 0, control_ai_consent: bool = True) -> BaseResult:
        if not isinstance(project_id, int) or project_id < 1:
            return BaseResult(error="Missing or invalid required argument 'project_id'. Expected integer.")
        if not isinstance(limit, int) or not isinstance(offset, int):
            return BaseResult(error="Invalid arguments 'limit'/'offset'. Expected integers.")

        if control_ai_consent:
            # Check if it's valid or allowed
            project_result = await bridge.read_project(self.token, self.ctx, project_id)
            if project_result.error:
                return project_result

        parameters = {
            "projectId": project_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        return await api_request(
            self.token,
            "GET",
            f"{TESTS_ENDPOINT}",
            result_formatter=format_tests,
            params=parameters
        )

    @staticmethod
    def _normalize_configuration_override(configuration: dict, test_data_override: dict) -> dict:
        # Switch between iteration and duration
        if configuration.get("holdFor") is not None and test_data_override.get("iterations") is not None:
            del test_data_override["iterations"]

        if configuration.get("iterations") is not None and test_data_override.get("holdFor") is not None:
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
            if first_location is not None and locations_concurrency[first_location] == 0:
                locations_concurrency[first_location] = 1  # Default behaviour on BlazeMeter

            test_data_override["locations"] = locations_concurrency

        return test_data_override

    @require_confirmation(operation=Operations.UPDATE)
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
        test_data_override = self._normalize_configuration_override(test_data_override, test_data_override)

        override_executions = [test_data_override] if test_data_override else None
        configuration_body = {
            "overrideExecutions": override_executions
        }

        return await api_request(
            self.token,
            "PATCH",
            f"{TESTS_ENDPOINT}/{performance_test.test_id}",
            result_formatter=format_tests,
            json=configuration_body)

    @require_confirmation(operation=Operations.UPDATE)
    async def configure_failure_criteria(self, args: Dict[str, Any]) -> BaseResult:
        """Replace failure criteria for a test via PATCH configuration (preserves plugins.jmeter)."""
        test_id = args.get("test_id")
        if not isinstance(test_id, int) or test_id < 1:
            return BaseResult(error="Missing or invalid required argument 'test_id'. Expected integer.")
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
        merged_configuration = merge_failure_criteria_into_configuration_dict(configuration, fc)
        return await api_request(
            self.token,
            "PATCH",
            f"{TESTS_ENDPOINT}/{test_id}",
            result_formatter=format_tests,
            json={"configuration": merged_configuration},
        )

    async def failure_criteria_meta(self, args: Dict[str, Any]) -> BaseResult:
        """Return the full KPI and condition catalog for building configure_failure_criteria rules (no API call)."""
        return BaseResult(result=[failure_criteria_meta_payload()])


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_tests",
        description="""
Operations on tests.
Actions:
- read: Read a test. Get the detailed information of a test.
    args(dict): Dictionary with the following required parameters:
        test_id (int): The only required parameter. The id of the test to read.
    When presenting failure_criteria to the user, use meta.general_labels, meta.rule_field_labels, meta.kpi_labels, and meta.condition_labels for readable text; avoid leading with raw kpi ids or op codes.
- create: Create a new test. Do not create a test if the user has not confirmed the location for validation of workspace, project and account.
    args(dict): Dictionary with the following required parameters:
        test_name (str): The required name of the test to create.
        project_id (int): The id of the project to list tests from.
- delete: Delete a test.
    args(dict): Dictionary with the following required parameters:
        test_id (int): The only required parameter. The id of the test to be deleted.
- list: List all tests. 
    args(dict): Dictionary with the following required parameters:
        project_id (int): The id of the project to list tests from.
        limit (int, default=10, valid=[1 to 50]): The number of tests to list.
        offset (int, default=0): Number of tests to skip.
    Each listed test may include failure_criteria; when describing it to the user, use meta labels like read (see read action).
- configure_load: Configure the load of a test for the given test id. The test id is the only required parameter. 
             The test will be configured based on the following parameters only if user confirms the configuration:
    args(dict): Dictionary with the following parameters:
        test_id (int): The only required parameter. The id of the test to configure.
        iterations (int, default=1, infinite=-1): The number of iterations to run the test with. Don't use if hold-for is provided.
        hold-for (str, default=1m): The length of time the test will run at the peak concurrency. Values can be provided in m (minutes) only. Don't use if iterations is provided.
        concurrency (int, default=20, disable=0, max=500000): The number of concurrent virtual users simulated to run. For example, 20 will set the test to run with 20 concurrent users. To disable it set to 0.
        ramp-up (str, disable=""): The length of time the test will take to ramp-up to full concurrency. Values can be provided in m (minutes) only. Can be empty.
        steps (int, default=1, disable=-1): The number of ramp-up steps. Can be empty.
        executor (str, default=jmeter): The script type you are running. Includes the following options: (gatling,grinder,jmeter,locust,pbench,selenium,siege).
- configure_locations: Configure the distribution of a test for given test id. The test id is the only required parameter. 
             The test will be configured based on the following parameters only if user confirms the configuration:
    args(dict): Dictionary with the following parameters:
        test_id (int): The only required parameter. The id of the test to configure.
        locations (list[str]): List of all locations with their percentage distribution of user load in a key value format "location_id=percent_value". Example: ["us-east4-a=25", "us-east1-b=25", "us-west1-a=25", "us-central1-a=25"]
- upload_assets: Upload main script test as well as multiple related assets to a test. Supports .zip, .csv, .jmx, .yaml and other file types.
    args(dict): Dictionary with the following required parameters:
        test_id (int): The id of the test to upload assets to.
        file_paths (list): List of full file paths to upload.
        main_script (str, optional): Path to the main script file. If provided, will update test configuration to use this script.
- failure_criteria_meta: Read-only catalog: overview (layers), top_level_tool_args, rule_fields, general, general_labels, rule_field_labels, kpis, conditions. Field names align with reading and configuring tests. No BlazeMeter API call.
    args(dict): Optional; may be empty {}. Unknown keys are ignored.
- configure_failure_criteria: Set failure criteria (BlazeMeter configuration.enableFailureCriteria and configuration.plugins.thresholds). Replaces the full rules list for the test.
    args(dict): Dictionary with the following parameters:
        test_id (int): Required. The test id.
        enabled (bool): Required. Master switch for the Failure Criteria section (API enableFailureCriteria).
        rules (list): Required. List of rule objects; use an empty list to clear all rules. Each object may include:
            kpi (str): Required per rule. API metric field name (`field`). Documented values (product may offer more):
                responseTime.avg, responseTime.min, responseTime.max, responseTime.std,
                responseTime.percentile.0, responseTime.percentile.50, responseTime.percentile.90,
                responseTime.percentile.95, responseTime.percentile.99,
                latency.avg, connectTime.avg, size.count, size.avg, size.rate,
                hits.count, hits.avg, hits.rate, duration.count,
                errors.count, errors.percent, errors.rate
            label (str, default=ALL): Label scope for the metric (default ALL labels).
            condition (str or null): API operator (`op`). Allowed string values:
                lt (Less than), gt (Greater than), eq (Equal to), ne (Not equal to),
                lte (Less than or equal to), gte (Greater than or equal to).
                Omit the key or use JSON null for no operator (incomplete / initial state).
            value (str): Threshold as string (numeric text, e.g. "500", "1"; may be empty until set).
            offset_percent (str, default=0.0): Baseline offset percentage string (API offsetPercentage).
            stop_test_on_violation (bool, default=false): Stop Test on violation (API stopTestOnViolation); product expects 1-min slide window when used.
            sliding_window (bool, default=false): 1-min slide window eval for this rule (API slidingWindow). Per-row "1-min slide window eval"; bulk "Enable 1-min slide window eval for all" means every rule has sliding_window true.
            ignore_rampup (bool, optional): Per-rule ignore ramp-up when the API includes it on the item.
            is_empty (bool, default=false): Incomplete row flag (API isEmpty).
        ignore_rampup (bool, optional): Container-level "Ignore failure criteria during ramp-up" (advanced); omit to keep existing value on merge.
        sliding_window_for_all (bool, optional): If set, sets every rule's sliding_window to this value after parsing rules (bulk convenience).
        from_taurus (bool, optional): plugins.thresholds.fromTaurus; omit to preserve existing.
        criteria_overridden_in_interface (bool, optional): Threshold-block metadata (maps to plugins.thresholds when merging); omit to preserve existing.
    Reading a test and configuring failure criteria use the same field names; BlazeMeter’s REST JSON is only used in HTTP calls inside the server.
Hints:
- **CRITICAL**: Always follow the action schema exactly. If args are required, include args with exact names/types.
- Before configure_failure_criteria, prefer failure_criteria_meta for kpi/condition codes and labels, then read if you must merge with existing rules.
- For configure_failure_criteria, call read first and merge client-side if you must keep existing rules; providing rules replaces all criteria rows for that test.
"""
    )
    async def tests(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        test_manager = TestManager(token, ctx)
        try:
            match action:
                case "read":
                    return await test_manager.read(args.get("test_id"))
                case "create":
                    return await test_manager.create(args.get("test_name"), args.get("project_id"))
                case "delete":
                    return await test_manager.delete(args.get("test_id"))
                case "list":
                    return await test_manager.list(args.get("project_id"), args.get("limit", 50), args.get("offset", 0))
                case "configure_load":
                    performance_test = PerformanceTestObject.from_args(args)
                    return await test_manager.configure(performance_test)
                case "configure_locations":
                    performance_test = PerformanceTestObject.from_args(args)
                    return await test_manager.configure(performance_test)
                case "upload_assets":
                    upload_result = await test_manager.upload_assets(
                        args.get("test_id"),
                        args.get("file_paths"),
                        args.get("main_script"),
                    )
                    if isinstance(upload_result, dict) and upload_result.get("error"):
                        return BaseResult(error=upload_result["error"])
                    return BaseResult(result=[upload_result])
                case "configure_failure_criteria":
                    return await test_manager.configure_failure_criteria(args)
                case "failure_criteria_meta":
                    return await test_manager.failure_criteria_meta(args)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in tests manager tool"
                    )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {format_sanitized_traceback()}"
            )
        except Exception:
            return BaseResult(
                error=f"""Error: {format_sanitized_traceback()}
                          If you think this is a bug, please contact BlazeMeter support or report issue at https://github.com/BlazeMeter/bzm-mcp/issues"""
            )
