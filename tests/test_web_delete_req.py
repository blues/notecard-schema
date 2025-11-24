import pytest
import jsonschema
import json

SCHEMA_FILE = "web.delete.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "web.delete", "route": "SensorService"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "web.delete", "route": "SensorService"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"route": "SensorService"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "web.delete", "cmd": "web.delete", "route": "SensorService"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "invalid.req", "route": "SensorService"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "invalid.cmd", "route": "SensorService"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_route_and_name(schema):
    """Tests valid request with route and name."""
    instance = {"req": "web.delete", "route": "SensorService", "name": "/deleteReading?id=1"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_content(schema):
    """Tests valid request with content type."""
    instance = {"req": "web.delete", "route": "SensorService", "content": "application/json"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_seconds(schema):
    """Tests valid request with timeout."""
    instance = {"req": "web.delete", "route": "SensorService", "seconds": 120}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_seconds_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "web.delete", "route": "SensorService", "seconds": "120"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_with_async(schema):
    """Tests valid request with async flag."""
    instance = {"req": "web.delete", "route": "SensorService", "async": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_async_type(schema):
    """Tests invalid type for async."""
    instance = {"req": "web.delete", "route": "SensorService", "async": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_valid_with_file_and_note(schema):
    """Tests valid request with file and note parameters."""
    instance = {"req": "web.delete", "route": "SensorService", "file": "response.dbx", "note": "response1"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_type(schema):
    """Tests invalid type for file."""
    instance = {"req": "web.delete", "route": "SensorService", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_note_type(schema):
    """Tests invalid type for note."""
    instance = {"req": "web.delete", "route": "SensorService", "note": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "web.delete", "route": "SensorService", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_complex_request(schema):
    """Tests a complex valid request with multiple parameters."""
    instance = {
        "req": "web.delete",
        "route": "SensorService",
        "name": "/deleteReading?id=1",
        "content": "application/json",
        "seconds": 90
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_async_request(schema):
    """Tests a valid asynchronous request with file storage."""
    instance = {
        "req": "web.delete",
        "route": "DataService",
        "name": "/bulk-delete",
        "async": True,
        "file": "delete-response.dbx",
        "note": "bulk-delete-001"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_missing_route(schema):
    """Tests invalid request missing required route parameter."""
    instance = {"req": "web.delete"}
    with pytest.raises(jsonschema.ValidationError):
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
