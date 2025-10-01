#!/usr/bin/env python3
"""Build script for creating PyInstaller binary."""
import os
import platform
import tomllib
from datetime import date
from pathlib import Path

import PyInstaller.__main__

sep = os.pathsep

def build_version_file():
    pyproject = Path(__file__).parent / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)

    version = data["project"]["version"]
    name = data["project"]["name"]
    description = data["project"]["description"]

    nums = tuple(int(x) for x in version.split(".")) + (0,) * (4 - len(version.split(".")))

    TEMPLATE = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={nums},
    prodvers={nums},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'BlazeMeter'),
        StringStruct('FileDescription', '{description}'),
        StringStruct('FileVersion', '{version}'),
        StringStruct('InternalName', '{name}'),
        StringStruct('LegalCopyright', '© {date.today().year} BlazeMeter'),
        StringStruct('OriginalFilename', '{name}.exe'),
        StringStruct('ProductName', 'BlazeMeter MCP'),
        StringStruct('ProductVersion', '{version}')])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""

    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(TEMPLATE.strip())


def build():
    """Build the binary using PyInstaller."""
    system = platform.system().lower()
    suffix = '.exe' if system == 'windows' else ''
    arch = platform.machine().lower()

    # Map architecture names to Docker-compatible format
    if arch in ['x86_64', 'amd64']:
        arch = 'amd64'
    elif arch in ['aarch64', 'arm64']:
        arch = 'arm64'
    elif arch.startswith('arm'):
        arch = 'arm64'  # Assume ARM64 for Docker compatibility

    system = "macos" if system == 'darwin' else system
    name = f'bzm-mcp-{system}-{arch}{suffix}'

    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--version-file=version_info.txt',
        f'--add-data=pyproject.toml{sep}.',
        f'--name={name}',
        '--icon=app.ico',
        '--clean',
        '--noconfirm',
    ])


if __name__ == "__main__":
    build_version_file()
    build()
