import pytest
import jsonschema

SCHEMA_FILE = "card.aux.serial.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "card.aux.serial"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "card.aux.serial"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "gps"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.aux.serial", "cmd": "card.aux.serial"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_valid(schema):
    """Tests valid mode enum values."""
    valid_modes = [
        "req", "gps", "notify", "notify,accel", "notify,signals",
        "notify,env", "notify,dfu"
    ]
    for mode in valid_modes:
        instance = {"req": "card.aux.serial", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.aux.serial", "mode": "invalid_mode"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid_mode' is not one of ['req'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.aux.serial", "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_with_mode(schema):
    """Tests a valid request including the mode field."""
    instance = {"req": "card.aux.serial", "mode": "notify,signals"}
    jsonschema.validate(instance=instance, schema=schema)
