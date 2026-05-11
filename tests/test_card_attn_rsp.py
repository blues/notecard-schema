import json
import pytest
import jsonschema

SCHEMA_FILE = "card.attn.rsp.notecard.api.json"

def test_minimal_valid_response(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_set_true(schema):
    """Tests a valid response with set=true."""
    instance = {"set": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_set_false(schema):
    """Tests a valid response with set=false."""
    instance = {"set": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_set_type(schema):
    """Tests an invalid response with a non-boolean type for set."""
    instance = {"set": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_files_single_item(schema):
    """Tests a valid response with a single item in the files array."""
    instance = {"files": ["event1.qo"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_multiple_items(schema):
    """Tests a valid response with multiple items in the files array."""
    instance = {"files": ["event1.qo", "_config.db"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_files_type(schema):
    """Tests an invalid response where files is not an array."""
    instance = {"files": "event1.qo"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'event1.qo' is not of type 'array'" in str(excinfo.value)

def test_invalid_files_item_type(schema):
    """Tests an invalid response with a non-string item in the files array."""
    instance = {"files": ["event1.qo", 123]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_invalid_files_empty_array(schema):
    """Tests an invalid response with an empty files array (minItems is 1)."""
    instance = {"files": []}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "should be non-empty" in str(excinfo.value) # Matches newer jsonschema message

def test_valid_payload(schema):
    """Tests a valid response with a string payload."""
    # Using a base64 encoded string as an example, format: binary is informational
    instance = {"payload": "aGVsbG8="}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_payload_type(schema):
    """Tests an invalid response with a non-string payload."""
    instance = {"payload": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_time(schema):
    """Tests a valid response with a non-negative integer time."""
    instance = {"time": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_time_type(schema):
    """Tests an invalid response with a non-integer time."""
    instance = {"time": 1678886400.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1678886400.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_off_true(schema):
    """Tests a valid response with off=true."""
    instance = {"off": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_off_false(schema):
    """Tests a valid response with off=false."""
    instance = {"off": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_off_type(schema):
    """Tests an invalid response with a non-boolean type for off."""
    instance = {"off": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_valid_multiple_fields(schema):
    """Tests a valid response containing multiple optional fields."""
    instance = {
        "set": True,
        "files": ["data.qo"],
        "payload": "aGVsbG8=",
        "time": 1234567890,
        "off": False
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_keyword_auxgpio(schema):
    """Tests that auxgpio is a valid keyword in the files array."""
    instance = {"files": ["auxgpio"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_keyword_journey(schema):
    """Tests that journey is a valid keyword in the files array."""
    instance = {"files": ["journey"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_keyword_modified(schema):
    """Tests that modified is a valid keyword in the files array."""
    instance = {"files": ["data.qi", "modified"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_keyword_motionchange(schema):
    """Tests that motionchange is a valid keyword in the files array."""
    instance = {"files": ["motionchange"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_keyword_signal(schema):
    """Tests that signal is a valid keyword in the files array."""
    instance = {"files": ["signal"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_keyword_usb(schema):
    """Tests that usb is a valid keyword in the files array."""
    instance = {"files": ["usb"]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_files_keyword_wireless(schema):
    """Tests that wireless is a valid keyword in the files array."""
    instance = {"files": ["wireless"]}
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
