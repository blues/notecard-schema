# Notecard API Schema

This repository contains the JSON schemas for the Notecard API.

## Adding a new schema

1. Create a new `.json` file in this directory. This should follow the Notecard
API naming convention, e.g. `card.aux.req.notecard.api.json`.

2. Add a test suite for the schema in the `tests` directory.

3. Add the schema to the `notecard.api.json` index file.

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

#### `samples`

An array of objects representing each of the JSON examples provided.

Example shown from `env.set`:

```json
"samples": [
    {
        "description": "Set A Variable",
        "json": "{\"req\":\"env.set\", \"name\":\"monitor-pump\", \"text\":\"on\"}"
    },
    {
        "description": "Clear A Variable",
        "json": "{\"req\":\"env.set\", \"name\":\"monitor-pump\"}"
    }
]
```

The value of `json` appears as the JSON code example, and the `description`
value appears as the tab header when multiple examples are present.

#### `skus`

An array indicating Notecard compatibility at both the API and parameter level.

Some APIs and parameters are reserved for specific Notecard SKUs (e.g.
`card.wifi` is used to configure the Wi-Fi connectivity of Wi-Fi compatible
Notecards). All APIs and parameters are considered valid by ALL Notecards,
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
or pattern matching values. In such cases, an additional object can be useful to
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
