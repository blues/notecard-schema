# Notecard API Schema

This repository contains the JSON schemas for the Notecard API.

## Table of Contents

- [Notecard API Schema](#notecard-api-schema)
  - [Table of Contents](#table-of-contents)
  - [Development](#development)
  - [Adding a new schema](#adding-a-new-schema)
    - [Custom Fields](#custom-fields)
      - [`annotations`](#annotations)
      - [`deprecated`](#deprecated)
      - [`minApiVersion`](#minapiversion)
      - [`samples`](#samples)
      - [`skus`](#skus)
      - [`sub-descriptions`](#sub-descriptions)
  - [Updating the schema version](#updating-the-schema-version)
  - [Running the tests](#running-the-tests)

## Development

- Python 3.12+
- `pipenv`

```bash
pipenv install --dev
pipenv run setup-hooks  # Install pre-commit hooks
pipenv run pytest
```

Pre-commit hooks will automatically validate and format files before each commit.

## Adding a new schema

Use the `scripts/create_api.py` script to create a new schema.

```bash
# Example for card.example
pipenv run python scripts/create_api.py card.example
```

This will create a new schema file with the necessary metadata and a basic structure that you can then fill in with the specific details of the API request or response.

1. This will create the `card.example.req.notecard.api.json` and `card.example.rsp.notecard.api.json` schemas.

2. Additionally, the script will create a test suite for both the request and response schemas in the `tests` directory.

3. Update these schemas with the specific details of the new API request or response.

### Custom Fields

The composition of all JSON schemas is also used to generate the
[Notecard API Reference Documentation](https://dev.blues.io/api-reference/).
In order to faithfully recreate the original documentation, several new fields
were created to capture any information that falls outside the scope of the
traditional JSON schema.

#### `annotations`

Annotations, such as "Deprecated", "Note" or "Warning" should be captured as
`deprecated`, `note` and `warning`, respectively.

Example shown from `hub.signal`:

```json
"annotations": [
    {
        "title":"note",
        "description":"See our guide to Using Inbound Signals for more information on how to set up a host microcontroller or single-board computer to receive inbound signals."
    },
    {
        "title":"warning",
        "description":"A Notecard must be in [continuous mode](https://dev.blues.io/api-reference/notecard-api/hub-requests/latest/#hub-set) and have its `sync` argument set to `true` to receive signals."
    }
]
```

#### `deprecated`

A boolean indicating if the API is deprecated.

Example shown from `card.attn`:

```json
"deprecated": true
```

#### `minApiVersion`

A string indicating the minimum API version that the API is compatible with.
This can be applied at the top level of the schema, at the level of a specific property, or at the level of a specific sub-description.
When this generates blues.dev documentation, the version dropdown will hide any content that is below the specified version.

Example shown from `auxgpio` in `card.attn`:

```json
{
    "const": "auxgpio",
    "description": "When armed, causes ATTN to fire if an AUX GPIO input changes. Disable by using `-auxgpio`.",
    "skus": [
        "CELL",
        "CELL+WIFI",
        "LORA",
        "WIFI"
    ],
    "minApiVersion": "3.4.1"
},
```

#### `samples`

An array of objects representing each of the JSON examples provided.
All `req` schemas must have a sample.
For `rsp` schemas, samples are optional if there is no response body.

Example shown from `card.attn`:

```json
"samples": [
    {
        "title": "Connected",
        "description": "Configure the Notecard to perform an interrupt on a successful connection to Notehub.",
        "json": "{\"req\":\"card.attn\",\"mode\":\"arm,connected\"}"
    },
    {
        "title": "Files",
        "description": "Configure the Notecard to perform an interrupt on the `data.qi` and `my-settings.db` Notefiles.",
        "json": "{\"req\":\"card.attn\",\"mode\":\"arm,files\",\"files\":[\"data.qi\",\"my-settings.db\"]}"
    },
    {
        "title": "Location",
        "description": "Configure the Notecard to perform an interrupt when the Notecard makes a position fix.",
        "json": "{\"req\":\"card.attn\",\"mode\":\"arm,location\"}"
    },
    ...
]
```

The value of `json` appears as the JSON code example, the `title`
value appears as the tab header when multiple examples are present, and
`description` is provided as a caption to the example code block.

#### `skus`

An array indicating Notecard compatibility at both the API and parameter level.

Some APIs and parameters are reserved for specific Notecard SKUs (e.g.
`card.wifi` is used to configure the WiFi connectivity of WiFi compatible
Notecards).
All APIs and parameters are considered valid by ALL Notecards,
however, they will be discarded when provided to an incompatible SKU.

Example shown from `card.transport`:

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://raw.githubusercontent.com/blues/notecard-schema/master/card.transport.req.notecard.api.json",
    "title": "card.transport Request Application Programming Interface (API) Schema",
    "description": "Specifies the connectivity protocol to prioritize on the Notecard Cell+WiFi, or when using NTN mode with Starnote and a compatible Notecard.",
    "type": "object",
    "version": "0.2.1",
    "apiVersion": "9.1.1",
    "skus": ["CELL","CELL+WIFI","WIFI"],
    "properties": {
        "method": {
            "description": "The connectivity method to enable on the Notecard.",
            "type": "string",
            "enum": [
                "-",
                "cell",
                "cell-ntn",
                "dual-wifi-cell",
                "ntn",
                "wifi",
                "wifi-cell",
                "wifi-cell-ntn",
                "wifi-ntn"
            ],
            "sub-descriptions": [
                {
                    "const": "-",
                    "description": "Resets the transport mode to the device default.",
                    "skus": ["CELL","CELL+WIFI","WIFI"]
                },
                {
                    "const": "cell",
                    "description": "Enables cellular only on the device.",
                    "skus": ["CELL","CELL+WIFI"]
                },
                {
                    "const": "cell-ntn",
                    "description": "Prioritizes cellular connectivity while falling back to NTN if a cellular connection cannot be established.",
                    "skus": ["CELL","CELL+WIFI"]
                },
                {
                    "const": "dual-wifi-cell",
                    "deprecated": true,
                    "description": "Deprecated form of `\"wifi-cell\"`",
                    "skus": ["CELL+WIFI"]
                },
                ...
            ]
        },
        ...
    }
}
```

> _**NOTE:** `skus` is valid at any level the `description` field is also valid._

#### `sub-descriptions`

An array of objects providing a detailed description of enumerated or pattern
matching values.

It can be difficult, or even impossible, to provide a description for enumerated
or pattern matching values.
In such cases, an additional object can be useful to
provide a description and other details for each of the valid values.

Example shown from `card.attn`:

```json
"mode": {
    "description": "A comma-separated list of one or more of the following keywords. Some keywords are only supported on certain types of Notecards.",
    "type": "string",
    "pattern": "^(?:-all|-env|-files|-location|-motion|-usb|arm|auxgpio|connected|disarm|env|files|location|motion|motionchange|rearm|signal|sleep|usb|watchdog|wireless)(?:,\\s*(?:-all|-env|-files|-location|-motion|-usb|arm|auxgpio|connected|disarm|env|files|location|motion|motionchange|rearm|signal|sleep|usb|watchdog|wireless))*\\s*$",
    "sub-descriptions": [
        {
            "const": "",
            "description": "Fetches currently pending events in the \"files\" collection.",
            "skus": ["CELL","CELL+WIFI","WIFI"]
        },
        {
            "const": "arm",
            "description": "Clear \"files\" events and cause the ATTN pin to go LOW. After an event occurs or \"seconds\" has elapsed, the ATTN pin will then go HIGH (a.k.a. \"fires\"). If \"seconds\" is 0, no timeout will be scheduled. If ATTN is armed, calling `arm` again will disarm (briefly pulling ATTN HIGH), then arm (non-idempotent).",
            "skus": ["CELL","CELL+WIFI","LORA","WIFI"]
        },
        {
            "const": "auxgpio",
            "description": "When armed, causes ATTN to fire if an AUX GPIO input changes. Disable by using `-auxgpio`.",
            "skus": ["CELL","CELL+WIFI","LORA","WIFI"]
        },
        ...
    ]
},
```

## Updating the schema version

To update the version of Notecard firmware that the schemas are compatible with,
run the following command:

```bash
python scripts/update_schema_version.py --property apiVersion --target-version 9.1.2 --pattern "card.attn.*"
```

This will update the `apiVersion` in all files that match the pattern `card.attn.*`.

## Running the tests

```bash
pipenv install --dev
pipenv run pytest
```
