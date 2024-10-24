# -*- coding: utf-8 -*-
"""
Author: {{ cookiecutter.author }}
Description: {{ cookiecutter.description }}

TODO: Remember to update the module-level docstring with specific details about your integration
and remove / address the TODOs in this template.
Remplace the example timestamp with a function of your choice.

This module provides routes for {{ cookiecutter.module_name }}, including a system route
for generating a timestamp, an experience route that wraps the system
functionality with LLM interaction, and a file generation route that creates
a timestamped file and returns its URL.

Integration Development Guidelines:
1. Use Pydantic v2 models to validate all inputs and outputs.
2. All functions should be defined as async.
3. Ensure that all code has full docstring coverage in Google docstring format.
4. Implement full unit test coverage (can also use doctest).
5. Use Jinja2 templates for LLM prompts and response formatting.
6. Implement proper error handling and logging.
7. Use environment variables for configuration where appropriate.
8. Follow PEP 8 style guidelines.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
import subprocess
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
# TODO: Update the template directory path if needed
template_env = Environment(loader=FileSystemLoader("dev/app/routes/{{ cookiecutter.module_name }}/templates"))

# TODO: Update these models to match your integration's input requirements
class TimestampInputModel(BaseModel):
    """Model to validate input data for timestamp generation."""
    format: str = Field(default="%Y%m%d%H%M%S", description="Format string for the date command")

class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""
    query: str = Field(..., description="The input query about time or timestamps")

class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""
    message: str
    type: str = "text"

class OutputModel(BaseModel):
    """Model to structure the output response."""
    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


# TODO: Replace this function with your own implementation that generates the desired output for your integration. This is just a sample function.
def generate_timestamp(format: str) -> str:
    """
    Generate a timestamp using the date command.

    Args:
        format (str): The format string for the date command.

    Returns:
        str: The generated timestamp.

    Raises:
        RuntimeError: If the timestamp generation fails.
    """
    try:
        log.debug(f"Generating timestamp with format: {format}")
        result = subprocess.run(
            ["date", f"+{format}"],
            capture_output=True,
            text=True,
            check=True
        )
        timestamp = result.stdout.strip()
        log.debug(f"Generated timestamp: {timestamp}")
        return timestamp
    except subprocess.CalledProcessError as e:
        log.error(f"Error generating timestamp: {e}")
        raise RuntimeError("Failed to generate timestamp")

def generate_zip_file(content: str, filename: str) -> str:
    """
    Generate a ZIP file containing the given content.

    Args:
        content (str): The content to be included in the ZIP file.
        filename (str): The name of the file to be created inside the ZIP.

    Returns:
        str: The URL of the generated ZIP file.
    """
    zip_file_name = f"{{ cookiecutter.module_name }}_{uuid4()}.zip"
    zip_file_path = os.path.join("public/{{ cookiecutter.module_name }}", zip_file_name)
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

    with zipfile.ZipFile(zip_file_path, "w") as zip_file:
        zip_file.writestr(filename, content)

    zip_file_url = f"{SERVER_NAME}/public/{{ cookiecutter.module_name }}/{zip_file_name}"
    log.info(f"Generated ZIP file URL: {zip_file_url}")
    return zip_file_url

def add_custom_routes(app: FastAPI):
    @app.post("/system/{{ cookiecutter.module_name }}/generate_timestamp/invoke")
    async def generate_timestamp_route(request: Request) -> OutputModel:
        """
        Handle POST requests to generate a timestamp.

        This is a sample system route that demonstrates how to implement
        a simple functionality without LLM interaction.

        TODO: Replace this route with your own system-level functionality.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or timestamp generation fails.
        """
        log.info("Received request to generate timestamp")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = TimestampInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(generate_timestamp, input_data.format)
                timestamp = future.result()
        except RuntimeError as e:
            log.error(f"Error generating timestamp: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate timestamp")

        log.info(f"Generated timestamp: {timestamp}")
        response_message = ResponseMessageModel(message=f"Generated timestamp: {timestamp}")
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/{{ cookiecutter.module_name }}/timestamp_experience/invoke")
    async def timestamp_experience(request: Request) -> OutputModel:
        """
        Handle POST requests for the timestamp experience.

        This route wraps the system timestamp generation with LLM interaction.
        It demonstrates how to combine a system-level function with LLM processing
        to create a more engaging user experience.

        TODO: Update this route to match your integration's requirements.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        log.info("Received request for timestamp experience")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ExperienceInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        # Generate a timestamp
        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(generate_timestamp, "%Y-%m-%d %H:%M:%S")
                timestamp = future.result()
        except RuntimeError as e:
            log.error(f"Error generating timestamp: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate timestamp")

        # Render the prompt using Jinja2
        # TODO: Update the template name if needed
        prompt_template = template_env.get_template("prompt.jinja")
        rendered_prompt = prompt_template.render(query=input_data.query, timestamp=timestamp)
        log.debug(f"Rendered prompt: {rendered_prompt}")

        # Call the LLM
        client = ICAClient()

        async def call_prompt_flow():
            """Async wrapper for the LLM call."""
            log.debug("Calling LLM")
            return await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt
            )

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                formatted_result_future = executor.submit(asyncio.run, call_prompt_flow())
                formatted_result = formatted_result_future.result()
            log.debug(f"Received LLM response: {formatted_result}")
        except Exception as e:
            log.error(f"Error calling LLM: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing request")

        # Render the response
        # TODO: Update the template name if needed
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(result=formatted_result, timestamp=timestamp)
        log.debug(f"Rendered response: {rendered_response}")

        response_message = ResponseMessageModel(message=rendered_response)
        log.info("Timestamp experience request processed successfully")
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/{{ cookiecutter.module_name }}/generate_{{ cookiecutter.module_name }}_file/invoke")
    async def generate_{{ cookiecutter.module_name }}_file(request: Request) -> OutputModel:
        """
        Handle POST requests to generate a {{ cookiecutter.module_name }} file and return its URL along with a formatted response.

        This route demonstrates how to create a file with generated content,
        zip it, and return both a formatted response and a URL for download.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response with a formatted message and the file URL.

        Raises:
            HTTPException: If the input is invalid or file generation fails.
        """
        log.info("Received request to generate {{ cookiecutter.module_name }} file")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = TimestampInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            timestamp = generate_timestamp(input_data.format)
            file_content = f"{{ cookiecutter.module_name.capitalize() }}: {timestamp}\nGenerated at: {generate_timestamp('%Y-%m-%d %H:%M:%S')}"
            zip_file_url = generate_zip_file(file_content, "{{ cookiecutter.module_name }}.txt")
        except Exception as e:
            log.error(f"Error generating {{ cookiecutter.module_name }} file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate {{ cookiecutter.module_name }} file")

        log.info(f"Generated {{ cookiecutter.module_name }} file: {zip_file_url}")

        # Render the response using a template
        response_template = template_env.get_template("file_response.jinja")
        rendered_response = response_template.render(zip_file_url=zip_file_url)

        response_messages = [
            ResponseMessageModel(message=rendered_response, type="text"),
            ResponseMessageModel(message=zip_file_url, type="text")
        ]
        return OutputModel(invocationId=invocation_id, response=response_messages)

# TODO: Add any additional routes or helper functions as needed for your integration

# TODO: Consider adding any additional configuration variables specific to your integration

# TODO: Implement additional error handling specific to your integration if needed

# TODO: Create corresponding test files for unit and integration tests
