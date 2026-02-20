import pytest
import jsonschema
import json

SCHEMA_FILE = "card.carrier.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.carrier"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.carrier"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "charging"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.carrier", "cmd": "card.carrier"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid value for req."""
    instance = {"req": "invalid.req"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_cmd_value(schema):
    """Tests invalid value for cmd."""
    instance = {"cmd": "invalid.cmd"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_charging(schema):
    """Tests valid mode 'charging'."""
    instance = {"req": "card.carrier", "mode": "charging"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_hyphen(schema):
    """Tests valid mode '-'."""
    instance = {"req": "card.carrier", "mode": "-"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_off(schema):
    """Tests valid mode 'off'."""
    instance = {"req": "card.carrier", "mode": "off"}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.carrier", "mode": "invalid_mode"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid_mode' is not one of ['charging', '-', 'off']" in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.carrier", "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.carrier", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_mode_sub_descriptions_exist(schema):
    """Tests that the mode property has sub-descriptions."""
    mode_prop = schema["properties"]["mode"]
    assert "sub-descriptions" in mode_prop, "mode property is missing sub-descriptions"

def test_mode_sub_descriptions_match_enum(schema):
    """Tests that every enum value has a corresponding sub-description and vice versa."""
    mode_prop = schema["properties"]["mode"]
    enum_values = set(mode_prop["enum"])
    sub_desc_values = {sd["const"] for sd in mode_prop["sub-descriptions"]}
    assert enum_values == sub_desc_values, (
        f"Mismatch between enum values and sub-description consts. "
        f"Missing sub-descriptions: {enum_values - sub_desc_values}. "
        f"Extra sub-descriptions: {sub_desc_values - enum_values}."
    )

def test_mode_sub_descriptions_have_description(schema):
    """Tests that each sub-description entry has a non-empty description."""
    mode_prop = schema["properties"]["mode"]
    for sd in mode_prop["sub-descriptions"]:
        assert "description" in sd, f"Sub-description for '{sd['const']}' is missing 'description'"
        assert len(sd["description"]) > 0, f"Sub-description for '{sd['const']}' has empty description"

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
