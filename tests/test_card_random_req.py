import pytest
import jsonschema
import json

SCHEMA_FILE = "card.random.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.random"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.random"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_count(schema):
    """Tests valid request with req and count."""
    instance = {"req": "card.random", "count": 100}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_count(schema):
    """Tests valid request with cmd and count."""
    instance = {"cmd": "card.random", "count": 50}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_mode_and_count(schema):
    """Tests valid request with req, mode, and count."""
    instance = {"req": "card.random", "mode": "payload", "count": 32}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_mode_and_count(schema):
    """Tests valid request with cmd, mode, and count."""
    instance = {"cmd": "card.random", "mode": "payload", "count": 16}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_type_validation(schema):
    """Tests that count must be an integer."""
    instance = {"req": "card.random", "count": "not_integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_count_negative_value(schema):
    """Tests that negative count values are allowed (schema doesn't restrict)."""
    instance = {"req": "card.random", "count": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_zero_value(schema):
    """Tests that zero count value is allowed."""
    instance = {"req": "card.random", "count": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_valid_value(schema):
    """Tests valid mode value 'payload'."""
    instance = {"req": "card.random", "mode": "payload", "count": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_value(schema):
    """Tests invalid mode value."""
    instance = {"req": "card.random", "mode": "invalid_mode", "count": 10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'payload' was expected" in str(excinfo.value)

def test_mode_without_count(schema):
    """Tests mode without count (should be valid)."""
    instance = {"req": "card.random", "mode": "payload"}
    jsonschema.validate(instance=instance, schema=schema)

def test_req_invalid_value(schema):
    """Tests invalid req value."""
    instance = {"req": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.random' was expected" in str(excinfo.value)

def test_cmd_invalid_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.random' was expected" in str(excinfo.value)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.random", "cmd": "card.random"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "card.random", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "card.random", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_large_count_value(schema):
    """Tests large count values are accepted."""
    instance = {"req": "card.random", "count": 2147483647}  # Max 32-bit signed int
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
