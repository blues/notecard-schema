import pytest
import jsonschema
import json

SCHEMA_FILE = "card.location.mode.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_mode_enums(schema):
    """Tests valid mode enum values."""
    valid_modes = ["continuous", "periodic", "off", "fixed"]
    for mode in valid_modes:
        instance = {"mode": mode}
        jsonschema.validate(instance=instance, schema=schema)

def test_mode_invalid_enum(schema):
    """Tests invalid mode enum value."""
    instance = {"mode": "invalid"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'invalid' is not one of ['continuous'," in str(excinfo.value)

def test_mode_invalid_type(schema):
    """Tests invalid type for mode."""
    instance = {"mode": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"seconds": 3600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"seconds": "3600"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'3600' is not of type 'integer'" in str(excinfo.value)

def test_seconds_invalid_minimum(schema):
    """Tests invalid minimum for seconds."""
    instance = {"seconds": -10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-10 is less than the minimum of 0" in str(excinfo.value)

def test_valid_lat(schema):
    """Tests valid lat field."""
    instance = {"lat": 42.12345}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"lat": -90}
    jsonschema.validate(instance=instance, schema=schema)

def test_lat_invalid_type(schema):
    """Tests invalid type for lat."""
    instance = {"lat": "42.123"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'42.123' is not of type 'number'" in str(excinfo.value)

def test_valid_lon(schema):
    """Tests valid lon field."""
    instance = {"lon": -71.54321}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"lon": 180}
    jsonschema.validate(instance=instance, schema=schema)

def test_lon_invalid_type(schema):
    """Tests invalid type for lon."""
    instance = {"lon": "-71.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'-71.5' is not of type 'number'" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {"max": 600}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"max": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"max": 600.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "600.5 is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "mode": "fixed",
        "seconds": 0, # Often present even if not periodic
        "lat": 40.7128,
        "lon": -74.0060,
        "max": 120
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_vseconds(schema):
    """Tests valid vseconds field."""
    instance = {"vseconds": "usb:3600;high:14400;normal:43200;low:86400;dead:0"}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"vseconds": ""}
    jsonschema.validate(instance=instance, schema=schema)

def test_vseconds_invalid_type(schema):
    """Tests invalid type for vseconds."""
    instance = {"vseconds": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"minutes": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"minutes": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"minutes": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_threshold(schema):
    """Tests valid threshold field."""
    instance = {"threshold": 0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"threshold": 10}
    jsonschema.validate(instance=instance, schema=schema)

def test_threshold_invalid_type(schema):
    """Tests invalid type for threshold."""
    instance = {"threshold": "0"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'0' is not of type 'integer'" in str(excinfo.value)

def test_valid_all_fields_updated(schema):
    """Tests a valid response with all fields including new ones."""
    instance = {
        "mode": "continuous",
        "seconds": 0,
        "vseconds": "usb:60;high:300;normal:3600;low:14400;dead:0",
        "lat": 42.5776,
        "lon": -70.87134,
        "max": 100,
        "minutes": 2,
        "threshold": 4
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"result": "success"}
    jsonschema.validate(instance=instance, schema=schema)

def test_mode_sub_descriptions_exist(schema):
    """Tests that the mode property has sub-descriptions."""
    mode_prop = schema["properties"]["mode"]
    assert "sub-descriptions" in mode_prop, "mode property is missing sub-descriptions"

def test_mode_sub_descriptions_match_enum(schema):
    """Tests that every enum value has a corresponding sub-description and vice versa."""
    mode_prop = schema["properties"]["mode"]
    enum_values = set(mode_prop["enum"])
    sub_desc_values = {sd["const"] for sd in mode_prop["sub-descriptions"]}
    assert enum_values == sub_desc_values, (
        f"Mismatch between enum values and sub-description consts. "
        f"Missing sub-descriptions: {enum_values - sub_desc_values}. "
        f"Extra sub-descriptions: {sub_desc_values - enum_values}."
    )

def test_mode_sub_descriptions_have_description(schema):
    """Tests that each sub-description entry has a non-empty description."""
    mode_prop = schema["properties"]["mode"]
    for sd in mode_prop["sub-descriptions"]:
        assert "description" in sd, f"Sub-description for '{sd['const']}' is missing 'description'"
        assert len(sd["description"]) > 0, f"Sub-description for '{sd['const']}' has empty description"

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
