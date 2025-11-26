import pytest
import jsonschema
import json

SCHEMA_FILE = "card.sleep.req.notecard.api.json"


def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.sleep"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.sleep"}
    jsonschema.validate(instance=instance, schema=schema)


def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.sleep", "cmd": "card.sleep"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)


def test_valid_on_field(schema):
    """Tests valid on field."""
    instance = {"req": "card.sleep", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.sleep", "on": False}
    jsonschema.validate(instance=instance, schema=schema)


def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {"req": "card.sleep", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)


def test_valid_off_field(schema):
    """Tests valid off field."""
    instance = {"cmd": "card.sleep", "off": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"cmd": "card.sleep", "off": False}
    jsonschema.validate(instance=instance, schema=schema)


def test_off_invalid_type(schema):
    """Tests invalid type for off."""
    instance = {"cmd": "card.sleep", "off": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)


def test_valid_seconds_field(schema):
    """Tests valid seconds field."""
    instance = {"req": "card.sleep", "seconds": -1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.sleep", "seconds": 30}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.sleep", "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.sleep", "seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)


def test_seconds_below_minimum(schema):
    """Tests seconds field below minimum value."""
    instance = {"req": "card.sleep", "seconds": 29}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "29 is not valid under any of the given schemas" in str(excinfo.value)


def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "card.sleep", "seconds": "60"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'60' is not of type 'integer'" in str(excinfo.value)


def test_seconds_invalid_float(schema):
    """Tests invalid float type for seconds."""
    instance = {"req": "card.sleep", "seconds": 60.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "60.5 is not of type 'integer'" in str(excinfo.value)


def test_valid_mode_field(schema):
    """Tests valid mode field."""
    instance = {"req": "card.sleep", "mode": "accel"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.sleep", "mode": "-accel"}
    jsonschema.validate(instance=instance, schema=schema)


def test_mode_invalid_value(schema):
    """Tests invalid value for mode."""
    instance = {"req": "card.sleep", "mode": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['accel', '-accel']" in str(excinfo.value)


def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.sleep", "mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)


def test_valid_all_fields_req(schema):
    """Tests valid request with all fields using 'req'."""
    instance = {"req": "card.sleep", "on": True, "seconds": 60, "mode": "accel"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_all_fields_cmd(schema):
    """Tests valid request with all fields using 'cmd'."""
    instance = {"cmd": "card.sleep", "off": True, "seconds": 30, "mode": "-accel"}
    jsonschema.validate(instance=instance, schema=schema)


def test_req_invalid_value(schema):
    """Tests invalid req value."""
    instance = {"req": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.sleep' was expected" in str(excinfo.value)


def test_cmd_invalid_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.sleep' was expected" in str(excinfo.value)


def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.sleep", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(
        excinfo.value
    )


def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(
                f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}"
            )
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
