import pytest
import jsonschema
import json

SCHEMA_FILE = "card.time.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_time(schema):
    """Tests valid time field."""
    instance = {"time": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)

def test_time_invalid_type(schema):
    """Tests invalid type for time."""
    instance = {"time": "1678886400"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1678886400' is not of type 'integer'" in str(excinfo.value)

def test_valid_area(schema):
    """Tests valid area field."""
    instance = {"area": "Greater Boston"}
    jsonschema.validate(instance=instance, schema=schema)

def test_area_invalid_type(schema):
    """Tests invalid type for area."""
    instance = {"area": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_zone(schema):
    """Tests valid zone field."""
    instance = {"zone": "America/New_York"}
    jsonschema.validate(instance=instance, schema=schema)

def test_zone_invalid_type(schema):
    """Tests invalid type for zone."""
    instance = {"zone": True}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "True is not of type 'string'" in str(excinfo.value)

def test_valid_minutes(schema):
    """Tests valid minutes field."""
    instance = {"minutes": -240} # EST offset
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"minutes": 0} # UTC
    jsonschema.validate(instance=instance, schema=schema)

def test_minutes_invalid_type(schema):
    """Tests invalid type for minutes."""
    instance = {"minutes": "-240"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'-240' is not of type 'integer'" in str(excinfo.value)

def test_valid_lat(schema):
    """Tests valid lat field."""
    instance = {"lat": 42.3601}
    jsonschema.validate(instance=instance, schema=schema)

def test_lat_invalid_type(schema):
    """Tests invalid type for lat."""
    instance = {"lat": "42.3601"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'42.3601' is not of type 'number'" in str(excinfo.value)

def test_valid_lon(schema):
    """Tests valid lon field."""
    instance = {"lon": -71.0589}
    jsonschema.validate(instance=instance, schema=schema)

def test_lon_invalid_type(schema):
    """Tests invalid type for lon."""
    instance = {"lon": "-71.0589"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'-71.0589' is not of type 'number'" in str(excinfo.value)

def test_valid_country(schema):
    """Tests valid country field."""
    instance = {"country": "US"}
    jsonschema.validate(instance=instance, schema=schema)

def test_country_invalid_type(schema):
    """Tests invalid type for country."""
    instance = {"country": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'string'" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "time": 1678886400,
        "area": "Silicon Valley",
        "zone": "America/Los_Angeles",
        "minutes": -480,
        "lat": 37.3875,
        "lon": -122.0575,
        "country": "US"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_additional_property(schema):
    """Tests invalid response with additional property."""
    instance = {"time": 1700000000, "source": "gps"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('source' was unexpected)" in str(excinfo.value)

def test_invalid_multiple_additional_properties(schema):
    """Tests response with multiple additional properties (should fail)."""
    instance = {
        "time": 1700000000,
        "source": "gps",
        "extra": "field"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

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
