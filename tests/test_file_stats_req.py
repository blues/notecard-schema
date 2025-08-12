import pytest
import jsonschema
import json

SCHEMA_FILE = "file.stats.req.notecard.api.json"

def test_valid_req_without_file(schema):
    """Tests a valid request without file parameter."""
    instance = {"req": "file.stats"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_without_file(schema):
    """Tests a valid command without file parameter."""
    instance = {"cmd": "file.stats"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_file(schema):
    """Tests a valid request with file parameter."""
    instance = {"req": "file.stats", "file": "sensors.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_file(schema):
    """Tests a valid command with file parameter."""
    instance = {"cmd": "file.stats", "file": "data.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "file.stats", "cmd": "file.stats"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.stats' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.stats' was expected" in str(excinfo.value)

def test_valid_file_various_extensions(schema):
    """Tests valid file with various extensions."""
    extensions = ["sensors.qo", "data.qos", "config.db", "settings.dbs"]
    for ext in extensions:
        instance = {"req": "file.stats", "file": ext}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_file_no_extension(schema):
    """Tests valid file without extension."""
    instance = {"req": "file.stats", "file": "data"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_file_empty_string(schema):
    """Tests valid file with empty string."""
    instance = {"req": "file.stats", "file": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_file_with_special_chars(schema):
    """Tests valid file with special characters."""
    instance = {"req": "file.stats", "file": "my-sensor_data.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_file_invalid_type(schema):
    """Tests invalid type for file."""
    instance = {"req": "file.stats", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_file_invalid_boolean(schema):
    """Tests invalid boolean type for file."""
    instance = {"req": "file.stats", "file": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_file_invalid_array(schema):
    """Tests invalid array type for file."""
    instance = {"req": "file.stats", "file": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_file_invalid_object(schema):
    """Tests invalid object type for file."""
    instance = {"req": "file.stats", "file": {"name": "data.qo"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_req_invalid_type(schema):
    """Tests invalid type for req."""
    instance = {"req": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.stats' was expected" in str(excinfo.value)

def test_cmd_invalid_type(schema):
    """Tests invalid type for cmd."""
    instance = {"cmd": ["file.stats"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.stats' was expected" in str(excinfo.value)

def test_req_invalid_boolean(schema):
    """Tests invalid boolean type for req."""
    instance = {"req": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.stats' was expected" in str(excinfo.value)

def test_cmd_invalid_boolean(schema):
    """Tests invalid boolean type for cmd."""
    instance = {"cmd": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.stats' was expected" in str(excinfo.value)

def test_file_parameter_optional(schema):
    """Tests that file parameter is optional."""
    instance = {"req": "file.stats"}
    jsonschema.validate(instance=instance, schema=schema)

def test_file_parameter_optional_with_cmd(schema):
    """Tests that file parameter is optional with cmd."""
    instance = {"cmd": "file.stats"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "file.stats", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with an additional property."""
    instance = {"cmd": "file.stats", "invalid": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "file.stats", "extra1": 123, "extra2": "value"}
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