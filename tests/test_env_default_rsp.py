import pytest
import jsonschema
import json

SCHEMA_FILE = "env.default.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_name_only(schema):
    """Tests valid response with name field only."""
    instance = {"name": "monitor-pump"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_name_and_text(schema):
    """Tests valid response with both name and text fields."""
    instance = {"name": "monitor-pump", "text": "on"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_text(schema):
    """Tests valid response with empty text."""
    instance = {"name": "debug-mode", "text": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_numeric_text(schema):
    """Tests valid response with numeric text value."""
    instance = {"name": "sample-rate", "text": "60"}
    jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_text_invalid_type(schema):
    """Tests invalid type for text."""
    instance = {"name": "test-var", "text": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_text_invalid_type_boolean(schema):
    """Tests invalid boolean type for text."""
    instance = {"name": "test-var", "text": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_text_invalid_type_array(schema):
    """Tests invalid array type for text."""
    instance = {"name": "test-var", "text": ["value"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"name": "test-var", "text": "value", "extra": 123}
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