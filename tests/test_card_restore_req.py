import pytest
import jsonschema
import json

SCHEMA_FILE = "card.restore.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.restore"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.restore"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_delete(schema):
    """Tests valid request with delete parameter."""
    instance = {"req": "card.restore", "delete": True}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"req": "card.restore", "delete": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_connected(schema):
    """Tests valid request with connected parameter."""
    instance = {"req": "card.restore", "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"req": "card.restore", "connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_both_parameters(schema):
    """Tests valid request with both delete and connected parameters."""
    instance = {"req": "card.restore", "delete": True, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"req": "card.restore", "delete": False, "connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_parameters(schema):
    """Tests valid cmd request with parameters."""
    instance = {"cmd": "card.restore", "delete": True, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_delete_type_validation(schema):
    """Tests that delete must be a boolean."""
    instance = {"req": "card.restore", "delete": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_connected_type_validation(schema):
    """Tests that connected must be a boolean."""
    instance = {"req": "card.restore", "connected": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_req_invalid_value(schema):
    """Tests invalid req value."""
    instance = {"req": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.restore' was expected" in str(excinfo.value)

def test_cmd_invalid_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.restore' was expected" in str(excinfo.value)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.restore", "cmd": "card.restore"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "card.restore", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "card.restore", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

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
