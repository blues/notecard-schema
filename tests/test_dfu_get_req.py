import pytest
import jsonschema
import json

SCHEMA_FILE = "dfu.get.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "dfu.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "dfu.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"length": 32, "offset": 32}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "dfu.get", "cmd": "dfu.get"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "invalid.req"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "invalid.cmd"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_length_and_offset(schema):
    """Tests valid length and offset values."""
    instance = {"req": "dfu.get", "length": 32, "offset": 32}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_length(schema):
    """Tests zero length for DFU mode verification."""
    instance = {"req": "dfu.get", "length": 0, "offset": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_length_invalid_type(schema):
    """Tests invalid type for length."""
    instance = {"req": "dfu.get", "length": "32"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_offset_invalid_type(schema):
    """Tests invalid type for offset."""
    instance = {"req": "dfu.get", "offset": "32"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "dfu.get", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

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
