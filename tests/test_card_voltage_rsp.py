import pytest
import jsonschema

SCHEMA_FILE = "card.voltage.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (all fields optional)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode(schema):
    """Tests valid mode field."""
    instance = {"mode": "lipo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_usb(schema):
    """Tests valid usb field."""
    instance = {"usb": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_usb_invalid_type(schema):
    """Tests invalid type for usb."""
    instance = {"usb": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["value", "vmin", "vmax", "vavg", "daily", "weekly", "monthly"]
)
def test_valid_number_field(schema, field_name):
    """Tests valid number type for various voltage fields."""
    instance = {field_name: 3.95}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 4}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -1.2}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["value", "vmin", "vmax", "vavg", "daily", "weekly", "monthly"]
)
def test_invalid_type_for_number_field(schema, field_name):
    """Tests invalid type for various voltage fields."""
    instance = {field_name: "3.9"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3.9' is not of type 'number'" in str(excinfo.value)

def test_valid_alert(schema):
    """Tests valid alert field."""
    instance = {"alert": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_alert_invalid_type(schema):
    """Tests invalid type for alert."""
    instance = {"alert": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_calibration(schema):
    """Tests valid calibration field."""
    instance = {"calibration": 3.3}
    jsonschema.validate(instance=instance, schema=schema)

def test_calibration_invalid_type(schema):
    """Tests invalid type for calibration."""
    instance = {"calibration": "3.3"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3.3' is not of type 'number'" in str(excinfo.value)

def test_valid_on(schema):
    """Tests valid on field."""
    instance = {"on": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {"on": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_sync(schema):
    """Tests valid sync field."""
    instance = {"sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_sync_invalid_type(schema):
    """Tests invalid type for sync."""
    instance = {"sync": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "alert": True,
        "calibration": 3.3,
        "daily": -0.05,
        "hours": 720,
        "minutes": 43200,
        "mode": "normal",
        "monthly": -0.8,
        "on": True,
        "sync": False,
        "usb": True,
        "value": 3.85,
        "vavg": 3.75,
        "vmax": 4.1,
        "vmin": 3.2,
        "weekly": -0.3
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_hours_field(schema):
    """Tests valid hours field."""
    instance = {"hours": 120}
    jsonschema.validate(instance=instance, schema=schema)

def test_hours_invalid_type(schema):
    """Tests invalid type for hours field."""
    instance = {"hours": "120"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'120' is not of type 'integer'" in str(excinfo.value)

def test_valid_minutes_field(schema):
    """Tests valid minutes field."""
    instance = {"minutes": 43200}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes field."""
    instance = {"minutes": "43200"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'43200' is not of type 'integer'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"value": 4.1, "status": "ok"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed ('status' was unexpected)" in str(excinfo.value)

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
