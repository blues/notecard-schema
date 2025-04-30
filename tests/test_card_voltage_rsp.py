import pytest
import jsonschema

SCHEMA_FILE = "card.voltage.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
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
    instance = {"usb": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_usb_invalid_type(schema):
    """Tests invalid type for usb."""
    instance = {"usb": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["value", "vref", "vmax", "vmin", "vhigh", "vnormal", "vlow", "vdead"]
)
def test_valid_number_field(schema, field_name):
    """Tests valid number type for various voltage fields."""
    instance = {field_name: 3.95}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 4}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -1.2}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["value", "vref", "vmax", "vmin", "vhigh", "vnormal", "vlow", "vdead"]
)
def test_invalid_type_for_number_field(schema, field_name):
    """Tests invalid type for various voltage fields."""
    instance = {field_name: "3.9"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3.9' is not of type 'number'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "mode": "default",
        "usb": False,
        "value": 4.01,
        "vref": 3.3,
        "vmax": 5.5,
        "vmin": 2.8,
        "vhigh": 4.5,
        "vnormal": 3.5,
        "vlow": 3.0,
        "vdead": 2.5
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"value": 4.1, "status": "ok"}
    jsonschema.validate(instance=instance, schema=schema)
