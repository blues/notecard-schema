import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.signal.req.notecard.api.json"

def test_valid_req_only(schema):
    """Tests a minimal valid request with only req."""
    instance = {"req": "hub.signal"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_only(schema):
    """Tests a minimal valid command with only cmd."""
    instance = {"cmd": "hub.signal"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_seconds(schema):
    """Tests valid request with seconds parameter."""
    instance = {"req": "hub.signal", "seconds": 30}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_seconds(schema):
    """Tests valid command with seconds parameter."""
    instance = {"cmd": "hub.signal", "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_seconds_zero(schema):
    """Tests valid request with seconds set to zero."""
    instance = {"req": "hub.signal", "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_seconds_large_value(schema):
    """Tests valid request with large seconds value."""
    instance = {"req": "hub.signal", "seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_seconds_small_value(schema):
    """Tests valid request with small seconds value."""
    instance = {"req": "hub.signal", "seconds": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"seconds": 30}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "hub.signal", "cmd": "hub.signal"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.signal' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.signal' was expected" in str(excinfo.value)

def test_seconds_invalid_type_string(schema):
    """Tests invalid string type for seconds."""
    instance = {"req": "hub.signal", "seconds": "30"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'30' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_float(schema):
    """Tests invalid float type for seconds."""
    instance = {"req": "hub.signal", "seconds": 30.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "30.5 is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_boolean(schema):
    """Tests invalid boolean type for seconds."""
    instance = {"req": "hub.signal", "seconds": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_array(schema):
    """Tests invalid array type for seconds."""
    instance = {"req": "hub.signal", "seconds": [30]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_object(schema):
    """Tests invalid object type for seconds."""
    instance = {"req": "hub.signal", "seconds": {"value": 30}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_req_invalid_type_integer(schema):
    """Tests invalid integer type for req."""
    instance = {"req": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.signal' was expected" in str(excinfo.value)

def test_req_invalid_type_boolean(schema):
    """Tests invalid boolean type for req."""
    instance = {"req": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.signal' was expected" in str(excinfo.value)

def test_cmd_invalid_type_array(schema):
    """Tests invalid array type for cmd."""
    instance = {"cmd": ["hub.signal"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.signal' was expected" in str(excinfo.value)

def test_cmd_invalid_type_object(schema):
    """Tests invalid object type for cmd."""
    instance = {"cmd": {"api": "hub.signal"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.signal' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "hub.signal", "extra": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with additional property."""
    instance = {"cmd": "hub.signal", "timeout": 30}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "hub.signal", "extra1": 123, "extra2": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"body": {}},
        {"signal": "data"},
        {"timeout": 30},
        {"wait": True},
        {"mode": "sync"},
        {"continuous": True}
    ]
    
    for field_dict in invalid_fields:
        field_dict["req"] = "hub.signal"
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_seconds_optional_parameter(schema):
    """Tests that seconds parameter is optional."""
    # Test with and without seconds parameter
    instances = [
        {"req": "hub.signal"},
        {"req": "hub.signal", "seconds": 30},
        {"cmd": "hub.signal"},
        {"cmd": "hub.signal", "seconds": 60}
    ]
    
    for instance in instances:
        jsonschema.validate(instance=instance, schema=schema)

def test_seconds_negative_value(schema):
    """Tests that negative seconds values are allowed."""
    # JSON Schema doesn't restrict negative values by default
    instance = {"req": "hub.signal", "seconds": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_extreme_values(schema):
    """Tests seconds with extreme integer values."""
    extreme_values = [0, 1, 86400, 999999]  # 0 seconds to very large values
    for value in extreme_values:
        instance = {"req": "hub.signal", "seconds": value}
        jsonschema.validate(instance=instance, schema=schema)

def test_empty_request_invalid(schema):
    """Tests that completely empty request is invalid."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

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