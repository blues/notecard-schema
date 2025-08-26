#!/usr/bin/env python3
"""
Script to fix the property order in Notecard API schema files.

This script reorders properties in JSON schema files to be in alphabetical order,
with 'req' and 'cmd' properties always placed at the end.

Usage:
    python fix_schema_property_order.py <schema_filename>
    python fix_schema_property_order.py card.attn.rsp.notecard.api.json

The script will:
1. Load the specified schema file
2. Sort all properties alphabetically (excluding req/cmd)
3. Place req/cmd at the end of the properties object
4. Preserve all other JSON structure and formatting
5. Write the corrected file back to disk
"""

import json
import argparse
import os
import sys
from collections import OrderedDict


def fix_property_order(schema_data):
    """
    Fix the property order in a schema object.

    Args:
        schema_data (dict): The parsed JSON schema data

    Returns:
        dict: The schema with properties in correct order
    """
    if "properties" not in schema_data or not isinstance(schema_data["properties"], dict):
        return schema_data

    properties = schema_data["properties"]

    # Separate req/cmd from other properties
    req_cmd_properties = {}
    other_properties = {}

    for key, value in properties.items():
        if key in ["req", "cmd"]:
            req_cmd_properties[key] = value
        else:
            other_properties[key] = value

    # Sort other properties alphabetically
    sorted_other_properties = OrderedDict(sorted(other_properties.items()))

    # Combine: sorted properties first, then req/cmd
    ordered_properties = OrderedDict()
    ordered_properties.update(sorted_other_properties)

    # Add req/cmd in consistent order (req first if both exist)
    if "req" in req_cmd_properties:
        ordered_properties["req"] = req_cmd_properties["req"]
    if "cmd" in req_cmd_properties:
        ordered_properties["cmd"] = req_cmd_properties["cmd"]

    # Update the schema data
    schema_data["properties"] = ordered_properties

    return schema_data


def load_json_preserving_order(file_path):
    """
    Load JSON file preserving the order of keys.

    Args:
        file_path (str): Path to the JSON file

    Returns:
        dict: Parsed JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file {file_path}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)


def save_json_preserving_format(data, file_path):
    """
    Save JSON data to file with consistent formatting.

    Args:
        data (dict): Data to save
        file_path (str): Path where to save the file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            # Add final newline
            f.write('\n')
        print(f"Successfully updated: {file_path}")
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        sys.exit(1)


def get_current_property_order(schema_data):
    """
    Get the current order of properties from schema data.

    Args:
        schema_data (dict): The parsed JSON schema data

    Returns:
        list: List of property names in current order
    """
    if "properties" not in schema_data or not isinstance(schema_data["properties"], dict):
        return []

    return list(schema_data["properties"].keys())


def get_all_schema_files(project_root):
    """
    Find all schema files in the project root directory.

    Args:
        project_root (str): Path to the project root directory

    Returns:
        list: List of schema filenames
    """
    import glob

    schema_files = []
    for pattern in ["*.req.notecard.api.json", "*.rsp.notecard.api.json"]:
        schema_files.extend(glob.glob(os.path.join(project_root, pattern)))

    # Return just the filenames, not full paths
    return sorted([os.path.basename(f) for f in schema_files])


def process_schema_file(schema_file, project_root, dry_run=False):
    """
    Process a single schema file to fix property order.

    Args:
        schema_file (str): Name of the schema file
        project_root (str): Path to the project root directory
        dry_run (bool): If True, show changes without applying them

    Returns:
        bool: True if changes were made or would be made, False if no changes needed
    """
    schema_path = os.path.join(project_root, schema_file)

    if not os.path.isfile(schema_path):
        print(f"⚠️  Warning: Schema file not found: {schema_file}")
        return False

    try:
        # Load the schema data
        schema_data = load_json_preserving_order(schema_path)

        # Get current property order
        current_order = get_current_property_order(schema_data)

        if not current_order:
            return False

        # Fix the property order
        fixed_schema_data = fix_property_order(schema_data)

        # Get new property order
        new_order = get_current_property_order(fixed_schema_data)

        # Check if any changes are needed
        if current_order == new_order:
            return False

        print(f"📁 {schema_file}")
        print(f"   Current: {' -> '.join(current_order)}")
        print(f"   New:     {' -> '.join(new_order)}")

        if dry_run:
            print("   🔍 DRY RUN: Would fix property order")
        else:
            # Save the fixed schema
            save_json_preserving_format(fixed_schema_data, schema_path)
            print("   ✅ Fixed property order")

        print()  # Add blank line for readability
        return True

    except Exception as e:
        print(f"❌ Error processing {schema_file}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Fix property order in Notecard API schema files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python fix_schema_property_order.py card.attn.rsp.notecard.api.json
    python fix_schema_property_order.py --all
    python fix_schema_property_order.py --all --dry-run
        """
    )

    parser.add_argument(
        "schema_file",
        nargs='?',
        help="Name of the schema file to fix (e.g., card.attn.rsp.notecard.api.json). Not required when using --all."
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Fix property order for all schema files in the project"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what changes would be made without actually modifying files"
    )

    args = parser.parse_args()

    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    if args.all:
        # Process all schema files
        print("🔍 Finding all schema files...")
        schema_files = get_all_schema_files(project_root)

        if not schema_files:
            print("No schema files found in project directory.")
            return

        print(f"Found {len(schema_files)} schema files")

        if args.dry_run:
            print("🔍 DRY RUN: Showing what changes would be made...\n")
        else:
            print("🔧 Processing schema files...\n")

        files_with_changes = 0
        files_processed = 0

        for schema_file in schema_files:
            files_processed += 1
            if process_schema_file(schema_file, project_root, args.dry_run):
                files_with_changes += 1

        print(f"📊 Summary:")
        print(f"   Total files processed: {files_processed}")
        print(f"   Files {'that would be' if args.dry_run else ''} changed: {files_with_changes}")
        print(f"   Files with correct order: {files_processed - files_with_changes}")

        if args.dry_run and files_with_changes > 0:
            print(f"\n🔧 Run without --dry-run to apply changes to {files_with_changes} files.")
        elif not args.dry_run and files_with_changes > 0:
            print(f"\n✅ Successfully fixed property order in {files_with_changes} files!")
        else:
            print(f"\n✅ All schema files already have correct property order!")

    else:
        # Process single file
        if not args.schema_file:
            print("Error: schema_file is required when --all is not specified.")
            parser.print_help()
            sys.exit(1)

        schema_path = os.path.join(project_root, args.schema_file)

        if not os.path.isfile(schema_path):
            print(f"Error: Schema file not found: {schema_path}")
            print(f"Make sure the file exists in the project root directory.")
            sys.exit(1)

        print(f"Processing schema file: {args.schema_file}")

        # Load the schema data
        schema_data = load_json_preserving_order(schema_path)

        # Get current property order
        current_order = get_current_property_order(schema_data)

        if not current_order:
            print("No properties found in schema file.")
            return

        print(f"Current property order: {' -> '.join(current_order)}")

        # Fix the property order
        fixed_schema_data = fix_property_order(schema_data)

        # Get new property order
        new_order = get_current_property_order(fixed_schema_data)
        print(f"New property order: {' -> '.join(new_order)}")

        # Check if any changes are needed
        if current_order == new_order:
            print("✅ Properties are already in correct order. No changes needed.")
            return

        if args.dry_run:
            print("🔍 DRY RUN: Would make the following changes:")
            print(f"   Current: {' -> '.join(current_order)}")
            print(f"   New:     {' -> '.join(new_order)}")
            print("   Run without --dry-run to apply changes.")
            return

        # Save the fixed schema
        save_json_preserving_format(fixed_schema_data, schema_path)

        print("✅ Property order fixed successfully!")


if __name__ == "__main__":
    main()
