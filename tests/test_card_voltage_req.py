import pytest
import jsonschema

SCHEMA_FILE = "card.voltage.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.voltage"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.voltage"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"hours": 24}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.voltage", "cmd": "card.voltage"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_hours(schema):
    """Tests valid hours field."""
    instance = {"req": "card.voltage", "hours": 720}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "hours": 1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "hours": 0} # Allowed?
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "hours": -1} # Allowed?
    jsonschema.validate(instance=instance, schema=schema)

def test_hours_invalid_type(schema):
    """Tests invalid type for hours."""
    instance = {"req": "card.voltage", "hours": "24"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'24' is not of type 'integer'" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = ["default", "lipo", "l91", "alkaline", "tad", "lic", "?"]
    for mode in valid_modes:
        instance = {"req": "card.voltage", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.voltage", "mode": "nimh"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'nimh' is not one of ['default'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.voltage", "mode": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_vmax(schema):
    """Tests valid vmax field."""
    instance = {"req": "card.voltage", "vmax": 4.2}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "vmax": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "vmax": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_vmax_invalid_type(schema):
    """Tests invalid type for vmax."""
    instance = {"req": "card.voltage", "vmax": "4.2"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'4.2' is not of type 'number'" in str(excinfo.value)

def test_valid_vmin(schema):
    """Tests valid vmin field."""
    instance = {"req": "card.voltage", "vmin": 3.0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "vmin": 2}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "vmin": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_vmin_invalid_type(schema):
    """Tests invalid type for vmin."""
    instance = {"req": "card.voltage", "vmin": "3.0"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3.0' is not of type 'number'" in str(excinfo.value)

def test_valid_mode_and_thresholds(schema):
    """Tests valid request with mode, vmax, and vmin."""
    instance = {"req": "card.voltage", "mode": "lipo", "vmax": 4.25, "vmin": 3.1}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {
        "req": "card.voltage",
        "hours": 48,
        "mode": "lipo",
        "offset": 12,
        "vmax": 4.5,
        "vmin": 2.5,
        "name": "voltage_config",
        "usb": True,
        "alert": True,
        "sync": True,
        "calibration": 0.35,
        "set": False
    }
    jsonschema.validate(instance=instance, schema=schema)

# Test new fields
def test_valid_offset(schema):
    """Tests valid offset field."""
    instance = {"req": "card.voltage", "offset": 24}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.voltage", "offset": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_name(schema):
    """Tests valid name field."""
    instance = {"req": "card.voltage", "name": "voltage_settings"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_usb_monitoring_fields(schema):
    """Tests valid USB monitoring fields."""
    instance = {"req": "card.voltage", "usb": True, "alert": True, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)
    
def test_valid_calibration_fields(schema):
    """Tests valid calibration fields."""
    instance = {"req": "card.voltage", "calibration": 0.35, "set": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_hours_maximum_constraint(schema):
    """Tests hours maximum constraint."""
    instance = {"req": "card.voltage", "hours": 720}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Test exceeding maximum
    instance = {"req": "card.voltage", "hours": 721}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "721 is greater than the maximum of 720" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.voltage", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    import json
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}")
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
