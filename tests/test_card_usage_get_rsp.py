import pytest
import jsonschema
import json

SCHEMA_FILE = "card.usage.get.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

# Test integer fields
@pytest.mark.parametrize(
    "field_name",
    [
        "seconds", "time", "bytes_sent", "bytes_received",
        "notes_sent", "notes_received", "sessions_standard", "sessions_secure"
    ]
)
def test_valid_integer_field(schema, field_name):
    """Tests valid integer type for various fields."""
    instance = {field_name: 123}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {field_name: -10} # Check if negative allowed
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    [
        "seconds", "time", "bytes_sent", "bytes_received",
        "notes_sent", "notes_received", "sessions_standard", "sessions_secure"
    ]
)
def test_invalid_type_for_integer_field(schema, field_name):
    """Tests invalid (string) type for various integer fields."""
    instance = {field_name: "123"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'123' is not of type 'integer'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    [
        "seconds", "time", "bytes_sent", "bytes_received", 
        "notes_sent", "notes_received", "sessions_standard", "sessions_secure"
    ]
)
def test_invalid_float_type_for_integer_field(schema, field_name):
    """Tests invalid (float) type for various integer fields."""
    instance = {field_name: 123.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields populated."""
    instance = {
        "seconds": 3600,
        "time": 1700000000,
        "bytes_sent": 1024,
        "bytes_received": 2048,
        "notes_sent": 10,
        "notes_received": 5,
        "sessions_standard": 2,
        "sessions_secure": 1
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"seconds": 60, "source": "live"}
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
