import pytest
import jsonschema

SCHEMA_FILE = "card.version.rsp.notecard.api.json"


def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only the required field."""
    instance = {"version": "notecard firmware v1.2.3"}
    jsonschema.validate(instance=instance, schema=schema)


def test_missing_required_field(schema):
    """Tests invalid response missing the required 'version' field."""
    instance = {"sku": "NOTE-NBGL"}  # Missing 'version'
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'version' is a required property" in str(excinfo.value)


def test_version_invalid_type(schema):
    """Tests invalid type for the required 'version' field."""
    instance = {"version": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)


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
        ("target", "r5", 123, "string"),
        ("version", "1.2.3", 123, "string"),
        ("ver_major", 1, "1", "integer"),
        ("ver_minor", 2, "2", "integer"),
        ("ver_patch", 3, "3", "integer"),
        ("ver_build", 1234, "1234", "integer"),
        ("built", "Sep  5 2023 12:21:30", 123456, "string"),  # String type check only
    ],
)
def test_body_sub_properties(
    schema, sub_field, valid_value, invalid_value, expected_type
):
    """Tests valid and invalid types for body sub-properties."""
    # Valid type
    instance = {"version": "v1", "body": {sub_field: valid_value}}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"version": "v1", "body": {sub_field: invalid_value}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert f"is not of type '{expected_type}'" in str(excinfo.value)


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
            "product": "Notecard",
            "target": "r5",
            "version": "notecard-5.3.1",
            "ver_major": 5,
            "ver_minor": 3,
            "ver_patch": 1,
            "ver_build": 371,
            "built": "Sep  5 2023 12:21:30",
        },
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
        ("wifi", True, 0, "boolean"),
    ],
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
    assert f"is not of type '{expected_type}'" in str(excinfo.value)


def test_device_valid_pattern(schema):
    """Tests valid device field patterns."""
    # Test typical DeviceUID format
    instance = {"version": "v1", "device": "dev:123456789012345"}
    jsonschema.validate(instance=instance, schema=schema)

    # Test other valid device formats
    instance = {"version": "v1", "device": "dev:000000000000000"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_all_fields_outer(schema):
    """Tests a valid response with all top-level fields populated."""
    instance = {
        "version": "firmware-v2.1.1-1234",
        "board": "WBNA-1",
        "body": {"version": "firmware-v2.1.1-1234"},  # Minimal body for this test
        "cell": True,
        "device": "dev:987654321012345",
        "gps": False,
        "name": "My Notecard",
        "sku": "NOTE-WBNA-500",
        "wifi": True,
    }
    jsonschema.validate(instance=instance, schema=schema)


def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"version": "v1", "extra": "data"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(
        excinfo.value
    )


def test_body_invalid_additional_property(schema):
    """Tests invalid body object with additional property."""
    instance = {"version": "v1", "body": {"org": "Blues", "invalid_field": "test"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert (
        "Additional properties are not allowed ('invalid_field' was unexpected)"
        in str(excinfo.value)
    )


def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    import json

    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(
                f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}"
            )
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
