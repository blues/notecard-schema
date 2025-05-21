import pytest
import jsonschema
import json

SCHEMA_FILE = "web.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_result(schema):
    """Tests valid result field."""
    instance = {"result": 200}
    jsonschema.validate(instance=instance, schema=schema)

def test_result_invalid_type(schema):
    """Tests invalid type for result."""
    instance = {"result": "200"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_body(schema):
    """Tests valid body field."""
    instance = {"body": {"foo": "bar"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_body_invalid_type(schema):
    """Tests invalid type for body."""
    instance = {"body": "not-an-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_valid_payload(schema):
    """Tests valid payload field."""
    instance = {"payload": "SGVsbG8sIFdvcmxkIQ=="}
    jsonschema.validate(instance=instance, schema=schema)

def test_payload_invalid_type(schema):
    """Tests invalid type for payload."""
    instance = {"payload": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_valid_length(schema):
    """Tests valid length field."""
    instance = {"length": 42}
    jsonschema.validate(instance=instance, schema=schema)

def test_length_invalid_type(schema):
    """Tests invalid type for length."""
    instance = {"length": "42"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_cobs(schema):
    """Tests valid cobs field."""
    instance = {"cobs": 100}
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_invalid_type(schema):
    """Tests invalid type for cobs."""
    instance = {"cobs": "100"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "result": 200,
        "body": {"foo": "bar"},
        "payload": "SGVsbG8sIFdvcmxkIQ==",
        "length": 12,
        "cobs": 12
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_additional_property(schema):
    """Tests response with an additional property (should be allowed)."""
    instance = {"result": 200, "extra": 123}
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
