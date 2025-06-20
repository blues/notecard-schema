import pytest
import jsonschema
import json

SCHEMA_FILE = "card.wireless.penalty.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.wireless.penalty"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.wireless.penalty"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.wireless.penalty", "cmd": "card.wireless.penalty"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "card.wireless.penalty", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "card.wireless.penalty", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_reset(schema):
    """Tests valid reset field."""
    instance = {"req": "card.wireless.penalty", "reset": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "reset": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_reset_invalid_type(schema):
    """Tests invalid type for reset."""
    instance = {"req": "card.wireless.penalty", "reset": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_set(schema):
    """Tests valid set field."""
    instance = {"req": "card.wireless.penalty", "set": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "set": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_set_invalid_type(schema):
    """Tests invalid type for set."""
    instance = {"req": "card.wireless.penalty", "set": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_rate(schema):
    """Tests valid rate field."""
    instance = {"req": "card.wireless.penalty", "rate": 2.0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "rate": 1.25}
    jsonschema.validate(instance=instance, schema=schema)

def test_rate_invalid_type(schema):
    """Tests invalid type for rate."""
    instance = {"req": "card.wireless.penalty", "rate": "2.0"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'2.0' is not of type 'number'" in str(excinfo.value)

def test_valid_add(schema):
    """Tests valid add field."""
    instance = {"req": "card.wireless.penalty", "add": 10}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "add": 15}
    jsonschema.validate(instance=instance, schema=schema)

def test_add_invalid_type(schema):
    """Tests invalid type for add."""
    instance = {"req": "card.wireless.penalty", "add": "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {"req": "card.wireless.penalty", "max": 720}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "max": 4320}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"req": "card.wireless.penalty", "max": "720"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'720' is not of type 'integer'" in str(excinfo.value)

def test_valid_min(schema):
    """Tests valid min field."""
    instance = {"req": "card.wireless.penalty", "min": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "min": 15}
    jsonschema.validate(instance=instance, schema=schema)

def test_min_invalid_type(schema):
    """Tests invalid type for min."""
    instance = {"req": "card.wireless.penalty", "min": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_set_with_override_fields(schema):
    """Tests valid request with set and override fields."""
    instance = {
        "req": "card.wireless.penalty", 
        "set": True, 
        "rate": 2.0, 
        "add": 10, 
        "max": 720, 
        "min": 5
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_reset_only(schema):
    """Tests valid request with only reset field."""
    instance = {"req": "card.wireless.penalty", "reset": True}
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
