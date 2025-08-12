import pytest
import jsonschema
import json

SCHEMA_FILE = "file.clear.req.notecard.api.json"

def test_valid_req_with_file(schema):
    """Tests a valid request with file parameter."""
    instance = {"req": "file.clear", "file": "data.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_file(schema):
    """Tests a valid command with file parameter."""
    instance = {"cmd": "file.clear", "file": "data.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_missing_file(schema):
    """Tests invalid request missing file parameter."""
    instance = {"req": "file.clear"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_cmd_missing_file(schema):
    """Tests invalid command missing file parameter."""
    instance = {"cmd": "file.clear"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "file.clear", "cmd": "file.clear", "file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.clear' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.clear' was expected" in str(excinfo.value)

def test_valid_file_qo_extension(schema):
    """Tests valid file with .qo extension."""
    instance = {"req": "file.clear", "file": "sensors.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_file_qos_extension(schema):
    """Tests valid file with .qos extension."""
    instance = {"req": "file.clear", "file": "sensors.qos"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_file_no_extension(schema):
    """Tests valid file without extension."""
    instance = {"req": "file.clear", "file": "data"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_file_empty_string(schema):
    """Tests valid file with empty string."""
    instance = {"req": "file.clear", "file": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_file_invalid_type(schema):
    """Tests invalid type for file."""
    instance = {"req": "file.clear", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_file_invalid_boolean(schema):
    """Tests invalid boolean type for file."""
    instance = {"req": "file.clear", "file": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_file_invalid_array(schema):
    """Tests invalid array type for file."""
    instance = {"req": "file.clear", "file": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_file_invalid_object(schema):
    """Tests invalid object type for file."""
    instance = {"req": "file.clear", "file": {"name": "data.qo"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_req_invalid_type(schema):
    """Tests invalid type for req."""
    instance = {"req": 123, "file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.clear' was expected" in str(excinfo.value)

def test_cmd_invalid_type(schema):
    """Tests invalid type for cmd."""
    instance = {"cmd": ["file.clear"], "file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.clear' was expected" in str(excinfo.value)

def test_req_invalid_boolean(schema):
    """Tests invalid boolean type for req."""
    instance = {"req": True, "file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.clear' was expected" in str(excinfo.value)

def test_cmd_invalid_boolean(schema):
    """Tests invalid boolean type for cmd."""
    instance = {"cmd": False, "file": "data.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.clear' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "file.clear", "file": "data.qo", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with an additional property."""
    instance = {"cmd": "file.clear", "file": "data.qo", "invalid": "value"}
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