# -*- coding: utf-8 -*-
"""
Author: Shrishti Shrivastav
Description: Generate manual test cases based on user story and generates an 
             excel with all the details of the test cases
           
This module provides route for test cases and XLSX generation -
A system route for
    1. Generating test cases by invoking the integration assistant_executer for a user story
    2. Generating an excel file by mapping the contents of the generated test cases to appropriate columns
"""

import asyncio 
import logging
import os
import json
import httpx
from typing import Dict, List, Optional, Tuple
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from app.routes.test_cases_agent.md_csv_util import *
from app.routes.userstory_excel_mapper.assistant_exec_util import assistant_executor 
from uuid import uuid4
from app.routes.test_cases_agent.config import *
from jinja2 import Environment, FileSystemLoader

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

class InputModel(BaseModel):
    """
    Represents the request for generating content using assistant.

    Attributes:
        input (str): The input to be passed to the assistant.
        mtcAssistantId (Optional[str]): The ID of the assistant to be used (optional).
    """

    input: list
    mtcAssistantId: Optional[str] = Field(
        default_factory=lambda: os.getenv("US_MTC_ASSISTANT_ID", "us_mtc_assistant_id")
    )


def load_config():
    """Load config.json file from test_cases_agent/json file."""

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


async def parse_request(request: Request) -> Tuple[list, str]:
    """Parse the input request body and convert it to a pydantic model for further processing"""

    """
    1. Parse the input (CSV string of a list of user stories) and retrieve 
    the content in json format using func csv_to_json()
    Convert json to proper userstory format for Generate manual test
    cases assistant using func transform_json_data()
    
    """
    body_text = await request.body() # body_text is the string input from request object
    clean_text = body_text.replace(b"\r\n", b"\n").decode("utf-8") # Replace the windows new line character with generic new line character
    formatted_pydantic_json = json.loads(clean_text)
    
    input_value = formatted_pydantic_json["input"] # input_value is the proper csv string of the input required for further processing
    mtcAssistantId = formatted_pydantic_json.get("mtcAssistantId", None)
    
    content_requestt = await csv_to_json(input_value) 

    userStoryList = await transform_json_data(content_requestt)

    return userStoryList, mtcAssistantId


async def load_assistant_config(mtcAssistantId) -> Tuple[str, Dict]:
    """
    Load the config file for this integration and fetch the required details.
    Also determine what assistant_id is to be used.
    """
    try:
        config = load_config()
        if mtcAssistantId is not None:
            mtc_assistant_id = mtcAssistantId
        else:
            mtc_assistant_id = config["mtc_assistant_id"] 

        return mtc_assistant_id, config
    except Exception as e:
        log.error(f"Error while fetching the assistantId for the inputType: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def execute_assistant_executor(input_list: List[dict], assistant_id: str) -> List[Dict]:
    """Takes the input list of each user story and the assistant_id 
       and invokes the assistant_executer in parallel."""

    try:
        tasks = []
        for item in input_list:
            # Convert each element which is of type dictionary to type string to pass to the Generate Manual Test Cases assistant
            formatted_item = json.dumps(item, indent=2, ensure_ascii=False)
            formatted_item = formatted_item.replace('{', '').replace('}', '').replace('"', "'")
            
            task = asyncio.create_task(invoke_assistant_executor(assistant_id, formatted_item))
            tasks.append(task)

        all_responses = await asyncio.gather(*tasks)
    except Exception as e:
        log.error(f"An error occurred while invoking assistant_executor: {e}")
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


async def get_excel_with_testcases(mtcAssistantId, userStoryList: InputModel, file_name: str) -> OutputModel:
    """
    Function that runs in the background for generating an excel with 
    testcases based on the provided input.

    Args:
        mtcAssistantId (str): AssistantId to generate test cases from the incoming request object.
        This request is an input csv string.

    Returns:
        OutputModel: The structured output response.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        """
        Retrieve assistant_id and other details from config.json
        """
        
        mtc_assistant_id, config = await load_assistant_config(mtcAssistantId)
    except Exception as e:
        log.error(f"Error while reading data from config: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        """
        1. First step: We have user story list as string. 
        First call to execute_assistant_executor to fetch manual test cases for each user story

        Pass the assistant_id and the required input to the assistant_executer integration
        and fetch the required content
        
        """
        all_detailed_testcases = await execute_assistant_executor(userStoryList, mtc_assistant_id)

    except Exception as e:
        log.error(f"Failed while invoking assistant_executer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        """
        2. Second step: The response generated from the assistant_executor is then parsed and processed into
        csv content which can be used to generate xlsx
        """
        csv_string = process_content_into_csv(all_detailed_testcases, config)
    except Exception as e:
        log.error(f"Failed to create csv content: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        """
        3. Third step: The processed csv content is then passed to xlsx_builder integration which can generate
        an xlsx file with the csv input
        """
        return await generate_excel_from_xlsx_builder(csv_string, file_name)
    except Exception as e:
        log.error(f"Failed to generate xlsx file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def add_custom_routes(app: FastAPI):
    @app.post("/system/testcases_excel_mapper/testcases_generate_excel/invoke")
    async def generate_excel_with_testcases(request: Request, background_tasks: BackgroundTasks) -> OutputModel:
        """
        Endpoint for generating content (test cases) in markdown format
        and an excel with that content based on the provided input.

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
            userStoryList, mtcAssistantId = await parse_request(request)

            """
            Create a unique file_name and path for the xlsx and pass it to xlsx_builder so that 
            the excel is generated with the given file_name and stored in the given path.
            """
            file_name, file_url = await generate_file_path()
            log.debug(f"Generated URL for XLSX with manual testcases: {file_url}")
        except json.JSONDecodeError as e:
            log.error(f"Failed to decode JSON: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON input")

        async def process_and_store() -> None:
            try:
                log.debug(f"Execution of background tasks has started")
                excel_generation_response = await get_excel_with_testcases(mtcAssistantId, userStoryList, file_name)
                final_message = excel_generation_response.response[0].message
                log.debug(f"{final_message}")

            except Exception as e:
                log.error(f"Error processing background task: {str(e)}")

        background_tasks.add_task(process_and_store)

        response_template = template_env.get_template("testcases_response.jinja")
        rendered_response = response_template.render(file_url=file_url)
        log.debug(f"Rendered response: {rendered_response}")

        response_message = ResponseMessageModel(
            message=rendered_response,
            type="text",
        )
        log.debug(f"Generation of manual test cases has started in the path {file_url}")
        return OutputModel(status="processing", invocationId=str(uuid4()), response=[response_message])