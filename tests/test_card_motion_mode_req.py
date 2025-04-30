import pytest
import jsonschema

SCHEMA_FILE = "card.motion.mode.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.motion.mode"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.motion.mode"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"start": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.motion.mode", "cmd": "card.motion.mode"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_start(schema):
    """Tests valid start field."""
    instance = {"req": "card.motion.mode", "start": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.mode", "start": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_start_invalid_type(schema):
    """Tests invalid type for start."""
    instance = {"req": "card.motion.mode", "start": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_stop(schema):
    """Tests valid stop field."""
    instance = {"req": "card.motion.mode", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.mode", "stop": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_stop_invalid_type(schema):
    """Tests invalid type for stop."""
    instance = {"req": "card.motion.mode", "stop": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"req": "card.motion.mode", "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.mode", "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.mode", "seconds": -10} # Allows negative?
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "card.motion.mode", "seconds": "60"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'60' is not of type 'integer'" in str(excinfo.value)

def test_valid_sensitivity(schema):
    """Tests valid sensitivity field."""
    instance = {"req": "card.motion.mode", "sensitivity": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.mode", "sensitivity": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.mode", "sensitivity": -1} # Allows negative?
    jsonschema.validate(instance=instance, schema=schema)

def test_sensitivity_invalid_type(schema):
    """Tests invalid type for sensitivity."""
    instance = {"req": "card.motion.mode", "sensitivity": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_start_with_settings(schema):
    """Tests valid start request with seconds and sensitivity."""
    instance = {"req": "card.motion.mode", "start": True, "seconds": 30, "sensitivity": 2}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_stop_request(schema):
    """Tests valid stop request."""
    instance = {"req": "card.motion.mode", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {
        "req": "card.motion.mode",
        "start": True,
        "stop": False,
        "seconds": 15,
        "sensitivity": 8
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.motion.mode", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
