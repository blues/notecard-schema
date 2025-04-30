import pytest
import jsonschema

SCHEMA_FILE = "card.location.mode.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.location.mode"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.location.mode"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "off"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.location.mode", "cmd": "card.location.mode"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = ["", "off", "periodic", "continuous", "fixed"]
    for mode in valid_modes:
        instance = {"req": "card.location.mode", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.location.mode", "mode": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['', 'off'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.location.mode", "mode": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"req": "card.location.mode", "seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.mode", "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "card.location.mode", "seconds": "3600"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3600' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_minimum(schema):
    """Tests invalid minimum for seconds."""
    instance = {"req": "card.location.mode", "seconds": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_valid_vseconds(schema):
    """Tests valid vseconds field."""
    instance = {"req": "card.location.mode", "vseconds": "{expression}"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.mode", "vseconds": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_vseconds_invalid_type(schema):
    """Tests invalid type for vseconds."""
    instance = {"req": "card.location.mode", "vseconds": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_lat(schema):
    """Tests valid lat field."""
    instance = {"req": "card.location.mode", "lat": 42.12345}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.mode", "lat": -90}
    jsonschema.validate(instance=instance, schema=schema)

def test_lat_invalid_type(schema):
    """Tests invalid type for lat."""
    instance = {"req": "card.location.mode", "lat": "42.123"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'42.123' is not of type 'number'" in str(excinfo.value)

def test_valid_lon(schema):
    """Tests valid lon field."""
    instance = {"req": "card.location.mode", "lon": -71.54321}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.mode", "lon": 180}
    jsonschema.validate(instance=instance, schema=schema)

def test_lon_invalid_type(schema):
    """Tests invalid type for lon."""
    instance = {"req": "card.location.mode", "lon": "-71.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'-71.5' is not of type 'number'" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {"req": "card.location.mode", "max": 600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.location.mode", "max": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"req": "card.location.mode", "max": "600.0"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'600.0' is not of type 'integer'" in str(excinfo.value)

def test_valid_fixed_mode_with_coords(schema):
    """Tests valid fixed mode with lat/lon."""
    instance = {"req": "card.location.mode", "mode": "fixed", "lat": 40.1, "lon": -70.2}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_periodic_mode_with_seconds(schema):
    """Tests valid periodic mode with seconds."""
    instance = {"req": "card.location.mode", "mode": "periodic", "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {
        "req": "card.location.mode",
        "mode": "periodic",
        "seconds": 300,
        "vseconds": "{voltage} > 3.0 ? 60 : 300",
        "lat": 45.0, # Ignored unless mode=fixed
        "lon": -90.0, # Ignored unless mode=fixed
        "max": 120
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.location.mode", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
