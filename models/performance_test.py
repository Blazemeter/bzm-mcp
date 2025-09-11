from typing import Any, Dict


class PerformanceTestObject:
    """ 'Factory' class for creating BlazeMeter test objects."""

    def __init__(self, test_data: Dict[str, Any]):
        self.test_id = test_data.get("test_id")
        self.override_execution = self._extract_override_execution(test_data)

    @classmethod
    def from_args(cls, args: Dict[str, Any]) -> 'PerformanceTestObject':
        return cls(args)

    @staticmethod
    def _extract_override_execution(test_data: Dict[str, Any]) -> Dict[str, Any]:
        execution_config = {}
        for param in ["iterations", "concurrency", "hold-for", "ramp-up", "steps", "executor"]:
            if param in test_data:
                match param:
                    case "ramp-up":
                        execution_config["rampUp"] = test_data[param]
                    case "hold-for":
                        execution_config["holdFor"] = test_data[param]
                    case _:
                        execution_config[param] = test_data[param]
        return execution_config

    def get_configuration(self) -> Dict[str, Any]:
        return self.override_execution

    def is_valid(self) -> bool:
        return self.test_id is not None
