#!/usr/bin/env python3
"""Script para firmar y notarizar binarios o .app desde un archivo .zip."""
import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
import zipfile


def find_developer_id():
    """Busca un Developer ID Application certificate en el keychain."""
    try:
        result = subprocess.run(
            ["security", "find-identity", "-v", "-p", "codesigning"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.split('\n'):
            if 'Developer ID Application' in line:
                # El formato es: "   1) ABC123... \"Developer ID Application: Name (TEAM_ID)\""
                # Buscar el contenido completo entre comillas que contiene "Developer ID Application"
                identity_match = re.search(r'"([^"]*Developer ID Application[^"]*)"', line)
                if identity_match:
                    # group(1) contiene el texto dentro de las comillas
                    return identity_match.group(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return None


def sign_binary(binary_path: Path, identity: str = None, entitlements: Path = None):
    """Firma un binario usando codesign.
    
    La identidad puede proporcionarse como parámetro o mediante variable de entorno:
    - CODESIGN_IDENTITY: Identidad completa (ej: "Developer ID Application: Your Name (TEAM_ID)")
    
    Si no se proporciona, intentará encontrar un Developer ID Application en el keychain.
    Si no se encuentra, usará la identidad predeterminada del keychain.
    """
    if not binary_path.exists():
        raise FileNotFoundError(f"Binary not found: {binary_path}")
    
    # Obtener identidad de variable de entorno si no se proporciona como parámetro
    identity = identity or os.getenv("CODESIGN_IDENTITY")
    
    # Si aún no hay identidad, intentar encontrar un Developer ID
    if not identity:
        developer_id = find_developer_id()
        if developer_id:
            print(f"Using Developer ID: {developer_id}")
            identity = developer_id
        else:
            print("Warning: No Developer ID found. Using default keychain identity.")
            identity = "-"
    
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
    # Siempre trabajar desde el directorio del source para evitar incluir rutas completas
    # Esto asegura que el zip solo contenga el nombre del archivo/directorio sin la ruta completa
    source_name = source_path.name
    source_parent = source_path.parent
    
    # Cambiar al directorio del source y crear el zip con nombre relativo
    subprocess.run(
        ["zip", "-r", str(zip_path), source_name],
        cwd=source_parent,
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
    
    Returns:
        bool: True si la notarización fue exitosa, False en caso contrario
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
        # Usar el perfil por defecto "bzm-mcp-notary" directamente
        default_profile = "bzm-mcp-notary"
        print(f"Using keychain profile: {default_profile}")
        cmd.extend(["--keychain-profile", default_profile])
        cmd.append("--wait")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        output = result.stdout or ""
        
        # Verificar el estado de la notarización en la salida
        if "status: Accepted" in output or '"status":"Accepted"' in output:
            print(f"Successfully notarized {zip_path.name}")
            if result.stdout:
                print(result.stdout)
            return True
        elif "status: Invalid" in output or '"status":"Invalid"' in output:
            print(f"Error: Notarization failed for {zip_path.name} - Status: Invalid")
            if result.stdout:
                print(result.stdout)
            # Intentar obtener más información sobre el error
            if "id:" in output:
                id_match = re.search(r'id:\s*([a-f0-9-]+)', output)
                if id_match:
                    submission_id = id_match.group(1)
                    print(f"\nFetching notarization log for submission {submission_id}...")
                    try:
                        log_cmd = ["xcrun", "notarytool", "log", submission_id]
                        if keychain_profile or os.getenv("APPLE_KEYCHAIN_PROFILE"):
                            profile = keychain_profile or os.getenv("APPLE_KEYCHAIN_PROFILE")
                            log_cmd.extend(["--keychain-profile", profile])
                        else:
                            log_cmd.extend(["--keychain-profile", "bzm-mcp-notary"])
                        log_result = subprocess.run(log_cmd, capture_output=True, text=True, check=True)
                        if log_result.stdout:
                            print("Notarization log:")
                            print(log_result.stdout)
                    except subprocess.CalledProcessError:
                        print("Could not fetch notarization log. Check Apple Developer portal for details.")
            return False
        else:
            # Si no podemos determinar el estado, asumir éxito si el comando terminó sin error
            print(f"Notarization completed for {zip_path.name} (status unclear)")
            if result.stdout:
                print(result.stdout)
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Notarization failed for {zip_path.name}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False


def staple_app(app_path: Path):
    """Engrapa (staple) el ticket de notarización a un .app bundle.
    
    Args:
        app_path: Ruta al .app bundle a engrapar
        
    Returns:
        bool: True si el staple fue exitoso, False en caso contrario
    """
    if not app_path.exists():
        raise FileNotFoundError(f"App bundle not found: {app_path}")
    
    if not app_path.suffix == ".app":
        raise ValueError(f"Path is not an .app bundle: {app_path}")
    
    print(f"Stapling {app_path.name}...")
    
    try:
        cmd = ["xcrun", "stapler", "staple", str(app_path)]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Successfully stapled {app_path.name}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to staple {app_path.name}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False


def download_file(url: str, dest_path: Path):
    """Descarga un archivo desde una URL."""
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Downloaded to {dest_path}")


def extract_zip(zip_path: Path, extract_dir: Path):
    """Extrae un archivo .zip a un directorio."""
    print(f"Extracting {zip_path.name} to {extract_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        # Restaurar permisos de ejecución para binarios después de extraer
        for member in zip_ref.infolist():
            # Buscar binarios ejecutables (bzm-mcp)
            if 'bzm-mcp' in member.filename and not member.filename.endswith('/'):
                extracted_path = extract_dir / member.filename
                if extracted_path.exists() and extracted_path.is_file():
                    # Restaurar permisos de ejecución (755)
                    os.chmod(extracted_path, 0o755)
    print(f"Extracted to {extract_dir}")


def find_binaries(directory: Path):
    """Encuentra binarios o .app bundles en un directorio."""
    binaries = []
    apps = []
    
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        
        # Saltar el directorio __MACOSX (metadatos de macOS en archivos zip)
        if '__MACOSX' in root_path.parts:
            continue
        
        # Buscar .app bundles
        for item in root_path.iterdir():
            if item.is_dir() and item.suffix == ".app":
                # Asegurarse de que no está dentro de __MACOSX
                if '__MACOSX' not in item.parts:
                    apps.append(item)
        
        # Buscar binarios ejecutables (sin extensión o con extensiones comunes)
        for file in files:
            file_path = root_path / file
            if file_path.is_file():
                # Verificar si es ejecutable
                if os.access(file_path, os.X_OK):
                    # Excluir archivos de sistema y scripts
                    if not file.startswith('.') and file not in ['launcher.sh', 'Info.plist']:
                        # Buscar binarios comunes de PyInstaller
                        if 'bzm-mcp' in file.lower() or file.endswith(('.bin', '')):
                            binaries.append(file_path)
    
    return binaries, apps


def find_entitlements_file(search_dir: Path = None):
    """Busca un archivo de entitlements en ubicaciones comunes."""
    if search_dir is None:
        search_dir = Path.cwd()
    
    # Obtener el directorio home del usuario
    home_dir = Path.home()
    
    possible_entitlements = [
        search_dir / "entitlements.plist",
        Path("entitlements.plist"),
        Path("dist") / "amd" / "entitlements.plist",
        Path("dist") / "arm" / "entitlements.plist",
        home_dir / "dist" / "amd" / "entitlements.plist",
        home_dir / "dist" / "arm" / "entitlements.plist",
        # Ruta específica usada en build.py
        Path("/Users/abstracta/dist/arm/entitlements.plist"),
        Path("/Users/abstracta/dist/amd/entitlements.plist"),
    ]
    
    for ent_path in possible_entitlements:
        if ent_path.exists():
            return ent_path
    
    return None


def process_zip(input_zip: Path, output_dir: Path = None, entitlements: Path = None, 
                notarize: bool = True, identity: str = None):
    """Procesa un archivo .zip: extrae, firma y vuelve a comprimir.
    
    Args:
        input_zip: Ruta al archivo .zip de entrada
        output_dir: Directorio donde guardar los archivos firmados (por defecto: mismo directorio que input_zip)
        entitlements: Ruta al archivo de entitlements (opcional, se buscará automáticamente si no se proporciona)
        notarize: Si True, notariza los archivos .zip resultantes
        identity: Identidad de firma (opcional, se usa CODESIGN_IDENTITY si no se proporciona)
    """
    if not input_zip.exists():
        raise FileNotFoundError(f"Input zip file not found: {input_zip}")
    
    if output_dir is None:
        output_dir = input_zip.parent
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Buscar entitlements si no se proporciona
    if entitlements is None:
        entitlements = find_entitlements_file()
        if entitlements:
            print(f"Found entitlements file: {entitlements}")
        else:
            print("Warning: No entitlements file found. Signing without entitlements.")
    
    # Crear directorio temporal para extraer
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        extract_dir = temp_path / "extracted"
        extract_dir.mkdir(exist_ok=True)
        
        # Extraer el .zip
        extract_zip(input_zip, extract_dir)
        
        # Buscar binarios y .app bundles
        binaries, apps = find_binaries(extract_dir)
        
        if not binaries and not apps:
            print("Warning: No binaries or .app bundles found in the zip file.")
            return
        
        print(f"Found {len(binaries)} binary(ies) and {len(apps)} .app bundle(s)")
        
        # Firmar binarios
        for binary in binaries:
            sign_binary(binary, identity=identity, entitlements=entitlements)
        
        # Firmar binarios dentro de .app bundles primero
        for app in apps:
            # Buscar el binario bzm-mcp dentro del .app
            app_binary = app / "Contents" / "MacOS" / "bzm-mcp"
            if app_binary.exists():
                print(f"Found binary inside {app.name}: {app_binary.name}")
                sign_binary(app_binary, identity=identity, entitlements=entitlements)
            else:
                # Buscar cualquier binario ejecutable en MacOS
                macos_dir = app / "Contents" / "MacOS"
                if macos_dir.exists():
                    for item in macos_dir.iterdir():
                        if item.is_file() and os.access(item, os.X_OK) and not item.name.endswith('.sh'):
                            print(f"Found binary inside {app.name}: {item.name}")
                            sign_binary(item, identity=identity, entitlements=entitlements)
                            break
        
        # Firmar .app bundles completos (después de firmar los binarios internos)
        for app in apps:
            sign_binary(app, identity=identity, entitlements=entitlements)
        
        # Copiar .app bundles al directorio de salida
        output_apps = []
        for app in apps:
            output_app = output_dir / app.name
            print(f"Copying {app.name} to output directory...")
            if output_app.exists():
                shutil.rmtree(output_app)
            # Usar copytree que preserva metadatos
            shutil.copytree(app, output_app, copy_function=shutil.copy2)
            
            # Asegurar que todos los binarios ejecutables mantengan sus permisos
            macos_dir = output_app / "Contents" / "MacOS"
            if macos_dir.exists():
                for item in macos_dir.iterdir():
                    if item.is_file() and os.access(item, os.X_OK):
                        # Asegurar permisos de ejecución (755) para mantener formato binario
                        os.chmod(item, 0o755)
                        print(f"Preserved binary format and permissions for {item.name}")
            
            output_apps.append(output_app)
            print(f"Copied {app.name} to {output_dir}")
        
        # Crear nuevos .zip files firmados
        signed_zips = []
        
        # Si hay un solo binario o .app, crear un .zip con ese nombre
        if len(binaries) == 1 and len(apps) == 0:
            binary = binaries[0]
            output_zip = output_dir / f"{binary.name}.zip"
            create_zip(binary, output_zip)
            signed_zips.append(output_zip)
        elif len(apps) == 1 and len(binaries) == 0:
            app = apps[0]
            output_zip = output_dir / f"{app.name}.zip"
            create_zip(app, output_zip)
            signed_zips.append(output_zip)
        else:
            # Si hay múltiples, crear un .zip con el contenido completo
            output_zip = output_dir / f"{input_zip.stem}_signed.zip"
            create_zip(extract_dir, output_zip)
            signed_zips.append(output_zip)
        
        # Notarizar si se solicita
        notarization_successful = False
        if notarize:
            for zip_file in signed_zips:
                if notarize_zip(zip_file):
                    notarization_successful = True
        
        # Hacer staple de los .app bundles si la notarización fue exitosa
        if notarization_successful and output_apps:
            print("\nWaiting a few seconds for notarization ticket to be available...")
            time.sleep(5)  # Esperar un poco para que el ticket esté disponible
            
            for output_app in output_apps:
                staple_app(output_app)
        
        print(f"\nProcess completed. Signed files:")
        for zip_file in signed_zips:
            print(f"  - {zip_file}")
        for output_app in output_apps:
            print(f"  - {output_app}")


def main():
    parser = argparse.ArgumentParser(
        description="Firma y notariza binarios o .app desde un archivo .zip",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Firmar un .zip local
  python code_sign.py input.zip
  
  # Firmar un .zip descargado desde URL
  python code_sign.py https://example.com/bzm-mcp.zip
  
  # Firmar sin notarizar
  python code_sign.py input.zip --no-notarize
  
  # Especificar entitlements y output
  python code_sign.py input.zip --entitlements entitlements.plist --output ./signed/
  
Variables de entorno:
  CODESIGN_IDENTITY: Identidad de firma (ej: "Developer ID Application: Your Name (TEAM_ID)")
  APPLE_KEYCHAIN_PROFILE: Perfil del keychain para notarización
  APPLE_ID: Apple ID para notarización
  APPLE_TEAM_ID: Team ID para notarización
  APPLE_PASSWORD: Contraseña de aplicación para notarización
        """
    )
    
    parser.add_argument(
        "input",
        help="Ruta al archivo .zip o URL para descargar"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Directorio de salida para los archivos firmados (por defecto: mismo directorio que input)"
    )
    
    parser.add_argument(
        "--entitlements", "-e",
        type=Path,
        help="Ruta al archivo de entitlements (se buscará automáticamente si no se proporciona)"
    )
    
    parser.add_argument(
        "--no-notarize",
        action="store_true",
        help="No notarizar los archivos .zip resultantes"
    )
    
    parser.add_argument(
        "--identity", "-i",
        help="Identidad de firma (sobrescribe CODESIGN_IDENTITY)"
    )
    
    args = parser.parse_args()
    
    # Verificar que estamos en macOS
    if platform.system() != "Darwin":
        print("Error: This script only works on macOS")
        sys.exit(1)
    
    input_path = Path(args.input)
    
    # Si es una URL, descargar primero
    if args.input.startswith(("http://", "https://")):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
            tmp_path = Path(tmp_file.name)
            try:
                download_file(args.input, tmp_path)
                input_path = tmp_path
            except Exception as e:
                print(f"Error downloading file: {e}")
                sys.exit(1)
    
    try:
        process_zip(
            input_path,
            output_dir=args.output,
            entitlements=args.entitlements,
            notarize=not args.no_notarize,
            identity=args.identity
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # Limpiar archivo temporal si fue descargado
        if args.input.startswith(("http://", "https://")) and input_path.exists():
            input_path.unlink()


if __name__ == "__main__":
    main()

