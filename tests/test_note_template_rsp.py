import pytest
import jsonschema
import json

SCHEMA_FILE = "note.template.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_bytes_property(schema):
    """Tests valid bytes property."""
    instance = {"bytes": 40}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_bytes_type(schema):
    """Tests invalid type for bytes property."""
    instance = {"bytes": "40"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'40' is not of type 'integer'" in str(excinfo.value)

def test_valid_template_property(schema):
    """Tests valid template property."""
    instance = {"template": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"template": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_template_type(schema):
    """Tests invalid type for template property."""
    instance = {"template": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_body_property(schema):
    """Tests valid body property."""
    instance = {"body": {"temperature": 14.1, "humidity": 11}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_body_type(schema):
    """Tests invalid type for body property."""
    instance = {"body": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not an object' is not of type 'object'" in str(excinfo.value)

def test_valid_length_property(schema):
    """Tests valid length property."""
    instance = {"length": 100}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_length_type(schema):
    """Tests invalid type for length property."""
    instance = {"length": "100"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'100' is not of type 'integer'" in str(excinfo.value)

def test_valid_format_property(schema):
    """Tests valid format property."""
    instance = {"format": "compact"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_format_type(schema):
    """Tests invalid type for format property."""
    instance = {"format": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_all_properties(schema):
    """Tests a response with all properties."""
    instance = {
        "bytes": 40,
        "template": True,
        "body": {"temperature": 14.1, "humidity": 11},
        "length": 100,
        "format": "compact"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (response schemas allow additional properties)."""
    instance = {"bytes": 40, "extra": "info"}
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
