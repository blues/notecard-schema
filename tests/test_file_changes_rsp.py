import pytest
import jsonschema
import json

SCHEMA_FILE = "file.changes.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_only(schema):
    """Tests valid response with only total field."""
    instance = {"total": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_changes_only(schema):
    """Tests valid response with only changes field."""
    instance = {"changes": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_and_changes(schema):
    """Tests valid response with total and changes fields."""
    instance = {"total": 3, "changes": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_zero_values(schema):
    """Tests valid response with zero values."""
    instance = {"total": 0, "changes": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_large_values(schema):
    """Tests valid response with large values."""
    instance = {"total": 1000, "changes": 500}
    jsonschema.validate(instance=instance, schema=schema)

def test_total_invalid_type(schema):
    """Tests invalid type for total."""
    instance = {"total": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_float(schema):
    """Tests invalid float type for total."""
    instance = {"total": 3.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "3.5 is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_boolean(schema):
    """Tests invalid boolean type for total."""
    instance = {"total": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_array(schema):
    """Tests invalid array type for total."""
    instance = {"total": [3]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_type(schema):
    """Tests invalid type for changes."""
    instance = {"changes": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_float(schema):
    """Tests invalid float type for changes."""
    instance = {"changes": 1.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1.5 is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_boolean(schema):
    """Tests invalid boolean type for changes."""
    instance = {"changes": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_array(schema):
    """Tests invalid array type for changes."""
    instance = {"changes": [1]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_info_empty_object(schema):
    """Tests valid response with empty info object."""
    instance = {"info": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_file_changes(schema):
    """Tests valid response with info containing file change counts."""
    instance = {"info": {"sensors.qo": {"changes": 5}, "data.qo": {"changes": 0}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_status(schema):
    """Tests valid response with info containing status information."""
    instance = {"info": {"sensors.qo": {"status": "synced"}, "data.qo": {"status": "pending"}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_changes_and_status(schema):
    """Tests valid response with info containing both changes and status."""
    instance = {"info": {"sensors.qo": {"changes": 5, "status": "synced"}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_additional_properties(schema):
    """Tests valid response with info containing additional properties."""
    instance = {"info": {"sensors.qo": {"changes": 5, "status": "synced", "lastModified": "2023-01-01"}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_multiple_files(schema):
    """Tests valid response with info for multiple files."""
    instance = {
        "info": {
            "sensors.qo": {"changes": 5, "status": "synced"},
            "data.qo": {"changes": 0, "status": "pending"},
            "events.qo": {"changes": 2}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_info_invalid_type(schema):
    """Tests invalid type for info."""
    instance = {"info": "not-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_info_invalid_array(schema):
    """Tests invalid array type for info."""
    instance = {"info": ["not", "object"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_info_invalid_integer(schema):
    """Tests invalid integer type for info."""
    instance = {"info": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'object'" in str(excinfo.value)

def test_info_file_changes_invalid_type(schema):
    """Tests invalid type for changes in info file object."""
    instance = {"info": {"sensors.qo": {"changes": "not-integer"}}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_info_file_status_invalid_type(schema):
    """Tests invalid type for status in info file object."""
    instance = {"info": {"sensors.qo": {"status": 123}}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_info_file_value_not_object(schema):
    """Tests invalid non-object value in info."""
    instance = {"info": {"sensors.qo": "not-object"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid response with all possible fields."""
    instance = {
        "total": 2,
        "changes": 1,
        "info": {
            "sensors.qo": {"changes": 5, "status": "synced"},
            "data.qo": {"changes": 0, "status": "pending"}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_total_optional(schema):
    """Tests that total field is optional."""
    instance = {"changes": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_changes_optional(schema):
    """Tests that changes field is optional."""
    instance = {"total": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_info_optional(schema):
    """Tests that info field is optional."""
    instance = {"total": 3, "changes": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"total": 3, "changes": 1, "extra": 123}
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