#!/usr/bin/env python3

"""
Test validation for custom schema fields like annotations and samples.
Ensures proper structure of these custom fields across all schema files.
"""

import json
import pytest
import glob
import os


def get_all_schema_files():
    """Get all .notecard.api.json schema files in the repository."""
    schema_files = []
    # Get all .req.notecard.api.json and .rsp.notecard.api.json files
    req_files = glob.glob("*.req.notecard.api.json")
    rsp_files = glob.glob("*.rsp.notecard.api.json")
    schema_files.extend(req_files)
    schema_files.extend(rsp_files)
    return sorted(schema_files)


@pytest.mark.parametrize("schema_file", get_all_schema_files())
def test_annotations_structure(schema_file):
    """Test that all annotations have required title and description fields."""
    if not os.path.exists(schema_file):
        pytest.skip(f"Schema file {schema_file} not found")

    with open(schema_file, 'r') as f:
        schema = json.load(f)

    # Check top-level annotations
    if "annotations" in schema:
        for i, annotation in enumerate(schema["annotations"]):
            assert isinstance(annotation, dict), f"Annotation {i} in {schema_file} is not a dictionary"
            assert "title" in annotation, f"Annotation {i} in {schema_file} missing 'title' field"
            assert "description" in annotation, f"Annotation {i} in {schema_file} missing 'description' field"
            assert isinstance(annotation["title"], str), f"Annotation {i} 'title' in {schema_file} is not a string"
            assert isinstance(annotation["description"], str), f"Annotation {i} 'description' in {schema_file} is not a string"
            assert len(annotation["title"].strip()) > 0, f"Annotation {i} 'title' in {schema_file} is empty"
            assert len(annotation["description"].strip()) > 0, f"Annotation {i} 'description' in {schema_file} is empty"

    # Check annotations in properties (recursively)
    def check_property_annotations(properties, path=""):
        if not isinstance(properties, dict):
            return

        for prop_name, prop_def in properties.items():
            current_path = f"{path}.{prop_name}" if path else prop_name

            if isinstance(prop_def, dict):
                # Check annotations in this property
                if "annotations" in prop_def:
                    for i, annotation in enumerate(prop_def["annotations"]):
                        assert isinstance(annotation, dict), f"Annotation {i} in property '{current_path}' of {schema_file} is not a dictionary"
                        assert "title" in annotation, f"Annotation {i} in property '{current_path}' of {schema_file} missing 'title' field"
                        assert "description" in annotation, f"Annotation {i} in property '{current_path}' of {schema_file} missing 'description' field"
                        assert isinstance(annotation["title"], str), f"Annotation {i} 'title' in property '{current_path}' of {schema_file} is not a string"
                        assert isinstance(annotation["description"], str), f"Annotation {i} 'description' in property '{current_path}' of {schema_file} is not a string"
                        assert len(annotation["title"].strip()) > 0, f"Annotation {i} 'title' in property '{current_path}' of {schema_file} is empty"
                        assert len(annotation["description"].strip()) > 0, f"Annotation {i} 'description' in property '{current_path}' of {schema_file} is empty"

                # Recursively check nested properties
                if "properties" in prop_def:
                    check_property_annotations(prop_def["properties"], current_path)

                # Check oneOf, anyOf, allOf schemas
                for schema_type in ["oneOf", "anyOf", "allOf"]:
                    if schema_type in prop_def:
                        for j, sub_schema in enumerate(prop_def[schema_type]):
                            if isinstance(sub_schema, dict) and "properties" in sub_schema:
                                check_property_annotations(sub_schema["properties"], f"{current_path}.{schema_type}[{j}]")

    # Check properties in the main schema
    if "properties" in schema:
        check_property_annotations(schema["properties"])

    # Check oneOf schemas at top level
    if "oneOf" in schema:
        for i, sub_schema in enumerate(schema["oneOf"]):
            if isinstance(sub_schema, dict) and "properties" in sub_schema:
                check_property_annotations(sub_schema["properties"], f"oneOf[{i}]")


@pytest.mark.parametrize("schema_file", get_all_schema_files())
def test_samples_structure(schema_file):
    """Test that all samples have required description and json fields, and optionally a title field."""
    if not os.path.exists(schema_file):
        pytest.skip(f"Schema file {schema_file} not found")

    with open(schema_file, 'r') as f:
        schema = json.load(f)

    # Check top-level samples
    if "samples" in schema:
        for i, sample in enumerate(schema["samples"]):
            assert isinstance(sample, dict), f"Sample {i} in {schema_file} is not a dictionary"
            assert "description" in sample, f"Sample {i} in {schema_file} missing 'description' field"
            assert "json" in sample, f"Sample {i} in {schema_file} missing 'json' field"

            assert isinstance(sample["description"], str), f"Sample {i} 'description' in {schema_file} is not a string"
            assert isinstance(sample["json"], str), f"Sample {i} 'json' in {schema_file} is not a string"

            assert len(sample["description"].strip()) > 0, f"Sample {i} 'description' in {schema_file} is empty"
            assert len(sample["json"].strip()) > 0, f"Sample {i} 'json' in {schema_file} is empty"

            # Title is optional, but if present, should be a non-empty string
            if "title" in sample:
                assert isinstance(sample["title"], str), f"Sample {i} 'title' in {schema_file} is not a string"
                assert len(sample["title"].strip()) > 0, f"Sample {i} 'title' in {schema_file} is empty"

            # Validate that the JSON string is valid JSON
            try:
                json.loads(sample["json"])
            except json.JSONDecodeError as e:
                pytest.fail(f"Sample {i} 'json' in {schema_file} is not valid JSON: {e}")

    # Check samples in properties (recursively)
    def check_property_samples(properties, path=""):
        if not isinstance(properties, dict):
            return

        for prop_name, prop_def in properties.items():
            current_path = f"{path}.{prop_name}" if path else prop_name

            if isinstance(prop_def, dict):
                # Check samples in this property
                if "samples" in prop_def:
                    for i, sample in enumerate(prop_def["samples"]):
                        assert isinstance(sample, dict), f"Sample {i} in property '{current_path}' of {schema_file} is not a dictionary"
                        assert "description" in sample, f"Sample {i} in property '{current_path}' of {schema_file} missing 'description' field"
                        assert "json" in sample, f"Sample {i} in property '{current_path}' of {schema_file} missing 'json' field"

                        assert isinstance(sample["description"], str), f"Sample {i} 'description' in property '{current_path}' of {schema_file} is not a string"
                        assert isinstance(sample["json"], str), f"Sample {i} 'json' in property '{current_path}' of {schema_file} is not a string"

                        assert len(sample["description"].strip()) > 0, f"Sample {i} 'description' in property '{current_path}' of {schema_file} is empty"
                        assert len(sample["json"].strip()) > 0, f"Sample {i} 'json' in property '{current_path}' of {schema_file} is empty"

                        # Title is optional, but if present, should be a non-empty string
                        if "title" in sample:
                            assert isinstance(sample["title"], str), f"Sample {i} 'title' in property '{current_path}' of {schema_file} is not a string"
                            assert len(sample["title"].strip()) > 0, f"Sample {i} 'title' in property '{current_path}' of {schema_file} is empty"

                        # Validate that the JSON string is valid JSON
                        try:
                            json.loads(sample["json"])
                        except json.JSONDecodeError as e:
                            pytest.fail(f"Sample {i} 'json' in property '{current_path}' of {schema_file} is not valid JSON: {e}")

                # Recursively check nested properties
                if "properties" in prop_def:
                    check_property_samples(prop_def["properties"], current_path)

                # Check oneOf, anyOf, allOf schemas
                for schema_type in ["oneOf", "anyOf", "allOf"]:
                    if schema_type in prop_def:
                        for j, sub_schema in enumerate(prop_def[schema_type]):
                            if isinstance(sub_schema, dict) and "properties" in sub_schema:
                                check_property_samples(sub_schema["properties"], f"{current_path}.{schema_type}[{j}]")

    # Check properties in the main schema
    if "properties" in schema:
        check_property_samples(schema["properties"])

    # Check oneOf schemas at top level
    if "oneOf" in schema:
        for i, sub_schema in enumerate(schema["oneOf"]):
            if isinstance(sub_schema, dict) and "properties" in sub_schema:
                check_property_samples(sub_schema["properties"], f"oneOf[{i}]")


if __name__ == "__main__":
    # Run tests directly
    schema_files = get_all_schema_files()
    print(f"Found {len(schema_files)} schema files to validate")

    # Test a few files directly for quick validation
    test_files = schema_files[:5] if len(schema_files) > 5 else schema_files
    print(f"Testing structure of first {len(test_files)} files: {test_files}")

    for schema_file in test_files:
        print(f"\nTesting {schema_file}...")
        try:
            test_annotations_structure(schema_file)
            print(f"  ✓ Annotations structure valid")
        except Exception as e:
            print(f"  ✗ Annotations structure failed: {e}")

        try:
            test_samples_structure(schema_file)
            print(f"  ✓ Samples structure valid")
        except Exception as e:
            print(f"  ✗ Samples structure failed: {e}")
