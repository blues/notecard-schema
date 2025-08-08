import pytest
import jsonschema
import json

SCHEMA_FILE = "card.location.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"status": "{gps-status}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = ["continuous", "periodic", "off"]
    for mode in valid_modes:
        instance = {"mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"mode": "always_on"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'always_on' is not one of ['continuous', 'periodic', 'off']" in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_lat(schema):
    """Tests valid lat field."""
    instance = {"lat": 42.12345}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"lat": -30}
    jsonschema.validate(instance=instance, schema=schema)

def test_lat_invalid_type(schema):
    """Tests invalid type for lat."""
    instance = {"lat": "42.123"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'42.123' is not of type 'number'" in str(excinfo.value)

def test_valid_lon(schema):
    """Tests valid lon field."""
    instance = {"lon": -71.54321}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"lon": 180}
    jsonschema.validate(instance=instance, schema=schema)

def test_lon_invalid_type(schema):
    """Tests invalid type for lon."""
    instance = {"lon": "-71.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'-71.5' is not of type 'number'" in str(excinfo.value)

def test_valid_time(schema):
    """Tests valid time field."""
    instance = {"time": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {"time": 1678886400.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1678886400.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {"max": 3600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"max": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"max": "unlimited"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'unlimited' is not of type 'integer'" in str(excinfo.value)

def test_valid_count(schema):
    """Tests valid count field."""
    instance = {"count": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"count": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"count": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_dop(schema):
    """Tests valid dop field."""
    instance = {"dop": 1.5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"dop": 0.8}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"dop": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_dop_invalid_type(schema):
    """Tests invalid type for dop."""
    instance = {"dop": "1.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1.5' is not of type 'number'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "status": "GPS updated (58 sec, 41dB SNR, 9 sats) {gps-active} {gps-signal} {gps-sats} {gps}",
        "mode": "periodic",
        "lat": 42.577600,
        "lon": -70.871340,
        "time": 1598554399,
        "max": 25,
        "count": 0,
        "dop": 1.2
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"result": "success"}
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
