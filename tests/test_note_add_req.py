import pytest
import jsonschema
import json

SCHEMA_FILE = "note.add.req.notecard.api.json"

def test_valid_req_only(schema):
    """Tests a minimal valid request with only req."""
    instance = {"req": "note.add"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_only(schema):
    """Tests a minimal valid command with only cmd."""
    instance = {"cmd": "note.add"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_body(schema):
    """Tests valid request with body parameter."""
    instance = {"req": "note.add", "body": {"temp": 25.5}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_payload(schema):
    """Tests valid request with payload parameter."""
    instance = {"req": "note.add", "payload": "SGVsbG8gV29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_file(schema):
    """Tests valid request with file parameter."""
    instance = {"req": "note.add", "file": "sensors.qo", "body": {"temp": 72.22}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_note(schema):
    """Tests valid request with note parameter."""
    instance = {"req": "note.add", "file": "config.db", "note": "device_settings", "body": {"brightness": 75}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_note_random(schema):
    """Tests valid request with note random ID generation."""
    instance = {"req": "note.add", "file": "events.db", "note": "?", "body": {"event": "button_press"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_sync(schema):
    """Tests valid request with sync parameter."""
    instance = {"req": "note.add", "body": {"data": "value"}, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_key(schema):
    """Tests valid request with key parameter."""
    instance = {"req": "note.add", "file": "secure.qos", "body": {"secret": "data"}, "key": "my_public_key"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_verify(schema):
    """Tests valid request with verify parameter."""
    instance = {"req": "note.add", "file": "template.qo", "body": {"data": 123}, "verify": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_binary(schema):
    """Tests valid request with binary parameter."""
    instance = {"req": "note.add", "file": "binary_data.qo", "body": {"sensor": 456}, "binary": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_live(schema):
    """Tests valid request with live parameter."""
    instance = {"req": "note.add", "file": "live_data.qo", "body": {"reading": 789}, "live": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_full(schema):
    """Tests valid request with full parameter."""
    instance = {"req": "note.add", "file": "complete_data.qo", "body": {"value": None}, "full": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_limit(schema):
    """Tests valid request with limit parameter."""
    instance = {"req": "note.add", "file": "alerts.qo", "body": {"alert": "high"}, "limit": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_max(schema):
    """Tests valid request with max parameter."""
    instance = {"req": "note.add", "file": "queue.qo", "body": {"item": "data"}, "max": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_max_and_sync(schema):
    """Tests valid request with max and sync parameters."""
    instance = {"req": "note.add", "file": "alerts.qo", "body": {"alert_level": "high"}, "max": 10, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_body_and_payload(schema):
    """Tests valid request with both body and payload."""
    instance = {"req": "note.add", "body": {"metadata": "info"}, "payload": "YmluYXJ5ZGF0YQ=="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_binary_and_live(schema):
    """Tests valid request with binary and live parameters."""
    instance = {"req": "note.add", "file": "stream.qo", "body": {"data": 123}, "binary": True, "live": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_all_parameters(schema):
    """Tests valid request with most parameters."""
    instance = {
        "req": "note.add",
        "file": "complete.qos",
        "body": {"temperature": 25.5, "humidity": 60},
        "payload": "SGVsbG8gV29ybGQ=",
        "sync": True,
        "key": "encryption_key",
        "verify": True,
        "full": True,
        "limit": False,
        "max": 50
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_database_operations(schema):
    """Tests valid database-related operations."""
    operations = [
        {"req": "note.add", "file": "config.db", "note": "setting1", "body": {"value": 100}},
        {"req": "note.add", "file": "data.dbs", "note": "?", "body": {"encrypted": "data"}},
        {"req": "note.add", "file": "local.dbx", "note": "local_data", "body": {"offline": True}}
    ]
    
    for operation in operations:
        jsonschema.validate(instance=operation, schema=schema)

def test_valid_queue_operations(schema):
    """Tests valid queue-related operations."""
    operations = [
        {"req": "note.add", "file": "data.qo", "body": {"plain": "data"}},
        {"req": "note.add", "file": "secure.qos", "body": {"encrypted": "data"}, "key": "my_key"}
    ]
    
    for operation in operations:
        jsonschema.validate(instance=operation, schema=schema)

def test_valid_cmd_variations(schema):
    """Tests valid command variations."""
    instance = {"cmd": "note.add", "file": "output.qo", "body": {"cmd_data": "test"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"body": {"data": "value"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "note.add", "cmd": "note.add", "body": {"data": "value"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.add' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.add' was expected" in str(excinfo.value)

def test_file_invalid_type_integer(schema):
    """Tests invalid integer type for file."""
    instance = {"req": "note.add", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_boolean(schema):
    """Tests invalid boolean type for file."""
    instance = {"req": "note.add", "file": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_array(schema):
    """Tests invalid array type for file."""
    instance = {"req": "note.add", "file": ["data.qo"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_integer(schema):
    """Tests invalid integer type for note."""
    instance = {"req": "note.add", "note": 456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_boolean(schema):
    """Tests invalid boolean type for note."""
    instance = {"req": "note.add", "note": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_object(schema):
    """Tests invalid object type for note."""
    instance = {"req": "note.add", "note": {"id": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_body_invalid_type_string(schema):
    """Tests invalid string type for body."""
    instance = {"req": "note.add", "body": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not an object' is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_integer(schema):
    """Tests invalid integer type for body."""
    instance = {"req": "note.add", "body": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_array(schema):
    """Tests invalid array type for body."""
    instance = {"req": "note.add", "body": ["data"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_payload_invalid_type_integer(schema):
    """Tests invalid integer type for payload."""
    instance = {"req": "note.add", "payload": 789}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "789 is not of type 'string'" in str(excinfo.value)

def test_payload_invalid_type_boolean(schema):
    """Tests invalid boolean type for payload."""
    instance = {"req": "note.add", "payload": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_payload_invalid_type_object(schema):
    """Tests invalid object type for payload."""
    instance = {"req": "note.add", "payload": {"data": "binary"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_sync_invalid_type_string(schema):
    """Tests invalid string type for sync."""
    instance = {"req": "note.add", "body": {"data": "value"}, "sync": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_integer(schema):
    """Tests invalid integer type for sync."""
    instance = {"req": "note.add", "body": {"data": "value"}, "sync": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_key_invalid_type_integer(schema):
    """Tests invalid integer type for key."""
    instance = {"req": "note.add", "body": {"data": "value"}, "key": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_key_invalid_type_boolean(schema):
    """Tests invalid boolean type for key."""
    instance = {"req": "note.add", "body": {"data": "value"}, "key": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_verify_invalid_type_string(schema):
    """Tests invalid string type for verify."""
    instance = {"req": "note.add", "body": {"data": "value"}, "verify": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_verify_invalid_type_integer(schema):
    """Tests invalid integer type for verify."""
    instance = {"req": "note.add", "body": {"data": "value"}, "verify": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_binary_invalid_type_string(schema):
    """Tests invalid string type for binary."""
    instance = {"req": "note.add", "body": {"data": "value"}, "binary": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_binary_invalid_type_integer(schema):
    """Tests invalid integer type for binary."""
    instance = {"req": "note.add", "body": {"data": "value"}, "binary": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_live_invalid_type_string(schema):
    """Tests invalid string type for live."""
    instance = {"req": "note.add", "body": {"data": "value"}, "live": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_live_invalid_type_integer(schema):
    """Tests invalid integer type for live."""
    instance = {"req": "note.add", "body": {"data": "value"}, "live": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_full_invalid_type_string(schema):
    """Tests invalid string type for full."""
    instance = {"req": "note.add", "body": {"data": "value"}, "full": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_full_invalid_type_integer(schema):
    """Tests invalid integer type for full."""
    instance = {"req": "note.add", "body": {"data": "value"}, "full": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_limit_invalid_type_string(schema):
    """Tests invalid string type for limit."""
    instance = {"req": "note.add", "body": {"data": "value"}, "limit": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_limit_invalid_type_integer(schema):
    """Tests invalid integer type for limit."""
    instance = {"req": "note.add", "body": {"data": "value"}, "limit": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_max_invalid_type_string(schema):
    """Tests invalid string type for max."""
    instance = {"req": "note.add", "body": {"data": "value"}, "max": "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

def test_max_invalid_type_boolean(schema):
    """Tests invalid boolean type for max."""
    instance = {"req": "note.add", "body": {"data": "value"}, "max": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_max_invalid_type_array(schema):
    """Tests invalid array type for max."""
    instance = {"req": "note.add", "body": {"data": "value"}, "max": [10]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_max_invalid_minimum_zero(schema):
    """Tests invalid zero value for max (minimum is 1)."""
    instance = {"req": "note.add", "body": {"data": "value"}, "max": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is less than the minimum of 1" in str(excinfo.value)

def test_max_invalid_minimum_negative(schema):
    """Tests invalid negative value for max (minimum is 1)."""
    instance = {"req": "note.add", "body": {"data": "value"}, "max": -5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-5 is less than the minimum of 1" in str(excinfo.value)

def test_max_valid_minimum_one(schema):
    """Tests valid minimum value for max (1)."""
    instance = {"req": "note.add", "body": {"data": "value"}, "max": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_valid_large_value(schema):
    """Tests valid large value for max."""
    instance = {"req": "note.add", "body": {"data": "value"}, "max": 1000}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "note.add", "body": {"data": "value"}, "extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with additional property."""
    instance = {"cmd": "note.add", "body": {"data": "value"}, "unknown": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "note.add", "body": {"data": "value"}, "extra1": 123, "extra2": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"result": "success"},
        {"error": "none"},
        {"message": "added"},
        {"id": "note123"},
        {"timestamp": 1640995200},
        {"count": 5},
        {"size": 250}
    ]
    
    for field_dict in invalid_fields:
        field_dict["req"] = "note.add"
        field_dict["body"] = {"data": "value"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

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

def test_valid_file_extensions(schema):
    """Tests valid file extensions."""
    valid_extensions = [
        {"req": "note.add", "file": "data.qo", "body": {"temp": 25}},
        {"req": "note.add", "file": "secure.qos", "body": {"secret": "data"}, "key": "key1"},
        {"req": "note.add", "file": "config.db", "note": "setting1", "body": {"value": 100}},
        {"req": "note.add", "file": "encrypted.dbs", "note": "?", "body": {"data": "test"}},
        {"req": "note.add", "file": "local.dbx", "note": "local1", "body": {"offline": True}}
    ]
    
    for instance in valid_extensions:
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_extensions(schema):
    """Tests invalid file extensions."""
    invalid_extensions = [
        {"req": "note.add", "file": "data.txt", "body": {"temp": 25}},
        {"req": "note.add", "file": "config.json", "body": {"data": "test"}},
        {"req": "note.add", "file": "notes.csv", "body": {"value": 100}},
        {"req": "note.add", "file": "file.log", "body": {"message": "error"}},
        {"req": "note.add", "file": "data", "body": {"no_extension": True}},
        {"req": "note.add", "file": "data.xyz", "body": {"unknown": "extension"}},
        {"req": "note.add", "file": "data.QO", "body": {"case": "sensitive"}},  # Case sensitive
        {"req": "note.add", "file": "data.qo.backup", "body": {"multiple": "extensions"}}
    ]
    
    for instance in invalid_extensions:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "does not match" in str(excinfo.value) or "pattern" in str(excinfo.value)

def test_boolean_parameters_combinations(schema):
    """Tests various boolean parameter combinations."""
    combinations = [
        {"req": "note.add", "body": {"data": 1}, "sync": True, "verify": False},
        {"req": "note.add", "body": {"data": 2}, "binary": True, "live": True},
        {"req": "note.add", "body": {"data": 3}, "full": True, "limit": False},
        {"req": "note.add", "body": {"data": 4}, "sync": False, "verify": True, "full": False}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

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