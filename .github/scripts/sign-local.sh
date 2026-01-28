#!/bin/bash
set -e

# ==============================================================================
# Local macOS Code Signing & Notarization Test Script
# Use this to test signing before setting up GitHub Actions
# ==============================================================================

# Check if binary path is provided
if [ -z "$1" ]; then
  echo "Usage: ./sign-local.sh <path-to-binary>"
  echo "Example: ./sign-local.sh dist/bzm-mcp-macos-arm64"
  exit 1
fi

BINARY="$1"
BINARY_NAME=$(basename "$BINARY")

# Configuration - Update these values
SIGNING_IDENTITY="${SIGNING_IDENTITY:-Developer ID Application}"
NOTARY_PROFILE="${NOTARY_PROFILE:-bzm-mcp-notary}"
ENTITLEMENTS="${ENTITLEMENTS:-entitlements.plist}"

echo "🚀 Starting local macOS signing & notarization..."
echo ""

# Check if binary exists
if [ ! -f "$BINARY" ]; then
  echo "❌ Error: Binary not found at $BINARY"
  exit 1
fi

# Check if entitlements file exists
if [ ! -f "$ENTITLEMENTS" ]; then
  echo "❌ Entitlements file '$ENTITLEMENTS' not found."
  echo "   Please create an entitlements plist with only the capabilities required by your application,"
  echo "   and set the ENTITLEMENTS environment variable or place it at '$ENTITLEMENTS'."
  exit 1
fi

# Get full signing identity name
FULL_IDENTITY=$(security find-identity -v -p codesigning | grep "$SIGNING_IDENTITY" | head -1 | grep -o '"[^"]*"' | tr -d '"')

if [ -z "$FULL_IDENTITY" ]; then
  echo "❌ Error: Could not find signing identity matching '$SIGNING_IDENTITY'"
  echo ""
  echo "Available identities:"
  security find-identity -v -p codesigning
  exit 1
fi

echo "Using signing identity: $FULL_IDENTITY"
echo ""

# 1. Remove quarantine attribute
echo "🧹 Checking for quarantine attribute..."
if xattr -l "$BINARY" 2>/dev/null | grep -q "com.apple.quarantine"; then
  echo "  Removing quarantine attribute..."
  xattr -d com.apple.quarantine "$BINARY"
fi

# 2. Remove existing signature
echo "🔓 Removing existing signature..."
codesign --remove-signature "$BINARY" 2>/dev/null || true

# 3. Sign with entitlements
echo "✍️ Signing binary..."
codesign --sign "$FULL_IDENTITY" \
  --entitlements "$ENTITLEMENTS" \
  --options runtime \
  --timestamp \
  --force \
  --verbose \
  "$BINARY"

# 4. Verify signature
echo "🔍 Verifying signature..."
codesign --verify --verbose "$BINARY"
codesign --display --verbose=4 "$BINARY" | grep Authority

# 5. Test binary
echo "🧪 Testing binary..."
"$BINARY" --version || echo "⚠️ Binary test failed, but continuing..."

# 6. Create ZIP
echo "📦 Creating ZIP..."
BINARY_DIR=$(dirname "$BINARY")
ZIP_FILE="${BINARY}.zip"
rm -f "$ZIP_FILE"

cd "$BINARY_DIR"
ditto -c -k --sequesterRsrc --keepParent "$BINARY_NAME" "$BINARY_NAME.zip"
cd - > /dev/null

# 7. Check notarization profile
echo "☁️ Checking notarization credentials..."
if ! xcrun notarytool history --keychain-profile "$NOTARY_PROFILE" >/dev/null 2>&1; then
  echo "❌ Error: Notarization profile '$NOTARY_PROFILE' not found or not working"
  echo ""
  echo "Please set up notarization credentials first:"
  echo "  xcrun notarytool store-credentials \"$NOTARY_PROFILE\" \\"
  echo "    --key ~/.apple-keys/AuthKey_XXXXXXXXXX.p8 \\"
  echo "    --key-id XXXXXXXXXX \\"
  echo "    --issuer YOUR-ISSUER-UUID"
  echo ""
  echo "❓ Do you want to continue without notarization? (y/N)"
  read -r response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Exiting. Binary is signed but not notarized."
    exit 1
  fi
  SKIP_NOTARIZATION=true
fi

if [ "$SKIP_NOTARIZATION" != "true" ]; then
  # 8. Notarize ZIP
  echo "☁️ Notarizing ZIP (this takes 1-5 minutes)..."
  xcrun notarytool submit "$ZIP_FILE" \
    --keychain-profile "$NOTARY_PROFILE" \
    --wait

  # 9. Verify notarization
  echo "✅ Final verification..."
  spctl --assess --type install "$ZIP_FILE" || echo "✅ Notarized (verification may require extraction)"
fi

echo ""
echo "🎉 All done!"
echo ""
echo "Signed binary: $BINARY"
if [ "$SKIP_NOTARIZATION" != "true" ]; then
  echo "Notarized ZIP: $ZIP_FILE"
  echo ""
  echo "⚠️ Note: ZIP files cannot be stapled. First-run verification requires internet connection."
else
  echo ""
  echo "⚠️ Binary is signed but NOT notarized."
fi
echo ""
echo "✅ Ready to test! Extract and run on a different Mac to verify."
