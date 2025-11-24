import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.reset.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests the valid empty response as per API reference."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property_single(schema):
    """Tests invalid response with single additional property."""
    instance = {"extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_success(schema):
    """Tests invalid response with legacy success property."""
    instance = {"success": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"message": "reset complete"},
        {"error": "none"},
        {"result": "success"},
        {"reset": True},
        {"cleared": True},
        {"configuration": "reset"},
        {"starnote": False},
        {"ntn": True},
        {"timestamp": 1640995200}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"status": "ok", "message": "reset complete", "success": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    properties_to_test = [
        "success", "status", "error", "message", "result", "data", 
        "reset", "cleared", "configuration", "starnote", "ntn",
        "timestamp", "complete", "finished", "done", "ok"
    ]
    
    for prop in properties_to_test:
        instance = {prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)


def test_empty_properties_validation(schema):
    """Tests that response schema has empty properties and strict validation."""
    # Schema should have empty properties
    properties = schema.get("properties", {})
    assert properties == {}, f"Expected empty properties, got: {properties}"
    
    # Only empty object should be valid
    jsonschema.validate(instance={}, schema=schema)
    
    # Any fields should be invalid
    invalid_responses = [
        {"any_field": "value"},
        {"status": "success"}, 
        {"reset_complete": True}
    ]
    
    for response in invalid_responses:
        with pytest.raises(jsonschema.ValidationError):
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
