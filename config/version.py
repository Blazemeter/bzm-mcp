import tomllib
from pathlib import Path

def get_version():
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject.exists():
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    return "unknown"

__version__ = get_version()
