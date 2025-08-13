import pytest
import jsonschema
import json

SCHEMA_FILE = "note.delete.req.notecard.api.json"

def test_valid_req_minimal(schema):
    """Tests a minimal valid request with required fields."""
    instance = {"req": "note.delete", "file": "data.db", "note": "test-id"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_minimal(schema):
    """Tests a minimal valid command with required fields."""
    instance = {"cmd": "note.delete", "file": "settings.db", "note": "config-id"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_verify_true(schema):
    """Tests valid request with verify parameter set to true."""
    instance = {"req": "note.delete", "file": "config.db", "note": "display-settings", "verify": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_verify_false(schema):
    """Tests valid request with verify parameter set to false."""
    instance = {"req": "note.delete", "file": "temp.db", "note": "sensor-data", "verify": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_verify(schema):
    """Tests valid command with verify parameter."""
    instance = {"cmd": "note.delete", "file": "cache.dbx", "note": "old-data", "verify": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_api_reference_example(schema):
    """Tests the exact example from API reference."""
    instance = {
        "req": "note.delete",
        "file": "my-settings.db",
        "note": "measurements"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_db_extensions(schema):
    """Tests various valid database file extensions."""
    db_files = ["data.db", "config.dbx", "settings.dbs", "cache.db"]
    
    for db_file in db_files:
        instance = {"req": "note.delete", "file": db_file, "note": "test-note"}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_note_id_variations(schema):
    """Tests various valid note ID formats."""
    note_ids = [
        "simple-id",
        "CamelCaseId", 
        "snake_case_id",
        "kebab-case-id",
        "123numeric",
        "mixed-Case_123",
        "very-long-note-id-with-many-parts",
        "a",  # Single character
        "note.with.dots"
    ]
    
    for note_id in note_ids:
        instance = {"req": "note.delete", "file": "test.db", "note": note_id}
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"file": "data.db", "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "note.delete", "cmd": "note.delete", "file": "data.db", "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "file": "data.db", "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.delete' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "file": "data.db", "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.delete' was expected" in str(excinfo.value)

def test_invalid_missing_file(schema):
    """Tests invalid request without required file parameter."""
    instance = {"req": "note.delete", "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)

def test_invalid_missing_note(schema):
    """Tests invalid request without required note parameter."""
    instance = {"req": "note.delete", "file": "data.db"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note' is a required property" in str(excinfo.value)

def test_invalid_missing_both_required(schema):
    """Tests invalid request without both required parameters."""
    instance = {"req": "note.delete"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)

def test_file_invalid_type_integer(schema):
    """Tests invalid integer type for file."""
    instance = {"req": "note.delete", "file": 123, "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_boolean(schema):
    """Tests invalid boolean type for file."""
    instance = {"req": "note.delete", "file": True, "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_array(schema):
    """Tests invalid array type for file."""
    instance = {"req": "note.delete", "file": ["data.db"], "note": "test-id"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_integer(schema):
    """Tests invalid integer type for note."""
    instance = {"req": "note.delete", "file": "data.db", "note": 456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_boolean(schema):
    """Tests invalid boolean type for note."""
    instance = {"req": "note.delete", "file": "data.db", "note": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_array(schema):
    """Tests invalid array type for note."""
    instance = {"req": "note.delete", "file": "data.db", "note": ["test-id"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_verify_invalid_type_string(schema):
    """Tests invalid string type for verify."""
    instance = {"req": "note.delete", "file": "data.db", "note": "test-id", "verify": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_verify_invalid_type_integer(schema):
    """Tests invalid integer type for verify."""
    instance = {"req": "note.delete", "file": "data.db", "note": "test-id", "verify": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_verify_invalid_type_array(schema):
    """Tests invalid array type for verify."""
    instance = {"req": "note.delete", "file": "data.db", "note": "test-id", "verify": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "note.delete", "file": "data.db", "note": "test-id", "extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with additional property."""
    instance = {"cmd": "note.delete", "file": "data.db", "note": "test-id", "unknown": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "note.delete", "file": "data.db", "note": "test-id", "extra1": 123, "extra2": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"result": "success"},
        {"error": "none"},
        {"message": "deleted"},
        {"success": True},
        {"count": 1},
        {"timestamp": 1640995200},
        {"notes": []},
        {"changes": 3}
    ]
    
    for field_dict in invalid_fields:
        field_dict["req"] = "note.delete"
        field_dict["file"] = "test.db"
        field_dict["note"] = "test-id"
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

def test_database_file_scenarios(schema):
    """Tests realistic database file scenarios."""
    scenarios = [
        {"req": "note.delete", "file": "sensor-data.db", "note": "temperature-001"},
        {"req": "note.delete", "file": "user-config.dbx", "note": "display-brightness"},
        {"req": "note.delete", "file": "system-logs.dbs", "note": "error-entry-123"},
        {"cmd": "note.delete", "file": "temp-cache.db", "note": "expired-session"},
        {"req": "note.delete", "file": "measurements.db", "note": "outlier-data", "verify": True}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_templated_notefile_scenarios(schema):
    """Tests scenarios specific to templated Notefiles."""
    # Templated files typically use verify parameter
    templated_scenarios = [
        {"req": "note.delete", "file": "template.db", "note": "old-template", "verify": True},
        {"cmd": "note.delete", "file": "config-template.dbx", "note": "deprecated-setting", "verify": False},
        {"req": "note.delete", "file": "user-template.db", "note": "user-123", "verify": True}
    ]
    
    for scenario in templated_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_edge_case_file_names(schema):
    """Tests edge case file naming patterns."""
    edge_case_files = [
        "a.db",  # Short name
        "very-long-file-name-with-many-parts.dbx",  # Long name
        "file_with_underscores.db",  # Underscores
        "file-with-dashes.dbx",  # Dashes
        "CamelCaseFile.db",  # CamelCase
        "123numeric.db",  # Starts with numbers
        "mixed-Case_123.dbx"  # Mixed format
    ]
    
    for filename in edge_case_files:
        instance = {"req": "note.delete", "file": filename, "note": "test-note"}
        jsonschema.validate(instance=instance, schema=schema)

def test_edge_case_note_ids(schema):
    """Tests edge case note ID patterns."""
    edge_case_notes = [
        "a",  # Single character
        "123",  # Numeric
        "note-with-many-dashes-and-parts",  # Long with dashes
        "note_with_underscores",  # Underscores
        "CamelCaseNote",  # CamelCase
        "note.with.dots",  # Dots
        "note:with:colons",  # Colons
        "note/with/slashes",  # Slashes
        "note@with@ats"  # At symbols
    ]
    
    for note_id in edge_case_notes:
        instance = {"req": "note.delete", "file": "test.db", "note": note_id}
        jsonschema.validate(instance=instance, schema=schema)

def test_field_combinations(schema):
    """Tests various valid field combinations."""
    combinations = [
        # Minimal required fields
        {"req": "note.delete", "file": "data.db", "note": "test"},
        {"cmd": "note.delete", "file": "data.db", "note": "test"},
        
        # With verify parameter
        {"req": "note.delete", "file": "data.db", "note": "test", "verify": True},
        {"req": "note.delete", "file": "data.db", "note": "test", "verify": False},
        {"cmd": "note.delete", "file": "data.db", "note": "test", "verify": True},
        {"cmd": "note.delete", "file": "data.db", "note": "test", "verify": False}
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