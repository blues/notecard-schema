import pytest
import jsonschema
import json

SCHEMA_FILE = "card.trace.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_response(schema):
    """Tests valid empty response from trace configuration."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"status": "enabled"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('status' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        "status": "enabled",
        "mode": "on",
        "extra": "field"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_string_property(schema):
    """Tests invalid response with string property."""
    instance = {"message": "trace enabled"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('message' was unexpected)" in str(excinfo.value)

def test_invalid_boolean_property(schema):
    """Tests invalid response with boolean property."""
    instance = {"success": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('success' was unexpected)" in str(excinfo.value)

def test_invalid_number_property(schema):
    """Tests invalid response with number property."""
    instance = {"code": 200}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('code' was unexpected)" in str(excinfo.value)

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