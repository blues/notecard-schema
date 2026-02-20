import pytest
import jsonschema
import json

SCHEMA_FILE = "card.contact.rsp.notecard.api.json"

REQUIRED_FIELDS = {
    "name": "John Doe",
    "org": "Blues Wireless",
    "role": "Developer",
    "email": "john@blues.com"
}

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only the required fields."""
    instance = {
        "name": "John Doe",
        "org": "Blues Wireless",
        "role": "Developer",
        "email": "john@blues.com"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_name(schema):
    """Tests that 'name' is a required property."""
    instance = {"org": "Blues", "role": "Developer", "email": "test@blues.com"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'name' is a required property" in str(excinfo.value)

def test_missing_required_org(schema):
    """Tests that 'org' is a required property."""
    instance = {"name": "John Doe", "role": "Developer", "email": "test@blues.com"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'org' is a required property" in str(excinfo.value)

def test_missing_required_role(schema):
    """Tests that 'role' is a required property."""
    instance = {"name": "John Doe", "org": "Blues", "email": "test@blues.com"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'role' is a required property" in str(excinfo.value)

def test_missing_required_email(schema):
    """Tests that 'email' is a required property."""
    instance = {"name": "John Doe", "org": "Blues", "role": "Developer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'email' is a required property" in str(excinfo.value)

def test_valid_name(schema):
    """Tests a valid response with the name field."""
    instance = {**REQUIRED_FIELDS, "name": "Jane Smith"}
    jsonschema.validate(instance=instance, schema=schema)

def test_name_invalid_type(schema):
    """Tests invalid type for name."""
    instance = {**REQUIRED_FIELDS, "name": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_org(schema):
    """Tests a valid response with the org field."""
    instance = {**REQUIRED_FIELDS, "org": "Example Inc."}
    jsonschema.validate(instance=instance, schema=schema)

def test_org_invalid_type(schema):
    """Tests invalid type for org."""
    instance = {**REQUIRED_FIELDS, "org": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_valid_role(schema):
    """Tests a valid response with the role field."""
    instance = {**REQUIRED_FIELDS, "role": "Manager"}
    jsonschema.validate(instance=instance, schema=schema)

def test_role_invalid_type(schema):
    """Tests invalid type for role."""
    instance = {**REQUIRED_FIELDS, "role": ["Manager"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "['Manager'] is not of type 'string'" in str(excinfo.value)

def test_valid_email(schema):
    """Tests a valid response with the email field."""
    instance = {**REQUIRED_FIELDS, "email": "test@example.com"}
    jsonschema.validate(instance=instance, schema=schema)
    # No format validation in response schema, so any string is fine
    instance = {**REQUIRED_FIELDS, "email": "not-an-email"}
    jsonschema.validate(instance=instance, schema=schema)

def test_email_invalid_type(schema):
    """Tests invalid type for email."""
    instance = {**REQUIRED_FIELDS, "email": 12345}
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
    instance = {**REQUIRED_FIELDS, "extra": True}
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
