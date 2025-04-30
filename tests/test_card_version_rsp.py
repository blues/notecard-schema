import pytest
import jsonschema

SCHEMA_FILE = "card.version.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only the required field."""
    instance = {"version": "notecard firmware v1.2.3"}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_field(schema):
    """Tests invalid response missing the required 'version' field."""
    instance = {"api": 1} # Missing 'version'
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'version' is a required property" in str(excinfo.value)

def test_version_invalid_type(schema):
    """Tests invalid type for the required 'version' field."""
    instance = {"version": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_api(schema):
    """Tests valid api field."""
    instance = {"version": "v1", "api": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_api_invalid_type(schema):
    """Tests invalid type for api."""
    instance = {"version": "v1", "api": "1"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1' is not of type 'integer'" in str(excinfo.value)

def test_valid_board(schema):
    """Tests valid board field."""
    instance = {"version": "v1", "board": "WBNA"}
    jsonschema.validate(instance=instance, schema=schema)

def test_board_invalid_type(schema):
    """Tests invalid type for board."""
    instance = {"version": "v1", "board": 1.0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1.0 is not of type 'string'" in str(excinfo.value)

def test_valid_body_empty(schema):
    """Tests valid empty body object."""
    instance = {"version": "v1", "body": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_body_invalid_type(schema):
    """Tests invalid type for body."""
    instance = {"version": "v1", "body": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not of type 'object'" in str(excinfo.value)

# Parametrized tests for body sub-properties
@pytest.mark.parametrize(
    "sub_field, valid_value, invalid_value, expected_type",
    [
        ("org", "Blues", 123, "string"),
        ("product", "Notecard", True, "string"),
        ("version", "1.2.3", 123, "string"),
        ("ver_major", 1, "1", "integer"),
        ("ver_minor", 2, "2", "integer"),
        ("ver_patch", 3, "3", "integer"),
        ("ver_build", 1234, "1234", "integer"),
        ("built", "2023-01-01T12:00:00Z", 123456, "string") # String type check only
    ]
)
def test_body_sub_properties(schema, sub_field, valid_value, invalid_value, expected_type):
    """Tests valid and invalid types for body sub-properties."""
    # Valid type
    instance = {"version": "v1", "body": {sub_field: valid_value}}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"version": "v1", "body": {sub_field: invalid_value}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert f"is not of type \'{expected_type}\'" in str(excinfo.value)

# Separate test for built format if needed, likely skipped
# def test_body_built_invalid_format(schema):
#     instance = {"version": "v1", "body": {"built": "not-a-date-time"}}
#     with pytest.raises(jsonschema.ValidationError) as excinfo:
#         jsonschema.validate(instance=instance, schema=schema)
#     assert "is not a 'date-time'" in str(excinfo.value)

def test_valid_body_all_fields(schema):
    """Tests valid body object with all sub-properties."""
    instance = {
        "version": "v1",
        "body": {
            "org": "Blues Wireless",
            "product": "Notecard-WBNA",
            "version": "firmware-v2.1.1-1234",
            "ver_major": 2,
            "ver_minor": 1,
            "ver_patch": 1,
            "ver_build": 1234,
            "built": "2024-01-15T10:30:00Z"
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

@pytest.mark.parametrize(
    "field_name, valid_value, invalid_value, expected_type",
    [
        ("cell", True, "true", "boolean"),
        ("device", "dev:123456789012345", 123, "string"),
        ("gps", False, "false", "boolean"),
        ("name", "Notecard Cell+WiFi", 1, "string"),
        ("sku", "NOTE-WBNA-500", True, "string"),
        ("wifi", True, 0, "boolean")
    ]
)
def test_optional_fields(schema, field_name, valid_value, invalid_value, expected_type):
    """Tests valid and invalid types for various optional fields."""
    # Valid type
    instance = {"version": "v1", field_name: valid_value}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"version": "v1", field_name: invalid_value}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert f"is not of type \'{expected_type}\'" in str(excinfo.value)

def test_device_invalid_pattern(schema):
    """Tests invalid pattern for device field."""
    instance = {"version": "v1", "device": "invalid-pattern"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "does not match '^dev:[0-9]{15}$'" in str(excinfo.value)

def test_valid_all_fields_outer(schema):
    """Tests a valid response with all top-level fields populated."""
    instance = {
        "version": "firmware-v2.1.1-1234",
        "api": 2,
        "board": "WBNA-1",
        "body": { # Minimal body for this test
            "version": "firmware-v2.1.1-1234"
        },
        "cell": True,
        "device": "dev:987654321012345",
        "gps": False,
        "name": "My Notecard",
        "sku": "NOTE-WBNA-500",
        "wifi": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"version": "v1", "extra": "data"}
    jsonschema.validate(instance=instance, schema=schema)
