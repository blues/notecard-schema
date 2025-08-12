import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.sync.status.req.notecard.api.json"

def test_valid_req_only(schema):
    """Tests a minimal valid request with only req."""
    instance = {"req": "hub.sync.status"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_only(schema):
    """Tests a minimal valid command with only cmd."""
    instance = {"cmd": "hub.sync.status"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_sync(schema):
    """Tests valid request with sync parameter."""
    instance = {"req": "hub.sync.status", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_sync(schema):
    """Tests valid command with sync parameter."""
    instance = {"cmd": "hub.sync.status", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_true(schema):
    """Tests valid request with sync true."""
    instance = {"req": "hub.sync.status", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_false(schema):
    """Tests valid request with sync false."""
    instance = {"req": "hub.sync.status", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"sync": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "hub.sync.status", "cmd": "hub.sync.status"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync.status' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync.status' was expected" in str(excinfo.value)

def test_sync_invalid_type_string(schema):
    """Tests invalid string type for sync."""
    instance = {"req": "hub.sync.status", "sync": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_integer(schema):
    """Tests invalid integer type for sync."""
    instance = {"req": "hub.sync.status", "sync": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_array(schema):
    """Tests invalid array type for sync."""
    instance = {"req": "hub.sync.status", "sync": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_object(schema):
    """Tests invalid object type for sync."""
    instance = {"req": "hub.sync.status", "sync": {"value": True}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_req_invalid_type_integer(schema):
    """Tests invalid integer type for req."""
    instance = {"req": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync.status' was expected" in str(excinfo.value)

def test_req_invalid_type_boolean(schema):
    """Tests invalid boolean type for req."""
    instance = {"req": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync.status' was expected" in str(excinfo.value)

def test_cmd_invalid_type_array(schema):
    """Tests invalid array type for cmd."""
    instance = {"cmd": ["hub.sync.status"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync.status' was expected" in str(excinfo.value)

def test_cmd_invalid_type_object(schema):
    """Tests invalid object type for cmd."""
    instance = {"cmd": {"api": "hub.sync.status"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync.status' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "hub.sync.status", "extra": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with additional property."""
    instance = {"cmd": "hub.sync.status", "status": "check"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "hub.sync.status", "extra1": 123, "extra2": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "check"},
        {"force": True},
        {"immediate": True},
        {"timeout": 30},
        {"mode": "status"},
        {"verbose": False}
    ]
    
    for field_dict in invalid_fields:
        field_dict["req"] = "hub.sync.status"
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_sync_parameter_optional(schema):
    """Tests that sync parameter is optional."""
    instance = {"req": "hub.sync.status"}
    jsonschema.validate(instance=instance, schema=schema)

def test_empty_object_invalid(schema):
    """Tests that empty object is invalid."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_request_object_type(schema):
    """Tests that request must be an object."""
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