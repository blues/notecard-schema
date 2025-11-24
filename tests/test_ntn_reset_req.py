import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.reset.req.notecard.api.json"

def test_valid_requests(schema):
    """Tests valid request and command formats."""
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

def test_reset_scenarios(schema):
    """Tests realistic Starnote reset scenarios."""
    scenarios = [
        {"req": "ntn.reset"},  # Standard reset request
        {"cmd": "ntn.reset"},  # Reset command without response
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_request_type_validation(schema):
    """Tests that request must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_req_cmd_validation(schema):
    """Tests req/cmd mutual exclusion and empty object validation."""
    # Only req should pass
    jsonschema.validate(instance={"req": "ntn.reset"}, schema=schema)
    
    # Only cmd should pass  
    jsonschema.validate(instance={"cmd": "ntn.reset"}, schema=schema)
    
    # Both req and cmd should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"req": "ntn.reset", "cmd": "ntn.reset"}, schema=schema)
    
    # Empty object should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={}, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

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
