import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.gps.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests a valid empty response."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_starnote_gps_response(schema):
    """Tests valid response indicating Starnote is using its own GPS."""
    instance = {"off": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_notecard_gps_response(schema):
    """Tests valid response indicating Starnote is using Notecard's GPS."""
    instance = {"on": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_response_with_both_fields(schema):
    """Tests valid response with both on and off fields."""
    instance = {
        "on": False,
        "off": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_boolean_combinations(schema):
    """Tests various valid boolean combinations."""
    combinations = [
        {"on": True},
        {"on": False},
        {"off": True},
        {"off": False},
        {"on": True, "off": False},
        {"on": False, "off": True},
        {"on": False, "off": False},
        {"on": True, "off": True}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_valid_configuration_states(schema):
    """Tests various GPS configuration state responses."""
    states = [
        # Default state - Starnote using own GPS
        {"off": True},
        # Override state - Starnote using Notecard GPS
        {"on": True},
        # Explicit state with both values
        {"on": False, "off": True},
        {"on": True, "off": False}
    ]
    
    for state in states:
        jsonschema.validate(instance=state, schema=schema)

def test_invalid_on_type_string(schema):
    """Tests invalid string type for on field."""
    instance = {"on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_invalid_on_type_integer(schema):
    """Tests invalid integer type for on field."""
    instance = {"on": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_invalid_off_type_string(schema):
    """Tests invalid string type for off field."""
    instance = {"off": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_invalid_off_type_integer(schema):
    """Tests invalid integer type for off field."""
    instance = {"off": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {
        "on": True,
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid response with multiple additional properties."""
    instance = {
        "off": True,
        "extra1": 123,
        "extra2": "test"
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

def test_starnote_response_scenarios(schema):
    """Tests realistic Starnote GPS response scenarios."""
    scenarios = [
        # Default configuration response
        {"off": True},
        # Notecard GPS override enabled response  
        {"on": True},
        # Query response showing default state
        {"on": False, "off": True},
        # Query response showing override state
        {"on": True, "off": False},
        # Empty response (no configuration set)
        {}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_ntn_gps_state_responses(schema):
    """Tests NTN GPS state response scenarios."""
    ntn_responses = [
        # Starnote using own GPS for satellite communication
        {"off": True},
        # Starnote using Notecard GPS for better accuracy
        {"on": True},
        # Configuration query showing both states
        {"on": False, "off": True},
        {"on": True, "off": False}
    ]
    
    for response in ntn_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_boolean_field_edge_cases(schema):
    """Tests edge cases with boolean field values."""
    edge_cases = [
        {"on": True, "off": True},    # Both true (edge case)
        {"on": False, "off": False},  # Both false (edge case)
        {"on": True, "off": False},   # Consistent override state
        {"on": False, "off": True}    # Consistent default state
    ]
    
    for case in edge_cases:
        jsonschema.validate(instance=case, schema=schema)

def test_minimal_responses(schema):
    """Tests minimal valid response formats."""
    minimal_responses = [
        {},                # Empty response
        {"on": True},      # Only on field
        {"off": True},     # Only off field
        {"on": False},     # Only on field with false
        {"off": False}     # Only off field with false
    ]
    
    for response in minimal_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_response_field_validation(schema):
    """Tests that response field types are correctly validated."""
    # Valid boolean fields should pass
    valid_responses = [
        {"on": True}, {"on": False},
        {"off": True}, {"off": False}
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)
    
    # Invalid field types should fail
    invalid_field_types = [
        {"on": "invalid"}, {"off": "invalid"},
        {"on": 123}, {"off": 456},
        {"on": []}, {"off": {}}
    ]
    
    for invalid_response in invalid_field_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_response, schema=schema)

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
