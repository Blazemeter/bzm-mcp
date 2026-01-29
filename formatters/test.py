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
from typing import List, Any, Optional

from models.test import Test
from tools.utils import get_date_time_iso


def format_tests(tests: List[Any], params: Optional[dict] = None) -> List[Test]:
    formatted_tests = []
    for test in tests:
        formatted_tests.append(
            Test(
                test_id=test.get("id"),
                test_name=test.get("name", "Unknown"),
                description=test.get("description", ""),
                created=get_date_time_iso(test.get("created")),
                updated=get_date_time_iso(test.get("updated")),
                project_id=test.get("projectId"),
                configuration=test.get("configuration", {}),
                override_executions=test.get("overrideExecutions", [])
            )
        )
    return formatted_tests
