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
        dist_dir = Path("dist")
        binary_path = dist_dir / name
        
        # Buscar archivo de entitlements en ubicaciones comunes
        entitlements = Path("/Users/abstracta/dist/arm/entitlements.plist")
        
        # Paso 1: Firmar el binario
        sign_binary(binary_path, entitlements=entitlements)
        
        # Paso 2: Comprimir el binario en bzm-mcp.zip
        binary_zip_path = dist_dir / "bzm-mcp.zip"
        create_zip(binary_path, binary_zip_path)
        
        # Paso 3: Notarizar el .zip del binario
        notarize_zip(binary_zip_path)
        
        # Paso 4: Crear el .app (ya estaba automatizado)
        app_name = f"bzm-mcp-{arch}.app"
        create_app_bundle(name, arch, dist_dir)
        
        # Firmar el .app bundle completo
        app_path = dist_dir / app_name
        sign_binary(app_path, entitlements=entitlements)
        
        # Paso 5: Comprimir el .app en un .zip
        app_zip_path = dist_dir / f"{app_name}.zip"
        create_zip(app_path, app_zip_path)
        
        # Paso 6: Notarizar el .zip del .app
        notarize_zip(app_zip_path)
        
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


def sign_binary(binary_path: Path, identity: str = None, entitlements: Path = None):
    """Firma un binario usando codesign.
    
    La identidad puede proporcionarse como parámetro o mediante variable de entorno:
    - CODESIGN_IDENTITY: Identidad completa (ej: "Developer ID Application: Your Name (TEAM_ID)")
    
    Si no se proporciona, usará la identidad predeterminada del keychain.
    """
    if not binary_path.exists():
        raise FileNotFoundError(f"Binary not found: {binary_path}")
    
    # Obtener identidad de variable de entorno si no se proporciona como parámetro
    identity = identity or os.getenv("CODESIGN_IDENTITY", "-")
    
    # Construir el comando de firma (mismo orden que el comando manual)
    cmd = ["codesign", "--sign", identity]
    
    # Agregar entitlements si se proporciona y existe
    if entitlements and entitlements.exists():
        cmd.extend(["--entitlements", str(entitlements)])
    
    # Agregar opciones de hardened runtime y timestamp (misma sintaxis que comando manual)
    cmd.extend(["--options", "runtime", "--timestamp"])
    
    # Agregar force y verbose
    cmd.extend(["--force", "--verbose"])
    
    # Si es un .app bundle, usar --deep para firmar recursivamente
    if str(binary_path).endswith(".app"):
        cmd.append("--deep")
    
    cmd.append(str(binary_path))
    
    print(f"Signing {binary_path.name}...")
    subprocess.run(cmd, check=True)
    print(f"Successfully signed {binary_path.name}")


def create_zip(source_path: Path, zip_path: Path):
    """Comprime un archivo o directorio en un .zip."""
    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source_path}")
    
    # Asegurar que el directorio padre del zip existe
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating {zip_path.name}...")
    # Si el zip está en el mismo directorio que el source, usar nombre relativo
    if source_path.parent == zip_path.parent:
        subprocess.run(
            ["zip", "-r", zip_path.name, source_path.name],
            cwd=source_path.parent,
            check=True,
        )
    else:
        # Si están en directorios diferentes, usar rutas absolutas
        subprocess.run(
            ["zip", "-r", str(zip_path), str(source_path)],
            check=True,
        )
    print(f"Successfully created {zip_path.name}")


def notarize_zip(zip_path: Path, apple_id: str = None, team_id: str = None, password: str = None, keychain_profile: str = None):
    """Notariza un archivo .zip usando xcrun notarytool.
    
    Las credenciales pueden proporcionarse como parámetros o mediante variables de entorno:
    - APPLE_ID: Apple ID para notarización
    - APPLE_TEAM_ID: Team ID (opcional)
    - APPLE_PASSWORD: Contraseña de aplicación (opcional, solo si no se usa keychain profile)
    - APPLE_KEYCHAIN_PROFILE: Nombre del perfil del keychain (opcional)
    """
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")
    
    print(f"Notarizing {zip_path.name}...")
    
    # Obtener credenciales de variables de entorno si no se proporcionan como parámetros
    apple_id = apple_id or os.getenv("APPLE_ID")
    team_id = team_id or os.getenv("APPLE_TEAM_ID")
    password = password or os.getenv("APPLE_PASSWORD")
    keychain_profile = keychain_profile or os.getenv("APPLE_KEYCHAIN_PROFILE")
    
    # Construir el comando de notarización
    cmd = ["xcrun", "notarytool", "submit", str(zip_path)]
    
    # Si se proporcionan credenciales explícitas, usarlas
    if apple_id and password:
        cmd.extend(["--apple-id", apple_id])
        if team_id:
            cmd.extend(["--team-id", team_id])
        cmd.extend(["--password", password])
        cmd.append("--wait")
    elif keychain_profile:
        # Usar el perfil del keychain especificado
        cmd.extend(["--keychain-profile", keychain_profile])
        cmd.append("--wait")
    else:
        # Intentar detectar perfiles disponibles
        try:
            result = subprocess.run(
                ["xcrun", "notarytool", "store-credentials", "--list"],
                capture_output=True,
                text=True,
                check=True
            )
            profiles = [line.strip() for line in result.stdout.split('\n') if line.strip() and not line.startswith('Profile')]
            if profiles:
                # Usar el primer perfil disponible
                profile = profiles[0].split()[0] if profiles else None
                if profile:
                    print(f"Using keychain profile: {profile}")
                    cmd.extend(["--keychain-profile", profile])
                    cmd.append("--wait")
                else:
                    print("Warning: No keychain profiles found. Skipping notarization.")
                    print("To set up notarization, run: xcrun notarytool store-credentials <profile-name>")
                    return
            else:
                print("Warning: No keychain profiles found. Skipping notarization.")
                print("To set up notarization, run: xcrun notarytool store-credentials <profile-name>")
                return
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Could not detect keychain profiles. Skipping notarization.")
            print("To set up notarization, run: xcrun notarytool store-credentials <profile-name>")
            return
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Successfully notarized {zip_path.name}")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Notarization may have failed for {zip_path.name}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        # No fallar el build si la notarización falla (puede requerir configuración manual)
        print("Continuing build process...")


if __name__ == "__main__":
    build_version_file()
    build()
