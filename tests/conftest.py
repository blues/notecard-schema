import pytest
import json
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(scope='module')
def schema(request):
    """Loads the JSON schema specified by the test module's SCHEMA_FILE."""
    schema_filename = getattr(request.module, "SCHEMA_FILE", None)
    if not schema_filename:
        pytest.fail(f"Test module {request.module.__name__} must define SCHEMA_FILE")

    schema_file_path = os.path.join(project_root, schema_filename)

    # Check if the file exists before opening
    if not os.path.exists(schema_file_path):
        pytest.fail(f"Schema file not found at: {schema_file_path}")

    with open(schema_file_path, 'r') as f:
        schema_data = json.load(f)
    return schema_data
