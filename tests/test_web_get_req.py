import pytest
import jsonschema
import json

SCHEMA_FILE = "web.get.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "web.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "web.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "web.get", "cmd": "web.get"}
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
    instance = {"req": "web.get", "route": "weatherInfo", "name": "/getLatest"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_content(schema):
    """Tests valid request with content type."""
    instance = {"req": "web.get", "content": "application/json"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_seconds(schema):
    """Tests valid request with timeout."""
    instance = {"req": "web.get", "seconds": 120}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_seconds_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "web.get", "seconds": "120"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_valid_with_async(schema):
    """Tests valid request with async flag."""
    instance = {"req": "web.get", "async": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_async_type(schema):
    """Tests invalid type for async."""
    instance = {"req": "web.get", "async": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_valid_with_binary_params(schema):
    """Tests valid request with binary parameters."""
    instance = {"req": "web.get", "binary": True, "offset": 0, "max": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_file_and_note(schema):
    """Tests valid request with file and note parameters."""
    instance = {"req": "web.get", "file": "response.dbx", "note": "note1"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body(schema):
    """Tests valid request with JSON body."""
    instance = {"req": "web.get", "body": {"key": "value", "number": 42}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_body_type(schema):
    """Tests invalid type for body."""
    instance = {"req": "web.get", "body": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "web.get", "extra": "field"}
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

