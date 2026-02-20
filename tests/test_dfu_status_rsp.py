import pytest
import jsonschema
import json

SCHEMA_FILE = "dfu.status.rsp.notecard.api.json"

REQUIRED_FIELDS = {"status": "no download in progress", "mode": "idle", "on": True}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with required fields."""
    instance = {"status": "no download in progress", "mode": "idle", "on": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_status(schema):
    """Tests that status is required."""
    instance = {"mode": "idle", "on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'status' is a required property" in str(excinfo.value)

def test_missing_required_mode(schema):
    """Tests that mode is required."""
    instance = {"status": "no download in progress", "on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'mode' is a required property" in str(excinfo.value)

def test_missing_required_on(schema):
    """Tests that on is required."""
    instance = {"status": "no download in progress", "mode": "idle"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'on' is a required property" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = ["idle", "error", "downloading", "ready", "completed"]
    for mode in valid_modes:
        instance = {"status": "test status", "mode": mode, "on": True}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"status": "test status", "mode": "invalid", "on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['idle', 'error', 'downloading', 'ready', 'completed']" in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"status": "test status", "mode": 123, "on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"status": "successfully downloaded", "mode": "ready", "on": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 123, "mode": "idle", "on": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_on_off(schema):
    """Tests valid on/off fields."""
    instance = {"status": "test", "mode": "idle", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "test", "mode": "idle", "on": True, "off": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {"status": "test", "mode": "idle", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_off_invalid_type(schema):
    """Tests invalid type for off."""
    instance = {"status": "test", "mode": "idle", "on": True, "off": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_pending(schema):
    """Tests valid pending field."""
    instance = {"status": "downloading", "mode": "downloading", "on": True, "pending": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"status": "idle", "mode": "idle", "on": True, "pending": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_pending_invalid_type(schema):
    """Tests invalid type for pending."""
    instance = {"status": "test", "mode": "idle", "on": True, "pending": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_body(schema):
    """Tests valid body field."""
    instance = {"status": "ready", "mode": "ready", "on": True, "body": {"length": 42892, "md5": "5a3f73a7f1b4bc8917b12b36c2532969"}}
    jsonschema.validate(instance=instance, schema=schema)

def test_body_invalid_type(schema):
    """Tests invalid type for body."""
    instance = {"status": "test", "mode": "idle", "on": True, "body": "not an object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not an object' is not of type 'object'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "mode": "ready",
        "status": "successfully downloaded",
        "on": True,
        "body": {
            "crc32": 2525287425,
            "created": 1599163431,
            "info": {},
            "length": 42892,
            "md5": "5a3f73a7f1b4bc8917b12b36c2532969",
            "modified": 1599163431,
            "name": "stm32-new-firmware$20200903200351.bin",
            "notes": "Latest prod firmware",
            "source": "stm32-new-firmware.bin",
            "type": "firmware"
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_all_non_required_fields_optional(schema):
    """Tests that all non-required fields are optional."""
    instance = {"status": "idle", "mode": "idle", "on": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"status": "test", "mode": "ready", "on": True, "extra": 123}
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
