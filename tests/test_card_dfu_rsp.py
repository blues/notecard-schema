import pytest
import jsonschema
import json

SCHEMA_FILE = "card.dfu.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_name_field(schema):
    """Tests valid response with name field."""
    instance = {"name": "stm32"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"name": "esp32"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"name": "mcuboot"}
    jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_type(schema):
    """Tests invalid type for name field."""
    instance = {"name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"some_field": "some_value"}
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
