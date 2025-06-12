import pytest
import jsonschema
import json

SCHEMA_FILE = "web.req.notecard.api.json"


def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "web", "method": "GET", "route": "weatherInfo"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "web", "method": "GET", "route": "weatherInfo"}
    jsonschema.validate(instance=instance, schema=schema)


def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"method": "GET", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "web", "cmd": "web", "method": "GET", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)


def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "invalid.req", "method": "GET", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'web' was expected" in str(excinfo.value)


def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "invalid.cmd", "method": "GET", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'web' was expected" in str(excinfo.value)


def test_missing_required_method_with_req(schema):
    """Tests that method field is required when using req."""
    instance = {"req": "web", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_missing_required_method_with_cmd(schema):
    """Tests that method field is required when using cmd."""
    instance = {"cmd": "web", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_missing_required_route_with_req(schema):
    """Tests that route field is required when using req."""
    instance = {"req": "web", "method": "GET"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_missing_required_route_with_cmd(schema):
    """Tests that route field is required when using cmd."""
    instance = {"cmd": "web", "method": "GET"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_valid_methods(schema):
    """Tests all valid HTTP methods."""
    valid_methods = [
        "CONNECT",
        "DELETE",
        "GET",
        "HEAD",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
        "TRACE",
    ]
    for method in valid_methods:
        instance = {"req": "web", "method": method, "route": "weatherInfo"}
        jsonschema.validate(instance=instance, schema=schema)
        instance = {"cmd": "web", "method": method, "route": "weatherInfo"}
        jsonschema.validate(instance=instance, schema=schema)


def test_invalid_method(schema):
    """Tests invalid HTTP method."""
    instance = {"req": "web", "method": "INVALID", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)
    instance = {"cmd": "web", "method": "INVALID", "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_method_invalid_type(schema):
    """Tests invalid type for method."""
    instance = {"req": "web", "method": 123, "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)
    instance = {"cmd": "web", "method": 123, "route": "weatherInfo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_valid_route(schema):
    """Tests valid route field."""
    instance = {"req": "web", "method": "GET", "route": "weatherInfo"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"cmd": "web", "method": "GET", "route": "weatherInfo"}
    jsonschema.validate(instance=instance, schema=schema)


def test_route_invalid_type(schema):
    """Tests invalid type for route."""
    instance = {"req": "web", "method": "GET", "route": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)
    instance = {"cmd": "web", "method": "GET", "route": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_valid_name(schema):
    """Tests valid name field."""
    instance = {"req": "web", "method": "GET", "route": "weatherInfo", "name": "/getLatest"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"cmd": "web", "method": "GET", "route": "weatherInfo", "name": "/getLatest"}
    jsonschema.validate(instance=instance, schema=schema)


def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"req": "web", "method": "GET", "route": "weatherInfo", "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)
    instance = {"cmd": "web", "method": "GET", "route": "weatherInfo", "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)


def test_valid_content(schema):
    """Tests valid content field."""
    instance = {"req": "web", "method": "GET", "route": "weatherInfo", "content": "application/json"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"cmd": "web", "method": "GET", "route": "weatherInfo", "content": "application/json"}
    jsonschema.validate(instance=instance, schema=schema)


def test_content_invalid_type(schema):
    """Tests invalid type for content."""
    instance = {"req": "web", "method": "GET", "route": "weatherInfo", "content": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)
    instance = {"cmd": "web", "method": "GET", "route": "weatherInfo", "content": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)


def test_valid_all_fields(schema):
    """Tests a valid request with all fields."""
    instance = {
        "req": "web",
        "method": "GET",
        "route": "weatherInfo",
        "name": "/getLatest",
        "content": "application/json",
    }
    jsonschema.validate(instance=instance, schema=schema)
    instance = {
        "cmd": "web",
        "method": "GET",
        "route": "weatherInfo",
        "name": "/getLatest",
        "content": "application/json",
    }
    jsonschema.validate(instance=instance, schema=schema)


def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "web", "method": "GET", "route": "weatherInfo", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(
        excinfo.value
    )
    instance = {"cmd": "web", "method": "GET", "route": "weatherInfo", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(
        excinfo.value
    )


def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(
                f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}"
            )
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
