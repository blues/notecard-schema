import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.status.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only required fields."""
    instance = {"status": "connected", "connected": True}
    jsonschema.validate(instance=instance, schema=schema)


def test_missing_required_status(schema):
    """Tests invalid response missing the required 'status' field."""
    instance = {"connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'status' is a required property" in str(excinfo.value)


def test_missing_required_connected(schema):
    """Tests invalid response missing the required 'connected' field."""
    instance = {"status": "connected"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'connected' is a required property" in str(excinfo.value)

def test_valid_both_fields(schema):
    """Tests valid response with both fields."""
    instance = {
        "status": "connected (session open) {connected}",
        "connected": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_connected_true(schema):
    """Tests valid response with connected true."""
    instance = {"status": "connected", "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_connected_false(schema):
    """Tests valid response with connected false."""
    instance = {"status": "disconnected", "connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status_connected_message(schema):
    """Tests valid response with connected status message."""
    instance = {"status": "connected (session open) {connected}", "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status_disconnected_message(schema):
    """Tests valid response with disconnected status message."""
    instance = {"status": "disconnected", "connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status_various_messages(schema):
    """Tests valid response with various status messages."""
    status_messages = [
        "connected (session open) {connected}",
        "disconnected",
        "connecting",
        "cellular: connecting",
        "wifi: connected",
        "lora: connected to gateway",
        "cellular: registered {roaming}"
    ]

    for status_msg in status_messages:
        instance = {"status": status_msg, "connected": True}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_status_empty_string(schema):
    """Tests valid response with empty status string."""
    instance = {"status": "", "connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_combinations(schema):
    """Tests valid responses with various field combinations."""
    combinations = [
        {"status": "connected", "connected": True},
        {"status": "disconnected", "connected": False},
        {"status": "connecting", "connected": False},
        {"status": "cellular: registered", "connected": True}
    ]

    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_all_non_required_fields_optional(schema):
    """Tests that non-required fields are optional (only status and connected are required)."""
    # Minimal valid with just required fields
    instance = {"status": "connected", "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type_integer(schema):
    """Tests invalid integer type for status."""
    instance = {"status": 123, "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_status_invalid_type_boolean(schema):
    """Tests invalid boolean type for status."""
    instance = {"status": True, "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_status_invalid_type_array(schema):
    """Tests invalid array type for status."""
    instance = {"status": ["connected"], "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_status_invalid_type_object(schema):
    """Tests invalid object type for status."""
    instance = {"status": {"state": "connected"}, "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_connected_invalid_type_string(schema):
    """Tests invalid string type for connected."""
    instance = {"status": "connected", "connected": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_connected_invalid_type_integer(schema):
    """Tests invalid integer type for connected."""
    instance = {"status": "connected", "connected": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_connected_invalid_type_array(schema):
    """Tests invalid array type for connected."""
    instance = {"status": "connected", "connected": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_connected_invalid_type_object(schema):
    """Tests invalid object type for connected."""
    instance = {"status": "connected", "connected": {"status": True}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"status": "connected", "connected": True, "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok", "connected": True, "result": "ok"},
        {"status": "ok", "connected": True, "message": "success"},
        {"status": "ok", "connected": True, "time": 1234567890},
        {"status": "ok", "connected": True, "version": "1.0"},
        {"status": "ok", "connected": True, "error": "none"},
        {"status": "ok", "connected": True, "data": "status"},
        {"status": "ok", "connected": True, "success": True},
        {"status": "ok", "connected": True, "state": "active"},
        {"status": "ok", "connected": True, "transport": "cellular"}
    ]

    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"status": "connected", "connected": True, "result": "ok", "message": "success"}
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

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    # Any property not in the defined schema should be rejected
    properties_to_test = [
        "device", "product", "result", "error", "message", "time",
        "data", "success", "code", "info", "warning", "state", "transport"
    ]

    for prop in properties_to_test:
        instance = {"status": "ok", "connected": True, prop: "test"}
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
