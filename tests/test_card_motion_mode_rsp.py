import pytest
import jsonschema
import json

SCHEMA_FILE = "card.motion.mode.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"tracking_enabled": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('tracking_enabled' was unexpected)" in str(excinfo.value)

def test_start_property(schema):
    """Tests valid response with start boolean."""
    jsonschema.validate(instance={"start": True}, schema=schema)
    jsonschema.validate(instance={"start": False}, schema=schema)

def test_start_invalid_type(schema):
    """Tests that start rejects non-boolean."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"start": 1}, schema=schema)

def test_stop_property(schema):
    """Tests valid response with stop boolean."""
    jsonschema.validate(instance={"stop": True}, schema=schema)
    jsonschema.validate(instance={"stop": False}, schema=schema)

def test_stop_invalid_type(schema):
    """Tests that stop rejects non-boolean."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"stop": 1}, schema=schema)

def test_seconds_property(schema):
    """Tests valid response with seconds integer."""
    jsonschema.validate(instance={"seconds": 5}, schema=schema)
    jsonschema.validate(instance={"seconds": 0}, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests that seconds rejects non-integer."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"seconds": "5"}, schema=schema)

def test_motion_property(schema):
    """Tests valid response with motion integer."""
    jsonschema.validate(instance={"motion": 2}, schema=schema)
    jsonschema.validate(instance={"motion": 0}, schema=schema)

def test_motion_invalid_type(schema):
    """Tests that motion rejects non-integer."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"motion": "2"}, schema=schema)

def test_all_properties(schema):
    """Tests response with all properties present."""
    instance = {"start": True, "seconds": 5, "motion": 2}
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
