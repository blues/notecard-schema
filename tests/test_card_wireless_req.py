import pytest
import jsonschema

SCHEMA_FILE = "card.wireless.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.wireless"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.wireless"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "auto"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.wireless", "cmd": "card.wireless"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = ["-", "auto", "m", "nb", "gprs"]
    for mode in valid_modes:
        instance = {"req": "card.wireless", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.wireless", "mode": "lte"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'lte' is not one of ['-'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.wireless", "mode": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_apn(schema):
    """Tests valid apn field."""
    instance = {"req": "card.wireless", "apn": "example.apn.com"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless", "apn": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_apn_invalid_type(schema):
    """Tests invalid type for apn."""
    instance = {"req": "card.wireless", "apn": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_method_enums(schema):
    """Tests valid method enum values."""
    valid_methods = ["-", "dual-primary-secondary", "dual-secondary-primary", "primary", "secondary"]
    for method in valid_methods:
        instance = {"req": "card.wireless", "method": method}
        jsonschema.validate(instance=instance, schema=schema)

def test_method_invalid_enum(schema):
    """Tests invalid method enum value."""
    instance = {"req": "card.wireless", "method": "primary_only"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'primary_only' is not one of ['-'," in str(excinfo.value)

def test_method_invalid_type(schema):
    """Tests invalid type for method."""
    instance = {"req": "card.wireless", "method": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {"req": "card.wireless", "mode": "auto", "apn": "test.apn", "method": "primary"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_hours_field(schema):
    """Tests valid hours field."""
    instance = {"req": "card.wireless", "method": "dual-primary-secondary", "hours": 24}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless", "method": "dual-secondary-primary", "hours": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_hours_invalid_type(schema):
    """Tests invalid type for hours field."""
    instance = {"req": "card.wireless", "hours": "24"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'24' is not of type 'integer'" in str(excinfo.value)

def test_hours_invalid_minimum(schema):
    """Tests hours field below minimum value."""
    instance = {"req": "card.wireless", "hours": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is less than the minimum of 1" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.wireless", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    import json
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}")
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
