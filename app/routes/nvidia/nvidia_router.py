# -*- coding: utf-8 -*-
"""
Authors: Mihai Criveti
Description: This module provides an integration with the NVIDIA Neva-22B API for recognizing images.

The main functionality includes:
- Making API calls to recognize images based on user input.
- Handling errors and providing informative responses to the user.

The module uses FastAPI for handling HTTP requests, Pydantic for input validation and output structuring,
and Jinja2 for templating the responses.

Example usage:
    # Make a POST request to the /neva22b/invoke endpoint with the following JSON payload:
    {
        "query": "What is in this image?",
        "image_url": "https://example.com/image.jpg"
    }

Environment variables:
    - NVIDIA_BEARER_TOKEN: The Bearer token for authenticating with the NVIDIA Neva-22B API.
"""

import logging
import uuid
from typing import Optional

from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field

from app.routes.nvidia.tools.nvidia_tools import call_neva22b_api, call_nvidia_generation_api, call_nvidia_llm_api

log = logging.getLogger(__name__)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/nvidia/templates"))


class InputModel(BaseModel):
    """Model to validate input data."""

    query: str
    image_url: Optional[str] = Field(default=None, description="Image URL of the image to be described")
    model: Optional[str] = Field(default=None, description="Model to be used")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str
    response: list[ResponseMessageModel] = Field(min_items=1)


def add_custom_routes(app: FastAPI):
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    @app.post("/system/nvidia/image/invoke", response_model=OutputModel)
    async def image_request(request: Request) -> OutputModel:
        """
        Handles the POST request to generate images using NVIDIA image generation APIs.

        This function takes the input data from the request, calls the NVIDIA Stable diffusion API to generate an image,
        and returns a response containing a text message with the link to the generated image.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, invocation ID, and response messages.

        Raises:
            HTTPException: If there is an error processing the request or recognizing the image.

        Example:
            >>> import requests
            >>> url = "https://your-app-url.com/system/nvidia/image/invoke"
            >>> data = {
            ...     "query": "A penguin in a suit",
            ...     "image_url": "",
            ...     "model": "stable-diffusion-3-medium"
            ... }
            >>> headers = {"Content-Type": "application/json"}
            >>> response = requests.post(url, json=data, headers=headers)
            >>> response.json()
            {
                "status": "success",
                "invocationId": "f62692d9-f6ce-47a5-b80e-2457083e914d",
                "response": [
                    {
                        "message": "path_to_image",
                        "type": "text"
                    }
                ]
            }
        """
        try:
            data = await request.json()
            input_data = InputModel(**data)

            image_url = await call_nvidia_generation_api(input_data.model, input_data.query)

            template = template_env.get_template("nvidia_response.jinja")
            formatted_result = template.render(response=image_url)

            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[
                    ResponseMessageModel(message=formatted_result, type="text"),
                    ResponseMessageModel(message=image_url, type="image"),
                ],
            )
        except KeyError:
            formatted_result = "I'm sorry but the NVIDIA integration is misconfigured. Please check the Bearer token."
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )
        except Exception as e:
            formatted_result = f"{e}"
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )

        return response

    @app.post("/system/nvidia/neva22b/invoke", response_model=OutputModel)
    async def neva22b_request(request: Request) -> OutputModel:
        """
        Handles the POST request to recognize images using NVIDIA Neva-22B.

        This function takes the input data from the request, calls the NVIDIA Neva-22B API to recognize an image,
        and returns a response containing a text message with the recognition result.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, invocation ID, and response messages.

        Raises:
            HTTPException: If there is an error processing the request or recognizing the image.

        Example:
            >>> import requests
            >>> url = "https://your-app-url.com/neva22b/invoke"
            >>> data = {
            ...     "query": "What is in this image?",
            ...     "image_url": "https://example.com/image.jpg"
            ... }
            >>> headers = {"Content-Type": "application/json"}
            >>> response = requests.post(url, json=data, headers=headers)
            >>> response.json()
            {
                "status": "success",
                "invocationId": "f62692d9-f6ce-47a5-b80e-2457083e914d",
                "response": [
                    {
                        "message": "The image contains a cat sitting on a couch.",
                        "type": "text"
                    }
                ]
            }
        """
        log.info("Received request to /system/nvidia/neva22b/invoke")
        try:
            data = await request.json()
            log.info(f"Request data: {data}")
            input_data = InputModel(**data)
            log.info(f"Input data validated: {input_data}")

            log.info("Calling NVIDIA Neva-22B API.")
            neva22b_response = await call_neva22b_api(input_data.image_url, input_data.query)
            log.info(f"NVIDIA Neva-22B API response: {neva22b_response}")

            log.info("Rendering response template.")
            template = template_env.get_template("neva_response.jinja")
            formatted_result = template.render(response=neva22b_response)
            log.info(f"Rendered response: {formatted_result}")

            log.info("Constructing output response.")
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )
            log.info(f"Output response: {response}")

        except KeyError as e:
            log.error(f"Bearer token error: {e}")
            formatted_result = "I'm sorry but the NVIDIA Neva-22B integration is misconfigured. Please check the Bearer token."
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )
        except Exception as e:
            log.error(f"Neva-22B API error: {e}")
            formatted_result = "I'm sorry but I couldn't recognize the image, please try with a different image."
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )

        log.info(f"Returning response: {response}")
        return response

    @app.post("/system/nvidia/llm/invoke")
    async def nvidia_llm_request(request: Request):
        """
        Handles the POST request to recognize images using a given NVIDIA model.

        This function takes the input data from the request, calls the given NVIDIA model API to generate an output,
        and returns a response containing a text message with the result.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, invocation ID, and response messages.

        Raises:
            HTTPException: If there is an error processing the request or recognizing the image.

        Example:
            >>> import requests
            >>> url = "https://your-app-url.com/nvidia/llm/invoke"
            >>> data = {
            ...     "query": "what is the percentage change of the net income from Q4 FY23 to Q4 FY24?",
            ...     "image_url": "",
            ...     "model": "llama3-chatqa-1.5-70b"
            ... }
            >>> headers = {"Content-Type": "application/json"}
            >>> response = requests.post(url, json=data, headers=headers)
            >>> response.json()
            {
                "status": "success",
                "invocationId": "f62692d9-f6ce-47a5-b80e-2457083e914d",
                "response": [
                    {
                        "message": "The percentage change of the net income ...",
                        "type": "text"
                    }
                ]
            }
        """
        log.info("Received request to /system/nvidia/llm/invoke")
        try:
            data = await request.json()
            log.info(f"Request data: {data}")
            input_data = InputModel(**data)
            log.info(f"Input data validated: {input_data}")

            nvidia_model_response = await call_nvidia_llm_api(input_data.model, input_data.query)

            template = template_env.get_template("nvidia_response.jinja")
            formatted_result = template.render(response=nvidia_model_response)

            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )

        except KeyError as e:
            log.error(f"Bearer token error: {e}")
            formatted_result = "I'm sorry but the NVIDIA model integration is misconfigured. Please check the Bearer token."
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )
        except Exception as e:
            log.error(f"Nvidia model API error: {e}")
            formatted_result = "I'm sorry but I couldn't generate a response. Please try with a different query."
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )

        log.info(f"Returning response: {response}")
        return response
