import pytest
import jsonschema

SCHEMA_FILE = "card.motion.track.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.motion.track"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.motion.track"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"start": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.motion.track", "cmd": "card.motion.track"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_start(schema):
    """Tests valid start field."""
    instance = {"req": "card.motion.track", "start": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "start": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_start_invalid_type(schema):
    """Tests invalid type for start."""
    instance = {"req": "card.motion.track", "start": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_stop(schema):
    """Tests valid stop field."""
    instance = {"req": "card.motion.track", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "stop": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_stop_invalid_type(schema):
    """Tests invalid type for stop."""
    instance = {"req": "card.motion.track", "stop": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"req": "card.motion.track", "minutes": 15}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "minutes": -10} # Allows negative?
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"req": "card.motion.track", "minutes": "15"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'15' is not of type 'integer'" in str(excinfo.value)

def test_valid_count(schema):
    """Tests valid count field."""
    instance = {"req": "card.motion.track", "count": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "count": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "count": -1} # Allows negative?
    jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"req": "card.motion.track", "count": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_threshold(schema):
    """Tests valid threshold field."""
    instance = {"req": "card.motion.track", "threshold": 3}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "threshold": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "threshold": -2} # Allows negative?
    jsonschema.validate(instance=instance, schema=schema)

def test_threshold_invalid_type(schema):
    """Tests invalid type for threshold."""
    instance = {"req": "card.motion.track", "threshold": "3"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3' is not of type 'integer'" in str(excinfo.value)

def test_valid_file(schema):
    """Tests valid file field."""
    instance = {"req": "card.motion.track", "file": "motion_logs.qo"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "file": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_file_invalid_type(schema):
    """Tests invalid type for file."""
    instance = {"req": "card.motion.track", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_now(schema):
    """Tests valid now field."""
    instance = {"req": "card.motion.track", "now": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion.track", "now": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_now_invalid_type(schema):
    """Tests invalid type for now."""
    instance = {"req": "card.motion.track", "now": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_start_with_params(schema):
    """Tests valid start request with parameters."""
    instance = {"req": "card.motion.track", "start": True, "minutes": 10, "count": 5, "threshold": 3, "file": "_motion.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_stop_request(schema):
    """Tests valid stop request."""
    instance = {"req": "card.motion.track", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_now_request(schema):
    """Tests valid now request."""
    instance = {"req": "card.motion.track", "now": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {
        "req": "card.motion.track",
        "start": True,
        "stop": False,
        "minutes": 5,
        "count": 10,
        "threshold": 2,
        "file": "custom_motion.qo",
        "now": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.motion.track", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
