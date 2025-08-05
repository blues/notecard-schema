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

## Schema Quality Assurance Checklist
When reviewing or updating existing schemas, perform these validation checks:

### 1. Documentation Accuracy
- **Compare descriptions**: Verify all parameter descriptions match the official API reference documentation exactly
- **Check mode descriptions**: Ensure enum sub-descriptions use exact wording from reference docs
- **Verify markdown formatting**: Preserve backticks, quotes, and formatting as specified in reference
- **Usage descriptions**: For parameters like `usage` arrays, ensure descriptions match reference format exactly

### 2. SKU Compatibility
- **Review SKU restrictions**: Verify SKU arrays match the compatibility shown in API documentation
- **Check mode-specific SKUs**: Some modes (like `count` operations) may have restricted SKU support
- **Parameter-level SKUs**: Ensure individual parameters have correct SKU restrictions where applicable

### 3. Schema Structure Validation
- **Request schema**: Must support both `req` and `cmd` patterns using `oneOf`
- **Response schema**: Structure must match the actual API response format from reference docs
- **Property types**: Verify all property types (string, integer, boolean, array, object) are correct
- **Constraints**: Check minimum/maximum values, enum lists, and array item types

### 4. Custom Schema Fields
- **Annotations**: Add INFO/NOTE sections from reference docs as annotations with `title: "note"`
- **Deprecated flags**: Add `deprecated: true` for deprecated parameters
- **Sub-descriptions**: Include detailed explanations for enum values
- **Samples**: Ensure sample JSON validates against the schema

### 5. Test Coverage Verification
- **Run existing tests**: `pipenv run pytest tests/test_[api]_req.py tests/test_[api]_rsp.py -v`
- **Update tests if needed**: When schema structure changes, update corresponding test files
- **Comprehensive coverage**: Tests should cover all parameters, types, validation rules, and edge cases
- **Sample validation**: Verify schema samples pass validation tests

### 6. Validation Commands
```bash
# Run specific API tests
pipenv run pytest tests/test_card_aux_req.py tests/test_card_aux_rsp.py -v

# Run all tests
pipenv run pytest

# Validate specific schema files exist and are properly named
ls card.aux.req.notecard.api.json card.aux.rsp.notecard.api.json
```

## Development Commands
- `pipenv install --dev` - Install development dependencies
- `pipenv run pytest` - Run all tests
- `python scripts/update_schema_version.py --property apiVersion --target-version X.X.X --pattern "card.*"` - Update API versions
