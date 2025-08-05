import pytest
import jsonschema
import json

SCHEMA_FILE = "card.aux.rsp.notecard.api.json"

def test_minimal_valid_response(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_valid(schema):
    """Tests a valid response with a string mode."""
    instance = {"mode": "gpio"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": "off"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"mode": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_type(schema):
    """Tests an invalid response with a non-string mode."""
    instance = {"mode": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_state_valid(schema):
    """Tests valid state array values."""
    # Empty state array
    instance = {"state": []}
    jsonschema.validate(instance=instance, schema=schema)

    # State with empty objects (pins off)
    instance = {"state": [{}, {}, {}, {}]}
    jsonschema.validate(instance=instance, schema=schema)

    # State with high/low pins
    instance = {"state": [{"high": True}, {"low": True}, {}, {}]}
    jsonschema.validate(instance=instance, schema=schema)

    # State with input pin
    instance = {"state": [{}, {}, {"input": True}, {}]}
    jsonschema.validate(instance=instance, schema=schema)

    # State with count pin
    instance = {"state": [{}, {}, {}, {"count": [3, 5, 2]}]}
    jsonschema.validate(instance=instance, schema=schema)

def test_state_invalid_type(schema):
    """Tests invalid type for state (must be array)."""
    instance = {"state": "gpio"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'gpio' is not of type 'array'" in str(excinfo.value)

def test_state_invalid_item_type(schema):
    """Tests invalid item type within state array (must be object)."""
    instance = {"state": ["high", "low"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_state_invalid_item_property_type(schema):
    """Tests invalid property type within state array items."""
    instance = {"state": [{"high": "true"}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_state_invalid_count_type(schema):
    """Tests invalid count property type within state array items."""
    instance = {"state": [{"count": "3"}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3' is not of type 'array'" in str(excinfo.value)

def test_state_invalid_count_item_type(schema):
    """Tests invalid count array item type."""
    instance = {"state": [{"count": [3, "5"]}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_state_additional_properties_not_allowed(schema):
    """Tests that additional properties are not allowed in state items."""
    instance = {"state": [{"invalid_prop": True}]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_time_valid(schema):
    """Tests valid time values (UNIX Epoch time)."""
    instance = {"time": 1592587637}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"time": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {"time": "1592587637"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1592587637' is not of type 'integer'" in str(excinfo.value)

def test_seconds_valid(schema):
    """Tests valid seconds values."""
    instance = {"seconds": 2}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"seconds": 2.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "2.5 is not of type 'integer'" in str(excinfo.value)

def test_power_valid(schema):
    """Tests valid power values (boolean)."""
    instance = {"power": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"power": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_power_invalid_type(schema):
    """Tests invalid type for power."""
    instance = {"power": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_gpio_response(schema):
    """Tests a complete valid GPIO mode response."""
    instance = {
        "mode": "gpio",
        "state": [
            {},  # AUX1 off
            {"low": True},  # AUX2 low
            {"high": True},  # AUX3 high
            {"count": [3]}  # AUX4 count
        ],
        "time": 1592587637,
        "seconds": 2
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_simple_response(schema):
    """Tests a simple valid response with just mode."""
    instance = {"mode": "track"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_power(schema):
    """Tests a valid response with power indicator."""
    instance = {
        "mode": "gpio",
        "power": True
    }
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
