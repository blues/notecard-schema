import pytest
import jsonschema

SCHEMA_FILE = "card.aux.rsp.notecard.api.json"

def test_minimal_valid_response(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_valid(schema):
    """Tests a valid response with a string mode."""
    instance = {"mode": "gpio"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests an invalid response with a non-string mode."""
    instance = {"mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_text_valid(schema):
    """Tests a valid response with a string text."""
    instance = {"text": "Received data"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"text": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_text_invalid_type(schema):
    """Tests an invalid response with a non-string text."""
    instance = {"text": ["data"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "['data'] is not of type 'string'" in str(excinfo.value)

def test_binary_valid(schema):
    """Tests a valid response with a string binary payload."""
    instance = {"binary": "aGVsbG8="}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"binary": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_binary_invalid_type(schema):
    """Tests an invalid response with a non-string binary payload."""
    instance = {"binary": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_count_valid(schema):
    """Tests valid count values (integer >= 0)."""
    instance = {"count": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"count": 1024}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"count": 10.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "10.5 is not of type 'integer'" in str(excinfo.value)

def test_count_invalid_minimum(schema):
    """Tests invalid count value (< 0)."""
    instance = {"count": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_valid_multiple_fields(schema):
    """Tests a valid response containing multiple optional fields."""
    instance = {
        "mode": "track",
        "text": "Tracking active",
        "binary": "",
        "count": 0
    }
    jsonschema.validate(instance=instance, schema=schema)

    instance = {
        "mode": "serial",
        "text": "Some text received",
        "binary": "YmluYXJ5IGRhdGE=",
        "count": 12
    }
    jsonschema.validate(instance=instance, schema=schema)
