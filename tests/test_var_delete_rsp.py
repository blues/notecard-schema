import pytest
import jsonschema
import json

SCHEMA_FILE = "var.delete.rsp.notecard.api.json"

def test_valid_success_response(schema):
    """Tests valid response with success field."""
    valid_responses = [
        {"success": True},
        {"success": False}
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_valid_empty_response(schema):
    """Tests valid empty response (success field is optional)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_success_type(schema):
    """Tests invalid type for success field."""
    invalid_success_types = [
        {"success": "true"},
        {"success": 1},
        {"success": 0},
        {"success": []},
        {"success": {}},
        {"success": None}
    ]
    
    for instance in invalid_success_types:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {
        "success": True,
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid response with multiple additional properties."""
    instance = {
        "success": True,
        "message": "deleted successfully",
        "timestamp": 1640995200
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"success": True, "status": "ok"},
        {"success": True, "message": "deleted"},
        {"success": True, "error": "none"},
        {"success": True, "result": "success"},
        {"success": True, "deleted": True},
        {"success": True, "name": "temperature"},
        {"success": True, "variable": "sensor_data"},
        {"success": True, "count": 1},
        {"success": True, "timestamp": 1640995200}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_variable_deletion_scenarios(schema):
    """Tests realistic variable deletion response scenarios."""
    scenarios = [
        {"success": True},   # Successful deletion
        {"success": False},  # Failed deletion (variable not found, etc.)
        {}                   # Empty response (success field optional)
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_success_field_optional(schema):
    """Tests that success field is optional."""
    # Response with success field
    jsonschema.validate(instance={"success": True}, schema=schema)
    jsonschema.validate(instance={"success": False}, schema=schema)
    
    # Response without success field should also be valid
    jsonschema.validate(instance={}, schema=schema)

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    properties_to_test = [
        "status", "error", "message", "result", "data", "deleted",
        "name", "variable", "count", "timestamp", "complete", "ok"
    ]
    
    for prop in properties_to_test:
        instance = {"success": True, prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_boolean_edge_cases(schema):
    """Tests edge cases for boolean success field."""
    valid_boolean_responses = [
        {"success": True},
        {"success": False}
    ]
    
    for response in valid_boolean_responses:
        jsonschema.validate(instance=response, schema=schema)
    
    # Test invalid boolean-like values
    invalid_boolean_responses = [
        {"success": "true"},
        {"success": "false"}, 
        {"success": 1},
        {"success": 0},
        {"success": "yes"},
        {"success": "no"}
    ]
    
    for response in invalid_boolean_responses:
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