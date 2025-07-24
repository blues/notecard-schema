import pytest
import jsonschema
import json

SCHEMA_FILE = "card.wireless.penalty.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"minutes": 69}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"minutes": "69"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'69' is not of type 'integer'" in str(excinfo.value)

def test_valid_count(schema):
    """Tests valid count field."""
    instance = {"count": 6}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"count": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"count": "6"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'6' is not of type 'integer'" in str(excinfo.value)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"status": "network: can't connect (55.4 min remaining) {registration-failure}{network}{extended-network-failure}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"seconds": 3324}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"seconds": "3324"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3324' is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {
        "seconds": 3324,
        "minutes": 69,
        "status": "network: can't connect (55.4 min remaining) {registration-failure}{network}{extended-network-failure}",
        "count": 6
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_no_penalty_status(schema):
    """Tests valid response with no active penalty."""
    instance = {"minutes": 0, "count": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_partial_fields(schema):
    """Tests valid response with partial fields."""
    instance = {"count": 3, "minutes": 15}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"minutes": 69, "additional": "property"}
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
