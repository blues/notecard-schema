import pytest
import jsonschema
import json

SCHEMA_FILE = "card.transport.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with only required fields."""
    instance = {"method": "cell"}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_method(schema):
    """Tests that method is required."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'method' is a required property" in str(excinfo.value)

@pytest.mark.parametrize(
    "method",
    ["-", "cell", "cell-ntn", "dual-wifi-cell", "ntn", "wifi", "wifi-cell", "wifi-cell-ntn", "wifi-ntn"]
)
def test_valid_method_values(schema, method):
    """Tests valid method field values in response."""
    instance = {"method": method}
    jsonschema.validate(instance=instance, schema=schema)

def test_method_invalid_value(schema):
    """Tests invalid value for method in response."""
    instance = {"method": "invalid-method"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid-method' is not one of" in str(excinfo.value)

def test_method_invalid_type(schema):
    """Tests invalid type for method."""
    instance = {"method": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_wifi_cell_response(schema):
    """Tests valid WiFi-cell response."""
    instance = {"method": "wifi-cell"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cellular_only_response(schema):
    """Tests valid cellular only response."""
    instance = {"method": "cell"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_wifi_only_response(schema):
    """Tests valid WiFi only response."""
    instance = {"method": "wifi"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_ntn_response(schema):
    """Tests valid NTN response."""
    instance = {"method": "ntn"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_reset_response(schema):
    """Tests valid reset to default response."""
    instance = {"method": "-"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_wifi_cell_ntn_response(schema):
    """Tests valid triple fallback response."""
    instance = {"method": "wifi-cell-ntn"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_deprecated_method(schema):
    """Tests valid deprecated dual-wifi-cell method."""
    instance = {"method": "dual-wifi-cell"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"method": "wifi-cell", "status": "active"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('status' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        "method": "wifi-cell",
        "status": "active",
        "timeout": 3600,
        "extra": "field"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_boolean_property(schema):
    """Tests invalid response with boolean property."""
    instance = {"method": "ntn", "enabled": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('enabled' was unexpected)" in str(excinfo.value)

def test_invalid_number_property(schema):
    """Tests invalid response with number property."""
    instance = {"method": "wifi-cell", "timeout": 3600}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('timeout' was unexpected)" in str(excinfo.value)

def test_method_sub_descriptions_exist(schema):
    """Tests that the method property has sub-descriptions."""
    method_prop = schema["properties"]["method"]
    assert "sub-descriptions" in method_prop, "method property is missing sub-descriptions"

def test_method_sub_descriptions_match_enum(schema):
    """Tests that every enum value has a corresponding sub-description and vice versa."""
    method_prop = schema["properties"]["method"]
    enum_values = set(method_prop["enum"])
    sub_desc_values = {sd["const"] for sd in method_prop["sub-descriptions"]}
    assert enum_values == sub_desc_values, (
        f"Mismatch between enum values and sub-description consts. "
        f"Missing sub-descriptions: {enum_values - sub_desc_values}. "
        f"Extra sub-descriptions: {sub_desc_values - enum_values}."
    )

def test_method_sub_descriptions_have_description(schema):
    """Tests that each sub-description entry has a non-empty description."""
    method_prop = schema["properties"]["method"]
    for sd in method_prop["sub-descriptions"]:
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
