# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Assistant executor tool.

This module provides a tool that calls assistants using the ICAClient.
"""

import json

from langchain.agents import tool

# Import the ICAClient from the main router
from app.routes.assistant_executor.assistant_executor_router import ICAClient


@tool
def assistant_executor_tool(input_str: str) -> str:
    """
    Tool for executing an assistant based on the provided assistant ID and prompt.

    Args:
        input_str (str): A JSON string containing the execution parameters.
            Required keys:
            - assistant_id (str): The ID of the assistant to be executed.
            - prompt (str): The prompt to be passed to the assistant.

    Returns:
        str: The response from the executed assistant.

    Example:
        >>> assistant_executor_tool('{"assistant_id": "3903", "prompt": "App to open the car trunk using facial recognition"}')
        'Response from assistant: ...'
    """
    try:
        input_data = json.loads(input_str)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    assistant_id = input_data.get("assistant_id")
    prompt = input_data.get("prompt")

    if not assistant_id or not prompt:
        return "Error: Both 'assistant_id' and 'prompt' are required in the input."

    try:
        client = ICAClient()
        response = client.prompt_flow(assistant_id=assistant_id, prompt=prompt)
        return f"Response from assistant: {response}"

    except Exception as e:
        return f"Error: Failed to execute assistant. Details: {str(e)}"
