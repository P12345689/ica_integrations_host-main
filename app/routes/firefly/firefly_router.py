# -*- coding: utf-8 -*-
"""
Authors: Stephen Badger, Mihai Criveti (async, local caching, pydantic validation)
Description: This module provides an integration with the Adobe Firefly API for generating and manipulating images.

The main functionality includes:
- Authenticating with the Firefly API using the provided client ID and secret.
- Making API calls to generate, expand, and fill images based on user input.
- Downloading and serving the generated images locally.
- Handling errors and providing informative responses to the user.

The module uses FastAPI for handling HTTP requests, Pydantic for input validation and output structuring,
and Jinja2 for templating the responses.

Example usage:
    # Make a POST request to the /firefly/invoke endpoint with the following JSON payload:
    {
        "query": "A beautiful sunset",
        "action": "generate",
        "image_type": "photo",
        "width": 1024,
        "height": 1024
    }

Environment variables:
    - ADOBE_FIREFLY_CLIENT_ID: The client ID for authenticating with the Firefly API.
    - ADOBE_FIREFLY_CLIENT_SECRET: The client secret for authenticating with the Firefly API.
    - ADOBE_FIREFLY_ENDPOINT: The endpoint URL for the Firefly API (default: "firefly-beta.adobe.io").
"""

import asyncio
import logging
import os
import uuid
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Literal

import requests
from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field
import app.tools.global_tools.adobe_firefly_tool as firefly_tool

# Logging
log = logging.getLogger(__name__)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/firefly/templates"))

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

class InputModel(BaseModel):
    """Model to validate input data."""

    query: str
    action: str = Field(default="generate")
    image_type: str = Field(default=firefly_tool.DEFAULT_IMAGE_TYPE)
    width: int = Field(default=firefly_tool.DEFAULT_IMAGE_WIDTH)
    height: int = Field(default=firefly_tool.DEFAULT_IMAGE_HEIGHT)
    visual_intensity: int = Field(default=firefly_tool.DEFAULT_VISUAL_INTENSITY)
    locale: str = Field(default=firefly_tool.DEFAULT_LOCALE)
    avoid: str = Field(default=None)
    reference_image: str = Field(default=None)
    mask_image: str = Field(default=None)


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: list[ResponseMessageModel] = Field(min_items=1)


def call_adobe_firefly_api(input_data: InputModel) -> str:
    """
    Makes a call to the Firefly API, authenticating as needed.

    Authentication is handled by taking the Client ID and Secret,
    then making an OAuth request for an access token.

    Args:
        input_data (InputModel): The input data for the API call.

    Returns:
        str: The presigned URL of the generated image.

    Raises:
        FireflyAuthException: If there is an error authenticating with Firefly.
        requests.RequestException: If there is an error making the API call.

    Examples:
        >>> input_data = InputModel(query="A beautiful sunset")
        >>> image_url = call_adobe_firefly_api(input_data)
        >>> assert image_url.startswith("https://")

    """
    match input_data.action:
        case "expand":
            input_json = json.dumps({
                "query": input_data.query, 
                "width": input_data.width, 
                "height": input_data.height, 
                "reference_image": input_data.reference_image })
            return firefly_tool.adobe_firefly_image_expand(input_json)
        case "fill":
            input_json = json.dumps({
                "query": input_data.query, 
                "width": input_data.width, 
                "height": input_data.height, 
                "reference_image": input_data.reference_image,
                "mask_image": input_data.mask_image })
            return firefly_tool.adobe_firefly_generative_fill(input_json)
        case _:
            input_json = json.dumps({
                "query": input_data.query,
                "image_type": input_data.image_type, 
                "width": input_data.width, 
                "height": input_data.height,
                "visual_intensity": input_data.visual_intensity, 
                "reference_image": input_data.reference_image,
                "locale": input_data.locale,
                "avoid": input_data.avoid })            
            return firefly_tool.adobe_firefly_image_generation(input_json)


def download_image(image_url: str, output_path: str) -> None:
    """
    Downloads an image from a URL and saves it to the specified output path.

    Args:
        image_url (str): The URL of the image to download.
        output_path (str): The path where the downloaded image will be saved.

    Raises:
        requests.RequestException: If there is an error downloading the image.

    Examples:
        >>> image_url = "https://example.com/image.png"
        >>> output_path = "public/firefly/image.png"
        >>> download_image(image_url, output_path)
        >>> assert os.path.exists(output_path)

    """
    response = requests.get(image_url)
    response.raise_for_status()
    with open(output_path, "wb") as file:
        file.write(response.content)


def add_custom_routes(app: FastAPI):
    @app.post("/firefly/invoke")
    async def adobe_firefly_request(request: Request):
        """
        Handles the POST request to generate images using Adobe Firefly.

        This function takes the input data from the request, calls the Adobe Firefly API to generate an image,
        downloads the generated image, and returns a response containing both a text message and an image URL.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, invocation ID, and response messages.

        Raises:
            HTTPException: If there is an error processing the request or generating the image.

        Example:
            >>> import requests
            >>> url = "https://your-app-url.com/firefly/invoke"
            >>> data = {
            ...     "query": "A beautiful sunset",
            ...     "image_type": "photo",
            ...     "width": 1024,
            ...     "height": 1024
            ... }
            >>> headers = {"Content-Type": "application/json"}
            >>> response = requests.post(url, json=data, headers=headers)
            >>> response.json()
            {
                "status": "success",
                "invocationId": "f62692d9-f6ce-47a5-b80e-2457083e914d",
                "response": [
                    {
                        "message": "Image Generation Result...",
                        "type": "text"
                    },
                    {
                        "message": "https://SERVER-NAME/public/firefly/f62692d9-f6ce-47a5-b80e-2457083e914d.png",
                        "type": "image"
                    }
                ]
            }
        """
        try:
            data = await request.json()
            input_data = InputModel(**data)

            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                firefly_response = await loop.run_in_executor(executor, call_adobe_firefly_api, input_data)

            invocation_id = str(uuid.uuid4())
            image_filename = f"{invocation_id}.png"
            output_path = f"public/firefly/{image_filename}"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            download_image(firefly_response, output_path)

            # Compose the server name
            image_url = f"{SERVER_NAME}/public/firefly/{image_filename}"

            template = template_env.get_template("firefly_response.jinja")
            formatted_result = template.render(image_url=image_url, source_url=firefly_response)

            response = OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[
                    ResponseMessageModel(message=formatted_result, type="text"),
                    ResponseMessageModel(message=image_url, type="image"),
                ],
            )

        except firefly_tool.FireflyAuthException as e:
            log.error(f"Firefly authentication error: {e}")
            formatted_result = "I'm sorry but the Firefly integration is misconfigured, or is not allowed to run this query."
            response = OutputModel(
                status="success", 
                invocationId=str(uuid.uuid4()), 
                response=[ResponseMessageModel(message=formatted_result, type="text")]
            )
        except ValueError:
            formatted_result = "I'm sorry but the input is invalid"
            response = OutputModel(
                status="success", 
                invocationId=str(uuid.uuid4()), 
                response=[ResponseMessageModel(message=formatted_result, type="text")]
            )
        except Exception as e:
            log.error(f"Firefly API error: {e}")
            formatted_result = "I'm sorry but I couldn't find a response, please try with a different query or image."
            response = OutputModel(
                status="success",
                invocationId=str(uuid.uuid4()),
                response=[ResponseMessageModel(message=formatted_result, type="text")],
            )

        return response
