import pytest
import jsonschema
import json

SCHEMA_FILE = "card.triangulate.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_motion_field(schema):
    """Tests valid motion field."""
    instance = {"motion": 1606757487}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Motion cannot be negative
    instance = {"motion": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_time_field(schema):
    """Tests valid time field."""
    instance = {"time": 1606755042}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Time cannot be negative
    instance = {"time": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_mode_field(schema):
    """Tests valid mode field."""
    instance = {"mode": "wifi,cell"}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"mode": "cell"}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_on_field(schema):
    """Tests valid on field."""
    instance = {"on": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {"on": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_usb_field(schema):
    """Tests valid usb field."""
    instance = {"usb": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"usb": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_usb_invalid_type(schema):
    """Tests invalid type for usb."""
    instance = {"usb": "yes"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'yes' is not of type 'boolean'" in str(excinfo.value)

def test_length_field(schema):
    """Tests valid length field."""
    instance = {"length": 443}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"length": 0}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Length cannot be negative
    instance = {"length": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_length_invalid_type(schema):
    """Tests invalid type for length."""
    instance = {"length": "443"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'443' is not of type 'integer'" in str(excinfo.value)

def test_complete_triangulation_response(schema):
    """Tests a complete valid triangulation response."""
    instance = {
        "usb": True,
        "mode": "wifi,cell",
        "length": 443,
        "on": True,
        "time": 1606755042,
        "motion": 1606757487
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_partial_response(schema):
    """Tests valid partial response."""
    instance = {
        "on": False,
        "usb": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_only_response(schema):
    """Tests valid response with mode only."""
    instance = {
        "mode": "cell"
    }
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
