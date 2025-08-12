import pytest
import jsonschema
import json

SCHEMA_FILE = "file.stats.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_only(schema):
    """Tests valid response with only total field."""
    instance = {"total": 83}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_changes_only(schema):
    """Tests valid response with only changes field."""
    instance = {"changes": 78}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_only(schema):
    """Tests valid response with only sync field."""
    instance = {"sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_false(schema):
    """Tests valid response with sync false."""
    instance = {"sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {"total": 83, "changes": 78, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_zero_values(schema):
    """Tests valid response with zero values."""
    instance = {"total": 0, "changes": 0, "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_large_values(schema):
    """Tests valid response with large values."""
    instance = {"total": 1000000, "changes": 999999, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_no_pending_changes(schema):
    """Tests valid response with no pending changes."""
    instance = {"total": 25, "changes": 0, "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_total_invalid_type(schema):
    """Tests invalid type for total."""
    instance = {"total": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_float(schema):
    """Tests invalid float type for total."""
    instance = {"total": 83.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "83.5 is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_boolean(schema):
    """Tests invalid boolean type for total."""
    instance = {"total": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_array(schema):
    """Tests invalid array type for total."""
    instance = {"total": [83]}
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
    instance = {"changes": 78.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "78.5 is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_boolean(schema):
    """Tests invalid boolean type for changes."""
    instance = {"changes": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_array(schema):
    """Tests invalid array type for changes."""
    instance = {"changes": [78]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_sync_invalid_type(schema):
    """Tests invalid type for sync."""
    instance = {"sync": "not-boolean"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-boolean' is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_integer(schema):
    """Tests invalid integer type for sync."""
    instance = {"sync": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_array(schema):
    """Tests invalid array type for sync."""
    instance = {"sync": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_object(schema):
    """Tests invalid object type for sync."""
    instance = {"sync": {"value": True}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_valid_partial_combinations(schema):
    """Tests valid responses with various field combinations."""
    combinations = [
        {"total": 100},
        {"changes": 50},
        {"sync": True},
        {"total": 100, "changes": 50},
        {"total": 100, "sync": True},
        {"changes": 50, "sync": False},
        {"total": 100, "changes": 50, "sync": True}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_total_optional(schema):
    """Tests that total field is optional."""
    instance = {"changes": 78, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_changes_optional(schema):
    """Tests that changes field is optional."""
    instance = {"total": 83, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_sync_optional(schema):
    """Tests that sync field is optional."""
    instance = {"total": 83, "changes": 78}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"total": 83, "changes": 78, "sync": True, "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"message": "success"},
        {"count": 5},
        {"files": []},
        {"result": {}},
        {"data": {"total": 83}}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = [
        "string",
        123,
        True,
        False,
        ["array"],
        None
    ]
    
    for invalid_instance in invalid_types:
        if invalid_instance is None:
            continue  # Skip None as it's handled differently
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=invalid_instance, schema=schema)
        # The error message will vary based on type, just ensure validation fails

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