import pytest
import jsonschema
import json

SCHEMA_FILE = "env.set.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request with required name."""
    instance = {"req": "env.set", "name": "test-var"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command with required name."""
    instance = {"cmd": "env.set", "name": "test-var"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"name": "test-var"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_missing_required_name(schema):
    """Tests that name is required at the top level."""
    instance = {"req": "env.set"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'name' is a required property" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "env.set", "cmd": "env.set", "name": "test-var"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api", "name": "test-var"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'env.set' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api", "name": "test-var"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'env.set' was expected" in str(excinfo.value)

def test_valid_name(schema):
    """Tests valid name field."""
    instance = {"req": "env.set", "name": "monitor-pump"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "env.set", "name": "SAMPLE_RATE"}
    jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"req": "env.set", "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_text(schema):
    """Tests valid text field."""
    instance = {"req": "env.set", "name": "test-var", "text": "on"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "env.set", "name": "test-var", "text": ""}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "env.set", "name": "test-var", "text": "60"}
    jsonschema.validate(instance=instance, schema=schema)

def test_text_invalid_type(schema):
    """Tests invalid type for text."""
    instance = {"req": "env.set", "name": "test-var", "text": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_text_optional(schema):
    """Tests that text field is optional."""
    instance = {"req": "env.set", "name": "test-var"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "env.set", "name": "test-var", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

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
