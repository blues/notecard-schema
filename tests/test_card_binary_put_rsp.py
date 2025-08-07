import pytest
import jsonschema
import json

SCHEMA_FILE = "card.binary.put.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_err(schema):
    """Tests a valid response with the err field."""
    instance = {"err": "{error-description}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_err_invalid_type(schema):
    """Tests invalid type for err."""
    instance = {"err": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (allowed by default)."""
    instance = {"err": "{error}", "extra": "allowed"}
    jsonschema.validate(instance=instance, schema=schema)

def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}")
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
