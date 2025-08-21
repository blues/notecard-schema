import pytest
import jsonschema
import json

SCHEMA_FILE = "var.set.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests the valid empty response as per API reference."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property_single(schema):
    """Tests invalid response with single additional property."""
    instance = {"extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_name(schema):
    """Tests invalid response with legacy name property."""
    instance = {"name": "status"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_text(schema):
    """Tests invalid response with legacy text property."""
    instance = {"text": "open"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"name": "status"},
        {"text": "value"},
        {"value": 42},
        {"flag": True},
        {"status": "ok"},
        {"message": "variable set"},
        {"error": "none"},
        {"result": "success"},
        {"success": True},
        {"updated": True},
        {"timestamp": 1640995200},
        {"file": "vars.db"},
        {"sync": True}
    ]

    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"status": "ok", "message": "variable set", "success": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]

    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    properties_to_test = [
        "name", "text", "value", "flag", "file", "sync", "status", "error",
        "message", "result", "data", "success", "updated", "created", "modified",
        "timestamp", "id", "type", "format", "encoding", "response", "output"
    ]

    for prop in properties_to_test:
        instance = {prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_empty_properties_validation(schema):
    """Tests that response schema has empty properties and strict validation."""
    # Schema should have empty properties
    properties = schema.get("properties", {})
    assert properties == {}, f"Expected empty properties, got: {properties}"

    # Only empty object should be valid
    jsonschema.validate(instance={}, schema=schema)

    # Any fields should be invalid
    invalid_responses = [
        {"any_field": "value"},
        {"status": "success"},
        {"variable_set": True},
        {"name": "temperature"},
        {"text": "updated"}
    ]

    for response in invalid_responses:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=response, schema=schema)

def test_variable_set_scenarios(schema):
    """Tests that only empty response is valid for var.set operations."""
    # Only empty response should be valid
    jsonschema.validate(instance={}, schema=schema)

    # All other responses should be invalid
    invalid_scenarios = [
        {"name": "status", "text": "open"},
        {"success": True},
        {"updated": True},
        {"message": "Variable set successfully"},
        {"result": "ok"},
        {"error": None},
        {"timestamp": 1640995200}
    ]

    for scenario in invalid_scenarios:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=scenario, schema=schema)

def test_legacy_response_properties_invalid(schema):
    """Tests that legacy response properties from v0.1.1 are no longer valid."""
    legacy_properties = [
        {"name": "temperature"},
        {"text": "23"},
        {"name": "status", "text": "active"},
        {"name": "flag", "text": "true"}
    ]

    for legacy_response in legacy_properties:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=legacy_response, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_api_reference_compliance(schema):
    """Tests that response schema complies with API reference (no response members)."""
    # API reference shows no response members, so only empty object should be valid
    jsonschema.validate(instance={}, schema=schema)

    # Any properties should be invalid per API reference
    potential_properties = [
        {"text": "value"},
        {"value": 42},
        {"flag": True},
        {"file": "vars.db"},
        {"sync": True},
        {"name": "variable"}
    ]

    for prop_response in potential_properties:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=prop_response, schema=schema)

def test_schema_structure_validation(schema):
    """Tests the overall schema structure is correct."""
    # Check required schema fields
    assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    assert schema.get("type") == "object"
    assert schema.get("version") == "0.2.1"
    assert schema.get("apiVersion") == "9.1.1"
    assert schema.get("additionalProperties") is False

    # Check properties is empty
    assert schema.get("properties") == {}
