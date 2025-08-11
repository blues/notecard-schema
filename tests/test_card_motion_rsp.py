import pytest
import jsonschema
import json

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

def test_valid_status_orientation_values(schema):
    """Tests valid status field with orientation values."""
    instance = {"status": "face-up"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "face-down"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "portrait-up"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "portrait-down"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "landscape-right"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "landscape-left"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "angled"}
    jsonschema.validate(instance=instance, schema=schema)
    
def test_valid_status_comma_separated(schema):
    """Tests valid status field with comma-separated values."""
    instance = {"status": "face-up,portrait-up"}
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

def test_valid_movements_base36(schema):
    """Tests valid movements field with base-36 characters."""
    instance = {"movements": "520000000000000000000A"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"movements": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"movements": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_movements_invalid_type(schema):
    """Tests invalid type for movements."""
    instance = {"movements": 123456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123456 is not of type 'string'" in str(excinfo.value)

def test_valid_mode(schema):
    """Tests valid mode field."""
    instance = {"mode": "stopped"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "moving"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {
        "count": 17,
        "alert": True,
        "motion": 1599741952,
        "status": "face-up",
        "seconds": 5,
        "movements": "520000000000000000000A",
        "mode": "stopped"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_motion_unix_timestamp(schema):
    """Tests valid motion field with UNIX epoch time."""
    instance = {"motion": 1599741952}  # Example from API reference
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"motion": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_response_with_sampling(schema):
    """Tests valid response when using minutes sampling."""
    instance = {
        "count": 17,
        "status": "face-up",
        "alert": True,
        "motion": 1599741952,
        "seconds": 5,
        "movements": "520000000000000000000A"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_response_without_sampling(schema):
    """Tests valid response without minutes sampling."""
    instance = {
        "count": 5,
        "alert": False,
        "motion": 1599741900,
        "status": "portrait-up,angled",
        "mode": "moving"
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
