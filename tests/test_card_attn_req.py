import pytest
import json
import jsonschema
import os

SCHEMA_FILE = "card.attn.req.notecard.api.json"

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Get the absolute path to the schema file relative to the project root
schema_file_path = os.path.join(project_root, SCHEMA_FILE)

@pytest.fixture(scope='module')
def schema():
    """Loads the JSON schema."""
    # Check if the file exists before opening
    if not os.path.exists(schema_file_path):
        pytest.fail(f"Schema file not found at: {schema_file_path}")
    with open(schema_file_path, 'r') as f:
        schema_data = json.load(f)
    return schema_data

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {
        "req": "card.attn"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {
        "cmd": "card.attn"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_watchdog_valid(schema):
    """Tests valid request with mode=watchdog and required seconds >= 60."""
    instance = {
        "req": "card.attn",
        "mode": "watchdog",
        "seconds": 60
    }
    jsonschema.validate(instance=instance, schema=schema)

    instance = {
        "req": "card.attn",
        "mode": "watchdog,motion",
        "seconds": 120
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_watchdog_invalid_missing_seconds(schema):
    """Tests invalid request with mode=watchdog missing seconds."""
    instance = {
        "req": "card.attn",
        "mode": "watchdog"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'seconds' is a required property" in str(excinfo.value)

def test_mode_watchdog_invalid_seconds_too_low(schema):
    """Tests invalid request with mode=watchdog and seconds < 60."""
    instance = {
        "req": "card.attn",
        "mode": "watchdog",
        "seconds": 59
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "59 is less than the minimum of 60" in str(excinfo.value)

def test_mode_sleep_valid(schema):
    """Tests valid request with mode=sleep and required seconds >= 0."""
    instance = {
        "req": "card.attn",
        "mode": "sleep",
        "seconds": 0
    }
    jsonschema.validate(instance=instance, schema=schema)

    instance = {
        "req": "card.attn",
        "mode": "sleep,files",
        "seconds": 10,
        "files": ["data.qo"]
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_sleep_invalid_missing_seconds(schema):
    """Tests invalid request with mode=sleep missing seconds."""
    instance = {
        "req": "card.attn",
        "mode": "sleep"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'seconds' is a required property" in str(excinfo.value)

def test_mode_other_invalid_with_seconds(schema):
    """Tests invalid request with mode other than watchdog/sleep having seconds."""
    instance = {
        "req": "card.attn",
        "mode": "arm",
        "seconds": 30
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    error_string = str(excinfo.value)
    assert "should not be valid under" in error_string
    assert "'required': ['seconds']" in error_string

    instance = {
        "req": "card.attn",
        "seconds": 30
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    error_string = str(excinfo.value)
    assert "should not be valid under" in error_string
    assert "'required': ['seconds']" in error_string

def test_mode_files_valid(schema):
    """Tests valid request with mode including 'files' and the files field."""
    instance = {
        "req": "card.attn",
        "mode": "files",
        "files": ["data.qo", "_track.qi"]
    }
    jsonschema.validate(instance=instance, schema=schema)

    instance = {
        "req": "card.attn",
        "mode": "motion,files,sleep",
        "files": ["events.db"],
        "seconds": 10
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_files_invalid_missing_files(schema):
    """Tests invalid request with mode including 'files' but missing files field."""
    instance = {
        "req": "card.attn",
        "mode": "files"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'files' is a required property" in str(excinfo.value)

def test_mode_other_invalid_with_files(schema):
    """Tests invalid request with mode NOT including 'files' but providing files field."""
    instance = {
        "req": "card.attn",
        "mode": "motion",
        "files": ["data.qo"]
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # Check for the error related to the 'else'/'not' condition for 'files'
    error_string = str(excinfo.value)
    assert "should not be valid under" in error_string
    assert "'required': ['files']" in error_string

    instance = {
        "req": "card.attn",
        "files": ["data.qo"]
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    error_string = str(excinfo.value)
    assert "should not be valid under" in error_string
    assert "'required': ['files']" in error_string

def test_files_field_valid(schema):
    """Tests valid contents of the files field."""
    valid_files = [
        ["data.qo"],
        ["readings.qi"],
        ["log.db"],
        ["archive.dbs"],
        ["my-data.qo", "_track.qi", "status.db", "another.dbs"]
    ]
    for files_list in valid_files:
        instance = {
            "req": "card.attn",
            "mode": "files",
            "files": files_list
        }
        jsonschema.validate(instance=instance, schema=schema)

def test_files_field_invalid_type(schema):
    """Tests invalid type for the files field (must be array)."""
    instance = {
        "req": "card.attn",
        "mode": "files",
        "files": "data.qo" # Should be an array
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'data.qo' is not of type 'array'" in str(excinfo.value)

def test_files_field_invalid_item_type(schema):
    """Tests invalid item type within the files array (must be string)."""
    instance = {
        "req": "card.attn",
        "mode": "files",
        "files": ["data.qo", 123] # 123 is not a string
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_files_field_invalid_item_pattern(schema):
    """Tests invalid item pattern within the files array."""
    invalid_filenames = [
        ["data.txt"],
        ["image.jpg"],
        [".qo"],
        ["data.d"],
        ["data.qoi"],
        ["data.dbss"],
        ["data.qo", "invalid"],
    ]
    for filename in invalid_filenames:
        instance = {
            "req": "card.attn",
            "mode": "files",
            "files": filename
        }
        try:
            jsonschema.validate(instance=instance, schema=schema)
            pytest.fail(f"Schema unexpectedly validated invalid filename(s): {filename}")
        except jsonschema.ValidationError as excinfo:
            error_str = str(excinfo)
            assert "does not match" in error_str
            assert excinfo.instance in filename

def test_files_field_invalid_minitems(schema):
    """Tests invalid files array with zero items (minItems is 1)."""
    instance = {
        "req": "card.attn",
        "mode": "files",
        "files": []
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # Adjust assertion to match the current jsonschema error message
    assert "should be non-empty" in str(excinfo.value)

def test_on_field(schema):
    """Tests the 'on' field type validation."""
    # Valid
    instance = {"req": "card.attn", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.attn", "on": False}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"req": "card.attn", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo)

def test_off_field(schema):
    """Tests the 'off' field type validation."""
    # Valid
    instance = {"req": "card.attn", "off": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.attn", "off": False}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"req": "card.attn", "off": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo)

def test_payload_field(schema):
    """Tests the 'payload' field type validation."""
    # Valid (string type, format 'binary' is informational)
    # Note: Standard jsonschema doesn't validate content for 'binary' format.
    # We test with a base64 encoded string representation as an example.
    instance = {"req": "card.attn", "payload": "aGVsbG8="} # base64 for 'hello'
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"req": "card.attn", "payload": [1, 2, 3]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "[1, 2, 3] is not of type 'string'" in str(excinfo)

def test_start_field(schema):
    """Tests the 'start' field type validation."""
    # Valid
    instance = {"req": "card.attn", "start": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.attn", "start": False}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"req": "card.attn", "start": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo)

def test_verify_field(schema):
    """Tests the 'verify' field type validation."""
    # Valid
    instance = {"req": "card.attn", "verify": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.attn", "verify": False}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"req": "card.attn", "verify": "yes"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'yes' is not of type 'boolean'" in str(excinfo)

def test_all_optional_fields_valid(schema):
    """Tests a request with all optional fields set to valid values."""
    # Note: 'files' and 'seconds' require specific modes, excluded here.
    instance = {
        "req": "card.attn",
        "on": True,
        "off": False, # on and off aren't mutually exclusive per schema
        "payload": "",
        "start": True,
        "verify": True
    }
    jsonschema.validate(instance=instance, schema=schema)
