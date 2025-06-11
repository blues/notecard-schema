import pytest
import jsonschema
import json

SCHEMA_FILE = "web.put.rsp.notecard.api.json"

def test_valid_minimal(schema):
    """Tests a minimal valid response with just result."""
    instance = {"result": 204}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests a valid response with a body object."""
    instance = {"result": 200, "body": {"message": "Update successful"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_payload(schema):
    """Tests a valid response with base64 payload."""
    instance = {"result": 200, "payload": "SGVsbG8gV29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_status(schema):
    """Tests a valid response with status (note: schema defines as integer, but description suggests string)."""
    # The schema incorrectly defines status as integer, but description says "32-character hex-encoded MD5 sum"
    # Testing according to schema definition (integer) for now
    instance = {"result": 200, "status": 12345}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_response(schema):
    """Tests a complete response with all possible fields."""
    instance = {
        "result": 200,
        "body": {"message": "Success", "data": {"updated": True}},
        "payload": "SGVsbG8gV29ybGQ=",
        "status": 67890
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
    """Tests invalid type for status (should be integer according to schema)."""
    # Note: This is testing the schema as-is, though the description suggests it should be a string
    instance = {"result": 200, "status": "not-an-integer"}
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
            "message": "Update successful",
            "data": {
                "id": 1234,
                "updated_fields": ["temp", "humidity"],
                "timestamp": "2023-01-01T12:00:00Z",
                "metadata": {
                    "version": "1.0",
                    "source": "sensor"
                }
            },
            "stats": {
                "affected_rows": 1,
                "execution_time_ms": 45
            }
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_put_specific_status_codes(schema):
    """Tests HTTP status codes common for PUT operations."""
    # 200 OK - successful update with response body
    instance = {"result": 200, "body": {"updated": True}}
    jsonschema.validate(instance=instance, schema=schema)

    # 204 No Content - successful update with no response body
    instance = {"result": 204}
    jsonschema.validate(instance=instance, schema=schema)

    # 201 Created - resource was created
    instance = {"result": 201, "body": {"created": True}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_error_responses(schema):
    """Tests valid error HTTP status codes with appropriate bodies."""
    error_cases = [
        (400, {"error": "Bad Request", "details": "Invalid JSON"}),
        (401, {"error": "Unauthorized", "message": "Invalid credentials"}),
        (403, {"error": "Forbidden", "message": "Access denied"}),
        (404, {"error": "Not Found", "message": "Resource not found"}),
        (422, {"error": "Unprocessable Entity", "validation_errors": ["field required"]}),
        (500, {"error": "Internal Server Error", "message": "Database connection failed"})
    ]

    for status_code, body in error_cases:
        instance = {"result": status_code, "body": body}
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
