import pytest
import jsonschema
import json

SCHEMA_FILE = "web.get.rsp.notecard.api.json"

def test_valid_minimal(schema):
    """Tests a minimal valid response with just result."""
    instance = {"result": 200}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests a valid response with a body object."""
    instance = {"result": 200, "body": {"temp": 75, "humidity": 49}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_payload_length_cobs(schema):
    """Tests a valid response with payload, length, and cobs."""
    instance = {"result": 200, "payload": "SGVsbG8=", "length": 6, "cobs": 8}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_result_type(schema):
    """Tests invalid type for result (should be integer)."""
    instance = {"result": "200"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_body_type(schema):
    """Tests invalid type for body (should be object)."""
    instance = {"result": 200, "body": "not-an-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_invalid_payload_type(schema):
    """Tests invalid type for payload (should be string)."""
    instance = {"result": 200, "payload": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_length_type(schema):
    """Tests invalid type for length (should be integer)."""
    instance = {"result": 200, "length": "6"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_cobs_type(schema):
    """Tests invalid type for cobs (should be integer)."""
    instance = {"result": 200, "cobs": "8"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

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
