import pytest
import jsonschema
import json

SCHEMA_FILE = "dfu.get.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_payload(schema):
    """Tests a valid response with the payload field."""
    instance = {"payload": "AAAAAAAAAAAAAAAAcy8ACIEvAAgAAAAAjy8ACJ0vAAg="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_empty_payload(schema):
    """Tests a valid response with an empty payload string."""
    instance = {"payload": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_payload_invalid_type(schema):
    """Tests invalid type for payload."""
    instance = {"payload": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_payload_invalid_type_boolean(schema):
    """Tests invalid boolean type for payload."""
    instance = {"payload": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_payload_invalid_type_array(schema):
    """Tests invalid array type for payload."""
    instance = {"payload": ["data"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"payload": "dGVzdA==", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_rsp_with_binary_fields(schema):
    """Tests a valid response with binary mode fields (cobs, length, status)."""
    instance = {"cobs": 10240, "length": 8192, "status": "5d41402abc4b2a76b9719d911017c592"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_cobs_only(schema):
    """Tests a valid response with only cobs field."""
    instance = {"cobs": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_length_only(schema):
    """Tests a valid response with only length field."""
    instance = {"length": 8192}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_status_only(schema):
    """Tests a valid response with only status field."""
    instance = {"status": "5d41402abc4b2a76b9719d911017c592"}
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_invalid_type(schema):
    """Tests invalid type for cobs field."""
    instance = {"cobs": "10240"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_length_invalid_type_in_response(schema):
    """Tests invalid type for length field in response."""
    instance = {"length": "8192"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_status_invalid_type(schema):
    """Tests invalid type for status field."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

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
