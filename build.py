#!/usr/bin/env python3
"""Build script for creating PyInstaller binary."""

import platform

import PyInstaller.__main__


def build():
    """Build the binary using PyInstaller."""
    suffix = '.exe' if platform.system() == 'Windows' else ''
    arch = platform.machine().lower()
    
    # Map architecture names to Docker-compatible format
    if arch in ['x86_64', 'amd64']:
        arch = 'amd64'
    elif arch in ['aarch64', 'arm64']:
        arch = 'arm64'
    elif arch.startswith('arm'):
        arch = 'arm64'  # Assume ARM64 for Docker compatibility
    
    # For Docker builds, we want Linux binaries with architecture
    system = platform.system().lower()
    if system == 'linux':
        name = f'bzm-mcp-linux-{arch}'
    else:
        name = f'bzm-mcp-{system}{suffix}'
    
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        f'--name={name}',
        '--clean',
        '--noconfirm',
    ])


if __name__ == "__main__":
    build()
