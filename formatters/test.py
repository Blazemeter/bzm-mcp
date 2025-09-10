from typing import List, Any

from models.test import Test
from tools.utils import get_date_time_iso


def format_tests(tests: List[Any]) -> List[Test]:
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
        formatted_tests.append(Test(**test_element))

    return formatted_tests
