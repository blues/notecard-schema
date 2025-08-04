# Claude Code Memory for Notecard Schema Repository

## Repository Overview
This repository contains JSON schemas for the Notecard API, following JSON Schema Draft 2020-12 specification. The schemas are used to generate the [Notecard API Reference Documentation](https://dev.blues.io/api-reference/).

## Schema Creation Process
When adding a new schema (e.g., `card.sleep`):

1. **Create schema files**: Both `.req.notecard.api.json` and `.rsp.notecard.api.json` files
2. **Add comprehensive tests**: Create corresponding test files in `tests/` directory
3. **Update index**: Add schema references to `notecard.api.json`
4. **Verify descriptions**: Ensure all descriptions match exactly with official API documentation
5. **Preserve markdown formatting**: Ensure all markdown formatting is preserved

## Repository Structure
- Root directory contains all schema files, in the format `category`.`api`.`api content (optional)`.`req/rsp`.`notecard`.json  (e.g., `card.attn.req.notecard.json`,`card.wireless.penalty.rsp.notecard.json`,`hub.get.req.notecard.json`)
- `tests/` directory contains test files following pattern `test_card_*_req.py` and `test_card_*_rsp.py`
- `notecard.api.json` serves as the main index file referencing all schemas

## Testing
- Uses `pipenv` for Python environment management
- Tests use `pytest` with `jsonschema` validation
- Run tests with: `pipenv run pytest`
- All schemas must pass validation tests before being considered complete

## Schema Conventions
- **Title**: Follow pattern `"category.api Request/Response Application Programming Interface (API) Schema"`, (e.g. where `category` and `api` could be `card.attn` or `hub.get`, etc.)
- **Version**: Currently using `"0.2.1"`
- **API Version**: Currently `"9.1.1"`
- **SKUs**: Include appropriate Notecard compatibility (e.g., `["WIFI"]` for WiFi-only APIs)
- **Properties**: Support both `req` and `cmd` patterns using `oneOf` validation
- **Additional Properties**: Set to `false` for strict validation

## Custom Schema Fields
The repository uses several custom fields for documentation generation:

### `annotations`
Used for notes, warnings, and deprecation notices:
```json
"annotations": [
    {
        "title": "note",
        "description": "Only valid for Notecard WiFi v2. Sleep mode will not activate while USB-connected."
    }
]
```

### `samples`
Provides JSON examples with titles and descriptions:
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
Detailed descriptions for known parameter values:
```json
"sub-descriptions": [
    {
        "const": "accel",
        "description": "Wake from deep sleep on any movement detected by the onboard accelerometer."
    }
]
```

### `skus`
Indicates Notecard compatibility at API and parameter level:
```json
"skus": ["WIFI"]
```

## Schema Validation Requirements
- All parameter descriptions must match official API documentation exactly
- Both request and response schemas are required for each API
- Test coverage must include validation of all fields, types, and edge cases
- Schemas must validate successfully against their own sample JSON

## Development Commands
- `pipenv install --dev` - Install development dependencies
- `pipenv run pytest` - Run all tests
- `python scripts/update_schema_version.py --property apiVersion --target-version X.X.X --pattern "card.*"` - Update API versions
