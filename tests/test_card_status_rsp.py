import pytest
import jsonschema
import json

SCHEMA_FILE = "card.status.rsp.notecard.api.json"

REQUIRED_FIELDS = {
    "status": "{normal}",
    "usb": True
}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with all required fields."""
    instance = {"status": "{normal}", "usb": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {**REQUIRED_FIELDS, "status": "{normal}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {**REQUIRED_FIELDS, "status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_missing_required_status(schema):
    """Tests that 'status' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["status"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'status' is a required property" in str(excinfo.value)

def test_missing_required_usb(schema):
    """Tests that 'usb' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["usb"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'usb' is a required property" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["usb", "connected", "cell", "sync", "gps", "wifi"]
)
def test_valid_boolean_field(schema, field_name):
    """Tests valid boolean type for various fields."""
    instance = {**REQUIRED_FIELDS, field_name: True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, field_name: False}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["usb", "connected", "cell", "sync", "gps", "wifi"]
)
def test_invalid_type_for_boolean_field(schema, field_name):
    """Tests invalid type for various boolean fields."""
    instance = {**REQUIRED_FIELDS, field_name: "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["storage", "time", "inbound", "outbound"]
)
def test_valid_integer_field(schema, field_name):
    """Tests valid integer type for various fields."""
    instance = {**REQUIRED_FIELDS, field_name: 10}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, field_name: 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {**REQUIRED_FIELDS, field_name: -5}
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name",
    ["storage", "time", "inbound", "outbound"]
)
def test_invalid_type_for_integer_field(schema, field_name):
    """Tests invalid (string) type for various integer fields."""
    instance = {**REQUIRED_FIELDS, field_name: "10"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'10' is not of type 'integer'" in str(excinfo.value)

@pytest.mark.parametrize(
    "field_name",
    ["storage", "time", "inbound", "outbound"]
)
def test_invalid_float_type_for_integer_field(schema, field_name):
    """Tests invalid (float) type for various integer fields."""
    instance = {**REQUIRED_FIELDS, field_name: 10.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "10.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "status": "{normal}",
        "usb": True,
        "storage": 5,
        "time": 1700000000,
        "connected": True,
        "cell": True,
        "gps": False,
        "wifi": True,
        "sync": False,
        "inbound": 0,
        "outbound": 2
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_all_non_required_fields_optional(schema):
    """Tests that non-required fields are optional."""
    instance = {**REQUIRED_FIELDS}
    jsonschema.validate(instance=instance, schema=schema)

    instance_with_cell = {**REQUIRED_FIELDS, "cell": True}
    jsonschema.validate(instance=instance_with_cell, schema=schema)

    instance_with_wifi = {**REQUIRED_FIELDS, "wifi": True}
    jsonschema.validate(instance=instance_with_wifi, schema=schema)

    instance_with_time = {**REQUIRED_FIELDS, "time": 1598367163}
    jsonschema.validate(instance=instance_with_time, schema=schema)

    instance_with_storage = {**REQUIRED_FIELDS, "storage": 8}
    jsonschema.validate(instance=instance_with_storage, schema=schema)

    instance_with_connected = {**REQUIRED_FIELDS, "connected": True}
    jsonschema.validate(instance=instance_with_connected, schema=schema)

    instance_with_gps = {**REQUIRED_FIELDS, "gps": True}
    jsonschema.validate(instance=instance_with_gps, schema=schema)

    instance_with_sync = {**REQUIRED_FIELDS, "sync": True}
    jsonschema.validate(instance=instance_with_sync, schema=schema)

    instance_with_inbound = {**REQUIRED_FIELDS, "inbound": 12}
    jsonschema.validate(instance=instance_with_inbound, schema=schema)

    instance_with_outbound = {**REQUIRED_FIELDS, "outbound": 34}
    jsonschema.validate(instance=instance_with_outbound, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {**REQUIRED_FIELDS, "extra": "info"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        **REQUIRED_FIELDS,
        "extra": "info",
        "another": "field"
    }
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
