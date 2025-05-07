import json
import os
import argparse
import html

def generate_mdx_content(schema_data, api_base_name, response_schema_data=None):
    """Generates an MDX string from the JSON schema, optionally including response info."""

    req_cmd_value = api_base_name
    if schema_data.get("properties"):
        if schema_data["properties"].get("req") and schema_data["properties"]["req"].get("const"):
            req_cmd_value = schema_data["properties"]["req"]["const"]
        elif schema_data["properties"].get("cmd") and schema_data["properties"].get("cmd").get("const"):
            req_cmd_value = schema_data["properties"]["cmd"]["const"]

    title = f"## {req_cmd_value}"
    description = schema_data.get("description", "")

    arguments_mdx_content = generate_arguments_mdx(schema_data.get("properties", {}))
    example_requests_block = generate_examples_mdx(schema_data.get("samples", []))

    # Prepare data for response sections, ensuring defaults if response_schema_data is None or incomplete
    effective_response_schema_data = response_schema_data if response_schema_data is not None else {}
    response_properties = effective_response_schema_data.get("properties", {})
    response_samples = effective_response_schema_data.get("samples", [])

    # generate_response_members_mdx always returns the block
    response_members_block = generate_response_members_mdx(response_properties)
    # generate_example_response_mdx returns block only if samples exist
    example_response_block = generate_example_response_mdx(response_samples)

    mdx_parts = [
        title,
        description,
        "<Arguments>",
        arguments_mdx_content,
        "</Arguments>",
        example_requests_block,
        response_members_block,
        example_response_block
    ]

    return "\n\n".join(filter(None, mdx_parts))

def generate_arguments_mdx(properties):
    """Generates MDX for schema properties (arguments). Content only."""
    if not properties:
        return ""
    args_list = []
    top_level_required = properties.get("required", [])
    for prop_name, prop_details in properties.items():
        if prop_name in ["req", "cmd", "required"]:
            continue
        prop_type = prop_details.get("type", "N/A")
        optional_tag = "(optional)"
        if isinstance(top_level_required, list) and prop_name in top_level_required:
             optional_tag = "(required)"
        elif isinstance(properties.get("oneOf"), list):
            pass
        type_display = f"_{prop_type} {optional_tag}_"
        if prop_details.get("format"):
            type_display = f"_{prop_type} (format: {prop_details.get('format')}) {optional_tag}_"
        elif "const" in prop_details:
            type_display = f"_const (value: `{prop_details["const"]}`) {optional_tag}_"
        description = prop_details.get("description", "No description.")
        args_list.append(f"### `{prop_name}`\n\n{type_display}\n\n{description}")
    return "\n\n".join(args_list)

def generate_cpp_for_sample(parsed_json_data):
    """Generates C++ code lines from parsed JSON data."""
    if not isinstance(parsed_json_data, dict):
        return []

    req_val = parsed_json_data.get("req")
    if not req_val:
        # Cannot generate C++ if the 'req' field is missing, as it's fundamental
        # for NoteNewRequest.
        return []

    cpp_lines = [f'J *req = NoteNewRequest("{req_val}");']

    for key, value in parsed_json_data.items():
        if key == "req":
            continue

        if isinstance(value, str):
            # Escape double quotes within the string value for C++
            escaped_value = value.replace('"', '\\"')
            cpp_lines.append(f'JAddStringToObject(req, "{key}", "{escaped_value}");')
        elif isinstance(value, (int, float)):
            cpp_lines.append(f'JAddNumberToObject(req, "{key}", {value});')
        elif isinstance(value, bool):
            cpp_lines.append(f'JAddBoolToObject(req, "{key}", {"true" if value else "false"});')

    cpp_lines.append("")
    cpp_lines.append("NoteRequest(req);");
    return cpp_lines

def generate_python_for_sample(parsed_json_data):
    """Generates Python code lines from parsed JSON data."""
    if not isinstance(parsed_json_data, dict):
        return []
    req_val = parsed_json_data.get("req")
    if not req_val: return []

    # Start with the base request dictionary initialization
    python_lines = [f'req = {{"req": "{req_val}"}}']

    for key, value in parsed_json_data.items():
        if key == "req":
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
        # Arrays and nested objects are not handled for Python generation in this simplified version

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

def generate_response_members_mdx(properties):
    """Generates MDX for response schema properties, always including wrapper tags."""
    members_list_strings = []
    if properties:
        for prop_name, prop_details in properties.items():
            prop_type = prop_details.get("type", "N/A")
            type_display = f"_{prop_type}_"
            if prop_details.get("format"):
                type_display = f"_{prop_type} (format: {prop_details.get('format')})_"
            description = prop_details.get("description", "No description.")
            members_list_strings.append(f"### `{prop_name}`\n\n{type_display}\n\n{description}")

    content = "\n\n".join(members_list_strings)
    if content:
      content = f"\n{content}\n"
    else:
      content = "\n"

    return f"""<ResponseMembers>{content}</ResponseMembers>"""

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
    parser.add_argument("-o", "--output_dir", default="./.docs", help="Directory to save the generated MDX file. Defaults to './docs/'.")

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