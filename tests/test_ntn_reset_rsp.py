import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.reset.rsp.notecard.api.json"

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
    # API reference shows {} which indicates empty response
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
    invalid_types = [
        "string",
        123,
        True,
        False,
        ["array"]
    ]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

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

def test_empty_object_variations(schema):
    """Tests various empty object representations."""
    empty_variations = [
        {},  # Standard empty object
    ]
    
    for empty_obj in empty_variations:
        jsonschema.validate(instance=empty_obj, schema=schema)

def test_starnote_reset_response_scenarios(schema):
    """Tests realistic Starnote reset response scenarios."""
    scenarios = [
        # Standard successful reset response
        {},
        # API reference example response
        {}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_ntn_configuration_reset_responses(schema):
    """Tests NTN configuration reset response scenarios."""
    reset_responses = [
        # Configuration cleared successfully
        {},
        # Starnote configuration reset
        {},
        # Return to testing mode confirmed
        {}
    ]
    
    for response in reset_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_api_consistency_responses(schema):
    """Tests API consistency for reset responses."""
    consistent_responses = [
        # Empty response as per API reference
        {},
        # Minimal success indication (empty object)
        {}
    ]
    
    for response in consistent_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_configuration_clear_confirmations(schema):
    """Tests configuration clear confirmation responses."""
    confirmations = [
        # Persistent configuration cleared
        {},
        # Starnote presence configuration reset
        {},
        # Testing mode enabled
        {}
    ]
    
    for confirmation in confirmations:
        jsonschema.validate(instance=confirmation, schema=schema)

def test_no_properties_defined(schema):
    """Tests that response schema has empty properties."""
    properties = schema.get("properties", {})
    assert properties == {}, f"Expected empty properties, got: {properties}"

def test_parameterless_response_validation(schema):
    """Tests that response contains no data fields."""
    # Only empty object should be valid
    jsonschema.validate(instance={}, schema=schema)
    
    # Any fields should be invalid
    invalid_responses = [
        {"any_field": "value"},
        {"status": "success"},
        {"reset_complete": True},
        {"configuration_cleared": True}
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