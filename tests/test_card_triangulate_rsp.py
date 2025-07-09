import pytest
import jsonschema
import json

SCHEMA_FILE = "card.triangulate.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_motion(schema):
    """Tests valid motion field."""
    instance = {"motion": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"motion": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_motion_invalid_type(schema):
    """Tests invalid type for motion."""
    instance = {"motion": 1678886400.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1678886400.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_time(schema):
    """Tests valid time field."""
    instance = {"time": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {"time": 1678886400.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1678886400.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_mode(schema):
    """Tests valid mode field."""
    instance = {"mode": "cell"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "wifi,cell"}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_length(schema):
    """Tests valid length field."""
    instance = {"length": 1024}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"length": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_length_invalid_type(schema):
    """Tests invalid type for length."""
    instance = {"length": "1024"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1024' is not of type 'integer'" in str(excinfo.value)

def test_valid_on(schema):
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


def test_valid_usb(schema):
    """Tests valid usb field."""
    instance = {"usb": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"usb": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_usb_invalid_type(schema):
    """Tests invalid type for usb."""
    instance = {"usb": "enabled"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'enabled' is not of type 'boolean'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "motion": 1678886400,
        "time": 1678886500,
        "mode": "wifi,cell",
        "on": True,
        "usb": True,
        "length": 1024
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"time": 1678886400, "status": "ok"}
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
