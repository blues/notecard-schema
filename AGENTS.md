# AGENTS.md

Guidance for AI coding agents working in this repository. This is the single
source of truth for agent instructions — `CLAUDE.md` imports this file, and
there is no separate Copilot instructions file.

## Repository Overview

This repository contains JSON Schema (Draft 2020-12) definitions for the
Notecard API. The composition of all schemas generates the
[Notecard API Reference Documentation](https://dev.blues.io/api-reference/).

Every schema file must validate against the meta-schema at
<https://json-schema.org/draft/2020-12/schema>.

Because these schemas *are* the published documentation, accuracy of prose
matters as much as structural correctness. Descriptions are copied verbatim
from the source of truth, not paraphrased.

## Source of Truth for API Definitions

The canonical reference for API definitions is the **`blues/notecard`
repository** (`/src` directory): <https://github.com/blues/notecard>. Read those
source files to get authoritative parameter names, descriptions, enum values,
and SKU restrictions before writing or updating any schema.

The published docs at <https://dev.blues.io/api-reference/notecard-api> are a
secondary reference — useful for INFO/WARNING callouts and examples that do not
appear in firmware source, but the firmware source wins on any conflict.

> **Public API gating:** Not all APIs in the firmware source are publicly
> exposed. Before adding any API that does not already exist in this repo,
> present it to the user and get explicit approval. Never add a schema for an
> undocumented or internal API without confirmation.

## File Naming

```
<category>.<api>[.<variant>].req.notecard.api.json   # request schema
<category>.<api>[.<variant>].rsp.notecard.api.json   # response schema
```

Examples: `card.attn.req.notecard.api.json`,
`card.wireless.penalty.rsp.notecard.api.json`, `hub.get.req.notecard.api.json`

Test files mirror the schema name with underscores:
`tests/test_card_aux_req.py`, `tests/test_card_wireless_penalty_rsp.py`

## Schema Structure

**Preserve field order exactly.** Use `card.aux.req.notecard.api.json` as the
canonical ordering reference. Top-level fields in order:

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://raw.githubusercontent.com/blues/notecard-schema/master/<filename>",
    "title": "<category.api> Request Application Programming Interface (API) Schema",
    "description": "<verbatim from source>",
    "type": "object",
    "version": "1.1.2",
    "apiVersion": "9.1.1",
    "skus": ["CELL", "CELL+WIFI", "LORA", "SKYLO", "WIFI"],
    "properties": { ... },
    "oneOf": [
        { "required": ["req"], "properties": { "req": { "const": "<api.name>" } } },
        { "required": ["cmd"], "properties": { "cmd": { "const": "<api.name>" } } }
    ],
    "unevaluatedProperties": false,
    "annotations": [ ... ],
    "samples": [ ... ],
    "links": [ ... ]
}
```

- `title` follows the pattern
  `"<category>.<api> Request/Response Application Programming Interface (API) Schema"`.
- `version` is the schema's own version; `apiVersion` is the Notecard firmware
  version the schema describes. Current repo-wide values are `1.1.2` and
  `9.1.1` — check an existing schema rather than trusting this line if it looks
  stale.
- `links` is optional and always placed last, after `samples`.
- Use **`"unevaluatedProperties": false`**, not `additionalProperties`. Request
  schemas put `req`/`cmd` inside `oneOf`, and `additionalProperties` does not
  see into subschemas — it would reject every valid request. All 75 request
  schemas and 60 response schemas use `unevaluatedProperties`.
- Add `required` only when the API genuinely requires a parameter. It is not
  boilerplate; most schemas omit it entirely.
- **Response schemas** do not use `oneOf` / `req` / `cmd`. They describe the
  response object directly, still with `"unevaluatedProperties": false`.
- Properties are sorted alphabetically with `req`/`cmd` last — run
  `scripts/fix_schema_property_order.py` rather than sorting by hand.

## Custom Schema Fields

These fields fall outside standard JSON Schema and exist to reproduce the
original documentation faithfully. The README has fuller examples for each; see
[Custom Fields](README.md#custom-fields).

| Field | Purpose |
| --- | --- |
| `annotations` | INFO/NOTE/WARNING/Deprecated callouts from the source docs |
| `deprecated` | Boolean marking a deprecated API, property, or enum value |
| `links` | Related docs, rendered as the "More information" block |
| `minApiVersion` | Minimum firmware version that introduced the item |
| `samples` | JSON examples rendered as code blocks |
| `skus` | Notecard family compatibility |
| `sub-descriptions` | Per-value detail for enums and pattern matches |

### `annotations`

Valid `title` values are `"note"`, `"warning"`, and `"deprecated"`.

```json
"annotations": [
    {
        "title": "note",
        "description": "Only valid for Notecard WiFi v2. Sleep mode will not activate while USB-connected."
    }
]
```

### `samples`

Every `req` schema must have at least one sample. For `rsp` schemas, samples
are optional only when there is no response body. Sample JSON must validate
against its own schema — this is enforced by
`test_validate_samples_from_schema`.

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

```json
"sub-descriptions": [
    {
        "const": "accel",
        "description": "Wake from deep sleep on any movement detected by the onboard accelerometer.",
        "skus": ["CELL", "CELL+WIFI", "SKYLO", "WIFI"]
    }
]
```

### `skus`

Valid values: `"CELL"`, `"CELL+WIFI"`, `"LORA"`, `"SKYLO"`, `"WIFI"`.

Set at the schema level and again at the individual property, enum, or
sub-description level whenever that item is not available on all SKUs. `skus`
is valid anywhere `description` is valid.

### `links`

URLs must be **absolute** so the schemas stay useful outside of blues.dev. The
docs generator rewrites `https://dev.blues.io` to a site-relative path when it
builds the site, so do not hand-write relative paths.

```json
"links": [
    {
        "title": "Working with the Notecard AUX Pins",
        "url": "https://dev.blues.io/notecard/notecard-walkthrough/working-with-the-notecard-aux-pins/"
    }
]
```

## Writing Descriptions

Transfer content from the source documentation **verbatim**, preserving:

- **Markdown links** — keep them as standard markdown links so the text stays
  useful for anyone reading the schema directly.
- **`code` formatting** — keep backticks around parameter names, literal
  values, and Notefile names.
- Quotes, emphasis, and punctuation exactly as written in the source.

Details that do not map to a schema field (examples, extra context, callouts)
belong in the custom fields above rather than being dropped.

## Adding a New Schema

1. **Look up the API** in `blues/notecard` `/src`. If the API is not already in
   this repo, get explicit user approval before proceeding.
2. **Scaffold** with the helper script — always start here:
   ```bash
   pipenv run python scripts/create_api.py card.example
   ```
   This creates `card.example.req.notecard.api.json`,
   `card.example.rsp.notecard.api.json`, `tests/test_card_example_req.py`, and
   `tests/test_card_example_rsp.py`, and registers the request schema in
   `notecard.api.json`.

   > The scaffold currently emits two stale defaults: `"version": "0.2.1"`
   > (repo is at `1.1.2`) and `"additionalProperties": false` (repo uses
   > `"unevaluatedProperties": false`). Correct both in the generated files.
3. **Fill in** both schema files with the verbatim API details.
4. **Verify the index** — `notecard.api.json` gets a `$ref` to the **request
   schema only**. Response schemas are never added to the index.
5. **Write tests** covering every property (see below).
6. **Run the tests**:
   ```bash
   pipenv run pytest tests/test_card_example_req.py tests/test_card_example_rsp.py -v
   ```
7. **Commit** with a clear message describing the new API.

## Updating an Existing Schema

1. Reconcile the schema against the current `blues/notecard` `/src` definition.
2. **Bump `version`** according to what changed:
   - **patch** — `description` changes only
   - **minor** — `properties` changes
   - **major** — breaking changes
3. Reflect any new or changed fields, including custom fields.
4. Update the test suite to cover new or changed behavior.
5. Run the tests and commit with a message describing the update.

To bump the firmware version the schemas target:

```bash
python3 scripts/update_schema_version.py --property apiVersion --target-version 9.1.2 --pattern "card.attn.*"
```

## Pull Request Scope

**One API per PR.** Each pull request targets a single API (e.g. `card.aux`).
If changes span multiple APIs, split them into separate PRs — one per API. This
keeps reviews focused and history bisectable.

## Tests

Every test file defines `SCHEMA_FILE` and includes
`test_validate_samples_from_schema`. The `schema` and `schema_samples` fixtures
come from `tests/conftest.py` — do not redefine them.

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

Coverage should include every parameter: valid type, invalid type, enum
enforcement, and any minimum/maximum constraints.

## Development Commands

```bash
# Install dependencies and git hooks
pipenv install --dev
pipenv run setup-hooks

# Run all tests
pipenv run pytest

# Run tests for a specific API
pipenv run pytest tests/test_card_aux_req.py tests/test_card_aux_rsp.py -v
```

Pre-commit hooks format and validate files before each commit, and CI runs both
`pre-commit` and `pytest` on every pull request. Schema files are formatted with
4-space indent and **unsorted** keys — this is why field order must be
maintained by hand rather than left to a formatter.

## Helper Scripts

All scripts live in `scripts/` and run from the repo root.

### `create_api.py` — scaffold a new API

```bash
pipenv run python scripts/create_api.py card.random
```

### `fix_schema_property_order.py` — sort properties alphabetically

Sorts `properties` keys alphabetically, placing `req`/`cmd` last. Run after
manually adding or reordering properties.

```bash
python3 scripts/fix_schema_property_order.py card.foo.req.notecard.api.json
python3 scripts/fix_schema_property_order.py --all --dry-run
python3 scripts/fix_schema_property_order.py --all
```

### `update_schema_version.py` — bulk version updates

```bash
python3 scripts/update_schema_version.py --property apiVersion --target-version 9.2.0
python3 scripts/update_schema_version.py --property version --target-version 1.1.3 --pattern "card.*"
```

## QA Checklist Before Submitting

**Scope**

- [ ] PR targets exactly one API — split multi-API changes into separate PRs
- [ ] If this is a new API: the user has explicitly approved adding it

**Accuracy — verified against `blues/notecard` `/src`**

- [ ] Descriptions match the source verbatim, with markdown links and backticks
      preserved
- [ ] Enum values and their `sub-descriptions` match the source exactly
- [ ] `skus` arrays are correct at the schema, property, and sub-description
      levels
- [ ] Annotations capture any INFO/WARNING/NOTE callouts
- [ ] `links` URLs are absolute and resolve without redirects

**Schema structure**

- [ ] Top-level field order matches `card.aux.req.notecard.api.json`
- [ ] Both `req` and `cmd` patterns work via `oneOf`
- [ ] `unevaluatedProperties: false` is set (not `additionalProperties`)
- [ ] The **request** schema is registered in `notecard.api.json`
- [ ] Properties are alphabetical with `req`/`cmd` last
- [ ] `version` bumped per the patch/minor/major rule above

**Tests**

- [ ] At least one `sample` exists and validates against the schema
- [ ] Tests cover every property: valid type, invalid type, enum, min/max
- [ ] `test_validate_samples_from_schema` is present and passing
- [ ] `pipenv run pytest` passes with no failures
