import pytest
import jsonschema
import json

SCHEMA_FILE = "card.triangulate.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.triangulate"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.triangulate"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.triangulate", "cmd": "card.triangulate"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "card.triangulate", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "card.triangulate", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_on_field_valid(schema):
    """Tests valid 'on' field values."""
    # Valid boolean values
    instance = {"req": "card.triangulate", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_field_invalid_type(schema):
    """Tests invalid type for 'on' field."""
    instance = {"req": "card.triangulate", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_on_field_invalid_number(schema):
    """Tests invalid number type for 'on' field."""
    instance = {"req": "card.triangulate", "on": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_request_with_cmd_and_on(schema):
    """Tests valid request using 'cmd' with 'on' parameter."""
    instance = {"cmd": "card.triangulate", "on": True}
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
