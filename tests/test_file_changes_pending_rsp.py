import pytest
import jsonschema
import json

SCHEMA_FILE = "file.changes.pending.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (all fields optional)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_only(schema):
    """Tests valid response with only total field."""
    instance = {"total": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_changes_with_total(schema):
    """Tests valid response with changes and total fields."""
    instance = {"total": 3, "changes": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_pending_with_total(schema):
    """Tests valid response with pending and total fields."""
    instance = {"total": 1, "pending": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_basic_fields(schema):
    """Tests valid response with basic fields."""
    instance = {"total": 3, "changes": 3, "pending": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_large_values(schema):
    """Tests valid response with large values."""
    instance = {"total": 1000, "changes": 500, "pending": True}
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
    instance = {"total": 1, "changes": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_float(schema):
    """Tests invalid float type for changes."""
    instance = {"total": 1, "changes": 3.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "3.5 is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_boolean(schema):
    """Tests invalid boolean type for changes."""
    instance = {"total": 1, "changes": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_array(schema):
    """Tests invalid array type for changes."""
    instance = {"total": 1, "changes": [3]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_pending_invalid_type(schema):
    """Tests invalid type for pending."""
    instance = {"total": 1, "pending": "not-boolean"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-boolean' is not of type 'boolean'" in str(excinfo.value)

def test_pending_invalid_integer(schema):
    """Tests invalid integer type for pending."""
    instance = {"total": 1, "pending": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_pending_invalid_array(schema):
    """Tests invalid array type for pending."""
    instance = {"total": 1, "pending": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_valid_info_empty_object(schema):
    """Tests valid response with empty info object."""
    instance = {"total": 1, "info": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_single_file(schema):
    """Tests valid response with info for single file."""
    instance = {"total": 3, "info": {"sensors.qo": {"changes": 3, "total": 3}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_multiple_files(schema):
    """Tests valid response with info for multiple files."""
    instance = {
        "total": 5,
        "info": {
            "sensors.qo": {"changes": 3, "total": 3},
            "data.qo": {"changes": 2, "total": 2}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_with_zero_values(schema):
    """Tests valid response with info containing zero values."""
    instance = {"total": 1, "info": {"sensors.qo": {"changes": 1, "total": 1}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_changes_only(schema):
    """Tests valid response with info containing only changes."""
    instance = {"total": 5, "info": {"sensors.qo": {"changes": 5}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_info_total_only(schema):
    """Tests valid response with info containing only total."""
    instance = {"total": 10, "info": {"sensors.qo": {"total": 10}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_info_invalid_type(schema):
    """Tests invalid type for info."""
    instance = {"total": 1, "info": "not-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_info_invalid_array(schema):
    """Tests invalid array type for info."""
    instance = {"total": 1, "info": ["not", "object"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_info_invalid_integer(schema):
    """Tests invalid integer type for info."""
    instance = {"total": 1, "info": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'object'" in str(excinfo.value)

def test_info_file_value_not_object(schema):
    """Tests invalid non-object value in info."""
    instance = {"total": 1, "info": {"sensors.qo": "not-object"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_info_file_changes_invalid_type(schema):
    """Tests invalid type for changes in info file object."""
    instance = {"total": 1, "info": {"sensors.qo": {"changes": "not-integer"}}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_info_file_total_invalid_type(schema):
    """Tests invalid type for total in info file object."""
    instance = {"total": 1, "info": {"sensors.qo": {"total": "not-integer"}}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_info_file_changes_invalid_float(schema):
    """Tests invalid float type for changes in info file object."""
    instance = {"total": 1, "info": {"sensors.qo": {"changes": 3.5}}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "3.5 is not of type 'integer'" in str(excinfo.value)

def test_info_file_total_invalid_float(schema):
    """Tests invalid float type for total in info file object."""
    instance = {"total": 1, "info": {"sensors.qo": {"total": 3.5}}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "3.5 is not of type 'integer'" in str(excinfo.value)

def test_info_file_additional_property_allowed(schema):
    """Tests that additional properties in info file objects are allowed."""
    instance = {"total": 3, "info": {"sensors.qo": {"changes": 3, "total": 3, "extra": "allowed"}}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid response with all possible fields."""
    instance = {
        "total": 5,
        "changes": 5,
        "pending": True,
        "info": {
            "sensors.qo": {"changes": 3, "total": 3},
            "data.qo": {"changes": 2, "total": 2}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_all_fields_optional(schema):
    """Tests that all fields are optional."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_changes_optional(schema):
    """Tests that changes field is optional."""
    instance = {"total": 3, "pending": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_pending_optional(schema):
    """Tests that pending field is optional."""
    instance = {"total": 3, "changes": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_info_optional(schema):
    """Tests that info field is optional."""
    instance = {"total": 3, "changes": 3, "pending": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"total": 3, "changes": 3, "pending": True, "extra": 123}
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
