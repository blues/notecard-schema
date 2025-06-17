import pytest
import jsonschema
import json

SCHEMA_FILE = "card.usage.test.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_max_response(schema):
    """Tests valid response with max field."""
    instance = {"max": 12730}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_days_response(schema):
    """Tests valid response with days field."""
    instance = {"days": 7}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_bytes_per_day_response(schema):
    """Tests valid response with bytes_per_day field."""
    instance = {"bytes_per_day": 41136}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_seconds_response(schema):
    """Tests valid response with seconds field."""
    instance = {"seconds": 1291377}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_time_response(schema):
    """Tests valid response with time field (UNIX timestamp)."""
    instance = {"time": 1598479763}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_bytes_sent_response(schema):
    """Tests valid response with bytes_sent field."""
    instance = {"bytes_sent": 163577}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_bytes_received_response(schema):
    """Tests valid response with bytes_received field."""
    instance = {"bytes_received": 454565}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_notes_sent_response(schema):
    """Tests valid response with notes_sent field."""
    instance = {"notes_sent": 114}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_notes_received_response(schema):
    """Tests valid response with notes_received field."""
    instance = {"notes_received": 26}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sessions_standard_response(schema):
    """Tests valid response with sessions_standard field."""
    instance = {"sessions_standard": 143}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sessions_secure_response(schema):
    """Tests valid response with sessions_secure field."""
    instance = {"sessions_secure": 31}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_response(schema):
    """Tests valid response with all fields."""
    instance = {
        "max": 12730,
        "days": 7,
        "bytes_per_day": 41136,
        "seconds": 1291377,
        "time": 1598479763,
        "bytes_sent": 163577,
        "bytes_received": 454565,
        "notes_sent": 114,
        "notes_received": 26,
        "sessions_standard": 143,
        "sessions_secure": 31
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max field."""
    instance = {"max": "12730"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'12730' is not of type 'integer'" in str(excinfo.value)

def test_days_invalid_type(schema):
    """Tests invalid type for days field."""
    instance = {"days": 7.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "7.5 is not of type 'integer'" in str(excinfo.value)

def test_bytes_per_day_invalid_type(schema):
    """Tests invalid type for bytes_per_day field."""
    instance = {"bytes_per_day": "41136"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'41136' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds field."""
    instance = {"seconds": [1291377]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "[1291377] is not of type 'integer'" in str(excinfo.value)

def test_time_invalid_type(schema):
    """Tests invalid type for time field."""
    instance = {"time": "1598479763"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1598479763' is not of type 'integer'" in str(excinfo.value)

def test_bytes_sent_invalid_type(schema):
    """Tests invalid type for bytes_sent field."""
    instance = {"bytes_sent": "163577"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'163577' is not of type 'integer'" in str(excinfo.value)

def test_bytes_received_invalid_type(schema):
    """Tests invalid type for bytes_received field."""
    instance = {"bytes_received": None}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "None is not of type 'integer'" in str(excinfo.value)

def test_notes_sent_invalid_type(schema):
    """Tests invalid type for notes_sent field."""
    instance = {"notes_sent": "114"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'114' is not of type 'integer'" in str(excinfo.value)

def test_notes_received_invalid_type(schema):
    """Tests invalid type for notes_received field."""
    instance = {"notes_received": {"value": 26}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "{'value': 26} is not of type 'integer'" in str(excinfo.value)

def test_sessions_standard_invalid_type(schema):
    """Tests invalid type for sessions_standard field."""
    instance = {"sessions_standard": "143"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'143' is not of type 'integer'" in str(excinfo.value)

def test_sessions_secure_invalid_type(schema):
    """Tests invalid type for sessions_secure field."""
    instance = {"sessions_secure": 31.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "31.5 is not of type 'integer'" in str(excinfo.value)

def test_zero_values_valid(schema):
    """Tests that zero values are valid for all integer fields."""
    instance = {
        "max": 0,
        "days": 0,
        "bytes_per_day": 0,
        "seconds": 0,
        "time": 0,
        "bytes_sent": 0,
        "bytes_received": 0,
        "notes_sent": 0,
        "notes_received": 0,
        "sessions_standard": 0,
        "sessions_secure": 0
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_negative_values_valid(schema):
    """Tests that negative values are valid (schema doesn't restrict them)."""
    instance = {
        "max": -1,
        "days": -5,
        "bytes_per_day": -100
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_large_values_valid(schema):
    """Tests that large integer values are valid."""
    instance = {
        "max": 999999999,
        "bytes_sent": 2147483647,
        "time": 9999999999
    }
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
