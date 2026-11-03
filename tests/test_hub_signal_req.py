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

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"extra": 30}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

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
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with additional property."""
    instance = {"cmd": "hub.signal", "timeout": 30}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "hub.signal", "extra1": 123, "extra2": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

def test_seconds_not_allowed(schema):
    """Tests that seconds is rejected, since hub.signal does not use it when receiving signals."""
    instance = {"req": "hub.signal", "seconds": 30}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

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
        assert "Unevaluated properties are not allowed" in str(excinfo.value)

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
