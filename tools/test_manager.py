import traceback
from .base import api_request
from typing import Optional
from config.token import BzmToken
from typing import Any, Dict
from models.performance_test import PerformanceTestObject

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
    
    async def configure(self, performance_test: PerformanceTestObject): 
        if not performance_test.is_valid():
            raise ValueError("PerformanceTestObject must have a valid test_id")
        
        configuration = performance_test.get_configuration()
        configuration_body = {
            "overrideExecutions": [configuration]
        }
        
        response = await api_request(self.token, "PATCH", f"/tests/{performance_test.test_id}", json=configuration_body)
        return response
    

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
                case "configure":
                    performance_test = PerformanceTestObject.from_args(args)
                    return await test_manager.configure(performance_test)
                case _:
                    return {"result": f"Action {action} not found in tests manager tool"}
        except Exception as e:
            return {"result": f"Error: {traceback.format_exc()}"}
