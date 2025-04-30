import pytest
import jsonschema

SCHEMA_FILE = "card.dfu.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.dfu"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.dfu"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.dfu", "cmd": "card.dfu"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_name(schema):
    """Tests valid name enum values."""
    valid_names = ["esp32", "stm32", "stm32-bi", "-"]
    for name in valid_names:
        instance = {"req": "card.dfu", "name": name}
        jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_enum(schema):
    """Tests invalid name enum value."""
    instance = {"req": "card.dfu", "name": "invalid_mcu"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid_mcu' is not one of ['esp32'," in str(excinfo.value)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"req": "card.dfu", "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_on(schema):
    """Tests valid on field."""
    instance = {"req": "card.dfu", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.dfu", "on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {"req": "card.dfu", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_off(schema):
    """Tests valid off field."""
    instance = {"req": "card.dfu", "off": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.dfu", "off": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_off_invalid_type(schema):
    """Tests invalid type for off."""
    instance = {"req": "card.dfu", "off": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"req": "card.dfu", "seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.dfu", "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "card.dfu", "seconds": 3600.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "3600.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_stop(schema):
    """Tests valid stop field."""
    instance = {"req": "card.dfu", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.dfu", "stop": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_stop_invalid_type(schema):
    """Tests invalid type for stop."""
    instance = {"req": "card.dfu", "stop": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_valid_off_with_seconds(schema):
    """Tests valid combination of off and seconds."""
    instance = {"req": "card.dfu", "off": True, "seconds": 60}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all optional fields."""
    instance = {
        "req": "card.dfu",
        "name": "esp32",
        "on": True,
        "off": False, # Note: on/off are independent
        "seconds": 120,
        "stop": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.dfu", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)
