#!/usr/bin/env python3
"""Script to sign and notarize binaries or .app bundles from a .zip file."""
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
    """Search for a Developer ID Application certificate in the keychain."""
    try:
        result = subprocess.run(
            ["security", "find-identity", "-v", "-p", "codesigning"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.split('\n'):
            if 'Developer ID Application' in line:
                # The format is: "   1) ABC123... \"Developer ID Application: Name (TEAM_ID)\""
                # Search for the complete content between quotes that contains "Developer ID Application"
                identity_match = re.search(r'"([^"]*Developer ID Application[^"]*)"', line)
                if identity_match:
                    # group(1) contains the text inside the quotes
                    return identity_match.group(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return None


def sign_binary(binary_path: Path, identity: str = None, entitlements: Path = None):
    """Sign a binary using codesign.
    
    The identity can be provided as a parameter or via environment variable:
    - CODESIGN_IDENTITY: Full identity (e.g.: "Developer ID Application: Your Name (TEAM_ID)")
    
    If not provided, it will try to find a Developer ID Application in the keychain.
    If not found, it will use the default keychain identity.
    """
    if not binary_path.exists():
        raise FileNotFoundError(f"Binary not found: {binary_path}")
    
    # Get identity from environment variable if not provided as parameter
    identity = identity or os.getenv("CODESIGN_IDENTITY")
    
    # If still no identity, try to find a Developer ID
    if not identity:
        developer_id = find_developer_id()
        if developer_id:
            print(f"Using Developer ID: {developer_id}")
            identity = developer_id
        else:
            print("Warning: No Developer ID found. Using default keychain identity.")
            identity = "-"
    
    # Build the signing command (same order as manual command)
    cmd = ["codesign", "--sign", identity]
    
    # Add entitlements if provided and exists
    if entitlements and entitlements.exists():
        cmd.extend(["--entitlements", str(entitlements)])
    
    # Add hardened runtime and timestamp options (same syntax as manual command)
    cmd.extend(["--options", "runtime", "--timestamp"])
    
    # Add force and verbose
    cmd.extend(["--force", "--verbose"])
    
    # If it's a .app bundle, use --deep to sign recursively
    if str(binary_path).endswith(".app"):
        cmd.append("--deep")
    
    cmd.append(str(binary_path))
    
    print(f"Signing {binary_path.name}...")
    subprocess.run(cmd, check=True)
    print(f"Successfully signed {binary_path.name}")


def create_zip(source_path: Path, zip_path: Path):
    """Compress a file or directory into a .zip."""
    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source_path}")
    
    # Ensure the zip parent directory exists
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating {zip_path.name}...")
    # Always work from the source directory to avoid including full paths
    # This ensures the zip only contains the file/directory name without the full path
    source_name = source_path.name
    source_parent = source_path.parent
    
    # Change to the source directory and create the zip with relative name
    subprocess.run(
        ["zip", "-r", str(zip_path), source_name],
        cwd=source_parent,
        check=True,
    )
    print(f"Successfully created {zip_path.name}")


def notarize_zip(zip_path: Path, apple_id: str = None, team_id: str = None, password: str = None, keychain_profile: str = None):
    """Notarize a .zip file using xcrun notarytool.
    
    Credentials can be provided as parameters or via environment variables:
    - APPLE_ID: Apple ID for notarization
    - APPLE_TEAM_ID: Team ID (optional)
    - APPLE_PASSWORD: Application password (optional, only if keychain profile is not used)
    - APPLE_KEYCHAIN_PROFILE: Keychain profile name (optional)
    
    Returns:
        bool: True if notarization was successful, False otherwise
    """
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")
    
    print(f"Notarizing {zip_path.name}...")
    
    # Get credentials from environment variables if not provided as parameters
    apple_id = apple_id or os.getenv("APPLE_ID")
    team_id = team_id or os.getenv("APPLE_TEAM_ID")
    password = password or os.getenv("APPLE_PASSWORD")
    keychain_profile = keychain_profile or os.getenv("APPLE_KEYCHAIN_PROFILE")
    
    # Build the notarization command
    cmd = ["xcrun", "notarytool", "submit", str(zip_path)]
    
    # If explicit credentials are provided, use them
    if apple_id and password:
        cmd.extend(["--apple-id", apple_id])
        if team_id:
            cmd.extend(["--team-id", team_id])
        cmd.extend(["--password", password])
        cmd.append("--wait")
    elif keychain_profile:
        # Use the specified keychain profile
        cmd.extend(["--keychain-profile", keychain_profile])
        cmd.append("--wait")
    else:
        # Use the default profile "bzm-mcp-notary" directly
        default_profile = "bzm-mcp-notary"
        print(f"Using keychain profile: {default_profile}")
        cmd.extend(["--keychain-profile", default_profile])
        cmd.append("--wait")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        output = result.stdout or ""
        
        # Check the notarization status in the output
        if "status: Accepted" in output or '"status":"Accepted"' in output:
            print(f"Successfully notarized {zip_path.name}")
            if result.stdout:
                print(result.stdout)
            return True
        elif "status: Invalid" in output or '"status":"Invalid"' in output:
            print(f"Error: Notarization failed for {zip_path.name} - Status: Invalid")
            if result.stdout:
                print(result.stdout)
            # Try to get more information about the error
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
            # If we can't determine the status, assume success if the command finished without error
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
    """Staple the notarization ticket to a .app bundle.
    
    Args:
        app_path: Path to the .app bundle to staple
        
    Returns:
        bool: True if the staple was successful, False otherwise
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
    """Download a file from a URL."""
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Downloaded to {dest_path}")


def extract_zip(zip_path: Path, extract_dir: Path):
    """Extract a .zip file to a directory."""
    print(f"Extracting {zip_path.name} to {extract_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all files
        zip_ref.extractall(extract_dir)
        
        # Restore execution permissions for all binaries after extraction
        for member in zip_ref.infolist():
            if not member.filename.endswith('/') and not member.is_dir():
                extracted_path = extract_dir / member.filename
                if extracted_path.exists() and extracted_path.is_file():
                    # Restore original permissions if available in the zip
                    if member.external_attr:
                        # Permissions are in the upper bits of external_attr
                        unix_permissions = (member.external_attr >> 16) & 0o777
                        if unix_permissions:
                            os.chmod(extracted_path, unix_permissions)
                        else:
                            # If no permissions in zip, detect if binary
                            _restore_binary_permissions(extracted_path)
                    else:
                        # If no external_attr, try to detect if binary
                        _restore_binary_permissions(extracted_path)
        
        # Recursively search for all binaries in .app bundles and restore permissions
        for root, dirs, files in os.walk(extract_dir):
            # Skip the __MACOSX directory
            if '__MACOSX' in root:
                continue
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    # Check if it's in a MacOS directory (inside .app)
                    if 'Contents/MacOS' in str(file_path) or file_path.parent.name == 'MacOS':
                        _restore_binary_permissions(file_path)
    
    print(f"Extracted to {extract_dir}")


def _restore_binary_permissions(file_path: Path):
    """Restore execution permissions for a file if it's a binary."""
    # Check if it's an executable binary (not script, not plist, etc.)
    if not file_path.name.endswith(('.sh', '.plist', '.txt', '.md', '.py', '.pyc')):
        # Check if the file is actually a binary by reading the header
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                # Check if it's a Mach-O or ELF binary
                is_binary_file = (header.startswith(b'\xcf\xfa\xed\xfe') or  # Mach-O 64-bit
                                 header.startswith(b'\xce\xfa\xed\xfe') or  # Mach-O 32-bit
                                 header.startswith(b'\x7fELF') or            # ELF
                                 header.startswith(b'MZ'))                   # PE/Windows
                if is_binary_file:
                    # Restore execution permissions (755) to maintain binary format
                    os.chmod(file_path, 0o755)
        except:
            # If we can't read the file, check if it's in MacOS (probably binary)
            if 'MacOS' in str(file_path.parent):
                os.chmod(file_path, 0o755)


def find_binaries(directory: Path):
    """Find binaries or .app bundles in a directory."""
    binaries = []
    apps = []
    
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        
        # Skip the __MACOSX directory (macOS metadata in zip files)
        if '__MACOSX' in root_path.parts:
            continue
        
        # Search for .app bundles
        for item in root_path.iterdir():
            if item.is_dir() and item.suffix == ".app":
                # Make sure it's not inside __MACOSX
                if '__MACOSX' not in item.parts:
                    apps.append(item)
        
        # Search for executable binaries (without extension or with common extensions)
        for file in files:
            file_path = root_path / file
            if file_path.is_file():
                # Check if it's executable
                if os.access(file_path, os.X_OK):
                    # Exclude system files and scripts
                    if not file.startswith('.') and file not in ['launcher.sh', 'Info.plist']:
                        # Search for common PyInstaller binaries
                        if 'bzm-mcp' in file.lower() or file.endswith(('.bin', '')):
                            binaries.append(file_path)
    
    return binaries, apps


def find_entitlements_file(search_dir: Path = None):
    """Search for an entitlements file in common locations."""
    if search_dir is None:
        search_dir = Path.cwd()
    
    # Get the user's home directory
    home_dir = Path.home()
    
    possible_entitlements = [
        search_dir / "entitlements.plist",
        Path("entitlements.plist"),
        Path("dist") / "amd" / "entitlements.plist",
        Path("dist") / "arm" / "entitlements.plist",
        home_dir / "dist" / "amd" / "entitlements.plist",
        home_dir / "dist" / "arm" / "entitlements.plist",
        # Specific path used in build.py
        Path("/Users/abstracta/dist/arm/entitlements.plist"),
        Path("/Users/abstracta/dist/amd/entitlements.plist"),
    ]
    
    for ent_path in possible_entitlements:
        if ent_path.exists():
            return ent_path
    
    return None


def process_zip(input_zip: Path, output_dir: Path = None, entitlements: Path = None, 
                notarize: bool = True, identity: str = None):
    """Process a .zip file: extract, sign, and recompress.
    
    Args:
        input_zip: Path to the input .zip file
        output_dir: Directory where to save signed files (default: same directory as input_zip)
        entitlements: Path to entitlements file (optional, will be searched automatically if not provided)
        notarize: If True, notarizes the resulting .zip files
        identity: Signing identity (optional, uses CODESIGN_IDENTITY if not provided)
    """
    if not input_zip.exists():
        raise FileNotFoundError(f"Input zip file not found: {input_zip}")
    
    if output_dir is None:
        output_dir = input_zip.parent
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Search for entitlements if not provided
    if entitlements is None:
        entitlements = find_entitlements_file()
        if entitlements:
            print(f"Found entitlements file: {entitlements}")
        else:
            print("Warning: No entitlements file found. Signing without entitlements.")
    
    # Create temporary directory to extract
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        extract_dir = temp_path / "extracted"
        extract_dir.mkdir(exist_ok=True)
        
        # Extract the .zip
        extract_zip(input_zip, extract_dir)
        
        # Search for binaries and .app bundles
        binaries, apps = find_binaries(extract_dir)
        
        if not binaries and not apps:
            print("Warning: No binaries or .app bundles found in the zip file.")
            return
        
        print(f"Found {len(binaries)} binary(ies) and {len(apps)} .app bundle(s)")
        
        # Sign binaries
        for binary in binaries:
            sign_binary(binary, identity=identity, entitlements=entitlements)
        
        # Sign binaries inside .app bundles first
        for app in apps:
            # Search for the bzm-mcp binary inside the .app
            app_binary = app / "Contents" / "MacOS" / "bzm-mcp"
            if app_binary.exists():
                print(f"Found binary inside {app.name}: {app_binary.name}")
                sign_binary(app_binary, identity=identity, entitlements=entitlements)
            else:
                # Search for any executable binary in MacOS
                macos_dir = app / "Contents" / "MacOS"
                if macos_dir.exists():
                    for item in macos_dir.iterdir():
                        if item.is_file() and os.access(item, os.X_OK) and not item.name.endswith('.sh'):
                            print(f"Found binary inside {app.name}: {item.name}")
                            sign_binary(item, identity=identity, entitlements=entitlements)
                            break
        
        # Sign complete .app bundles (after signing internal binaries)
        for app in apps:
            sign_binary(app, identity=identity, entitlements=entitlements)
        
        # Copy .app bundles to output directory
        output_apps = []
        for app in apps:
            output_app = output_dir / app.name
            print(f"Copying {app.name} to output directory...")
            if output_app.exists():
                shutil.rmtree(output_app)
            # Use copytree that preserves metadata
            shutil.copytree(app, output_app, copy_function=shutil.copy2)
            
            # Ensure all executable binaries maintain their permissions
            macos_dir = output_app / "Contents" / "MacOS"
            if macos_dir.exists():
                for item in macos_dir.iterdir():
                    if item.is_file():
                        # Check if it's a binary (not script, not plist, etc.)
                        is_binary = not item.name.endswith(('.sh', '.plist', '.txt', '.md', '.py'))
                        if is_binary:
                            # Check if the file is actually a binary by reading the header
                            try:
                                with open(item, 'rb') as f:
                                    header = f.read(4)
                                    # Check if it's a Mach-O or ELF binary
                                    is_binary_file = (header.startswith(b'\xcf\xfa\xed\xfe') or  # Mach-O 64-bit
                                                     header.startswith(b'\xce\xfa\xed\xfe') or  # Mach-O 32-bit
                                                     header.startswith(b'\x7fELF') or            # ELF
                                                     header.startswith(b'MZ'))                   # PE/Windows
                                    if is_binary_file:
                                        # Restore execution permissions (755) to maintain binary format
                                        os.chmod(item, 0o755)
                                        print(f"Preserved binary format and permissions for {item.name}")
                            except:
                                # If we can't read the file, assume it's binary if not script
                                if not item.name.endswith('.sh'):
                                    os.chmod(item, 0o755)
                                    print(f"Preserved binary format and permissions for {item.name}")
            
            output_apps.append(output_app)
            print(f"Copied {app.name} to {output_dir}")
        
        # Create new signed .zip files
        signed_zips = []
        
        # If there's a single binary or .app, create a .zip with that name
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
            # If there are multiple, create a .zip with the complete content
            output_zip = output_dir / f"{input_zip.stem}_signed.zip"
            create_zip(extract_dir, output_zip)
            signed_zips.append(output_zip)
        
        # Notarize if requested
        notarization_successful = False
        if notarize:
            for zip_file in signed_zips:
                if notarize_zip(zip_file):
                    notarization_successful = True
        
        # Staple .app bundles if notarization was successful
        if notarization_successful and output_apps:
            print("\nWaiting a few seconds for notarization ticket to be available...")
            time.sleep(5)  # Wait a bit for the ticket to be available
            
            for output_app in output_apps:
                staple_app(output_app)
        
        print(f"\nProcess completed. Signed files:")
        for zip_file in signed_zips:
            print(f"  - {zip_file}")
        for output_app in output_apps:
            print(f"  - {output_app}")


def main():
    parser = argparse.ArgumentParser(
        description="Sign and notarize binaries or .app bundles from a .zip file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sign a local .zip
  python code_sign.py input.zip
  
  # Sign a .zip downloaded from URL
  python code_sign.py https://example.com/bzm-mcp.zip
  
  # Sign without notarizing
  python code_sign.py input.zip --no-notarize
  
  # Specify entitlements and output
  python code_sign.py input.zip --entitlements entitlements.plist --output ./signed/
  
Environment variables:
  CODESIGN_IDENTITY: Signing identity (e.g.: "Developer ID Application: Your Name (TEAM_ID)")
  APPLE_KEYCHAIN_PROFILE: Keychain profile for notarization
  APPLE_ID: Apple ID for notarization
  APPLE_TEAM_ID: Team ID for notarization
  APPLE_PASSWORD: Application password for notarization
        """
    )
    
    parser.add_argument(
        "input",
        help="Path to .zip file or URL to download"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output directory for signed files (default: same directory as input)"
    )
    
    parser.add_argument(
        "--entitlements", "-e",
        type=Path,
        help="Path to entitlements file (will be searched automatically if not provided)"
    )
    
    parser.add_argument(
        "--no-notarize",
        action="store_true",
        help="Do not notarize the resulting .zip files"
    )
    
    parser.add_argument(
        "--identity", "-i",
        help="Signing identity (overrides CODESIGN_IDENTITY)"
    )
    
    args = parser.parse_args()
    
    # Verify we are on macOS
    if platform.system() != "Darwin":
        print("Error: This script only works on macOS")
        sys.exit(1)
    
    input_path = Path(args.input)
    
    # If it's a URL, download first
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
        # Clean up temporary file if it was downloaded
        if args.input.startswith(("http://", "https://")) and input_path.exists():
            input_path.unlink()


if __name__ == "__main__":
    main()

