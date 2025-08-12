import pytest
import jsonschema
import json

SCHEMA_FILE = "env.get.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "env.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "env.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"name": "test-var"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "env.get", "cmd": "env.get"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'env.get' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'env.get' was expected" in str(excinfo.value)

def test_valid_name(schema):
    """Tests valid name field."""
    instance = {"req": "env.get", "name": "monitor-pump-one"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "env.get", "name": "SAMPLE_RATE"}
    jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"req": "env.get", "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_names_array(schema):
    """Tests valid names array."""
    instance = {"req": "env.get", "names": ["monitor-pump-one", "monitor-pump-two"]}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "env.get", "names": ["single-var"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_names_empty_array(schema):
    """Tests that names array cannot be empty."""
    instance = {"req": "env.get", "names": []}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "[] should be non-empty" in str(excinfo.value)

def test_names_invalid_type(schema):
    """Tests invalid type for names."""
    instance = {"req": "env.get", "names": "not-array"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-array' is not of type 'array'" in str(excinfo.value)

def test_names_invalid_item_type(schema):
    """Tests invalid type for names array items."""
    instance = {"req": "env.get", "names": ["valid-name", 123]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_time(schema):
    """Tests valid time field."""
    instance = {"req": "env.get", "name": "test-var", "time": 1656315835}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "env.get", "time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {"req": "env.get", "time": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_float(schema):
    """Tests invalid float type for time."""
    instance = {"req": "env.get", "time": 1656315835.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1656315835.5 is not of type 'integer'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "env.get", "extra": 123}
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