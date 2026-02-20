import pytest
import jsonschema
import json

SCHEMA_FILE = "card.location.mode.rsp.notecard.api.json"

REQUIRED_FIELDS = {"threshold": 4}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only the required field."""
    instance = {"threshold": 4}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_threshold(schema):
    """Tests that 'threshold' is a required property."""
    instance = {"mode": "continuous"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'threshold' is a required property" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = ["continuous", "periodic", "off", "fixed"]
    for mode in valid_modes:
        instance = {**REQUIRED_FIELDS, "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {**REQUIRED_FIELDS, "mode": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['continuous'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {**REQUIRED_FIELDS, "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {**REQUIRED_FIELDS, "seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {**REQUIRED_FIELDS, "seconds": "3600"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3600' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_minimum(schema):
    """Tests invalid minimum for seconds."""
    instance = {**REQUIRED_FIELDS, "seconds": -10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-10 is less than the minimum of 0" in str(excinfo.value)

def test_valid_lat(schema):
    """Tests valid lat field."""
    instance = {**REQUIRED_FIELDS, "lat": 42.12345}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "lat": -90}
    jsonschema.validate(instance=instance, schema=schema)

def test_lat_invalid_type(schema):
    """Tests invalid type for lat."""
    instance = {**REQUIRED_FIELDS, "lat": "42.123"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'42.123' is not of type 'number'" in str(excinfo.value)

def test_valid_lon(schema):
    """Tests valid lon field."""
    instance = {**REQUIRED_FIELDS, "lon": -71.54321}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "lon": 180}
    jsonschema.validate(instance=instance, schema=schema)

def test_lon_invalid_type(schema):
    """Tests invalid type for lon."""
    instance = {**REQUIRED_FIELDS, "lon": "-71.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'-71.5' is not of type 'number'" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {**REQUIRED_FIELDS, "max": 600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "max": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {**REQUIRED_FIELDS, "max": 600.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "600.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "mode": "fixed",
        "seconds": 0,
        "lat": 40.7128,
        "lon": -74.0060,
        "max": 120,
        "threshold": 4
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_vseconds(schema):
    """Tests valid vseconds field."""
    instance = {**REQUIRED_FIELDS, "vseconds": "usb:3600;high:14400;normal:43200;low:86400;dead:0"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "vseconds": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_vseconds_invalid_type(schema):
    """Tests invalid type for vseconds."""
    instance = {**REQUIRED_FIELDS, "vseconds": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {**REQUIRED_FIELDS, "minutes": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {**REQUIRED_FIELDS, "minutes": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_threshold(schema):
    """Tests valid threshold field."""
    instance = {"threshold": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"threshold": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_threshold_invalid_type(schema):
    """Tests invalid type for threshold."""
    instance = {**REQUIRED_FIELDS, "threshold": "0"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'0' is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields_updated(schema):
    """Tests a valid response with all fields including new ones."""
    instance = {
        "mode": "continuous",
        "seconds": 0,
        "vseconds": "usb:60;high:300;normal:3600;low:14400;dead:0",
        "lat": 42.5776,
        "lon": -70.87134,
        "max": 100,
        "minutes": 2,
        "threshold": 4
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {**REQUIRED_FIELDS, "result": "success"}
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
