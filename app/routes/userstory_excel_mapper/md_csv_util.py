# -*- coding: utf-8 -*-
import csv
import logging
import re
from io import StringIO
from typing import Dict, List

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def process_content_into_csv(all_responses: List[Dict], config: Dict, inputType: str) -> str:
    """The response generated from the assistant_executor is then parsed and processed into
    csv content which can be used to generate xlsx. For this the functions in md_csv_util.py
    are used.
    """
    contentToBeFormatted = [
        response_dict.message
        for response_item in (all_responses or [])
        for response_dict in (response_item.response or [])
    ]

    # TODO: Revisit the headers in config.json to make it more generic and user friendly
    requiredHeaders = config[inputType]["headers"]
    section_to_header_mapping = config[inputType]["section_to_header_mapping"]

    parsedInputText = parse_content(contentToBeFormatted, requiredHeaders, section_to_header_mapping)

    csv_formatted_result = prepare_csv_data(parsedInputText, requiredHeaders)

    updated_csv = add_issue_type_column(csv_formatted_result, "Story")

    return convert_to_csv_string(updated_csv)


def parse_content(content_list, headers, section_to_header_mapping):
    """
    Parses content to map sections to their corresponding headers. Subheadings are included
    only in the "Acceptance Criteria" column.
    Args:
        content_list : A list of strings, where each string represents a piece of content (like a user story or a test case)
                       that needs to be parsed and organized.
        headers: A list of headers or column names that define how the parsed content should be organized
                (e.g., "User Story," "Classification," "Acceptance Criteria").
        section_to_header_mapping: A dictionary mapping specific sections (like "User Story," "Classification") to their
                                   corresponding headers in the output.
    """
    parsed_stories = []

    for story in content_list:
        # Initialize a dictionary to hold each header's content
        content_dict = {header: "" for header in headers}

        # Split the story into sections based on the markdown headers
        sections = re.split(r"\*\*(.+?)\*\*", story)

        for i in range(1, len(sections), 2):
            section_title = sections[i].strip().rstrip(":")
            section_content = sections[i + 1].strip() if (i + 1) < len(sections) else ""

            # Determine which header this section should map to
            mapped_header = section_to_header_mapping.get(section_title)

            if mapped_header:
                if mapped_header == "Acceptance Criteria":
                    # Include subheading in "Acceptance Criteria" column
                    existing_content = content_dict.get(mapped_header, "")
                    if existing_content:
                        content_dict[mapped_header] += f"\n\n{section_title}:\n{section_content}"
                    else:
                        content_dict[mapped_header] = f"{section_title}:\n{section_content}"
                else:
                    # For other columns, only include content without subheading
                    existing_content = content_dict.get(mapped_header, "")
                    if existing_content:
                        content_dict[mapped_header] += f"\n\n{section_content}"
                    else:
                        content_dict[mapped_header] = section_content
            else:
                log.warning(f"Section '{section_title}' not found in mapping. Skipping.")

        # Strip any leading/trailing whitespace from the sections
        for key in content_dict:
            content_dict[key] = content_dict[key].strip()

        parsed_stories.append(content_dict)

    return parsed_stories


def prepare_csv_data(parsed_list, headers):
    """
    The prepare_csv_data function is responsible for converting the structured data (produced by parse_content)
    into a format that is ready to be written to a CSV file. The main purpose of prepare_csv_data is to take the
    parsed and structured content (a list of dictionaries, where each dictionary represents a row of data) and
    convert it into a format suitable for CSV generation. This involves ensuring that each row is properly aligned
    with the headers, and any necessary formatting (like joining content from different sections) is applied.

    Args:
        parsed_list : A list of dictionaries where each dictionary contains the parsed content for a user story or test case.
                      The keys in the dictionary correspond to the headers (like "User Story," "Classification," "Acceptance Criteria"),
                      and the values contain the associated content.
        headers: A list of strings that represent the column names or headers for the CSV file. These headers dictate the order
                 and structure of the content in the CSV file.

    """
    # Initialize the CSV data with headers
    csv_data = [headers]

    for item in parsed_list:
        row = []
        for header in headers:
            value = item.get(header, "")
            # Ensure value is properly quoted to handle commas, newlines, etc.
            row.append(f'{value}')
        csv_data.append(row)

    return csv_data


def add_issue_type_column(csv_data, issueType):
    """
    This function is used to add the "Issue Type" as the first column in the excel and add a static
    value "issueType" as its content
    """
    issue_type_column = "Issue Type"
    issue_type_value = issueType

    # Add the "Issue Type" column to the headers
    csv_data[0] = [issue_type_column] + csv_data[0]

    # Add "Story" to each row
    for i in range(1, len(csv_data)):
        csv_data[i] = [issue_type_value] + csv_data[i]

    return csv_data


def convert_to_csv_string(data):
    """
    The primary purpose of convert_to_csv_string is to transform the row-based data structure
    (generated prepare_csv_data) into a single string formatted according to the CSV standard.
    The string generated in this function is then passed to xlsx_builder as an input.
    """
    output = StringIO()
    csv_writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerows(data)
    return output.getvalue()
