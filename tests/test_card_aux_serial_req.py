import pytest
import jsonschema
import json

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

def test_minutes_valid(schema):
    """Tests valid minutes values (integer >= 1)."""
    instance = {"req": "card.aux.serial", "minutes": 1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "minutes": 30}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "minutes": 1440}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"req": "card.aux.serial", "minutes": "30"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'30' is not of type 'integer'" in str(excinfo.value)

def test_minutes_invalid_minimum(schema):
    """Tests invalid minutes value (< 1)."""
    instance = {"req": "card.aux.serial", "minutes": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is less than the minimum of 1" in str(excinfo.value)

def test_minutes_invalid_float(schema):
    """Tests invalid float type for minutes."""
    instance = {"req": "card.aux.serial", "minutes": 30.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "30.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_with_mode_and_minutes(schema):
    """Tests a valid request with both mode and minutes."""
    instance = {"cmd": "card.aux.serial", "mode": "notify,dfu", "minutes": 60}
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
