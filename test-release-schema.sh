#!/bin/bash

# Test script for release schema generation
# This simulates the workflow steps locally

set -e

# Configuration
TAG_NAME="${1:-v1.1.1}"
VERSION="${TAG_NAME#v}"
INPUT_FILE="notecard.api.json"
TEST_FILE="notecard.api.test.json"
TEST_SCHEMA_PATTERN="*.test.json"

echo "Testing release schema generation with tag: $TAG_NAME (version: $VERSION)"
echo ""

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE not found!"
    exit 1
fi

# Check if Python script exists
if [ ! -f "scripts/update_schema_version.py" ]; then
    echo "Error: scripts/update_schema_version.py not found!"
    exit 1
fi

# Create test copies of a few schema files to test version updates
echo "Step 1: Testing schema version updates..."
echo "========================================="

# Find a few schema files to test
TEST_SCHEMAS=($(ls *.req.notecard.api.json 2>/dev/null | head -3))

if [ ${#TEST_SCHEMAS[@]} -eq 0 ]; then
    echo "Warning: No schema files found to test version updates"
else
    # Backup original files
    for schema in "${TEST_SCHEMAS[@]}"; do
        cp "$schema" "${schema}.backup"
    done

    # Update versions using the Python script (only test files)
    echo "Updating version to $VERSION in test schema files..."

    # Create temporary test copies
    for schema in "${TEST_SCHEMAS[@]}"; do
        TEST_SCHEMA="${schema%.json}.test.json"
        cp "$schema" "$TEST_SCHEMA"
    done

    # Run the version update script on test files
    python3 scripts/update_schema_version.py --property version --target-version "$VERSION" --pattern "$TEST_SCHEMA_PATTERN"

    # Verify version updates
    echo ""
    echo "Verifying version updates:"
    for schema in "${TEST_SCHEMAS[@]}"; do
        TEST_SCHEMA="${schema%.json}.test.json"
        CURRENT_VERSION=$(python3 -c "import json; print(json.load(open('$TEST_SCHEMA')).get('version', 'NOT FOUND'))")
        if [ "$CURRENT_VERSION" = "$VERSION" ]; then
            echo "  ✓ $schema: version updated to $VERSION"
        else
            echo "  ✗ $schema: version is $CURRENT_VERSION (expected $VERSION)"
        fi
    done

    # Clean up test files and restore originals
    for schema in "${TEST_SCHEMAS[@]}"; do
        TEST_SCHEMA="${schema%.json}.test.json"
        rm -f "$TEST_SCHEMA"
        mv "${schema}.backup" "$schema"
    done
fi

echo ""
echo "Step 2: Testing release-specific schema file generation..."
echo "==========================================================="

# Create a test copy to avoid modifying the original
cp "$INPUT_FILE" "$TEST_FILE"

# Clean up any previous test files
rm -f "$TEST_FILE.bak"

echo "Creating release-specific schema file..."

# Update URLs to point to the tagged version
sed -i '' "s|https://raw.githubusercontent.com/blues/notecard-schema/master/|https://raw.githubusercontent.com/blues/notecard-schema/refs/tags/${TAG_NAME}/|g" "$TEST_FILE"

# Also update the $id field to reference the tagged version
sed -i '' "s|https://raw.githubusercontent.com/blues/notecard-schema/master/notecard.api.json|https://raw.githubusercontent.com/blues/notecard-schema/refs/tags/${TAG_NAME}/notecard.api.json|g" "$TEST_FILE"

echo "Generated file: $TEST_FILE"

# Validation checks
echo ""
echo "Validation Results:"
echo "==================="

# Check if $id was updated correctly
echo "1. Checking \$id field:"
ID_LINE=$(grep '"$id"' "$TEST_FILE")
echo "   $ID_LINE"

if echo "$ID_LINE" | grep -q "refs/tags/$TAG_NAME"; then
    echo "   ✓ \$id field updated correctly"
else
    echo "   ✗ \$id field NOT updated correctly"
fi

# Check a few \$ref URLs were updated
echo ""
echo "2. Checking \$ref URLs (first 5):"
REF_COUNT=$(grep -c "refs/tags/$TAG_NAME" "$TEST_FILE")
echo "   Found $REF_COUNT references to $TAG_NAME"

if [ "$REF_COUNT" -gt 0 ]; then
    echo "   ✓ \$ref URLs updated correctly"
    echo "   Sample references:"
    grep "refs/tags/$TAG_NAME" "$TEST_FILE" | head -3 | sed 's/^/     /'
else
    echo "   ✗ \$ref URLs NOT updated correctly"
fi

# Check that no master references remain
echo ""
echo "3. Checking for remaining master references:"
MASTER_COUNT=$(grep -c "/master/" "$TEST_FILE" || true)
if [ "$MASTER_COUNT" -eq 0 ]; then
    echo "   ✓ No master references found"
else
    echo "   ✗ Found $MASTER_COUNT master references still present:"
    grep "/master/" "$TEST_FILE" | sed 's/^/     /'
fi

# Validate JSON syntax
echo ""
echo "4. Validating JSON syntax:"
if python3 -m json.tool "$TEST_FILE" > /dev/null 2>&1; then
    echo "   ✓ Valid JSON syntax"
else
    echo "   ✗ Invalid JSON syntax"
fi

echo ""
echo "=== Test Complete ==="
echo ""
echo "All workflow steps have been tested locally."
echo "To test with a different tag, run:"
echo "  ./test-release-schema.sh v2.0.0"
echo ""

# Clean up test file
rm -f "$TEST_FILE"