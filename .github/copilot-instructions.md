This repository contains a collection of JSON schema files that define the
structure and validation rules for Notecard API requests and responses.

All schema files must validate against the meta schema defined at
https://json-schema.org/draft/2020-12/schema.

When creating a new schema file, use the `scripts/create-api.py` script to
generate the initial structure. This script will create a new schema file with
the necessary metadata and a basic structure that you can then fill in with
the specific details of the API request or response.

Once the basic schema has been created, or when updating an existing schema
file, reference the source API documentation at
https://dev.blues.io/api-reference/notecard-api for the specified API to ensure
that all the content is preserved.

Often, there are details in the documentation that may not map directly to
fields in the schema, such as examples or additional context. These details
should be captured in the fields described in the "Custom Fields" section of
the README.md file.

When adding a new schema file, ensure that it is added to the `notecard.api.json`
index file. This index file serves as a central reference for all schemas in
the repository and is used to generate the Notecard API Reference Documentation.

When transferring the content to be used in the `description` field of a schema
object from the source API documentation, ensure that you:

- Preserve links found in the documentation as standard markdown links in the
schema file. This ensures that the documentation remains accessible and
relevant for users who may need to reference it while working with the schema.
- Preserve `code` formatting found in the documentation using the standard markdown backticks.

When creating a new schema file, follow these steps:
1. Run the `scripts/create-api.py` script to generate the initial schema file.
2. Fill in the schema file with the specific details of the API request or response.
3. Add the schema file to the `notecard.api.json` index file.
4. Add a test suite for the schema in the `tests` directory to ensure that the schema
   behaves as expected and validates correctly against various inputs.
5. Commit the changes to the repository with a clear commit message that describes
   the new schema or updates made to an existing schema.

When updating an existing schema file, ensure that:
1. The schema file is updated to reflect any changes in the API documentation.
2. Increment the patch version of the schema file if there are only changes to
   the `description`s, the minor version if there are only changes to the
   `properties`, and the major version if there are breaking changes.
3. The content from the source API documentation at
   https://dev.blues.io/api-reference/notecard-api is preserved.
4. Any new fields or changes to existing fields are reflected in the schema file.
5. The test suite for the schema is updated to cover any new or changed functionality.
6. The changes are committed with a clear commit message that describes the updates made.
