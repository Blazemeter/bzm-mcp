# macOS Code Signing & Notarization - GitHub Actions Setup

This document describes how to set up GitHub Secrets for automated macOS code signing and notarization in the CI/CD pipeline.

## Required GitHub Secrets

You need to create the following secrets in your GitHub repository:
**Settings → Secrets and variables → Actions → New repository secret**

### 1. APPLE_CERTIFICATE_P12
**Base64-encoded .p12 certificate file**

```bash
# On your Mac, convert the certificate to base64:
base64 -i Apple-Developer-ID-Application-2025.p12 | pbcopy
```

Then paste the output into the GitHub secret value.

### 2. APPLE_CERTIFICATE_PASSWORD
**Password for the .p12 certificate file**

This is the password from your `password.txt` file that came with your certificates.

### 3. APPLE_API_KEY_P8
**Base64-encoded .p8 API key file**

```bash
# On your Mac, convert the API key to base64:
base64 -i AuthKey_XXXXXXXXXX.p8 | pbcopy
```

Then paste the output into the GitHub secret value.

### 4. APPLE_API_KEY_ID
**The Key ID from your .p8 filename**

This is the `XXXXXXXXXX` part from `AuthKey_XXXXXXXXXX.p8`

### 5. APPLE_ISSUER_ID
**Your Apple Issuer UUID**

This is your team's UUID from App Store Connect. You can find it at:
- Go to https://appstoreconnect.apple.com/access/api
- Under "Issuer ID", copy the UUID

### 6. KEYCHAIN_PASSWORD
**A temporary password for the build keychain**

This can be any strong password (it's only used temporarily during the build).
Example: Generate with `openssl rand -base64 32`

## How to Get Your Credentials

### Getting the .p12 Certificate

If you already have the certificate installed in your Keychain:

```bash
# List your signing identities
security find-identity -v -p codesigning

# Export the certificate (it will prompt for a password)
security export -k login.keychain-db \
  -t identities \
  -f pkcs12 \
  -o Apple-Developer-ID-Application-2025.p12
```

### Getting the .p8 API Key

If you already set up the API key:

```bash
# Check if you have it in the recommended location
ls -la ~/.apple-keys/

# If found, that's your .p8 file
```

If you need to create a new API key:
1. Go to https://appstoreconnect.apple.com/access/api
2. Click the "+" button next to "Keys"
3. Give it a name (e.g., "GitHub Actions Notarization")
4. Select "Developer" role
5. Click "Generate"
6. Download the .p8 file (you can only download it once!)

## Security Best Practices

✅ **DO:**
- Store all credentials as GitHub Encrypted Secrets
- Use repository secrets (not environment secrets) for sensitive data
- Limit access to who can view/edit secrets
- Rotate credentials periodically
- Use a dedicated Apple Developer account for CI/CD

❌ **DON'T:**
- Commit credentials to git (even in private repos)
- Print or log credentials in workflow output
- Share credentials via email or chat
- Use personal certificates for automated builds
- Store credentials in code or configuration files

## Workflow Overview

The automated process in `.github/workflows/build.yaml` does the following:

1. **For Linux/Windows**: Builds binaries as before (no signing on Linux, Windows signing separate)

2. **For macOS** (only on `main` branch pushes):
   - Creates a temporary keychain
   - Imports the signing certificate
   - Stores notarization credentials
   - Signs the binary with hardened runtime
   - Applies entitlements for PyInstaller compatibility
   - Creates a ZIP archive
   - Submits to Apple for notarization
   - Waits for approval (1-5 minutes)
   - Cleans up temporary files

3. **Artifacts**: Both signed binaries and notarized ZIP files are uploaded

## Testing the Setup

### Local Testing (Optional)

Before setting up GitHub Actions, you can test the signing process locally:

```bash
# Make sure you have credentials set up per the main doc
cd /path/to/bzm-mcp

# Test signing a single binary
./scripts/sign-local.sh dist/bzm-mcp-macos-arm64
```

### Testing in GitHub Actions

1. Set up all the secrets as described above
2. Push to a feature branch first (signing only runs on `main`)
3. Merge to `main` to trigger the full signing workflow
4. Check the Actions tab for workflow progress
5. Download the artifacts and test on a different Mac

## Troubleshooting

### "Error: Command failed: security import"
- Check that APPLE_CERTIFICATE_PASSWORD is correct
- Verify the .p12 file is not corrupted (base64 decode it locally to test)

### "Error: NotarizationError"
- Check that all three API credentials are correct (KEY_ID, ISSUER_ID, and the .p8 file)
- Verify your Apple Developer Program membership is active

### "Error: The specified item could not be found in the keychain"
- The keychain setup may have failed
- Check that KEYCHAIN_PASSWORD is set

### Binary runs locally but fails on other Macs
- Ensure hardened runtime is enabled (`--options runtime`)
- Verify entitlements are applied correctly
- Check that notarization completed successfully (look for "Accepted" status)

## What Files Are Created

After the workflow runs, you'll have:

```
dist/
├── bzm-mcp-linux-amd64           # Linux binary
├── bzm-mcp-linux-arm64           # Linux binary
├── bzm-mcp-windows-amd64.exe     # Windows binary
├── bzm-mcp-macos-arm64           # macOS binary (signed)
├── bzm-mcp-macos-arm64.zip       # macOS ZIP (signed & notarized)
├── bzm-mcp-macos-amd64           # macOS binary (signed)
└── bzm-mcp-macos-amd64.zip       # macOS ZIP (signed & notarized)
```

## Distribution Notes

### For End Users (ZIP Method)

The signed and notarized ZIP files are ready to distribute:

```bash
# Users download and extract:
unzip bzm-mcp-macos-arm64.zip

# First run requires internet connection
./bzm-mcp-macos-arm64 --version

# Subsequent runs work offline
```

### Alternative: DMG Distribution

If you want to create DMG files instead (supports stapling for offline verification):

1. Modify the workflow to use the DMG creation commands from the doc
2. Add DMG signing and stapling steps
3. Users get a better offline experience

## Resources

- [Apple Code Signing Guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/)
- [Notarizing macOS Software](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [GitHub Actions: Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## Questions?

If you encounter issues:
1. Check the GitHub Actions logs for detailed error messages
2. Review the security checklist in the main documentation
3. Verify all secrets are set correctly (no extra spaces or newlines)
4. Test the credentials locally first if possible
