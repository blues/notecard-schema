import pytest
import jsonschema
import json

SCHEMA_FILE = "card.transport.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.transport"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.transport"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"method": "wifi-cell"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.transport", "cmd": "card.transport"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

@pytest.mark.parametrize(
    "method",
    ["-", "cell", "cell-ntn", "dual-wifi-cell", "ntn", "wifi", "wifi-cell", "wifi-cell-ntn", "wifi-ntn"]
)
def test_valid_method_values(schema, method):
    """Tests valid method field values."""
    instance = {"req": "card.transport", "method": method}
    jsonschema.validate(instance=instance, schema=schema)

def test_method_invalid_value(schema):
    """Tests invalid value for method."""
    instance = {"req": "card.transport", "method": "invalid-method"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid-method' is not one of" in str(excinfo.value)

def test_method_invalid_type(schema):
    """Tests invalid type for method."""
    instance = {"req": "card.transport", "method": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"req": "card.transport", "method": "wifi-cell", "seconds": 1800}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.transport", "method": "wifi-cell", "seconds": -1}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.transport", "method": "wifi-cell", "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "card.transport", "method": "wifi-cell", "seconds": "1800"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1800' is not of type 'integer'" in str(excinfo.value)

def test_seconds_below_minimum(schema):
    """Tests seconds value below minimum."""
    instance = {"req": "card.transport", "method": "wifi-cell", "seconds": -2}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-2 is less than the minimum of -1" in str(excinfo.value)

def test_valid_allow_field(schema):
    """Tests valid allow field."""
    instance = {"req": "card.transport", "method": "ntn", "allow": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.transport", "method": "ntn", "allow": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_allow_invalid_type(schema):
    """Tests invalid type for allow."""
    instance = {"req": "card.transport", "method": "ntn", "allow": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_valid_umin_field(schema):
    """Tests valid umin field."""
    instance = {"req": "card.transport", "method": "wifi", "umin": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"req": "card.transport", "method": "wifi", "umin": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_umin_invalid_type(schema):
    """Tests invalid type for umin."""
    instance = {"req": "card.transport", "method": "wifi", "umin": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_req_invalid_value(schema):
    """Tests invalid req value."""
    instance = {"req": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.transport' was expected" in str(excinfo.value)

def test_cmd_invalid_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "invalid.command"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'card.transport' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with an additional property."""
    instance = {"req": "card.transport", "method": "wifi-cell", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_complete_request(schema):
    """Tests valid complete request with all fields."""
    instance = {
        "req": "card.transport",
        "method": "wifi-cell-ntn",
        "seconds": 1800,
        "allow": True,
        "umin": False
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_ntn_configuration(schema):
    """Tests valid NTN configuration request."""
    instance = {
        "req": "card.transport",
        "method": "ntn",
        "allow": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_reset_to_default(schema):
    """Tests valid reset to default configuration."""
    instance = {"cmd": "card.transport", "method": "-"}
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