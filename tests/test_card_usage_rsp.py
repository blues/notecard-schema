import pytest
import jsonschema

SCHEMA_FILE = "card.usage.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

# Test integer fields
@pytest.mark.parametrize(
    "field_name",
    [
        "seconds", "time", "bytes_sent", "bytes_received", "bytes_pending",
        "notes_sent", "notes_received", "notes_pending", "syncs", "requested",
        "completed", "failed", "minutes_connected", "minutes_cellular",
        "minutes_charging", "minutes_powered", "minutes_usb", "minutes_active"
    ]
)
def test_valid_integer_field(schema, field_name):
    """Tests valid integer type for various fields."""
    instance = {field_name: 123}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -10} # Check if negative allowed
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    [
        "seconds", "time", "bytes_sent", "bytes_received", "bytes_pending",
        "notes_sent", "notes_received", "notes_pending", "syncs", "requested",
        "completed", "failed", "minutes_connected", "minutes_cellular",
        "minutes_charging", "minutes_powered", "minutes_usb", "minutes_active"
    ]
)
def test_invalid_type_for_integer_field(schema, field_name):
    """Tests invalid (string) type for various integer fields."""
    instance = {field_name: "123"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'123' is not of type 'integer'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    [
        "seconds", "time", "bytes_sent", "bytes_received", "bytes_pending",
        "notes_sent", "notes_received", "notes_pending", "syncs", "requested",
        "completed", "failed", "minutes_connected", "minutes_cellular",
        "minutes_charging", "minutes_powered", "minutes_usb", "minutes_active"
    ]
)
def test_invalid_float_type_for_integer_field(schema, field_name):
    """Tests invalid (float) type for various integer fields."""
    instance = {field_name: 123.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123.5 is not of type 'integer'" in str(excinfo.value)

# Test number fields
@pytest.mark.parametrize(
    "field_name",
    [
        "voltage_min", "voltage_max", "voltage_begin", "voltage_end",
        "temp_min", "temp_max", "temp_begin", "temp_end"
    ]
)
def test_valid_number_field(schema, field_name):
    """Tests valid number type (int and float) for various fields."""
    instance = {field_name: 10.5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 10}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -5.2}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    [
        "voltage_min", "voltage_max", "voltage_begin", "voltage_end",
        "temp_min", "temp_max", "temp_begin", "temp_end"
    ]
)
def test_invalid_type_for_number_field(schema, field_name):
    """Tests invalid (string) type for various number fields."""
    instance = {field_name: "10.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10.5' is not of type 'number'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields populated."""
    instance = {
        "seconds": 3600,
        "time": 1700000000,
        "bytes_sent": 1024,
        "bytes_received": 2048,
        "bytes_pending": 0,
        "notes_sent": 10,
        "notes_received": 5,
        "notes_pending": 0,
        "syncs": 2,
        "requested": 1,
        "completed": 2,
        "failed": 0,
        "minutes_connected": 55,
        "minutes_cellular": 50,
        "minutes_charging": 10,
        "minutes_powered": 60,
        "minutes_usb": 5,
        "minutes_active": 45,
        "voltage_min": 3.8,
        "voltage_max": 4.1,
        "voltage_begin": 4.0,
        "voltage_end": 3.9,
        "temp_min": 15.5,
        "temp_max": 25.0,
        "temp_begin": 20.0,
        "temp_end": 22.5
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"seconds": 60, "source": "live"}
    jsonschema.validate(instance=instance, schema=schema)
