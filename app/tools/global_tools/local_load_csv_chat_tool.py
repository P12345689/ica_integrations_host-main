# -*- coding: utf-8 -*-
"""
Chat tool for querying CSV data loading within the local-load router.

This module provides a tool that uses the local-load-csv chat functionality from the main router.
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
from app.routes.local_load_csv_chat.local_load_csv_chat_router import chat_with_csv # load_dataframe, process_csv_chat

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

@tool
@run_async_in_thread
async def local_load_csv_chat_tool(input_json: str) -> str:
    """
    Tool for querying locally-loaded CSV data using natural language.

    Args:
        input_json (str): JSON string containing the query and csvType.

    Returns:
        str: The response to the query based on the CSV data.
    """

    try:
        params = json.loads(input_json)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    query = params.get("query")
    csvType = params.get("csvType")

    response = await chat_with_csv(query, csvType)
    return response.json()
