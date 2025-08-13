import pytest
import jsonschema
import json

SCHEMA_FILE = "note.template.req.notecard.api.json"

def test_valid_req_basic_template(schema):
    """Tests a valid request with basic template setup."""
    instance = {
        "req": "note.template",
        "file": "readings.qo",
        "body": {"new_vals": True, "temperature": 14.1, "humidity": 11, "pump_state": "4"}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_basic_template(schema):
    """Tests a valid command with basic template setup."""
    instance = {
        "cmd": "note.template",
        "file": "sensor-data.qo",
        "body": {"temperature": 23.5, "humidity": 65, "status": "active"}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"file": "test.qo", "body": {"data": "test"}}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {
        "req": "note.template",
        "cmd": "note.template",
        "file": "test.qo",
        "body": {"data": "test"}
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_missing_file(schema):
    """Tests invalid request without required file parameter."""
    instance = {
        "req": "note.template",
        "body": {"data": "test"}
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'file' is a required property" in str(excinfo.value)

def test_valid_with_format(schema):
    """Tests valid request with format parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "format": "compact"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests valid request with body parameter."""
    instance = {
        "req": "note.template",
        "file": "readings.qo",
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
        "file": "test.qo",
        "format": True
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_invalid_body_type(schema):
    """Tests invalid request with non-object body parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
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
        "file": "test.qo",
        "invalid_property": "should_fail"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_valid_verify_parameter(schema):
    """Tests valid request with verify parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "verify": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_verify_type(schema):
    """Tests invalid request with non-boolean verify parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "verify": "true"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_length_parameter(schema):
    """Tests valid request with length parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "length": 250
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_length_type(schema):
    """Tests invalid request with non-integer length parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "length": "250"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'250' is not of type 'integer'" in str(excinfo.value)

def test_valid_length_negative_one(schema):
    """Tests valid request with length=-1 (now allowed in schema)."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "length": -1
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_delete_parameter(schema):
    """Tests valid request with delete parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "delete": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_delete_type(schema):
    """Tests invalid request with non-boolean delete parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "delete": 1
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_format_compact(schema):
    """Tests valid request with format=compact parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "format": "compact"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_length_too_negative(schema):
    """Tests invalid request with length less than -1."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "length": -2
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-2 is less than the minimum of -1" in str(excinfo.value)

def test_valid_port_parameter(schema):
    """Tests valid request with port parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "port": 50
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_port_type(schema):
    """Tests invalid request with non-integer port parameter."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "port": "50"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'50' is not of type 'integer'" in str(excinfo.value)

def test_invalid_port_too_low(schema):
    """Tests invalid request with port below minimum."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "port": 0
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is less than the minimum of 1" in str(excinfo.value)

def test_invalid_port_too_high(schema):
    """Tests invalid request with port above maximum."""
    instance = {
        "req": "note.template",
        "file": "test.qo",
        "port": 101
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "101 is greater than the maximum of 100" in str(excinfo.value)

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