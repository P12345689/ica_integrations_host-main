# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti (updated)
Description: Agent Copilot Integration for interacting with Azure OpenAI Assistants API

This module provides a streamlined interface for interacting with Azure OpenAI Assistants.
It handles the entire conversation flow, including thread creation, message sending,
and running the assistant.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from typing import Dict, List
from uuid import uuid4

import requests
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Load environment variables
AGENT_COPILOT_ENDPOINT = os.getenv("AGENT_COPILOT_ENDPOINT", "https://va-gpt-4omni.openai.azure.com/")
AGENT_COPILOT_API_KEY = os.getenv("AGENT_COPILOT_API_KEY", "")
AGENT_COPILOT_API_VERSION = os.getenv("AGENT_COPILOT_API_VERSION", "2024-02-15-preview")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Define available assistants
AVAILABLE_ASSISTANTS = {
    "appmod": "asst_u60Wef7HJOWjHuOV6nhuBHsS",
    "migration": "asst_xfL12XBmKIM2pfzeMMOiQz3e",
}

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/agent_copilot/templates"))


class ConversationInputModel(BaseModel):
    """Model to validate input data for the conversation."""

    message: str = Field(..., description="The message to send to the assistant")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def agent_copilot_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Agent Copilot API.

    Args:
        method (str): HTTP method (GET, POST, etc.)
        endpoint (str): API endpoint
        data (Dict, optional): Request payload

    Returns:
        Dict: API response

    Raises:
        HTTPException: If the API request fails
    """
    url = f"{AGENT_COPILOT_ENDPOINT}/openai/{endpoint}"
    headers = {"api-key": AGENT_COPILOT_API_KEY, "Content-Type": "application/json"}
    params = {"api-version": AGENT_COPILOT_API_VERSION}

    try:
        response = requests.request(method, url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log.error(f"Agent Copilot API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with Agent Copilot API: {str(e)}",
        )


async def create_thread_and_run(assistant_id: str, message: str) -> Dict:
    """
    Create a new thread, send a message, and run the assistant.

    Args:
        assistant_id (str): The ID of the assistant to use
        message (str): The initial message to start the conversation

    Returns:
        Dict: The result of the assistant run

    Raises:
        HTTPException: If any step in the process fails
    """
    try:
        # Create a new thread with the initial message
        thread = agent_copilot_request("POST", "threads", {"messages": [{"role": "user", "content": message}]})
        thread_id = thread["id"]
        log.info(f"Thread created with ID: {thread_id}")

        # Run the assistant on the thread
        run = agent_copilot_request("POST", f"threads/{thread_id}/runs", {"assistant_id": assistant_id})
        run_id = run["id"]
        log.info(f"Run initiated with ID: {run_id}")

        # Wait for the run to complete
        while True:
            run_status = agent_copilot_request("GET", f"threads/{thread_id}/runs/{run_id}")
            status = run_status["status"]
            log.info(f"Run status: {status}")
            if status == "completed":
                break
            elif status in ["failed", "cancelled", "expired"]:
                raise HTTPException(status_code=500, detail=f"Run failed with status: {status}")
            await asyncio.sleep(1)

        # Retrieve the assistant's response
        messages = agent_copilot_request("GET", f"threads/{thread_id}/messages")
        assistant_response = messages["data"][0]["content"][0]["text"]["value"]
        log.info("Assistant response retrieved")

        return {"thread_id": thread_id, "response": assistant_response}
    except Exception as e:
        log.error(f"Error in create_thread_and_run: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to complete conversation: {str(e)}")


def add_custom_routes(app: FastAPI):
    @app.post("/agent_copilot/{assistant_name}/invoke")
    async def invoke_assistant(assistant_name: str, request: Request) -> OutputModel:
        """
        Invoke an assistant for a conversation.

        Args:
            assistant_name (str): The name of the assistant to invoke
            request (Request): The incoming request containing the conversation input

        Returns:
            OutputModel: The structured output response

        Raises:
            HTTPException: If the assistant is not found or if there's an error in processing
        """
        log.info(f"Received request to invoke assistant: {assistant_name}")
        invocation_id = str(uuid4())

        if assistant_name not in AVAILABLE_ASSISTANTS:
            raise HTTPException(status_code=404, detail=f"Assistant '{assistant_name}' not found")

        assistant_id = AVAILABLE_ASSISTANTS[assistant_name]

        try:
            data = await request.json()
            input_data = ConversationInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            result = await create_thread_and_run(assistant_id, input_data.message)
        except Exception as e:
            log.error(f"Error in conversation: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

        log.info(f"Conversation completed for thread: {result['thread_id']}")
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(
            result=f"Assistant response: {result['response']}",
            action=f"invoke_{assistant_name}",
        )
        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.get("/agent_copilot/assistants")
    async def list_assistants() -> Dict[str, str]:
        """
        List available assistants.

        Returns:
            Dict[str, str]: A dictionary of available assistants and their IDs
        """
        return AVAILABLE_ASSISTANTS
