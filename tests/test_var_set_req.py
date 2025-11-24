import pytest
import jsonschema
import json

SCHEMA_FILE = "var.set.req.notecard.api.json"

def test_valid_text_requests(schema):
    """Tests valid request formats with text parameter."""
    valid_requests = [
        {"req": "var.set", "name": "status", "text": "open"},
        {"cmd": "var.set", "name": "message", "text": "hello"},
        {"req": "var.set", "name": "status", "text": "active", "file": "sensors.db"},
        {"cmd": "var.set", "name": "config", "text": "enabled", "sync": True}
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_valid_value_requests(schema):
    """Tests valid request formats with value parameter."""
    valid_requests = [
        {"req": "var.set", "name": "temperature", "value": 23},
        {"cmd": "var.set", "name": "count", "value": 0},
        {"req": "var.set", "name": "humidity", "value": 65, "file": "sensors.db"},
        {"cmd": "var.set", "name": "reading", "value": -10, "sync": True}
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_valid_flag_requests(schema):
    """Tests valid request formats with flag parameter."""
    valid_requests = [
        {"req": "var.set", "name": "active", "flag": True},
        {"cmd": "var.set", "name": "enabled", "flag": False},
        {"req": "var.set", "name": "running", "flag": True, "file": "status.db"},
        {"cmd": "var.set", "name": "connected", "flag": False, "sync": True}
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"name": "status", "text": "open"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {
        "req": "var.set",
        "cmd": "var.set",
        "name": "status",
        "text": "open"
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {
        "req": "wrong.api",
        "name": "status",
        "text": "open"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'var.set' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {
        "cmd": "wrong.api",
        "name": "status",
        "text": "open"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'var.set' was expected" in str(excinfo.value)

def test_missing_name_parameter(schema):
    """Tests invalid request missing required name parameter."""
    invalid_requests = [
        {"req": "var.set", "text": "open"},
        {"cmd": "var.set", "value": 42},
        {"req": "var.set", "flag": True}
    ]
    
    for request in invalid_requests:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=request, schema=schema)

def test_missing_value_parameter(schema):
    """Tests invalid request missing required value parameter (text, value, or flag)."""
    invalid_requests = [
        {"req": "var.set", "name": "status"},
        {"cmd": "var.set", "name": "temperature"},
        {"req": "var.set", "name": "active", "file": "test.db"},
        {"cmd": "var.set", "name": "config", "sync": True}
    ]
    
    for request in invalid_requests:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=request, schema=schema)

def test_invalid_name_type(schema):
    """Tests invalid type for name parameter."""
    invalid_name_types = [
        {"req": "var.set", "name": 123, "text": "open"},
        {"req": "var.set", "name": True, "value": 42},
        {"req": "var.set", "name": [], "flag": False},
        {"req": "var.set", "name": {}, "text": "test"},
        {"cmd": "var.set", "name": None, "value": 10}
    ]
    
    for instance in invalid_name_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_type(schema):
    """Tests invalid type for file parameter."""
    invalid_file_types = [
        {"req": "var.set", "name": "test", "text": "value", "file": 123},
        {"req": "var.set", "name": "test", "value": 42, "file": True},
        {"req": "var.set", "name": "test", "flag": False, "file": []},
        {"req": "var.set", "name": "test", "text": "test", "file": {}},
        {"cmd": "var.set", "name": "test", "value": 10, "file": None}
    ]
    
    for instance in invalid_file_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_invalid_text_type(schema):
    """Tests invalid type for text parameter."""
    invalid_text_types = [
        {"req": "var.set", "name": "test", "text": 123},
        {"req": "var.set", "name": "test", "text": True},
        {"req": "var.set", "name": "test", "text": []},
        {"req": "var.set", "name": "test", "text": {}},
        {"cmd": "var.set", "name": "test", "text": None}
    ]
    
    for instance in invalid_text_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_invalid_value_type(schema):
    """Tests invalid type for value parameter."""
    invalid_value_types = [
        {"req": "var.set", "name": "test", "value": "123"},
        {"req": "var.set", "name": "test", "value": True},
        {"req": "var.set", "name": "test", "value": []},
        {"req": "var.set", "name": "test", "value": {}},
        {"cmd": "var.set", "name": "test", "value": None},
        {"req": "var.set", "name": "test", "value": 12.34}  # Should be integer
    ]
    
    for instance in invalid_value_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_invalid_flag_type(schema):
    """Tests invalid type for flag parameter."""
    invalid_flag_types = [
        {"req": "var.set", "name": "test", "flag": "true"},
        {"req": "var.set", "name": "test", "flag": 1},
        {"req": "var.set", "name": "test", "flag": 0},
        {"req": "var.set", "name": "test", "flag": []},
        {"req": "var.set", "name": "test", "flag": {}},
        {"cmd": "var.set", "name": "test", "flag": None}
    ]
    
    for instance in invalid_flag_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_invalid_sync_type(schema):
    """Tests invalid type for sync parameter."""
    invalid_sync_types = [
        {"req": "var.set", "name": "test", "text": "value", "sync": "true"},
        {"req": "var.set", "name": "test", "value": 42, "sync": 1},
        {"req": "var.set", "name": "test", "flag": True, "sync": 0},
        {"req": "var.set", "name": "test", "text": "test", "sync": []},
        {"cmd": "var.set", "name": "test", "value": 10, "sync": {}}
    ]
    
    for instance in invalid_sync_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_multiple_value_parameters(schema):
    """Tests requests with multiple value parameters (should be valid)."""
    valid_requests = [
        {"req": "var.set", "name": "test", "text": "hello", "value": 42},
        {"cmd": "var.set", "name": "test", "text": "active", "flag": True},
        {"req": "var.set", "name": "test", "value": 10, "flag": False},
        {"cmd": "var.set", "name": "test", "text": "data", "value": 25, "flag": True}
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_optional_parameters(schema):
    """Tests that file and sync parameters are optional."""
    valid_requests = [
        {"req": "var.set", "name": "status", "text": "open"},  # No optional params
        {"cmd": "var.set", "name": "count", "value": 5, "file": "data.db"},  # Only file
        {"req": "var.set", "name": "active", "flag": True, "sync": True},  # Only sync
        {"cmd": "var.set", "name": "temp", "value": 23, "file": "sensors.db", "sync": False}  # Both optional
    ]
    
    for request in valid_requests:
        jsonschema.validate(instance=request, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {
        "req": "var.set",
        "name": "status",
        "text": "open",
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {
        "req": "var.set",
        "name": "status",
        "text": "open",
        "force": True,
        "timeout": 30
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_variable_setting_scenarios(schema):
    """Tests various realistic variable setting scenarios."""
    scenarios = [
        {"req": "var.set", "name": "status", "text": "open"},
        {"req": "var.set", "name": "temperature", "value": 23, "file": "sensors.db"},
        {"req": "var.set", "name": "active", "flag": True, "sync": True},
        {"cmd": "var.set", "name": "humidity", "value": 65},
        {"cmd": "var.set", "name": "message", "text": "hello world", "file": "messages.db"},
        {"req": "var.set", "name": "enabled", "flag": False},
        {"cmd": "var.set", "name": "counter", "value": 0, "sync": False},
        {"req": "var.set", "name": "config", "text": "production", "file": "config.db", "sync": True}
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
    """Tests req/cmd mutual exclusion and required parameters."""
    # Valid requests with required parameters
    jsonschema.validate(instance={"req": "var.set", "name": "test", "text": "value"}, schema=schema)
    jsonschema.validate(instance={"cmd": "var.set", "name": "test", "value": 42}, schema=schema)
    
    # Both req and cmd should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"req": "var.set", "cmd": "var.set", "name": "test", "text": "value"}, schema=schema)
    
    # Empty object should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={}, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_empty_string_values(schema):
    """Tests empty string values for name and text."""
    valid_requests = [
        {"req": "var.set", "name": "", "text": "value"},
        {"req": "var.set", "name": "test", "text": ""},
        {"cmd": "var.set", "name": "", "text": "", "file": ""}
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
