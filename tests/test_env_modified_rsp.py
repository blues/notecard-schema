import pytest
import jsonschema
import json

SCHEMA_FILE = "env.modified.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_time_response(schema):
    """Tests valid response with time field."""
    instance = {"time": 1605814493}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_zero_time(schema):
    """Tests valid response with zero time."""
    instance = {"time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_large_time(schema):
    """Tests valid response with large timestamp."""
    instance = {"time": 2147483647}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {"time": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_float(schema):
    """Tests invalid float type for time."""
    instance = {"time": 1605814493.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1605814493.5 is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_boolean(schema):
    """Tests invalid boolean type for time."""
    instance = {"time": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_array(schema):
    """Tests invalid array type for time."""
    instance = {"time": [1605814493]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"time": 1605814493, "extra": 123}
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
