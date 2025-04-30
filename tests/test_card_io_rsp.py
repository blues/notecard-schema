import pytest
import jsonschema

SCHEMA_FILE = "card.io.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"result": "success"}
    jsonschema.validate(instance=instance, schema=schema) 