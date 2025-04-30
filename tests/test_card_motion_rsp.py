import pytest
import jsonschema

SCHEMA_FILE = "card.motion.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_count(schema):
    """Tests valid count field."""
    instance = {"count": 10}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"count": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"count": "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"status": "{motion-status-string}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_valid_alert(schema):
    """Tests valid alert field."""
    instance = {"alert": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"alert": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_alert_invalid_type(schema):
    """Tests invalid type for alert."""
    instance = {"alert": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_motion(schema):
    """Tests valid motion field."""
    instance = {"motion": 1700000000}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"motion": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_motion_invalid_type(schema):
    """Tests invalid type for motion."""
    instance = {"motion": 1700000000.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1700000000.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"seconds": "300"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'300' is not of type 'integer'" in str(excinfo.value)

def test_valid_movements(schema):
    """Tests valid movements field."""
    instance = {"movements": "0,1,2,3,4,5"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"movements": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_movements_invalid_type(schema):
    """Tests invalid type for movements."""
    instance = {"movements": 123456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123456 is not of type 'string'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {
        "count": 5,
        "status": "motion detected",
        "alert": False,
        "motion": 1700000123,
        "seconds": 12,
        "movements": "0,0,1,2,1,1"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"status": "ok", "orientation": "flat"}
    jsonschema.validate(instance=instance, schema=schema)
