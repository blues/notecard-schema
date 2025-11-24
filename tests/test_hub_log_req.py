import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.log.req.notecard.api.json"

def test_valid_req_with_text(schema):
    """Tests a minimal valid request with text."""
    instance = {"req": "hub.log", "text": "System status"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_text(schema):
    """Tests a minimal valid command with text."""
    instance = {"cmd": "hub.log", "text": "System status"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_only(schema):
    """Tests valid request with only req field."""
    instance = {"req": "hub.log"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_only(schema):
    """Tests valid command with only cmd field."""
    instance = {"cmd": "hub.log"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {
        "req": "hub.log",
        "text": "something is wrong!",
        "alert": True,
        "sync": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_alert_false(schema):
    """Tests valid request with alert false."""
    instance = {"req": "hub.log", "text": "System normal", "alert": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_false(schema):
    """Tests valid request with sync false."""
    instance = {"req": "hub.log", "text": "System normal", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_text_only(schema):
    """Tests valid request with only text parameter."""
    instance = {"req": "hub.log", "text": "Just logging something"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_alert_only(schema):
    """Tests valid request with only alert parameter."""
    instance = {"req": "hub.log", "alert": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_only(schema):
    """Tests valid request with only sync parameter."""
    instance = {"req": "hub.log", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_text(schema):
    """Tests valid request with empty text."""
    instance = {"req": "hub.log", "text": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_long_text(schema):
    """Tests valid request with long text."""
    long_text = "A" * 1000
    instance = {"req": "hub.log", "text": long_text}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"text": "some text"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "hub.log", "cmd": "hub.log", "text": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "text": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.log' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "text": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.log' was expected" in str(excinfo.value)

def test_text_invalid_type(schema):
    """Tests invalid type for text."""
    instance = {"req": "hub.log", "text": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_text_invalid_boolean(schema):
    """Tests invalid boolean type for text."""
    instance = {"req": "hub.log", "text": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_text_invalid_array(schema):
    """Tests invalid array type for text."""
    instance = {"req": "hub.log", "text": ["message"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_alert_invalid_type(schema):
    """Tests invalid type for alert."""
    instance = {"req": "hub.log", "alert": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_alert_invalid_integer(schema):
    """Tests invalid integer type for alert."""
    instance = {"req": "hub.log", "alert": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type(schema):
    """Tests invalid type for sync."""
    instance = {"req": "hub.log", "sync": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_integer(schema):
    """Tests invalid integer type for sync."""
    instance = {"req": "hub.log", "sync": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_req_invalid_type(schema):
    """Tests invalid type for req."""
    instance = {"req": 123, "text": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.log' was expected" in str(excinfo.value)

def test_cmd_invalid_type(schema):
    """Tests invalid type for cmd."""
    instance = {"cmd": ["hub.log"], "text": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.log' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "hub.log", "text": "test", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with an additional property."""
    instance = {"cmd": "hub.log", "text": "test", "invalid": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "hub.log", "text": "test", "extra1": 123, "extra2": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_valid_field_combinations(schema):
    """Tests valid requests with various field combinations."""
    combinations = [
        {"req": "hub.log", "text": "message", "alert": True},
        {"req": "hub.log", "text": "message", "sync": True},
        {"req": "hub.log", "alert": False, "sync": False},
        {"cmd": "hub.log", "text": "message", "alert": True, "sync": True},
        {"cmd": "hub.log", "alert": True},
        {"cmd": "hub.log", "sync": False}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_all_parameters_optional(schema):
    """Tests that all parameters except req/cmd are optional."""
    # Test individual optional parameters
    optional_params = [
        {"req": "hub.log", "text": "message"},
        {"req": "hub.log", "alert": True},
        {"req": "hub.log", "sync": False}
    ]
    
    for param_dict in optional_params:
        jsonschema.validate(instance=param_dict, schema=schema)

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
