import json
import requests
import os

def fetch_schema(url):
    """Fetches and parses JSON schema from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from URL {url}")
        return None

def generate_markdown_for_schema(schema):
    """Generates Markdown documentation for a single Notecard API schema."""
    md_parts = []

    title = schema.get("title", "Untitled Request")
    description = schema.get("description", "No description available.")

    # Schema properties are often nested, but prioritize root level
    properties = None
    if 'properties' in schema: # Check root level first
        properties = schema['properties']
    elif 'allOf' in schema and isinstance(schema['allOf'], list): # Fallback to checking allOf
        for item in schema['allOf']:
            if isinstance(item, dict) and 'properties' in item:
                properties = item['properties']
                break

    # Determine request name: prefer const from req/cmd, fallback to title
    req_name = None
    if properties and isinstance(properties, dict):
        if 'req' in properties and isinstance(properties['req'], dict) and 'const' in properties['req']:
            req_name = properties['req']['const']
        elif 'cmd' in properties and isinstance(properties['cmd'], dict) and 'const' in properties['cmd']:
             req_name = properties['cmd']['const']

    if not req_name:
        req_name = title.split(' ')[0] if title else "request" # Fallback

    md_parts.append(f"### `{req_name}`\n")
    md_parts.append(f"{description}\n")

    if properties and isinstance(properties, dict):
        # Filter out req and cmd to see if other parameters exist
        other_props = {k: v for k, v in properties.items() if k not in ('req', 'cmd')}

        if other_props:
            md_parts.append("**Parameters:**\n")
            md_parts.append("| Parameter | Type | Description | Default |")
            md_parts.append("|---|---|---|---|")

            for name, details in other_props.items():
                if isinstance(details, dict):
                    prop_type = details.get('type', '-')
                    prop_desc = details.get('description', '-')
                    prop_default = details.get('default', '-')

                    # Append enum values to description if present
                    if 'enum' in details and isinstance(details['enum'], list):
                        enum_values = ", ".join([f"`{v}`" for v in details['enum']])
                        prop_desc += f". Allowed values: {enum_values}"
                    # Else, check if pattern suggests allowed values
                    elif 'pattern' in details and isinstance(details['pattern'], str):
                        pattern_str = details['pattern']
                        if pattern_str.startswith('^(?:') and pattern_str.count('|') > 0:
                            try:
                                inner_part = pattern_str.split('(?:')[1].split(')')[0]
                                potential_values = sorted(list(set(val.strip() for val in inner_part.split('|') if val.strip())))
                                if potential_values:
                                    pattern_values = ", ".join([f"`{v}`" for v in potential_values])
                                    # Check if description already hints at this list
                                    if "one of the following" not in prop_desc.lower() and "must be" not in prop_desc.lower():
                                        prop_desc += "."
                                    prop_desc += f" Allowed values (comma separated): {pattern_values}"
                            except IndexError: # Handle cases where split logic fails
                                pass # Ignore if pattern doesn't match expected format

                    # Handle cases where default is not a simple string/number
                    if isinstance(prop_default, (dict, list)):
                        prop_default = json.dumps(prop_default)
                    else:
                        prop_default = f"`{prop_default}`"

                    md_parts.append(f"| `{name}` | `{prop_type}` | {prop_desc} | {prop_default} |")
                else:
                     md_parts.append(f"| `{name}` | `unknown` | Invalid property definition | `-` |")
            md_parts.append("\n")
    else:
        md_parts.append("No specific parameters defined.\n")

    return "\n".join(md_parts)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)

    main_schema_path = os.path.join(workspace_root, "notecard.api.json")
    output_md_path = os.path.join(workspace_root, "NOTECARD_API.md")

    try:
        with open(main_schema_path, 'r') as f:
            main_schema = json.load(f)
    except FileNotFoundError:
        print(f"Error: Main schema file not found at {main_schema_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from {main_schema_path}")
        return

    if "oneOf" not in main_schema or not isinstance(main_schema["oneOf"], list):
        print("Error: 'oneOf' key missing or not a list in main schema.")
        return

    schema_refs = []
    for item in main_schema["oneOf"]:
        if isinstance(item, dict) and "$ref" in item:
            schema_refs.append(item["$ref"])
        else:
            print(f"Warning: Invalid item found in 'oneOf': {item}")

    schema_refs.sort()

    print(f"Found {len(schema_refs)} schema references. Fetching...")
    all_schemas_data = [] # Store tuples of (ref, schema_content)
    fetched_count = 0
    failed_count = 0

    for ref in schema_refs:
        schema_content = fetch_schema(ref)
        if schema_content:
            all_schemas_data.append((ref, schema_content))
            fetched_count += 1
        else:
            failed_count += 1
            print(f"Failed to fetch or parse {ref}")

    print(f"\nFetching complete. Successfully fetched: {fetched_count}, Failed: {failed_count}")

    if not all_schemas_data:
        print("No schemas fetched, cannot generate documentation.")
        return

    # Generate Markdown content
    print(f"Generating Markdown for {len(all_schemas_data)} schemas...")
    markdown_output = []
    api_version = main_schema.get("apiVersion", "Unknown")
    schema_version = main_schema.get("version", "Unknown")

    markdown_output.append("# Notecard API Reference")
    markdown_output.append(f"_Generated from [notecard-schema](https://github.com/blues/notecard-schema) version {schema_version} (API Version: {api_version})_\n")
    markdown_output.append("## Requests\n")
    markdown_output.append("The Notecard accepts requests in JSON format. Each request object must contain a `req` or `cmd` field specifying the request type. E.g. `{\"req\": \"card.status\"}` or `{\"cmd\": \"card.status\"}`\n")

    for ref, schema in all_schemas_data:
        try:
            markdown_output.append(generate_markdown_for_schema(schema))
        except Exception as e:
            print(f"Error generating markdown for {ref}: {e}")

    try:
        with open(output_md_path, 'w') as f:
            f.write("\n".join(markdown_output))
            # Ensure newline at end of file
            if not markdown_output[-1].endswith('\n'):
                 f.write('\n')

        print(f"\nSuccessfully generated Markdown documentation at: {output_md_path}")
    except IOError as e:
        print(f"Error writing Markdown file to {output_md_path}: {e}")

if __name__ == "__main__":
    main()
