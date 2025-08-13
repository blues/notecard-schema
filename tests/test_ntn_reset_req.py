import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.reset.req.notecard.api.json"

def test_valid_req_reset_configuration(schema):
    """Tests a valid request to reset Starnote configuration."""
    instance = {
        "req": "ntn.reset"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_reset_configuration(schema):
    """Tests a valid command to reset Starnote configuration."""
    instance = {
        "cmd": "ntn.reset"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_minimal_requests(schema):
    """Tests minimal valid request and command formats."""
    valid_requests = [
        {"req": "ntn.reset"},
        {"cmd": "ntn.reset"}
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {
        "req": "ntn.reset",
        "cmd": "ntn.reset"
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {
        "req": "wrong.api"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'ntn.reset' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {
        "cmd": "wrong.api"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'ntn.reset' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {
        "req": "ntn.reset",
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {
        "req": "ntn.reset",
        "extra1": 123,
        "extra2": "test"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_parameters(schema):
    """Tests that no parameters are allowed beyond req/cmd."""
    invalid_parameters = [
        {"req": "ntn.reset", "force": True},
        {"req": "ntn.reset", "confirm": True},
        {"cmd": "ntn.reset", "reset": True},
        {"req": "ntn.reset", "mode": "full"},
        {"cmd": "ntn.reset", "type": "configuration"}
    ]
    
    for invalid_request in invalid_parameters:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=invalid_request, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_starnote_reset_scenarios(schema):
    """Tests realistic Starnote reset scenarios."""
    scenarios = [
        # Reset after Starnote testing
        {"req": "ntn.reset"},
        # Reset to clear Starnote configuration
        {"cmd": "ntn.reset"},
        # Return to cellular/Wi-Fi testing
        {"req": "ntn.reset"}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_ntn_testing_scenarios(schema):
    """Tests NTN testing reset scenarios."""
    ntn_scenarios = [
        # Clear Starnote configuration for cellular testing
        {"req": "ntn.reset"},
        # Reset for Wi-Fi NTN simulation
        {"cmd": "ntn.reset"},
        # Return to non-Starnote NTN mode
        {"req": "ntn.reset"}
    ]
    
    for scenario in ntn_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_configuration_reset_scenarios(schema):
    """Tests configuration reset use cases."""
    reset_scenarios = [
        # Reset persistent Starnote configuration
        {"req": "ntn.reset"},
        # Clear configuration that survives card.restore
        {"cmd": "ntn.reset"},
        # Enable testing mode after physical Starnote connection
        {"req": "ntn.reset"}
    ]
    
    for scenario in reset_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_request_type_validation(schema):
    """Tests that request must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_empty_object_invalid(schema):
    """Tests that empty object is invalid (requires req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_req_cmd_mutual_exclusion(schema):
    """Tests that req and cmd are mutually exclusive."""
    # Only req should pass
    jsonschema.validate(instance={"req": "ntn.reset"}, schema=schema)
    
    # Only cmd should pass  
    jsonschema.validate(instance={"cmd": "ntn.reset"}, schema=schema)
    
    # Both req and cmd should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"req": "ntn.reset", "cmd": "ntn.reset"}, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_parameter_less_api(schema):
    """Tests that ntn.reset requires no parameters beyond req/cmd."""
    # Valid parameterless requests
    valid_requests = [
        {"req": "ntn.reset"},
        {"cmd": "ntn.reset"}
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)
    
    # Any additional parameters should fail
    invalid_requests = [
        {"req": "ntn.reset", "any_param": "value"},
        {"cmd": "ntn.reset", "force": True},
        {"req": "ntn.reset", "mode": "test"}
    ]
    
    for request in invalid_requests:
        with pytest.raises(jsonschema.ValidationError):
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