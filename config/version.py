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
import os
import subprocess
import sys
import tomllib
from pathlib import Path


def get_version():
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject.exists():
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    return "unknown"


def get_executable():
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.join(os.path.abspath(Path(__file__).parent.parent), "main.py")


def get_bundle_executable():
    executable_path = os.path.realpath(get_executable())
    if sys.platform == "darwin":
        translocated_path = executable_path
        result = subprocess.check_output(
            ['/usr/bin/security', 'translocate-original-path', translocated_path],
            stderr=subprocess.STDOUT
        )
        original_path = result.decode('utf-8').split('\n')[-2].strip()

        return os.path.realpath(os.path.join(original_path, "..", "..", ".."))
    else:
        return executable_path

__version__ = get_version()
__executable__ = get_executable()
__bundle__ = get_bundle_executable()
