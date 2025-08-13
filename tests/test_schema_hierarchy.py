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

def get_properties_keys_order(file_path):
    """Extract the order of keys from the properties object in a JSON schema file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse JSON while preserving order
        data = json.loads(content)
        if 'properties' in data and isinstance(data['properties'], dict):
            return list(data['properties'].keys())
        return []
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

def check_req_cmd_at_end(properties_keys):
    """Check that 'req' and 'cmd' properties are at the end of the properties object."""
    issues = []

    if not properties_keys:
        return issues

    # Find positions of req and cmd
    req_pos = properties_keys.index('req') if 'req' in properties_keys else -1
    cmd_pos = properties_keys.index('cmd') if 'cmd' in properties_keys else -1

    # If we have req or cmd, check they come after all other properties
    if req_pos >= 0:
        for i, key in enumerate(properties_keys):
            if key != 'req' and key != 'cmd' and i > req_pos:
                issues.append(f"Property '{key}' appears after 'req' but should come before it")

    if cmd_pos >= 0:
        for i, key in enumerate(properties_keys):
            if key != 'req' and key != 'cmd' and i > cmd_pos:
                issues.append(f"Property '{key}' appears after 'cmd' but should come before it")

    # If both req and cmd exist, they should be adjacent at the end
    if req_pos >= 0 and cmd_pos >= 0:
        expected_end_positions = sorted([req_pos, cmd_pos])
        actual_end_positions = [len(properties_keys) - 2, len(properties_keys) - 1]

        if expected_end_positions != actual_end_positions:
            issues.append("'req' and 'cmd' properties should be the last two properties in the properties object")
    elif req_pos >= 0 and req_pos != len(properties_keys) - 1:
        issues.append("'req' property should be the last property in the properties object")
    elif cmd_pos >= 0 and cmd_pos != len(properties_keys) - 1:
        issues.append("'cmd' property should be the last property in the properties object")

    return issues

def get_all_schema_files():
    """Get all schema files in the project."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    schema_files = []

    for pattern in ["*.req.notecard.api.json", "*.rsp.notecard.api.json"]:
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
        properties_keys = get_properties_keys_order(file_path)

        issues = check_hierarchy(keys)
        properties_issues = check_req_cmd_at_end(properties_keys)

        all_issues = issues + properties_issues

        if all_issues:
            failed_files.append({
                'file': file_name,
                'issues': all_issues,
                'current_order': keys,
                'properties_order': properties_keys
            })

    if failed_files:
        error_message = "Schema field hierarchy violations found:\n\n"
        error_message += f"Expected top-level hierarchy: {' -> '.join(EXPECTED_HIERARCHY)}\n"
        error_message += "Expected properties hierarchy: [other properties] -> req/cmd (at end)\n\n"

        for failed_file in failed_files:
            error_message += f"❌ {failed_file['file']}:\n"
            for issue in failed_file['issues']:
                error_message += f"   - {issue}\n"
            error_message += f"   Current top-level order: {' -> '.join(failed_file['current_order'])}\n"
            if failed_file['properties_order']:
                error_message += f"   Current properties order: {' -> '.join(failed_file['properties_order'])}\n"
            error_message += "\n"

        pytest.fail(error_message)

@pytest.mark.parametrize("schema_file", get_all_schema_files())
def test_individual_schema_hierarchy(schema_file):
    """Parametrized test to check each schema file individually."""
    file_name = os.path.basename(schema_file)
    keys = get_json_keys_order(schema_file)
    properties_keys = get_properties_keys_order(schema_file)

    issues = check_hierarchy(keys)
    properties_issues = check_req_cmd_at_end(properties_keys)

    all_issues = issues + properties_issues

    if all_issues:
        error_message = f"Schema field hierarchy violations in {file_name}:\n"
        error_message += f"Expected top-level hierarchy: {' -> '.join(EXPECTED_HIERARCHY)}\n"
        error_message += "Expected properties hierarchy: [other properties] -> req/cmd (at end)\n"
        for issue in all_issues:
            error_message += f"   - {issue}\n"
        error_message += f"Current top-level order: {' -> '.join(keys)}\n"
        if properties_keys:
            error_message += f"Current properties order: {' -> '.join(properties_keys)}"
        pytest.fail(error_message)
