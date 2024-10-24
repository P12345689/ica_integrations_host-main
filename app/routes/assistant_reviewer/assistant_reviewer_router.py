# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Review assistant output and provide feedback

It grades the quality of assistants and scores them.

Can be used to test assistants using diff. models

Input:
- Agent ID
- Prompt ID used to build the agent
- Input Prompt
- Expected Output

Output:
- Assistant review / score
"""

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/assistant_reviewer/templates"))
log.debug("Jinja2 environment initialized with template directory.")


class InputModel(BaseModel):
    """Model to validate input data."""

    assistant_id: int
    assistant_input: str
    assistant_output: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: Annotated[List[ResponseMessageModel], Field(min_length=1)]


def add_custom_routes(app: FastAPI) -> None:
    """Add custom routes to the FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.

    Example:
        >>> from fastapi.testclient import TestClient
        >>> app = FastAPI()
        >>> add_custom_routes(app)
        >>> client = TestClient(app)
        >>> response = client.post("/assistant_reviewer/invoke", json={"prompt": "Hello"})
        >>> response.status_code
        200
        >>> response.json()["status"]
        'success'
    """

    @app.api_route("/assistant_reviewer/invoke", methods=["POST"])
    async def invoke(request: Request) -> OutputModel:
        """Handle POST requests to the invoke endpoint.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the JSON is invalid or if validation fails.
        """
        # Generate an invocation id
        invocation_id = str(uuid4())  # Generate a unique invocation ID

        # get the type of request
        request_type = request.method
        log.debug(f"Received {request_type}")

        # get the data
        try:
            data = await request.json()
            input_data = InputModel(**data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

        # Create an ICA Client object
        consulting_assistants_model = ICAClient()

        # Initialize assistant variables with default values
        assistant_title = None
        assistant_description = None
        assistant_expected_outcome = None
        assistant_welcome_message = None
        found_assistant = False

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            # Get the assistants list
            assistants_list_future = executor.submit(consulting_assistants_model.get_assistants, refresh_data=True)
            assistants_list = assistants_list_future.result()

            for assistant in assistants_list:
                if assistant["id"] == str(input_data.assistant_id):
                    log.info(f"*Found assistant_id: {input_data.assistant_id}")
                    assistant_title = assistant["title"]
                    assistant_description = assistant["description"]
                    assistant_expected_outcome = assistant["expectedOutcome"]
                    assistant_welcome_message = assistant["welcomeMessage"]
                    found_assistant = True
                    break

        if not found_assistant:
            # Return cannot find assistant id response
            log.error(f"Could not find any assistant with id: {input_data.assistant_id}")
            response_dict = ResponseMessageModel(
                message=f"Cannot find assistant with id: {input_data.assistant_id}",
                type="text",
            )
            response_data = OutputModel(invocationId=invocation_id, response=[response_dict])
            return response_data

        # Load and render the prompt template using Jinja2 template
        template = template_env.get_template("prompt_template.jinja")
        rendered_input = template.render(
            assistant_input=input_data.assistant_input,
            assistant_output=input_data.assistant_output,
            assistant_title=assistant_title,
            assistant_description=assistant_description,
            assistant_expected_outcome=assistant_expected_outcome,
            assistant_welcome_message=assistant_welcome_message,
        )
        log.info(f"* Calling LLM with template: {rendered_input}")

        # instantiate the LLM client and get the response if it's a POST request
        if request_type == "POST":
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                llm_response_future = executor.submit(
                    consulting_assistants_model.prompt_flow,
                    model_id_or_name=DEFAULT_MODEL,
                    prompt=rendered_input,
                )
                llm_response = llm_response_future.result()

        if llm_response is None:
            llm_response = "No response from LLM"

        # Load and render the response using Jinja2 template
        template = template_env.get_template("response_template.jinja")
        rendered_response = template.render(
            llm_response=llm_response,
            assistant_id=input_data.assistant_id,
            assistant_title=assistant_title,
        )

        # Return the response
        response_dict = ResponseMessageModel(message=rendered_response, type="text")

        response_data = OutputModel(invocationId=invocation_id, response=[response_dict])

        return response_data
