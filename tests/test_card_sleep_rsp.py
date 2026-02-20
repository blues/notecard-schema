import pytest
import jsonschema
import json

SCHEMA_FILE = "card.sleep.rsp.notecard.api.json"

REQUIRED_FIELDS = {"on": True, "off": False, "seconds": 60}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only required fields."""
    instance = {"on": True, "off": False, "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_on(schema):
    """Tests that on is required."""
    instance = {"off": False, "seconds": 60}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'on' is a required property" in str(excinfo.value)

def test_missing_required_off(schema):
    """Tests that off is required."""
    instance = {"on": True, "seconds": 60}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'off' is a required property" in str(excinfo.value)

def test_missing_required_seconds(schema):
    """Tests that seconds is required."""
    instance = {"on": True, "off": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'seconds' is a required property" in str(excinfo.value)

def test_valid_on_field(schema):
    """Tests valid on field."""
    instance = {**REQUIRED_FIELDS, "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {**REQUIRED_FIELDS, "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_off_field(schema):
    """Tests valid off field."""
    instance = {**REQUIRED_FIELDS, "off": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "off": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_off_invalid_type(schema):
    """Tests invalid type for off."""
    instance = {**REQUIRED_FIELDS, "off": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_valid_seconds_field(schema):
    """Tests valid seconds field."""
    instance = {**REQUIRED_FIELDS, "seconds": 30}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "seconds": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {**REQUIRED_FIELDS, "seconds": "60"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'60' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_float(schema):
    """Tests invalid float type for seconds."""
    instance = {**REQUIRED_FIELDS, "seconds": 60.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "60.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_mode_field(schema):
    """Tests valid mode field."""
    instance = {**REQUIRED_FIELDS, "mode": "accel"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "mode": "-accel"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "mode": "custom_mode"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, "mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {**REQUIRED_FIELDS, "mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_number(schema):
    """Tests invalid number type for mode."""
    instance = {**REQUIRED_FIELDS, "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name,field_type,valid_values",
    [
        ("on", "boolean", [True, False]),
        ("off", "boolean", [True, False]),
        ("seconds", "integer", [0, 30, 60, 3600, -1]),
        ("mode", "string", ["accel", "-accel", "custom", ""])
    ]
)
def test_valid_field_types(schema, field_name, field_type, valid_values):
    """Tests valid field types for various response fields."""
    for value in valid_values:
        instance = {**REQUIRED_FIELDS, field_name: value}
        jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name,invalid_values",
    [
        ("on", ["true", "false", 1, 0, None]),
        ("off", ["true", "false", 1, 0, None]),
        ("seconds", ["60", 60.5, True, None]),
        ("mode", [True, False, 123, None])
    ]
)
def test_invalid_field_types(schema, field_name, invalid_values):
    """Tests invalid field types for various response fields."""
    for value in invalid_values:
        instance = {**REQUIRED_FIELDS, field_name: value}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "on": True,
        "off": False,
        "seconds": 60,
        "mode": "accel"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_all_non_required_fields_optional(schema):
    """Tests valid response with only required fields (non-required fields are optional)."""
    instance = {"on": True, "off": False, "seconds": 30}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"on": True, "off": False, "seconds": 30, "status": "enabled"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('status' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        "on": True,
        "off": False,
        "seconds": 60,
        "status": "enabled",
        "extra": "field"
    }
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
