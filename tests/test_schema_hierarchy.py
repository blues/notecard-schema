"""
Test to verify JSON schema field hierarchy across all Notecard API schemas.
Uses card.aux.serial.req.notecard.api.json as the reference pattern.
"""

import json
import glob
import os
import pytest
from pathlib import Path

# Define the expected hierarchy based on card.aux.serial.req.notecard.api.json
EXPECTED_HIERARCHY = [
    "$schema",
    "$id",
    "title",
    "description",
    "type",
    "version",
    "apiVersion",
    "skus",
    "properties",
    "oneOf",
    "additionalProperties",
    "annotations",
    "samples"
]

def get_json_keys_order(file_path):
    """Extract the order of top-level keys from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse JSON while preserving order
        data = json.loads(content)
        return list(data.keys())
    except Exception as e:
        pytest.fail(f"Error reading {file_path}: {e}")

def check_hierarchy(keys):
    """Check if the keys follow the expected hierarchy."""
    issues = []

    # Create a mapping of expected positions
    expected_positions = {key: i for i, key in enumerate(EXPECTED_HIERARCHY)}

    # Check each key's position relative to others
    for i, key in enumerate(keys):
        if key not in expected_positions:
            continue

        expected_pos = expected_positions[key]

        # Check if any previous keys should come after this one
        for j in range(i):
            prev_key = keys[j]
            if prev_key in expected_positions:
                prev_expected_pos = expected_positions[prev_key]
                if prev_expected_pos > expected_pos:
                    issues.append(f"'{prev_key}' appears before '{key}' but should come after")

    return issues

def get_all_schema_files():
    """Get all schema files in the project."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    schema_files = []

    # TODO: remove this once we have a proper schema hierarchy, apply this pattern to all schemas
    for pattern in ["card.*.req.notecard.api.json", "card.*.rsp.notecard.api.json"]:
        schema_files.extend(glob.glob(os.path.join(project_root, pattern)))

    return sorted(schema_files)

def test_schema_field_hierarchy():
    """Test that all schema files follow the expected field hierarchy."""
    schema_files = get_all_schema_files()

    assert len(schema_files) > 0, "No schema files found to test"

    failed_files = []

    for file_path in schema_files:
        file_name = os.path.basename(file_path)
        keys = get_json_keys_order(file_path)
        issues = check_hierarchy(keys)

        if issues:
            failed_files.append({
                'file': file_name,
                'issues': issues,
                'current_order': keys
            })

    if failed_files:
        error_message = "Schema field hierarchy violations found:\n\n"
        error_message += f"Expected hierarchy: {' -> '.join(EXPECTED_HIERARCHY)}\n\n"

        for failed_file in failed_files:
            error_message += f"❌ {failed_file['file']}:\n"
            for issue in failed_file['issues']:
                error_message += f"   - {issue}\n"
            error_message += f"   Current order: {' -> '.join(failed_file['current_order'])}\n\n"

        pytest.fail(error_message)

@pytest.mark.parametrize("schema_file", get_all_schema_files())
def test_individual_schema_hierarchy(schema_file):
    """Parametrized test to check each schema file individually."""
    file_name = os.path.basename(schema_file)
    keys = get_json_keys_order(schema_file)
    issues = check_hierarchy(keys)

    if issues:
        error_message = f"Schema field hierarchy violations in {file_name}:\n"
        error_message += f"Expected hierarchy: {' -> '.join(EXPECTED_HIERARCHY)}\n"
        for issue in issues:
            error_message += f"   - {issue}\n"
        error_message += f"Current order: {' -> '.join(keys)}"
        pytest.fail(error_message)
