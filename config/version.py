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
