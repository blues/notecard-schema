import pytest
import jsonschema
import json

SCHEMA_FILE = "web.post.rsp.notecard.api.json"

def test_valid_minimal(schema):
    """Tests a minimal valid response with just result."""
    instance = {"result": 200}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests a valid response with a body object."""
    instance = {"result": 200, "body": {"message": "Reading added successfully"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_payload(schema):
    """Tests a valid response with base64 payload."""
    instance = {"result": 200, "payload": "SGVsbG8gV29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_status(schema):
    """Tests a valid response with status (MD5 sum)."""
    instance = {"result": 200, "status": "5d41402abc4b2a76b9719d911017c592"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_cobs_and_length(schema):
    """Tests a valid response with cobs and length for binary payload."""
    instance = {"result": 200, "cobs": 8, "length": 6}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_response(schema):
    """Tests a complete response with all possible fields."""
    instance = {
        "result": 200,
        "body": {"message": "Success"},
        "payload": "SGVsbG8gV29ybGQ=",
        "status": "5d41402abc4b2a76b9719d911017c592",
        "cobs": 8,
        "length": 6
    }
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

def test_invalid_status_type(schema):
    """Tests invalid type for status (should be string)."""
    instance = {"result": 200, "status": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_cobs_type(schema):
    """Tests invalid type for cobs (should be integer)."""
    instance = {"result": 200, "cobs": "8"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_length_type(schema):
    """Tests invalid type for length (should be integer)."""
    instance = {"result": 200, "length": "6"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_http_status_codes(schema):
    """Tests valid HTTP status codes."""
    for status_code in [200, 201, 204, 400, 401, 404, 500, 502, 503]:
        instance = {"result": status_code}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_body(schema):
    """Tests valid response with empty body object."""
    instance = {"result": 200, "body": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complex_body(schema):
    """Tests valid response with complex body object."""
    instance = {
        "result": 200,
        "body": {
            "message": "Success",
            "data": {
                "id": 123,
                "readings": [
                    {"temp": 72.32, "timestamp": "2023-01-01T12:00:00Z"},
                    {"temp": 73.15, "timestamp": "2023-01-01T12:05:00Z"}
                ]
            },
            "meta": {
                "count": 2,
                "next": None
            }
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (schema allows them)."""
    instance = {"result": 200, "extra": "field"}
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
