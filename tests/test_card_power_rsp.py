import pytest
import jsonschema
import json

SCHEMA_FILE = "card.power.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_temperature(schema):
    """Tests valid temperature field."""
    instance = {"temperature": 26.028314208984398}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"temperature": 25}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"temperature": -10.5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"temperature": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_temperature_invalid_type(schema):
    """Tests invalid type for temperature."""
    instance = {"temperature": "26.0"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'26.0' is not of type 'number'" in str(excinfo.value)

def test_valid_voltage(schema):
    """Tests valid voltage field."""
    instance = {"voltage": 4.200970458984375}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"voltage": 3.3}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"voltage": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"voltage": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_voltage_invalid_type(schema):
    """Tests invalid type for voltage."""
    instance = {"voltage": "4.2"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'4.2' is not of type 'number'" in str(excinfo.value)

def test_valid_milliamp_hours(schema):
    """Tests valid milliamp_hours field."""
    instance = {"milliamp_hours": 3.9566722000000007}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"milliamp_hours": 100.5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"milliamp_hours": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"milliamp_hours": 1000}
    jsonschema.validate(instance=instance, schema=schema)

def test_milliamp_hours_invalid_type(schema):
    """Tests invalid type for milliamp_hours."""
    instance = {"milliamp_hours": "3.95"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3.95' is not of type 'number'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["temperature", "voltage", "milliamp_hours"]
)
def test_valid_number_field(schema, field_name):
    """Tests valid number type for various fields."""
    instance = {field_name: 42.5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 100}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -5.2}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["temperature", "voltage", "milliamp_hours"]
)
def test_invalid_type_for_number_field(schema, field_name):
    """Tests invalid type for various number fields."""
    instance = {field_name: "42.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'42.5' is not of type 'number'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "temperature": 26.028314208984398,
        "voltage": 4.200970458984375,
        "milliamp_hours": 3.9566722000000007
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_partial_fields(schema):
    """Tests valid response with partial fields."""
    instance = {"temperature": 25.0, "voltage": 3.7}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"voltage": 4.1, "milliamp_hours": 150.5}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"temperature": 22.5}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"temperature": 25.0, "voltage": 4.1, "status": "ok"}
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
