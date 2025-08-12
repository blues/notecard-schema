import pytest
import jsonschema
import json

SCHEMA_FILE = "card.sleep.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_on_field(schema):
    """Tests valid on field."""
    instance = {"on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {"on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_off_field(schema):
    """Tests valid off field."""
    instance = {"off": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"off": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_off_invalid_type(schema):
    """Tests invalid type for off."""
    instance = {"off": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_valid_seconds_field(schema):
    """Tests valid seconds field."""
    instance = {"seconds": 30}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"seconds": "60"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'60' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_float(schema):
    """Tests invalid float type for seconds."""
    instance = {"seconds": 60.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "60.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_mode_field(schema):
    """Tests valid mode field."""
    instance = {"mode": "accel"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "-accel"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "custom_mode"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_number(schema):
    """Tests invalid number type for mode."""
    instance = {"mode": 123}
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
        instance = {field_name: value}
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
        instance = {field_name: value}
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

def test_valid_partial_fields(schema):
    """Tests valid response with partial fields."""
    instance = {"on": True, "seconds": 30}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"mode": "accel", "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"off": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"on": True, "seconds": 30, "status": "enabled"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('status' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        "on": True,
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
