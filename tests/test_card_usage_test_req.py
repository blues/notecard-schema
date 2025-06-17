import pytest
import jsonschema
import json

SCHEMA_FILE = "card.usage.test.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.usage.test"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.usage.test"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_days(schema):
    """Tests valid request with req and days parameter."""
    instance = {"req": "card.usage.test", "days": 7}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_hours(schema):
    """Tests valid request with req and hours parameter."""
    instance = {"req": "card.usage.test", "hours": 12}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_megabytes(schema):
    """Tests valid request with req and megabytes parameter."""
    instance = {"req": "card.usage.test", "megabytes": 500}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_all_params(schema):
    """Tests valid request with cmd and all parameters."""
    instance = {"cmd": "card.usage.test", "days": 30, "megabytes": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_days_and_megabytes(schema):
    """Tests valid request with req, days, and megabytes."""
    instance = {"req": "card.usage.test", "days": 14, "megabytes": 2048}
    jsonschema.validate(instance=instance, schema=schema)

def test_days_invalid_type(schema):
    """Tests invalid type for days parameter."""
    instance = {"req": "card.usage.test", "days": "seven"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'seven' is not of type 'integer'" in str(excinfo.value)

def test_hours_invalid_type(schema):
    """Tests invalid type for hours parameter."""
    instance = {"req": "card.usage.test", "hours": 12.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "12.5 is not of type 'integer'" in str(excinfo.value)

def test_megabytes_invalid_type(schema):
    """Tests invalid type for megabytes parameter."""
    instance = {"req": "card.usage.test", "megabytes": "1024"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1024' is not of type 'integer'" in str(excinfo.value)

def test_days_negative_value(schema):
    """Tests negative value for days parameter."""
    instance = {"req": "card.usage.test", "days": -5}
    jsonschema.validate(instance=instance, schema=schema)  # Schema doesn't restrict negative values

def test_hours_zero_value(schema):
    """Tests zero value for hours parameter."""
    instance = {"req": "card.usage.test", "hours": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_megabytes_large_value(schema):
    """Tests large value for megabytes parameter."""
    instance = {"req": "card.usage.test", "megabytes": 999999}
    jsonschema.validate(instance=instance, schema=schema)

def test_req_invalid_value(schema):
    """Tests invalid req value."""
    instance = {"req": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.usage.test' was expected" in str(excinfo.value)

def test_cmd_invalid_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.usage.test' was expected" in str(excinfo.value)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.usage.test", "cmd": "card.usage.test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "card.usage.test", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "card.usage.test", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

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
