import pytest
import jsonschema
import json

SCHEMA_FILE = "card.wifi.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_with_secure(schema):
    """Tests a valid response with the secure field."""
    instance = {"secure": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"secure": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_secure_invalid_type(schema):
    """Tests invalid type for secure."""
    instance = {"secure": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_rsp_with_version(schema):
    """Tests a valid response with the version field."""
    instance = {"version": "3.12.3"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"version": "1.0.0"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"version": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_version_invalid_type(schema):
    """Tests invalid type for version."""
    instance = {"version": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_rsp_with_ssid(schema):
    """Tests a valid response with the ssid field."""
    instance = {"ssid": "MyHomeNetwork"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"ssid": "WiFi-Guest"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"ssid": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_ssid_invalid_type(schema):
    """Tests invalid type for ssid."""
    instance = {"ssid": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_rsp_with_security(schema):
    """Tests a valid response with the security field."""
    for value in ["open", "wep", "wpa2-wpa1", "wpa2-psk", ""]:
        instance = {"security": value}
        jsonschema.validate(instance=instance, schema=schema)

def test_security_invalid_type(schema):
    """Tests invalid type for security."""
    instance = {"security": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_rsp_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "secure": True,
        "version": "3.12.3",
        "ssid": "MyHomeNetwork",
        "security": "wpa2-psk"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_rsp_partial_fields(schema):
    """Tests valid responses with various field combinations."""
    instance = {"secure": True, "ssid": "MyNetwork"}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"version": "3.12.3", "security": "open"}
    jsonschema.validate(instance=instance, schema=schema)

    instance = {"secure": False, "version": "2.1.0", "ssid": "TestNetwork"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"secure": True, "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Unevaluated properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_security_sub_descriptions_exist(schema):
    """Tests that the security property has sub-descriptions."""
    security_prop = schema["properties"]["security"]
    assert "sub-descriptions" in security_prop, "security property is missing sub-descriptions"

def test_security_sub_descriptions_cover_supported_values(schema):
    """Tests that sub-descriptions document every security protocol Notecard supports."""
    security_prop = schema["properties"]["security"]
    sub_desc_values = {sd["const"] for sd in security_prop["sub-descriptions"]}
    expected = {"open", "wep", "wpa2-wpa1", "wpa2-psk"}
    assert sub_desc_values == expected, (
        f"Mismatch between documented security values and sub-description consts. "
        f"Missing sub-descriptions: {expected - sub_desc_values}. "
        f"Extra sub-descriptions: {sub_desc_values - expected}."
    )

def test_security_sub_descriptions_have_description(schema):
    """Tests that each sub-description entry has a non-empty description."""
    security_prop = schema["properties"]["security"]
    for sd in security_prop["sub-descriptions"]:
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
