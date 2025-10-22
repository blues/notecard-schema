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

def generate_version_check_wrapper(content, min_api_version, include_note=False):
    """Wrap content in VersionCheck tags if minApiVersion is present."""
    if not min_api_version:
        return content

    # Convert version format from X.Y.Z to X-Y-Z
    version = min_api_version.replace('.', '-')

    if include_note:
        opening_tag = f'<VersionCheck pageProps={{props}} version="{version}" includeNote={{true}}>'
    else:
        opening_tag = f'<VersionCheck pageProps={{props}} version="{version}">'

    return f"{opening_tag}\n\n{content}\n\n</VersionCheck>"

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

    # Check for top-level minApiVersion in both request and response schemas
    req_min_version = schema_data.get("minApiVersion")
    rsp_min_version = effective_response_schema_data.get("minApiVersion")

    # Use the higher version if both exist, or whichever exists
    top_level_version = None
    if req_min_version and rsp_min_version:
        # Compare versions and use the higher one
        req_parts = [int(x) for x in req_min_version.split('.')]
        rsp_parts = [int(x) for x in rsp_min_version.split('.')]
        top_level_version = req_min_version if req_parts >= rsp_parts else rsp_min_version
    elif req_min_version:
        top_level_version = req_min_version
    elif rsp_min_version:
        top_level_version = rsp_min_version

    # If there's a top-level version, wrap everything except the title
    if top_level_version:
        content_parts = [
            description,
            annotations_block,
            "<Arguments>",
            arguments_mdx_content,
            "</Arguments>",
            example_requests_block,
            response_members_block,
            example_response_block
        ]
        content_without_title = "\n\n".join(filter(None, content_parts))
        wrapped_content = generate_version_check_wrapper(content_without_title, top_level_version, include_note=True)
        mdx_parts = [title, wrapped_content]
    else:
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

        prop_type_raw = prop_details.get("type", "N/A")

        # Handle multiple types (e.g. ["string", "object"] -> "string or object")
        if isinstance(prop_type_raw, list):
            prop_type = " or ".join(prop_type_raw)
        else:
            prop_type = prop_type_raw

        # Handle array types (e.g. array with items -> "array of string" or "array of string, integer")
        if prop_type == "array" and "items" in prop_details:
            items = prop_details["items"]
            if "type" in items:
                item_type = items["type"]
                if isinstance(item_type, list):
                    # Multiple item types: "array of string, integer"
                    prop_type = f"array of {', '.join(item_type)}"
                else:
                    # Single item type: "array of string"
                    prop_type = f"array of {item_type}"

        optional_tag = " (optional)"
        if prop_name in top_level_required:
            optional_tag = ""

        # Add default value if present
        default_value = prop_details.get("default")
        if default_value is not None:
            # Format all default values with backticks
            if isinstance(default_value, bool):
                # Use lowercase boolean values in backticks
                formatted_default = f"`{str(default_value).lower()}`"
            elif isinstance(default_value, str):
                formatted_default = f"`{default_value}`"
            else:
                # All other types (int, float, etc.) in backticks
                formatted_default = f"`{str(default_value)}`"

            if optional_tag:
                # Replace " (optional)" with " (optional, default X)"
                optional_tag = f" (optional, default {formatted_default})"
            else:
                # Add default to required field
                optional_tag = f" (default {formatted_default})"

        type_display = f"_{prop_type}{optional_tag}_"
        if prop_details.get("format"):
            type_display = f"_{prop_type} (format: {prop_details.get('format')}){optional_tag}_"
        elif prop_name == "time" and prop_type == "integer":
            type_display = f"_UNIX Epoch time{optional_tag}_"
        elif "const" in prop_details and prop_type == "N/A":
            # Only show const when there's no explicit type
            type_display = f"_const (value: `{prop_details['const']}`){optional_tag}_"

        description = prop_details.get("description", "No description.")

        # Generate SKU badges for individual parameters
        param_skus = prop_details.get("skus", [])
        param_badges = generate_argument_badges(param_skus) if param_skus else ""

        # Generate deprecated badge if property is deprecated
        deprecated_badge = ""
        if prop_details.get("deprecated", False):
            deprecated_badge = '<Badge type="deprecated" usage="argument" />'

        # Create badges paragraph if any badges exist
        badges_para = ""
        all_badges = []
        if param_badges:
            # Add &nbsp; between individual SKU badges for proper spacing
            badges_with_spacing = param_badges.replace('"/>', '"/>&nbsp;')
            # Remove trailing &nbsp; if it exists
            badges_with_spacing = badges_with_spacing.rstrip('&nbsp;')
            all_badges.append(badges_with_spacing)
        if deprecated_badge:
            all_badges.append(deprecated_badge)

        if all_badges:
            # Join all badge groups with &nbsp; spacing
            badges_combined = "&nbsp;".join(all_badges)
            badges_para = f"\n\n<p>{badges_combined}</p>"

        # Handle parameters with sub-descriptions
        if "sub-descriptions" in prop_details:
            sub_desc_content = generate_mode_sub_descriptions(prop_details["sub-descriptions"])
            param_content = f"### `{prop_name}`\n\n{type_display}{badges_para}\n\n{description}\n\n{sub_desc_content}"
        # Handle array parameters with sub-descriptions in items
        elif prop_type == "array" and "items" in prop_details and "sub-descriptions" in prop_details["items"]:
            sub_desc_content = generate_mode_sub_descriptions(prop_details["items"]["sub-descriptions"])
            param_content = f"### `{prop_name}`\n\n{type_display}{badges_para}\n\n{description}\n\n{sub_desc_content}"
        else:
            param_content = f"### `{prop_name}`\n\n{type_display}{badges_para}\n\n{description}"

        # Check if this property has minApiVersion and wrap it if so
        prop_min_version = prop_details.get("minApiVersion")
        if prop_min_version:
            param_content = generate_version_check_wrapper(param_content, prop_min_version)

        args_list.append(param_content)

    return "\n\n".join(args_list)

def generate_mode_sub_descriptions(sub_descriptions):
    """Generate formatted sub-descriptions for mode parameter."""
    sub_desc_parts = []

    for sub_desc in sub_descriptions:
        const_value = sub_desc.get("const")
        pattern_value = sub_desc.get("pattern")
        description = sub_desc.get("description", "")
        skus = sub_desc.get("skus", [])
        min_version = sub_desc.get("minApiVersion")
        is_deprecated = sub_desc.get("deprecated", False)

        # Skip sub-descriptions that have pattern fields - these are handled differently in the main description
        if pattern_value and not const_value:
            continue

        # Skip if we don't have a const value to display
        if const_value is None:
            continue

        badges = generate_argument_badges(skus)

        # Add deprecated badge if this sub-description is deprecated
        if is_deprecated:
            deprecated_badge = '<Badge type="deprecated" usage="argument" />'
            if badges:
                badges = badges + deprecated_badge
            else:
                badges = deprecated_badge

        # Handle special formatting for different types
        if const_value == "":
            const_display = '`""`'
        elif isinstance(const_value, (int, float)):
            # Numeric values don't need quotes
            const_display = f'`{const_value}`'
        else:
            # String values need quotes
            const_display = f'`"{const_value}"`'

        if badges:
            sub_desc_content = f"{const_display} {badges}\n\n{description}"
        else:
            sub_desc_content = f"{const_display}: {description}"

        # Wrap with VersionCheck if minApiVersion exists
        if min_version:
            sub_desc_content = generate_version_check_wrapper(sub_desc_content, min_version)

        sub_desc_parts.append(sub_desc_content)

    return "\n\n".join(sub_desc_parts)

def generate_cpp_for_sample(parsed_json_data_list):
    """Generates C++ code lines from a list of parsed JSON data objects."""
    if not isinstance(parsed_json_data_list, list):
        return []

    all_cpp_lines = []

    for i, parsed_json_data in enumerate(parsed_json_data_list):
        if not isinstance(parsed_json_data, dict):
            continue

        req_val = parsed_json_data.get("req") or parsed_json_data.get("cmd")
        if not req_val:
            # Cannot generate C++ if neither 'req' nor 'cmd' field is present
            continue

        if i == 0:
            cpp_lines = [f'J *req = NoteNewRequest("{req_val}");']
        else:
            cpp_lines = [f'req = NoteNewRequest("{req_val}");']

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
            elif isinstance(value, dict):
                # Handle objects
                cpp_lines.append(f'J *{key} = JAddObjectToObject(req, "{key}");')
                for obj_key, obj_value in value.items():
                    if isinstance(obj_value, str):
                        escaped_obj_value = obj_value.replace('"', '\\"')
                        cpp_lines.append(f'JAddStringToObject({key}, "{obj_key}", "{escaped_obj_value}");')
                    elif isinstance(obj_value, bool):
                        cpp_lines.append(f'JAddBoolToObject({key}, "{obj_key}", {"true" if obj_value else "false"});')
                    elif isinstance(obj_value, (int, float)):
                        cpp_lines.append(f'JAddNumberToObject({key}, "{obj_key}", {obj_value});')
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

        # Add separator between multiple requests except for the last one
        if i < len(parsed_json_data_list) - 1:
            cpp_lines.append("")

        all_cpp_lines.extend(cpp_lines)

    return all_cpp_lines

def generate_python_for_sample(parsed_json_data_list):
    """Generates Python code lines from a list of parsed JSON data objects."""
    if not isinstance(parsed_json_data_list, list):
        return []

    all_python_lines = []

    for i, parsed_json_data in enumerate(parsed_json_data_list):
        if not isinstance(parsed_json_data, dict):
            continue

        req_val = parsed_json_data.get("req") or parsed_json_data.get("cmd")
        if not req_val:
            continue

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
            elif isinstance(value, dict):
                # Handle objects
                python_lines.append(f'req["{key}"] = {json.dumps(value)}')
            elif isinstance(value, list):
                # Handle arrays
                python_lines.append(f'req["{key}"] = {json.dumps(value)}')

        if "cmd" in parsed_json_data:
            python_lines.append("card.Transaction(req)")
        else:
            python_lines.append("rsp = card.Transaction(req)")

        # Add separator between multiple requests except for the last one
        if i < len(parsed_json_data_list) - 1:
            python_lines.append("")

        all_python_lines.extend(python_lines)

    return all_python_lines

def parse_json_sample(json_string):
    """Parse JSON sample that can be a single object, array of objects, or comma-separated objects."""
    json_objects = []

    try:
        # First try to parse as valid JSON
        parsed = json.loads(json_string)

        if isinstance(parsed, list):
            # It's a JSON array - return the objects in the array
            json_objects = [obj for obj in parsed if isinstance(obj, dict)]
        elif isinstance(parsed, dict):
            # It's a single JSON object
            json_objects = [parsed]
    except json.JSONDecodeError:
        # Fallback: try to parse as comma-separated JSON objects (legacy format)
        parts = json_string.split("},{")

        if len(parts) > 1:
            # Multiple JSON objects (legacy comma-separated format)
            for i, part in enumerate(parts):
                # Add back the closing brace for all but the last part
                if i < len(parts) - 1:
                    part = part + "}"
                # Add back the opening brace for all but the first part
                if i > 0:
                    part = "{" + part

                try:
                    parsed = json.loads(part)
                    json_objects.append(parsed)
                except json.JSONDecodeError:
                    continue

    return json_objects

def format_json_objects_for_display(json_objects):
    """Format a list of JSON objects for display with proper spacing."""
    formatted_objects = []

    for json_obj in json_objects:
        formatted_json = json.dumps(json_obj, indent=2)
        formatted_objects.append(formatted_json)

    return "\n\n".join(formatted_objects)

def generate_examples_mdx(samples):
    """Generates MDX for code samples, including C++ and Python if possible."""
    if not samples:
        return ""

    num_samples = len(samples)
    all_individual_code_tabs_blocks_mdx = []

    for sample_obj in samples:
        title = sample_obj.get("title", "Example")
        description = sample_obj.get("description", "")
        json_sample_str = sample_obj.get("json", "{}")

        formatted_json_block = ""
        cpp_code_lines = []
        python_code_lines = []

        # Parse JSON sample (single object, array of objects, or legacy comma-separated)
        parsed_json_objects = parse_json_sample(json_sample_str)

        if parsed_json_objects:
            # Format the JSON objects for display
            formatted_json_sample = format_json_objects_for_display(parsed_json_objects)
            formatted_json_block = f"```json\n{formatted_json_sample}\n```"

            # Generate code for all JSON objects
            cpp_code_lines = generate_cpp_for_sample(parsed_json_objects)
            python_code_lines = generate_python_for_sample(parsed_json_objects)
        else:
            # If JSON parsing fails, still show it as a raw string in the JSON block
            formatted_json_block = f"```json\n{json_sample_str}\n```"
            # Cannot generate C++ or Python for invalid JSON

        code_tabs_inner_content_parts = [formatted_json_block]
        if cpp_code_lines:
            cpp_block = "```cpp\n" + "\n".join(cpp_code_lines) + "\n```"
            code_tabs_inner_content_parts.append(cpp_block)
        if python_code_lines:
            python_block = "```python\n" + "\n".join(python_code_lines) + "\n```"
            code_tabs_inner_content_parts.append(python_block)

        tabs_inner_mdx = "\n\n".join(filter(None, code_tabs_inner_content_parts))

        # Add description after the code blocks if it exists
        if description:
            tabs_inner_mdx += f"\n\n{description}"

        if num_samples == 1:
            # Single sample: <CodeTabs> without exampleRequestTitle
            individual_code_tabs_block = f"<CodeTabs>\n{tabs_inner_mdx}\n</CodeTabs>"
        else:
            # Multiple samples: <CodeTabs> with exampleRequestTitle
            escaped_title = html.escape(title, quote=True)
            individual_code_tabs_block = f'<CodeTabs exampleRequestTitle="{escaped_title}">\n{tabs_inner_mdx}\n</CodeTabs>'

        all_individual_code_tabs_blocks_mdx.append(individual_code_tabs_block)

    if not all_individual_code_tabs_blocks_mdx:
        return ""

    joined_code_tabs_blocks = "\n\n".join(all_individual_code_tabs_blocks_mdx)

    return f"""<ExampleRequests>

{joined_code_tabs_blocks}

</ExampleRequests>"""

def generate_response_members_mdx(properties, schema_data=None):
    """Generates MDX for response schema properties, always including wrapper tags."""
    members_list_strings = []
    if properties:
        for prop_name, prop_details in properties.items():
            prop_type_raw = prop_details.get("type", "N/A")

            # Handle multiple types (e.g. ["string", "object"] -> "string or object")
            if isinstance(prop_type_raw, list):
                prop_type = " or ".join(prop_type_raw)
            else:
                prop_type = prop_type_raw

            # Handle array types (e.g. array with items -> "array of string" or "array of string, integer")
            if prop_type == "array" and "items" in prop_details:
                items = prop_details["items"]
                if "type" in items:
                    item_type = items["type"]
                    if isinstance(item_type, list):
                        # Multiple item types: "array of string, integer"
                        prop_type = f"array of {', '.join(item_type)}"
                    else:
                        # Single item type: "array of string"
                        prop_type = f"array of {item_type}"
            type_display = f"_{prop_type}_"
            if prop_details.get("format"):
                type_display = f"_{prop_type} (format: {prop_details.get('format')})_"
            elif prop_details.get("contentEncoding"):
                type_display = f"_{prop_details.get('contentEncoding')} string_"
            elif prop_name == "time" and prop_type == "integer":
                type_display = "_UNIX Epoch time_"

            description = prop_details.get("description", "No description.")

            # Handle sub-descriptions for any property
            if "sub-descriptions" in prop_details:
                sub_desc_content = generate_mode_sub_descriptions(prop_details["sub-descriptions"])
                member_content = f"### `{prop_name}`\n\n{type_display}\n\n{description}\n\n{sub_desc_content}"
            else:
                member_content = f"### `{prop_name}`\n\n{type_display}\n\n{description}"

            # Check if this property has minApiVersion and wrap it if so
            prop_min_version = prop_details.get("minApiVersion")
            if prop_min_version:
                member_content = generate_version_check_wrapper(member_content, prop_min_version)

            members_list_strings.append(member_content)

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
        elif title.lower() == "deprecated":
            component = "Deprecated"
        else:
            component = "Note"  # Default to Note for unknown types

        annotation_blocks.append(f"<{component}>\n\n{description}\n\n</{component}>")

    return "\n\n".join(annotation_blocks)

def generate_example_response_mdx(samples):
    """Generates MDX for example response samples in simple format."""
    if not samples:
        return ""

    num_samples = len(samples)
    sample_blocks = []

    for sample_obj in samples:
        description = sample_obj.get("description", "")
        json_sample_str = sample_obj.get("json", "{}")

        # Format JSON for display
        try:
            parsed_json = json.loads(json_sample_str)
            formatted_json_sample = json.dumps(parsed_json, indent=2)
            formatted_json_block = f"```json\n{formatted_json_sample}\n```"
        except json.JSONDecodeError:
            formatted_json_block = f"```json\n{json_sample_str}\n```"

        # Create sample block with JSON and description (only for multiple samples)
        sample_block = formatted_json_block
        if description and num_samples > 1:
            sample_block += f"\n\n{description}"

        sample_blocks.append(sample_block)

    if not sample_blocks:
        return ""

    joined_samples = "\n\n".join(sample_blocks)

    return f"""<ExampleResponse>

{joined_samples}

</ExampleResponse>"""

def find_all_api_base_names(schema_dir):
    """Find all API base names by looking for .req.notecard.api.json files."""
    api_base_names = []

    # Look for all .req.notecard.api.json files
    for filename in os.listdir(schema_dir):
        if filename.endswith('.req.notecard.api.json'):
            # Extract the API base name (everything before .req.notecard.api.json)
            api_base_name = filename.replace('.req.notecard.api.json', '')
            api_base_names.append(api_base_name)

    return sorted(api_base_names)

def get_category_name(api_base_name):
    """Get the category name and order number for an API."""
    category_mapping = {
        'card': ('01 card Requests', 1),
        'dfu': ('02 dfu Requests', 2),
        'env': ('03 env Requests', 3),
        'file': ('04 file Requests', 4),
        'hub': ('05 hub Requests', 5),
        'note': ('06 note Requests', 6),
        'ntn': ('07 ntn Requests', 7),
        'var': ('08 var Requests', 8),
        'web': ('09 web Requests', 9)
    }

    # Extract category from API base name (e.g., 'card.attn' -> 'card')
    category = api_base_name.split('.')[0]
    return category_mapping.get(category, (f'{category} Requests', 99))

def get_api_order_number(api_base_name, all_apis_in_category):
    """Get a sequential order number for API within its category."""
    # Get all APIs in the same category
    category = api_base_name.split('.')[0]
    category_apis = [api for api in all_apis_in_category if api.startswith(category + '.') or api == category]

    # Sort APIs with special handling for bare category names
    def sort_key(api):
        parts = api.split('.')
        if len(parts) == 1:
            # Bare category API (like "web") - sort first with empty suffix
            return ("",)
        else:
            # Regular API (like "web.delete") - sort by suffix parts
            return tuple(parts[1:])

    category_apis.sort(key=sort_key)

    # Find the position of this API in the sorted list
    try:
        position = category_apis.index(api_base_name)
    except ValueError:
        position = 0

    # Generate sequential numbers: 00, 05, 10, 15, 20, etc.
    return position * 5

def generate_single_mdx(api_base_name, schema_dir, output_dir, tidy=False, all_apis=None):
    """Generate MDX for a single API."""
    req_schema_filename = f"{api_base_name}.req.notecard.api.json"
    rsp_schema_filename = f"{api_base_name}.rsp.notecard.api.json"

    req_schema_path = os.path.join(schema_dir, req_schema_filename)
    rsp_schema_path = os.path.join(schema_dir, rsp_schema_filename)

    if not os.path.isfile(req_schema_path):
        print(f"Error: Request schema file not found at {req_schema_path}")
        return False

    schema_data = None
    response_schema_data = None

    try:
        with open(req_schema_path, "r") as f:
            schema_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from request schema {req_schema_path}")
        return False

    if os.path.isfile(rsp_schema_path):
        try:
            with open(rsp_schema_path, "r") as f:
                response_schema_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON from response schema {rsp_schema_path}. Response sections might be empty or based on defaults.")
    else:
        print(f"Info: Response schema file not found at {rsp_schema_path}. Response sections might be empty or based on defaults.")

    if tidy:
        # Generate tidy directory structure
        category_name, _ = get_category_name(api_base_name)
        if all_apis is None:
            all_apis = [api_base_name]  # Fallback for single API generation
        api_order = get_api_order_number(api_base_name, all_apis)
        api_folder_name = f"{api_order:02d} {api_base_name}"

        output_mdx_path = os.path.join(output_dir, category_name, api_folder_name, "_main.mdx")
    else:
        # Original flat structure
        output_mdx_filename = f"{api_base_name}.mdx"
        output_mdx_path = os.path.join(output_dir, output_mdx_filename)

    os.makedirs(os.path.dirname(output_mdx_path), exist_ok=True)

    mdx_output = generate_mdx_content(schema_data, api_base_name, response_schema_data)

    with open(output_mdx_path, "w") as f:
        f.write(mdx_output.strip())
    with open(output_mdx_path, "a") as f:
        f.write("\n")
    print(f"MDX file generated at {output_mdx_path}")
    return True

def generate_category_main_mdx(category_name, category_apis, output_dir, prev_category=None, next_category=None):
    """Generate a category-level _main.mdx file that imports and renders all APIs in the category."""
    # Sort APIs to ensure consistent ordering
    category_apis.sort()

    # Create imports
    imports = []
    components = []

    for api_name in category_apis:
        api_order = get_api_order_number(api_name, category_apis)
        folder_name = f"{api_order:02d} {api_name}"
        component_name = f"S{api_order:02d}"

        imports.append(f'import {component_name} from "./{folder_name}/_main.mdx";')
        components.append(f'<{component_name} {{...props}} />')

    # Generate the complete file content
    imports_section = '\n'.join(imports)
    components_section = '\n'.join(components)

    # Extract the category name for the title (e.g., "01 card Requests" -> "card Requests")
    title = category_name.split(' ', 1)[1] if ' ' in category_name else category_name

    # Build navigation section
    navigation_section = ""

    # Add Previous tag
    if prev_category:
        prev_title = prev_category.split(' ', 1)[1] if ' ' in prev_category else prev_category
        # Convert category name to URL slug (lowercase, spaces to hyphens)
        prev_slug = prev_title.lower().replace(' ', '-')
        navigation_section += f"""<Previous
  title="{prev_title}"
  href="/api-reference/notecard-api/{prev_slug}"
/>"""
    else:
        # First category points to introduction
        navigation_section += """<Previous
  title="Introduction"
  href="/api-reference/notecard-api/introduction"
/>"""

    # Add Next tag
    if next_category:
        next_title = next_category.split(' ', 1)[1] if ' ' in next_category else next_category
        # Convert category name to URL slug (lowercase, spaces to hyphens)
        next_slug = next_title.lower().replace(' ', '-')
        navigation_section += f"""

<Next title="{next_title}" href="/api-reference/notecard-api/{next_slug}" />"""

    mdx_content = f"""{imports_section}

# {title}

{{props.urlConfig.description}}

<SlugPicker
  options={{props.allOptions}}
  config={{props.urlConfig}}
  text="Notecard Firmware Version:"
/>

{components_section}

{navigation_section}
"""

    # Write the category main file
    category_main_path = os.path.join(output_dir, category_name, "_main.mdx")
    os.makedirs(os.path.dirname(category_main_path), exist_ok=True)

    with open(category_main_path, "w") as f:
        f.write(mdx_content.strip())
    with open(category_main_path, "a") as f:
        f.write("\n")

    print(f"Category MDX file generated at {category_main_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate MDX file(s) from Notecard API schema(s).")
    parser.add_argument("api_base_name", nargs='?', help="Base name of the Notecard API (e.g., card.contact, hub.set). Not required when using --all.")
    parser.add_argument("--all", action="store_true", help="Generate MDX files for all APIs found in the schema directory.")
    parser.add_argument("--schema_dir", default=".", help="Directory where schema files are located. Defaults to current directory.")
    parser.add_argument("-o", "--output_dir", default="./docs", help="Directory to save the generated MDX file(s). Defaults to './docs/'.")
    parser.add_argument("--tidy", action="store_true", help="Generate files in organized directory structure with category folders and _main.mdx files (following blues.dev structure).")

    args = parser.parse_args()

    schema_dir = args.schema_dir
    output_dir = args.output_dir
    tidy = args.tidy

    if args.all:
        # Generate MDX files for all APIs
        api_base_names = find_all_api_base_names(schema_dir)
        if not api_base_names:
            print(f"No .req.notecard.api.json files found in {schema_dir}")
            return

        print(f"Found {len(api_base_names)} APIs: {', '.join(api_base_names)}")
        if tidy:
            print("Using tidy directory structure with category folders...")

        success_count = 0
        for api_base_name in api_base_names:
            print(f"\nGenerating MDX for {api_base_name}...")
            if generate_single_mdx(api_base_name, schema_dir, output_dir, tidy, api_base_names):
                success_count += 1

        print(f"\nCompleted: {success_count}/{len(api_base_names)} MDX files generated successfully.")

        # Generate category-level _main.mdx files if using tidy structure
        if tidy:
            print(f"\nGenerating category-level _main.mdx files...")
            categories = {}

            # Group APIs by category
            for api_name in api_base_names:
                category_name, _ = get_category_name(api_name)

                if category_name not in categories:
                    categories[category_name] = []
                categories[category_name].append(api_name)

            # Generate category files
            category_success = 0
            # Sort categories by their numerical prefix to ensure correct ordering
            category_items = sorted(categories.items(), key=lambda x: x[0])

            for i, (category_name, category_apis) in enumerate(category_items):
                # Determine previous and next categories
                prev_category = category_items[i-1][0] if i > 0 else None
                next_category = category_items[i+1][0] if i < len(category_items) - 1 else None

                print(f"Generating category file for {category_name}...")
                if generate_category_main_mdx(category_name, category_apis, output_dir, prev_category, next_category):
                    category_success += 1

            print(f"Generated {category_success}/{len(categories)} category files successfully.")
    else:
        # Generate MDX for single API
        if not args.api_base_name:
            print("Error: api_base_name is required when --all is not specified.")
            parser.print_help()
            return

        if tidy:
            print("Error: --tidy option only supports --all flag. Use --all --tidy to generate all APIs in tidy structure.")
            return

        generate_single_mdx(args.api_base_name, schema_dir, output_dir, tidy)

if __name__ == "__main__":
    main()
    print("Script finished.")
