# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Test route that returns debug information about the client connection and input parameters.

This module provides a test route that captures and returns various details about the incoming request,
including headers, client information, input parameters, and a curl command to reproduce the request.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

# Constants
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def format_headers(headers: Dict[str, str]) -> str:
    """
    Format request headers into a string.

    Args:
        headers (Dict[str, str]): The request headers.

    Returns:
        str: A formatted string of headers.

    >>> format_headers({"Content-Type": "application/json", "User-Agent": "curl/7.64.1"})
    'Content-Type: application/json\\nUser-Agent: curl/7.64.1'
    """
    return "\n".join([f"{k}: {v}" for k, v in headers.items()])


def format_curl_command(request: Request, data: Dict[str, Any]) -> str:
    """
    Format a curl command based on the request.

    Args:
        request (Request): The FastAPI request object.
        data (Dict[str, Any]): The request data.

    Returns:
        str: A formatted curl command.

    >>> from fastapi.testclient import TestClient
    >>> app = FastAPI()
    >>> @app.post("/test")
    ... async def test(request: Request):
    ...     data = await request.json()
    ...     return format_curl_command(request, data)
    >>> client = TestClient(app)
    >>> response = client.post("/test", json={"key": "value"})
    >>> "curl -X POST http://testserver/test -H 'Content-Type: application/json' -d '{\"key\": \"value\"}'" in response.text
    True
    """
    headers = " ".join([f"-H '{k}: {v}'" for k, v in request.headers.items()])
    data_str = f"-d '{json.dumps(data)}'" if data else ""
    return f"curl -X {request.method} {request.url} {headers} {data_str}".strip()


def add_custom_routes(app: FastAPI) -> None:
    """
    Add custom routes to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None

    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
    >>> app.routes[-1].path
    '/system/test/debug/invoke'
    """

    @app.api_route("/test/invoke", methods=["GET", "POST", "PUT", "DELETE"])
    @app.api_route("/system/test/debug/invoke", methods=["GET", "POST", "PUT", "DELETE"])
    async def test_debug(request: Request) -> OutputModel:
        """
        Handle requests to the test debug route.

        This function captures various details about the incoming request and returns them
        along with a curl command to reproduce the request.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error processing the request.
        """
        log.info(f"Received {request.method} request to {request.url}")

        try:
            # Get request data
            data = await request.json() if request.method in ["POST", "PUT"] else dict(request.query_params)
        except json.JSONDecodeError:
            log.warning("Failed to parse JSON, attempting to read as form data")
            try:
                data = await request.form()
            except Exception as e:
                log.error(f"Error processing request data: {str(e)}")
                data = {}

        # Prepare debug information
        debug_info = [
            f"Request Method: {request.method}",
            f"Request URL: {request.url}",
            f"Client Host: {request.client.host}",
            f"Client Port: {request.client.port}",
            "\n# Headers:",
            format_headers(request.headers),
            "\n# Query Parameters:",
            json.dumps(dict(request.query_params), indent=2),
            "\n# Request Data:",
            json.dumps(data, indent=2),
            "\n# Curl Command:",
            format_curl_command(request, data),
        ]

        # Generate response
        invocation_id = str(uuid4())
        debug_message = "\n".join(debug_info)

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            response_message = await asyncio.to_thread(lambda: ResponseMessageModel(message=debug_message, type="text"))

        return OutputModel(status="success", invocationId=invocation_id, response=[response_message])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
