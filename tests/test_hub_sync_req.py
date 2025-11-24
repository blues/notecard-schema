import pytest
import jsonschema
import json

SCHEMA_FILE = "hub.sync.req.notecard.api.json"

def test_valid_req_only(schema):
    """Tests a minimal valid request with only req."""
    instance = {"req": "hub.sync"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_only(schema):
    """Tests a minimal valid command with only cmd."""
    instance = {"cmd": "hub.sync"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_allow(schema):
    """Tests valid request with allow parameter."""
    instance = {"req": "hub.sync", "allow": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd_with_allow(schema):
    """Tests valid command with allow parameter."""
    instance = {"cmd": "hub.sync", "allow": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_out(schema):
    """Tests valid request with out parameter."""
    instance = {"req": "hub.sync", "out": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_req_with_in(schema):
    """Tests valid request with in parameter."""
    instance = {"req": "hub.sync", "in": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_allow_true(schema):
    """Tests valid request with allow true."""
    instance = {"req": "hub.sync", "allow": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_allow_false(schema):
    """Tests valid request with allow false."""
    instance = {"req": "hub.sync", "allow": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_out_true(schema):
    """Tests valid request with out true."""
    instance = {"req": "hub.sync", "out": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_out_false(schema):
    """Tests valid request with out false."""
    instance = {"req": "hub.sync", "out": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_in_true(schema):
    """Tests valid request with in true."""
    instance = {"req": "hub.sync", "in": True}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_in_false(schema):
    """Tests valid request with in false."""
    instance = {"req": "hub.sync", "in": False}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_all_parameters(schema):
    """Tests valid request with all parameters."""
    instance = {
        "req": "hub.sync",
        "allow": True,
        "out": False,
        "in": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_parameter_combinations(schema):
    """Tests valid parameter combinations."""
    combinations = [
        {"req": "hub.sync", "allow": True, "out": True},
        {"req": "hub.sync", "allow": False, "in": True},
        {"req": "hub.sync", "out": True, "in": False},
        {"cmd": "hub.sync", "allow": True, "out": True, "in": False}
    ]
    
    for combo in combinations:
        jsonschema.validate(instance=combo, schema=schema)

def test_valid_single_parameters(schema):
    """Tests valid requests with single optional parameters."""
    parameters = [
        {"req": "hub.sync", "allow": True},
        {"req": "hub.sync", "out": True},
        {"req": "hub.sync", "in": True}
    ]
    
    for param_dict in parameters:
        jsonschema.validate(instance=param_dict, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    """Tests invalid request with neither req nor cmd."""
    instance = {"allow": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request with both req and cmd."""
    instance = {"req": "hub.sync", "cmd": "hub.sync"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_req_value(schema):
    """Tests invalid req value."""
    instance = {"req": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync' was expected" in str(excinfo.value)

def test_invalid_cmd_value(schema):
    """Tests invalid cmd value."""
    instance = {"cmd": "wrong.api"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync' was expected" in str(excinfo.value)

def test_allow_invalid_type_string(schema):
    """Tests invalid string type for allow."""
    instance = {"req": "hub.sync", "allow": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_allow_invalid_type_integer(schema):
    """Tests invalid integer type for allow."""
    instance = {"req": "hub.sync", "allow": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_allow_invalid_type_array(schema):
    """Tests invalid array type for allow."""
    instance = {"req": "hub.sync", "allow": [True]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'boolean'" in str(excinfo.value)

def test_out_invalid_type_string(schema):
    """Tests invalid string type for out."""
    instance = {"req": "hub.sync", "out": "false"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'false' is not of type 'boolean'" in str(excinfo.value)

def test_out_invalid_type_integer(schema):
    """Tests invalid integer type for out."""
    instance = {"req": "hub.sync", "out": 0}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0 is not of type 'boolean'" in str(excinfo.value)

def test_in_invalid_type_string(schema):
    """Tests invalid string type for in."""
    instance = {"req": "hub.sync", "in": "true"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'true' is not of type 'boolean'" in str(excinfo.value)

def test_in_invalid_type_integer(schema):
    """Tests invalid integer type for in."""
    instance = {"req": "hub.sync", "in": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_req_invalid_type_integer(schema):
    """Tests invalid integer type for req."""
    instance = {"req": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync' was expected" in str(excinfo.value)

def test_req_invalid_type_boolean(schema):
    """Tests invalid boolean type for req."""
    instance = {"req": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync' was expected" in str(excinfo.value)

def test_cmd_invalid_type_array(schema):
    """Tests invalid array type for cmd."""
    instance = {"cmd": ["hub.sync"]}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync' was expected" in str(excinfo.value)

def test_cmd_invalid_type_object(schema):
    """Tests invalid object type for cmd."""
    instance = {"cmd": {"api": "hub.sync"}}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'hub.sync' was expected" in str(excinfo.value)

def test_invalid_additional_property(schema):
    """Tests invalid request with additional property."""
    instance = {"req": "hub.sync", "extra": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid command with additional property."""
    instance = {"cmd": "hub.sync", "force": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests invalid request with multiple additional properties."""
    instance = {"req": "hub.sync", "extra1": 123, "extra2": "value"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_invalid_common_additional_properties(schema):
    """Tests that common additional properties are not allowed."""
    invalid_fields = [
        {"force": True},
        {"immediate": True},
        {"timeout": 30},
        {"retry": False},
        {"sync_all": True},
        {"mode": "manual"}
    ]
    
    for field_dict in invalid_fields:
        field_dict["req"] = "hub.sync"
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=field_dict, schema=schema)
        assert "Additional properties are not allowed" in str(excinfo.value)

def test_all_parameters_optional(schema):
    """Tests that all parameters except req/cmd are optional."""
    instance = {"req": "hub.sync"}
    jsonschema.validate(instance=instance, schema=schema)

def test_empty_object_invalid(schema):
    """Tests that empty object is invalid."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_conflicting_parameters_allowed(schema):
    """Tests that conflicting parameters are allowed by schema."""
    # Schema doesn't prevent both out and in being true simultaneously
    instance = {"req": "hub.sync", "out": True, "in": True}
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
