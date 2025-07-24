import pytest
import jsonschema
import json

SCHEMA_FILE = "card.triangulate.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_status(schema):
    """Tests valid status field."""
    instance = {"status": "triangulated"}
    jsonschema.validate(instance=instance, schema=schema)

def test_status_invalid_type(schema):
    """Tests invalid type for status."""
    instance = {"status": 123}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "123 is not of type 'string'" in str(excinfo.value)

def test_valid_location_fields(schema):
    """Tests valid latitude and longitude fields."""
    instance = {
        "lat": 37.7749,
        "lon": -122.4194
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_lat_boundary_values(schema):
    """Tests latitude boundary values."""
    # Valid boundary values
    instance = {"lat": -90}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"lat": 90}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Invalid boundary values
    instance = {"lat": -90.1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-90.1 is less than the minimum of -90" in str(excinfo.value)
    
    instance = {"lat": 90.1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "90.1 is greater than the maximum of 90" in str(excinfo.value)

def test_lon_boundary_values(schema):
    """Tests longitude boundary values."""
    # Valid boundary values
    instance = {"lon": -180}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"lon": 180}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Invalid boundary values  
    instance = {"lon": -180.1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-180.1 is less than the minimum of -180" in str(excinfo.value)
    
    instance = {"lon": 180.1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "180.1 is greater than the maximum of 180" in str(excinfo.value)

def test_time_field(schema):
    """Tests valid time field."""
    instance = {"time": 1678886400}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Time cannot be negative
    instance = {"time": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_accuracy_field(schema):
    """Tests valid accuracy field."""
    instance = {"accuracy": 150.5}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"accuracy": 0}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Accuracy cannot be negative
    instance = {"accuracy": -10}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-10 is less than the minimum of 0" in str(excinfo.value)

def test_towers_field(schema):
    """Tests valid towers field."""
    instance = {"towers": 3}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"towers": 0}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Towers cannot be negative
    instance = {"towers": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_wifi_field(schema):
    """Tests valid wifi field."""
    instance = {"wifi": 5}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"wifi": 0}
    jsonschema.validate(instance=instance, schema=schema)
    
    # WiFi count cannot be negative
    instance = {"wifi": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_on_field(schema):
    """Tests valid on field."""
    instance = {"on": True}
    jsonschema.validate(instance=instance, schema=schema)
    
    instance = {"on": False}
    jsonschema.validate(instance=instance, schema=schema)
    
    # Invalid type
    instance = {"on": 1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "1 is not of type 'boolean'" in str(excinfo.value)

def test_complete_triangulation_response(schema):
    """Tests a complete valid triangulation response."""
    instance = {
        "status": "triangulated",
        "lat": 37.7749,
        "lon": -122.4194,
        "time": 1678886400,
        "accuracy": 150.5,
        "towers": 3,
        "wifi": 5,
        "on": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_insufficient_data_response(schema):
    """Tests valid response when insufficient data is available."""
    instance = {
        "status": "insufficient-data",
        "towers": 1,
        "wifi": 0,
        "on": True
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_disabled_response(schema):
    """Tests valid response when triangulation is disabled."""
    instance = {
        "status": "disabled",
        "on": False
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
