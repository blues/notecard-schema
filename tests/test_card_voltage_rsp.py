import pytest
import jsonschema

SCHEMA_FILE = "card.voltage.rsp.notecard.api.json"

REQUIRED_FIELDS = {"usb": True}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only the required field."""
    instance = {"usb": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_usb(schema):
    """Tests that 'usb' is a required property."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'usb' is a required property" in str(excinfo.value)

def test_valid_mode(schema):
    """Tests valid mode field."""
    instance = {**REQUIRED_FIELDS, "mode": "lipo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {**REQUIRED_FIELDS, "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_usb(schema):
    """Tests valid usb field."""
    instance = {"usb": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"usb": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_usb_invalid_type(schema):
    """Tests invalid type for usb."""
    instance = {**REQUIRED_FIELDS, "usb": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["value", "vmin", "vmax", "vavg", "daily", "weekly", "monthly"]
)
def test_valid_number_field(schema, field_name):
    """Tests valid number type for various voltage fields."""
    instance = {**REQUIRED_FIELDS, field_name: 3.95}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, field_name: 4}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, field_name: -1.2}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["value", "vmin", "vmax", "vavg", "daily", "weekly", "monthly"]
)
def test_invalid_type_for_number_field(schema, field_name):
    """Tests invalid type for various voltage fields."""
    instance = {**REQUIRED_FIELDS, field_name: "3.9"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3.9' is not of type 'number'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "mode": "normal",
        "usb": False,
        "value": 3.85,
        "hours": 720,
        "vmin": 3.2,
        "vmax": 4.1,
        "vavg": 3.75,
        "daily": -0.05,
        "weekly": -0.3,
        "monthly": -0.8,
        "minutes": 43200
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_hours_field(schema):
    """Tests valid hours field."""
    instance = {**REQUIRED_FIELDS, "hours": 120}
    jsonschema.validate(instance=instance, schema=schema)

def test_hours_invalid_type(schema):
    """Tests invalid type for hours field."""
    instance = {**REQUIRED_FIELDS, "hours": "120"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'120' is not of type 'integer'" in str(excinfo.value)

def test_valid_minutes_field(schema):
    """Tests valid minutes field."""
    instance = {**REQUIRED_FIELDS, "minutes": 43200}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes field."""
    instance = {**REQUIRED_FIELDS, "minutes": "43200"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'43200' is not of type 'integer'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {**REQUIRED_FIELDS, "value": 4.1, "status": "ok"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('status' was unexpected)" in str(excinfo.value)

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
