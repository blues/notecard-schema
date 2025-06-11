import pytest
import jsonschema
import json

SCHEMA_FILE = "web.put.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "web.put"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "web.put"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"route": "SensorService"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "web.put", "cmd": "web.put"}
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

def test_valid_with_route_and_name(schema):
    """Tests valid request with route and name."""
    instance = {"req": "web.put", "route": "SensorService", "name": "/updateReading"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests valid request with JSON body."""
    instance = {"req": "web.put", "body": {"id": 1234, "temp": 72.32, "humidity": 32.2}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_body_type(schema):
    """Tests invalid type for body."""
    instance = {"req": "web.put", "body": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_valid_with_payload(schema):
    """Tests valid request with base64 payload."""
    instance = {"req": "web.put", "payload": "SGVsbG8gV29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_payload_type(schema):
    """Tests invalid type for payload."""
    instance = {"req": "web.put", "payload": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_valid_with_content(schema):
    """Tests valid request with content type."""
    instance = {"req": "web.put", "content": "application/json"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_seconds(schema):
    """Tests valid request with timeout."""
    instance = {"req": "web.put", "seconds": 120}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_seconds_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "web.put", "seconds": "120"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_with_total_and_offset(schema):
    """Tests valid request with total and offset for fragmented payloads."""
    instance = {"req": "web.put", "total": 1024, "offset": 512}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_total_type(schema):
    """Tests invalid type for total."""
    instance = {"req": "web.put", "total": "1024"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_offset_type(schema):
    """Tests invalid type for offset."""
    instance = {"req": "web.put", "offset": "512"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_with_status(schema):
    """Tests valid request with MD5 status."""
    instance = {"req": "web.put", "status": "5d41402abc4b2a76b9719d911017c592"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_max(schema):
    """Tests valid request with max response size."""
    instance = {"req": "web.put", "max": 2048}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_max_type(schema):
    """Tests invalid type for max."""
    instance = {"req": "web.put", "max": "2048"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_with_verify(schema):
    """Tests valid request with verify flag."""
    instance = {"req": "web.put", "verify": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_verify_type(schema):
    """Tests invalid type for verify."""
    instance = {"req": "web.put", "verify": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_valid_with_async(schema):
    """Tests valid request with async flag."""
    instance = {"req": "web.put", "async": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_async_type(schema):
    """Tests invalid type for async."""
    instance = {"req": "web.put", "async": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_valid_with_file_and_note(schema):
    """Tests valid request with file and note parameters."""
    instance = {"req": "web.put", "file": "response.dbx", "note": "response1"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_type(schema):
    """Tests invalid type for file."""
    instance = {"req": "web.put", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_note_type(schema):
    """Tests invalid type for note."""
    instance = {"req": "web.put", "note": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "web.put", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_complex_request(schema):
    """Tests a complex valid request with multiple parameters."""
    instance = {
        "req": "web.put",
        "route": "SensorService",
        "name": "/updateReading?id=1",
        "body": {"id": 1234, "temp": 72.32, "humidity": 32.2},
        "content": "application/json",
        "seconds": 90,
        "max": 1024
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_fragmented_payload_request(schema):
    """Tests a valid request with fragmented payload parameters."""
    instance = {
        "req": "web.put",
        "route": "FileService",
        "name": "/upload",
        "payload": "SGVsbG8gV29ybGQ=",
        "total": 2048,
        "offset": 1024,
        "status": "5d41402abc4b2a76b9719d911017c592",
        "verify": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_async_request(schema):
    """Tests a valid asynchronous request with file storage."""
    instance = {
        "req": "web.put",
        "route": "DataService",
        "name": "/bulk-update",
        "body": {"data": [1, 2, 3, 4, 5]},
        "async": True,
        "file": "update-response.dbx",
        "note": "bulk-update-001"
    }
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
