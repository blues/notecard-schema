import pytest
import jsonschema
import json

SCHEMA_FILE = "note.get.req.notecard.api.json"

def test_valid_req_minimal(schema):
    """Tests a minimal valid request with only req."""
    instance = {"req": "note.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_minimal(schema):
    """Tests a minimal valid command with only cmd."""
    instance = {"cmd": "note.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_file(schema):
    """Tests valid request with file parameter."""
    instance = {"req": "note.get", "file": "requests.qi"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_db_note(schema):
    """Tests valid request with DB file and note ID."""
    instance = {"req": "note.get", "file": "my-settings.db", "note": "measurements"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_delete(schema):
    """Tests valid request with delete parameter."""
    instance = {"req": "note.get", "file": "requests.qi", "delete": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_deleted(schema):
    """Tests valid request with deleted parameter."""
    instance = {"req": "note.get", "file": "config.db", "note": "old-setting", "deleted": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_decrypt(schema):
    """Tests valid request with decrypt parameter."""
    instance = {"req": "note.get", "file": "secure.qis", "decrypt": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_api_reference_examples(schema):
    """Tests the exact examples from API reference."""
    # Pop From QI example
    instance = {"req": "note.get", "file": "requests.qi", "delete": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Read from DB example
    instance = {"req": "note.get", "file": "my-settings.db", "note": "measurements"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_file_extensions(schema):
    """Tests various valid file extensions."""
    file_extensions = [
        "data.qi",      # Plaintext inbound queue
        "secure.qis",   # Encrypted inbound queue
        "config.db",    # Local database
        "cache.dbx"     # Local database extended
    ]
    
    for filename in file_extensions:
        instance = {"req": "note.get", "file": filename}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_parameters(schema):
    """Tests valid request with multiple parameters."""
    instance = {
        "req": "note.get",
        "file": "data.db",
        "note": "sensor-reading",
        "delete": False,
        "deleted": True,
        "decrypt": False
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_boolean_combinations(schema):
    """Tests various boolean parameter combinations."""
    combinations = [
        {"req": "note.get", "delete": True, "deleted": False},
        {"req": "note.get", "delete": False, "decrypt": True},
        {"req": "note.get", "deleted": True, "decrypt": False},
        {"req": "note.get", "delete": True, "deleted": True, "decrypt": True}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"file": "data.qi"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "note.get", "cmd": "note.get", "file": "data.qi"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "file": "data.qi"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.get' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "file": "data.qi"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'note.get' was expected" in str(excinfo.value)

def test_file_invalid_type_integer(schema):
    """Tests invalid integer type for file."""
    instance = {"req": "note.get", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_file_invalid_type_boolean(schema):
    """Tests invalid boolean type for file."""
    instance = {"req": "note.get", "file": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_integer(schema):
    """Tests invalid integer type for note."""
    instance = {"req": "note.get", "file": "data.db", "note": 456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_note_invalid_type_array(schema):
    """Tests invalid array type for note."""
    instance = {"req": "note.get", "file": "data.db", "note": ["test-id"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_delete_invalid_type_string(schema):
    """Tests invalid string type for delete."""
    instance = {"req": "note.get", "file": "data.qi", "delete": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_deleted_invalid_type_integer(schema):
    """Tests invalid integer type for deleted."""
    instance = {"req": "note.get", "file": "data.db", "deleted": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_decrypt_invalid_type_array(schema):
    """Tests invalid array type for decrypt."""
    instance = {"req": "note.get", "file": "secure.qis", "decrypt": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "note.get", "file": "data.qi", "extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "note.get", "file": "data.qi", "extra1": 123, "extra2": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_queue_file_scenarios(schema):
    """Tests scenarios specific to queue files."""
    queue_scenarios = [
        {"req": "note.get", "file": "incoming.qi"},
        {"req": "note.get", "file": "requests.qi", "delete": True},
        {"req": "note.get", "file": "encrypted.qis", "decrypt": True},
        {"cmd": "note.get", "file": "data.qi", "delete": True}
    ]
    
    for scenario in queue_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_database_file_scenarios(schema):
    """Tests scenarios specific to database files."""
    db_scenarios = [
        {"req": "note.get", "file": "settings.db", "note": "config-1"},
        {"req": "note.get", "file": "cache.dbx", "note": "temp-data", "delete": True},
        {"req": "note.get", "file": "archive.db", "note": "old-record", "deleted": True},
        {"cmd": "note.get", "file": "logs.db", "note": "error-123"}
    ]
    
    for scenario in db_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_encrypted_file_scenarios(schema):
    """Tests scenarios for encrypted files."""
    encrypted_scenarios = [
        {"req": "note.get", "file": "secure.qis", "decrypt": True},
        {"req": "note.get", "file": "private.qis", "delete": True, "decrypt": True},
        {"cmd": "note.get", "file": "confidential.qis", "decrypt": False}
    ]
    
    for scenario in encrypted_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_edge_case_file_names(schema):
    """Tests edge case file naming patterns."""
    edge_case_files = [
        "a.qi",                        # Short name
        "very-long-file-name.db",      # Long name
        "file_with_underscores.dbx",   # Underscores
        "file-with-dashes.qis",        # Dashes
        "CamelCaseFile.qi",           # CamelCase
        "123numeric.db",              # Starts with numbers
        "mixed-Case_123.qis"          # Mixed format
    ]
    
    for filename in edge_case_files:
        instance = {"req": "note.get", "file": filename}
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
        "note:with:colons"           # Colons
    ]
    
    for note_id in edge_case_notes:
        instance = {"req": "note.get", "file": "test.db", "note": note_id}
        jsonschema.validate(instance=instance, schema=schema)

def test_default_file_behavior(schema):
    """Tests behavior with default file parameter."""
    # Schema has default="data.qi" for file parameter
    minimal_requests = [
        {"req": "note.get"},
        {"cmd": "note.get"},
        {"req": "note.get", "delete": True},
        {"req": "note.get", "decrypt": False}
    ]
    
    for request in minimal_requests:
        jsonschema.validate(instance=request, schema=schema)

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