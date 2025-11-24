import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.gps.req.notecard.api.json"

def test_valid_req_enable_notecard_gps(schema):
    """Tests a valid request to enable Notecard GPS override."""
    instance = {
        "req": "ntn.gps",
        "on": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_enable_notecard_gps(schema):
    """Tests a valid command to enable Notecard GPS override."""
    instance = {
        "cmd": "ntn.gps",
        "on": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_use_starnote_gps(schema):
    """Tests a valid request to use Starnote's own GPS."""
    instance = {
        "req": "ntn.gps",
        "off": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_use_starnote_gps(schema):
    """Tests a valid command to use Starnote's own GPS."""
    instance = {
        "cmd": "ntn.gps",
        "off": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_query_configuration(schema):
    """Tests a valid request to query current GPS configuration."""
    instance = {
        "req": "ntn.gps"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_query_configuration(schema):
    """Tests a valid command to query current GPS configuration."""
    instance = {
        "cmd": "ntn.gps"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_both_parameters(schema):
    """Tests a valid request with both on and off parameters."""
    # Note: API allows both parameters to be present
    instance = {
        "req": "ntn.gps",
        "on": True,
        "off": False
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_boolean_combinations(schema):
    """Tests various valid boolean combinations."""
    combinations = [
        {"req": "ntn.gps", "on": True},
        {"req": "ntn.gps", "on": False},
        {"req": "ntn.gps", "off": True},
        {"req": "ntn.gps", "off": False},
        {"cmd": "ntn.gps", "on": True},
        {"cmd": "ntn.gps", "off": True},
        {"req": "ntn.gps", "on": True, "off": False},
        {"req": "ntn.gps", "on": False, "off": True}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"on": True}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {
        "req": "ntn.gps",
        "cmd": "ntn.gps",
        "on": True
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {
        "req": "wrong.api",
        "on": True
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'ntn.gps' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {
        "cmd": "wrong.api",
        "on": True
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'ntn.gps' was expected" in str(excinfo.value)

def test_invalid_on_type_string(schema):
    """Tests invalid string type for on parameter."""
    instance = {
        "req": "ntn.gps",
        "on": "true"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_invalid_on_type_integer(schema):
    """Tests invalid integer type for on parameter."""
    instance = {
        "req": "ntn.gps",
        "on": 1
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_invalid_off_type_string(schema):
    """Tests invalid string type for off parameter."""
    instance = {
        "req": "ntn.gps",
        "off": "true"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_invalid_off_type_integer(schema):
    """Tests invalid integer type for off parameter."""
    instance = {
        "req": "ntn.gps",
        "off": 1
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {
        "req": "ntn.gps",
        "on": True,
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {
        "req": "ntn.gps",
        "on": True,
        "extra1": 123,
        "extra2": "test"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_starnote_gps_scenarios(schema):
    """Tests realistic Starnote GPS configuration scenarios."""
    scenarios = [
        # Enable Notecard GPS override for better accuracy
        {
            "req": "ntn.gps",
            "on": True
        },
        # Return to default Starnote GPS
        {
            "cmd": "ntn.gps",
            "off": True
        },
        # Query current configuration
        {
            "req": "ntn.gps"
        },
        # Explicit configuration with both parameters
        {
            "req": "ntn.gps",
            "on": False,
            "off": True
        }
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_ntn_compatibility_scenarios(schema):
    """Tests NTN (satellite) specific GPS scenarios."""
    ntn_scenarios = [
        # Use Notecard GPS for satellite communication
        {
            "req": "ntn.gps",
            "on": True
        },
        # Use Starnote's dedicated GPS receiver
        {
            "req": "ntn.gps",
            "off": True
        },
        # Command to switch GPS source without response
        {
            "cmd": "ntn.gps",
            "on": True
        }
    ]
    
    for scenario in ntn_scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_edge_case_boolean_values(schema):
    """Tests edge cases with boolean values."""
    edge_cases = [
        {"req": "ntn.gps", "on": True, "off": False},
        {"req": "ntn.gps", "on": False, "off": True},
        {"cmd": "ntn.gps", "on": False, "off": False},
        {"cmd": "ntn.gps", "on": True, "off": True}
    ]
    
    for case in edge_cases:
        jsonschema.validate(instance=case, schema=schema)

def test_request_type_validation(schema):
    """Tests that request must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

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
