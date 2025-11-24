import pytest
import jsonschema
import json

SCHEMA_FILE = "card.trace.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.trace"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.trace"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "on"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.trace", "cmd": "card.trace"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_mode_on(schema):
    """Tests valid mode field set to 'on'."""
    instance = {"req": "card.trace", "mode": "on"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_off(schema):
    """Tests valid mode field set to 'off'."""
    instance = {"cmd": "card.trace", "mode": "off"}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_value(schema):
    """Tests invalid value for mode."""
    instance = {"req": "card.trace", "mode": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['on', 'off']" in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.trace", "mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_req_invalid_value(schema):
    """Tests invalid req value."""
    instance = {"req": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.trace' was expected" in str(excinfo.value)

def test_cmd_invalid_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.trace' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.trace", "mode": "on", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_trace_enable_request(schema):
    """Tests valid complete request to enable trace mode."""
    instance = {"req": "card.trace", "mode": "on"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_trace_disable_request(schema):
    """Tests valid complete request to disable trace mode."""
    instance = {"cmd": "card.trace", "mode": "off"}
    jsonschema.validate(instance=instance, schema=schema)

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
