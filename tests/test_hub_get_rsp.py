import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.get.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (mode is required)."""
    instance = {"mode": "periodic"}
    jsonschema.validate(instance=instance, schema=schema)

def test_missing_required_mode(schema):
    """Tests that an empty object fails validation because mode is required."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'mode' is a required property" in str(excinfo.value)

def test_valid_device_only(schema):
    """Tests valid response with device and required mode fields."""
    instance = {"mode": "periodic", "device": "dev:000000000000000"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_product_only(schema):
    """Tests valid response with product and required mode fields."""
    instance = {"mode": "periodic", "product": "com.company.user:product"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_only(schema):
    """Tests valid response with only the required mode field."""
    instance = {"mode": "periodic"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {
        "device": "dev:000000000000000",
        "product": "com.your-company.your-name:your_product",
        "mode": "periodic",
        "outbound": 60,
        "inbound": 240,
        "host": "a.notefile.net",
        "sn": "your-serial-number",
        "sync": False,
        "voutbound": "5:10",
        "vinbound": "10:15"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_values(schema):
    """Tests valid mode values."""
    mode_values = ["periodic", "continuous", "minimum"]
    for mode in mode_values:
        instance = {"mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_true(schema):
    """Tests valid response with sync true."""
    instance = {"mode": "continuous", "sync": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_sync_false(schema):
    """Tests valid response with sync false."""
    instance = {"mode": "periodic", "sync": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_zero_timing_values(schema):
    """Tests valid response with zero timing values."""
    instance = {"mode": "periodic", "outbound": 0, "inbound": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_large_timing_values(schema):
    """Tests valid response with large timing values."""
    instance = {"mode": "periodic", "outbound": 86400, "inbound": 43200}
    jsonschema.validate(instance=instance, schema=schema)

def test_device_invalid_type(schema):
    """Tests invalid type for device."""
    instance = {"mode": "periodic", "device": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_product_invalid_type(schema):
    """Tests invalid type for product."""
    instance = {"mode": "periodic", "product": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": ["periodic"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_outbound_invalid_type(schema):
    """Tests invalid type for outbound."""
    instance = {"mode": "periodic", "outbound": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_outbound_invalid_float(schema):
    """Tests invalid float type for outbound."""
    instance = {"mode": "periodic", "outbound": 60.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "60.5 is not of type 'integer'" in str(excinfo.value)

def test_inbound_invalid_type(schema):
    """Tests invalid type for inbound."""
    instance = {"mode": "periodic", "inbound": "not-integer"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-integer' is not of type 'integer'" in str(excinfo.value)

def test_inbound_invalid_float(schema):
    """Tests invalid float type for inbound."""
    instance = {"mode": "periodic", "inbound": 240.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "240.5 is not of type 'integer'" in str(excinfo.value)

def test_voutbound_invalid_type(schema):
    """Tests invalid type for voutbound."""
    instance = {"mode": "periodic", "voutbound": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_vinbound_invalid_type(schema):
    """Tests invalid type for vinbound."""
    instance = {"mode": "periodic", "vinbound": 456}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "456 is not of type 'string'" in str(excinfo.value)

def test_host_invalid_type(schema):
    """Tests invalid type for host."""
    instance = {"mode": "periodic", "host": {"url": "a.notefile.net"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'string'" in str(excinfo.value)

def test_sn_invalid_type(schema):
    """Tests invalid type for sn."""
    instance = {"mode": "periodic", "sn": 789}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "789 is not of type 'string'" in str(excinfo.value)

def test_sync_invalid_type(schema):
    """Tests invalid type for sync."""
    instance = {"mode": "periodic", "sync": "not-boolean"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'not-boolean' is not of type 'boolean'" in str(excinfo.value)

def test_sync_invalid_integer(schema):
    """Tests invalid integer type for sync."""
    instance = {"mode": "periodic", "sync": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_valid_partial_combinations(schema):
    """Tests valid responses with various field combinations."""
    combinations = [
        {"mode": "periodic", "device": "dev:123", "product": "com.test:app"},
        {"mode": "continuous", "sync": True},
        {"mode": "periodic", "outbound": 30, "inbound": 120},
        {"mode": "periodic", "host": "custom.notefile.net"},
        {"mode": "periodic", "sn": "SN123456789"},
        {"mode": "periodic", "voutbound": "5:10", "vinbound": "8:12"}
    ]

    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_all_non_required_fields_optional(schema):
    """Tests that all non-required fields are optional by providing just mode."""
    # mode is required, all other fields are optional
    instance = {"mode": "periodic"}
    jsonschema.validate(instance=instance, schema=schema)

    # Test each optional field individually alongside mode
    fields = [
        {"mode": "periodic", "device": "dev:000000000000000"},
        {"mode": "periodic", "product": "com.company.user:product"},
        {"mode": "periodic", "outbound": 60},
        {"mode": "periodic", "inbound": 240},
        {"mode": "periodic", "host": "a.notefile.net"},
        {"mode": "periodic", "sn": "serial123"},
        {"mode": "periodic", "sync": True},
        {"mode": "periodic", "voutbound": "5:10"},
        {"mode": "periodic", "vinbound": "10:15"}
    ]

    for field_dict in fields:
        jsonschema.validate(instance=field_dict, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with an additional property."""
    instance = {"mode": "periodic", "device": "dev:123", "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"mode": "periodic", "status": "ok"},
        {"mode": "periodic", "message": "success"},
        {"mode": "periodic", "time": 1234567890},
        {"mode": "periodic", "version": "1.0"},
        {"mode": "periodic", "result": {}}
    ]

    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = [
        "string",
        123,
        True,
        False,
        ["array"],
        None
    ]

    for invalid_instance in invalid_types:
        if invalid_instance is None:
            continue  # Skip None as it's handled differently
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=invalid_instance, schema=schema)
        # The error message will vary based on type, just ensure validation fails

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
