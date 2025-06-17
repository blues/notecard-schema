import pytest
import jsonschema
import json
import base64

SCHEMA_FILE = "card.random.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_count_response(schema):
    """Tests valid response with count field."""
    instance = {"count": 86}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_payload_response(schema):
    """Tests valid response with payload field (base64 encoded)."""
    # Create valid base64 encoded data
    test_data = b"random_bytes_data"
    encoded_data = base64.b64encode(test_data).decode('ascii')
    instance = {"payload": encoded_data}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_both_count_and_payload(schema):
    """Tests valid response with both count and payload fields."""
    test_data = b"test"
    encoded_data = base64.b64encode(test_data).decode('ascii')
    instance = {"count": 42, "payload": encoded_data}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_type_validation(schema):
    """Tests that count must be an integer."""
    instance = {"count": "not_integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_count_negative_value(schema):
    """Tests that negative count values are allowed (schema doesn't restrict)."""
    instance = {"count": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_zero_value(schema):
    """Tests that zero count value is allowed."""
    instance = {"count": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_large_value(schema):
    """Tests large count values are accepted."""
    instance = {"count": 2147483647}  # Max 32-bit signed int
    jsonschema.validate(instance=instance, schema=schema)

def test_payload_string_validation(schema):
    """Tests that payload accepts string values."""
    instance = {"payload": "dGVzdA=="}  # base64 for "test"
    jsonschema.validate(instance=instance, schema=schema)

def test_payload_empty_string(schema):
    """Tests that payload accepts empty string."""
    instance = {"payload": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_payload_non_string_type(schema):
    """Tests that payload rejects non-string types."""
    instance = {"payload": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type" in str(excinfo.value)

def test_payload_valid_base64_patterns(schema):
    """Tests various valid base64 patterns."""
    valid_base64_examples = [
        "QQ==",  # "A"
        "QUI=",  # "AB"
        "QUJD",  # "ABC"
        "UXVpY2sgYnJvd24gZm94",  # "Quick brown fox"
        "SGVsbG8gV29ybGQ=",  # "Hello World"
    ]

    for b64_data in valid_base64_examples:
        instance = {"payload": b64_data}
        jsonschema.validate(instance=instance, schema=schema)

def test_multiple_additional_properties(schema):
    """Tests response with multiple additional properties."""
    instance = {
        "count": 50,
        "status": "success",
        "extra_field": "value",
        "another_field": 123
    }
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
