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
                configuration=test.get("configuration", {})
            )
        )
    return formatted_tests
