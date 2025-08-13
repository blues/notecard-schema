import pytest
import jsonschema
import json

SCHEMA_FILE = "note.delete.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests a valid empty response."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_minimal_response(schema):
    """Tests the minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_empty_response_from_api_reference(schema):
    """Tests the empty response structure as indicated by API reference."""
    # API reference shows <ResponseMembers /> which indicates empty response
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property_single(schema):
    """Tests invalid response with single additional property."""
    instance = {"extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_success(schema):
    """Tests invalid response with success property (removed from v0.2.1)."""
    instance = {"success": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"message": "deleted"},
        {"error": "none"},
        {"result": "success"},
        {"success": True},
        {"count": 1},
        {"timestamp": 1640995200},
        {"file": "data.db"},
        {"note": "test-id"},
        {"verify": True},
        {"deleted": True},
        {"total": 1},
        {"changes": 0}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"status": "ok", "message": "deleted", "success": True}
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
        "file", "note", "verify", "cmd", "req", "status", "error", 
        "message", "result", "data", "success", "code", "info", "warning",
        "timestamp", "count", "index", "position", "deleted", "total",
        "changes", "notes", "tracker", "max", "start", "stop", "delete", "reset"
    ]
    
    for prop in properties_to_test:
        instance = {prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_empty_object_variations(schema):
    """Tests various empty object representations."""
    empty_variations = [
        {},  # Standard empty object
    ]
    
    for empty_obj in empty_variations:
        jsonschema.validate(instance=empty_obj, schema=schema)

def test_response_consistency(schema):
    """Tests response consistency across different scenarios."""
    # All successful deletions should return empty response
    success_responses = [
        {},  # Standard success
        {},  # Another empty response
        {}   # Yet another empty response
    ]
    
    for response in success_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_schema_structure_validation(schema):
    """Tests that schema structure is correct."""
    # Verify required schema properties that are stable
    assert schema.get("type") == "object"
    assert schema.get("additionalProperties") is False
    assert isinstance(schema.get("properties"), dict)
    assert len(schema.get("properties")) == 0  # Empty properties for empty response

def test_error_scenarios_blocked(schema):
    """Tests that error response patterns are blocked."""
    # These would be error responses, not success responses
    error_patterns = [
        {"error": "Note not found"},
        {"err": "File does not exist"},
        {"status": "failed"},
        {"message": "Deletion failed"},
        {"result": "error"}
    ]
    
    for error_pattern in error_patterns:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=error_pattern, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_legacy_success_field_blocked(schema):
    """Tests that legacy success field is blocked in v0.2.1."""
    # The old v0.1.1 schema had a success field, but v0.2.1 should not
    legacy_responses = [
        {"success": True},
        {"success": False}
    ]
    
    for legacy_response in legacy_responses:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=legacy_response, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_request_fields_blocked(schema):
    """Tests that request fields are blocked in response."""
    request_fields = [
        {"req": "note.delete"},
        {"cmd": "note.delete"},
        {"file": "data.db"},
        {"note": "test-id"},
        {"verify": True}
    ]
    
    for request_field in request_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=request_field, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_other_api_response_fields_blocked(schema):
    """Tests that fields from other APIs are blocked."""
    other_api_fields = [
        {"total": 10},  # From note.changes
        {"changes": 5},  # From note.changes  
        {"notes": {}},  # From note.changes
        {"tracker": "test"},  # From note.changes
        {"body": {}},  # From note.get
        {"time": 1234567890},  # From note.get
        {"template": True}  # From note.add
    ]
    
    for other_field in other_api_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=other_field, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_database_operation_consistency(schema):
    """Tests response consistency for database operations."""
    # All database operations should have same response format
    db_operation_responses = [
        {},  # Delete from .db file
        {},  # Delete from .dbx file  
        {},  # Delete with verify=true
        {},  # Delete with verify=false
    ]
    
    for response in db_operation_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_templated_notefile_response_consistency(schema):
    """Tests response consistency for templated Notefile operations."""
    # Templated operations (with verify) should also return empty response
    templated_responses = [
        {},  # Templated delete with verify=true
        {},  # Templated delete with verify=false
    ]
    
    for response in templated_responses:
        jsonschema.validate(instance=response, schema=schema)

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

def test_api_reference_compliance(schema):
    """Tests compliance with API reference specification."""
    # API reference shows <ResponseMembers /> indicating empty response
    # This means successful deletion returns empty object
    api_compliant_response = {}
    jsonschema.validate(instance=api_compliant_response, schema=schema)

def test_schema_version_consistency(schema):
    """Tests that schema has expected structural elements."""
    assert "$schema" in schema
    assert "$id" in schema
    assert "title" in schema
    assert "description" in schema
    assert schema.get("type") == "object"
    assert schema.get("additionalProperties") is False
    assert "samples" in schema