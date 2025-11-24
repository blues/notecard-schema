import pytest
import jsonschema
import json

SCHEMA_FILE = "note.get.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests a valid empty response."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_only(schema):
    """Tests valid response with only body field."""
    instance = {"body": {"api-key1": "api-val1"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_payload_only(schema):
    """Tests valid response with only payload field."""
    instance = {"payload": "aGVsbG8gd29ybGQ="}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_time_only(schema):
    """Tests valid response with only time field."""
    instance = {"time": 1598909219}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_and_time(schema):
    """Tests valid response with body and time fields."""
    instance = {"body": {"temperature": 23.5}, "time": 1598909220}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_payload_and_time(schema):
    """Tests valid response with payload and time fields."""
    instance = {"payload": "YWRkaXRpb25hbERhdGE=", "time": 1598909221}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {
        "body": {"sensor": "data"}, 
        "payload": "ZXh0cmFEYXRh", 
        "time": 1598909222
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complex_body(schema):
    """Tests valid response with complex body object."""
    instance = {
        "body": {
            "config": {
                "display": {"brightness": 75, "contrast": 80},
                "network": {"ssid": "MyWifi", "connected": True}
            },
            "data": {
                "sensors": [
                    {"type": "temperature", "value": 23.5},
                    {"type": "humidity", "value": 65}
                ]
            }
        },
        "time": 1598909223
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_empty_body(schema):
    """Tests valid response with empty body object."""
    instance = {"body": {}, "time": 1598909224}
    jsonschema.validate(instance=instance, schema=schema)

def test_body_invalid_type_string(schema):
    """Tests invalid string type for body."""
    instance = {"body": "should be object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'should be object' is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_array(schema):
    """Tests invalid array type for body."""
    instance = {"body": ["array", "not", "object"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_body_invalid_type_integer(schema):
    """Tests invalid integer type for body."""
    instance = {"body": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'object'" in str(excinfo.value)

def test_payload_invalid_type_integer(schema):
    """Tests invalid integer type for payload."""
    instance = {"payload": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "12345 is not of type 'string'" in str(excinfo.value)

def test_payload_invalid_type_boolean(schema):
    """Tests invalid boolean type for payload."""
    instance = {"payload": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_payload_invalid_type_array(schema):
    """Tests invalid array type for payload."""
    instance = {"payload": ["data"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_time_invalid_type_string(schema):
    """Tests invalid string type for time."""
    instance = {"time": "1598909219"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1598909219' is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_type_boolean(schema):
    """Tests invalid boolean type for time."""
    instance = {"time": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_type_array(schema):
    """Tests invalid array type for time."""
    instance = {"time": [1598909219]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_time_valid_zero(schema):
    """Tests valid zero time."""
    instance = {"time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_valid_negative(schema):
    """Tests valid negative time (edge case)."""
    instance = {"time": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_valid_large_value(schema):
    """Tests valid large time value."""
    instance = {"time": 2147483647}  # Max 32-bit signed integer
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"body": {"data": "test"}, "extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"message": "retrieved"},
        {"error": "none"},
        {"result": "success"},
        {"note": "test-id"},
        {"file": "data.qi"},
        {"delete": True},
        {"deleted": False},
        {"decrypt": True}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"body": {"data": "test"}, "status": "ok", "message": "retrieved"}
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
        ["array"]
    ]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    properties_to_test = [
        "file", "note", "delete", "deleted", "decrypt", "cmd", "req", 
        "status", "error", "message", "result", "data", "success"
    ]
    
    for prop in properties_to_test:
        instance = {prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_base64_payload_patterns(schema):
    """Tests various base64 payload patterns."""
    base64_patterns = [
        "SGVsbG8gV29ybGQ=",           # Hello World
        "VGhpcyBpcyBhIHRlc3Q=",       # This is a test
        "YWJjZGVmZ2hpamtsbW5vcA==",   # abcdefghijklmnop
        "MTIzNDU2Nzg5MA==",           # 1234567890
        ""                            # Empty string
    ]
    
    for payload in base64_patterns:
        instance = {"payload": payload, "time": 1598909225}
        jsonschema.validate(instance=instance, schema=schema)

def test_queue_response_scenarios(schema):
    """Tests typical queue response scenarios."""
    queue_responses = [
        {"body": {"request": "data"}, "time": 1598909226},
        {"payload": "cXVldWVEYXRh", "time": 1598909227},
        {"body": {"action": "process"}, "payload": "bWV0YWRhdGE=", "time": 1598909228}
    ]
    
    for response in queue_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_database_response_scenarios(schema):
    """Tests typical database response scenarios."""
    db_responses = [
        {"body": {"setting": "value"}, "time": 1598909229},
        {"body": {"config": {"enabled": True}}, "time": 1598909230},
        {"time": 1598909231}  # Just timestamp
    ]
    
    for response in db_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_encrypted_response_scenarios(schema):
    """Tests responses from encrypted notefiles."""
    encrypted_responses = [
        {"body": {"decrypted": "data"}, "time": 1598909232},
        {"payload": "ZGVjcnlwdGVkUGF5bG9hZA==", "time": 1598909233}
    ]
    
    for response in encrypted_responses:
        jsonschema.validate(instance=response, schema=schema)

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
