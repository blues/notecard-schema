import pytest
import jsonschema
import json

SCHEMA_FILE = "ntn.config.rsp.notecard.api.json"

STRING_FIELDS = [
    "device", "modem", "policy", "sku", "ordering_code", "apn", "band",
    "channel", "org", "product", "target", "version", "built"
]

INTEGER_FIELDS = [
    "mtu", "up_mtu", "down_mtu",
    "ver_major", "ver_minor", "ver_patch", "ver_build"
]

def test_valid_empty_response(schema):
    """Tests a valid empty response."""
    jsonschema.validate(instance={}, schema=schema)

def test_valid_empty_body(schema):
    """Tests a response with an empty body object."""
    jsonschema.validate(instance={"body": {}}, schema=schema)

def test_valid_full_response(schema):
    """Tests a response with every documented body field."""
    instance = {
        "body": {
            "device": "skylo:901980000000000",
            "mtu": 256,
            "modem": "CC660DLSAAR01A03_01.001.01.001",
            "policy": "10TPM",
            "sku": "NTN-SKY1",
            "ordering_code": "AZ",
            "apn": "blues.prod",
            "band": "0",
            "channel": "0",
            "org": "Blues Inc",
            "product": "Starnote",
            "target": "Starnote",
            "version": "starnote-s-10.2.2.17790",
            "ver_major": 10,
            "ver_minor": 2,
            "ver_patch": 2,
            "ver_build": 17790,
            "built": "Sep 03 2026 12:40:29",
            "down_mtu": 256,
            "up_mtu": 256
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_error_response(schema):
    """Tests valid response with error field."""
    instance = {"err": "no NTN module is connected {no-ntn-module}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_string_fields(schema):
    """Tests each string body field individually."""
    for field in STRING_FIELDS:
        jsonschema.validate(instance={"body": {field: "value"}}, schema=schema)

def test_valid_integer_fields(schema):
    """Tests each integer body field individually."""
    for field in INTEGER_FIELDS:
        jsonschema.validate(instance={"body": {field: 42}}, schema=schema)

def test_invalid_string_field_types(schema):
    """Tests invalid types for string body fields."""
    for field in STRING_FIELDS:
        for bad in [123, True, [], {}]:
            with pytest.raises(jsonschema.ValidationError) as excinfo:
                jsonschema.validate(instance={"body": {field: bad}}, schema=schema)
            assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_integer_field_types(schema):
    """Tests invalid types for integer body fields."""
    for field in INTEGER_FIELDS:
        for bad in ["256", 1.5, True, [], {}]:
            with pytest.raises(jsonschema.ValidationError) as excinfo:
                jsonschema.validate(instance={"body": {field: bad}}, schema=schema)
            assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_err_type(schema):
    """Tests invalid types for err field."""
    for bad in [123, True, [], {}]:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance={"err": bad}, schema=schema)
        assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_body_type(schema):
    """Tests that body must be an object."""
    for bad in ["string", 123, True, ["array"]]:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance={"body": bad}, schema=schema)
        assert "is not of type 'object'" in str(excinfo.value)

def test_invalid_body_additional_property(schema):
    """Tests invalid body with additional property."""
    instance = {"body": {"version": "starnote-s-10.2.2.17790", "extra": "not allowed"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_top_level_field(schema):
    """Tests that body fields are not accepted at the top level."""
    instance = {"version": "starnote-s-10.2.2.17790"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]

    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_additional_properties_false(schema):
    """Tests that unevaluatedProperties is set to false."""
    assert schema.get("unevaluatedProperties") is False

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
