import json
import jsonschema
import os
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCHEMA_FILE = "notecard.api.json"

def test_notecard_api_schema_is_valid(schema):
    """
    Validates that the notecard.api.json schema itself is a valid
    JSON Schema according to the 2020-12 draft.
    """
    schema_dict, registry = schema
    jsonschema.Draft202012Validator.check_schema(schema_dict)

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
