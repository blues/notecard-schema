import json
import os
import argparse
import re
from pathlib import Path

def is_valid_semver(version_str):
    """Checks if a string is a valid semantic version (X.Y.Z)."""
    return re.match(r"^\d+\.\d+\.\d+$", version_str) is not None

def main():
    parser = argparse.ArgumentParser(description="Set version strings in JSON schema files to a specific value.")
    parser.add_argument("--property", required=True, choices=["version", "apiVersion"], help="The property to update ('version' or 'apiVersion').")
    parser.add_argument("--target-version", required=True, help="The exact version string to set (e.g., '1.2.3').")
    parser.add_argument("--dir", default=".", help="Directory containing the schema files. Defaults to the current directory.")
    parser.add_argument("--pattern", default="*.json", help="Glob pattern for matching schema files. Defaults to '*.json'.")

    args = parser.parse_args()

    if not is_valid_semver(args.target_version):
        print(f"Error: Provided target version '{args.target_version}' is not a valid semantic version (X.Y.Z).")
        return

    schema_dir = Path(args.dir)
    updated_files = 0

    for filepath in schema_dir.glob(args.pattern):
        if filepath.is_file() and filepath.parent.name != "scripts":
            try:
                with open(filepath, "r+") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON: {filepath}")
                        continue

                    if args.property in data:
                        current_version = data[args.property]
                        if current_version == args.target_version:
                            print(f"Skipping {filepath}: Property '{args.property}' is already '{args.target_version}'.")
                            continue

                        new_version = args.target_version
                        data[args.property] = new_version

                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                        # Ensure trailing newline
                        f.seek(0, os.SEEK_END)
                        if f.tell() > 0:
                            f.seek(f.tell() - 1)
                            last_char = f.read(1)
                            if last_char != '\n':
                                f.write('\n')

                        print(f"Updated {args.property} in {filepath} from '{current_version}' to '{new_version}'")
                        updated_files += 1
                    else:
                        pass

            except Exception as e:
                print(f"Error processing file {filepath}: {e}")

    print(f"\nFinished. Updated {updated_files} files.")

if __name__ == "__main__":
    main()
