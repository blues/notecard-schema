import pytest
import jsonschema
import json

SCHEMA_FILE = "card.monitor.req.notecard.api.json"


def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.monitor"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.monitor"}
    jsonschema.validate(instance=instance, schema=schema)


def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "green"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.monitor", "cmd": "card.monitor"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)


def test_valid_mode_green(schema):
    """Tests valid mode field with green."""
    instance = {"req": "card.monitor", "mode": "green"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_mode_red(schema):
    """Tests valid mode field with red."""
    instance = {"req": "card.monitor", "mode": "red"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_mode_yellow(schema):
    """Tests valid mode field with yellow."""
    instance = {"req": "card.monitor", "mode": "yellow"}
    jsonschema.validate(instance=instance, schema=schema)


def test_mode_invalid_value(schema):
    """Tests invalid value for mode."""
    instance = {"req": "card.monitor", "mode": "blue"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'blue' is not one of ['green', 'red', 'yellow']" in str(excinfo.value)


def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.monitor", "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)


def test_valid_count_positive(schema):
    """Tests valid count field with positive integer."""
    instance = {"req": "card.monitor", "count": 5}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_count_zero(schema):
    """Tests valid count field with zero (returns LED to default)."""
    instance = {"req": "card.monitor", "count": 0}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_count_large(schema):
    """Tests valid count field with large number."""
    instance = {"req": "card.monitor", "count": 1000}
    jsonschema.validate(instance=instance, schema=schema)


def test_count_invalid_negative(schema):
    """Tests invalid negative count."""
    instance = {"req": "card.monitor", "count": -2}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-2 is less than the minimum of -1" in str(excinfo.value)


def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"req": "card.monitor", "count": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)


def test_valid_usb_true(schema):
    """Tests valid usb field set to true."""
    instance = {"req": "card.monitor", "usb": True}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_usb_false(schema):
    """Tests valid usb field set to false."""
    instance = {"req": "card.monitor", "usb": False}
    jsonschema.validate(instance=instance, schema=schema)


def test_usb_invalid_type(schema):
    """Tests invalid type for usb."""
    instance = {"req": "card.monitor", "usb": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)


def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {"req": "card.monitor", "mode": "green", "count": 5, "usb": True}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_mode_count_combination(schema):
    """Tests valid mode and count combination."""
    instance = {"req": "card.monitor", "mode": "red", "count": 10}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_reset_led_behavior(schema):
    """Tests resetting LED to default behavior with count 0."""
    instance = {"req": "card.monitor", "mode": "yellow", "count": 0}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_usb_only_mode(schema):
    """Tests USB-only LED behavior configuration."""
    instance = {"req": "card.monitor", "usb": True}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_cmd_variant(schema):
    """Tests valid command variant with all fields."""
    instance = {"cmd": "card.monitor", "mode": "red", "count": 3, "usb": False}
    jsonschema.validate(instance=instance, schema=schema)


def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.monitor", "extra": "field"}
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
