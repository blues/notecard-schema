import pytest
import jsonschema
import json

SCHEMA_FILE = "note.changes.req.notecard.api.json"

def test_valid_req_only_with_file(schema):
    """Tests a minimal valid request with only req and file."""
    instance = {"req": "note.changes", "file": "data.db"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_only_with_file(schema):
    """Tests a minimal valid command with only cmd and file."""
    instance = {"cmd": "note.changes", "file": "settings.db"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_tracker(schema):
    """Tests valid request with tracker parameter."""
    instance = {"req": "note.changes", "file": "my-settings.db", "tracker": "inbound-tracker"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_max(schema):
    """Tests valid request with max parameter."""
    instance = {"req": "note.changes", "file": "data.db", "max": 5}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_start(schema):
    """Tests valid request with start parameter."""
    instance = {"req": "note.changes", "file": "events.db", "tracker": "event-tracker", "start": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_stop(schema):
    """Tests valid request with stop parameter."""
    instance = {"req": "note.changes", "file": "logs.db", "tracker": "log-tracker", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_deleted(schema):
    """Tests valid request with deleted parameter."""
    instance = {"req": "note.changes", "file": "config.db", "tracker": "config-tracker", "deleted": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_delete(schema):
    """Tests valid request with delete parameter."""
    instance = {"req": "note.changes", "file": "temp.db", "delete": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_reset(schema):
    """Tests valid request with reset parameter."""
    instance = {"req": "note.changes", "file": "status.db", "tracker": "status-tracker", "reset": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_peek_example(schema):
    """Tests the peek example from API reference."""
    instance = {
        "req": "note.changes",
        "file": "my-settings.db",
        "tracker": "inbound-tracker", 
        "start": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_pop_example(schema):
    """Tests the pop example from API reference."""
    instance = {
        "req": "note.changes",
        "file": "my-settings.db",
        "tracker": "inbound-tracker",
        "start": True,
        "delete": True,
        "max": 2
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_all_parameters(schema):
    """Tests valid request with most parameters."""
    instance = {
        "req": "note.changes",
        "file": "comprehensive.db",
        "tracker": "comprehensive-tracker",
        "max": 10,
        "start": False,
        "deleted": True,
        "delete": False
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_variations(schema):
    """Tests valid command variations."""
    instance = {"cmd": "note.changes", "file": "cmd-test.db", "tracker": "cmd-tracker"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_boolean_combinations(schema):
    """Tests various boolean parameter combinations."""
    combinations = [
        {"req": "note.changes", "file": "test1.db", "start": True, "deleted": True},
        {"req": "note.changes", "file": "test2.db", "stop": True, "delete": False},
        {"req": "note.changes", "file": "test3.db", "reset": True, "start": False},
        {"req": "note.changes", "file": "test4.db", "deleted": False, "delete": True}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"file": "data.db"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "note.changes", "cmd": "note.changes", "file": "data.db"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "file": "data.db"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.changes' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "file": "data.db"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.changes' was expected" in str(excinfo.value)

def test_invalid_missing_file(schema):
    """Tests invalid request without required file parameter."""
    instance = {"req": "note.changes", "tracker": "test-tracker"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)

def test_file_invalid_type_integer(schema):
    """Tests invalid integer type for file."""
    instance = {"req": "note.changes", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_boolean(schema):
    """Tests invalid boolean type for file."""
    instance = {"req": "note.changes", "file": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_array(schema):
    """Tests invalid array type for file."""
    instance = {"req": "note.changes", "file": ["data.db"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_tracker_invalid_type_integer(schema):
    """Tests invalid integer type for tracker."""
    instance = {"req": "note.changes", "file": "data.db", "tracker": 456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_tracker_invalid_type_boolean(schema):
    """Tests invalid boolean type for tracker."""
    instance = {"req": "note.changes", "file": "data.db", "tracker": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_max_invalid_type_string(schema):
    """Tests invalid string type for max."""
    instance = {"req": "note.changes", "file": "data.db", "max": "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

def test_max_invalid_type_boolean(schema):
    """Tests invalid boolean type for max."""
    instance = {"req": "note.changes", "file": "data.db", "max": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_max_invalid_minimum_zero(schema):
    """Tests invalid zero value for max (minimum is 1)."""
    instance = {"req": "note.changes", "file": "data.db", "max": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is less than the minimum of 1" in str(excinfo.value)

def test_max_invalid_minimum_negative(schema):
    """Tests invalid negative value for max (minimum is 1)."""
    instance = {"req": "note.changes", "file": "data.db", "max": -5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-5 is less than the minimum of 1" in str(excinfo.value)

def test_max_valid_minimum_one(schema):
    """Tests valid minimum value for max (1)."""
    instance = {"req": "note.changes", "file": "data.db", "max": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_valid_large_value(schema):
    """Tests valid large value for max."""
    instance = {"req": "note.changes", "file": "data.db", "max": 1000}
    jsonschema.validate(instance=instance, schema=schema)

def test_start_invalid_type_string(schema):
    """Tests invalid string type for start."""
    instance = {"req": "note.changes", "file": "data.db", "start": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_start_invalid_type_integer(schema):
    """Tests invalid integer type for start."""
    instance = {"req": "note.changes", "file": "data.db", "start": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_stop_invalid_type_string(schema):
    """Tests invalid string type for stop."""
    instance = {"req": "note.changes", "file": "data.db", "stop": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_stop_invalid_type_integer(schema):
    """Tests invalid integer type for stop."""
    instance = {"req": "note.changes", "file": "data.db", "stop": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_deleted_invalid_type_string(schema):
    """Tests invalid string type for deleted."""
    instance = {"req": "note.changes", "file": "data.db", "deleted": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_deleted_invalid_type_integer(schema):
    """Tests invalid integer type for deleted."""
    instance = {"req": "note.changes", "file": "data.db", "deleted": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_delete_invalid_type_string(schema):
    """Tests invalid string type for delete."""
    instance = {"req": "note.changes", "file": "data.db", "delete": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_delete_invalid_type_integer(schema):
    """Tests invalid integer type for delete."""
    instance = {"req": "note.changes", "file": "data.db", "delete": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_reset_invalid_type_string(schema):
    """Tests invalid string type for reset."""
    instance = {"req": "note.changes", "file": "data.db", "reset": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_reset_invalid_type_integer(schema):
    """Tests invalid integer type for reset."""
    instance = {"req": "note.changes", "file": "data.db", "reset": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "note.changes", "file": "data.db", "extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with additional property."""
    instance = {"cmd": "note.changes", "file": "data.db", "unknown": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "note.changes", "file": "data.db", "extra1": 123, "extra2": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"result": "success"},
        {"error": "none"},
        {"message": "retrieved"},
        {"count": 5},
        {"timestamp": 1640995200},
        {"notes": []},
        {"changes": 3}
    ]
    
    for field_dict in invalid_fields:
        field_dict["req"] = "note.changes"
        field_dict["file"] = "test.db"
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_empty_object_invalid(schema):
    """Tests that empty object is invalid."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)

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

def test_tracker_operations(schema):
    """Tests tracker-related operations."""
    operations = [
        {"req": "note.changes", "file": "data.db", "tracker": "tracker1", "start": True},
        {"req": "note.changes", "file": "data.db", "tracker": "tracker2", "reset": True},
        {"req": "note.changes", "file": "data.db", "tracker": "tracker3", "stop": True},
        {"req": "note.changes", "file": "data.db", "tracker": "tracker4", "start": True, "delete": True}
    ]
    
    for operation in operations:
        jsonschema.validate(instance=operation, schema=schema)

def test_file_parameter_required(schema):
    """Tests that file parameter is always required."""
    # Test with req but no file
    instance = {"req": "note.changes", "tracker": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)
    
    # Test with cmd but no file
    instance = {"cmd": "note.changes", "max": 5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)

def test_database_file_patterns(schema):
    """Tests various database file naming patterns."""
    valid_files = [
        "settings.db",
        "config.dbs", 
        "events.dbx",
        "data.qo",
        "encrypted.qi",
        "simple-name.db",
        "complex_name_with_underscores.dbs",
        "name-with-dashes.dbx",
        "123numeric.db",
        "CamelCase.db"
    ]
    
    for filename in valid_files:
        instance = {"req": "note.changes", "file": filename}
        jsonschema.validate(instance=instance, schema=schema)

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
