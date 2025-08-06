import json
import os
import argparse
import html
import re

def generate_sku_badges(skus):
    """Generate badge HTML for SKUs."""
    if not skus:
        return ""

    sku_map = {
        "CELL": "cell",
        "CELL+WIFI": "cell+wifi",
        "LORA": "lora",
        "WIFI": "wifi"
    }

    badges = []
    for sku in skus:
        if sku in sku_map:
            badges.append(f'<Badge type="{sku_map[sku]}"/>')

    return "".join(badges)

def generate_argument_badges(skus):
    """Generate argument-specific badge HTML for SKUs."""
    if not skus:
        return ""

    sku_map = {
        "CELL": "cell",
        "CELL+WIFI": "cell+wifi",
        "LORA": "lora",
        "WIFI": "wifi"
    }

    badges = []
    for sku in skus:
        if sku in sku_map:
            badges.append(f'<Badge type="{sku_map[sku]}" usage="argument"/>')

    return "".join(badges)

def convert_blues_urls_to_relative(text):
    """Convert absolute Blues.io URLs to relative URLs."""
    # Pattern to match Blues.io URLs
    pattern = r'https://dev\.blues\.io(/[^)\s]*)'
    replacement = r'\1'
    return re.sub(pattern, replacement, text)

def generate_mdx_content(schema_data, api_base_name, response_schema_data=None):
    """Generates an MDX string from the JSON schema, optionally including response info."""

    req_cmd_value = api_base_name
    if schema_data.get("properties"):
        if schema_data["properties"].get("req") and schema_data["properties"]["req"].get("const"):
            req_cmd_value = schema_data["properties"]["req"]["const"]
        elif schema_data["properties"].get("cmd") and schema_data["properties"].get("cmd").get("const"):
            req_cmd_value = schema_data["properties"]["cmd"]["const"]

    # Generate badges for SKUs
    sku_badges = generate_sku_badges(schema_data.get("skus", []))
    title = f"## {req_cmd_value} {sku_badges}".strip()
    description = schema_data.get("description", "")

    # Generate annotations block
    annotations_block = generate_annotations_mdx(schema_data.get("annotations", []))

    arguments_mdx_content = generate_arguments_mdx(schema_data.get("properties", {}), schema_data)
    example_requests_block = generate_examples_mdx(schema_data.get("samples", []))

    # Prepare data for response sections, ensuring defaults if response_schema_data is None or incomplete
    effective_response_schema_data = response_schema_data if response_schema_data is not None else {}
    response_properties = effective_response_schema_data.get("properties", {})
    response_samples = effective_response_schema_data.get("samples", [])

    # generate_response_members_mdx always returns the block
    response_members_block = generate_response_members_mdx(response_properties, effective_response_schema_data)
    # generate_example_response_mdx returns block only if samples exist
    example_response_block = generate_example_response_mdx(response_samples)

    mdx_parts = [
        title,
        description,
        annotations_block,
        "<Arguments>",
        arguments_mdx_content,
        "</Arguments>",
        example_requests_block,
        response_members_block,
        example_response_block
    ]

    mdx_content = "\n\n".join(filter(None, mdx_parts))
    # Convert absolute Blues.io URLs to relative URLs
    mdx_content = convert_blues_urls_to_relative(mdx_content)
    return mdx_content

def generate_arguments_mdx(properties, schema_data):
    """Generates MDX for schema properties (arguments). Content only."""
    if not properties:
        return ""
    args_list = []

    # Check if this is using oneOf structure for required fields
    one_of_structure = schema_data.get("oneOf", [])
    top_level_required = []
    if one_of_structure:
        # Extract required fields from oneOf structure
        for variant in one_of_structure:
            if "required" in variant:
                top_level_required.extend(variant["required"])

    for prop_name, prop_details in properties.items():
        if prop_name in ["req", "cmd", "required"]:
            continue

        prop_type = prop_details.get("type", "N/A")
        optional_tag = " (optional)"
        if prop_name in top_level_required:
            optional_tag = ""

        type_display = f"_{prop_type}{optional_tag}_"
        if prop_details.get("format"):
            type_display = f"_{prop_type} (format: {prop_details.get('format')}){optional_tag}_"
        elif "const" in prop_details:
            type_display = f"_const (value: `{prop_details['const']}`){optional_tag}_"

        description = prop_details.get("description", "No description.")

        # Generate SKU badges for individual parameters
        param_skus = prop_details.get("skus", [])
        param_badges = generate_argument_badges(param_skus) if param_skus else ""

        # Handle special case for mode parameter with sub-descriptions
        if prop_name == "mode" and "sub-descriptions" in prop_details:
            sub_desc_content = generate_mode_sub_descriptions(prop_details["sub-descriptions"])
            args_list.append(f"### `{prop_name}`\n\n{type_display}\n\n{description}\n\n{sub_desc_content}")
        # Handle array parameters with sub-descriptions in items
        elif prop_type == "array" and "items" in prop_details and "sub-descriptions" in prop_details["items"]:
            sub_desc_content = generate_mode_sub_descriptions(prop_details["items"]["sub-descriptions"])
            args_list.append(f"### `{prop_name}`\n\n{type_display}\n\n{description}\n\n{sub_desc_content}")
        else:
            # Add parameter SKU badges after the parameter name if they exist
            param_header = f"### `{prop_name}`"
            if param_badges:
                param_header = f"### `{prop_name}` {param_badges}"
            args_list.append(f"{param_header}\n\n{type_display}\n\n{description}")

    return "\n\n".join(args_list)

def generate_mode_sub_descriptions(sub_descriptions):
    """Generate formatted sub-descriptions for mode parameter."""
    sub_desc_parts = []

    for sub_desc in sub_descriptions:
        const_value = sub_desc.get("const", "")
        description = sub_desc.get("description", "")
        skus = sub_desc.get("skus", [])

        badges = generate_argument_badges(skus)

        # Handle special formatting for empty string
        if const_value == "":
            const_display = '`""`'
        else:
            const_display = f'`"{const_value}"`'

        sub_desc_parts.append(f"{const_display} {badges}\n\n{description}")

    return "\n\n".join(sub_desc_parts)

def generate_cpp_for_sample(parsed_json_data):
    """Generates C++ code lines from parsed JSON data."""
    if not isinstance(parsed_json_data, dict):
        return []

    req_val = parsed_json_data.get("req") or parsed_json_data.get("cmd")
    if not req_val:
        # Cannot generate C++ if neither 'req' nor 'cmd' field is present
        return []

    cpp_lines = [f'J *req = NoteNewRequest("{req_val}");']

    for key, value in parsed_json_data.items():
        if key in ["req", "cmd"]:
            continue

        if isinstance(value, str):
            # Escape double quotes within the string value for C++
            escaped_value = value.replace('"', '\\"')
            cpp_lines.append(f'JAddStringToObject(req, "{key}", "{escaped_value}");')
        elif isinstance(value, bool):
            cpp_lines.append(f'JAddBoolToObject(req, "{key}", {"true" if value else "false"});')
        elif isinstance(value, (int, float)):
            cpp_lines.append(f'JAddNumberToObject(req, "{key}", {value});')
        elif isinstance(value, list):
            # Handle arrays
            cpp_lines.append(f'J *{key} = JAddArrayToObject(req, "{key}");')
            for item in value:
                if isinstance(item, str):
                    cpp_lines.append(f'JAddItemToArray({key}, JCreateString("{item}"));')
                elif isinstance(item, (int, float)):
                    cpp_lines.append(f'JAddItemToArray({key}, JCreateNumber({item}));')
                elif isinstance(item, bool):
                    cpp_lines.append(f'JAddItemToArray({key}, JCreateBool({"true" if item else "false"}));')

    cpp_lines.append("")
    cpp_lines.append("NoteRequest(req);")
    return cpp_lines

def generate_python_for_sample(parsed_json_data):
    """Generates Python code lines from parsed JSON data."""
    if not isinstance(parsed_json_data, dict):
        return []
    req_val = parsed_json_data.get("req") or parsed_json_data.get("cmd")
    if not req_val: return []

    # Start with the base request dictionary initialization
    if "cmd" in parsed_json_data:
        python_lines = [f'req = {{"cmd": "{req_val}"}}']
    else:
        python_lines = [f'req = {{"req": "{req_val}"}}']

    for key, value in parsed_json_data.items():
        if key in ["req", "cmd"]:
            continue

        if isinstance(value, str):
            # Python string literals handle internal quotes automatically if the outer quotes differ,
            # or use triple quotes. For simplicity, we'll rely on standard string repr.
            # json.dumps can be good for ensuring valid Python string literal for the value.
            python_lines.append(f'req["{key}"] = {json.dumps(value)}')
        elif isinstance(value, bool): # Must check bool before int, as bool is a subclass of int
            python_lines.append(f'req["{key}"] = {True if value else False}')
        elif isinstance(value, (int, float)):
            python_lines.append(f'req["{key}"] = {value}')
        elif isinstance(value, list):
            # Handle arrays
            python_lines.append(f'req["{key}"] = {json.dumps(value)}')

    if "cmd" in parsed_json_data:
        python_lines.append("card.Transaction(req)")
    else:
        python_lines.append("rsp = card.Transaction(req)")
    return python_lines

def generate_examples_mdx(samples):
    """Generates MDX for code samples, including C++ and Python if possible."""
    if not samples:
        return ""

    num_samples = len(samples)
    all_individual_code_tabs_blocks_mdx = []

    for sample_obj in samples:
        description = sample_obj.get("description", "Example")
        json_sample_str = sample_obj.get("json", "{}")

        formatted_json_block = ""
        cpp_code_lines = []
        python_code_lines = []

        try:
            parsed_json_data = json.loads(json_sample_str)
            formatted_json_sample = json.dumps(parsed_json_data, indent=2)
            formatted_json_block = f"```json\n{formatted_json_sample}\n```"
            cpp_code_lines = generate_cpp_for_sample(parsed_json_data)
            python_code_lines = generate_python_for_sample(parsed_json_data)
        except json.JSONDecodeError:
            # If JSON is invalid, still show it as a raw string in the JSON block
            formatted_json_block = f"```json\n{json_sample_str}\n```"
            # Cannot generate C++ for invalid JSON

        code_tabs_inner_content_parts = [formatted_json_block]
        if cpp_code_lines:
            cpp_block = "```cpp\n" + "\n".join(cpp_code_lines) + "\n```"
            code_tabs_inner_content_parts.append(cpp_block)
        if python_code_lines:
            python_block = "```python\n" + "\n".join(python_code_lines) + "\n```"
            code_tabs_inner_content_parts.append(python_block)

        tabs_inner_mdx = "\n\n".join(filter(None, code_tabs_inner_content_parts))

        if num_samples == 1:
            # Single sample: <CodeTabs> without exampleRequestTitle
            individual_code_tabs_block = f"<CodeTabs>\n{tabs_inner_mdx}\n</CodeTabs>"
        else:
            # Multiple samples: <CodeTabs> with exampleRequestTitle
            escaped_description = html.escape(description, quote=True)
            individual_code_tabs_block = f'<CodeTabs exampleRequestTitle="{escaped_description}">\n{tabs_inner_mdx}\n</CodeTabs>'

        all_individual_code_tabs_blocks_mdx.append(individual_code_tabs_block)

    if not all_individual_code_tabs_blocks_mdx:
        return ""

    joined_code_tabs_blocks = "\n\n".join(all_individual_code_tabs_blocks_mdx)

    return f"""<ExampleRequests>

{joined_code_tabs_blocks}

</ExampleRequests>"""

def generate_response_members_mdx(properties, response_schema_data):
    """Generates MDX for response schema properties, always including wrapper tags."""
    members_list_strings = []
    if properties:
        for prop_name, prop_details in properties.items():
            prop_type = prop_details.get("type", "N/A")
            type_display = f"_{prop_type}_"
            if prop_details.get("format"):
                type_display = f"_{prop_type} (format: {prop_details.get('format')})_"
            elif prop_details.get("contentEncoding"):
                type_display = f"_{prop_details.get('contentEncoding')} string_"
            elif prop_name == "time" and prop_type == "integer":
                type_display = "_UNIX Epoch time_"

            description = prop_details.get("description", "No description.")

            # Handle special formatting for files property with sub-descriptions
            if prop_name == "files" and "sub-descriptions" in prop_details:
                sub_desc_content = generate_response_sub_descriptions(prop_details["sub-descriptions"])
                members_list_strings.append(f"### `{prop_name}`\n\n{type_display}\n\n{description}\n\n{sub_desc_content}")
            else:
                members_list_strings.append(f"### `{prop_name}`\n\n{type_display}\n\n{description}")

    content = "\n\n".join(members_list_strings)
    if content:
      content = f"\n\n{content}\n\n"
    else:
      content = "\n\n"

    return f"""<ResponseMembers>{content}</ResponseMembers>"""

def generate_response_sub_descriptions(sub_descriptions):
    """Generate formatted sub-descriptions for response properties."""
    sub_desc_parts = []

    for sub_desc in sub_descriptions:
        const_value = sub_desc.get("const", "")
        sub_desc_parts.append(f'`"{const_value}"`')

    return "\n\n".join(sub_desc_parts)

def generate_annotations_mdx(annotations):
    """Generate MDX for schema annotations (notes, warnings, etc.)."""
    if not annotations:
        return ""
    
    annotation_blocks = []
    
    for annotation in annotations:
        title = annotation.get("title", "note")
        description = annotation.get("description", "")
        
        # Map annotation titles to MDX components
        if title.lower() == "note":
            component = "Note"
        elif title.lower() == "info":
            component = "Note"  # Info also uses Note component
        elif title.lower() == "warning":
            component = "Warning"
        else:
            component = "Note"  # Default to Note for unknown types
        
        annotation_blocks.append(f"<{component}>\n\n{description}\n\n</{component}>")
    
    return "\n\n".join(annotation_blocks)

def generate_example_response_mdx(samples):
    """Generates MDX for example response only if samples exist."""
    if not samples:
        return ""

    content = ""
    sample = samples[0]
    json_sample_str = sample.get("json", "{}")
    try:
        parsed_json = json.loads(json_sample_str)
        formatted_json_sample = json.dumps(parsed_json, indent=2)
        content = f"\n```json\n{formatted_json_sample}\n```\n"
    except json.JSONDecodeError:
        content = f"\n```json\n{json_sample_str}\n```\n"

    return f"""<ExampleResponse>{content}</ExampleResponse>"""

def main():
    parser = argparse.ArgumentParser(description="Generate an MDX file from a Notecard API base name (e.g., card.contact).")
    parser.add_argument("api_base_name", help="Base name of the Notecard API (e.g., card.contact, hub.set).")
    parser.add_argument("--schema_dir", default=".", help="Directory where schema files are located. Defaults to current directory.")
    parser.add_argument("-o", "--output_dir", default="./docs", help="Directory to save the generated MDX file. Defaults to './docs/'.")

    args = parser.parse_args()

    api_base_name = args.api_base_name
    schema_dir = args.schema_dir
    output_dir = args.output_dir

    req_schema_filename = f"{api_base_name}.req.notecard.api.json"
    rsp_schema_filename = f"{api_base_name}.rsp.notecard.api.json"

    req_schema_path = os.path.join(schema_dir, req_schema_filename)
    rsp_schema_path = os.path.join(schema_dir, rsp_schema_filename)

    if not os.path.isfile(req_schema_path):
        print(f"Error: Request schema file not found at {req_schema_path}")
        return

    schema_data = None
    response_schema_data = None

    try:
        with open(req_schema_path, "r") as f:
            schema_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from request schema {req_schema_path}")
        return

    if os.path.isfile(rsp_schema_path):
        try:
            with open(rsp_schema_path, "r") as f:
                response_schema_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON from response schema {rsp_schema_path}. Response sections might be empty or based on defaults.")
    else:
        print(f"Info: Response schema file not found at {rsp_schema_path}. Response sections might be empty or based on defaults.")

    output_mdx_filename = f"{api_base_name}.mdx"
    output_mdx_path = os.path.join(output_dir, output_mdx_filename)

    os.makedirs(os.path.dirname(output_mdx_path), exist_ok=True)

    mdx_output = generate_mdx_content(schema_data, api_base_name, response_schema_data)

    with open(output_mdx_path, "w") as f:
        f.write(mdx_output.strip())
    with open(output_mdx_path, "a") as f:
        f.write("\n")
    print(f"MDX file generated at {output_mdx_path}")

if __name__ == "__main__":
    main()
    print("Script finished.")
