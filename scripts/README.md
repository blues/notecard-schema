# Notecard Schema Scripts

This directory contains utility scripts for working with the Notecard JSON schemas.
These scripts help with schema creation, documentation generation, version management, and publishing workflows.

## Scripts Overview

### 1. `create_api.py` - Create New API Schema Templates

Creates new Notecard API schema templates with proper structure and boilerplate.

**Usage:**

```bash
python3 scripts/create_api.py <api_name>
```

**Examples:**

```bash
# Create schemas for card.random API
python3 scripts/create_api.py card.random

# Create schemas for hub.sync API
python3 scripts/create_api.py hub.sync
```

**What it creates:**

- `<api_name>.req.notecard.api.json` - Request schema template
- `<api_name>.rsp.notecard.api.json` - Response schema template
- `tests/test_<api_name>_req.py` - Request validation tests
- `tests/test_<api_name>_rsp.py` - Response validation tests

**Features:**

- Generates proper JSON Schema Draft 2020-12 structure
- Includes standard Notecard schema conventions
- Creates corresponding test files
- Supports both `req` and `cmd` patterns

---

### 2. `generate_mdx_from_schema.py` - Generate MDX Documentation

Converts JSON schemas into MDX documentation files for the blues.dev site.

**Usage:**

```bash
python3 scripts/generate_mdx_from_schema.py [options]
```

**Key Options:**

```bash
--all                    # Generate docs for all APIs
--tidy                   # Clean up output formatting
--schema_dir DIR         # Schema directory (default: current)
--output_dir DIR         # Output directory (default: ./mdx_output)
--api API_NAME           # Generate docs for specific API
```

**Examples:**

```bash
# Generate docs for all APIs
python3 scripts/generate_mdx_from_schema.py --all --tidy

# Generate docs for specific API
python3 scripts/generate_mdx_from_schema.py --api card.attn --tidy

# Custom output directory
python3 scripts/generate_mdx_from_schema.py --all --output_dir /path/to/docs
```

**Features:**

- Converts JSON Schema to human-readable MDX
- Generates parameter tables, examples, and descriptions
- Preserves markdown formatting from schema descriptions
- Supports custom schema fields (annotations, samples, sub-descriptions)
- Creates organized directory structure for documentation site

---

### 3. `generate_docs.py` - Documentation Generation Utilities

Contains utility functions for processing schema data and generating API reference documentation content.

**Usage:**
This is primarily a utility module imported by other scripts, but can be used directly for custom documentation workflows.

**Key Functions:**

- `load_schema()` - Load and parse JSON schemas
- `inject_absolute_urls()` - Convert relative links to absolute URLs
- Schema processing and formatting utilities

---

### 4. `update_docs.py` - Update Blues Documentation Site

Automatically updates the blues.dev repository with generated MDX documentation from schemas.

**Usage:**

```bash
python3 scripts/update_docs.py [options]
```

**Key Options:**

```bash
--schema_dir DIR         # Schema directory (default: current)
--existing-repo PATH     # Use existing blues.dev repo (skips cloning)
--branch BRANCH          # Clone specific branch
--dir DIR                # Directory to clone repo to
--commit                 # Commit changes
--push                   # Push changes (requires --commit)
--commit-message MSG     # Custom commit message
--dry-run                # Preview changes without applying
```

**Examples:**

```bash
# Dry run to preview changes
python3 scripts/update_docs.py --dry-run

# Use existing repository
python3 scripts/update_docs.py --existing-repo /path/to/blues.dev --dry-run

# Full workflow: clone, update, commit, and push
python3 scripts/update_docs.py --commit --push --commit-message "Update API docs"

# Work with specific branch
python3 scripts/update_docs.py --branch feature-branch --commit
```

**Features:**

- Clones blues.dev repository or uses existing directory
- Preserves existing `_meta.json` files and Introduction content
- Generates and applies new MDX documentation
- Optional git commit and push capabilities
- Comprehensive dry-run mode for safe testing

**Workflow:**

1. Clone blues.dev repository (or use existing)
2. Preserve metadata and introduction files
3. Generate new MDX documentation from schemas
4. Replace documentation directory contents
5. Restore preserved metadata files
6. Optionally commit and push changes

---

### 5. `update_schema_version.py` - Version Management

Updates version strings across multiple schema files.

**Usage:**

```bash
python3 scripts/update_schema_version.py --property PROPERTY --target-version VERSION [options]
```

**Required Arguments:**

- `--property` - Property to update (`version` or `apiVersion`)
- `--target-version` - Target version (e.g., `9.1.1`)

**Optional Arguments:**

```bash
--dir DIR                # Directory containing schemas (default: current)
--pattern PATTERN        # File pattern (default: *.json)
```

**Examples:**

```bash
# Update API version for all schemas
python3 scripts/update_schema_version.py --property apiVersion --target-version 9.2.0

# Update schema version for card.* APIs only
python3 scripts/update_schema_version.py --property version --target-version 0.2.2 --pattern "card.*.json"

# Update in specific directory
python3 scripts/update_schema_version.py --property apiVersion --target-version 9.1.1 --dir /path/to/schemas
```

**Features:**

- Bulk updates across multiple files
- Semantic version validation
- File pattern matching support
- Preserves JSON formatting
- Skips files that already have target version

---

### 6. `schema_to_openapi.py` - Convert JSON Schemas to OpenAPI

Converts all Notecard JSON Schema files into a single OpenAPI 3.1 specification. This enables interoperability with the broad OpenAPI tooling ecosystem (code generators, documentation tools, API clients).

**Usage:**

```bash
python3 scripts/schema_to_openapi.py [options]
```

**Key Options:**

```bash
--schema-dir DIR         # Directory containing .notecard.api.json files (default: current)
--output FILE            # Output OpenAPI file (default: notecard-api.openapi.json)
--title TITLE            # API title (default: "Notecard API")
```

**Examples:**

```bash
# Convert all schemas to OpenAPI
python3 scripts/schema_to_openapi.py

# Custom output path
python3 scripts/schema_to_openapi.py --output /path/to/output.json

# From specific schema directory
python3 scripts/schema_to_openapi.py --schema-dir /path/to/schemas
```

**Features:**

- Generates OpenAPI 3.1 specification from individual JSON Schema files
- Maps safety semantics to HTTP methods (GET → readonly, PUT → idempotent, POST → non-idempotent, DELETE → destructive)
- Preserves custom Notecard metadata as `x-` extensions (annotations, samples, sub-descriptions, SKU info)
- Handles polymorphic endpoints (req/cmd discrimination via oneOf)
- Includes binary transfer annotations from supplementary data
- Requires `safety_semantics.json` and `binary_transfer.json` data files in the same directory

---

### 7. `openapi_to_schema.py` - Convert OpenAPI to JSON Schemas

Reverses the OpenAPI conversion, producing individual JSON Schema files from an OpenAPI 3.1 specification.

**Usage:**

```bash
python3 scripts/openapi_to_schema.py [options]
```

**Key Options:**

```bash
--input FILE             # Input OpenAPI file (default: notecard-api.openapi.json)
--output-dir DIR         # Output directory for schema files (default: current)
```

**Examples:**

```bash
# Convert OpenAPI back to individual schemas
python3 scripts/openapi_to_schema.py

# Custom input/output
python3 scripts/openapi_to_schema.py --input api.json --output-dir /path/to/schemas
```

**Features:**

- Produces individual `*.notecard.api.json` schema files
- Rebuilds req/cmd properties and oneOf discrimination
- Restores `$schema` and `$id` envelope structure
- Reverse-maps `x-` extensions back to native Notecard metadata keys

---

### 8. `verify_roundtrip.py` - Round-Trip Verification

Verifies that converting JSON Schema → OpenAPI → JSON Schema produces identical output, ensuring no information is lost in the conversion process.

**Usage:**

```bash
python3 scripts/verify_roundtrip.py [options]
```

**Key Options:**

```bash
--schema-dir DIR         # Directory containing original schemas (default: current)
```

**Examples:**

```bash
# Verify round-trip fidelity for all schemas
python3 scripts/verify_roundtrip.py

# Verify schemas in specific directory
python3 scripts/verify_roundtrip.py --schema-dir /path/to/schemas
```

**Features:**

- Converts all schemas to OpenAPI and back, then compares with originals
- Validates properties, types, descriptions, metadata, allOf, and samples
- Reports per-endpoint pass/fail with detailed diff on failure
- Currently passes 74/74 Notecard API endpoints

---

## Common Workflows

### Creating a New API

1. **Create schema templates:**

   ```bash
   python3 scripts/create_api.py hub.newapi
   ```

2. **Edit the generated schemas** to match the API specification

3. **Run tests** to validate schemas:

   ```bash
   pipenv run pytest tests/test_hub_newapi_req.py tests/test_hub_newapi_rsp.py -v
   ```

4. **Generate documentation:**

   ```bash
   python3 scripts/generate_mdx_from_schema.py --api hub.newapi --tidy
   ```

### Updating Documentation Site

1. **Dry run to preview changes:**

   ```bash
   python3 scripts/update_docs.py --dry-run
   ```

2. **Apply changes to existing repository:**

   ```bash
   python3 scripts/update_docs.py --existing-repo /path/to/blues.dev --commit --push
   ```

### OpenAPI Conversion

1. **Convert schemas to OpenAPI:**

   ```bash
   python3 scripts/schema_to_openapi.py --output notecard-api.openapi.json
   ```

2. **Convert back to individual schemas:**

   ```bash
   python3 scripts/openapi_to_schema.py --input notecard-api.openapi.json --output-dir ./rebuilt
   ```

3. **Verify round-trip fidelity:**

   ```bash
   python3 scripts/verify_roundtrip.py
   ```

### Version Management

1. **Update API version across all schemas:**

   ```bash
   python3 scripts/update_schema_version.py --property apiVersion --target-version 9.2.0
   ```

2. **Update specific schema versions:**

   ```bash
   python3 scripts/update_schema_version.py --property version --target-version 0.3.0 --pattern "card.*.json"
   ```

## Requirements

- Python 3.6+
- `pipenv` for dependency management
- Git (for update_docs.py)
- Internet connection (for cloning repositories)

## Dependencies

The scripts use standard Python libraries and project-specific modules. Install project dependencies with:

```bash
pipenv install --dev
```

## Automation

### GitHub Workflow

The repository includes an automated workflow (`.github/workflows/update-docs.yml`) that automatically updates the blues.dev documentation site when:

- **Tagged Release**: A new release is published on the notecard-schema repository
- **Manual Trigger**: The workflow is manually dispatched via GitHub Actions

**Features:**
- Automatically clones the blues.dev repository
- Generates updated MDX documentation from schemas
- Creates a new branch and commits changes
- Opens a pull request with detailed change information
- Handles both release and manual trigger scenarios

**Required Secrets:**
- `BLUES_DEV_TOKEN`: GitHub token with write access to the blues/blues.dev repository

**Manual Trigger Options:**
- `branch`: Target branch in blues.dev repository (default: main)
- `pr_title`: Custom title for the pull request

**Workflow Steps:**
1. Checkout notecard-schema repository
2. Set up Python environment and dependencies
3. Determine version and branch information
4. Clone blues.dev repository
5. Create new branch for documentation updates
6. Generate and apply documentation changes using `update_docs.py`
7. Push changes and create pull request

## Notes

- All scripts support `--help` for detailed usage information
- Use `--dry-run` options where available to preview changes
- Test schemas thoroughly after creation or modification
- Follow the repository's schema conventions and validation requirements
- The automation workflow preserves all metadata and introduction files
- Manual workflow triggers are useful for testing documentation changes before release
