import pytest
import jsonschema

SCHEMA_FILE = "card.temp.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.temp"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.temp"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"minutes": 5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.temp", "cmd": "card.temp"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"req": "card.temp", "minutes": 15}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.temp", "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.temp", "minutes": -10} # Allowed?
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"req": "card.temp", "minutes": "15"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'15' is not of type 'integer'" in str(excinfo.value)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"req": "card.temp", "status": "{voltage-variable}"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.temp", "status": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"req": "card.temp", "status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_stop(schema):
    """Tests valid stop field."""
    instance = {"req": "card.temp", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.temp", "stop": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_stop_invalid_type(schema):
    """Tests invalid type for stop."""
    instance = {"req": "card.temp", "stop": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_valid_sync(schema):
    """Tests valid sync field."""
    instance = {"req": "card.temp", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.temp", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_sync_invalid_type(schema):
    """Tests invalid type for sync."""
    instance = {"req": "card.temp", "sync": "yes"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'yes' is not of type 'boolean'" in str(excinfo.value)

def test_valid_minutes_and_status(schema):
    """Tests valid request with minutes and status."""
    instance = {"req": "card.temp", "minutes": 30, "status": "v={voltage}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_stop_request(schema):
    """Tests valid stop request."""
    instance = {"req": "card.temp", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_request(schema):
    """Tests valid sync request."""
    instance = {"req": "card.temp", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {
        "req": "card.temp",
        "minutes": 60,
        "status": "{v}",
        "stop": False,
        "sync": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.temp", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
