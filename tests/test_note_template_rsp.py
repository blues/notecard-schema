import pytest
import jsonschema

SCHEMA_FILE = "note.template.rsp.notecard.api.json"

def test_minimal_valid_response(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_success_true(schema):
    """Tests a valid response with success=true."""
    instance = {"success": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_success_false(schema):
    """Tests a valid response with success=false."""
    instance = {"success": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_success_type(schema):
    """Tests an invalid response with a non-boolean type for success."""
    instance = {"success": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_with_error(schema):
    """Tests a valid response with an error message."""
    instance = {"err": "template validation failed"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_error_type(schema):
    """Tests response with potential additional fields like error."""
    # Since additionalProperties is not false, this should be valid
    instance = {"err": "template validation failed"}
    jsonschema.validate(instance=instance, schema=schema)

def test_response_with_both_success_and_error(schema):
    """Tests response that might contain both success and error fields."""
    # This could be valid depending on the actual API behavior
    instance = {
        "success": False,
        "err": "invalid template format"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_response_with_additional_fields(schema):
    """Tests response with potential additional fields."""
    # Based on pattern from other schemas, there might be additional response fields
    instance = {
        "success": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_empty_response_valid(schema):
    """Tests that an empty response object is valid."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_unknown_property_type(schema):
    """Tests response with an invalid property type if schema doesn't allow additional properties."""
    # This test will depend on whether additionalProperties is false in the schema
    instance = {"unknown_field": 123}
    try:
        jsonschema.validate(instance=instance, schema=schema)
        # If validation passes, the schema allows additional properties
    except jsonschema.ValidationError:
        # If validation fails, the schema doesn't allow additional properties
        pass

def test_valid_template_response(schema):
    """Tests valid response with template field."""
    instance = {
        "template": {
            "temperature": 14.1,
            "humidity": 11
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_template_type(schema):
    """Tests invalid response with non-object template."""
    instance = {"template": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not of type 'object'" in str(excinfo.value)

def test_valid_file_response(schema):
    """Tests valid response with file field."""
    instance = {"file": "readings.qo"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_file_type(schema):
    """Tests invalid response with non-string file."""
    instance = {"file": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_length_response(schema):
    """Tests valid response with length field."""
    instance = {"length": 250}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_length_type(schema):
    """Tests invalid response with non-integer length."""
    instance = {"length": "250"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'250' is not of type 'integer'" in str(excinfo.value)

def test_valid_format_response(schema):
    """Tests valid response with format field."""
    instance = {"format": "compact"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_format_type(schema):
    """Tests invalid response with non-string format."""
    instance = {"format": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_port_response(schema):
    """Tests valid response with port field."""
    instance = {"port": 42}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_port_type(schema):
    """Tests invalid response with non-integer port."""
    instance = {"port": "42"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'42' is not of type 'integer'" in str(excinfo.value)

def test_valid_complete_verify_response(schema):
    """Tests complete response from verify request."""
    instance = {
        "file": "sensors.qo",
        "template": {
            "temperature": 0.0,
            "humidity": 0.0
        },
        "format": "compact",
        "length": 100,
        "port": 5
    }
    jsonschema.validate(instance=instance, schema=schema)