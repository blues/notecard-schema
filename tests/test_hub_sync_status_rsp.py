import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.sync.status.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status_field(schema):
    """Tests valid status field."""
    instance = {"status": "completed {sync-end}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_field(schema):
    """Tests valid mode field."""
    instance = {"mode": "{modem-off}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_time_field(schema):
    """Tests valid time field."""
    instance = {"time": 1598367163}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_alert_field(schema):
    """Tests valid alert field."""
    instance = {"alert": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"alert": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_field(schema):
    """Tests valid sync field."""
    instance = {"sync": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_completed_field(schema):
    """Tests valid completed field."""
    instance = {"completed": 1648}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_requested_field(schema):
    """Tests valid requested field."""
    instance = {"requested": 3600}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_seconds_field(schema):
    """Tests valid seconds field."""
    instance = {"seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_scan_field(schema):
    """Tests valid scan field."""
    instance = {"scan": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"scan": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_response(schema):
    """Tests valid complete response with all fields."""
    instance = {
        "status": "completed {sync-end}",
        "mode": "{modem-off}",
        "time": 1598367163,
        "alert": True,
        "sync": True,
        "completed": 1648,
        "requested": 3600,
        "seconds": 0,
        "scan": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_partial_response(schema):
    """Tests valid partial response with some fields."""
    instance = {
        "status": "waiting {network-down}",
        "mode": "{modem-off}",
        "sync": False,
        "seconds": 300
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_penalty_box_response(schema):
    """Tests valid penalty box response."""
    instance = {
        "status": "waiting {network-down}",
        "mode": "{modem-off}",
        "sync": False,
        "seconds": 300
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_recent_sync_response(schema):
    """Tests valid recent sync response."""
    instance = {
        "status": "completed {sync-end}",
        "mode": "{modem-off}",
        "time": 1598367163,
        "sync": False,
        "completed": 45,
        "scan": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type_integer(schema):
    """Tests invalid integer type for status."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_status_invalid_type_boolean(schema):
    """Tests invalid boolean type for status."""
    instance = {"status": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_status_invalid_type_array(schema):
    """Tests invalid array type for status."""
    instance = {"status": ["completed"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_type_integer(schema):
    """Tests invalid integer type for mode."""
    instance = {"mode": 456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_type_boolean(schema):
    """Tests invalid boolean type for mode."""
    instance = {"mode": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_time_invalid_type_string(schema):
    """Tests invalid string type for time."""
    instance = {"time": "1598367163"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1598367163' is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_type_boolean(schema):
    """Tests invalid boolean type for time."""
    instance = {"time": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_type_array(schema):
    """Tests invalid array type for time."""
    instance = {"time": [1598367163]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_alert_invalid_type_string(schema):
    """Tests invalid string type for alert."""
    instance = {"alert": "True"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'True' is not of type 'boolean'" in str(excinfo.value)

def test_alert_invalid_type_integer(schema):
    """Tests invalid integer type for alert."""
    instance = {"alert": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_alert_invalid_type_array(schema):
    """Tests invalid array type for alert."""
    instance = {"alert": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_string(schema):
    """Tests invalid string type for sync."""
    instance = {"sync": "False"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'False' is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_integer(schema):
    """Tests invalid integer type for sync."""
    instance = {"sync": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_object(schema):
    """Tests invalid object type for sync."""
    instance = {"sync": {"value": False}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_completed_invalid_type_string(schema):
    """Tests invalid string type for completed."""
    instance = {"completed": "1648"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1648' is not of type 'integer'" in str(excinfo.value)

def test_completed_invalid_type_boolean(schema):
    """Tests invalid boolean type for completed."""
    instance = {"completed": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_completed_invalid_type_array(schema):
    """Tests invalid array type for completed."""
    instance = {"completed": [1648]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_requested_invalid_type_string(schema):
    """Tests invalid string type for requested."""
    instance = {"requested": "3600"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3600' is not of type 'integer'" in str(excinfo.value)

def test_requested_invalid_type_boolean(schema):
    """Tests invalid boolean type for requested."""
    instance = {"requested": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_string(schema):
    """Tests invalid string type for seconds."""
    instance = {"seconds": "300"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'300' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_boolean(schema):
    """Tests invalid boolean type for seconds."""
    instance = {"seconds": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_object(schema):
    """Tests invalid object type for seconds."""
    instance = {"seconds": {"value": 300}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_scan_invalid_type_string(schema):
    """Tests invalid string type for scan."""
    instance = {"scan": "True"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'True' is not of type 'boolean'" in str(excinfo.value)

def test_scan_invalid_type_integer(schema):
    """Tests invalid integer type for scan."""
    instance = {"scan": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_scan_invalid_type_array(schema):
    """Tests invalid array type for scan."""
    instance = {"scan": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_negative_time_values(schema):
    """Tests that negative time values are accepted."""
    instance = {"time": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_negative_completed_values(schema):
    """Tests that negative completed values are accepted."""
    instance = {"completed": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_negative_requested_values(schema):
    """Tests that negative requested values are accepted."""
    instance = {"requested": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_negative_seconds_values(schema):
    """Tests that negative seconds values are accepted."""
    instance = {"seconds": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_time_values(schema):
    """Tests that zero time values are accepted."""
    instance = {"time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_completed_values(schema):
    """Tests that zero completed values are accepted."""
    instance = {"completed": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_requested_values(schema):
    """Tests that zero requested values are accepted."""
    instance = {"requested": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_seconds_values(schema):
    """Tests that zero seconds values are accepted."""
    instance = {"seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_large_integer_values(schema):
    """Tests that large integer values are accepted."""
    large_value = 2147483647  # Max 32-bit signed integer
    
    instance = {"time": large_value}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"completed": large_value}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"requested": large_value}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"seconds": large_value}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"result": "ok"},
        {"message": "synced"},
        {"error": "none"},
        {"data": "sync_complete"},
        {"success": True},
        {"synced": True},
        {"sync_result": "complete"},
        {"version": "1.0"},
        {"timestamp": 1598367163},
        {"duration": 30}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"extra1": "value1", "extra2": "value2"}
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

def test_additional_properties_False(schema):
    """Tests that additionalProperties is set to False."""
    # Verify schema has additionalProperties: False
    assert schema.get("additionalProperties") is False

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    # Any additional property should be rejected
    properties_to_test = [
        "device", "product", "result", "error", "message", "data",
        "success", "code", "info", "warning", "synced", "sync_result",
        "timestamp", "duration", "version", "id", "response", "body"
    ]
    
    for prop in properties_to_test:
        instance = {prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_common_status_codes(schema):
    """Tests that common status codes are accepted."""
    status_codes = [
        "completed {sync-end}",
        "waiting {network-down}",
        "waiting {sync-retry}",
        "syncing {in-progress}",
        "error {connection-failed}",
        "{modem-off}",
        "{cellular-preparing}",
        "{cellular-connecting}",
        "{cellular-connected}"
    ]
    
    for status in status_codes:
        instance = {"status": status}
        jsonschema.validate(instance=instance, schema=schema)

def test_common_mode_values(schema):
    """Tests that common mode values are accepted."""
    mode_values = [
        "{modem-off}",
        "{cellular-preparing}",
        "{cellular-connecting}",
        "{cellular-connected}",
        "{wifi-ready}",
        "{wifi-connecting}",
        "{wifi-connected}",
        "{lora-ready}"
    ]
    
    for mode in mode_values:
        instance = {"mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_edge_case_combinations(schema):
    """Tests edge case field combinations."""
    edge_cases = [
        # All boolean fields False
        {"alert": False, "sync": False, "scan": False},
        # All boolean fields True  
        {"alert": True, "sync": True, "scan": True},
        # Mixed booleans with zero integers
        {"alert": True, "sync": False, "time": 0, "completed": 0, "requested": 0, "seconds": 0},
        # Only status field
        {"status": "completed {sync-end}"},
        # Only mode field
        {"mode": "{modem-off}"},
        # Only time field
        {"time": 1598367163}
    ]
    
    for case in edge_cases:
        jsonschema.validate(instance=case, schema=schema)

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
