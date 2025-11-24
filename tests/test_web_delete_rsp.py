import pytest
import jsonschema
import json

SCHEMA_FILE = "web.delete.rsp.notecard.api.json"

def test_valid_minimal(schema):
    """Tests a minimal valid response with just result."""
    instance = {"result": 204}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests a valid response with a body object."""
    instance = {"result": 200, "body": {"message": "Resource deleted successfully"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_payload(schema):
    """Tests a valid response with base64 payload."""
    instance = {"result": 200, "payload": "SGVsbG8gV29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_status(schema):
    """Tests a valid response with status (32-character hex-encoded MD5 sum)."""
    instance = {"result": 200, "status": "5d41402abc4b2a76b9719d911017c592"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_response(schema):
    """Tests a complete response with all possible fields."""
    instance = {
        "result": 200,
        "body": {"message": "Success", "deleted_count": 1},
        "payload": "SGVsbG8gV29ybGQ=",
        "status": "5d41402abc4b2a76b9719d911017c592"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_result_type(schema):
    """Tests invalid type for result (should be integer)."""
    instance = {"result": "204"}
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

def test_valid_http_status_codes(schema):
    """Tests valid HTTP status codes."""
    for status_code in [200, 204, 400, 401, 404, 500, 502, 503]:
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
            "message": "Delete operation completed",
            "data": {
                "deleted_items": ["item1", "item2", "item3"],
                "deletion_time": "2023-01-01T12:00:00Z",
                "metadata": {
                    "total_deleted": 3,
                    "cascade_deletions": 5
                }
            },
            "warnings": [
                "Some related records were automatically deleted"
            ]
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_delete_specific_status_codes(schema):
    """Tests HTTP status codes common for DELETE operations."""
    # 200 OK - successful deletion with response body
    instance = {"result": 200, "body": {"deleted": True}}
    jsonschema.validate(instance=instance, schema=schema)

    # 204 No Content - successful deletion with no response body
    instance = {"result": 204}
    jsonschema.validate(instance=instance, schema=schema)

    # 404 Not Found - resource to delete was not found
    instance = {"result": 404, "body": {"error": "Resource not found"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_error_responses(schema):
    """Tests valid error response formats."""
    error_cases = [
        (400, {"error": "Bad Request", "message": "Invalid resource ID"}),
        (401, {"error": "Unauthorized", "message": "Authentication required"}),
        (403, {"error": "Forbidden", "message": "Insufficient permissions"}),
        (404, {"error": "Not Found", "message": "Resource does not exist"}),
        (409, {"error": "Conflict", "message": "Resource cannot be deleted due to dependencies"}),
        (500, {"error": "Internal Server Error", "message": "Database connection failed"})
    ]

    for status_code, body in error_cases:
        instance = {"result": status_code, "body": body}
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property (not allowed)."""
    instance = {"result": 200, "extra": "field"}
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
