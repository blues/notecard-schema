import pytest
import jsonschema
import json

SCHEMA_FILE = "note.template.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests a valid empty response."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_bytes_response(schema):
    """Tests valid response with bytes field."""
    instance = {"bytes": 40}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_template_set_response(schema):
    """Tests valid response when template is successfully set."""
    instance = {"bytes": 25}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_template_verify_response(schema):
    """Tests valid response when verifying existing template."""
    instance = {
        "template": True,
        "body": {"temperature": 14.1, "humidity": 11},
        "bytes": 40
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_template_with_format_response(schema):
    """Tests valid response showing compact format template."""
    instance = {
        "template": True,
        "format": "compact",
        "bytes": 25
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_template_with_length_response(schema):
    """Tests valid response with length field."""
    instance = {
        "template": True,
        "body": {"sensor": "temp-01", "value": 25.4},
        "length": 256,
        "bytes": 32
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_complete_verify_response(schema):
    """Tests complete response from verify request with all fields."""
    instance = {
        "bytes": 40,
        "template": True,
        "body": {
            "temperature": 0.0,
            "humidity": 0.0
        },
        "format": "compact",
        "length": 100
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_bytes_type(schema):
    """Tests invalid response with non-integer bytes."""
    instance = {"bytes": "40"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'40' is not of type 'integer'" in str(excinfo.value)

def test_invalid_template_type(schema):
    """Tests invalid response with non-boolean template."""
    instance = {"template": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not of type 'boolean'" in str(excinfo.value)

def test_invalid_body_type(schema):
    """Tests invalid response with non-object body."""
    instance = {"body": "should be object"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'should be object' is not of type 'object'" in str(excinfo.value)

def test_invalid_length_type(schema):
    """Tests invalid response with non-integer length."""
    instance = {"length": "250"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'250' is not of type 'integer'" in str(excinfo.value)

def test_invalid_format_type(schema):
    """Tests invalid response with non-string format."""
    instance = {"format": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"extra": "not allowed"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid response with multiple additional properties."""
    instance = {"extra1": 123, "extra2": "test"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

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
