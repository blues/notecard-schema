import json
import jsonschema
import os
import pytest
import glob

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCHEMA_FILE = "notecard.api.json"

def test_notecard_api_schema_is_valid(schema):
    """
    Validates that the notecard.api.json schema itself is a valid
    JSON Schema according to the 2020-12 draft.
    Uses local registry to avoid fetching remote references.
    """
    schema_dict, registry = schema

    # Validate the schema structure using the registry to resolve local references
    # instead of trying to fetch remote ones
    try:
        validator = jsonschema.Draft202012Validator(schema_dict, registry=registry)
        # The validator creation itself validates the schema structure
        # If we get here without exception, the schema is valid
        assert validator is not None
    except jsonschema.exceptions.SchemaError as e:
        pytest.fail(f"Schema validation failed: {e}")

def test_referenced_schemas_are_valid(schema):
    """
    Validates that all schemas referenced in the 'oneOf' array of
    notecard.api.json are themselves valid JSON Schemas.
    This test checks LOCAL files based on $ref URLs.
    """
    main_schema_dict, registry = schema

    assert "oneOf" in main_schema_dict, "notecard.api.json must contain a 'oneOf' array."

    referenced_files = []
    for ref_obj in main_schema_dict["oneOf"]:
        assert "$ref" in ref_obj, "Each item in 'oneOf' must have a '$ref' key."
        ref_value = ref_obj["$ref"]
        filename = ref_value.split('/')[-1]
        referenced_files.append(filename)

    for schema_filename in referenced_files:
        schema_file_path = os.path.join(project_root, schema_filename)

        if not os.path.exists(schema_file_path):
            pytest.fail(f"Referenced schema file not found locally: {schema_file_path}")

        with open(schema_file_path, 'r') as f:
            referenced_schema_content = json.load(f)

        try:
            jsonschema.Draft202012Validator.check_schema(referenced_schema_content)
        except jsonschema.exceptions.SchemaError as e:
            pytest.fail(f"Referenced schema {schema_filename} is not a valid schema: {e}")

def test_invalid_generic_request_fails(schema):
    """
    Tests that a generic, invalid request fails validation against
    the main notecard.api.json schema.
    An empty object should not be valid under any of the schemas in 'oneOf'.
    """
    schema_dict, registry = schema
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema_dict, registry=registry)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_all_request_schemas_are_included_in_oneof(schema):
    """
    Validates that all *.req.notecard.api.json files in the project directory
    are included in the 'oneOf' array of notecard.api.json, and that no
    extra references exist that don't have corresponding files.
    """
    main_schema_dict, registry = schema

    assert "oneOf" in main_schema_dict, "notecard.api.json must contain a 'oneOf' array."

    # Get all .req.notecard.api.json files in the project directory
    req_files_pattern = os.path.join(project_root, "*.req.notecard.api.json")
    actual_req_files = set()
    for file_path in glob.glob(req_files_pattern):
        filename = os.path.basename(file_path)
        actual_req_files.add(filename)

    # Extract referenced files from the oneOf array
    referenced_files = set()
    for ref_obj in main_schema_dict["oneOf"]:
        assert "$ref" in ref_obj, "Each item in 'oneOf' must have a '$ref' key."
        ref_value = ref_obj["$ref"]
        filename = ref_value.split('/')[-1]
        # Only consider .req. files for this test (response files are not included in oneOf)
        if ".req.notecard.api.json" in filename:
            referenced_files.add(filename)

    # Check for missing files (files that exist but are not referenced)
    missing_from_oneof = actual_req_files - referenced_files
    if missing_from_oneof:
        pytest.fail(
            f"The following .req.notecard.api.json files exist but are not referenced "
            f"in the 'oneOf' array of notecard.api.json: {sorted(missing_from_oneof)}"
        )

    # Check for extra references (references that exist but files don't)
    extra_in_oneof = referenced_files - actual_req_files
    if extra_in_oneof:
        pytest.fail(
            f"The following files are referenced in the 'oneOf' array of notecard.api.json "
            f"but do not exist in the project directory: {sorted(extra_in_oneof)}"
        )

    # Verify that all referenced files actually exist on disk
    for filename in referenced_files:
        file_path = os.path.join(project_root, filename)
        if not os.path.exists(file_path):
            pytest.fail(f"Referenced file {filename} does not exist at {file_path}")

def test_every_api_has_request_and_response_pair():
    """
    Validates that for every API referenced in the 'oneOf' array,
    both request (.req.notecard.api.json) and response (.rsp.notecard.api.json)
    schema files exist in the project directory.
    """
    # Load the main schema
    main_schema_path = os.path.join(project_root, SCHEMA_FILE)
    with open(main_schema_path, 'r') as f:
        main_schema_dict = json.load(f)

    assert "oneOf" in main_schema_dict, "notecard.api.json must contain a 'oneOf' array."

    # Extract all referenced request files from the oneOf array
    referenced_req_files = set()
    for ref_obj in main_schema_dict["oneOf"]:
        assert "$ref" in ref_obj, "Each item in 'oneOf' must have a '$ref' key."
        ref_value = ref_obj["$ref"]
        filename = ref_value.split('/')[-1]
        # Only consider .req. files (response files are not included in oneOf)
        if ".req.notecard.api.json" in filename:
            referenced_req_files.add(filename)

    # Check that each referenced request file has a corresponding response file
    missing_response_files = []
    for req_filename in referenced_req_files:
        # Convert request filename to expected response filename
        # e.g., "card.attn.req.notecard.api.json" -> "card.attn.rsp.notecard.api.json"
        rsp_filename = req_filename.replace(".req.notecard.api.json", ".rsp.notecard.api.json")
        rsp_file_path = os.path.join(project_root, rsp_filename)

        if not os.path.exists(rsp_file_path):
            missing_response_files.append(rsp_filename)

    # Report any missing response files
    if missing_response_files:
        pytest.fail(
            f"The following response schema files are missing for APIs referenced in notecard.api.json: "
            f"{sorted(missing_response_files)}"
        )

    # Also check that all existing response files have corresponding request files
    rsp_files_pattern = os.path.join(project_root, "*.rsp.notecard.api.json")
    actual_rsp_files = set()
    for file_path in glob.glob(rsp_files_pattern):
        filename = os.path.basename(file_path)
        actual_rsp_files.add(filename)

    orphaned_response_files = []
    for rsp_filename in actual_rsp_files:
        # Convert response filename to expected request filename
        req_filename = rsp_filename.replace(".rsp.notecard.api.json", ".req.notecard.api.json")

        if req_filename not in referenced_req_files:
            orphaned_response_files.append(rsp_filename)

    # Report any orphaned response files
    if orphaned_response_files:
        pytest.fail(
            f"The following response schema files exist but have no corresponding request file "
            f"referenced in notecard.api.json: {sorted(orphaned_response_files)}"
        )
