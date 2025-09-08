import asyncio
import logging
import os
import traceback
from pathlib import Path
from typing import Any, Dict
from typing import Optional, List, Union

from mcp.server.fastmcp import Context
from pydantic import Field, BaseModel

from config.token import BzmToken
from models.performance_test import PerformanceTestObject
from models.result import BaseResult
from .base import api_request, get_date_time_iso, TOOLS_PREFIX

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Test(BaseModel):
    """Test basic information structure."""
    test_id: int = Field(description="The unique identifier for the test. Also known as a testId")
    test_name: str = Field(description="The test name")
    description: str = Field(description="A description of the test")
    created: Optional[str] = Field(description="The datetime that the test was created.", default=None)
    updated: Optional[str] = Field(description="The datetime that the test was updated", default=None)
    project_id: int = Field(description="The project Id to which this test belongs")
    status: str = Field(description="The status of the test")  # TODO: Really exist?
    type: str = Field(description="The type of the test")  # TODO: Really exist?
    configuration: Dict[str, Any] = Field(description="Contains all the advanced BlazeMeter related configurations")


class TestResult(BaseResult):
    result: Optional[List[Union[Test]]] = Field(description="Tests List", default=None)

class TestUploadResult:
    result: Optional[Dict[str: Any]] = Field(description="Upload Result", default=None)

class TestManager:

    def __init__(self, token: Optional[BzmToken]):
        self.token = token

    async def create(self, test_name: str, project_id: int) -> TestResult:
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
        test_response = await api_request(self.token, "POST", "/tests", json=test_body)
        if "error" in test_response and test_response["error"]:
            return TestResult(
                error=test_response.get("error")
            )

        tests = [test_response.get("result", None)]
        return TestResult(
            result=self.normalize_tests(tests)
        )

    @staticmethod
    def _validate_files(file_paths: List[str], valid_files: List[str], invalid_files: List[str]):
        for file_path in file_paths:
            logger.debug(f"Checking file: {file_path}")
            if os.path.exists(file_path) and os.path.isfile(file_path):
                logger.debug(f"File exists: {file_path}")
                valid_files.append(file_path)
            else:
                logger.debug(f"File does not exist: {file_path}")
                invalid_files.append(file_path)

    def _process_upload_results(self, upload_results: List[Dict[str, Any]], valid_files: List[str],
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

    async def upload_assets(self, test_id: int, file_paths: List[str], main_script: Optional[str] = None) -> Dict[
        str, Any]:
        logger.debug(f"Starting upload_assets for test_id: {test_id}")
        logger.debug(f"File paths: {file_paths}")
        logger.debug(f"Main script: {main_script}")

        valid_files = []
        invalid_files = []

        self._validate_files(file_paths, valid_files, invalid_files)

        logger.debug(f"Valid files: {valid_files}")
        logger.debug(f"Invalid files: {invalid_files}")

        if not valid_files:
            logger.error("No valid files found to upload")
            return {
                "error": "No valid files found to upload",
                "invalid_files": invalid_files
            }

        logger.debug("Starting concurrent uploads")
        upload_tasks = [self._upload_single_file(test_id, file_path) for file_path in valid_files]
        upload_results = await asyncio.gather(*upload_tasks, return_exceptions=True)

        logger.debug(f"Upload results: {upload_results}")

        successful_uploads = []
        failed_uploads = []

        self._process_upload_results(upload_results, valid_files, successful_uploads, failed_uploads)

        config_update_result = None
        if main_script and main_script in valid_files:
            logger.debug(f"Updating test configuration with main script: {main_script}")
            config_update_result = await self._update_test_configuration(test_id, main_script)

        return {
            "test_id": test_id,
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads,
            "invalid_files": invalid_files,
            "config_update": config_update_result
        }

    async def _upload_single_file(self, test_id: int, file_path: str) -> Dict[str, Any]:
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

            endpoint = f"/tests/{test_id}/files"
            logger.debug(f"Uploading to endpoint: {endpoint}")

            result = await api_request(self.token, "POST", endpoint, files=files)
            logger.debug(f"Upload result: {result}")

            return result

        except Exception as e:
            logger.error(f"Exception in _upload_single_file: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to upload {file_path}: {str(e)}")

    async def _update_test_configuration(self, test_id: int, main_script_path: str) -> Dict[str, Any]:
        try:
            file_name = Path(main_script_path).name

            script_type = self._get_script_type(file_name)

            config_update = {
                "configuration": {
                    "filename": file_name,
                    "scriptType": script_type
                }
            }

            endpoint = f"/tests/{test_id}"
            result = await api_request(
                self.token,
                "PATCH",
                endpoint,
                json=config_update
            )

            return result

        except Exception as e:
            raise Exception(f"Failed to update test configuration: {str(e)}")

    def _get_mime_type(self, file_path: str) -> str:
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

    def _get_script_type(self, file_name: str) -> str:
        extension = Path(file_name).suffix.lower()

        script_types = {
            '.jmx': 'jmeter',
            '.yaml': 'taurus',
            '.yml': 'taurus',
            '.py': 'python',
            '.js': 'javascript'
        }

        return script_types.get(extension, 'unknown')

    async def list(self, account_id: int, workspace_id: int, project_id: int, limit: int = 50,
                   offset: int = 0) -> TestResult:
        parameters = {
            "projectId": project_id,
            "workspaceId": workspace_id,
            "accountId": account_id,
            "limit": limit,
            "skip": offset,
            "sort[]": "-updated"
        }

        tests_response = await api_request(self.token, "GET", "/tests", params=parameters)

        if "error" in tests_response and tests_response["error"]:
            return TestResult(
                error=tests_response.get("error")
            )

        tests = tests_response.get("result", [])
        has_more = tests_response.get("total", 0) - (offset + limit) > 0

        return TestResult(
            result=self.normalize_tests(tests),
            has_more=has_more
        )

    async def configure(self, performance_test: PerformanceTestObject) -> TestResult:
        if not performance_test.is_valid():
            raise ValueError("PerformanceTestObject must have a valid test_id")

        configuration = performance_test.get_configuration()
        configuration_body = {
            "overrideExecutions": [configuration]
        }

        test_response = await api_request(self.token, "PATCH", f"/tests/{performance_test.test_id}",
                                          json=configuration_body)

        if "error" in test_response and test_response["error"]:
            return TestResult(
                error=test_response.get("error")
            )

        tests = [test_response.get("result", None)]
        return TestResult(
            result=self.normalize_tests(tests)
        )

    @staticmethod
    def normalize_tests(tests: List[Any]) -> List[Test]:

        formatted_tests = []
        for test in tests:
            test_element = {
                "test_id": test.get("id"),
                "test_name": test.get("name", "Unknown"),
                "description": test.get("description", ""),
                "created": get_date_time_iso(test.get("created")),
                "updated": get_date_time_iso(test.get("updated")),
                "project_id": test.get("projectId"),
                "status": test.get("status", "Unknown"),
                "type": test.get("type", "Unknown"),
                "configuration": test.get("configuration", {})
            }
            test_object = Test(**test_element)
            formatted_tests.append(test_object)

        return formatted_tests





def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_tests",
        description="""
        Operations on tests.
        Actions:
        - create: Create a new test. Do not create a test if the user has not confirmed the location for validation of workspace, project and account.
            args(dict): Dictionary with the following required parameters:
                test_name (str): The required name of the test to create.
                project_id (int): The id of the project to list tests from.
        - list: List all tests. 
            args(dict): Dictionary with the following required parameters:
                account_id (int): The id of the account to list the tests from
                workspace_id (int): The id of the workspace to list tests from.
                project_id (int): The id of the project to list tests from.
                limit (int, default=50): The number of tests to list.
                offset (int, default=0): Number of tests to skip.
        - configure: Configure a performance test for the given test id. The test id is the only required parameter. 
                     The test will be configured based on the following parameters only if user confirms the configuration:
            args(dict): Dictionary with the following parameters:
                test_id (int): The only required parameter. The id of the test to configure.
                iterations (int, default=1): The number of iterations to run the test with. Not available if hold-for is provided. null if disabled.
                hold-for (str, default=1m): The length of time the test will run at the peak concurrency. Values can be provided in m (minutes) only. Not available if iterations is provided. null if disabled.
                concurrency (int, default=20): The number of concurrent virtual users simulated to run. For example, 20 will set the test to run with 20 concurrent users. Minimum: 1.
                ramp-up (str): The length of time the test will take to ramp-up to full concurrency. Values can be provided in m (minutes) only. Can be empty.
                steps (int, default=1): The number of ramp-up steps. Can be empty.
                executor (str, default=jmeter): The script type you are running. Includes the following options: (gatling,grinder,jmeter,locust,pbench,selenium,siege).
        - upload_assets: Upload main script test as well as multiple related assets to a test. Supports .zip, .csv, .jmx, .yaml and other file types.
            args(dict): Dictionary with the following required parameters:
                test_id (int): The id of the test to upload assets to.
                file_paths (list): List of full file paths to upload.
                main_script (str, optional): Path to the main script file. If provided, will update test configuration to use this script.
        """
    )
    async def tests(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        test_manager = TestManager(token)
        try:
            match action:
                case "create":
                    return await test_manager.create(args["test_name"], args["project_id"])
                case "list":
                    return await test_manager.list(args["account_id"], args["workspace_id"], args["project_id"],
                                                   args.get("limit", 50), args.get("offset", 0))
                case "configure":
                    performance_test = PerformanceTestObject.from_args(args)
                    return await test_manager.configure(performance_test)
                case "upload_assets":
                    return BaseResult(
                        result = [await test_manager.upload_assets(
                        args["test_id"],
                        args["file_paths"],
                        args.get("main_script"))]
                    )
                case _:
                    return TestResult(
                        error=f"Action {action} not found in tests manager tool"
                    )
        except Exception:
            return TestResult(
                error=f"Error: {traceback.format_exc()}"
            )
