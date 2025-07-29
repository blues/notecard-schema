import pytest
import jsonschema

SCHEMA_FILE = "note.template.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {
        "req": "note.template"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {
        "cmd": "note.template"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_missing_req_cmd(schema):
    """Tests invalid request missing both req and cmd."""
    instance = {
        "file": "test.qo"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # Should fail because neither 'req' nor 'cmd' is present

def test_valid_with_file(schema):
    """Tests valid request with file parameter."""
    instance = {
        "req": "note.template",
        "file": "data.qo"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_format(schema):
    """Tests valid request with format parameter."""
    instance = {
        "req": "note.template",
        "format": "compact"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests valid request with body parameter."""
    instance = {
        "req": "note.template",
        "body": {
            "readings": {
                "temp": 0,
                "humid": 0
            }
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_request(schema):
    """Tests valid request with all parameters."""
    instance = {
        "req": "note.template", 
        "file": "sensors.qo",
        "format": "compact",
        "body": {
            "temperature": 0.0,
            "humidity": 0.0,
            "pressure": 0.0
        },
        "length": 100
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_type(schema):
    """Tests invalid request with non-string file parameter."""
    instance = {
        "req": "note.template",
        "file": 123
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_invalid_format_type(schema):
    """Tests invalid request with non-string format parameter."""
    instance = {
        "req": "note.template",
        "format": True
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_invalid_body_type(schema):
    """Tests invalid request with non-object body parameter."""
    instance = {
        "req": "note.template",
        "body": []
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "[] is not of type 'object'" in str(excinfo.value)

def test_cmd_instead_of_req(schema):
    """Tests valid command instead of request."""
    instance = {
        "cmd": "note.template",
        "file": "data.qo",
        "body": {"type": "sensor"}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_properties(schema):
    """Tests that additional properties are not allowed."""
    instance = {
        "req": "note.template",
        "invalid_property": "should_fail"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_valid_verify_parameter(schema):
    """Tests valid request with verify parameter."""
    instance = {
        "req": "note.template",
        "verify": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_verify_type(schema):
    """Tests invalid request with non-boolean verify parameter."""
    instance = {
        "req": "note.template",
        "verify": "true"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_length_parameter(schema):
    """Tests valid request with length parameter."""
    instance = {
        "req": "note.template",
        "length": 250
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_length_type(schema):
    """Tests invalid request with non-integer length parameter."""
    instance = {
        "req": "note.template",
        "length": "250"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'250' is not of type 'integer'" in str(excinfo.value)

def test_invalid_length_negative(schema):
    """Tests invalid request with negative length parameter."""
    instance = {
        "req": "note.template",
        "length": -1
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_valid_delete_parameter(schema):
    """Tests valid request with delete parameter."""
    instance = {
        "req": "note.template",
        "delete": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_delete_type(schema):
    """Tests invalid request with non-boolean delete parameter."""
    instance = {
        "req": "note.template",
        "delete": 1
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_format_compact(schema):
    """Tests valid request with format=compact parameter."""
    instance = {
        "req": "note.template",
        "format": "compact"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_format_value(schema):
    """Tests invalid request with invalid format value."""
    instance = {
        "req": "note.template",
        "format": "invalid"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['compact']" in str(excinfo.value)