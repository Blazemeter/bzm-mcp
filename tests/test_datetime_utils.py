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

from tools.utils import get_date_time_iso


class TestDateTimeIsoTimezone:
    def test_returns_none_for_none_timestamp(self):
        assert get_date_time_iso(None) is None

    def test_returns_utc_timezone_for_unix_epoch(self):
        assert get_date_time_iso(0) == "1970-01-01T00:00:00+00:00"

    def test_returns_utc_timezone_for_known_timestamp(self):
        assert get_date_time_iso(1710000000) == "2024-03-09T16:00:00+00:00"
