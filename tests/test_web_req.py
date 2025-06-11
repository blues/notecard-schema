import pytest
import jsonschema
import json

SCHEMA_FILE = "web.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "web"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "web"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"method": "get"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "web", "cmd": "web"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "invalid.req"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "invalid.cmd"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_method_get(schema):
    """Tests valid request with GET method."""
    instance = {"req": "web", "method": "get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_method_post(schema):
    """Tests valid request with POST method."""
    instance = {"req": "web", "method": "post"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_method_put(schema):
    """Tests valid request with PUT method."""
    instance = {"req": "web", "method": "put"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_method_delete(schema):
    """Tests valid request with DELETE method."""
    instance = {"req": "web", "method": "delete"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_method_value(schema):
    """Tests invalid HTTP method."""
    instance = {"req": "web", "method": "patch"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not one of" in str(excinfo.value)

def test_invalid_method_type(schema):
    """Tests invalid type for method."""
    instance = {"req": "web", "method": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_valid_with_route(schema):
    """Tests valid request with route."""
    instance = {"req": "web", "route": "/api/v1/data"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_route_type(schema):
    """Tests invalid type for route."""
    instance = {"req": "web", "route": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_valid_with_body(schema):
    """Tests valid request with body object."""
    instance = {"req": "web", "body": {"key": "value", "number": 42}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_body_type(schema):
    """Tests invalid type for body."""
    instance = {"req": "web", "body": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_valid_with_payload(schema):
    """Tests valid request with binary payload."""
    instance = {"req": "web", "payload": "SGVsbG8gV29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_payload_type(schema):
    """Tests invalid type for payload."""
    instance = {"req": "web", "payload": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_valid_with_headers(schema):
    """Tests valid request with headers."""
    instance = {"req": "web", "headers": {"Authorization": "Bearer token123", "Content-Type": "application/json"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_headers_type(schema):
    """Tests invalid type for headers."""
    instance = {"req": "web", "headers": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_valid_empty_headers(schema):
    """Tests valid request with empty headers object."""
    instance = {"req": "web", "headers": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_body(schema):
    """Tests valid request with empty body object."""
    instance = {"req": "web", "body": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complex_request(schema):
    """Tests a complex valid request with multiple parameters."""
    instance = {
        "req": "web",
        "method": "post",
        "route": "/api/v1/sensors",
        "body": {"temp": 72.32, "humidity": 32.2},
        "headers": {"Authorization": "Bearer token123", "Content-Type": "application/json"}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "web", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

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
