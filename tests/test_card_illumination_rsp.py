import pytest
import jsonschema

SCHEMA_FILE = "card.illumination.rsp.notecard.api.json"

def test_valid_lux(schema):
    """Tests a valid response with the 'lux' field."""
    instance = {"lux": 100.5}
    jsonschema.validate(instance=instance, schema=schema)

def test_lux_invalid_type(schema):
    """Tests an invalid type for the 'lux' field."""
    instance = {"lux": "high"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'high' is not of type 'number'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests a valid response with an additional property."""
    instance = {"lux": 50, "status": "ok"}
    jsonschema.validate(instance=instance, schema=schema)

def test_empty_object_valid(schema):
    """Tests that an empty object is a valid response (lux is not required)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)
