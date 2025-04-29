# Notecard API Schema

This repository contains the JSON schemas for the Notecard API.

## Adding a new schema

1. Create a new `.json` file in this directory. This should follow the Notecard API naming convention, e.g. `card.aux.req.notecard.api.json`.
2. Add a test suite for the schema in the `tests` directory.
3. Add the schema to the `notecard.api.json` file.

## Updating the schema version

To update the version of Notecard firmware that the schemas are compatible with, run the following command:

```bash
python scripts/increment_schema_version.py --property apiVersion --target-version 9.1.2 --pattern "card.attn.*"
```

This will update the `apiVersion` in all files that match the pattern `card.attn.*`.

## Running the tests

```bash
pipenv install --dev
pipenv run pytest
```
