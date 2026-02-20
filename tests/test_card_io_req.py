import pytest
import jsonschema
import json

SCHEMA_FILE = "card.io.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.io"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.io"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"i2c": 0x18}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.io", "cmd": "card.io"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_valid_i2c(schema):
    """Tests valid i2c field values."""
    instance = {"req": "card.io", "i2c": 0x18} # Set alternate address
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.io", "i2c": -1} # Reset to default
    jsonschema.validate(instance=instance, schema=schema)

def test_i2c_invalid_type(schema):
    """Tests invalid type for i2c."""
    instance = {"req": "card.io", "i2c": "0x18"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'0x18' is not of type 'integer'" in str(excinfo.value)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = [
        "-usb", "usb", "+usb", "+busy", "-busy",
        "i2c-master-disable", "i2c-master-enable",
        "+fallback", "-fallback"
    ]
    for mode in valid_modes:
        instance = {"req": "card.io", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.io", "mode": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['-" in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.io", "mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid request with all optional fields."""
    instance = {"req": "card.io", "i2c": 0x19, "mode": "+usb"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.io", "extra": "property"}
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
