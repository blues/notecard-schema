import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.status.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests a valid empty response."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status_response(schema):
    """Tests valid response with status field."""
    instance = {"status": "{ntn-idle}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_error_response(schema):
    """Tests valid response with error field."""
    instance = {"err": "no NTN module is connected {no-ntn-module}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status_with_location_info(schema):
    """Tests valid response with detailed status including location."""
    instance = {"status": "{ntn-idle}{ntn-unknown-location}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_response_combinations(schema):
    """Tests various valid response combinations."""
    valid_responses = [
        {},  # Empty response
        {"status": "{ntn-idle}"},
        {"status": "{ntn-connecting}"},
        {"status": "{ntn-idle}{ntn-unknown-location}"},
        {"status": "{ntn-transmitting}{ntn-location-known}"},
        {"err": "no NTN module is connected {no-ntn-module}"},
        {"err": "connection timeout"},
        {"status": "{ntn-idle}", "err": "warning message"},  # Both fields allowed
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_invalid_status_type(schema):
    """Tests invalid type for status field."""
    invalid_status_types = [
        {"status": 123},
        {"status": True},
        {"status": []},
        {"status": {}}
    ]
    
    for instance in invalid_status_types:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_err_type(schema):
    """Tests invalid type for err field."""
    invalid_err_types = [
        {"err": 123},
        {"err": True},
        {"err": []},
        {"err": {}}
    ]
    
    for instance in invalid_err_types:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {
        "status": "{ntn-idle}",
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid response with multiple additional properties."""
    instance = {
        "status": "{ntn-idle}",
        "connected": True,
        "time": 1640995200
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_starnote_status_responses(schema):
    """Tests realistic Starnote status response scenarios."""
    scenarios = [
        # Standard idle status
        {"status": "{ntn-idle}"},
        # Connection error
        {"err": "no NTN module is connected {no-ntn-module}"},
        # Status with location info
        {"status": "{ntn-idle}{ntn-unknown-location}"},
        # Transmitting status
        {"status": "{ntn-transmitting}"},
        # Multiple status flags
        {"status": "{ntn-connecting}{ntn-location-known}"},
        # Empty response (no status available)
        {}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_error_scenarios(schema):
    """Tests various error response scenarios."""
    error_scenarios = [
        {"err": "no NTN module is connected {no-ntn-module}"},
        {"err": "connection timeout"},
        {"err": "authentication failed"},
        {"err": "satellite not in range"},
        {"err": "hardware error"}
    ]
    
    for scenario in error_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_status_flag_patterns(schema):
    """Tests various status flag patterns."""
    status_patterns = [
        {"status": "{ntn-idle}"},
        {"status": "{ntn-connecting}"},
        {"status": "{ntn-transmitting}"},
        {"status": "{ntn-receiving}"},
        {"status": "{ntn-unknown-location}"},
        {"status": "{ntn-location-known}"},
        {"status": "{ntn-idle}{ntn-unknown-location}"},
        {"status": "{ntn-connecting}{ntn-location-known}"},
        {"status": "{ntn-transmitting}{ntn-location-known}"}
    ]
    
    for pattern in status_patterns:
        jsonschema.validate(instance=pattern, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_optional_fields_validation(schema):
    """Tests that all response fields are optional."""
    # All these should be valid since all fields are optional
    valid_responses = [
        {},  # No fields
        {"status": "{ntn-idle}"},  # Only status
        {"err": "error message"},  # Only err
        {"status": "{ntn-idle}", "err": "warning"}  # Both fields
    ]
    
    for response in valid_responses:
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