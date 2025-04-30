import pytest
import jsonschema

SCHEMA_FILE = "card.binary.get.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_status(schema):
    """Tests a valid response with the status field."""
    instance = {"status": "md5:abcdef0123456789"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_err(schema):
    """Tests a valid response with the err field."""
    instance = {"err": "{description}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_all_fields(schema):
    """Tests a valid response with all defined fields."""
    instance = {
        "status": "md5:9876543210fedcba",
        "err": "{an-error-occurred}"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "12345 is not of type 'string'" in str(excinfo.value)

def test_err_invalid_type(schema):
    """Tests invalid type for err."""
    instance = {"err": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (allowed by default)."""
    instance = {"status": "md5:ok", "extra": "data"}
    jsonschema.validate(instance=instance, schema=schema)
