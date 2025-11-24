import pytest
import jsonschema
import json

SCHEMA_FILE = "card.location.track.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_start(schema):
    """Tests valid start field."""
    instance = {"start": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"start": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_start_invalid_type(schema):
    """Tests invalid type for start."""
    instance = {"start": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_stop(schema):
    """Tests valid stop field."""
    instance = {"stop": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"stop": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_stop_invalid_type(schema):
    """Tests invalid type for stop."""
    instance = {"stop": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_heartbeat(schema):
    """Tests valid heartbeat field."""
    instance = {"heartbeat": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"heartbeat": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_heartbeat_invalid_type(schema):
    """Tests invalid type for heartbeat."""
    instance = {"heartbeat": "yes"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'yes' is not of type 'boolean'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 86400}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"seconds": "300"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'300' is not of type 'integer'" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"minutes": 120}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"minutes": 1440}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"minutes": 120.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "120.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_file(schema):
    """Tests valid file field."""
    instance = {"file": "_track.qo"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"file": "locations.qo"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"file": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_file_invalid_type(schema):
    """Tests invalid type for file."""
    instance = {"file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_complete_response(schema):
    """Tests valid response with all fields."""
    instance = {
        "start": True,
        "heartbeat": True,
        "file": "locations.qo",
        "minutes": 120,
        "seconds": 300
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_tracking_disabled_response(schema):
    """Tests valid response when tracking is disabled."""
    instance = {
        "stop": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_tracking_enabled_response(schema):
    """Tests valid response when tracking is enabled without heartbeat."""
    instance = {
        "start": True,
        "seconds": 600,
        "file": "_track.qo"
    }
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
