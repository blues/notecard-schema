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

    # If this is notecard.api.json, pre-fetch its remote $refs
    # and add them to the registry to prevent live HTTP requests during validation
    # and to avoid DeprecationWarnings from jsonschema.
    if schema_filename == "notecard.api.json" and "oneOf" in main_schema_content:
        for ref_obj in main_schema_content.get("oneOf", []):
            if "$ref" in ref_obj:
                ref_url = ref_obj["$ref"]
                if ref_url.startswith(("http://", "https://")):
                    try:
                        # Check if registry already has this specific URL resolved
                        # registry.contents(ref_url) would raise KeyError if not found.
                        # To avoid re-adding if already present by its $id which might be the ref_url:
                        try:
                            registry.contents(ref_url)
                            # If above doesn't raise, it means something is at ref_url URI in registry
                            # Potentially, the resource was already added if its $id == ref_url
                        except KeyError:
                            with urllib.request.urlopen(ref_url) as response:
                                if response.status == 200:
                                    ref_content_str = response.read().decode('utf-8')
                                    ref_content_dict = json.loads(ref_content_str)
                                    ref_resource = Resource.from_contents(ref_content_dict)
                                    registry = ref_resource @ registry
                                else:
                                    pytest.fail(f"Failed to fetch $ref {ref_url}: HTTP {response.status}")
                    except urllib.error.URLError as e:
                        pytest.fail(f"URL Error fetching $ref {ref_url}: {e.reason}")
                    except json.JSONDecodeError as e:
                        pytest.fail(f"JSON Decode Error for $ref {ref_url}: {e}")
                    except Exception as e:
                        pytest.fail(f"Generic Error fetching $ref {ref_url}: {e}")

    if schema_filename == "notecard.api.json":
        return main_schema_content, registry
    else:
        # For all other schema files, return only the schema content
        # and do not pass a registry, as they do not need it or expect it.
        return main_schema_content
