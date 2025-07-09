import pytest
import jsonschema
import json

SCHEMA_FILE = "card.triangulate.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.triangulate"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.triangulate"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.triangulate", "cmd": "card.triangulate"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "card.triangulate", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "card.triangulate", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_on_parameter(schema):
    """Tests valid on parameter."""
    instance = {"req": "card.triangulate", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.triangulate", "on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_set_parameter(schema):
    """Tests valid set parameter."""
    instance = {"req": "card.triangulate", "set": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.triangulate", "set": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_minutes_parameter(schema):
    """Tests valid minutes parameter."""
    instance = {"req": "card.triangulate", "minutes": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.triangulate", "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_negative_valid(schema):
    """Tests that negative minutes are allowed (no minimum constraint in schema)."""
    instance = {"req": "card.triangulate", "minutes": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_text_parameter(schema):
    """Tests valid text parameter."""
    instance = {"req": "card.triangulate", "text": "ESP32 AT+CWLAP output\n"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_parameter(schema):
    """Tests valid mode parameter."""
    instance = {"req": "card.triangulate", "mode": "cell"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.triangulate", "mode": "wifi"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.triangulate", "mode": "-"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_usb_parameter(schema):
    """Tests valid usb parameter."""
    instance = {"req": "card.triangulate", "usb": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.triangulate", "usb": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_time_parameter(schema):
    """Tests valid time parameter."""
    instance = {"req": "card.triangulate", "time": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.triangulate", "time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_parameters(schema):
    """Tests valid request with all parameters."""
    instance = {
        "req": "card.triangulate",
        "mode": "wifi",
        "on": True,
        "set": True,
        "minutes": 5,
        "text": "WiFi access point data\n",
        "usb": True,
        "time": 1678886400
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
