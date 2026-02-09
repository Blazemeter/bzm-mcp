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
from typing import Any, Dict


class PerformanceTestObject:
    """ 'Factory' class for creating BlazeMeter test objects."""

    def __init__(self, test_data: Dict[str, Any]):
        self.test_id = test_data.get("test_id")
        self.override_execution = self._extract_override_execution(test_data)

    @staticmethod
    def safe_float(value):
        try:
            return float(value)
        except ValueError:
            return None

    @classmethod
    def from_args(cls, args: Dict[str, Any]) -> 'PerformanceTestObject':
        return cls(args)

    @staticmethod
    def _extract_override_execution(test_data: Dict[str, Any], concurrency: int = 1) -> Dict[str, Any]:
        execution_config = {}
        for param in ["iterations", "concurrency", "hold-for", "ramp-up", "steps", "executor", "locations"]:
            if param in test_data:
                match param:
                    case "ramp-up":
                        execution_config["rampUp"] = test_data[param]
                    case "hold-for":
                        execution_config["holdFor"] = test_data[param]
                    case "locations":
                        locations_percents = {}
                        for location in test_data[param]:
                            location_kv = location.split("=")
                            location_percent = PerformanceTestObject.safe_float(location_kv[1])
                            if location_percent:
                                locations_percents[location_kv[0]] = location_percent
                        execution_config["locationsPercents"] = locations_percents
                    case _:
                        execution_config[param] = test_data[param]
        return execution_config

    def get_configuration(self) -> Dict[str, Any]:
        return self.override_execution

    def is_valid(self) -> bool:
        return self.test_id is not None
