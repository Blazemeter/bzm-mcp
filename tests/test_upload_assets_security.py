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

from pathlib import Path

from tools.test_manager import TestManager as UploadAssetsManager


class TestUploadAssetsSensitivePathDetection:
    def test_detects_sensitive_system_prefixes(self):
        assert UploadAssetsManager._detect_sensitive_path_reason("/etc/passwd") is not None
        assert UploadAssetsManager._detect_sensitive_path_reason(r"C:\Windows\System32\config\SAM") is not None
        assert UploadAssetsManager._detect_sensitive_path_reason(r"D:\Windows\System32\config\SAM") is not None

    def test_detects_sensitive_user_secret_directories(self):
        assert UploadAssetsManager._detect_sensitive_path_reason("/home/user/.ssh/id_rsa") is not None
        assert UploadAssetsManager._detect_sensitive_path_reason(r"C:\Users\john\.aws\credentials") is not None
        assert UploadAssetsManager._detect_sensitive_path_reason(r"C:\Users\john\.azure\azureProfile.json") is not None

    def test_detects_sensitive_file_name_and_extensions(self):
        assert UploadAssetsManager._detect_sensitive_path_reason("/workspace/.env") is not None
        assert UploadAssetsManager._detect_sensitive_path_reason("/workspace/certificates/server.key") is not None
        assert UploadAssetsManager._detect_sensitive_path_reason("/workspace/.netrc") is not None
        assert UploadAssetsManager._detect_sensitive_path_reason("/workspace/env/terraform.tfstate") is not None

    def test_allows_regular_test_assets(self):
        assert UploadAssetsManager._detect_sensitive_path_reason("/workspace/tests/demo.jmx") is None
        assert UploadAssetsManager._detect_sensitive_path_reason("/workspace/data/input.csv") is None
        assert UploadAssetsManager._detect_sensitive_path_reason("relative/path/archive.zip") is None


class TestUploadAssetsFileValidation:
    def test_validate_files_classifies_valid_invalid_and_blocked(self, tmp_path):
        safe_file = tmp_path / "test.jmx"
        safe_file.write_text("content", encoding="utf-8")

        env_file = tmp_path / ".env"
        env_file.write_text("SECRET=value", encoding="utf-8")

        missing_file = tmp_path / "missing.csv"

        valid_files = []
        invalid_files = []
        blocked_files = []

        UploadAssetsManager._validate_files(
            [str(safe_file), str(env_file), str(missing_file)],
            valid_files,
            invalid_files,
            blocked_files,
        )

        assert valid_files == [str(safe_file)]
        assert invalid_files == [str(missing_file)]
        assert len(blocked_files) == 1
        assert blocked_files[0]["file"] == str(env_file)
        assert "sensitive" in blocked_files[0]["reason"]
