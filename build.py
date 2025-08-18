#!/usr/bin/env python3
"""Build script for creating PyInstaller binary."""

import PyInstaller.__main__
import sys
import platform
from pathlib import Path

def build():
    """Build the binary using PyInstaller."""
    suffix = '.exe' if platform.system() == 'Windows' else ''
    name = f'bzm-mcp-{platform.system().lower()}{suffix}'
    
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        f'--name={name}',
        '--clean',
        '--noconfirm',
    ])

if __name__ == "__main__":
    build()
