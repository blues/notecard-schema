import pytest
import jsonschema
import json

SCHEMA_FILE = "card.wifi.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.wifi"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.wifi"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"ssid": "MyNetwork"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.wifi", "cmd": "card.wifi"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "invalid.req"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "invalid.cmd"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_ssid(schema):
    """Tests valid ssid parameter."""
    instance = {"req": "card.wifi", "ssid": "MyNetwork"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_ssid_clear(schema):
    """Tests valid ssid parameter with clear value."""
    instance = {"req": "card.wifi", "ssid": "-"}
    jsonschema.validate(instance=instance, schema=schema)

def test_ssid_invalid_type(schema):
    """Tests invalid type for ssid."""
    instance = {"req": "card.wifi", "ssid": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_password(schema):
    """Tests valid password parameter."""
    instance = {"req": "card.wifi", "password": "mypassword123"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_password_clear(schema):
    """Tests valid password parameter with clear value."""
    instance = {"req": "card.wifi", "password": "-"}
    jsonschema.validate(instance=instance, schema=schema)

def test_password_invalid_type(schema):
    """Tests invalid type for password."""
    instance = {"req": "card.wifi", "password": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_name(schema):
    """Tests valid name parameter."""
    instance = {"req": "card.wifi", "name": "MyNotecard"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_name_with_dash(schema):
    """Tests valid name parameter with dash suffix for MAC append."""
    instance = {"req": "card.wifi", "name": "acme-"}
    jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"req": "card.wifi", "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_org(schema):
    """Tests valid org parameter."""
    instance = {"req": "card.wifi", "org": "My Company"}
    jsonschema.validate(instance=instance, schema=schema)

def test_org_invalid_type(schema):
    """Tests invalid type for org."""
    instance = {"req": "card.wifi", "org": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_start_true(schema):
    """Tests valid start parameter with true value."""
    instance = {"req": "card.wifi", "start": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_start_false(schema):
    """Tests valid start parameter with false value."""
    instance = {"req": "card.wifi", "start": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_start_invalid_type(schema):
    """Tests invalid type for start."""
    instance = {"req": "card.wifi", "start": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_text(schema):
    """Tests valid text parameter with access point array."""
    instance = {"req": "card.wifi", "text": "[\"SSID1\",\"PASS1\"],[\"SSID2\",\"PASS2\"]"}
    jsonschema.validate(instance=instance, schema=schema)

def test_text_invalid_type(schema):
    """Tests invalid type for text."""
    instance = {"req": "card.wifi", "text": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_all_parameters(schema):
    """Tests valid request with all parameters."""
    instance = {
        "req": "card.wifi",
        "ssid": "MyNetwork",
        "password": "mypassword",
        "name": "CustomNotecard-",
        "org": "My Organization",
        "start": True,
        "text": "[\"BACKUP-SSID\",\"BACKUP-PASS\"]"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.wifi", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

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
