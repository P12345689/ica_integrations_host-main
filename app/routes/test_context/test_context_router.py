# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Test route that returns debug information about the client connection and input parameters.

This module provides test routes that capture and return various details about the incoming request,
including headers, client information, input parameters, and a curl command to reproduce the request.
It includes support for context handling in a conversational debug route.
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, ValidationError

from ...agents.agent_context import format_context, parse_context

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


class InputModel(BaseModel):
    """Model for incoming request data including context."""

    query: str = Field(description="Query to execute against the agent.")
    context: Optional[str] = Field(default=None, description="Stringified JSON of context items.")
    use_context: bool = Field(default=False, description="Whether to use the provided context.")


def format_headers(headers: Dict[str, str]) -> str:
    """Format request headers into a string."""
    return "\n".join([f"{k}: {v}" for k, v in headers.items()])


def format_curl_command(request: Request, data: Dict[str, Any]) -> str:
    """Format a curl command based on the request."""
    headers = " ".join([f"-H '{k}: {v}'" for k, v in request.headers.items()])
    data_str = f"-d '{json.dumps(data)}'" if data else ""
    return f"curl -X {request.method} {request.url} {headers} {data_str}".strip()


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/test/debug/conversation")
    async def test_conversation_debug(request: Request) -> OutputModel:
        """Handle requests to the conversational debug route."""
        log.info(f"Received POST request to {request.url}")

        try:
            data = await request.json()
            input_data = InputModel(**data)
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            return OutputModel(
                status="error",
                invocationId=str(uuid4()),
                response=[ResponseMessageModel(message="Invalid JSON", type="error")],
            )
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            return OutputModel(
                status="error",
                invocationId=str(uuid4()),
                response=[ResponseMessageModel(message=str(e), type="error")],
            )

        context_items = parse_context(input_data.context) if input_data.use_context else []
        formatted_context = format_context(context_items) if context_items else "No context provided"

        debug_info = [
            f"Query: {input_data.query}",
            f"Use Context: {input_data.use_context}",
            "\n# Formatted Context:",
            formatted_context,
            "\n# Raw Context Data:",
            json.dumps(input_data.context, indent=2) if input_data.context else "None",
            "\n# Curl Command:",
            format_curl_command(request, data),
        ]

        invocation_id = str(uuid4())
        debug_message = "\n".join(debug_info)

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            response_message = await asyncio.to_thread(lambda: ResponseMessageModel(message=debug_message, type="text"))

        return OutputModel(status="success", invocationId=invocation_id, response=[response_message])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
