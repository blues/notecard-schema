import pytest
import jsonschema
import json

SCHEMA_FILE = "file.changes.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only required fields."""
    instance = {"total": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_total(schema):
    """Tests that total field is required."""
    instance = {"changes": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'total' is a required property" in str(excinfo.value)

def test_valid_total_only(schema):
    """Tests valid response with only total field."""
    instance = {"total": 3}
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
    instance = {"total": 0, "changes": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_float(schema):
    """Tests invalid float type for changes."""
    instance = {"total": 0, "changes": 1.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1.5 is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_boolean(schema):
    """Tests invalid boolean type for changes."""
    instance = {"total": 0, "changes": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_array(schema):
    """Tests invalid array type for changes."""
    instance = {"total": 0, "changes": [1]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_info_empty_object(schema):
    """Tests valid response with empty info object."""
    instance = {"total": 0, "info": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_file_changes(schema):
    """Tests valid response with info containing file change counts."""
    instance = {"total": 5, "info": {"sensors.qo": {"changes": 5}, "data.qo": {"changes": 0}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_changes_only(schema):
    """Tests valid response with info containing only changes."""
    instance = {"total": 5, "info": {"sensors.qo": {"changes": 3}, "data.qo": {"changes": 2}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_changes_and_total(schema):
    """Tests valid response with info containing both changes and total."""
    instance = {"total": 10, "info": {"sensors.qo": {"changes": 5, "total": 10}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_additional_properties(schema):
    """Tests valid response with info containing additional properties."""
    instance = {"total": 8, "info": {"sensors.qo": {"changes": 5, "total": 8, "lastModified": "2023-01-01"}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_multiple_files(schema):
    """Tests valid response with info for multiple files."""
    instance = {
        "total": 16,
        "info": {
            "sensors.qo": {"changes": 5, "total": 8},
            "data.qo": {"changes": 0, "total": 3},
            "events.qo": {"changes": 2, "total": 5}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_info_invalid_type(schema):
    """Tests invalid type for info."""
    instance = {"total": 0, "info": "not-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_info_invalid_array(schema):
    """Tests invalid array type for info."""
    instance = {"total": 0, "info": ["not", "object"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_info_invalid_integer(schema):
    """Tests invalid integer type for info."""
    instance = {"total": 0, "info": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'object'" in str(excinfo.value)

def test_info_file_changes_invalid_type(schema):
    """Tests invalid type for changes in info file object."""
    instance = {"total": 0, "info": {"sensors.qo": {"changes": "not-integer"}}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_info_file_additional_properties_allowed(schema):
    """Tests that additional properties are allowed in info file objects."""
    # Since additionalProperties is true, any additional properties should be allowed
    instance = {"total": 5, "info": {"sensors.qo": {"changes": 5, "custom_field": "any_value", "timestamp": 123}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_info_file_value_not_object(schema):
    """Tests invalid non-object value in info."""
    instance = {"total": 0, "info": {"sensors.qo": "not-object"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid response with all possible fields."""
    instance = {
        "total": 2,
        "changes": 1,
        "pending": True,
        "info": {
            "sensors.qo": {"changes": 5, "total": 8},
            "data.qo": {"changes": 0, "total": 3}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_all_non_required_fields_optional(schema):
    """Tests that all non-required fields are optional."""
    # Only total is required; changes, pending, and info are optional
    instance = {"total": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_changes_optional(schema):
    """Tests that changes field is optional."""
    instance = {"total": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_info_optional(schema):
    """Tests that info field is optional."""
    instance = {"total": 3, "changes": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_pending_field(schema):
    """Tests valid pending field."""
    valid_instances = [
        {"total": 0, "pending": True},
        {"total": 0, "pending": False},
        {"total": 5, "pending": True},
        {"changes": 3, "total": 5, "pending": False}
    ]

    for instance in valid_instances:
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_pending_type(schema):
    """Tests invalid type for pending field."""
    invalid_pending_types = [
        {"total": 0, "pending": "true"},
        {"total": 0, "pending": 1},
        {"total": 0, "pending": 0},
        {"total": 0, "pending": []},
        {"total": 0, "pending": {}},
        {"total": 0, "pending": None}
    ]

    for instance in invalid_pending_types:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'boolean'" in str(excinfo.value)

def test_pending_optional(schema):
    """Tests that pending field is optional."""
    # Response without pending field should be valid
    jsonschema.validate(instance={"total": 5}, schema=schema)

    # Response with pending field should also be valid
    jsonschema.validate(instance={"total": 0, "pending": True}, schema=schema)
    jsonschema.validate(instance={"total": 0, "pending": False}, schema=schema)

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
