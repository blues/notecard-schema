import pytest
import jsonschema
import json

SCHEMA_FILE = "note.template.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "note.template"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "note.template"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "note.template", "cmd": "note.template"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "note.template", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "note.template", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_file_property(schema):
    """Tests valid file property."""
    instance = {"req": "note.template", "file": "readings.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_type(schema):
    """Tests invalid type for file property."""
    instance = {"req": "note.template", "file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_body_property(schema):
    """Tests valid body property."""
    instance = {"req": "note.template", "body": {"temperature": 14.1, "humidity": 11}}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_body_type(schema):
    """Tests invalid type for body property."""
    instance = {"req": "note.template", "body": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not an object' is not of type 'object'" in str(excinfo.value)

def test_valid_length_property(schema):
    """Tests valid length property."""
    instance = {"req": "note.template", "length": 100}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_length_type(schema):
    """Tests invalid type for length property."""
    instance = {"req": "note.template", "length": "100"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'100' is not of type 'integer'" in str(excinfo.value)

def test_valid_verify_property(schema):
    """Tests valid verify property."""
    instance = {"req": "note.template", "verify": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "note.template", "verify": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_verify_type(schema):
    """Tests invalid type for verify property."""
    instance = {"req": "note.template", "verify": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_format_property(schema):
    """Tests valid format property."""
    instance = {"req": "note.template", "format": "compact"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_format_type(schema):
    """Tests invalid type for format property."""
    instance = {"req": "note.template", "format": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_port_property(schema):
    """Tests valid port property."""
    instance = {"req": "note.template", "port": 50}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_port_type(schema):
    """Tests invalid type for port property."""
    instance = {"req": "note.template", "port": "50"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'50' is not of type 'integer'" in str(excinfo.value)

def test_valid_delete_property(schema):
    """Tests valid delete property."""
    instance = {"req": "note.template", "delete": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "note.template", "delete": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_delete_type(schema):
    """Tests invalid type for delete property."""
    instance = {"req": "note.template", "delete": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_complete_request(schema):
    """Tests a complete valid request with all properties."""
    instance = {
        "req": "note.template",
        "file": "readings.qo",
        "body": {"temperature": 14.1, "humidity": 11, "pump_state": "4"},
        "length": 100,
        "verify": False,
        "format": "compact",
        "port": 50,
        "delete": False
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
