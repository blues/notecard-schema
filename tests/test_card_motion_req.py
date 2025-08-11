import pytest
import jsonschema
import json

SCHEMA_FILE = "card.motion.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.motion"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.motion"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"minutes": 5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.motion", "cmd": "card.motion"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"req": "card.motion", "minutes": 10}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion", "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion", "minutes": -5} # Allows negative?
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"req": "card.motion", "minutes": "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

def test_valid_with_minutes(schema):
    """Tests valid request with minutes field."""
    instance = {"req": "card.motion", "minutes": 15}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_minutes_positive(schema):
    """Tests valid positive minutes values."""
    instance = {"req": "card.motion", "minutes": 1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.motion", "minutes": 60}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_minutes(schema):
    """Tests valid command variant with minutes."""
    instance = {"cmd": "card.motion", "minutes": 5}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.motion", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

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
