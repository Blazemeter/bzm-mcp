# Code Signing and Notarization Guide

## build.py

Builds the binary and optionally signs and notarizes it.

### Basic Usage

```bash
# Build without signing
python build.py

# Build and sign/notarize
python build.py --sign --entitlements /path/to/entitlements.plist
```

### Arguments

- `--sign`: Enable code signing and notarization
- `--entitlements`: Path to entitlements.plist file (required when using --sign)

## code_sign.py

Signs and notarizes binaries or .app bundles from a .zip file.

### Basic Usage

```bash
# Sign and notarize a local .zip
python code_sign.py input.zip -o output_dir

# Sign without notarizing
python code_sign.py input.zip --no-notarize -o output_dir

# Specify entitlements
python code_sign.py input.zip --entitlements entitlements.plist -o output_dir
```

### Arguments

- `input`: Path to .zip file or URL
- `--output, -o`: Output directory (default: same as input)
- `--entitlements, -e`: Path to entitlements file (auto-searched if not provided)
- `--no-notarize`: Skip notarization
- `--identity, -i`: Signing identity (overrides CODESIGN_IDENTITY env var)

### Environment Variables

- `CODESIGN_IDENTITY`: Signing identity (e.g., "Developer ID Application: Name (TEAM_ID)")
- `APPLE_KEYCHAIN_PROFILE`: Keychain profile for notarization (default: "bzm-mcp-notary" this has to be changed as per user configuration)
- `APPLE_ID`: Apple ID for notarization
- `APPLE_TEAM_ID`: Team ID for notarization
- `APPLE_PASSWORD`: Application password for notarization

## Workflow

1. **Build**: Run `build.py --sign --entitlements entitlements.plist` to create and sign binaries
2. **Re-sign existing**: Use `code_sign.py` to sign pre-built .zip files
3. **Output**: Signed .app bundles are copied to the output directory, and .zip files are created for notarization

