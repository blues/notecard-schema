import pytest
import jsonschema
import json

SCHEMA_FILE = "card.temp.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_value_field(schema):
    """Tests valid value field (onboard sensor temperature)."""
    instance = {"value": 27.625}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"value": -10.0}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"value": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_calibration_field(schema):
    """Tests valid calibration field."""
    instance = {"calibration": -3.0}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"calibration": 2.5}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"calibration": 0.0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_usb_field(schema):
    """Tests valid usb field."""
    instance = {"usb": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"usb": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_voltage_field(schema):
    """Tests valid voltage field."""
    instance = {"voltage": 4.95}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"voltage": 3.3}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"voltage": 0}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["value", "calibration", "temperature", "humidity", "pressure", "voltage"]
)
def test_valid_number_field(schema, field_name):
    """Tests valid number type for various fields."""
    instance = {field_name: 22.5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 50}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -10.2}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name", 
    ["value", "calibration", "temperature", "humidity", "pressure", "voltage"]
)
def test_invalid_type_for_number_field(schema, field_name):
    """Tests invalid type for various number fields."""
    instance = {field_name: "22.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'22.5' is not of type 'number'" in str(excinfo.value)

def test_usb_invalid_type(schema):
    """Tests invalid type for usb field."""
    instance = {"usb": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "value": 25.5,
        "calibration": -2.5,
        "temperature": 24.8,
        "humidity": 45.2,
        "pressure": 101325,
        "usb": True,
        "voltage": 4.95
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_basic_response(schema):
    """Tests valid basic response with onboard sensor only."""
    instance = {"value": 27.625, "calibration": -3.0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_i2c_sensor_response(schema):
    """Tests valid response with I2C sensor data."""
    instance = {
        "value": 25.0,
        "temperature": 24.8,
        "humidity": 45.2,
        "pressure": 101325
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"value": 25.0, "sensor": "onboard"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('sensor' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        "value": 25.0,
        "sensor": "onboard",
        "extra": "field"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

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
