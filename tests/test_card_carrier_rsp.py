import pytest
import jsonschema

SCHEMA_FILE = "card.carrier.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_mode(schema):
    """Tests a valid response with the mode field."""
    instance = {"mode": "charging"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "off"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_rsp_with_charging(schema):
    """Tests a valid response with the charging field."""
    instance = {"charging": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"charging": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_charging_invalid_type(schema):
    """Tests invalid type for charging."""
    instance = {"charging": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_rsp_all_fields(schema):
    """Tests a valid response with both fields."""
    instance = {"mode": "charging", "charging": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (allowed by default)."""
    instance = {"mode": "off", "extra": 123}
    jsonschema.validate(instance=instance, schema=schema)
