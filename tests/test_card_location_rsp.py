import pytest
import jsonschema
import json

SCHEMA_FILE = "card.location.rsp.notecard.api.json"

REQUIRED_FIELDS = {"mode": "periodic"}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only the required field."""
    instance = {"mode": "periodic"}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_mode(schema):
    """Tests that 'mode' is a required property."""
    instance = {"status": "{gps-status}"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'mode' is a required property" in str(excinfo.value)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {**REQUIRED_FIELDS, "status": "{gps-status}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {**REQUIRED_FIELDS, "status": 123}
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
    instance = {**REQUIRED_FIELDS, "mode": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_lat(schema):
    """Tests valid lat field."""
    instance = {**REQUIRED_FIELDS, "lat": 42.12345}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "lat": -30}
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

def test_valid_time(schema):
    """Tests valid time field."""
    instance = {**REQUIRED_FIELDS, "time": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {**REQUIRED_FIELDS, "time": 1678886400.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1678886400.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {**REQUIRED_FIELDS, "max": 3600}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {**REQUIRED_FIELDS, "max": "unlimited"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'unlimited' is not of type 'integer'" in str(excinfo.value)

def test_valid_count(schema):
    """Tests valid count field."""
    instance = {**REQUIRED_FIELDS, "count": 5}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {**REQUIRED_FIELDS, "count": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_dop(schema):
    """Tests valid dop field."""
    instance = {**REQUIRED_FIELDS, "dop": 1.5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "dop": 0.8}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "dop": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_dop_invalid_type(schema):
    """Tests invalid type for dop."""
    instance = {**REQUIRED_FIELDS, "dop": "1.5"}
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
        "count": 3,
        "dop": 1.2
    }
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
