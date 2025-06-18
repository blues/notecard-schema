import pytest
import jsonschema
import json

SCHEMA_FILE = "card.power.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.power"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.power"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"minutes": 60}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.power", "cmd": "card.power"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"req": "card.power", "minutes": 720}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.power", "minutes": 60}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.power", "minutes": 1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.power", "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.power", "minutes": -1} # Test negative values
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"req": "card.power", "minutes": "60"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'60' is not of type 'integer'" in str(excinfo.value)

def test_minutes_invalid_float(schema):
    """Tests invalid float type for minutes."""
    instance = {"req": "card.power", "minutes": 60.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "60.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_reset(schema):
    """Tests valid reset field."""
    instance = {"cmd": "card.power", "reset": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"cmd": "card.power", "reset": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_reset_invalid_type(schema):
    """Tests invalid type for reset."""
    instance = {"cmd": "card.power", "reset": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_reset_invalid_number(schema):
    """Tests invalid number type for reset."""
    instance = {"cmd": "card.power", "reset": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_minutes_with_req(schema):
    """Tests valid request with minutes using 'req'."""
    instance = {"req": "card.power", "minutes": 60}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_reset_with_cmd(schema):
    """Tests valid request with reset using 'cmd'."""
    instance = {"cmd": "card.power", "reset": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields_req(schema):
    """Tests valid request with all fields using 'req'."""
    instance = {"req": "card.power", "minutes": 720, "reset": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields_cmd(schema):
    """Tests valid request with all fields using 'cmd'."""
    instance = {"cmd": "card.power", "minutes": 120, "reset": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.power", "extra": "field"}
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
