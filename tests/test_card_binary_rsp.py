import pytest
import jsonschema

SCHEMA_FILE = "card.binary.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_all_fields(schema):
    """Tests a valid response with all fields populated."""
    instance = {
        "cobs": 128,
        "connected": True,
        "length": 100,
        "err": "some error description"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_some_fields(schema):
    """Tests a valid response with a subset of fields."""
    instance = {
        "connected": False,
        "length": 50
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_valid(schema):
    """Tests valid cobs values (integer)."""
    instance = {"cobs": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"cobs": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_invalid_type(schema):
    """Tests invalid type for cobs."""
    instance = {"cobs": "128"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'128' is not of type 'integer'" in str(excinfo.value)

def test_connected_valid(schema):
    """Tests valid connected values (boolean)."""
    instance = {"connected": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_connected_invalid_type(schema):
    """Tests invalid type for connected."""
    instance = {"connected": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_length_valid(schema):
    """Tests valid length values (integer)."""
    instance = {"length": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"length": 5000}
    jsonschema.validate(instance=instance, schema=schema)

def test_length_invalid_type(schema):
    """Tests invalid type for length."""
    instance = {"length": 100.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "100.5 is not of type 'integer'" in str(excinfo.value)

def test_err_valid(schema):
    """Tests valid err value (string)."""
    instance = {"err": "{error-message}"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"err": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_err_invalid_type(schema):
    """Tests invalid type for err."""
    instance = {"err": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (allowed by default)."""
    instance = {"cobs": 10, "extra_field": "hello"}
    jsonschema.validate(instance=instance, schema=schema)
