"""Insert the release `version` into notecard.api.json.

The committed notecard.api.json has no `version` field; the release workflow
runs this to add one (taken from the release tag) to the uploaded asset. The
line is inserted directly above `apiVersion` so the rest of the file's
formatting is left untouched.

Usage: python3 scripts/stamp_release_version.py <version> [path]
"""

import json
import re
import sys


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: stamp_release_version.py <version> [path]")
    version = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) == 3 else "notecard.api.json"

    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"Error: '{version}' is not a semantic version (X.Y.Z).")

    with open(path, encoding="utf-8") as f:
        text = f.read()

    if "version" in json.loads(text):
        sys.exit(f"Error: {path} already has a top-level 'version'.")

    stamped, count = re.subn(
        r'^(    "apiVersion":)',
        f'    "version": "{version}",\n\\1',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        sys.exit(f"Error: no top-level 'apiVersion' line found in {path}.")

    if json.loads(stamped).get("version") != version:
        sys.exit("Error: stamped file did not parse with the expected version.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(stamped)
    print(f"Set version {version} in {path}")


if __name__ == "__main__":
    main()
