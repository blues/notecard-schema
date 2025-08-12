import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.set.rsp.notecard.api.json"

def test_empty_response_object(schema):
    """Tests that empty response object is valid."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"message": "success"},
        {"time": 1234567890},
        {"version": "1.0"},
        {"result": {}},
        {"error": "none"},
        {"data": "configured"},
        {"success": True},
        {"config": {}}
    ]

    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"status": "ok", "message": "configured"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = [
        "string",
        123,
        True,
        False,
        ["array"],
        None
    ]

    for invalid_instance in invalid_types:
        if invalid_instance is None:
            continue  # Skip None as it's handled differently
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=invalid_instance, schema=schema)
        # The error message will vary based on type, just ensure validation fails

def test_response_is_object_type(schema):
    """Tests that response schema requires object type."""
    # String should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance="not an object", schema=schema)

    # Number should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=42, schema=schema)

    # Array should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=[], schema=schema)

    # Boolean should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=True, schema=schema)

def test_no_properties_defined(schema):
    """Tests that the schema defines no properties."""
    # Verify schema has empty properties
    assert schema.get("properties") == {}

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    # Verify schema has additionalProperties: false
    assert schema.get("additionalProperties") is False

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    # Any property should be rejected
    properties_to_test = [
        "device", "product", "status", "error", "message", "time",
        "result", "data", "success", "code", "info", "warning", "config"
    ]

    for prop in properties_to_test:
        instance = {prop: "test"}
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
