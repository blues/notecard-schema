import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.set.req.notecard.api.json"


def test_valid_req_only(schema):
    """Tests a minimal valid request with only req."""
    instance = {"req": "hub.set"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_cmd_only(schema):
    """Tests a minimal valid command with only cmd."""
    instance = {"cmd": "hub.set"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_product_only(schema):
    """Tests valid request with product field."""
    instance = {"req": "hub.set", "product": "com.company.user:product"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_mode_values(schema):
    """Tests all valid mode values."""
    modes = ["periodic", "continuous", "minimum", "off", "dfu"]
    for mode in modes:
        instance = {"req": "hub.set", "mode": mode}
        jsonschema.validate(instance=instance, schema=schema)


def test_valid_periodic_mode_config(schema):
    """Tests valid periodic mode configuration."""
    instance = {
        "req": "hub.set",
        "mode": "periodic",
        "product": "com.your-company.your-name:your_product",
        "outbound": 90,
        "inbound": 240,
    }
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_continuous_mode_config(schema):
    """Tests valid continuous mode configuration."""
    instance = {
        "req": "hub.set",
        "mode": "continuous",
        "product": "com.your-company.your-name:your_product",
        "outbound": 30,
        "inbound": 60,
        "duration": 240,
        "sync": True,
    }
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_minimum_mode_config(schema):
    """Tests valid minimum mode configuration."""
    instance = {
        "req": "hub.set",
        "product": "com.your-company.your-name:your_product",
        "mode": "minimum",
    }
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_off_mode_config(schema):
    """Tests valid off mode configuration."""
    instance = {"req": "hub.set", "mode": "off"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_host_configuration(schema):
    """Tests valid host configuration."""
    instance = {"req": "hub.set", "host": "a.mynotehub.net"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_host_reset(schema):
    """Tests valid host reset with dash."""
    instance = {"req": "hub.set", "host": "-"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_serial_number(schema):
    """Tests valid serial number configuration."""
    instance = {"req": "hub.set", "sn": "my-device-123"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_outbound_timing(schema):
    """Tests valid outbound timing values."""
    valid_values = [0, 30, 60, 120, 1440]
    for value in valid_values:
        instance = {"req": "hub.set", "outbound": value}
        jsonschema.validate(instance=instance, schema=schema)


def test_valid_outbound_reset(schema):
    """Tests valid outbound reset with -1."""
    instance = {"req": "hub.set", "outbound": -1}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_inbound_timing(schema):
    """Tests valid inbound timing values."""
    valid_values = [0, 60, 240, 480, 1440]
    for value in valid_values:
        instance = {"req": "hub.set", "inbound": value}
        jsonschema.validate(instance=instance, schema=schema)


def test_valid_inbound_reset(schema):
    """Tests valid inbound reset with -1."""
    instance = {"req": "hub.set", "inbound": -1}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_duration_minimum(schema):
    """Tests valid duration minimum value."""
    instance = {"req": "hub.set", "duration": 15}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_duration_values(schema):
    """Tests valid duration values."""
    valid_values = [-1, 15, 60, 240, 480]
    for value in valid_values:
        instance = {"req": "hub.set", "duration": value}
        jsonschema.validate(instance=instance, schema=schema)


def test_valid_voltage_variable_sync(schema):
    """Tests valid voltage-variable sync configuration."""
    instance = {
        "req": "hub.set",
        "mode": "periodic",
        "voutbound": "usb:30;high:60;normal:90;low:120;dead:0",
        "vinbound": "usb:60;high:120;normal:240;low:480;dead:0",
    }
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_voltage_variable_clear(schema):
    """Tests valid voltage-variable clear with dash."""
    instance = {"req": "hub.set", "voutbound": "-", "vinbound": "-"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_align_true(schema):
    """Tests valid align true."""
    instance = {"req": "hub.set", "align": True}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_align_false(schema):
    """Tests valid align false."""
    instance = {"req": "hub.set", "align": False}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_sync_true(schema):
    """Tests valid sync true."""
    instance = {"req": "hub.set", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_sync_false(schema):
    """Tests valid sync false."""
    instance = {"req": "hub.set", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_usb_power_modes(schema):
    """Tests valid USB power variable modes."""
    modes = [{"uperiodic": True}, {"umin": True}, {"uoff": True}]
    for mode_dict in modes:
        instance = {"req": "hub.set", **mode_dict}
        jsonschema.validate(instance=instance, schema=schema)


def test_valid_web_transaction_control(schema):
    """Tests valid web transaction control."""
    instance = {"req": "hub.set", "on": True, "seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_web_transaction_off(schema):
    """Tests valid web transaction off."""
    instance = {"req": "hub.set", "off": True}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_version_string(schema):
    """Tests valid version as string."""
    instance = {"req": "hub.set", "version": "1.0.0"}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_version_object(schema):
    """Tests valid version as object."""
    version_obj = {
        "org": "my-organization",
        "product": "My Product",
        "description": "A description of the image",
        "version": "1.2.4",
        "built": "Jan 01 2025 01:02:03",
        "ver_major": 1,
        "ver_minor": 2,
        "ver_patch": 4,
        "ver_build": 5,
        "builder": "The Builder",
    }
    instance = {"req": "hub.set", "version": version_obj}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_lorawan_details_object(schema):
    """Tests valid LoRaWAN details object."""
    details_obj = {
        "deveui": "0080E11500088B37",
        "appeui": "6E6F746563617264",
        "appkey": "00088B37",
    }
    instance = {"req": "hub.set", "details": details_obj}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_lorawan_details_reset(schema):
    """Tests valid LoRaWAN details reset."""
    instance = {"req": "hub.set", "details": "-"}
    jsonschema.validate(instance=instance, schema=schema)


def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"product": "com.test:app"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)


def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "hub.set", "cmd": "hub.set"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)


def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.set' was expected" in str(excinfo.value)


def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.set' was expected" in str(excinfo.value)


def test_invalid_mode_value(schema):
    """Tests invalid mode value."""
    instance = {"req": "hub.set", "mode": "invalid_mode"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not one of" in str(excinfo.value)


def test_invalid_duration_below_minimum(schema):
    """Tests invalid duration below minimum."""
    instance = {"req": "hub.set", "duration": 10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "10 is not valid under any of the given schemas" in str(excinfo.value)


def test_invalid_outbound_below_minimum(schema):
    """Tests invalid outbound below minimum."""
    instance = {"req": "hub.set", "outbound": -2}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-2 is less than the minimum of -1" in str(excinfo.value)


def test_invalid_inbound_below_minimum(schema):
    """Tests invalid inbound below minimum."""
    instance = {"req": "hub.set", "inbound": -5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-5 is less than the minimum of -1" in str(excinfo.value)


def test_invalid_type_product(schema):
    """Tests invalid type for product."""
    instance = {"req": "hub.set", "product": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)


def test_invalid_type_host(schema):
    """Tests invalid type for host."""
    instance = {"req": "hub.set", "host": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)


def test_invalid_type_sn(schema):
    """Tests invalid type for sn."""
    instance = {"req": "hub.set", "sn": []}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)


def test_invalid_type_outbound(schema):
    """Tests invalid type for outbound."""
    instance = {"req": "hub.set", "outbound": "60"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'60' is not of type 'integer'" in str(excinfo.value)


def test_invalid_type_inbound(schema):
    """Tests invalid type for inbound."""
    instance = {"req": "hub.set", "inbound": 60.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "60.5 is not of type 'integer'" in str(excinfo.value)


def test_invalid_type_duration(schema):
    """Tests invalid type for duration."""
    instance = {"req": "hub.set", "duration": "240"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'240' is not of type 'integer'" in str(excinfo.value)


def test_invalid_type_align(schema):
    """Tests invalid type for align."""
    instance = {"req": "hub.set", "align": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)


def test_invalid_type_sync(schema):
    """Tests invalid type for sync."""
    instance = {"req": "hub.set", "sync": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)


def test_invalid_type_voutbound(schema):
    """Tests invalid type for voutbound."""
    instance = {"req": "hub.set", "voutbound": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)


def test_invalid_type_vinbound(schema):
    """Tests invalid type for vinbound."""
    instance = {"req": "hub.set", "vinbound": False}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "False is not of type 'string'" in str(excinfo.value)


def test_invalid_version_type(schema):
    """Tests invalid version type."""
    instance = {"req": "hub.set", "version": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string', 'object'" in str(excinfo.value)


def test_invalid_lorawan_details_type(schema):
    """Tests invalid LoRaWAN details type."""
    instance = {"req": "hub.set", "details": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'-' was expected" in str(excinfo.value)


def test_invalid_lorawan_details_missing_field(schema):
    """Tests invalid LoRaWAN details missing required field."""
    details_obj = {
        "deveui": "0080E11500088B37",
        "appeui": "6E6F746563617264",
        # Missing appkey
    }
    instance = {"req": "hub.set", "details": details_obj}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'appkey' is a required property" in str(excinfo.value)


def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "hub.set", "extra": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)


def test_valid_complex_configuration(schema):
    """Tests valid complex configuration with multiple fields."""
    instance = {
        "req": "hub.set",
        "product": "com.company.user:device",
        "mode": "continuous",
        "host": "custom.notehub.net",
        "sn": "device-001",
        "outbound": 30,
        "inbound": 60,
        "duration": 240,
        "align": True,
        "sync": True,
        "version": "1.2.3",
    }
    jsonschema.validate(instance=instance, schema=schema)


def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(
                f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}"
            )
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
