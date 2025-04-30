import pytest
import jsonschema

SCHEMA_FILE = "card.temp.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["temperature", "humidity", "pressure"]
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
    ["temperature", "humidity", "pressure"]
)
def test_invalid_type_for_number_field(schema, field_name):
    """Tests invalid type for various number fields."""
    instance = {field_name: "22.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'22.5' is not of type 'number'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "temperature": 21.8,
        "humidity": 45.2,
        "pressure": 1013.25
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"temperature": 20.0, "sensor": "onboard"}
    jsonschema.validate(instance=instance, schema=schema)
