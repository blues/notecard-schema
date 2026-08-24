import pytest
import jsonschema
import json

SCHEMA_FILE = "file.changes.pending.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "file.changes.pending"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "file.changes.pending"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "file.changes.pending", "cmd": "file.changes.pending"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_req_invalid_type(schema):
    """Tests invalid type for req."""
    instance = {"req": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_cmd_invalid_type(schema):
    """Tests invalid type for cmd."""
    instance = {"cmd": ["file.changes.pending"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_req_invalid_boolean(schema):
    """Tests invalid boolean type for req."""
    instance = {"req": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_cmd_invalid_boolean(schema):
    """Tests invalid boolean type for cmd."""
    instance = {"cmd": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_req_invalid_object(schema):
    """Tests invalid object type for req."""
    instance = {"req": {"api": "file.changes.pending"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_cmd_invalid_object(schema):
    """Tests invalid object type for cmd."""
    instance = {"cmd": {"api": "file.changes.pending"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes.pending' was expected" in str(excinfo.value)

def test_valid_files_single(schema):
    """Tests valid request with a single file."""
    instance = {"req": "file.changes.pending", "files": ["sensors.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_multiple(schema):
    """Tests valid request with multiple files."""
    instance = {"req": "file.changes.pending", "files": ["sensors.qo", "data.qo", "events.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_empty_array(schema):
    """Tests valid request with empty files array."""
    instance = {"req": "file.changes.pending", "files": []}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_with_cmd(schema):
    """Tests valid command with files."""
    instance = {"cmd": "file.changes.pending", "files": ["sensors.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_files_optional(schema):
    """Tests that the files field is optional."""
    instance = {"req": "file.changes.pending"}
    jsonschema.validate(instance=instance, schema=schema)

def test_files_invalid_type(schema):
    """Tests invalid type for files."""
    instance = {"req": "file.changes.pending", "files": "not-array"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-array' is not of type 'array'" in str(excinfo.value)

def test_files_invalid_item_type(schema):
    """Tests invalid item type in files array."""
    instance = {"req": "file.changes.pending", "files": [123, "sensors.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_files_invalid_item_object(schema):
    """Tests invalid object item in files array."""
    instance = {"req": "file.changes.pending", "files": [{"name": "sensors.qo"}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "file.changes.pending", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with an additional property."""
    instance = {"cmd": "file.changes.pending", "invalid": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "file.changes.pending", "extra1": 123, "extra2": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

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
