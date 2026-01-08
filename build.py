#!/usr/bin/env python3
"""Build script for creating PyInstaller binary."""
import os
import platform
import shutil
import subprocess
import tomllib
from datetime import date
from pathlib import Path

import PyInstaller.__main__

sep = os.pathsep


def clean_build():
    build_dir = Path('build')
    if build_dir.exists():
        shutil.rmtree(build_dir)


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


def normalize_architecture(arch: str) -> str:
    if arch in ['x86_64', 'amd64']:
        return 'amd64'
    elif arch in ['aarch64', 'arm64']:
        return 'arm64'
    elif arch.startswith('arm'):
        return 'arm64'
    return arch


def normalize_system_name(system: str) -> str:
    return "macos" if system == 'darwin' else system


def get_binary_name(system: str, arch: str) -> str:
    suffix = '.exe' if system == 'windows' else ''
    return f'bzm-mcp-{system}-{arch}{suffix}'


def get_icon_file(system: str) -> str:
    return 'app.icns' if system == 'macos' else 'app.ico'


def run_pyinstaller(name: str, icon: str):
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--version-file=version_info.txt',
        f'--add-data=pyproject.toml{sep}.',
        f'--add-data=resources{sep}resources',
        f'--name={name}',
        f'--icon={icon}',
        '--clean',
        '--noconfirm',
    ])


def build():
    clean_build()

    system = normalize_system_name(platform.system().lower())
    arch = normalize_architecture(platform.machine().lower())
    name = get_binary_name(system, arch)
    icon = get_icon_file(system)

    run_pyinstaller(name, icon)
    clean_build()
    
    if system == "macos":
        create_app_bundle(name, arch, dist_dir=Path("dist"))
    elif system == "linux":
        create_sha256_checksum(name, dist_dir=Path("dist"))


def create_app_directory_structure(app_path: Path) -> Path:
    macos_path = app_path / "Contents" / "MacOS"
    macos_path.mkdir(parents=True, exist_ok=True)
    return macos_path


def copy_binary_to_app(binary_path: Path, target_path: Path):
    if not binary_path.exists():
        raise FileNotFoundError(f"Binary not found: {binary_path}")
    shutil.copy2(binary_path, target_path)
    os.chmod(target_path, 0o755)


def create_launcher_script(launcher_path: Path):
    launcher_content = """#!/bin/bash
set -e

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN="$BIN_DIR/bzm-mcp"

if [ -t 1 ]; then
  exec "$BIN" "$@"
else
  open -a Terminal "$BIN"
fi
"""
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_content)
    os.chmod(launcher_path, 0o755)


def create_info_plist(plist_path: Path):
    info_plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>launcher.sh</string>

  <key>CFBundleIdentifier</key>
  <string>com.blazemeter.mcp</string>

  <key>CFBundleName</key>
  <string>BlazeMeter MCP</string>

  <key>CFBundlePackageType</key>
  <string>APPL</string>
</dict>
</plist>
"""
    with open(plist_path, "w", encoding="utf-8") as f:
        f.write(info_plist_content)


def create_app_bundle(binary_name: str, arch: str, dist_dir: Path):
    app_name = f"bzm-mcp-{arch}.app"
    app_path = dist_dir / app_name
    contents_path = app_path / "Contents"

    macos_path = create_app_directory_structure(app_path)

    binary_path = dist_dir / binary_name
    copy_binary_to_app(binary_path, macos_path / "bzm-mcp")

    create_launcher_script(macos_path / "launcher.sh")
    create_info_plist(contents_path / "Info.plist")

    binary_path.unlink()
    print(f"Created {app_name} in {dist_dir}")


def create_sha256_checksum(binary_name: str, dist_dir: Path):
    binary_path = dist_dir / binary_name
    checksum_path = dist_dir / f"{binary_name}.sha256"
    
    if not binary_path.exists():
        raise FileNotFoundError(f"Binary not found: {binary_path}")
    
    with open(checksum_path, "w") as f:
        subprocess.run(
            ["sha256sum", binary_name],
            cwd=dist_dir,
            stdout=f,
            check=True,
        )
    
    print(f"Created {checksum_path.name} in {dist_dir}")


if __name__ == "__main__":
    build_version_file()
    build()
