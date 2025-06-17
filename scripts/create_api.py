#!/usr/bin/env python3
"""
Script to create new Notecard API schema templates.

Usage: python scripts/create_api.py <api_name>
Example: python scripts/create_api.py card.random
"""

import os
import json
import sys
import argparse
from typing import Dict, Any


def get_project_root() -> str:
    """Get the project root directory."""
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_request_schema_template(api_name: str) -> Dict[str, Any]:
    """Create a template for the request schema."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://raw.githubusercontent.com/blues/notecard-schema/master/{api_name}.req.notecard.api.json",
        "title": f"{api_name} Request Application Programming Interface (API) Schema",
        "description": f"Request schema for {api_name} API command.",
        "type": "object",
        "skus": ["CELL","CELL+WIFI","WIFI","LORA"],
        "version": "0.1.1",
        "apiVersion": "9.1.1",
        "properties": {
            "cmd": {
                "description": "Command for the Notecard (no response)",
                "const": api_name
            },
            "req": {
                "description": "Request for the Notecard (expects response)",
                "const": api_name
            }
        },
        "oneOf": [
            {
                "required": ["req"],
                "properties": {
                    "req": {
                        "const": api_name
                    }
                }
            },
            {
                "required": ["cmd"],
                "properties": {
                    "cmd": {
                        "const": api_name
                    }
                }
            }
        ],
        "additionalProperties": False,
        "samples": [
            {
                "description": f"Basic {api_name} request.",
                "json": f'{{\"req\":\"{api_name}\"}}'
            }
        ],
        "annotations": [
            {
                "title": "note",
                "description": "Placeholder annotation."
            }
        ]
    }


def create_response_schema_template(api_name: str) -> Dict[str, Any]:
    """Create a template for the response schema."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://raw.githubusercontent.com/blues/notecard-schema/master/{api_name}.rsp.notecard.api.json",
        "title": f"{api_name} Response Application Programming Interface (API) Schema",
        "type": "object",
        "version": "0.1.1",
        "apiVersion": "9.1.1",
        "properties": {
            # Add sample properties - users can customize these
            "status": {
                "description": "Status of the operation",
                "type": "string"
            }
        },
        "samples": [
            {
                "description": f"Basic {api_name} response.",
                "json": '{"status": "success"}'
            }
        ]
    }


def create_request_test_template(api_name: str) -> str:
    """Create a template for the request test file."""
    test_name = api_name.replace('.', '_')
    return f'''import pytest
import jsonschema
import json

SCHEMA_FILE = "{api_name}.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {{"req": "{api_name}"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {{"cmd": "{api_name}"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {{}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {{"req": "{api_name}", "cmd": "{api_name}"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {{"req": "{api_name}", "extra": "field"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {{"cmd": "{api_name}", "extra": "field"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(f"Sample missing 'json' field: {{sample.get('description', 'Unnamed sample')}}")
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {{sample_json_str}}\\nError: {{e}}")

        jsonschema.validate(instance=instance, schema=schema)
'''


def create_response_test_template(api_name: str) -> str:
    """Create a template for the response test file."""
    test_name = api_name.replace('.', '_')
    return f'''import pytest
import jsonschema
import json

SCHEMA_FILE = "{api_name}.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {{}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {{"status": "success"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {{"status": 123}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {{"status": "success", "additional": "property"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(f"Sample missing 'json' field: {{sample.get('description', 'Unnamed sample')}}")
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {{sample_json_str}}\\nError: {{e}}")

        jsonschema.validate(instance=instance, schema=schema)
'''


def update_main_api_schema(api_name: str, project_root: str) -> None:
    """Update the main notecard.api.json file to include the new request schema."""
    api_file_path = os.path.join(project_root, "notecard.api.json")

    with open(api_file_path, 'r') as f:
        api_schema = json.load(f)

    # Add reference to the new request schema
    new_ref = {"$ref": f"https://raw.githubusercontent.com/blues/notecard-schema/master/{api_name}.req.notecard.api.json"}

    # Insert in alphabetical order
    one_of = api_schema.get("oneOf", [])
    new_ref_url = new_ref["$ref"]

    # Find the correct position to insert
    insert_index = len(one_of)
    for i, ref in enumerate(one_of):
        if ref.get("$ref", "") > new_ref_url:
            insert_index = i
            break

    one_of.insert(insert_index, new_ref)
    api_schema["oneOf"] = one_of

    # Write back to file
    with open(api_file_path, 'w') as f:
        json.dump(api_schema, f, indent=4)

    print(f"✓ Updated {api_file_path}")


def create_files(api_name: str) -> None:
    """Create all the files for the new API."""
    project_root = get_project_root()

    # Create request schema
    req_schema = create_request_schema_template(api_name)
    req_file_path = os.path.join(project_root, f"{api_name}.req.notecard.api.json")
    with open(req_file_path, 'w') as f:
        json.dump(req_schema, f, indent=4)
    print(f"✓ Created {req_file_path}")

    # Create response schema
    rsp_schema = create_response_schema_template(api_name)
    rsp_file_path = os.path.join(project_root, f"{api_name}.rsp.notecard.api.json")
    with open(rsp_file_path, 'w') as f:
        json.dump(rsp_schema, f, indent=4)
    print(f"✓ Created {rsp_file_path}")

    # Create request test
    req_test_content = create_request_test_template(api_name)
    test_name = api_name.replace('.', '_')
    req_test_path = os.path.join(project_root, "tests", f"test_{test_name}_req.py")
    with open(req_test_path, 'w') as f:
        f.write(req_test_content)
    print(f"✓ Created {req_test_path}")

    # Create response test
    rsp_test_content = create_response_test_template(api_name)
    rsp_test_path = os.path.join(project_root, "tests", f"test_{test_name}_rsp.py")
    with open(rsp_test_path, 'w') as f:
        f.write(rsp_test_content)
    print(f"✓ Created {rsp_test_path}")

    # Update main API schema
    update_main_api_schema(api_name, project_root)

    print(f"\n✅ Successfully created API templates for '{api_name}'!")
    print(f"\nNext steps:")
    print(f"1. Edit {api_name}.req.notecard.api.json to add specific request properties")
    print(f"2. Edit {api_name}.rsp.notecard.api.json to add specific response properties")
    print(f"3. Update the test files to match your schema properties")
    print(f"4. Run 'pytest tests/test_{test_name}_*.py' to verify your schemas")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Create new Notecard API schema templates",
        epilog="Example: python scripts/create_api.py card.random"
    )
    parser.add_argument(
        "api_name",
        help="Name of the API (e.g., 'card.random')"
    )

    args = parser.parse_args()

    # Validate API name format
    if not args.api_name or '.' not in args.api_name:
        print("Error: API name must contain at least one dot (e.g., 'card.random')")
        sys.exit(1)

    # Check if files already exist
    project_root = get_project_root()
    req_file = os.path.join(project_root, f"{args.api_name}.req.notecard.api.json")
    rsp_file = os.path.join(project_root, f"{args.api_name}.rsp.notecard.api.json")

    if os.path.exists(req_file) or os.path.exists(rsp_file):
        print(f"Error: Files for '{args.api_name}' already exist!")
        sys.exit(1)

    try:
        create_files(args.api_name)
    except Exception as e:
        print(f"Error creating files: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
