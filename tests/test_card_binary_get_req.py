import pytest
import jsonschema

SCHEMA_FILE = "card.binary.get.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.binary.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.binary.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"cobs": 10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.binary.get", "cmd": "card.binary.get"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "card.binary"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "card.binary"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_cobs(schema):
    """Tests valid request with cobs."""
    instance = {"req": "card.binary.get", "cobs": 128}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.binary.get", "cobs": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_invalid_type(schema):
    """Tests invalid type for cobs."""
    instance = {"req": "card.binary.get", "cobs": "128"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'128' is not of type 'integer'" in str(excinfo.value)

def test_valid_with_offset(schema):
    """Tests valid request with offset."""
    instance = {"req": "card.binary.get", "offset": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.binary.get", "offset": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_offset_invalid_type(schema):
    """Tests invalid type for offset."""
    instance = {"req": "card.binary.get", "offset": 10.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "10.5 is not of type 'integer'" in str(excinfo.value)

def test_offset_invalid_minimum(schema):
    """Tests invalid offset minimum value."""
    instance = {"req": "card.binary.get", "offset": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_valid_with_length(schema):
    """Tests valid request with length."""
    instance = {"req": "card.binary.get", "length": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.binary.get", "length": 512}
    jsonschema.validate(instance=instance, schema=schema)

def test_length_invalid_type(schema):
    """Tests invalid type for length."""
    instance = {"req": "card.binary.get", "length": "512"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'512' is not of type 'integer'" in str(excinfo.value)

def test_length_invalid_minimum(schema):
    """Tests invalid length minimum value."""
    instance = {"req": "card.binary.get", "length": -10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-10 is less than the minimum of 0" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid request with all optional fields."""
    instance = {
        "req": "card.binary.get",
        "cobs": 128,
        "offset": 10,
        "length": 64
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.binary.get", "extra": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
