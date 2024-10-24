# -*- coding: utf-8 -*-
"""
ASVS Chat tool for querying CSV data.

This module provides a tool that uses the ASVS chat functionality from the main router.
"""

from typing import Optional
import json

from fastapi import UploadFile
from langchain.agents import tool
#===
from functools import wraps
import asyncio
from concurrent.futures import ThreadPoolExecutor
#===

# Import the process_csv_chat and load_dataframe functions from the main router
from app.routes.asvs_chat.asvs_chat_router import chat_with_csv # load_dataframe, process_csv_chat

def run_async_in_thread(coro):
    """
    Decorator to run an asynchronous coroutine in a separate thread.

    This decorator allows running asynchronous functions in a synchronous context
    by executing them in a separate thread with a new event loop.

    Args:
        coro (Callable): The asynchronous coroutine to be executed.

    Returns:
        Callable: A wrapped function that executes the coroutine in a thread.
    """

    @wraps(coro)
    def wrapper(*args, **kwargs):
        """
        Wrapper function that runs the coroutine in a thread.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the coroutine execution.
        """
        with ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: asyncio.run(coro(*args, **kwargs)))
            return future.result()

    return wrapper


def clean_json_string(json_string):
    # Remove the starting ```json and ending ```
    cleaned_string = json_string.replace("```json", "").replace("```", "")

    # Find the index of the last closing brace
    last_brace_index = cleaned_string.rfind('}')
    
    # Remove any text after it
    if last_brace_index != -1:
        cleaned_string = cleaned_string[:last_brace_index + 1]

    # Remove the first character if it's a single quote
    if cleaned_string.startswith("'"):
        cleaned_string = cleaned_string[1:]

    # Strip any leading/trailing whitespace or newlines
    return cleaned_string.strip()

@tool
@run_async_in_thread
async def asvs_chat_tool(input_json: str) -> str:
    """
    Tool for querying ASVS CSV data using natural language.

    Args:
        input_json (str): JSON string containing the query, csv_content or file_url.

    Returns:
        str: The response to the query based on the CSV data.
    """
    
    # Strip unnecessary characters
    input_json = input_json.strip()
    
    try:
        params = json.loads(clean_json_string(input_json))
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    query = params.get("query")
    csv_content = params.get("csv_content")
    file_url = params.get("file_url")

    response = await chat_with_csv(query=query, csv_content=csv_content, file_url=file_url)
    return response.json()
