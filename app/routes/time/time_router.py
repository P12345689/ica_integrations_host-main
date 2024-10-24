# -*- coding: utf-8 -*-
"""
Author: Chris Hay, Mihai Criveti
Description: Time integration router.

This module provides routes for getting the current time and answering time-related questions.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv(
    "ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct"
)
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/time/templates"))


class TimeInputModel(BaseModel):
    """Model to validate input data for time-related queries."""

    query: str = Field(..., description="The time-related query")


class SystemTimeInputModel(BaseModel):
    """Model to validate input data for system time retrieval."""

    format: str = Field(
        default="%Y-%m-%dT%H:%M:%S%Z", description="The format for the time string"
    )


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_system_time(format: str = "%Y-%m-%dT%H:%M:%S%Z") -> str:
    """Returns the current date and time in the specified format."""
    from datetime import datetime, timezone

    current_time = datetime.now(timezone.utc)
    formatted_time = current_time.strftime(format).replace("UTC", "Z")
    return formatted_time


def add_custom_routes(app: FastAPI):
    @app.post("/experience/time/ask_time/invoke")
    async def ask_time(request: Request) -> OutputModel:
        """
        Handle POST requests to ask time-related questions.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid.
        """
        invocation_id = str(uuid4())

        # Retrieve the API input
        try:
            data = await request.json()
            input_data = TimeInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        # Get the current time
        current_time = get_system_time()

        # Render the prompt using Jinja2
        prompt_template = template_env.get_template("prompt_template.jinja")
        rendered_prompt = prompt_template.render(
            query=input_data.query, current_time=current_time
        )

        # Call the LLM
        client = ICAClient()

        async def call_prompt_flow():
            return await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            formatted_result_future = executor.submit(asyncio.run, call_prompt_flow())
            formatted_result = formatted_result_future.result()

        # Render the response
        response_template = template_env.get_template("response_template.jinja")
        rendered_response = response_template.render(result=formatted_result)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/time/retrievers/get_current_time/invoke")
    async def get_current_time_route(request: Request) -> OutputModel:
        """
        Handle POST requests to get the current system time.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid.
        """
        invocation_id = str(uuid4())

        # Retrieve the API input
        try:
            data = await request.json()
            input_data = SystemTimeInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        # Get the current time
        current_time = get_system_time(input_data.format)

        # Render the response
        response_message = ResponseMessageModel(
            message=f"The current time is: {current_time}"
        )
        return OutputModel(invocationId=invocation_id, response=[response_message])
