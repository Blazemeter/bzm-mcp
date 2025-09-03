import traceback
import os
import asyncio
from pathlib import Path
from .base import api_request
from typing import Optional, List
from config.token import BzmToken
from typing import Any, Dict
import httpx

class TestManager:

    def __init__(self,token: Optional[BzmToken]):
        self.tests = []
        self.token = token

    async def create(self, test_name: str, project_id: int):
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
        return await api_request(self.token, "POST", "/tests", json=test_body)

    async def upload_assets(self, test_id: int, file_paths: List[str], main_script: Optional[str] = None) -> Dict[str, Any]:
  
        valid_files = []
        invalid_files = []
        
        for file_path in file_paths:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                valid_files.append(file_path)
            else:
                invalid_files.append(file_path)
        
        if not valid_files:
            return {
                "error": "No valid files found to upload",
                "invalid_files": invalid_files
            }
        
        upload_tasks = [self._upload_single_file(test_id, file_path) for file_path in valid_files]
        upload_results = await asyncio.gather(*upload_tasks, return_exceptions=True)
        
        successful_uploads = []
        failed_uploads = []
        
        for i, result in enumerate(upload_results):
            if isinstance(result, Exception):
                failed_uploads.append({
                    "file": valid_files[i],
                    "error": str(result)
                })
            else:
                successful_uploads.append({
                    "file": valid_files[i],
                    "result": result
                })
        
        config_update_result = None
        if main_script and main_script in valid_files:
            config_update_result = await self._update_test_configuration(test_id, main_script)
        
        return {
            "test_id": test_id,
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads,
            "invalid_files": invalid_files,
            "config_update": config_update_result
        }
    
    async def _upload_single_file(self, test_id: int, file_path: str) -> Dict[str, Any]:
        try:
            file_path_obj = Path(file_path)
            file_name = file_path_obj.name
            
            # Read file content
            with open(file_path, 'rb') as file:
                file_content = file.read()
            
            files = {
                'file': (file_name, file_content, self._get_mime_type(file_path))
            }
            
            endpoint = f"/tests/{test_id}/files"
            result = await api_request(
                self.token, 
                "POST", 
                endpoint, 
                files=files
            )
            
            return result
            
        except Exception as e:
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
        """
        Get MIME type based on file extension.
        
        Args:
            file_path: Path to the file
        
        Returns:
            MIME type string
        """
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

    async def list(self, account_id: int, workspace_id: int, project_id: int, limit: int = 50, offset: int = 0):
        parameters = {
            "projectId": project_id,
            "workspaceId": workspace_id,
            "accountId": account_id,
            "limit": limit,
            "skip": offset
        }

        tests_response = await api_request(self.token, "GET", f"/tests", params=parameters)
        tests = tests_response.get("result", [])
        has_more = tests_response.get("total", 0) - (offset + limit) > 0

        return {
            "tests": self.normalize_tests(tests),
            "has_more": has_more
        }
    
    def normalize_tests(self, tests) -> Dict[str, Any]:
        
        formatted_tests = []
        for test in tests:
            formatted_test = {
                "id": test.get("id"),
                "name": test.get("name", "Unknown"),
                "description": test.get("description", ""),
                "created": test.get("created"),
                "updated": test.get("updated"),
                "projectId": test.get("projectId"),
                "status": test.get("status", "Unknown"),
                "type": test.get("type", "Unknown"),
                "configuration": test.get("configuration", {})
            }
            formatted_tests.append(formatted_test)
        
        return formatted_tests


def register(mcp, token: Optional[BzmToken]):

    @mcp.tool(
        name="bzm_mcp_tests_tool",
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
        - upload_assets: Upload multiple assets to a test. Supports .zip, .csv, .jmx, .yaml and other file types.
            args(dict): Dictionary with the following required parameters:
                test_id (int): The id of the test to upload assets to.
                file_paths (list): List of full file paths to upload.
                main_script (str, optional): Path to the main script file. If provided, will update test configuration to use this script.
        """
    )
    async def bzm_mcp_tests_tool(action: str, args: Dict[str, Any]) -> Dict[str, Any]:
        test_manager = TestManager(token)
        try:
            match action:
                case "create": 
                    return await test_manager.create(args["test_name"], args["project_id"])
                case "list":
                    return await test_manager.list(args["account_id"], args["workspace_id"], args["project_id"], args["limit"], args["offset"])
                case "upload_assets":
                    return await test_manager.upload_assets(
                        args["test_id"], 
                        args["file_paths"], 
                        args.get("main_script")
                    )
                case _:
                    return {"result": f"Action {action} not found in tests manager tool"}
        except Exception as e:
            return {"result": f"Error: {traceback.format_exc()}"}
