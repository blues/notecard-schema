import pytest
import jsonschema

SCHEMA_FILE = "card.status.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"status": "{normal}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["usb", "connected", "cell", "sync"]
)
def test_valid_boolean_field(schema, field_name):
    """Tests valid boolean type for various fields."""
    instance = {field_name: True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: False}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["usb", "connected", "cell", "sync"]
)
def test_invalid_type_for_boolean_field(schema, field_name):
    """Tests invalid type for various boolean fields."""
    instance = {field_name: "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["storage", "time", "inbound", "outbound"]
)
def test_valid_integer_field(schema, field_name):
    """Tests valid integer type for various fields."""
    instance = {field_name: 10}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -5} # Check if negative allowed
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["storage", "time", "inbound", "outbound"]
)
def test_invalid_type_for_integer_field(schema, field_name):
    """Tests invalid (string) type for various integer fields."""
    instance = {field_name: "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["storage", "time", "inbound", "outbound"]
)
def test_invalid_float_type_for_integer_field(schema, field_name):
    """Tests invalid (float) type for various integer fields."""
    instance = {field_name: 10.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "10.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "status": "{normal}",
        "usb": True,
        "storage": 5,
        "time": 1700000000,
        "connected": True,
        "cell": True,
        "sync": False,
        "inbound": 0,
        "outbound": 2
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"status": "{normal}", "extra": "info"}
    jsonschema.validate(instance=instance, schema=schema)
