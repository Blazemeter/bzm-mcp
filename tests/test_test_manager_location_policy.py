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

from tools.test_manager import TestManager


class TestTestManagerLocationNormalizationPolicy:
    def test_only_first_zero_location_is_normalized_to_one(self):
        override = {
            "concurrency": 1,
            "locationsPercents": {
                "us-east4-a": 25,
                "us-east1-b": 25,
                "us-west1-a": 25,
                "us-central1-a": 25,
            }
        }

        normalized = TestManager._normalize_configuration_override(override, override.copy())
        locations = normalized["locations"]

        assert locations["us-east4-a"] == 1
        assert locations["us-east1-b"] == 0
        assert locations["us-west1-a"] == 0
        assert locations["us-central1-a"] == 0

    def test_other_zero_locations_are_not_normalized_when_first_is_non_zero(self):
        override = {
            "concurrency": 4,
            "locationsPercents": {
                "us-east4-a": 100,
                "us-east1-b": 0,
                "us-west1-a": 0,
            }
        }

        normalized = TestManager._normalize_configuration_override(override, override.copy())
        locations = normalized["locations"]

        assert locations["us-east4-a"] == 4
        assert locations["us-east1-b"] == 0
        assert locations["us-west1-a"] == 0
