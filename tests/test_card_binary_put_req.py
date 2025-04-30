import pytest
import jsonschema

SCHEMA_FILE = "card.binary.put.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.binary.put"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.binary.put"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"offset": 10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.binary.put", "cmd": "card.binary.put"}
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

def test_valid_with_offset(schema):
    """Tests valid request with offset."""
    instance = {"req": "card.binary.put", "offset": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.binary.put", "offset": 2048}
    jsonschema.validate(instance=instance, schema=schema)

def test_offset_invalid_type(schema):
    """Tests invalid type for offset."""
    instance = {"req": "card.binary.put", "offset": "start"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'start' is not of type 'integer'" in str(excinfo.value)

def test_offset_invalid_minimum(schema):
    """Tests invalid offset minimum value."""
    instance = {"req": "card.binary.put", "offset": -5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-5 is less than the minimum of 0" in str(excinfo.value)

def test_valid_with_cobs(schema):
    """Tests valid request with cobs."""
    instance = {"req": "card.binary.put", "cobs": 128}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.binary.put", "cobs": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_invalid_type(schema):
    """Tests invalid type for cobs."""
    instance = {"req": "card.binary.put", "cobs": 128.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "128.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_with_status(schema):
    """Tests valid request with status."""
    instance = {"req": "card.binary.put", "status": "md5:abcdef0123456789"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.binary.put", "status": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"req": "card.binary.put", "status": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid request with all optional fields."""
    instance = {
        "req": "card.binary.put",
        "offset": 100,
        "cobs": 512,
        "status": "md5:1234567890abcdef"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.binary.put", "extra": "disallowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
