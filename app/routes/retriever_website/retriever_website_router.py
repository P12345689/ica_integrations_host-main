# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Website content retriever API

This module provides API endpoints for retrieving the content of a website and converting it to plain text.
It allows users to send a URL, and the API will fetch the content, extract the text, and return it in a structured format.

The module uses asynchronous calls to retrieve website content and returns the response in a structured format,
including a unique invocation ID.

Examples:
    >>> from fastapi.testclient import TestClient
    >>> client = TestClient(app)
    >>> response = client.post("/retriever_website/invoke", json={"url": "https://example.com"})
    >>> response.status_code
    200
    >>> response.json()["status"]
    "success"
"""

import json
import logging
from typing import List, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from app.tools.global_tools.retriever_website_tool import retrieve_website_content

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

app = FastAPI()


class WebsiteRetrieverRequest(BaseModel):
    """
    Represents the request for the website content retriever.

    Attributes:
        url (str): The URL of the website to retrieve content from.
    """

    url: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text"]


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

    @app.post("/retriever_website/invoke", response_model=OutputModel)
    async def retriever_website(request: Request) -> OutputModel:
        """
        Endpoint for retrieving website content and converting it to plain text.

        Args:
            request (Request): The incoming request object containing the URL.

        Returns:
            OutputModel: The structured output response containing the extracted text.

        Raises:
            HTTPException: If there's an error processing the request or if the JSON is invalid.
        """
        try:
            data = await request.json()
            website_request = WebsiteRetrieverRequest(**data)

            input_json = json.dumps({"url": website_request.url})

            content = retrieve_website_content(input_json)
            response_message = ResponseMessageModel(message=content, type="text")
            output_model = OutputModel(invocationId=str(uuid4()), response=[response_message])

            return output_model

        except ValueError as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

        except Exception as e:
            log.error(f"Failed to process the request: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to retrieve website content")

    @app.post(
        "/system/retriever_website/transformers/url_to_text/invoke",
        response_model=OutputModel,
    )
    async def retriever_website_system(request: Request) -> OutputModel:
        """
        System endpoint for retrieving website content and converting it to plain text.

        Args:
            request (Request): The incoming request object containing the URL.

        Returns:
            OutputModel: The structured output response containing the extracted text.

        Raises:
            HTTPException: If there's an error processing the request or if the JSON is invalid.
        """
        return await retriever_website(request)


# Add the routes to the app
add_custom_routes(app)
