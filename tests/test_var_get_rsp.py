import pytest
import jsonschema
import json

SCHEMA_FILE = "var.get.rsp.notecard.api.json"

def test_valid_text_response(schema):
    """Tests valid response with text field."""
    valid_responses = [
        {"text": "open"},
        {"text": "closed"},
        {"text": "active"},
        {"text": ""}
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_valid_value_response(schema):
    """Tests valid response with value field."""
    valid_responses = [
        {"value": 42},
        {"value": 0},
        {"value": -10},
        {"value": 1000},
        {"value": 23.5},
        {"value": -12.34},
        {"value": 0.0}
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_valid_flag_response(schema):
    """Tests valid response with flag field."""
    valid_responses = [
        {"flag": True},
        {"flag": False}
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_valid_empty_response(schema):
    """Tests valid empty response (all fields optional)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_text_type(schema):
    """Tests invalid type for text field."""
    invalid_text_types = [
        {"text": 123},
        {"text": True},
        {"text": []},
        {"text": {}},
        {"text": None}
    ]
    
    for instance in invalid_text_types:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'string'" in str(excinfo.value)

def test_invalid_value_type(schema):
    """Tests invalid type for value field."""
    invalid_value_types = [
        {"value": "123"},
        {"value": True},
        {"value": []},
        {"value": {}},
        {"value": None}
    ]
    
    for instance in invalid_value_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=instance, schema=schema)

def test_invalid_flag_type(schema):
    """Tests invalid type for flag field."""
    invalid_flag_types = [
        {"flag": "true"},
        {"flag": 1},
        {"flag": 0},
        {"flag": []},
        {"flag": {}},
        {"flag": None}
    ]
    
    for instance in invalid_flag_types:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "is not of type 'boolean'" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {
        "text": "open",
        "extra": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid response with multiple additional properties."""
    instance = {
        "text": "open",
        "name": "status",
        "timestamp": 1640995200
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"text": "open", "name": "status"},
        {"value": 42, "id": "temperature"},
        {"flag": True, "status": "ok"},
        {"text": "test", "error": "none"},
        {"value": 10, "result": "success"},
        {"flag": False, "message": "retrieved"},
        {"text": "data", "timestamp": 1640995200},
        {"value": 25, "unit": "celsius"},
        {"flag": True, "source": "sensor"}
    ]
    
    for field_dict in invalid_fields:
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_response_type_validation(schema):
    """Tests that response must be an object."""
    invalid_types = ["string", 123, True, False, ["array"]]
    
    for invalid_instance in invalid_types:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=schema)

def test_variable_retrieval_scenarios(schema):
    """Tests realistic variable retrieval response scenarios."""
    scenarios = [
        {"text": "open"},        # String value
        {"value": 23},          # Integer temperature reading  
        {"value": 23.5},        # Float temperature reading
        {"flag": True},         # Boolean status
        {"text": "error"},      # Error message
        {"value": 0},           # Zero value
        {"value": 0.0},         # Zero float value
        {"flag": False},        # False flag
        {"text": "active"},     # Status text
        {"value": -5},          # Negative integer value
        {"value": -12.34},      # Negative float value
        {}                      # Empty response (no variable found)
    ]
    
    for scenario in scenarios:
        jsonschema.validate(instance=scenario, schema=schema)

def test_additional_properties_false(schema):
    """Tests that additionalProperties is set to false."""
    assert schema.get("additionalProperties") is False

def test_all_fields_optional(schema):
    """Tests that all response fields are optional."""
    valid_responses = [
        {},                    # No fields
        {"text": "value"},     # Only text
        {"value": 42},         # Only value  
        {"flag": True}         # Only flag
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_multiple_fields_allowed(schema):
    """Tests that multiple response fields can be present together."""
    # Note: While the API typically returns one field, the schema allows multiple
    valid_responses = [
        {"text": "status", "value": 1},
        {"text": "active", "flag": True},
        {"value": 42, "flag": False},
        {"text": "test", "value": 10, "flag": True}
    ]
    
    for response in valid_responses:
        jsonschema.validate(instance=response, schema=schema)

def test_strict_validation(schema):
    """Tests that schema enforces strict validation."""
    properties_to_test = [
        "name", "id", "status", "error", "message", "result", "data",
        "timestamp", "unit", "source", "type", "format", "encoding"
    ]
    
    for prop in properties_to_test:
        instance = {"text": "test", prop: "value"}
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_number_edge_cases(schema):
    """Tests edge cases for numeric value field."""
    valid_number_responses = [
        {"value": 0},
        {"value": 0.0},
        {"value": -1},
        {"value": -1.0},
        {"value": 2147483647},   # Max 32-bit signed int
        {"value": -2147483648},  # Min 32-bit signed int
        {"value": 1.7976931348623157e+308},  # Large float
        {"value": -1.7976931348623157e+308}, # Large negative float
        {"value": 2.2250738585072014e-308},  # Small positive float
        {"value": -2.2250738585072014e-308}  # Small negative float
    ]
    
    for response in valid_number_responses:
        jsonschema.validate(instance=response, schema=schema)

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
