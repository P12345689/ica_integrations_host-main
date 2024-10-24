# -*- coding: utf-8 -*-
"""
Description: GPT-4 Vision API integration for image-to-text transformation.

This module provides API endpoints for integrating with the GPT-4 Vision API to perform image-to-text transformation.
It allows users to send an image URL along with a query, and the GPT-4 Vision API will process the image and generate
a textual response based on the provided query.

The module uses asynchronous calls to the GPT-4 Vision API and returns the response in a structured format, including
a unique invocation ID.

Examples:
    >>> from fastapi.testclient import TestClient
    >>> client = TestClient(app)
    >>> response = client.post("/gpt4vision_imagetotext/invoke", json={"query": "What is in the image?", "image_url": "https://example.com/img.jpg"})
    >>> response.status_code
    200
    >>> response.json()["status"]
    "success"
"""

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Literal
from uuid import uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from app.tools.global_tools.gpt4vision_tool import call_gpt4_vision_api

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

app = FastAPI()

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))


class GPT4VisionRequest(BaseModel):
    """
    Represents the request for the GPT-4 Vision API.

    Attributes:
        query (str): The query to be sent to the GPT-4 Vision API.
        image_url (str): The URL of the image to be processed by the GPT-4 Vision API.
    """

    query: str
    image_url: str


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
    """
    Adds custom routes to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.post("/gpt4vision_imagetotext/invoke", response_model=OutputModel)
    async def gpt4vision_imagetotext(request: Request) -> OutputModel:
        """
        Endpoint for image-to-text transformation using the GPT-4 Vision API.

        Args:
            request (Request): The incoming request object containing the query and image URL.

        Returns:
            OutputModel: The structured output response containing the transformed text.

        Raises:
            HTTPException: If there's an error processing the request or if the JSON is invalid.
        """
        return await gpt4vision_image_to_text_system(request)

    @app.post("/experience/gpt4vision/askimage/invoke", response_model=OutputModel)
    async def gpt4vision_imagetotext_experience(request: Request) -> OutputModel:
        """
        Endpoint for image-to-text transformation using the GPT-4 Vision API (experience route).

        Args:
            request (Request): The incoming request object containing the query and image URL.

        Returns:
            OutputModel: The structured output response containing the transformed text.

        Raises:
            HTTPException: If there's an error processing the request or if the JSON is invalid.
        """
        return await gpt4vision_image_to_text_system(request)

    @app.post(
        "/system/gpt4vision/transformers/image_to_text/invoke",
        response_model=OutputModel,
    )
    async def gpt4vision_image_to_text_system(request: Request) -> OutputModel:
        """
        Endpoint for image-to-text transformation using the GPT-4 Vision API (system route).

        Args:
            request (Request): The incoming request object containing the query and image URL.

        Returns:
            OutputModel: The structured output response containing the transformed text.

        Raises:
            HTTPException: If there's an error processing the request or if the JSON is invalid.
        """
        try:
            data = await request.json()
            gpt4vision_request = GPT4VisionRequest(**data)

            input_json = json.dumps(
                {
                    "image": gpt4vision_request.image_url,
                    "query": gpt4vision_request.query,
                }
            )

            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                gpt4_vision_future = executor.submit(call_gpt4_vision_api, input_json)
                formatted_result = gpt4_vision_future.result()

        except ValueError as value_error:
            formatted_result = f"Invalid input. {str(value_error)}"

        except Exception as e:
            log.error(f"Failed to process the request: {str(e)}")
            formatted_result = "I'm sorry but I couldn't find a response, please try with a different query or image."

        response_message = ResponseMessageModel(message=formatted_result, type="text")
        output_model = OutputModel(invocationId=str(uuid4()), response=[response_message])

        return output_model
