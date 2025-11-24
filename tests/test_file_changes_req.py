import pytest
import jsonschema
import json

SCHEMA_FILE = "file.changes.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "file.changes"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "file.changes"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"files": ["sensors.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "file.changes", "cmd": "file.changes"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.changes' was expected" in str(excinfo.value)

def test_valid_files_single(schema):
    """Tests valid request with single file."""
    instance = {"req": "file.changes", "files": ["sensors.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_multiple(schema):
    """Tests valid request with multiple files."""
    instance = {"req": "file.changes", "files": ["sensors.qo", "data.qo", "events.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_empty_array(schema):
    """Tests valid request with empty files array."""
    instance = {"req": "file.changes", "files": []}
    jsonschema.validate(instance=instance, schema=schema)

def test_files_invalid_type(schema):
    """Tests invalid type for files."""
    instance = {"req": "file.changes", "files": "not-array"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-array' is not of type 'array'" in str(excinfo.value)

def test_files_invalid_item_type(schema):
    """Tests invalid item type in files array."""
    instance = {"req": "file.changes", "files": [123, "sensors.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_files_invalid_item_object(schema):
    """Tests invalid object item in files array."""
    instance = {"req": "file.changes", "files": [{"name": "sensors.qo"}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_valid_tracker(schema):
    """Tests valid request with tracker."""
    instance = {"req": "file.changes", "tracker": "my-tracker"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_tracker_empty_string(schema):
    """Tests valid request with empty tracker string."""
    instance = {"req": "file.changes", "tracker": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_tracker_with_special_chars(schema):
    """Tests valid request with tracker containing special characters."""
    instance = {"req": "file.changes", "tracker": "sensor-tracker_123"}
    jsonschema.validate(instance=instance, schema=schema)

def test_tracker_invalid_type(schema):
    """Tests invalid type for tracker."""
    instance = {"req": "file.changes", "tracker": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_tracker_invalid_boolean(schema):
    """Tests invalid boolean type for tracker."""
    instance = {"req": "file.changes", "tracker": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_tracker_invalid_array(schema):
    """Tests invalid array type for tracker."""
    instance = {"req": "file.changes", "tracker": ["tracker"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_valid_files_and_tracker(schema):
    """Tests valid request with both files and tracker."""
    instance = {"req": "file.changes", "files": ["sensors.qo"], "tracker": "sensor-tracker"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_optional_params(schema):
    """Tests valid request with all optional parameters."""
    instance = {"req": "file.changes", "files": ["sensors.qo", "data.qo"], "tracker": "my-tracker"}
    jsonschema.validate(instance=instance, schema=schema)

def test_files_optional(schema):
    """Tests that files field is optional."""
    instance = {"req": "file.changes", "tracker": "my-tracker"}
    jsonschema.validate(instance=instance, schema=schema)

def test_tracker_optional(schema):
    """Tests that tracker field is optional."""
    instance = {"req": "file.changes", "files": ["sensors.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "file.changes", "extra": 123}
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
