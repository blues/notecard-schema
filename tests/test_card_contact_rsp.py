import pytest
import jsonschema
import json
SCHEMA_FILE = "card.contact.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_name(schema):
    """Tests a valid response with the name field."""
    instance = {"name": "John Doe"}
    jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {"name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_org(schema):
    """Tests a valid response with the org field."""
    instance = {"org": "Blues Wireless"}
    jsonschema.validate(instance=instance, schema=schema)

def test_org_invalid_type(schema):
    """Tests invalid type for org."""
    instance = {"org": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_valid_role(schema):
    """Tests a valid response with the role field."""
    instance = {"role": "Developer"}
    jsonschema.validate(instance=instance, schema=schema)

def test_role_invalid_type(schema):
    """Tests invalid type for role."""
    instance = {"role": ["Manager"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "['Manager'] is not of type 'string'" in str(excinfo.value)

def test_valid_email(schema):
    """Tests a valid response with the email field."""
    instance = {"email": "test@example.com"}
    jsonschema.validate(instance=instance, schema=schema)
    # No format validation in response schema, so any string is fine
    instance = {"email": "not-an-email"}
    jsonschema.validate(instance=instance, schema=schema)

def test_email_invalid_type(schema):
    """Tests invalid type for email."""
    instance = {"email": 12345}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "12345 is not of type 'string'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields populated."""
    instance = {
        "name": "Jane Doe",
        "org": "Example Inc.",
        "role": "Tester",
        "email": "jane.doe@example.org"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"name": "Test", "extra": True}
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
