import pytest
import jsonschema
import json

SCHEMA_FILE = "card.status.rsp.notecard.api.json"

REQUIRED_FIELDS = {
    "status": "{normal}",
    "time": 1598367163,
    "storage": 8,
    "usb": True,
    "connected": True,
    "gps": True,
    "sync": True,
    "inbound": 12,
    "outbound": 34
}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with all required fields."""
    instance = {**REQUIRED_FIELDS}
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

def test_missing_required_time(schema):
    """Tests that 'time' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["time"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'time' is a required property" in str(excinfo.value)

def test_missing_required_storage(schema):
    """Tests that 'storage' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["storage"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'storage' is a required property" in str(excinfo.value)

def test_missing_required_usb(schema):
    """Tests that 'usb' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["usb"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'usb' is a required property" in str(excinfo.value)

def test_missing_required_connected(schema):
    """Tests that 'connected' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["connected"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'connected' is a required property" in str(excinfo.value)

def test_missing_required_gps(schema):
    """Tests that 'gps' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["gps"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'gps' is a required property" in str(excinfo.value)

def test_missing_required_sync(schema):
    """Tests that 'sync' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["sync"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'sync' is a required property" in str(excinfo.value)

def test_missing_required_inbound(schema):
    """Tests that 'inbound' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["inbound"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'inbound' is a required property" in str(excinfo.value)

def test_missing_required_outbound(schema):
    """Tests that 'outbound' is required."""
    instance = {**REQUIRED_FIELDS}
    del instance["outbound"]
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'outbound' is a required property" in str(excinfo.value)

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
    """Tests that non-required fields (cell, wifi) are optional."""
    instance = {**REQUIRED_FIELDS}
    jsonschema.validate(instance=instance, schema=schema)

    instance_with_cell = {**REQUIRED_FIELDS, "cell": True}
    jsonschema.validate(instance=instance_with_cell, schema=schema)

    instance_with_wifi = {**REQUIRED_FIELDS, "wifi": True}
    jsonschema.validate(instance=instance_with_wifi, schema=schema)

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
