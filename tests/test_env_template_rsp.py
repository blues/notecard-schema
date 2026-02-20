import pytest
import jsonschema
import json

SCHEMA_FILE = "env.template.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with required fields."""
    instance = {"bytes": 22}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_bytes(schema):
    """Tests that bytes is required."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'bytes' is a required property" in str(excinfo.value)

def test_valid_bytes_response(schema):
    """Tests valid response with bytes field."""
    instance = {"bytes": 22}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_large_bytes(schema):
    """Tests valid response with large byte count."""
    instance = {"bytes": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_max_bytes(schema):
    """Tests valid response with maximum byte count."""
    instance = {"bytes": 2147483647}
    jsonschema.validate(instance=instance, schema=schema)

def test_bytes_invalid_type(schema):
    """Tests invalid type for bytes."""
    instance = {"bytes": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_bytes_invalid_float(schema):
    """Tests invalid float type for bytes."""
    instance = {"bytes": 22.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "22.5 is not of type 'integer'" in str(excinfo.value)

def test_bytes_invalid_boolean(schema):
    """Tests invalid boolean type for bytes."""
    instance = {"bytes": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_bytes_invalid_array(schema):
    """Tests invalid array type for bytes."""
    instance = {"bytes": [22]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_bytes_invalid_object(schema):
    """Tests invalid object type for bytes."""
    instance = {"bytes": {"value": 22}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"bytes": 22, "extra": 123}
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
