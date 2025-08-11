import pytest
import jsonschema
import json

SCHEMA_FILE = "card.restart.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"restarting": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('restarting' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        "status": "restarting",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

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
