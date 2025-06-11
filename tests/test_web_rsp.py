import pytest
import jsonschema
import json

SCHEMA_FILE = "web.rsp.notecard.api.json"

def test_valid_minimal(schema):
    """Tests a minimal valid response with just status."""
    instance = {"status": 200}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests a valid response with body string."""
    instance = {"status": 200, "body": "Success response"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_headers(schema):
    """Tests a valid response with headers object."""
    instance = {"status": 200, "headers": {"Content-Type": "application/json", "Server": "nginx"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_response(schema):
    """Tests a complete response with all possible fields."""
    instance = {
        "status": 200,
        "body": "JSON response data",
        "headers": {
            "Content-Type": "application/json",
            "Content-Length": "42",
            "Server": "nginx/1.18"
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_status_type(schema):
    """Tests invalid type for status (should be integer)."""
    instance = {"status": "200"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_body_type(schema):
    """Tests invalid type for body (should be string)."""
    instance = {"status": 200, "body": {"key": "value"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_headers_type(schema):
    """Tests invalid type for headers (should be object)."""
    instance = {"status": 200, "headers": "not-an-object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_valid_http_status_codes(schema):
    """Tests valid HTTP status codes."""
    for status_code in [200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502, 503]:
        instance = {"status": status_code}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_body(schema):
    """Tests valid response with empty body string."""
    instance = {"status": 200, "body": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_headers(schema):
    """Tests valid response with empty headers object."""
    instance = {"status": 200, "headers": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_json_body_as_string(schema):
    """Tests valid response with JSON content as string body."""
    instance = {"status": 200, "body": "{\"message\": \"Success\", \"data\": [1, 2, 3]}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_error_status_codes(schema):
    """Tests valid error HTTP status codes."""
    for status_code in [400, 401, 403, 404, 422, 500, 502, 503, 504]:
        instance = {"status": status_code, "body": "Error message"}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_multiline_body(schema):
    """Tests valid response with multiline body string."""
    instance = {
        "status": 200,
        "body": "Line 1\nLine 2\nLine 3"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_common_headers(schema):
    """Tests valid response with common HTTP headers."""
    instance = {
        "status": 200,
        "headers": {
            "Content-Type": "application/json",
            "Content-Length": "1024",
            "Cache-Control": "no-cache",
            "Server": "nginx/1.18.0",
            "Date": "Wed, 21 Oct 2015 07:28:00 GMT",
            "Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT",
            "ETag": "\"1234567890\"",
            "Access-Control-Allow-Origin": "*"
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (schema allows them)."""
    instance = {"status": 200, "extra": "field"}
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
