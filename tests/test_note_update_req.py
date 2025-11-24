import pytest
import jsonschema
import json

SCHEMA_FILE = "note.update.req.notecard.api.json"

def test_valid_req_with_body(schema):
    """Tests a valid request with body."""
    instance = {"req": "note.update", "file": "my-settings.db", "note": "measurements", "body": {"interval": 60}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_body(schema):
    """Tests a valid command with body."""
    instance = {"cmd": "note.update", "file": "config.db", "note": "setting-1", "body": {"enabled": True}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_payload(schema):
    """Tests a valid request with payload."""
    instance = {"req": "note.update", "file": "data.db", "note": "sensor-1", "payload": "SGVsbG8gV29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_body_and_payload(schema):
    """Tests a valid request with both body and payload."""
    instance = {
        "req": "note.update", 
        "file": "config.db", 
        "note": "device-config", 
        "body": {"enabled": True}, 
        "payload": "YWRkaXRpb25hbERhdGE="
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_verify(schema):
    """Tests a valid request with verify parameter."""
    instance = {
        "req": "note.update", 
        "file": "template.db", 
        "note": "user-setting", 
        "body": {"theme": "dark"}, 
        "verify": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_api_reference_example(schema):
    """Tests the exact example from API reference."""
    instance = {
        "req": "note.update",
        "file": "my-settings.db",
        "note": "measurements",
        "body": {"interval": 60}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_db_file_extensions(schema):
    """Tests various valid database file extensions."""
    db_files = ["settings.db", "config.dbx", "cache.dbs", "template.db"]
    
    for db_file in db_files:
        instance = {"req": "note.update", "file": db_file, "note": "test-note", "body": {"data": "test"}}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_complex_body(schema):
    """Tests valid request with complex body object."""
    instance = {
        "req": "note.update",
        "file": "complex.db",
        "note": "config",
        "body": {
            "settings": {
                "display": {"brightness": 75, "contrast": 80},
                "network": {"ssid": "MyWifi", "connected": True}
            },
            "sensors": [
                {"type": "temperature", "enabled": True},
                {"type": "humidity", "enabled": False}
            ]
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_body(schema):
    """Tests valid request with empty body object."""
    instance = {"req": "note.update", "file": "data.db", "note": "empty-test", "body": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_base64_payloads(schema):
    """Tests various valid base64 payload patterns."""
    base64_patterns = [
        "SGVsbG8gV29ybGQ=",           # Hello World
        "VGhpcyBpcyBhIHRlc3Q=",       # This is a test
        "YWJjZGVmZ2hpamtsbW5vcA==",   # abcdefghijklmnop
        "MTIzNDU2Nzg5MA==",           # 1234567890
        ""                            # Empty string
    ]
    
    for payload in base64_patterns:
        instance = {"req": "note.update", "file": "data.db", "note": "test", "payload": payload}
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"file": "data.db", "note": "test", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "note.update", "cmd": "note.update", "file": "data.db", "note": "test", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "file": "data.db", "note": "test", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.update' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "file": "data.db", "note": "test", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.update' was expected" in str(excinfo.value)

def test_invalid_missing_file(schema):
    """Tests invalid request without required file parameter."""
    instance = {"req": "note.update", "note": "test", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)

def test_invalid_missing_note(schema):
    """Tests invalid request without required note parameter."""
    instance = {"req": "note.update", "file": "data.db", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note' is a required property" in str(excinfo.value)

def test_invalid_missing_body_and_payload(schema):
    """Tests invalid request without either body or payload."""
    instance = {"req": "note.update", "file": "data.db", "note": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # Should fail anyOf validation requiring either body or payload
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_file_invalid_type_integer(schema):
    """Tests invalid integer type for file."""
    instance = {"req": "note.update", "file": 123, "note": "test", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_boolean(schema):
    """Tests invalid boolean type for file."""
    instance = {"req": "note.update", "file": True, "note": "test", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_integer(schema):
    """Tests invalid integer type for note."""
    instance = {"req": "note.update", "file": "data.db", "note": 456, "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_array(schema):
    """Tests invalid array type for note."""
    instance = {"req": "note.update", "file": "data.db", "note": ["test-id"], "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_body_invalid_type_string(schema):
    """Tests invalid string type for body."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "body": "should be object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'should be object' is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_array(schema):
    """Tests invalid array type for body."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "body": ["array", "not", "object"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_payload_invalid_type_integer(schema):
    """Tests invalid integer type for payload."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "payload": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "12345 is not of type 'string'" in str(excinfo.value)

def test_payload_invalid_type_boolean(schema):
    """Tests invalid boolean type for payload."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "payload": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_verify_invalid_type_string(schema):
    """Tests invalid string type for verify."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "body": {"data": "test"}, "verify": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_verify_invalid_type_integer(schema):
    """Tests invalid integer type for verify."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "body": {"data": "test"}, "verify": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "body": {"data": "test"}, "extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "note.update", "file": "data.db", "note": "test", "body": {"data": "test"}, "extra1": 123, "extra2": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_database_update_scenarios(schema):
    """Tests typical database update scenarios."""
    scenarios = [
        {"req": "note.update", "file": "settings.db", "note": "config-1", "body": {"enabled": True}},
        {"req": "note.update", "file": "cache.dbx", "note": "temp-data", "payload": "dXBkYXRlZERhdGE="},
        {"cmd": "note.update", "file": "logs.db", "note": "error-123", "body": {"resolved": True}},
        {"req": "note.update", "file": "user-data.db", "note": "profile", "body": {"name": "John"}, "payload": "YXZhdGFy"}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_templated_notefile_scenarios(schema):
    """Tests scenarios for templated Notefiles with verify parameter."""
    templated_scenarios = [
        {"req": "note.update", "file": "template.db", "note": "user-1", "body": {"theme": "dark"}, "verify": True},
        {"cmd": "note.update", "file": "config-template.dbx", "note": "global-setting", "body": {"debug": False}, "verify": False},
        {"req": "note.update", "file": "user-template.db", "note": "preferences", "payload": "cHJlZnM=", "verify": True}
    ]
    
    for scenario in templated_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_edge_case_file_names(schema):
    """Tests edge case file naming patterns."""
    edge_case_files = [
        "a.db",                        # Short name
        "very-long-file-name.dbx",     # Long name
        "file_with_underscores.db",    # Underscores
        "file-with-dashes.dbx",        # Dashes
        "CamelCaseFile.db",           # CamelCase
        "123numeric.db",              # Starts with numbers
        "mixed-Case_123.dbx"          # Mixed format
    ]
    
    for filename in edge_case_files:
        instance = {"req": "note.update", "file": filename, "note": "test", "body": {"data": "test"}}
        jsonschema.validate(instance=instance, schema=schema)

def test_edge_case_note_ids(schema):
    """Tests edge case note ID patterns."""
    edge_case_notes = [
        "a",                          # Single character
        "123",                        # Numeric
        "note-with-many-dashes",      # Long with dashes
        "note_with_underscores",      # Underscores
        "CamelCaseNote",             # CamelCase
        "note.with.dots",            # Dots
        "note:with:colons",          # Colons
        "note/with/slashes"          # Slashes
    ]
    
    for note_id in edge_case_notes:
        instance = {"req": "note.update", "file": "test.db", "note": note_id, "body": {"data": "test"}}
        jsonschema.validate(instance=instance, schema=schema)

def test_boolean_verify_combinations(schema):
    """Tests various boolean combinations for verify parameter."""
    combinations = [
        {"req": "note.update", "file": "test.db", "note": "test", "body": {"data": 1}, "verify": True},
        {"req": "note.update", "file": "test.db", "note": "test", "body": {"data": 2}, "verify": False},
        {"cmd": "note.update", "file": "test.db", "note": "test", "payload": "dGVzdA==", "verify": True},
        {"cmd": "note.update", "file": "test.db", "note": "test", "payload": "dGVzdDI=", "verify": False}
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
