import pytest
import json
import os
from referencing import Registry, Resource
import urllib.request

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(scope='module')
def schema(request):
    """Loads the JSON schema specified by the test module's SCHEMA_FILE.
    If the schema is 'notecard.api.json', its remote $refs are also fetched
    and added to a registry. Returns a tuple (schema_dict, registry).
    """
    schema_filename = getattr(request.module, "SCHEMA_FILE", None)
    if not schema_filename:
        pytest.fail(f"Test module {request.module.__name__} must define SCHEMA_FILE")

    schema_file_path = os.path.join(project_root, schema_filename)

    if not os.path.exists(schema_file_path):
        pytest.fail(f"Schema file not found at: {schema_file_path}")

    with open(schema_file_path, 'r') as f:
        main_schema_content = json.load(f)

    main_resource = Resource.from_contents(main_schema_content)
    # Initialize registry using the @ operator with the main resource.
    # This assumes main_resource has an $id.
    registry = main_resource @ Registry()

    # If this is notecard.api.json, load its remote $refs from local files
    # and add them to the registry to prevent live HTTP requests during validation
    # and to avoid DeprecationWarnings from jsonschema.
    if schema_filename == "notecard.api.json" and "oneOf" in main_schema_content:
        for ref_obj in main_schema_content.get("oneOf", []):
            if "$ref" in ref_obj:
                ref_url = ref_obj["$ref"]
                if ref_url.startswith(("http://", "https://")):
                    # Extract filename from URL and look for it locally
                    filename = ref_url.split('/')[-1]
                    local_file_path = os.path.join(project_root, filename)
                    
                    try:
                        # Check if registry already has this specific URL resolved
                        registry.contents(ref_url)
                        # If above doesn't raise, it means something is at ref_url URI in registry
                    except KeyError:
                        # Load the local file instead of fetching remote
                        if os.path.exists(local_file_path):
                            try:
                                with open(local_file_path, 'r') as f:
                                    ref_content_dict = json.load(f)
                                ref_resource = Resource.from_contents(ref_content_dict)
                                registry = ref_resource @ registry
                            except (json.JSONDecodeError, IOError) as e:
                                pytest.fail(f"Error loading local file {filename}: {e}")
                        else:
                            # If local file doesn't exist, skip it instead of failing
                            # This allows tests to run even if some referenced schemas are missing
                            continue

    if schema_filename == "notecard.api.json":
        return main_schema_content, registry
    else:
        # For all other schema files, return only the schema content
        # and do not pass a registry, as they do not need it or expect it.
        return main_schema_content

@pytest.fixture(scope='module')
def schema_samples(request):
    """Loads samples from the JSON schema specified by the test module's SCHEMA_FILE."""
    schema_filename = getattr(request.module, "SCHEMA_FILE", None)
    if not schema_filename:
        pytest.fail(f"Test module {request.module.__name__} must define SCHEMA_FILE to use schema_samples")

    schema_file_path = os.path.join(project_root, schema_filename)

    if not os.path.exists(schema_file_path):
        pytest.fail(f"Schema file not found at: {schema_file_path} for schema_samples")

    with open(schema_file_path, 'r') as f:
        schema_data = json.load(f)

    samples = schema_data.get("samples", [])
    if not samples:
        pytest.skip("No samples found in the schema to validate.")

    return samples
