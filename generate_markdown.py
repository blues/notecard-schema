import json
import argparse
import sys
import glob
import re

def generate_markdown(schema, request_name):
    """
    Generates Markdown lines for a single loaded JSON schema dictionary.

    Args:
        schema (dict): The loaded JSON schema.

    Returns:
        list: A list of Markdown strings for this schema.
    """
    print(f"DEBUG: Schema name: {request_name}")
    markdown_lines = []

    heading = f"`{request_name}`" if request_name else schema.get('title', 'Unknown API')
    description = schema.get('description', '')

    markdown_lines.append(f"## {heading}\n")
    if description:
        markdown_lines.append(f"{description}\n")

    # --- Properties ---
    properties = schema.get('properties', {})
    if properties:
        # Use H3 for Parameters subheading
        markdown_lines.append("### Arguments\n")
        markdown_lines.append("| Arguments | Type | Description | Constraints |")
        markdown_lines.append("|---|---|---|---|")

        for name, details in properties.items():
            # Skip internal schema details if they appear as properties
            if name in ["manifestVersion", "apiVersion", "oneOf"]:
                continue

            param_type = details.get('type', 'any')
            param_desc = details.get('description', '')
            constraints = []
            if 'const' in details:
                constraints.append(f"Must be: `{details['const']}`")
            if 'pattern' in details:
                pattern_str = details['pattern']
                options_regex = r"\(\?\:(.*?)\)" 
                match = re.search(options_regex, pattern_str)

                if match:
                    options_part = match.group(1) # E.g. card.attn.req should be "-all|-env|...|wireless"
                    items = options_part.split('|')
                    # Filter out empty strings that might result from split
                    items = [item for item in items if item]

                    if items:
                        formatted_items = [f"`{item}`" for item in items]
                        constraints.append(", ".join(formatted_items))
                    else:
                        # Regex matched but splitting failed
                        constraints.append(f"Pattern: `{pattern_str}`")
                else:
                    # Regex did not match the ^(?:...) structure
                    constraints.append(f"Pattern: `{pattern_str}`")
            if 'minimum' in details:
                constraints.append(f"Minimum: `{details['minimum']}`")
            if 'format' in details:
                 constraints.append(f"Format: `{details['format']}`")
            if details.get('type') == 'array':
                if 'minItems' in details:
                     constraints.append(f"Min items: {details['minItems']}")
                if 'items' in details and 'type' in details['items']:
                    param_type = f"array of {details['items']['type']}"
                if 'items' in details and 'pattern' in details['items']:
                     constraints.append(f"Item pattern: `{details['items']['pattern']}`")


            constraints_str = "<br>".join(constraints) if constraints else ""
            markdown_lines.append(f"| `{name}` | `{param_type}` | {param_desc} | {constraints_str} |")

        markdown_lines.append("\n") # Add space after the table

    return markdown_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a combined Markdown API spec from JSON schema files matching a pattern.')
    parser.add_argument('schema_pattern', help='Glob pattern for the JSON schema files (e.g., "card.*.json").')
    parser.add_argument('-o', '--output', help='Path to the output Markdown file (optional, prints to stdout if omitted).')
    args = parser.parse_args()

    schema_files = glob.glob(args.schema_pattern)

    if not schema_files:
        print(f"Error: No schema files found matching pattern '{args.schema_pattern}'", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(schema_files)} schema files matching '{args.schema_pattern}'.")
    # Pair request and response schemas together
    schema_files.sort()

    # TODO: Add version number to the title
    combined_markdown_lines = ["# Notecard API Specification\n"]

    for schema_path in schema_files:
        print(f"Processing: {schema_path}")
        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
        except FileNotFoundError:
            print(f"  Warning: File not found (should not happen with glob?) {schema_path}", file=sys.stderr)
            continue
        except json.JSONDecodeError:
            print(f"  Warning: Invalid JSON in schema file {schema_path}, skipping.", file=sys.stderr)
            continue
        except Exception as e:
            print(f"  Warning: Could not process file {schema_path}: {e}", file=sys.stderr)
            continue

        # Add separator before each new file section (except the first)
        if len(combined_markdown_lines) > 1:
             combined_markdown_lines.append("\n---\n")

        # Split name from path, e.g. card.attn.req.notecard.api.json -> card.attn.req
        name = ".".join(schema_path.split(".")[:3])
        markdown_section = generate_markdown(schema, name)
        combined_markdown_lines.extend(markdown_section)


    output_content = "\n".join(combined_markdown_lines) + "\n" # Ensure trailing newline

    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output_content)
            print(f"\nCombined Markdown generated successfully: {args.output}")
        except IOError as e:
            print(f"Error writing to output file {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\n" + output_content)