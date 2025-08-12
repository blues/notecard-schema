import pytest
import jsonschema

SCHEMA_FILE = "card.wireless.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"status": "{modem-status}"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_count(schema):
    """Tests valid count field."""
    instance = {"count": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"count": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"count": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_net_empty_object(schema):
    """Tests valid net field with an empty object."""
    instance = {"net": {}}
    jsonschema.validate(instance=instance, schema=schema)

def test_net_invalid_type(schema):
    """Tests invalid type for net (must be object)."""
    instance = {"net": []}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "[] is not of type 'object'" in str(excinfo.value)

# Parametrized tests for net object sub-properties (string)
@pytest.mark.parametrize(
    "sub_field, valid_value, invalid_value",
    [
        ("iccid", "00000000000000000000", 123),
        ("imsi", "000000000000000", True),
        ("imei", "000000000000000", 123),
        ("modem", "EG91NAXGAR07A03M1G", 123),
        ("band", "LTE BAND 2", 123),
        ("rat", "lte", 123)
    ]
)
def test_net_string_sub_properties(schema, sub_field, valid_value, invalid_value):
    """Tests valid and invalid types for net object string sub-properties."""
    # Valid type
    instance = {"net": {sub_field: valid_value}}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"net": {sub_field: invalid_value}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert f"is not of type 'string'" in str(excinfo.value)

# Parametrized tests for net object sub-properties (integer)
@pytest.mark.parametrize(
    "sub_field, valid_value, invalid_value",
    [
        ("rssir", -69, "-69"),
        ("rssi", -70, "-70"),
        ("rsrp", -105, "-105"),
        ("sinr", -3, "-3"),
        ("rsrq", -17, "-17"),
        ("bars", 1, "1"),
        ("mcc", 310, 310.5),
        ("mnc", 410, True),
        ("lac", 28681, "28681"),
        ("cid", 211150856, "211150856"),
        ("updated", 1599225076, "1599225076")
    ]
)
def test_net_integer_sub_properties(schema, sub_field, valid_value, invalid_value):
    """Tests valid and invalid types for net object integer sub-properties."""
    # Valid type
    instance = {"net": {sub_field: valid_value}}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"net": {sub_field: invalid_value}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert f"is not of type 'integer'" in str(excinfo.value)

def test_valid_net_object_all_fields(schema):
    """Tests valid net object with all sub-properties."""
    instance = {"net": {
        "iccid": "00000000000000000000",
        "imsi": "000000000000000",
        "imei": "000000000000000",
        "modem": "EG91NAXGAR07A03M1G_BETA0415_01.001.01.001",
        "band": "LTE BAND 2",
        "rat": "lte",
        "rssir": -69,
        "rssi": -70,
        "rsrp": -105,
        "sinr": -3,
        "rsrq": -17,
        "bars": 1,
        "mcc": 310,
        "mnc": 410,
        "lac": 28681,
        "cid": 211150856,
        "updated": 1599225076
    }}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_top_level_fields(schema):
    """Tests valid response with all top-level fields."""
    instance = {
        "status": "connected",
        "count": 1,
        "net": {
            "rat": "lte",
            "rssi": -85
        }
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"status": "ok", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_net_invalid_additional_property(schema):
    """Tests invalid net object with an additional property."""
    instance = {"net": {"rssi": -70, "extra": "field"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    import json
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}")
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
