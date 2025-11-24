import pytest
import jsonschema
import json

SCHEMA_FILE = "file.delete.req.notecard.api.json"

def test_valid_req_with_files(schema):
    """Tests a valid request with files parameter."""
    instance = {"req": "file.delete", "files": ["my-settings.db", "other-settings.db"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_files(schema):
    """Tests a valid command with files parameter."""
    instance = {"cmd": "file.delete", "files": ["data.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_missing_files(schema):
    """Tests invalid request missing files parameter."""
    instance = {"req": "file.delete"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_cmd_missing_files(schema):
    """Tests invalid command missing files parameter."""
    instance = {"cmd": "file.delete"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "file.delete", "cmd": "file.delete", "files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.delete' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.delete' was expected" in str(excinfo.value)

def test_valid_files_single_item(schema):
    """Tests valid files array with single item."""
    instance = {"req": "file.delete", "files": ["data.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_multiple_items(schema):
    """Tests valid files array with multiple items."""
    instance = {"req": "file.delete", "files": ["sensors.db", "data.qo", "config.qos"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_empty_array(schema):
    """Tests valid files array that is empty."""
    instance = {"req": "file.delete", "files": []}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_various_extensions(schema):
    """Tests valid files with various extensions."""
    instance = {"req": "file.delete", "files": ["data.qo", "secure.qos", "settings.db", "temp.dbs"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_no_extensions(schema):
    """Tests valid files without extensions."""
    instance = {"req": "file.delete", "files": ["data", "settings", "temp"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_empty_strings(schema):
    """Tests valid files with empty strings."""
    instance = {"req": "file.delete", "files": ["", "data.qo", ""]}
    jsonschema.validate(instance=instance, schema=schema)

def test_files_invalid_type(schema):
    """Tests invalid type for files."""
    instance = {"req": "file.delete", "files": "not-array"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-array' is not of type 'array'" in str(excinfo.value)

def test_files_invalid_integer(schema):
    """Tests invalid integer type for files."""
    instance = {"req": "file.delete", "files": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'array'" in str(excinfo.value)

def test_files_invalid_boolean(schema):
    """Tests invalid boolean type for files."""
    instance = {"req": "file.delete", "files": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'array'" in str(excinfo.value)

def test_files_invalid_object(schema):
    """Tests invalid object type for files."""
    instance = {"req": "file.delete", "files": {"name": "data.qo"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'array'" in str(excinfo.value)

def test_files_item_invalid_type(schema):
    """Tests invalid item type in files array."""
    instance = {"req": "file.delete", "files": [123, "data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_files_item_invalid_boolean(schema):
    """Tests invalid boolean item in files array."""
    instance = {"req": "file.delete", "files": ["data.qo", True, "config.db"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_files_item_invalid_object(schema):
    """Tests invalid object item in files array."""
    instance = {"req": "file.delete", "files": [{"name": "data.qo"}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_files_item_invalid_array(schema):
    """Tests invalid array item in files array."""
    instance = {"req": "file.delete", "files": [["data.qo"]]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_req_invalid_type(schema):
    """Tests invalid type for req."""
    instance = {"req": 123, "files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.delete' was expected" in str(excinfo.value)

def test_cmd_invalid_type(schema):
    """Tests invalid type for cmd."""
    instance = {"cmd": ["file.delete"], "files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.delete' was expected" in str(excinfo.value)

def test_req_invalid_boolean(schema):
    """Tests invalid boolean type for req."""
    instance = {"req": True, "files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.delete' was expected" in str(excinfo.value)

def test_cmd_invalid_boolean(schema):
    """Tests invalid boolean type for cmd."""
    instance = {"cmd": False, "files": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file.delete' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "file.delete", "files": ["data.qo"], "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with an additional property."""
    instance = {"cmd": "file.delete", "files": ["data.qo"], "invalid": "value"}
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
