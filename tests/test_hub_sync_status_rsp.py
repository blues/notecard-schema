import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.sync.status.rsp.notecard.api.json"

REQUIRED_FIELDS = {"status": "completed {sync-end}", "sync": True}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with required fields."""
    instance = {"status": "completed {sync-end}", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_status(schema):
    """Tests that 'status' is a required property."""
    instance = {"sync": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'status' is a required property" in str(excinfo.value)

def test_missing_required_sync(schema):
    """Tests that 'sync' is a required property."""
    instance = {"status": "completed {sync-end}"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'sync' is a required property" in str(excinfo.value)

def test_valid_status_field(schema):
    """Tests valid status field."""
    instance = {**REQUIRED_FIELDS, "status": "completed {sync-end}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_field(schema):
    """Tests valid mode field."""
    instance = {**REQUIRED_FIELDS, "mode": "{modem-off}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_time_field(schema):
    """Tests valid time field."""
    instance = {**REQUIRED_FIELDS, "time": 1598367163}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_alert_field(schema):
    """Tests valid alert field."""
    instance = {**REQUIRED_FIELDS, "alert": True}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {**REQUIRED_FIELDS, "alert": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_field(schema):
    """Tests valid sync field."""
    instance = {**REQUIRED_FIELDS, "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {**REQUIRED_FIELDS, "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_completed_field(schema):
    """Tests valid completed field."""
    instance = {**REQUIRED_FIELDS, "completed": 1648}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_requested_field(schema):
    """Tests valid requested field."""
    instance = {**REQUIRED_FIELDS, "requested": 3600}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_seconds_field(schema):
    """Tests valid seconds field."""
    instance = {**REQUIRED_FIELDS, "seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_scan_field(schema):
    """Tests valid scan field."""
    instance = {**REQUIRED_FIELDS, "scan": True}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {**REQUIRED_FIELDS, "scan": False}
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
    instance = {**REQUIRED_FIELDS, "status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_status_invalid_type_boolean(schema):
    """Tests invalid boolean type for status."""
    instance = {**REQUIRED_FIELDS, "status": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_status_invalid_type_array(schema):
    """Tests invalid array type for status."""
    instance = {**REQUIRED_FIELDS, "status": ["completed"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_type_integer(schema):
    """Tests invalid integer type for mode."""
    instance = {**REQUIRED_FIELDS, "mode": 456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_type_boolean(schema):
    """Tests invalid boolean type for mode."""
    instance = {**REQUIRED_FIELDS, "mode": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)

def test_time_invalid_type_string(schema):
    """Tests invalid string type for time."""
    instance = {**REQUIRED_FIELDS, "time": "1598367163"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1598367163' is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_type_boolean(schema):
    """Tests invalid boolean type for time."""
    instance = {**REQUIRED_FIELDS, "time": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_type_array(schema):
    """Tests invalid array type for time."""
    instance = {**REQUIRED_FIELDS, "time": [1598367163]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_alert_invalid_type_string(schema):
    """Tests invalid string type for alert."""
    instance = {**REQUIRED_FIELDS, "alert": "True"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'True' is not of type 'boolean'" in str(excinfo.value)

def test_alert_invalid_type_integer(schema):
    """Tests invalid integer type for alert."""
    instance = {**REQUIRED_FIELDS, "alert": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_alert_invalid_type_array(schema):
    """Tests invalid array type for alert."""
    instance = {**REQUIRED_FIELDS, "alert": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_string(schema):
    """Tests invalid string type for sync."""
    instance = {**REQUIRED_FIELDS, "sync": "False"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'False' is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_integer(schema):
    """Tests invalid integer type for sync."""
    instance = {**REQUIRED_FIELDS, "sync": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_type_object(schema):
    """Tests invalid object type for sync."""
    instance = {**REQUIRED_FIELDS, "sync": {"value": False}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_completed_invalid_type_string(schema):
    """Tests invalid string type for completed."""
    instance = {**REQUIRED_FIELDS, "completed": "1648"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1648' is not of type 'integer'" in str(excinfo.value)

def test_completed_invalid_type_boolean(schema):
    """Tests invalid boolean type for completed."""
    instance = {**REQUIRED_FIELDS, "completed": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_completed_invalid_type_array(schema):
    """Tests invalid array type for completed."""
    instance = {**REQUIRED_FIELDS, "completed": [1648]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_requested_invalid_type_string(schema):
    """Tests invalid string type for requested."""
    instance = {**REQUIRED_FIELDS, "requested": "3600"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3600' is not of type 'integer'" in str(excinfo.value)

def test_requested_invalid_type_boolean(schema):
    """Tests invalid boolean type for requested."""
    instance = {**REQUIRED_FIELDS, "requested": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_string(schema):
    """Tests invalid string type for seconds."""
    instance = {**REQUIRED_FIELDS, "seconds": "300"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'300' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_boolean(schema):
    """Tests invalid boolean type for seconds."""
    instance = {**REQUIRED_FIELDS, "seconds": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type_object(schema):
    """Tests invalid object type for seconds."""
    instance = {**REQUIRED_FIELDS, "seconds": {"value": 300}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_scan_invalid_type_string(schema):
    """Tests invalid string type for scan."""
    instance = {**REQUIRED_FIELDS, "scan": "True"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'True' is not of type 'boolean'" in str(excinfo.value)

def test_scan_invalid_type_integer(schema):
    """Tests invalid integer type for scan."""
    instance = {**REQUIRED_FIELDS, "scan": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_scan_invalid_type_array(schema):
    """Tests invalid array type for scan."""
    instance = {**REQUIRED_FIELDS, "scan": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_negative_time_values(schema):
    """Tests that negative time values are accepted."""
    instance = {**REQUIRED_FIELDS, "time": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_negative_completed_values(schema):
    """Tests that negative completed values are accepted."""
    instance = {**REQUIRED_FIELDS, "completed": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_negative_requested_values(schema):
    """Tests that negative requested values are accepted."""
    instance = {**REQUIRED_FIELDS, "requested": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_negative_seconds_values(schema):
    """Tests that negative seconds values are accepted."""
    instance = {**REQUIRED_FIELDS, "seconds": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_time_values(schema):
    """Tests that zero time values are accepted."""
    instance = {**REQUIRED_FIELDS, "time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_completed_values(schema):
    """Tests that zero completed values are accepted."""
    instance = {**REQUIRED_FIELDS, "completed": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_requested_values(schema):
    """Tests that zero requested values are accepted."""
    instance = {**REQUIRED_FIELDS, "requested": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_zero_seconds_values(schema):
    """Tests that zero seconds values are accepted."""
    instance = {**REQUIRED_FIELDS, "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_large_integer_values(schema):
    """Tests that large integer values are accepted."""
    large_value = 2147483647  # Max 32-bit signed integer

    instance = {**REQUIRED_FIELDS, "time": large_value}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {**REQUIRED_FIELDS, "completed": large_value}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {**REQUIRED_FIELDS, "requested": large_value}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {**REQUIRED_FIELDS, "seconds": large_value}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {**REQUIRED_FIELDS, "extra": 123}
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
        instance = {**REQUIRED_FIELDS, **field_dict}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {**REQUIRED_FIELDS, "extra1": "value1", "extra2": "value2"}
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
        instance = {**REQUIRED_FIELDS, prop: "test"}
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
        instance = {**REQUIRED_FIELDS, "status": status}
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
        instance = {**REQUIRED_FIELDS, "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_edge_case_combinations(schema):
    """Tests edge case field combinations."""
    edge_cases = [
        # All boolean fields False
        {**REQUIRED_FIELDS, "alert": False, "sync": False, "scan": False},
        # All boolean fields True
        {**REQUIRED_FIELDS, "alert": True, "sync": True, "scan": True},
        # Mixed booleans with zero integers
        {**REQUIRED_FIELDS, "alert": True, "sync": False, "time": 0, "completed": 0, "requested": 0, "seconds": 0},
        # Only required fields with different status
        {**REQUIRED_FIELDS, "status": "completed {sync-end}"},
        # Only required fields with different mode
        {**REQUIRED_FIELDS, "mode": "{modem-off}"},
        # Required fields with time
        {**REQUIRED_FIELDS, "time": 1598367163}
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
