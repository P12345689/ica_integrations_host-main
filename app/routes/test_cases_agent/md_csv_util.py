# -*- coding: utf-8 -*-
import csv
import logging
import re
from io import StringIO
from typing import Dict, List

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def process_content_into_csv(all_responses: List[Dict], config: Dict) -> str:
    """The response generated from the assistant_executor is then parsed and processed into
    csv content which can be used to generate xlsx. For this the functions in md_csv_util.py
    are used.
    """
 
    contentToBeFormatted = [
        response_dict.message
        for response_item in all_responses
        for response_dict in response_item.response
    ]

    requiredHeaders = config["headers"]
    section_to_header_mapping = config["section_to_header_mapping"]
    skip_sections = config["skip_sections"]

    parsedInputText = parse_content(contentToBeFormatted, requiredHeaders, section_to_header_mapping, skip_sections)

    csv_formatted_result = prepare_csv_data(parsedInputText, requiredHeaders)

    updated_csv = add_issue_type_column(csv_formatted_result, "Test Case")

    return convert_to_csv_string(updated_csv)


def parse_content(content_list, headers, section_to_header_mapping, skip_sections):
    """
    Parses content to map sections to their corresponding headers. Subheadings are included
    only in the "Description" column.
    Args:
        content_list : A list of strings, where each string represents a piece of content (multiple test 
                       cases for a single user story) that needs to be parsed and organized.                       
        headers: A list of headers or column names that define how the parsed content should be organized
                (e.g., "Description," "Summary," "Issue Type").
        section_to_header_mapping: A dictionary mapping specific sections (like "Precondition," "Test Steps") to their
                                   corresponding headers in the output.
    """
    parsed_testcases = []
    
    # Iterate through each content block; 
    for content in content_list:
        # Split the multiple test cases into individual test cases based on the test case title pattern (e.g., **Test Case**)
        test_cases = re.split(r"(?=\*\*Test Case)", content)

        for case in test_cases:
            if case.strip() == "":
                continue

            # Initialize a dictionary to hold each header's content
            content_dict = {header: "" for header in headers}

            # Split the test case into sections based on the markdown headers
            sections = re.split(r"\*\*(.+?)\*\*", case)
            
            for i in range(1, len(sections), 2):
                section_title = sections[i].strip().rstrip(":")
                section_content = sections[i + 1].strip() if (i + 1) < len(sections) else ""
                section_content = re.sub(r'\s*\d+\.\s*$', '', section_content).strip()

                # Ignore sections that should not be appended
                if section_title in skip_sections or section_title.isdigit():
                    log.info(f'Skipping irrelevant section: {section_title}')
                    continue

                # Determine which header this section should map to
                mapped_header = section_to_header_mapping.get(section_title)

                if mapped_header:
                    if mapped_header == "Description":
                        # Include subheading in "Description" column
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

            # Skip adding content_dict if both 'Summary' and 'Description' are empty
            if not content_dict.get('Summary') and not content_dict.get('Description'):
                log.info("Skipping empty content_dict (both 'Summary' and 'Description' are empty).")
                continue

            # Append the parsed test case to the list
            parsed_testcases.append(content_dict)

    return parsed_testcases


def prepare_csv_data(parsed_list, headers):
    """
    The prepare_csv_data function is responsible for converting the structured data (produced by parse_content func)
    into a format that is ready to be written to a CSV file. The main purpose of prepare_csv_data is to take the
    parsed and structured content (a list of dictionaries, where each dictionary represents a row of single test case) and
    convert it into a format suitable for CSV generation. This involves ensuring that each row is properly aligned
    with the headers, and any necessary formatting (like joining content from different sections) is applied.

    Args:
        parsed_list : A list of dictionaries where each dictionary contains the parsed content for a user story or test case.
                      The keys in the dictionary correspond to the headers (like "Description," "Summary," "Issue Type"),
                      and the values contain the associated content.
        headers: A list of strings that represent the column names or headers for the CSV file. These headers dictate the order
                 and structure of the content in the CSV file (like "Description," "Summary," "Issue Type")

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
    value "Test Case" as its content 
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

def convert_csv_string_to_list(csv_string):
    """
    Converts a CSV-formatted string back into a list of lists.

    Args:
        csv_string (str): The CSV-formatted string.

    Returns:
        List[List[str]]: A list of lists where each inner list represents a row in the CSV.
    """
    # Create a StringIO object from the CSV string
    input_stream = StringIO(csv_string)
    
    # Create a CSV reader object
    csv_reader = csv.reader(input_stream)
    
    # Convert the CSV reader to a list of lists
    data = [row for row in csv_reader]
    
    return data



async def csv_to_json(csv_string):
    '''
    Transform csv string (input- list of detailed user stories in a single line csv string format) to json (list of dictionaries)
    json_data = [{'Issue Type': 'Story', 'Summary': 'Property Owner Login', 'Description': 'As a Property Owner, I want to be able to log in to my account so that I can access my property information and maintenance requests.', 'Priority': 'Medium', 'Classification': 'Property Management', 'Acceptance Criteria': "Constraints:\n1. The Property Owner's account must be verified and activated before they can log in.\nAcceptance Criteria:\n1. Given the Property Owner has a valid account, when they enter their login credentials, then they are redirected to their account dashboard.\nValidation Rules:\n1. The Property Owner's login credentials must match the stored credentials in the system.\nBusiness Rules:\n1. The Property Owner's account information must be kept confidential and secure.\nNon-Functional Requirements (NFRs):\n1. The login process should be completed within 5 seconds for 95% of transactions.\nPlease let me know if this meets your expectations or if you'd like me to make any changes!"}, {'Issue Type': 'Story', 'Summary': 'Service Provider Account Login', 'Description': 'As a Service Provider using the online platform, I want to be able to log in to my account so that I can access my service requests and quotes.', 'Priority': 'Medium', 'Classification': 'Account Management', 'Acceptance Criteria': "Constraints:\n1. The Service Provider must have a valid email address and password to log in.\nAcceptance Criteria:\n1. The Service Provider can enter their email address and password to initiate the login process.\nValidation Rules:\n1. The email address and password must match the Service Provider's registered credentials.\nBusiness Rules:\n1. The Service Provider's login credentials should be stored securely and comply with industry security standards.\nNon-Functional Requirements (NFRs):\n1. The login process should take no more than 3 seconds to complete for 95% of users."}]

    expected json_data = [
        {
            "Issue Type": "value",
            "Summary": "value",
            "Description": "value",
            "Priority": "value",
            "Classification": "value",
            "Acceptance Criteria": {
                "Constraints": "1. value",
                "Acceptance Criteria": "1. value",
                "Validation Rules": "1. value",
                "Business Rules": "1. value",
                "Non-Functional Requirements (NFRs)": "1. value"
            }
        }
    ]
    
    '''
    # Use StringIO to treat the CSV string as a file object
    csv_file = StringIO(csv_string)
    
    # Read the CSV data
    reader = csv.DictReader(csv_file)
    
    # Convert the CSV rows into a list of dictionaries
    json_data = []
    for row in reader:
        json_data.append(row)

    return json_data


async def transform_json_data(json_data):

    '''
    Transform json_data structure to proper structure required by Generate Manual Test Cases assistant
    transformed_data = [{'Test Case': 'Property Owner Login', 'Description': 'As a Property Owner, I want to be able to log in to my account so that I can access my property information and maintenance requests.', 'Priority': 'Medium', 'Classification': 'Property Management', 'Constraints': ["1. The Property Owner's account must be verified and activated before they can log in."], 'Acceptance Criteria': ['1. Given the Property Owner has a valid account, when they enter their login credentials, then they are redirected to their account dashboard.'], 'Validation Rules': ["1. The Property Owner's login credentials must match the stored credentials in the system."], 'Business Rules': ["1. The Property Owner's account information must be kept confidential and secure."], 'Non-Functional Requirements (NFRs)': ['1. The login process should be completed within 5 seconds for 95% of transactions.', "Please let me know if this meets your expectations or if you'd like me to make any changes!"]}, {'Test Case': 'Service Provider Account Login', 'Description': 'As a Service Provider using the online platform, I want to be able to log in to my account so that I can access my service requests and quotes.', 'Priority': 'Medium', 'Classification': 'Account Management', 'Constraints': ['1. The Service Provider must have a valid email address and password to log in.'], 'Acceptance Criteria': ['1. The Service Provider can enter their email address and password to initiate the login process.'], 'Validation Rules': ["1. The email address and password must match the Service Provider's registered credentials."], 'Business Rules': ["1. The Service Provider's login credentials should be stored securely and comply with industry security standards."], 'Non-Functional Requirements (NFRs)': ['1. The login process should take no more than 3 seconds to complete for 95% of users.']}]

    expected transformed_data = [
        {
            "Test Case": "value",
            "Description": "value",
            "Priority": "value",
            "Classification": "value",
            "Constraints": [
                "1. value"
            ],
            "Acceptance Criteria": [
                "value"
            ],
            "Validation Rules": [
                "value"
            ],
            "Business Rules": [
                "value"
            ],
            "Non-Functional Requirements (NFRs)": [
                "value"
            ]
        }
    ]
    '''

    transformed_data = []

    for story in json_data:
        transformed_story = {
            'Test Case': story['Summary'],
            'Description': story['Description'],
            'Priority': story['Priority'],
            'Classification': story['Classification'],
            'Constraints': [],
            'Acceptance Criteria': [],
            'Validation Rules': [],
            'Business Rules': [],
            'Non-Functional Requirements (NFRs)': []
        }

        # Split the Acceptance Criteria into sections
        criteria_sections = story['Acceptance Criteria'].split("\n")

        current_section = None

        for line in criteria_sections:
            line = line.strip()
            if line.startswith("Constraints:"):
                current_section = 'Constraints'
            elif line.startswith("Acceptance Criteria:"):
                current_section = 'Acceptance Criteria'
            elif line.startswith("Validation Rules:"):
                current_section = 'Validation Rules'
            elif line.startswith("Business Rules:"):
                current_section = 'Business Rules'
            elif line.startswith("Non-Functional Requirements (NFRs):"):
                current_section = 'Non-Functional Requirements (NFRs)'
            else:
                if current_section:
                    # Add the line to the appropriate section
                    transformed_story[current_section].append(line)

        transformed_data.append(transformed_story)

    return transformed_data

 


