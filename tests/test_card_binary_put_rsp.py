import pytest
import jsonschema

SCHEMA_FILE = "card.binary.put.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_err(schema):
    """Tests a valid response with the err field."""
    instance = {"err": "{error-description}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_err_invalid_type(schema):
    """Tests invalid type for err."""
    instance = {"err": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (allowed by default)."""
    instance = {"err": "{error}", "extra": "allowed"}
    jsonschema.validate(instance=instance, schema=schema)
