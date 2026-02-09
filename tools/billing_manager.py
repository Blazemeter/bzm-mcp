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

from config.blazemeter import TOOLS_PREFIX, SUPPORT_MESSAGE
from config.token import BzmToken
from models.manager import Manager
from models.result import BaseResult
from tools.billing_utils import calculate_test_cost


class BillingManager(Manager):

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    async def calculate_cost_from_config(self, args: Dict) -> BaseResult:
        result = calculate_test_cost(args)
        return BaseResult(result=[
            {
                "cost": result,
                "context": ""
                           "- IMPORTANT! The 'amount' value within the 'allowance' of a Workspace is how much credit is available. "
                           "You can determine whether the calculated usage can be executed if it does not exceed"
                           " the available credit."
                           ""
            }
        ])


def register(mcp, token: Optional[BzmToken]) -> None:
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_billing",
        description="""
Operations on Billing.
Actions: 
- calculate_cost_from_config: Calculate the cost of a test based on test configuration and workspace allowance type.
    args(dict): Dictionary with the following parameters:
        allowance_type (str, required, valid=["credits", "virtualUserHours", "actualThreads", "serverHours", "functionalRequests"]): The workspace allowance.
        test_type (str, required, default="performance", valid=["performance", "browser_performance", "gui_functional", "api_monitoring", "service_virtualization"]): Type of test.
        concurrency (int, required for performance/browser_performance): Maximum concurrent virtual users/threads.
        duration_minutes (float, required for performance/browser_performance/gui_functional): Test duration in minutes.
        iterations (int, optional, alternative to duration_minutes): Number of iterations.
        browser_sessions (int, required for gui_functional): Number of browser sessions.
        api_calls (int, required for api_monitoring): Number of API calls.
        virtual_services (int, required for service_virtualization): Number of virtual services.
        transactions (int, optional, for service_virtualization): Number of transactions.
        locations (list[str], optional): List of location IDs for load distribution.
        uses_test_data (bool, optional, default=False): Whether test uses BlazeMeter Test Data (adds 50% to cost).
        number_of_servers (int, optional, for serverHours calculation): Number of engines/servers. If not provided, estimated based on concurrency (~1000 users per engine).
    Hints:
    - The workspace allowance type is automatically determined from the workspace (via 'read' action).
    - Supported allowance types: "credits", "virtualUserHours", "actualThreads", "serverHours", "functionalRequests".
    - Allowance type details:
      * credits: Tests as Credit (1 credit per test).
      * virtualUserHours: Variable Unit Hours (VUH) as Credit, formerly known as Virtual User Hour.
      * actualThreads: Variable Unit (VU) as Credit - Maximum concurrent threads/units reached (peak concurrency).
      * serverHours: Number of Server Hours - Server/engine hours consumed (engines × duration in hours).
      * functionalRequests: API Functional Tests - Number of API Calls - One unit per API call.
    - The 'amount' value within the 'allowance' of a Workspace is how much credit is available. 
    - For Performance/Browser Performance tests: provide concurrency and duration_minutes.
    - For GUI Functional tests: provide browser_sessions and duration_minutes.
    - For API Monitoring tests: provide api_calls.
    - For Service Virtualization tests: provide virtual_services and optionally transactions.
    - Test Data usage increases cost by 50% for all test types.
    - Server hours calculation can use provided number_of_servers or estimate based on concurrency (~1000 users per engine).
    - All calculations are based on official BlazeMeter documentation (blazemeter-usage-billing skill).
    """
    )
    async def billing(action: str, args: Dict[str, Any], ctx: Context) -> BaseResult:
        billing_manager = BillingManager(token, ctx)
        try:
            match action:
                case "calculate_cost_from_config":
                    return await billing_manager.calculate_cost_from_config(args)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in billing manager tool"
                    )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}\n{SUPPORT_MESSAGE}"
            )
