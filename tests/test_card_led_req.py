import pytest
import jsonschema

SCHEMA_FILE = "card.led.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.led"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.led"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "red"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.led", "cmd": "card.led"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = [
        "red", "green", "yellow", "blue", "cyan", "magenta",
        "orange", "white", "gray"
    ]
    for mode in valid_modes:
        instance = {"req": "card.led", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.led", "mode": "purple"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'purple' is not one of ['red'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.led", "mode": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_on(schema):
    """Tests valid on field values."""
    instance = {"req": "card.led", "on": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.led", "on": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_on_invalid_type(schema):
    """Tests invalid type for on."""
    instance = {"req": "card.led", "on": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_off(schema):
    """Tests valid off field values."""
    instance = {"req": "card.led", "off": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.led", "off": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_off_invalid_type(schema):
    """Tests invalid type for off."""
    instance = {"req": "card.led", "off": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_mode_and_on(schema):
    """Tests valid request with mode and on."""
    instance = {"req": "card.led", "mode": "blue", "on": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_and_off(schema):
    """Tests valid request with mode and off."""
    instance = {"req": "card.led", "mode": "green", "off": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid request with all optional fields."""
    instance = {"req": "card.led", "mode": "white", "on": True, "off": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.led", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_schema_samples(schema):
    """Tests that all schema samples validate against the schema."""
    import json

    def parse_json_sample(json_string):
        """Parse JSON sample that can be a single object, array of objects, or comma-separated objects."""
        json_objects = []

        try:
            # First try to parse as valid JSON
            parsed = json.loads(json_string)

            if isinstance(parsed, list):
                # It's a JSON array - return the objects in the array
                json_objects = [obj for obj in parsed if isinstance(obj, dict)]
            elif isinstance(parsed, dict):
                # It's a single JSON object
                json_objects = [parsed]
        except json.JSONDecodeError:
            # Fallback: try to parse as comma-separated JSON objects (legacy format)
            parts = json_string.split("},{")

            if len(parts) > 1:
                # Multiple JSON objects (legacy comma-separated format)
                for i, part in enumerate(parts):
                    # Add back the closing brace for all but the last part
                    if i < len(parts) - 1:
                        part = part + "}"
                    # Add back the opening brace for all but the first part
                    if i > 0:
                        part = "{" + part

                    try:
                        parsed = json.loads(part)
                        json_objects.append(parsed)
                    except json.JSONDecodeError:
                        continue

        return json_objects

    samples = schema.get("samples", [])
    for sample in samples:
        json_objects = parse_json_sample(sample["json"])

        # Only validate JSON objects that match this schema (card.led)
        for json_obj in json_objects:
            req_val = json_obj.get("req") or json_obj.get("cmd")
            if req_val == "card.led":
                jsonschema.validate(instance=json_obj, schema=schema)
