# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Ollama-like integration router.

This module provides routes for generating text using an Ollama-like interface
while using the prompt_flow based API under the hood.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/ollama_like/templates"))


class GenerateInputModel(BaseModel):
    """Model to validate input data for text generation."""

    model: str = Field(..., description="The model to use for generation")
    prompt: str = Field(..., description="The prompt for text generation")
    system: Optional[str] = Field(None, description="Optional system message")
    template: Optional[str] = Field(None, description="Optional template for formatting")
    context: Optional[str] = Field(None, description="Optional context for generation")
    options: Optional[dict] = Field(None, description="Optional generation options")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def add_custom_routes(app: FastAPI):
    @app.post("/experience/ollama_like/generate/invoke")
    async def generate(request: Request) -> OutputModel:
        """
        Handle POST requests to generate text using an Ollama-like interface.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or an error occurs during generation.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> client = TestClient(app)
            >>> response = client.post("/experience/ollama_like/generate/invoke",
            ...     json={"model": "llama2", "prompt": "Hello, world!"})
            >>> assert response.status_code == 200
            >>> assert "invocationId" in response.json()
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = GenerateInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input data: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        # Render the prompt using Jinja2
        prompt_template = template_env.get_template("prompt_template.jinja")
        rendered_prompt = prompt_template.render(
            prompt=input_data.prompt,
            system=input_data.system,
            context=input_data.context,
        )

        # Call the LLM
        client = ICAClient()

        async def call_prompt_flow():
            try:
                return await asyncio.to_thread(
                    client.prompt_flow,
                    model_id_or_name=DEFAULT_MODEL,
                    prompt=rendered_prompt,
                )
            except Exception as e:
                log.error(f"Error calling prompt_flow: {str(e)}")
                raise HTTPException(status_code=500, detail="Error generating response")

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            try:
                formatted_result_future = executor.submit(asyncio.run, call_prompt_flow())
                formatted_result = formatted_result_future.result()
            except Exception as e:
                log.error(f"Error in ThreadPoolExecutor: {str(e)}")
                raise HTTPException(status_code=500, detail="Error processing request")

        # Render the response
        response_template = template_env.get_template("response_template.jinja")
        rendered_response = response_template.render(result=formatted_result)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/ollama_like/model_info/invoke")
    async def model_info(request: Request) -> OutputModel:
        """
        Handle POST requests to get information about the available model.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response with model information.

        Raises:
            HTTPException: If the input is invalid.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> client = TestClient(app)
            >>> response = client.post("/system/ollama_like/model_info/invoke")
            >>> assert response.status_code == 200
            >>> assert "invocationId" in response.json()
        """
        invocation_id = str(uuid4())

        model_info = {
            "model": DEFAULT_MODEL,
            "description": "Default model for text generation",
            "type": "LLM",
        }

        response_message = ResponseMessageModel(message=str(model_info))
        return OutputModel(invocationId=invocation_id, response=[response_message])
