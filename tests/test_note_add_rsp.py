import pytest
import jsonschema
import json

SCHEMA_FILE = "note.add.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response with required total field."""
    instance = {"total": 1}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_field(schema):
    """Tests valid total field."""
    instance = {"total": 12}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_template_field(schema):
    """Tests valid template field."""
    instance = {"total": 10, "template": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"total": 5, "template": False}
    jsonschema.validate(instance=instance, schema=schema)


def test_valid_total_and_template(schema):
    """Tests valid response with total and template fields."""
    instance = {"total": 8, "template": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_fields(schema):
    """Tests valid response with both fields."""
    instance = {"total": 15, "template": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_zero(schema):
    """Tests valid response with total of zero."""
    instance = {"total": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_total_large_number(schema):
    """Tests valid response with large total number."""
    instance = {"total": 999999}
    jsonschema.validate(instance=instance, schema=schema)


def test_total_invalid_type_string(schema):
    """Tests invalid string type for total."""
    instance = {"total": "12"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'12' is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_type_boolean(schema):
    """Tests invalid boolean type for total."""
    instance = {"total": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_type_array(schema):
    """Tests invalid array type for total."""
    instance = {"total": [12]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_total_invalid_type_object(schema):
    """Tests invalid object type for total."""
    instance = {"total": {"count": 12}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_total_valid_negative(schema):
    """Tests valid negative total (allowed by schema)."""
    instance = {"total": -1}
    jsonschema.validate(instance=instance, schema=schema)

def test_template_invalid_type_string(schema):
    """Tests invalid string type for template."""
    instance = {"total": 1, "template": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_template_invalid_type_integer(schema):
    """Tests invalid integer type for template."""
    instance = {"total": 1, "template": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_template_invalid_type_array(schema):
    """Tests invalid array type for template."""
    instance = {"total": 1, "template": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_template_invalid_type_object(schema):
    """Tests invalid object type for template."""
    instance = {"total": 1, "template": {"active": True}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)


def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"total": 1, "extra": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"status": "ok"},
        {"message": "note added"},
        {"error": "none"},
        {"result": "success"},
        {"id": "123"},
        {"timestamp": 1640995200},
        {"file": "data.qo"},
        {"body": {"data": "value"}},
        {"payload": "base64data"},
        {"sync": True},
        {"key": "encryption_key"},
        {"verify": False},
        {"binary": True},
        {"live": False},
        {"full": True},
        {"limit": False},
        {"max": 10},
        {"note": "should_not_be_in_response"}
    ]
    
    for field_dict in invalid_fields:
        field_dict["total"] = 1  # Add required field
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests that multiple additional properties are not allowed."""
    instance = {"total": 1, "status": "ok", "message": "added", "extra": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
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

def test_response_is_object_type(schema):
    """Tests that response schema requires object type."""
    # String should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance="not an object", schema=schema)
    
    # Number should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=42, schema=schema)
    
    # Array should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=[], schema=schema)
    
    # Boolean should fail
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=True, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    # Verify schema has additionalProperties: false
    assert schema.get("additionalProperties") is False

def test_empty_response_invalid(schema):
    """Tests that empty response is invalid due to required total field."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'total' is a required property" in str(excinfo.value)

def test_template_only_invalid(schema):
    """Tests that response with only template field is invalid."""
    instance = {"template": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'total' is a required property" in str(excinfo.value)

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    # Any additional property should be rejected
    properties_to_test = [
        "file", "body", "payload", "sync", "key", "verify", "binary", 
        "live", "full", "limit", "max", "cmd", "req", "status", "error", 
        "message", "result", "data", "success", "code", "info", "warning",
        "timestamp", "size", "count", "index", "position", "note"
    ]
    
    for prop in properties_to_test:
        instance = {"total": 1, prop: "test"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_field_combinations(schema):
    """Tests various valid field combinations."""
    combinations = [
        {"total": 1},
        {"total": 5, "template": False},
        {"total": 0, "template": True}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_edge_case_values(schema):
    """Tests edge case values for fields."""
    edge_cases = [
        # Large total values
        {"total": 2147483647},  # Max 32-bit signed integer
        {"total": 0},  # Minimum reasonable value
        
        # Boolean values
        {"total": 1, "template": True},
        {"total": 0, "template": False},
        
    ]
    
    for case in edge_cases:
        jsonschema.validate(instance=case, schema=schema)

def test_database_response_scenarios(schema):
    """Tests typical database response scenarios."""
    scenarios = [
        # Database operation
        {"total": 7},
        # Templated database
        {"total": 12, "template": True},
        # Basic database response
        {"total": 4, "template": False}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_queue_response_scenarios(schema):
    """Tests typical queue response scenarios."""
    scenarios = [
        # Basic queue add
        {"total": 25},
        # Templated queue
        {"total": 18, "template": True},
        # Empty queue after first add
        {"total": 1},
        # Large queue
        {"total": 500}
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_zero_and_negative_totals(schema):
    """Tests zero and negative total values."""
    test_values = [
        {"total": 0},    # Zero notes
        {"total": -1},   # Negative (edge case, might occur in error conditions)
        {"total": -100}  # Large negative
    ]
    
    for value in test_values:
        jsonschema.validate(instance=value, schema=schema)


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