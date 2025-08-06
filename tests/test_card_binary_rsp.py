import pytest
import jsonschema
import json

SCHEMA_FILE = "card.binary.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_all_fields(schema):
    """Tests a valid response with all fields populated."""
    instance = {
        "cobs": 128,
        "connected": True,
        "length": 100,
        "max": 130554,
        "status": "ce6fdef565eeecf14ab38d83643b922d",
        "err": "some error description"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_some_fields(schema):
    """Tests a valid response with a subset of fields."""
    instance = {
        "connected": False,
        "length": 50
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_valid(schema):
    """Tests valid cobs values (integer)."""
    instance = {"cobs": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"cobs": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_cobs_invalid_type(schema):
    """Tests invalid type for cobs."""
    instance = {"cobs": "128"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'128' is not of type 'integer'" in str(excinfo.value)

def test_connected_valid(schema):
    """Tests valid connected values (boolean)."""
    instance = {"connected": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_connected_invalid_type(schema):
    """Tests invalid type for connected."""
    instance = {"connected": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_length_valid(schema):
    """Tests valid length values (integer)."""
    instance = {"length": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"length": 5000}
    jsonschema.validate(instance=instance, schema=schema)

def test_length_invalid_type(schema):
    """Tests invalid type for length."""
    instance = {"length": 100.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "100.5 is not of type 'integer'" in str(excinfo.value)

def test_err_valid(schema):
    """Tests valid err value (string)."""
    instance = {"err": "{error-message}"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"err": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_err_invalid_type(schema):
    """Tests invalid type for err."""
    instance = {"err": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_max_valid(schema):
    """Tests valid max values (integer)."""
    instance = {"max": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"max": 130554}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"max": "130554"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'130554' is not of type 'integer'" in str(excinfo.value)

def test_status_valid(schema):
    """Tests valid status value (string)."""
    instance = {"status": "ce6fdef565eeecf14ab38d83643b922d"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property (allowed by default)."""
    instance = {"cobs": 10, "extra_field": "hello"}
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
