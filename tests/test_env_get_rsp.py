import pytest
import jsonschema
import json

SCHEMA_FILE = "env.get.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_text_response(schema):
    """Tests valid response with text field (single variable)."""
    instance = {"text": "on"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_text_with_time(schema):
    """Tests valid response with text and time fields."""
    instance = {"text": "on", "time": 1656315835}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_response(schema):
    """Tests valid response with body field (multiple variables)."""
    instance = {"body": {"monitor-pump-one": "on", "monitor-pump-two": "off"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_with_time(schema):
    """Tests valid response with body and time fields."""
    instance = {
        "body": {"monitor-pump-one": "on", "monitor-pump-two": "off"}, 
        "time": 1656315835
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_error_response(schema):
    """Tests valid error response."""
    instance = {"err": "environment hasn't been modified {env-not-modified}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_text_invalid_type(schema):
    """Tests invalid type for text."""
    instance = {"text": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_text_invalid_type_boolean(schema):
    """Tests invalid boolean type for text."""
    instance = {"text": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_body_invalid_type(schema):
    """Tests invalid type for body."""
    instance = {"body": "not-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_array(schema):
    """Tests invalid array type for body."""
    instance = {"body": ["not", "object"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {"time": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_float(schema):
    """Tests invalid float type for time."""
    instance = {"time": 1656315835.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1656315835.5 is not of type 'integer'" in str(excinfo.value)

def test_err_invalid_type(schema):
    """Tests invalid type for err."""
    instance = {"err": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_complex_response(schema):
    """Tests a valid response with all possible fields."""
    instance = {
        "body": {
            "monitor-pump-one": "on",
            "monitor-pump-two": "off",
            "monitor-pump-three": "on"
        },
        "time": 1656315835
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"text": "on", "extra": 123}
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