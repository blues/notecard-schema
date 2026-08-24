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

### 2. `generate_docs.py` - Documentation Generation Utilities

Contains utility functions for processing schema data and generating API reference documentation content.

**Usage:**
This is primarily a utility module imported by other scripts, but can be used directly for custom documentation workflows.

**Key Functions:**

- `load_schema()` - Load and parse JSON schemas
- `inject_absolute_urls()` - Convert relative links to absolute URLs
- Schema processing and formatting utilities

---

### 3. `update_schema_version.py` - Version Management

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

The blues.dev API reference picks the new API up on the next release; see
[Automation](#automation) below.

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

## Dependencies

The scripts use standard Python libraries and project-specific modules. Install project dependencies with:

```bash
pipenv install --dev
```

## Automation

update-docs.yml`) that automatically updates the blues.dev documentation site when:

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
- Test schemas thoroughly after creation or modification
- Follow the repository's schema conventions and validation requirements
