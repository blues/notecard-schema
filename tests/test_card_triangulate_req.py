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

def test_on_field_valid(schema):
    """Tests valid 'on' field values."""
    # Valid boolean values
    instance = {"req": "card.triangulate", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_field_invalid_type(schema):
    """Tests invalid type for 'on' field."""
    instance = {"req": "card.triangulate", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_on_field_invalid_number(schema):
    """Tests invalid number type for 'on' field."""
    instance = {"req": "card.triangulate", "on": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_mode_values(schema):
    """Tests valid mode field values."""
    # Valid single modes
    instance = {"req": "card.triangulate", "mode": "cell"}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "mode": "wifi"}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Valid combined modes
    instance = {"req": "card.triangulate", "mode": "wifi,cell"}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "mode": "cell,wifi"}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Clear mode
    instance = {"req": "card.triangulate", "mode": "-"}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_values(schema):
    """Tests invalid mode field values."""
    # Invalid mode value
    instance = {"req": "card.triangulate", "mode": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "does not match" in str(excinfo.value)
    
    # Invalid combination
    instance = {"req": "card.triangulate", "mode": "cell,wifi,invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "does not match" in str(excinfo.value)

def test_usb_field_valid(schema):
    """Tests valid 'usb' field values."""
    instance = {"req": "card.triangulate", "usb": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "usb": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_usb_field_invalid_type(schema):
    """Tests invalid type for 'usb' field."""
    instance = {"req": "card.triangulate", "usb": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_set_field_valid(schema):
    """Tests valid 'set' field values."""
    instance = {"req": "card.triangulate", "set": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "set": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_set_field_invalid_type(schema):
    """Tests invalid type for 'set' field."""
    instance = {"req": "card.triangulate", "set": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_minutes_field_valid(schema):
    """Tests valid 'minutes' field values."""
    instance = {"req": "card.triangulate", "minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "minutes": 60}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "minutes": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_field_invalid_type(schema):
    """Tests invalid type for 'minutes' field."""
    instance = {"req": "card.triangulate", "minutes": "60"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'60' is not of type 'integer'" in str(excinfo.value)

def test_minutes_below_minimum(schema):
    """Tests minutes value below minimum."""
    instance = {"req": "card.triangulate", "minutes": -2}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-2 is less than the minimum of -1" in str(excinfo.value)

def test_text_field_valid(schema):
    """Tests valid 'text' field values."""
    instance = {"req": "card.triangulate", "text": "+CWLAP:(4,\"Blues\",-51,\"74:ac:b9:12:12:f8\",1)\n"}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "text": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_text_field_invalid_type(schema):
    """Tests invalid type for 'text' field."""
    instance = {"req": "card.triangulate", "text": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_time_field_valid(schema):
    """Tests valid 'time' field values."""
    instance = {"req": "card.triangulate", "time": 1606755042}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.triangulate", "time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_field_invalid_type(schema):
    """Tests invalid type for 'time' field."""
    instance = {"req": "card.triangulate", "time": "1606755042"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1606755042' is not of type 'integer'" in str(excinfo.value)

def test_req_invalid_value(schema):
    """Tests invalid req value."""
    instance = {"req": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.triangulate' was expected" in str(excinfo.value)

def test_cmd_invalid_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.triangulate' was expected" in str(excinfo.value)

def test_valid_complete_request(schema):
    """Tests valid complete request with all fields."""
    instance = {
        "req": "card.triangulate",
        "mode": "wifi,cell",
        "on": True,
        "usb": True,
        "set": True,
        "minutes": 30,
        "text": "+CWLAP:(4,\"Blues\",-51,\"74:ac:b9:12:12:f8\",1)\n",
        "time": 1606755042
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_request_with_cmd_and_on(schema):
    """Tests valid request using 'cmd' with 'on' parameter."""
    instance = {"cmd": "card.triangulate", "on": True}
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
