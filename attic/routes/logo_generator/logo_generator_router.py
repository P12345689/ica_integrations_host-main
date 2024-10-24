# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Generates a logo for marketing purpuse

Notes for integration developers:
1. Use Pydantic v2 models to validate all inputs and all outputs
2. All functions should be defined as async
3. Ensure that all code has full docstring coverage in Google docstring format
4. Full unit test coverage (can also use doctest)
"""

import json
import logging
import os
from typing import Any, Dict, List, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("dev/app/routes/logo_generator/templates"))
log.debug("Jinja2 environment initialized with template directory.")


class InputModel(BaseModel):
    """Model to validate input data."""

    user_input: str


class LLMResponseModel(BaseModel):
    """Model to structure the LLM response data."""

    requestType: str
    requestData: Dict[str, Any]
    curlCommand: str
    llmResponse: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str
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
        >>> response = client.post("/logo_generator/invoke", json={"model": "test_model", "prompt": "Hello"})
        >>> response.status_code
        200
        >>> response.json()["status"]
        'success'
    """

    @app.api_route("/logo_generator/invoke", methods=["POST"])
    async def logo_generator(request: Request) -> OutputModel:
        """Handle POST requests to the invoke endpoint.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the JSON is invalid or if validation fails.
        """
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

        # Load and render the prompt template using Jinja2 template
        template = template_env.get_template("prompt_template.jinja")
        rendered_input = template.render(user_input=input_data.user_input, dynamic_input="Make this in Spanish")

        # instantiate the LLM client and get the response if it's a POST request
        if request_type == "POST":
            consulting_assistants_model = ICAClient()
            llm_response = consulting_assistants_model.prompt_flow(
                model_id_or_name=DEFAULT_MODEL, prompt=rendered_input
            )

        if llm_response is None:
            llm_response = "No response from LLM"

        # Load and render the response using Jinja2 template
        template = template_env.get_template("response_template.jinja")
        rendered_response = template.render(llm_response=llm_response)

        # Return the response
        invocation_id = str(uuid4())  # Generate a unique invocation ID
        response_dict = ResponseMessageModel(message=rendered_response, type="text")

        response_data = OutputModel(invocationId=invocation_id, response=[response_dict])

        return response_data
