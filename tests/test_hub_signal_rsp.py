import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.signal.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (only required connected field)."""
    instance = {"connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_connected(schema):
    """Tests that missing required connected field fails validation."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'connected' is a required property" in str(excinfo.value)

def test_valid_body_only(schema):
    """Tests valid response with body and required connected field."""
    instance = {"body": {"example-key": "example-value"}, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_connected_only(schema):
    """Tests valid response with only connected field."""
    instance = {"connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_signals_only(schema):
    """Tests valid response with signals and required connected field."""
    instance = {"signals": 3, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {
        "body": {"data": "signal-content", "timestamp": 1234567890},
        "connected": True,
        "signals": 2
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_empty_object(schema):
    """Tests valid response with empty body object."""
    instance = {"body": {}, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_complex_object(schema):
    """Tests valid response with complex body object."""
    complex_body = {
        "sensor_data": {
            "temperature": 23.5,
            "humidity": 65.2
        },
        "metadata": {
            "device_id": "sensor-001",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        "alerts": ["high_temp", "low_battery"]
    }
    instance = {"body": complex_body, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_connected_true(schema):
    """Tests valid response with connected true."""
    instance = {"connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_connected_false(schema):
    """Tests valid response with connected false."""
    instance = {"connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_signals_zero(schema):
    """Tests valid response with signals zero."""
    instance = {"signals": 0, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_signals_positive(schema):
    """Tests valid response with positive signals count."""
    valid_counts = [1, 5, 10, 100]
    for count in valid_counts:
        instance = {"signals": count, "connected": True}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_partial_combinations(schema):
    """Tests valid responses with various field combinations."""
    combinations = [
        {"body": {"key": "value"}, "connected": True},
        {"body": {"data": 123}, "connected": True, "signals": 2},
        {"connected": False, "signals": 0},
        {"body": {"alert": "message"}, "connected": True},
        {"connected": True, "signals": 1}
    ]

    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_all_non_required_fields_optional(schema):
    """Tests that all non-required fields are optional."""
    # connected is required, body and signals are optional
    instance = {"connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_body_invalid_type_string(schema):
    """Tests invalid string type for body."""
    instance = {"body": "not an object", "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not an object' is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_array(schema):
    """Tests invalid array type for body."""
    instance = {"body": ["array", "not", "object"], "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_integer(schema):
    """Tests invalid integer type for body."""
    instance = {"body": 123, "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_boolean(schema):
    """Tests invalid boolean type for body."""
    instance = {"body": True, "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'object'" in str(excinfo.value)

def test_connected_invalid_type_string(schema):
    """Tests invalid string type for connected."""
    instance = {"connected": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_connected_invalid_type_integer(schema):
    """Tests invalid integer type for connected."""
    instance = {"connected": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_connected_invalid_type_object(schema):
    """Tests invalid object type for connected."""
    instance = {"connected": {"status": True}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_signals_invalid_type_string(schema):
    """Tests invalid string type for signals."""
    instance = {"signals": "5", "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_signals_invalid_type_float(schema):
    """Tests invalid float type for signals."""
    instance = {"signals": 3.5, "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "3.5 is not of type 'integer'" in str(excinfo.value)

def test_signals_invalid_type_boolean(schema):
    """Tests invalid boolean type for signals."""
    instance = {"signals": False, "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_signals_invalid_type_array(schema):
    """Tests invalid array type for signals."""
    instance = {"signals": [1, 2, 3], "connected": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_signals_negative_value(schema):
    """Tests that negative signals values are allowed."""
    # JSON Schema doesn't restrict negative values by default
    instance = {"signals": -1, "connected": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"body": {"key": "value"}, "connected": True, "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"connected": True, "status": "ok"},
        {"connected": True, "message": "received"},
        {"connected": True, "time": 1234567890},
        {"connected": True, "version": "1.0"},
        {"connected": True, "result": {}},
        {"connected": True, "error": "none"},
        {"connected": True, "data": "signal"},
        {"connected": True, "success": True},
        {"connected": True, "signal_id": "abc123"}
    ]

    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"body": {}, "connected": True, "status": "ok", "message": "received"}
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
        "device", "product", "status", "error", "message", "time",
        "result", "data", "success", "code", "info", "warning", "signal_id"
    ]

    for prop in properties_to_test:
        instance = {"connected": True, prop: "test"}
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
