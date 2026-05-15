---
name: notecard-schema
description: >-
  Expert guidance for creating, updating, and validating Notecard API JSON
  schemas in this repository. Use when adding new schemas, fixing existing ones,
  reviewing schema accuracy against official docs, or writing/updating tests.
---

# Notecard Schema Development

This repository contains JSON Schema Draft 2020-12 definitions for the Notecard API. Schemas power the [Notecard API Reference Documentation](https://dev.blues.io/api-reference/).

## Looking Up Official API Documentation

The canonical reference for all API definitions is the **blues/notecard** repository (`/src` directory): https://github.com/blues/notecard. Read those source files to get authoritative parameter names, descriptions, enum values, and SKU restrictions before writing or updating any schema.

**Important — public API gating:** Not all APIs in the source are publicly exposed. Before adding any API that does not already exist in this schema repo, present it to the user and get explicit approval. Never add a new schema for an undocumented or internal API without confirmation.

## File Naming

```
<category>.<api>[.<variant>].req.notecard.api.json   # request schema
<category>.<api>[.<variant>].rsp.notecard.api.json   # response schema
```

Examples: `card.attn.req.notecard.api.json`, `card.wireless.penalty.rsp.notecard.api.json`, `hub.get.req.notecard.api.json`

Test files mirror the schema name with underscores: `tests/test_card_aux_req.py`

## Schema Structure (follow this field order exactly)

Use `card.aux.req.notecard.api.json` as the canonical ordering reference. Required top-level fields in order:

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://raw.githubusercontent.com/blues/notecard-schema/master/<filename>",
    "title": "<category.api> Request/Response Application Programming Interface (API) Schema",
    "description": "<from official docs>",
    "type": "object",
    "version": "0.2.1",
    "apiVersion": "9.1.1",
    "skus": ["CELL", "CELL+WIFI", "LORA", "WIFI"],
    "properties": { ... },
    "oneOf": [
        { "required": ["req"], "properties": { "req": { "const": "<api.name>" } } },
        { "required": ["cmd"], "properties": { "cmd": { "const": "<api.name>" } } }
    ],
    "required": [],
    "additionalProperties": false,
    "annotations": [ ... ],
    "samples": [ ... ]
}
```

**Response schemas** do not use `oneOf` / `req` / `cmd` — they simply describe the response object with `"additionalProperties": false`.

## Custom Schema Fields

### `annotations`
For INFO/NOTE/WARNING sections from the reference docs:
```json
"annotations": [
    {
        "title": "note",
        "description": "Only valid for Notecard WiFi v2. Sleep mode will not activate while USB-connected."
    }
]
```

### `samples`
At least one sample per schema. Sample JSON must validate against the schema:
```json
"samples": [
    {
        "title": "Enable Sleep Mode",
        "description": "Enable sleep mode with default settings.",
        "json": "{\"req\": \"card.sleep\", \"on\": true}"
    }
]
```

### `sub-descriptions`
Detailed explanations for enum values:
```json
"sub-descriptions": [
    {
        "const": "accel",
        "description": "Wake from deep sleep on any movement detected by the onboard accelerometer."
    }
]
```

### `skus`
Notecard family compatibility — set at both the schema level and individual property level when a property is not available on all SKUs:
```json
"skus": ["CELL", "CELL+WIFI", "WIFI"]
```

Valid SKU values: `"CELL"`, `"CELL+WIFI"`, `"LORA"`, `"WIFI"`

### `deprecated`
Mark deprecated properties with `"deprecated": true`.

### `minApiVersion`
Minimum firmware version that introduced the property: `"minApiVersion": "3.3.1"`

## Pull Request Scope

**One API per PR.** Each pull request must target a single API (e.g. `card.aux`). If changes span multiple APIs, split them into separate PRs — one per API. This keeps reviews focused and history bisectable.

## Adding a New Schema — Checklist

1. **Look up the API** — read the relevant source files in `blues/notecard /src` (https://github.com/blues/notecard) to get authoritative descriptions and parameters; get user approval before proceeding if the API is not already in this repo
2. **Create `<api>.req.notecard.api.json`** — follow the field order from `card.aux.req.notecard.api.json`
3. **Create `<api>.rsp.notecard.api.json`** — model the response structure from the docs
4. **Register both** in `notecard.api.json` (the main index) by adding `$ref` entries under `oneOf`
5. **Write tests** — `tests/test_<api>_req.py` and `tests/test_<api>_rsp.py`
6. **Run tests** — `pipenv run pytest tests/test_<api>_req.py tests/test_<api>_rsp.py -v`

## Test File Structure

Every test file must define `SCHEMA_FILE` and include `test_validate_samples_from_schema`:

```python
import pytest
import jsonschema
import json

SCHEMA_FILE = "card.foo.req.notecard.api.json"


def test_valid_req(schema):
    jsonschema.validate(instance={"req": "card.foo"}, schema=schema)

def test_valid_cmd(schema):
    jsonschema.validate(instance={"cmd": "card.foo"}, schema=schema)

def test_invalid_no_req_or_cmd(schema):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"some_field": True}, schema=schema)

def test_invalid_both_req_and_cmd(schema):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance={"req": "card.foo", "cmd": "card.foo"}, schema=schema)

# ... one test_<field>_valid and test_<field>_invalid_type per property ...

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
```

The `schema` and `schema_samples` fixtures are provided by `tests/conftest.py` — do not redefine them.

## Development Commands

```bash
# Install dependencies
pipenv install --dev

# Run all tests
pipenv run pytest

# Run tests for a specific API
pipenv run pytest tests/test_card_aux_req.py tests/test_card_aux_rsp.py -v
```

## Helper Scripts

All scripts live in `scripts/` and are run from the repo root.

### `create_api.py` — scaffold a new API

**Always start here when adding a new API.** Generates the req/rsp schema templates and corresponding test files with correct boilerplate:

```bash
python3 scripts/create_api.py card.random
python3 scripts/create_api.py hub.sync
```

Creates four files: `<api>.req.notecard.api.json`, `<api>.rsp.notecard.api.json`, `tests/test_<api>_req.py`, `tests/test_<api>_rsp.py`. Edit them to fill in the real API details after scaffolding.

### `fix_schema_property_order.py` — sort properties alphabetically

Sorts `properties` keys alphabetically, placing `req`/`cmd` at the end. Run after manually adding or reordering properties:

```bash
# Fix a single schema file
python3 scripts/fix_schema_property_order.py card.foo.req.notecard.api.json

# Preview changes without modifying files
python3 scripts/fix_schema_property_order.py --all --dry-run

# Fix all schema files
python3 scripts/fix_schema_property_order.py --all
```

### `update_schema_version.py` — bulk version updates

Updates `version` or `apiVersion` across multiple schema files:

```bash
# Update apiVersion across all schemas
python3 scripts/update_schema_version.py --property apiVersion --target-version 9.2.0

# Update schema version for card.* APIs only
python3 scripts/update_schema_version.py --property version --target-version 0.2.2 --pattern "card.*"
```

### `generate_mdx_from_schema.py` — preview documentation output

Converts schemas to MDX to preview how they'll render in the docs site:

```bash
# Generate docs for a specific API
python3 scripts/generate_mdx_from_schema.py --api card.foo --tidy

# Generate docs for all APIs
python3 scripts/generate_mdx_from_schema.py --all --tidy --output_dir ./mdx_output
```

### `update_docs.py` — push docs to blues.dev (human-only)

Clones the blues.dev repo, applies generated MDX, and optionally commits and pushes. This should only be run by a human — do not invoke this autonomously:

```bash
# Dry run to preview changes
python3 scripts/update_docs.py --dry-run

# Apply to existing local repo checkout
python3 scripts/update_docs.py --existing-repo /path/to/blues.dev --commit --push
```

## QA Checklist Before Submitting

**Scope**
- [ ] PR targets exactly one API — if changes span multiple APIs, split into separate PRs
- [ ] If this is a new API: user has explicitly approved adding it (not all firmware APIs are public)

**Accuracy — verified against `blues/notecard /src`**
- [ ] Enum values and their `sub-descriptions` match the source exactly
- [ ] SKU arrays are correct at both schema and property level
- [ ] Annotations capture any INFO/WARNING/NOTE callouts from the source

**Schema structure**
- [ ] Both `req` and `cmd` patterns work via `oneOf`
- [ ] `additionalProperties: false` is set
- [ ] Both schema files are registered in `notecard.api.json`
- [ ] Properties are in alphabetical order (`req`/`cmd` last) — run `fix_schema_property_order.py` if unsure

**Tests**
- [ ] At least one `sample` exists and validates against the schema
- [ ] Tests cover every property: valid type, invalid type, enum enforcement, min/max
- [ ] `test_validate_samples_from_schema` is present and passing
- [ ] `pipenv run pytest` passes with no failures
