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

def test_valid_net_empty_array(schema):
    """Tests valid net field with an empty array."""
    instance = {"net": []}
    jsonschema.validate(instance=instance, schema=schema)

def test_net_invalid_type(schema):
    """Tests invalid type for net (must be array)."""
    instance = {"net": {}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "{} is not of type 'array'" in str(excinfo.value)

def test_net_invalid_item_type(schema):
    """Tests invalid item type within net array (must be object)."""
    instance = {"net": ["invalid"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not of type 'object'" in str(excinfo.value)

def test_valid_net_item_empty_object(schema):
    """Tests valid net array with an empty object item."""
    instance = {"net": [{}]}
    jsonschema.validate(instance=instance, schema=schema)

# Parametrized tests for net item sub-properties (string)
@pytest.mark.parametrize(
    "sub_field, valid_value, invalid_value",
    [
        ("rat", "lte", 123),
        ("band", "20", True)
    ]
)
def test_net_item_string_sub_properties(schema, sub_field, valid_value, invalid_value):
    """Tests valid and invalid types for net item string sub-properties."""
    # Valid type
    instance = {"net": [{sub_field: valid_value}]}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"net": [{sub_field: invalid_value}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert f"is not of type 'string'" in str(excinfo.value)

# Parametrized tests for net item sub-properties (integer)
@pytest.mark.parametrize(
    "sub_field, valid_value, invalid_value",
    [
        ("rssi", -90, "-90"),
        ("mcc", 310, 310.5),
        ("mnc", 410, True),
        ("lac", 12345, "12345"),
        ("cid", 54321, 54321.5)
    ]
)
def test_net_item_integer_sub_properties(schema, sub_field, valid_value, invalid_value):
    """Tests valid and invalid types for net item integer sub-properties."""
    # Valid type
    instance = {"net": [{sub_field: valid_value}]}
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {"net": [{sub_field: invalid_value}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert f"is not of type 'integer'" in str(excinfo.value)

def test_valid_net_item_all_fields(schema):
    """Tests valid net array with item having all sub-properties."""
    instance = {"net": [{
        "rat": "nbiot",
        "band": "8",
        "rssi": -105,
        "mcc": 234,
        "mnc": 15,
        "lac": 5432,
        "cid": 98765
    }]}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_top_level_fields(schema):
    """Tests valid response with all top-level fields."""
    instance = {
        "status": "connected",
        "count": 1,
        "net": [{
            "rat": "lte",
            "rssi": -85
        }]
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"status": "ok", "imei": "123456789012345"}
    jsonschema.validate(instance=instance, schema=schema)
