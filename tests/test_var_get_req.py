import pytest
import jsonschema
import json

SCHEMA_FILE = "var.get.req.notecard.api.json"

def test_valid_requests(schema):
    """Tests valid request and command formats with name parameter."""
    valid_requests = [
        {"req": "var.get", "name": "status"},
        {"cmd": "var.get", "name": "temperature"},
        {"req": "var.get", "name": "sensor_data"},
        {"cmd": "var.get", "name": "config_value"},
        {"req": "var.get", "name": "status", "file": "sensors.db"},
        {"cmd": "var.get", "name": "data", "file": "vars.db"}
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"name": "status"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {
        "req": "var.get",
        "cmd": "var.get",
        "name": "status"
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {
        "req": "wrong.api",
        "name": "status"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'var.get' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {
        "cmd": "wrong.api",
        "name": "status"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'var.get' was expected" in str(excinfo.value)

def test_missing_name_parameter(schema):
    """Tests invalid request missing required name parameter."""
    invalid_requests = [
        {"req": "var.get"},
        {"cmd": "var.get"}
    ]
    
    for request in invalid_requests:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=request, schema=schema)

def test_invalid_name_type(schema):
    """Tests invalid type for name parameter."""
    invalid_name_types = [
        {"req": "var.get", "name": 123},
        {"req": "var.get", "name": True},
        {"req": "var.get", "name": []},
        {"req": "var.get", "name": {}},
        {"cmd": "var.get", "name": None}
    ]
    
    for instance in invalid_name_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_type(schema):
    """Tests invalid type for file parameter."""
    invalid_file_types = [
        {"req": "var.get", "name": "test", "file": 123},
        {"req": "var.get", "name": "test", "file": True},
        {"req": "var.get", "name": "test", "file": []},
        {"req": "var.get", "name": "test", "file": {}},
        {"cmd": "var.get", "name": "test", "file": None}
    ]
    
    for instance in invalid_file_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_file_parameter_optional(schema):
    """Tests that file parameter is optional."""
    valid_requests = [
        {"req": "var.get", "name": "status"},  # No file parameter
        {"cmd": "var.get", "name": "data"},    # No file parameter
        {"req": "var.get", "name": "temp", "file": "sensors.db"},  # With file
        {"cmd": "var.get", "name": "config", "file": "vars.db"}    # With file
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {
        "req": "var.get",
        "name": "status",
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {
        "req": "var.get",
        "name": "status",
        "force": True,
        "timeout": 30
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_variable_retrieval_scenarios(schema):
    """Tests various realistic variable retrieval scenarios."""
    scenarios = [
        {"req": "var.get", "name": "status"},
        {"req": "var.get", "name": "temperature", "file": "sensors.db"},
        {"req": "var.get", "name": "humidity"},
        {"req": "var.get", "name": "config_value", "file": "config.db"},
        {"req": "var.get", "name": "device_status"},
        {"cmd": "var.get", "name": "last_reading", "file": "data.db"},
        {"cmd": "var.get", "name": "system_info"},
        {"req": "var.get", "name": "user_preference", "file": "vars.db"}
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
    """Tests req/cmd mutual exclusion and name requirement."""
    # Only req with name should pass
    jsonschema.validate(instance={"req": "var.get", "name": "test"}, schema=schema)
    
    # Only cmd with name should pass  
    jsonschema.validate(instance={"cmd": "var.get", "name": "test"}, schema=schema)
    
    # Both req and cmd should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"req": "var.get", "cmd": "var.get", "name": "test"}, schema=schema)
    
    # Empty object should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={}, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_empty_name_string(schema):
    """Tests empty name string validation."""
    valid_requests = [
        {"req": "var.get", "name": ""},
        {"cmd": "var.get", "name": ""}
    ]
    
    for request in valid_requests:
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
