# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Executes an assistant with the provided prompt. Used as a tool by other integrations.

This module provides an API endpoint for executing an assistant based on the provided assistant ID and prompt.
It uses the ICAClient to make asynchronous calls to the LLM (Language Model) and returns the response in the
specified format, including a unique invocation ID.

Examples:
    >>> from fastapi.testclient import TestClient
    >>> client = TestClient(app)
    >>> response = client.post("/system/assistant_executor/retrievers/assistant/invoke", json={"assistant_id": "74", "prompt": "App to open the car trunk using facial recognition"})
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

from fastapi import FastAPI, HTTPException, Request
from libica import ICAClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))


class ExecutionRequest(BaseModel):
    """
    Represents the request for executing an assistant.

    Attributes:
        assistant_id (str): The ID of the assistant to be executed.
        prompt (str): The prompt to be passed to the assistant.
    """

    assistant_id: str
    prompt: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: Annotated[List[ResponseMessageModel], Field(min_length=1)]


def is_assistant_valid(client: ICAClient, assistant_id: str) -> bool:
    """
    Checks to see if the assistant_id given exists.

    Attributes:
        client (str): The prompt to be passed to the assistant.
        assistant_id (str): The ID of the assistant to be executed.
    """
    found_assistant = False

    # Check if assistant_id exists
    with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
        # Get the assistants list
        assistants_list_future = executor.submit(client.get_assistants, refresh_data=True)
        assistants_list = assistants_list_future.result()
        for assistant in assistants_list:
            if assistant["id"] == str(assistant_id):
                log.info(f"*Found assistant_id: {assistant_id}")
                found_assistant = True
                break

    return found_assistant


def add_custom_routes(app: FastAPI) -> None:
    """
    Adds custom routes to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.post(
        "/system/assistant_executor/retrievers/assistant/invoke",
        response_model=OutputModel,
    )
    async def assistant_executor(request: Request) -> OutputModel:
        """
        Endpoint for executing an assistant based on the provided assistant ID and prompt.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error processing the request.
        """
        try:
            body_text = await request.body()
            log.info(f"Received raw request body: {body_text}")

            clean_text = body_text.replace(b"\r\n", b"\n").decode("utf-8")
            formatted_json = clean_text.replace("\n", "\\n")
            log.info(f"Cleaned request text from Windows newlines: {formatted_json}")

            execution_request = ExecutionRequest.parse_raw(formatted_json)
            if not execution_request.prompt or not execution_request.assistant_id:
                raise json.JSONDecodeError("One or more field(s) are empty", execution_request.prompt, 0)
            log.info(f"Parsed JSON data successfully: {execution_request}")
        except json.JSONDecodeError as e:
            log.error(f"Failed to decode JSON: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON input: {str(e)}")

        try:
            client = ICAClient()

            if not is_assistant_valid(client=client, assistant_id=execution_request.assistant_id):
                raise HTTPException(status_code=400,
                                    detail=f"Invalid 'assistant_id' field. Assistant with ID: {execution_request.assistant_id} not found.")

            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                # Call LLM to execute the assistant
                llm_future = executor.submit(
                    client.prompt_flow,
                    assistant_id=execution_request.assistant_id,
                    prompt=execution_request.prompt,
                )

                # Wait for the LLM response
                llm_response = llm_future.result()
                log.info(f"LLM response: {llm_response}")

            response_message = ResponseMessageModel(message=llm_response.strip(), type="text")
            output_model = OutputModel(invocationId=str(uuid4()), response=[response_message])

            return output_model

        except HTTPException as e:
            log.error(f"HTTPException: {str(e)}")
            raise e
        except Exception as e:
            log.error(f"Failed to process the request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
