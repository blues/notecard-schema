import pytest
import jsonschema

SCHEMA_FILE = "card.binary.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.binary"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.binary"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_delete_true(schema):
    """Tests a valid request with delete=True."""
    instance = {"req": "card.binary", "delete": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_delete_false(schema):
    """Tests a valid request with delete=False."""
    instance = {"req": "card.binary", "delete": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_delete_true(schema):
    """Tests a valid command with delete=True."""
    instance = {"cmd": "card.binary", "delete": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_delete_false(schema):
    """Tests a valid command with delete=False."""
    instance = {"cmd": "card.binary", "delete": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"delete": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # Check that the error is about failing the oneOf constraint
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.binary", "cmd": "card.binary"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # Check that the error is about failing the oneOf constraint
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "invalid.request"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_delete_type(schema):
    """Tests invalid type for delete."""
    instance = {"req": "card.binary", "delete": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.binary", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
