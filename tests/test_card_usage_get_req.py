import pytest
import jsonschema
import json

SCHEMA_FILE = "card.usage.get.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.usage.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.usage.get"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "total"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.usage.get", "cmd": "card.usage.get"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = [
        "total", "1hour", "1day", "30day"
    ]
    for mode in valid_modes:
        instance = {"req": "card.usage.get", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.usage.get", "mode": "yearly"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'yearly' is not one of ['total'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.usage.get", "mode": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_offset(schema):
    """Tests valid offset field."""
    instance = {"req": "card.usage.get", "offset": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.usage.get", "offset": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.usage.get", "offset": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_offset_invalid_type(schema):
    """Tests invalid type for offset."""
    instance = {"req": "card.usage.get", "offset": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_mode_with_offset(schema):
    """Tests valid combination of mode and offset."""
    modes_with_offset = ["total", "1hour", "1day", "30day"]
    for mode in modes_with_offset:
        instance = {"req": "card.usage.get", "mode": mode, "offset": 2}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_without_offset(schema):
    """Tests valid combination of mode without offset."""
    modes_without_offset = ["total", "1hour", "1day", "30day"]
    for mode in modes_without_offset:
        instance = {"req": "card.usage.get", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all optional fields."""
    instance = {"req": "card.usage.get", "mode": "total", "offset": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.usage.get", "extra": "field"}
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
