import pytest
import jsonschema
import json

SCHEMA_FILE = "card.aux.serial.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests the minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_properties(schema):
    """Tests that additional properties are allowed as per schema default."""
    instance = {"some_field": 123, "another": "value"}
    # This should be valid because additionalProperties is not set to false
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_type(schema):
    """Tests that non-object types are invalid."""
    invalid_instances = [
        None,       # null
        [],         # array
        "string",   # string
        123,        # integer
        True        # boolean
    ]
    for instance in invalid_instances:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'object'" in str(excinfo.value)

def test_mode_valid(schema):
    """Tests valid mode field."""
    instance = {"mode": "notify,env"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "gps"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_array(schema):
    """Tests invalid array type for mode."""
    instance = {"mode": ["notify", "env"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_rate_valid(schema):
    """Tests valid rate field."""
    instance = {"rate": 115200}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"rate": 9600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"rate": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_rate_invalid_type(schema):
    """Tests invalid type for rate."""
    instance = {"rate": "115200"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'115200' is not of type 'integer'" in str(excinfo.value)

def test_rate_invalid_float(schema):
    """Tests invalid float type for rate."""
    instance = {"rate": 115200.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "115200.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_with_mode_and_rate(schema):
    """Tests a valid response with both mode and rate."""
    instance = {"mode": "req", "rate": 115200}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "gps", "rate": 9600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "notify,accel", "rate": 115200}
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
