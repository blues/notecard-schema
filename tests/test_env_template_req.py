import pytest
import jsonschema
import json

SCHEMA_FILE = "env.template.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "env.template"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "env.template"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"body": {"test": "value"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "env.template", "cmd": "env.template"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'env.template' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'env.template' was expected" in str(excinfo.value)

def test_valid_body_simple(schema):
    """Tests valid body with simple data types."""
    instance = {"req": "env.template", "body": {"env_var_int": 11, "env_var_string": "10"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_complex(schema):
    """Tests valid body with multiple data types."""
    instance = {
        "req": "env.template", 
        "body": {
            "enabled": True,
            "temperature": 23.5,
            "count": 42,
            "name": "sensor"
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_empty_object(schema):
    """Tests valid body with empty object."""
    instance = {"req": "env.template", "body": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_nested_object(schema):
    """Tests valid body with nested objects."""
    instance = {
        "req": "env.template", 
        "body": {
            "config": {"enabled": True, "rate": 10},
            "status": "active"
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_with_arrays(schema):
    """Tests valid body with array values."""
    instance = {
        "req": "env.template", 
        "body": {
            "sensors": [1, 2, 3],
            "names": ["temp", "pressure"]
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_body_invalid_type(schema):
    """Tests invalid type for body."""
    instance = {"req": "env.template", "body": "not-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-object' is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_array(schema):
    """Tests invalid array type for body."""
    instance = {"req": "env.template", "body": ["not", "object"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_integer(schema):
    """Tests invalid integer type for body."""
    instance = {"req": "env.template", "body": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'object'" in str(excinfo.value)

def test_body_optional(schema):
    """Tests that body field is optional."""
    instance = {"req": "env.template"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "env.template", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

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
