# -*- coding: utf-8 -*-
"""
Author: Charan Kumar Samudrala
Description: Generates user stories for the given one line requirements and generates an excel with all the details of the user stories

This module provides route for user story and XLSX generation -
A system route for
    1. generating user stories by invoking the integration assistant_executer for each of the input one line requirements
    2. generating an excel file by mapping the contents of the generated user stories to appropriate columns
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
import httpx
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field
from app.routes.userstory_excel_mapper.config import *
from app.routes.userstory_excel_mapper.md_csv_util import *
from app.routes.userstory_excel_mapper.assistant_exec_util import assistant_executor

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


class ResultsModel(BaseModel):
    """Model to structure the results response."""

    status: str
    invocationId: str  # noqa: N815
    message: str


class ExecutionRequest(BaseModel):
    """
    Represents the request for executing an assistant.

    Attributes:
        assistant_id (str): The ID of the assistant to be executed.
        prompt (str): The prompt to be passed to the assistant.
    """

    assistant_id: str
    prompt: str


class InputModel(BaseModel):
    """
    Represents the request for generating content using assistant.

    Attributes:
        inputType (str): The type of content to be generated - user story/test case
        input (str): The input to be passed to the assistant.
        epicToUsAssistantId (Optional[str]): The ID of the assistant to be used (optional).
        usDetailAssistantId (Optional[str]): The ID of the assistant to be used (optional).
    """

    inputType: str
    input: list
    epicToUsAssistantId: Optional[str] = Field(
        default_factory=lambda: os.getenv("EPIC_US_ASSISTANT_ID", "epic_us_assistant_id")
    )
    usDetailAssistantId: Optional[str] = Field(
        default_factory=lambda: os.getenv("US_DETAIL_ASSISTANT_ID", "us_detail_assistant_id")
    )


def load_config():
    """Load configuration from file."""

    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        log.warning(f"Configuration file not found at {CONFIG_FILE_PATH}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except json.JSONDecodeError:
        log.error(f"Invalid JSON in configuration file {CONFIG_FILE_PATH}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def parse_request(request: Request) -> Tuple[InputModel, bool]:
    """Parse the input request body and convert it to a pydantic model for further processing"""

    body_text = await request.body()

    # Replace the windows new line character with generic new line character
    clean_text = body_text.replace(b"\r\n", b"\n").decode("utf-8")

    formatted_pydantic_json = json.loads(clean_text)

    input_value = formatted_pydantic_json["input"]

    if isinstance(input_value, str):
        # Fetch the input stripped off of the extra requirements - Only 10 allowed
        trimmed_input, is_trimmed = await trim_input_requirements(input_value)
        formatted_pydantic_json["input"] = [trimmed_input]

    json_string = json.dumps(formatted_pydantic_json)

    return InputModel.model_validate_json(json_string), is_trimmed


async def trim_input_requirements(input_str: str, max_requirements: int = MAX_REQUIREMENTS) -> Tuple[str, bool]:
    # Split the string by newline characters to get individual lines
    lines = input_str.split("\n")
    
     # Find the starting index of the line containing "Requirement"
    req_index = next((i for i, line in enumerate(lines) if "Requirement" in line), -1)
    
    # If "Requirement" is not found, return the original text and False
    if req_index == -1:
        return input_str, False
    
    # Extract the requirements part
    requirements = lines[req_index + 1:]

    # Initialize a flag to indicate whether trimming happened
    is_trimmed = False
    
    # If there are more than max_requirements, trim the extra ones
    if len(requirements) > max_requirements:
        requirements = requirements[:max_requirements]
        is_trimmed = True  # Set the flag to True if trimming occurs
    
    # Reconstruct the string with trimmed requirements
    trimmed_string = "\n".join(lines[:req_index + 1] + requirements)
    
    return trimmed_string, is_trimmed


def load_assistant_config(request) -> Tuple[str, Dict]:
    """
    Load the config file for this integration and fetch the required details.
    Also determine what assistant_id is to be used.
    """

    try:
        config = load_config()
        if request.epicToUsAssistantId == "epic_us_assistant_id":
            epic_us_assistant_id = config[request.inputType]["epic_us_assistant_id"]
            us_detail_assistant_id = config[request.inputType]["us_detail_assistant_id"]
        else:
            epic_us_assistant_id = request.epicToUsAssistantId
            us_detail_assistant_id = request.usDetailAssistantId

        return epic_us_assistant_id, us_detail_assistant_id, config
    except Exception as e:
        log.error(f"Error while fetching the assistantId for the inputType: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def execute_assistant_executor(input_list: List[str], assistant_id: str) -> List[Dict]:
    """Takes the input list of single-line requirements and the assistant_id and invokes the assistant_executer in parallel."""
    
    try:
        tasks = []
        for item in input_list:
            task = asyncio.create_task(invoke_assistant_executor(assistant_id, item))
            tasks.append(task)

        all_responses = await asyncio.gather(*tasks)
    except Exception as e:
        log.error(f"An error occurred while invoking assistant_executor: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    log.debug(f"Complete response from assistant_executor for assistant_id {assistant_id}: {all_responses}")
    return all_responses
  

async def invoke_assistant_executor(assistant_id: str, input_item: str):
    """Helper function to fetch response from the API using assistant_executor."""

    exec_request = {"assistant_id": assistant_id, "prompt": input_item}
    response = await assistant_executor(exec_request)  # Ensure assistant_executor supports async
    return response


async def generate_excel_from_xlsx_builder(csv_string: str, file_name: str) -> OutputModel:
    """The processed csv content is passed to xlsx_builder integration which can generate
    an xlsx file with the csv input
    Args:
        csv_string : The csv content that would be used to generate xlsx
        file_name: Name of the xlsx file to be generated
    """
    
    xlsx_builder_request = {"csv_data": {"Sheet1": csv_string}, "file_name": file_name}
    headers = {"Accept": "application/json", "Content-Type": "application/json", "Integrations-API-Key": API_KEY}

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(f"{SERVER_NAME}/system/xlsx_builder/generate_xlsx/invoke", headers=headers, json=xlsx_builder_request)
        response.raise_for_status()
        log.debug(f"Response received: {response.status_code}")
        final_xlsx = response.json()
        return OutputModel.model_validate(final_xlsx)


async def generate_file_path():
    """
    Create a unique file_name and path for the xlsx and pass it to xlsx_builder so that 
    the excel is generated with the given file_name and stored in the given path.
    """
    file_name = f"xlsx_{uuid4()}.xlsx"
    file_path = f"{PUBLIC_DIR}/{file_name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file_url = f"{SERVER_NAME}/{file_path}"
    return file_name, file_url


async def get_excel_with_userstories(content_request: InputModel, file_name: str) -> OutputModel:
    """
    Function that runs in the background for generating an excel with 
    detailed userstories based on the provided input.

    Args:
        request (Request): The incoming request object.
        file_name (str): Name of the excel file to be generated

    Returns:
        OutputModel: The structured output response.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        """
        Retrieve assistant_id (based on the inputType in request) and
        other details from config.json
        """
        epic_us_assistant_id, us_detail_assistant_id, config = load_assistant_config(content_request)
    except Exception as e:
        log.error(f"Error while reading data from config: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        """
        Pass the assistant_id and the required input to the assistant_executer integration
        and fetch the required content
        First call to execute_assistant_executor to fetch Single line user stories from Epic
        """
        # Run this in an async context
        oneLineUserStories = await execute_assistant_executor(content_request.input, epic_us_assistant_id)
    except Exception as e:
        log.error(f"Failed while invoking assistant_executer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        """
        Pass the assistant_id and the required input to the assistant_executer integration
        and fetch the required content
        Second call to execute_assistant_executor to fetch detailed user stories from single line user stories
        """
        # Extract the "message" property from each item in the list
        userStotyList = [item.message for response in oneLineUserStories for item in response.response]
        # Join the content into a single string
        content_str = ''.join(userStotyList)

        # Regular expression to match all the numbered user stories
        items = re.findall(r'\d+\.\s+.*', content_str)

        all_detailed_userstories = await execute_assistant_executor(items, us_detail_assistant_id)

    except Exception as e:
        log.error(f"Failed while invoking assistant_executer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        """
        The response generated from the assistant_executor is then parsed and processed into
        csv content which can be used to generate xlsx
        """
        csv_string = process_content_into_csv(all_detailed_userstories, config, content_request.inputType)
    except Exception as e:
        log.error(f"Failed to create csv content: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        """
        The processed csv content is then passed to xlsx_builder integration which can generate
        an xlsx file with the csv input
        """
        return await generate_excel_from_xlsx_builder(csv_string, file_name)
    except Exception as e:
        log.error(f"Failed to generate xlsx file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def add_custom_routes(app: FastAPI):
    @app.post("/system/us_excel_mapper/generate_excel/invoke")
    async def generate_excel_with_userstories(request: Request, background_tasks: BackgroundTasks) -> OutputModel:
        """
        Endpoint for generating content (userstories) in markdown format
        and an excel with that content based on the provided inputType and input.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error processing the request.
        """
        try:
            """
            Parse the input request body and retrieve the content in json format
            to be passed to assistant_executer
            """
            content_request, is_trimmed = await parse_request(request)

            """
            Create a unique file_name and path for the xlsx and pass it to xlsx_builder so that 
            the excel is generated with the given file_name and stored in the given path.
            """
            file_name, file_url = await generate_file_path()
            log.debug(f"Generated URL for XLSX with User stories: {file_url}")
        except json.JSONDecodeError as e:
            log.error(f"Failed to decode JSON: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON input")

        async def process_and_store() -> None:
            try:
                log.debug(f"Execution of background tasks has started")
                excel_generation_response = await get_excel_with_userstories(content_request, file_name)
                final_message = excel_generation_response.response[0].message
                log.debug(f"{final_message}")

            except Exception as e:
                log.error(f"Error processing background task: {str(e)}")

        background_tasks.add_task(process_and_store)

        response_template = template_env.get_template("userstory_response.jinja")
        rendered_response = response_template.render(file_url=file_url, is_trimmed=is_trimmed)
        log.debug(f"Rendered response: {rendered_response}")

        response_message = ResponseMessageModel(
            message=rendered_response,
            type="text",
        )
        log.debug(f"Generation of user stories has started in the path {file_url}")
        return OutputModel(status="processing", invocationId=str(uuid4()), response=[response_message])