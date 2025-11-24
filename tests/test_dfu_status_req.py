import pytest
import jsonschema
import json

SCHEMA_FILE = "dfu.status.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "dfu.status"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "dfu.status"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "dfu.status", "cmd": "dfu.status"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'dfu.status' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'dfu.status' was expected" in str(excinfo.value)

def test_valid_name_enums(schema):
    """Tests valid name enum values."""
    valid_names = ["user", "card"]
    for name in valid_names:
        instance = {"req": "dfu.status", "name": name}
        jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_enum(schema):
    """Tests invalid name enum value."""
    instance = {"req": "dfu.status", "name": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['user', 'card']" in str(excinfo.value)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"req": "dfu.status", "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_stop(schema):
    """Tests valid stop field."""
    instance = {"req": "dfu.status", "stop": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "dfu.status", "stop": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_stop_invalid_type(schema):
    """Tests invalid type for stop."""
    instance = {"req": "dfu.status", "stop": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"req": "dfu.status", "status": "Update cancelled by user"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"req": "dfu.status", "status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_version_string(schema):
    """Tests valid version as string."""
    instance = {"req": "dfu.status", "version": "1.2.4"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_version_object(schema):
    """Tests valid version as object."""
    instance = {"req": "dfu.status", "version": {"ver_major": 1, "ver_minor": 2}}
    jsonschema.validate(instance=instance, schema=schema)

def test_version_invalid_type(schema):
    """Tests invalid type for version."""
    instance = {"req": "dfu.status", "version": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string', 'object'" in str(excinfo.value)

def test_valid_vvalue(schema):
    """Tests valid vvalue field."""
    instance = {"req": "dfu.status", "vvalue": "usb:1;high:1;normal:0;low:0;dead:0"}
    jsonschema.validate(instance=instance, schema=schema)

def test_vvalue_invalid_type(schema):
    """Tests invalid type for vvalue."""
    instance = {"req": "dfu.status", "vvalue": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_on_off(schema):
    """Tests valid on/off fields."""
    instance = {"req": "dfu.status", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "dfu.status", "off": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_off_invalid_type(schema):
    """Tests invalid type for on/off."""
    instance = {"req": "dfu.status", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_err(schema):
    """Tests valid err field."""
    instance = {"req": "dfu.status", "err": "Firmware corrupted"}
    jsonschema.validate(instance=instance, schema=schema)

def test_err_invalid_type(schema):
    """Tests invalid type for err."""
    instance = {"req": "dfu.status", "err": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "dfu.status", "extra": 123}
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
