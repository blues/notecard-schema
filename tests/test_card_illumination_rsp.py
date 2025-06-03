import pytest
import jsonschema
import json

SCHEMA_FILE = "card.illumination.rsp.notecard.api.json"

def test_valid_value(schema):
    """Tests a valid response with the 'value' field."""
    instance = {"value": 100.5}
    jsonschema.validate(instance=instance, schema=schema)

def test_value_invalid_type(schema):
    """Tests an invalid type for the 'value' field."""
    instance = {"value": "high"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'high' is not of type 'number'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests a valid response with an additional property."""
    instance = {"value": 50, "status": "ok"}
    jsonschema.validate(instance=instance, schema=schema)

def test_empty_object_valid(schema):
    """Tests that an empty object is a valid response (lux is not required)."""
    instance = {}
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
