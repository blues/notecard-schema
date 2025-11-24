import pytest
import jsonschema
import json

SCHEMA_FILE = "note.changes.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_field(schema):
    """Tests valid total field."""
    instance = {"total": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_changes_field(schema):
    """Tests valid changes field."""
    instance = {"changes": 5}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_notes_field(schema):
    """Tests valid empty notes field."""
    instance = {"notes": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_notes_with_single_entry(schema):
    """Tests valid notes field with single entry."""
    instance = {
        "notes": {
            "config-update": {
                "body": {"brightness": 75, "volume": 50},
                "time": 1609459200
            }
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_notes_with_multiple_entries(schema):
    """Tests valid notes field with multiple entries."""
    instance = {
        "notes": {
            "setting-one": {"body": {"foo": "bar"}, "time": 1598918235},
            "setting-two": {"body": {"foo": "bat"}, "time": 1598918245},
            "setting-three": {"body": {"foo": "baz"}, "time": 1598918225}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_response(schema):
    """Tests valid complete response with all fields."""
    instance = {
        "total": 4,
        "changes": 4,
        "notes": {
            "setting-one": {"body": {"foo": "bar"}, "time": 1598918235},
            "setting-two": {"body": {"foo": "bat"}, "time": 1598918245},
            "setting-three": {"body": {"foo": "baz"}, "time": 1598918225},
            "setting-four": {"body": {"foo": "foo"}, "time": 1598910532}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_no_changes_response(schema):
    """Tests valid response with no changes."""
    instance = {
        "changes": 0,
        "total": 10,
        "notes": {}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_partial_response_total_only(schema):
    """Tests valid response with only total field."""
    instance = {"total": 25}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_partial_response_changes_only(schema):
    """Tests valid response with only changes field."""
    instance = {"changes": 3}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_partial_response_notes_only(schema):
    """Tests valid response with only notes field."""
    instance = {
        "notes": {
            "test-note": {"body": {"test": "value"}, "time": 1640995200}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_total_invalid_type_string(schema):
    """Tests invalid string type for total."""
    instance = {"total": "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_type_boolean(schema):
    """Tests invalid boolean type for total."""
    instance = {"total": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_type_array(schema):
    """Tests invalid array type for total."""
    instance = {"total": [10]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_total_valid_zero(schema):
    """Tests valid zero total."""
    instance = {"total": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_total_valid_negative(schema):
    """Tests valid negative total (edge case)."""
    instance = {"total": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_changes_invalid_type_string(schema):
    """Tests invalid string type for changes."""
    instance = {"changes": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_type_boolean(schema):
    """Tests invalid boolean type for changes."""
    instance = {"changes": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_changes_invalid_type_array(schema):
    """Tests invalid array type for changes."""
    instance = {"changes": [5]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_changes_valid_zero(schema):
    """Tests valid zero changes."""
    instance = {"changes": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_changes_valid_negative(schema):
    """Tests valid negative changes (edge case)."""
    instance = {"changes": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_notes_invalid_type_string(schema):
    """Tests invalid string type for notes."""
    instance = {"notes": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not an object' is not of type 'object'" in str(excinfo.value)

def test_notes_invalid_type_array(schema):
    """Tests invalid array type for notes."""
    instance = {"notes": ["note1", "note2"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_notes_invalid_type_boolean(schema):
    """Tests invalid boolean type for notes."""
    instance = {"notes": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'object'" in str(excinfo.value)

def test_note_entry_missing_body(schema):
    """Tests invalid note entry missing required body field."""
    instance = {
        "notes": {
            "invalid-note": {"time": 1609459200}
        }
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'body' is a required property" in str(excinfo.value)

def test_note_entry_missing_time(schema):
    """Tests invalid note entry missing required time field."""
    instance = {
        "notes": {
            "invalid-note": {"body": {"test": "value"}}
        }
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'time' is a required property" in str(excinfo.value)

def test_note_entry_body_invalid_type_string(schema):
    """Tests invalid string type for note body."""
    instance = {
        "notes": {
            "invalid-note": {"body": "should be object", "time": 1609459200}
        }
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'should be object' is not of type 'object'" in str(excinfo.value)

def test_note_entry_body_invalid_type_array(schema):
    """Tests invalid array type for note body."""
    instance = {
        "notes": {
            "invalid-note": {"body": ["array", "not", "object"], "time": 1609459200}
        }
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_note_entry_time_invalid_type_string(schema):
    """Tests invalid string type for note time."""
    instance = {
        "notes": {
            "invalid-note": {"body": {"test": "value"}, "time": "1609459200"}
        }
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1609459200' is not of type 'integer'" in str(excinfo.value)

def test_note_entry_time_invalid_type_boolean(schema):
    """Tests invalid boolean type for note time."""
    instance = {
        "notes": {
            "invalid-note": {"body": {"test": "value"}, "time": True}
        }
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_note_entry_additional_properties_invalid(schema):
    """Tests invalid additional properties in note entries."""
    instance = {
        "notes": {
            "invalid-note": {
                "body": {"test": "value"},
                "time": 1609459200,
                "extra": "not allowed"
            }
        }
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_note_entry_valid_empty_body(schema):
    """Tests valid note entry with empty body object."""
    instance = {
        "notes": {
            "empty-body-note": {"body": {}, "time": 1609459200}
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_note_entry_valid_complex_body(schema):
    """Tests valid note entry with complex body object."""
    instance = {
        "notes": {
            "complex-note": {
                "body": {
                    "config": {
                        "display": {"brightness": 75, "contrast": 80},
                        "audio": {"volume": 50, "mute": False},
                        "network": {"ssid": "MyWifi", "connected": True}
                    },
                    "metadata": {
                        "version": "1.2.3",
                        "timestamp": "2021-01-01T00:00:00Z",
                        "tags": ["config", "user-settings", "device"]
                    }
                },
                "time": 1609459200
            }
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_note_entry_valid_time_formats(schema):
    """Tests valid time formats (all integers)."""
    valid_times = [0, 1, 1609459200, 2147483647, -1]  # Various valid integer timestamps
    
    for timestamp in valid_times:
        instance = {
            "notes": {
                f"time-test-{timestamp}": {"body": {"test": True}, "time": timestamp}
            }
        }
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"message": "changes retrieved"},
        {"error": "none"},
        {"result": "success"},
        {"count": 5},
        {"timestamp": 1640995200},
        {"tracker": "tracker-id"},
        {"file": "data.db"},
        {"max": 10},
        {"start": True},
        {"stop": False},
        {"deleted": True},
        {"delete": False},
        {"reset": True}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"status": "ok", "message": "retrieved", "extra": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
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

def test_response_is_object_type(schema):
    """Tests that response schema requires object type."""
    # String should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance="not an object", schema=schema)
    
    # Number should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=42, schema=schema)
    
    # Array should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=[], schema=schema)
    
    # Boolean should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=True, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    # Verify schema has additionalProperties: false
    assert schema.get("additionalProperties") is False

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    # Any additional property should be rejected
    properties_to_test = [
        "file", "tracker", "max", "start", "stop", "deleted", "delete", "reset",
        "cmd", "req", "status", "error", "message", "result", "data", "success",
        "code", "info", "warning", "timestamp", "count", "index", "position"
    ]
    
    for prop in properties_to_test:
        instance = {prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_field_combinations(schema):
    """Tests various valid field combinations."""
    combinations = [
        {"total": 1},
        {"changes": 2},
        {"notes": {}},
        {"total": 5, "changes": 2},
        {"total": 10, "notes": {}},
        {"changes": 3, "notes": {"note1": {"body": {"test": True}, "time": 1609459200}}},
        {"total": 4, "changes": 4, "notes": {"note1": {"body": {"a": 1}, "time": 123}, "note2": {"body": {"b": 2}, "time": 456}}}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_edge_case_values(schema):
    """Tests edge case values for fields."""
    edge_cases = [
        # Large values
        {"total": 2147483647, "changes": 1000000},
        # Zero values
        {"total": 0, "changes": 0},
        # Negative values (edge case)
        {"total": -1, "changes": -5},
        # Mixed scenarios
        {"total": 100, "changes": 0, "notes": {}},  # No changes but high total
        {"total": 0, "changes": 5, "notes": {}}     # Changes without total (edge case)
    ]
    
    for case in edge_cases:
        jsonschema.validate(instance=case, schema=schema)

def test_notes_key_variations(schema):
    """Tests various note key formats."""
    key_variations = {
        "simple": {"body": {"data": 1}, "time": 1609459200},
        "with-dashes": {"body": {"data": 2}, "time": 1609459201},
        "with_underscores": {"body": {"data": 3}, "time": 1609459202},
        "CamelCase": {"body": {"data": 4}, "time": 1609459203},
        "123numeric": {"body": {"data": 5}, "time": 1609459204},
        "mixed-Case_123": {"body": {"data": 6}, "time": 1609459205},
        "very_long_key_name_with_many_parts": {"body": {"data": 7}, "time": 1609459206},
        "": {"body": {"data": 8}, "time": 1609459207}  # Empty key
    }
    
    instance = {"notes": key_variations}
    jsonschema.validate(instance=instance, schema=schema)

def test_api_reference_example(schema):
    """Tests the exact example from API reference."""
    instance = {
        "changes": 4,
        "total": 4,
        "notes": {
            "setting-one": {"body": {"foo": "bar"}, "time": 1598918235},
            "setting-two": {"body": {"foo": "bat"}, "time": 1598918245},
            "setting-three": {"body": {"foo": "baz"}, "time": 1598918225},
            "setting-four": {"body": {"foo": "foo"}, "time": 1598910532}
        }
    }
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
