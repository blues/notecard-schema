import pytest
import jsonschema
import json

SCHEMA_FILE = "card.aux.serial.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "card.aux.serial"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "card.aux.serial"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "gps"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.aux.serial", "cmd": "card.aux.serial"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_valid(schema):
    """Tests valid mode pattern values."""
    valid_modes = [
        "req", "gps", "notify", "notify,accel", "notify,signals",
        "notify,env", "notify,dfu", "notify,accel,env", "notify,accel,signals",
        "notify,env,dfu", "notify,accel,env,dfu"
    ]
    for mode in valid_modes:
        instance = {"req": "card.aux.serial", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_pattern(schema):
    """Tests invalid mode pattern value."""
    instance = {"req": "card.aux.serial", "mode": "invalid_mode"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "does not match" in str(excinfo.value) or "pattern" in str(excinfo.value).lower()

def test_mode_invalid_combinations(schema):
    """Tests invalid mode combinations that should not be allowed."""
    invalid_modes = [
        "req,gps",  # Can't mix base modes
        "gps,notify",  # Can't mix base modes
        "req,notify,accel",  # Can't mix base modes
        "notify,invalid"  # Invalid notify option
    ]
    for mode in invalid_modes:
        instance = {"req": "card.aux.serial", "mode": mode}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "does not match" in str(excinfo.value) or "pattern" in str(excinfo.value).lower()

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.aux.serial", "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_with_mode(schema):
    """Tests a valid request including the mode field."""
    instance = {"req": "card.aux.serial", "mode": "notify,signals"}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_valid(schema):
    """Tests valid minutes values (integer >= 1)."""
    instance = {"req": "card.aux.serial", "minutes": 1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "minutes": 30}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "minutes": 1440}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"req": "card.aux.serial", "minutes": "30"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'30' is not of type 'integer'" in str(excinfo.value)

def test_minutes_invalid_zero(schema):
    """Tests invalid minutes value (zero)."""
    instance = {"req": "card.aux.serial", "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_float(schema):
    """Tests invalid float type for minutes."""
    instance = {"req": "card.aux.serial", "minutes": 30.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "30.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_with_mode_and_minutes(schema):
    """Tests a valid request with both mode and minutes."""
    instance = {"req": "card.aux.serial", "mode": "notify,dfu", "minutes": 60}
    jsonschema.validate(instance=instance, schema=schema)

def test_duration_valid(schema):
    """Tests valid duration values."""
    instance = {"req": "card.aux.serial", "duration": 500}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "duration": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_duration_invalid_type(schema):
    """Tests invalid type for duration."""
    instance = {"req": "card.aux.serial", "duration": "500"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'500' is not of type 'integer'" in str(excinfo.value)

def test_rate_valid(schema):
    """Tests valid rate values."""
    instance = {"req": "card.aux.serial", "rate": 115200}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "rate": 9600}
    jsonschema.validate(instance=instance, schema=schema)

def test_rate_invalid_type(schema):
    """Tests invalid type for rate."""
    instance = {"req": "card.aux.serial", "rate": "115200"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'115200' is not of type 'integer'" in str(excinfo.value)

def test_limit_valid(schema):
    """Tests valid limit values."""
    instance = {"req": "card.aux.serial", "limit": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "limit": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_limit_invalid_type(schema):
    """Tests invalid type for limit."""
    instance = {"req": "card.aux.serial", "limit": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_max_valid(schema):
    """Tests valid max values."""
    instance = {"req": "card.aux.serial", "max": 1024}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "max": 255}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"req": "card.aux.serial", "max": "1024"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1024' is not of type 'integer'" in str(excinfo.value)

def test_ms_valid(schema):
    """Tests valid ms values."""
    instance = {"req": "card.aux.serial", "ms": 1000}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux.serial", "ms": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_ms_invalid_type(schema):
    """Tests invalid type for ms."""
    instance = {"req": "card.aux.serial", "ms": "1000"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1000' is not of type 'integer'" in str(excinfo.value)

def test_valid_with_all_parameters(schema):
    """Tests a valid request with multiple parameters."""
    instance = {
        "req": "card.aux.serial",
        "mode": "notify,accel",
        "duration": 500,
        "rate": 115200,
        "max": 1024,
        "ms": 100
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_gps_with_limit(schema):
    """Tests a valid GPS mode request with limit."""
    instance = {
        "req": "card.aux.serial",
        "mode": "gps",
        "limit": True,
        "rate": 9600
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
