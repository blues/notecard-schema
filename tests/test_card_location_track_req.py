import pytest
import jsonschema

SCHEMA_FILE = "card.location.track.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.location.track"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.location.track"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"start": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.location.track", "cmd": "card.location.track"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_start(schema):
    """Tests valid start field."""
    instance = {"req": "card.location.track", "start": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.track", "start": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_start_invalid_type(schema):
    """Tests invalid type for start."""
    instance = {"req": "card.location.track", "start": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_heartbeat(schema):
    """Tests valid heartbeat field."""
    instance = {"req": "card.location.track", "heartbeat": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.track", "heartbeat": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_heartbeat_invalid_type(schema):
    """Tests invalid type for heartbeat."""
    instance = {"req": "card.location.track", "heartbeat": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_hours(schema):
    """Tests valid hours field."""
    instance = {"req": "card.location.track", "hours": 24}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.track", "hours": -60} # minutes
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.track", "hours": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_hours_invalid_type(schema):
    """Tests invalid type for hours."""
    instance = {"req": "card.location.track", "hours": "12"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'12' is not of type 'integer'" in str(excinfo.value)

def test_valid_sync(schema):
    """Tests valid sync field."""
    instance = {"req": "card.location.track", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.track", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_sync_invalid_type(schema):
    """Tests invalid type for sync."""
    instance = {"req": "card.location.track", "sync": "maybe"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'maybe' is not of type 'boolean'" in str(excinfo.value)

def test_valid_stop(schema):
    """Tests valid stop field."""
    instance = {"req": "card.location.track", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.track", "stop": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_stop_invalid_type(schema):
    """Tests invalid type for stop."""
    instance = {"req": "card.location.track", "stop": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_valid_file(schema):
    """Tests valid file field."""
    instance = {"req": "card.location.track", "file": "mylogs.qo"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.track", "file": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_file_invalid_type(schema):
    """Tests invalid type for file."""
    instance = {"req": "card.location.track", "file": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_valid_start_heartbeat_hours(schema):
    """Tests valid combination: start, heartbeat, hours."""
    instance = {"req": "card.location.track", "start": True, "heartbeat": True, "hours": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_stop_request(schema):
    """Tests valid stop request."""
    instance = {"req": "card.location.track", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {
        "req": "card.location.track",
        "start": True,
        "heartbeat": True,
        "hours": -30,
        "sync": True,
        "stop": False,
        "file": "custom_track.qo"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.location.track", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
