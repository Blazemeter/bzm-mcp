import traceback
from typing import Optional, Dict, Any

from config.blazemeter import BZM_BASE_URL
from config.token import BzmToken
from tools.base import api_request


class TestExecutionManager:

    def __init__(self, token: Optional[BzmToken]):
        self.token = token

    async def start(self, test_id: int, delayed_start_ready: bool = True, is_debug_run: bool = False) -> dict[str, any]:
        parameters = {
            "delayedStart": delayed_start_ready
        }
        start_body = {
            "isDebugRun": is_debug_run,
        }
        start_response = await api_request(self.token, "POST", f"/tests/{test_id}/start", params=parameters,
                                           json=start_body)

        result = start_response.get("result", {})

        if "id" in result:
            master_id = result.get("id")
            return {
                "master_id": master_id,
                "execution_url": f"{BZM_BASE_URL}/app/#/masters/{master_id}"
            }
        else:
            return {"error": start_response.get("error")}


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name="bzm_mcp_test_execution_tool",
        description="""
        Operations on tests.
        Actions:
        - start: start a preconfigured load test, you need to know the testId of a created and configured test.
            args(dict): Dictionary with the following required parameters:
                test_id (int): The test Id that should be started.
        """
    )
    async def bzm_mcp_test_execution_tool(action: str, args: Dict[str, Any]) -> Dict[str, Any]:
        test_manager = TestExecutionManager(token)
        try:
            match action:
                case "start":
                    return await test_manager.start(args["test_id"])
                case _:
                    return {"result": f"Action {action} not found in tests manager tool"}
        except Exception as e:
            return {"result": f"Error: {traceback.format_exc()}"}
