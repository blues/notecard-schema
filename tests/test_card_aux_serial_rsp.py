import pytest
import jsonschema

SCHEMA_FILE = "card.aux.serial.rsp.notecard.api.json"

def test_valid_empty_response(schema):
    """Tests the minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_properties(schema):
    """Tests that additional properties are allowed as per schema default."""
    instance = {"some_field": 123, "another": "value"}
    # This should be valid because additionalProperties is not set to false
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_type(schema):
    """Tests that non-object types are invalid."""
    invalid_instances = [
        None,       # null
        [],         # array
        "string",   # string
        123,        # integer
        True        # boolean
    ]
    for instance in invalid_instances:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'object'" in str(excinfo.value)
