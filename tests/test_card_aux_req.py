import pytest
import jsonschema

SCHEMA_FILE = "card.aux.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {"req": "card.aux"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {"cmd": "card.aux"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request missing req/cmd."""
    instance = {"mode": "gpio"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.aux", "cmd": "card.aux"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_valid(schema):
    """Tests valid mode enum values."""
    valid_modes = [
        "dfu", "gpio", "led", "monitor", "motion", "neo",
        "neo-monitor", "off", "track", "track-monitor",
        "track-neo-monitor", "-"
    ]
    for mode in valid_modes:
        instance = {"req": "card.aux", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"req": "card.aux", "mode": "invalid_mode"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid_mode' is not one of ['dfu'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"req": "card.aux", "mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_usage_valid(schema):
    """Tests valid usage array and items."""
    valid_usages = [
        [""], ["off"], ["high"], ["low"], ["input"], ["input-pulldown"],
        ["input-pullup"], ["count"], ["count-pulldown"], ["count-pullup"],
        ["high", "low", "input", "off"] # Mix of valid items
    ]
    for usage_list in valid_usages:
        instance = {"req": "card.aux", "usage": usage_list}
        jsonschema.validate(instance=instance, schema=schema)

def test_usage_invalid_type(schema):
    """Tests invalid type for usage (must be array)."""
    instance = {"req": "card.aux", "usage": "high"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'high' is not of type 'array'" in str(excinfo.value)

def test_usage_invalid_item_type(schema):
    """Tests invalid item type within usage array."""
    instance = {"req": "card.aux", "usage": ["high", 1]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_usage_invalid_item_enum(schema):
    """Tests invalid item enum value within usage array."""
    instance = {"req": "card.aux", "usage": ["high", "invalid_usage"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid_usage' is not one of [''," in str(excinfo.value)

def test_seconds_valid(schema):
    """Tests valid seconds values (integer >= 0)."""
    instance = {"req": "card.aux", "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "card.aux", "seconds": "30"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'30' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_minimum(schema):
    """Tests invalid seconds value (< 0)."""
    instance = {"req": "card.aux", "seconds": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_max_valid(schema):
    """Tests valid max values (integer >= 0)."""
    instance = {"req": "card.aux", "max": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "max": 100}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"req": "card.aux", "max": 10.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "10.5 is not of type 'integer'" in str(excinfo.value)

def test_max_invalid_minimum(schema):
    """Tests invalid max value (< 0)."""
    instance = {"req": "card.aux", "max": -5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-5 is less than the minimum of 0" in str(excinfo.value)

def test_start_valid(schema):
    """Tests valid start values (boolean)."""
    instance = {"req": "card.aux", "start": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "start": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_start_invalid_type(schema):
    """Tests invalid type for start."""
    instance = {"req": "card.aux", "start": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_gps_valid(schema):
    """Tests valid gps values (boolean)."""
    instance = {"req": "card.aux", "gps": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "gps": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_gps_invalid_type(schema):
    """Tests invalid type for gps."""
    instance = {"req": "card.aux", "gps": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_rate_valid(schema):
    """Tests valid rate enum values."""
    valid_rates = [
        300, 600, 1200, 2400, 4800, 9600, 19200, 38400,
        57600, 115200, 230400, 460800, 921600
    ]
    for rate in valid_rates:
        instance = {"req": "card.aux", "rate": rate}
        jsonschema.validate(instance=instance, schema=schema)

def test_rate_invalid_enum(schema):
    """Tests invalid rate enum value."""
    instance = {"req": "card.aux", "rate": 14400}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "14400 is not one of [300, 600," in str(excinfo.value)

def test_rate_invalid_type(schema):
    """Tests invalid type for rate."""
    instance = {"req": "card.aux", "rate": "9600"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # enum checks both type and value, so error might be about enum first
    assert "'9600' is not one of [300, 600," in str(excinfo.value) \
        or "'9600' is not of type" in str(excinfo.value)

def test_sync_valid(schema):
    """Tests valid sync values (boolean)."""
    instance = {"req": "card.aux", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_sync_invalid_type(schema):
    """Tests invalid type for sync."""
    instance = {"req": "card.aux", "sync": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_file_valid(schema):
    """Tests valid file value (string)."""
    instance = {"req": "card.aux", "file": "gpio_changes.qo"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "file": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_file_invalid_type(schema):
    """Tests invalid type for file."""
    instance = {"req": "card.aux", "file": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_connected_valid(schema):
    """Tests valid connected values (boolean)."""
    instance = {"req": "card.aux", "connected": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "connected": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_connected_invalid_type(schema):
    """Tests invalid type for connected."""
    instance = {"req": "card.aux", "connected": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_limit_valid(schema):
    """Tests valid limit values (boolean)."""
    instance = {"req": "card.aux", "limit": True}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "limit": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_limit_invalid_type(schema):
    """Tests invalid type for limit."""
    instance = {"req": "card.aux", "limit": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_sensitivity_valid(schema):
    """Tests valid sensitivity values (integer 1-100)."""
    instance = {"req": "card.aux", "sensitivity": 1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "sensitivity": 50}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "sensitivity": 100}
    jsonschema.validate(instance=instance, schema=schema)

def test_sensitivity_invalid_type(schema):
    """Tests invalid type for sensitivity."""
    instance = {"req": "card.aux", "sensitivity": 50.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "50.5 is not of type 'integer'" in str(excinfo.value)

def test_sensitivity_invalid_minimum(schema):
    """Tests invalid sensitivity value (< 1)."""
    instance = {"req": "card.aux", "sensitivity": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is less than the minimum of 1" in str(excinfo.value)

def test_sensitivity_invalid_maximum(schema):
    """Tests invalid sensitivity value (> 100)."""
    instance = {"req": "card.aux", "sensitivity": 101}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "101 is greater than the maximum of 100" in str(excinfo.value)

def test_ms_valid(schema):
    """Tests valid ms values (integer >= 0)."""
    instance = {"req": "card.aux", "ms": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "ms": 100}
    jsonschema.validate(instance=instance, schema=schema)

def test_ms_invalid_type(schema):
    """Tests invalid type for ms."""
    instance = {"req": "card.aux", "ms": "50"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'50' is not of type 'integer'" in str(excinfo.value)

def test_ms_invalid_minimum(schema):
    """Tests invalid ms value (< 0)."""
    instance = {"req": "card.aux", "ms": -10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-10 is less than the minimum of 0" in str(excinfo.value)

def test_count_valid(schema):
    """Tests valid count enum values."""
    valid_counts = [1, 2, 5]
    for count in valid_counts:
        instance = {"req": "card.aux", "count": count}
        jsonschema.validate(instance=instance, schema=schema)

def test_count_invalid_enum(schema):
    """Tests invalid count enum value."""
    instance = {"req": "card.aux", "count": 3}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "3 is not one of [1, 2, 5]" in str(excinfo.value)

def test_count_invalid_type(schema):
    """Tests invalid type for count."""
    instance = {"req": "card.aux", "count": "1"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # enum checks both type and value, so error might be about enum first
    assert "'1' is not one of [1, 2, 5]" in str(excinfo.value) \
        or "'1' is not of type" in str(excinfo.value)

def test_offset_valid(schema):
    """Tests valid offset values (integer >= 1)."""
    instance = {"req": "card.aux", "offset": 1}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.aux", "offset": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_offset_invalid_type(schema):
    """Tests invalid type for offset."""
    instance = {"req": "card.aux", "offset": 1.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1.5 is not of type 'integer'" in str(excinfo.value)

def test_offset_invalid_minimum(schema):
    """Tests invalid offset value (< 1)."""
    instance = {"req": "card.aux", "offset": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is less than the minimum of 1" in str(excinfo.value)

def test_valid_multiple_fields(schema):
    """Tests a valid request with multiple optional fields."""
    instance = {
        "req": "card.aux",
        "mode": "gpio",
        "usage": ["input-pullup", "count-pulldown"],
        "seconds": 60,
        "max": 10,
        "start": True,
        "sync": True,
        "file": "aux_events.qo",
        "connected": False,
        "ms": 20
        # Not including fields unrelated to gpio mode like sensitivity, rate, gps etc.
        # although the schema doesn't enforce these dependencies.
    }
    jsonschema.validate(instance=instance, schema=schema)
