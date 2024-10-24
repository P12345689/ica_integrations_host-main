# -*- coding: utf-8 -*-
"""
Authors: Mihai Criveti
Description: Wikipedia tool for use with langchain agents

This module provides a tool for searching Wikipedia entries using langchain agents.
It handles the asynchronous nature of the Wikipedia search function by running it
in a separate thread, allowing it to work within the synchronous context of langchain tools.
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from langchain.agents import tool

from app.routes.wikipedia.wikipedia_router import WikipediaSearchInput, search_wikipedia

# Set up logging
log = logging.getLogger(__name__)


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
async def search_wikipedia_entries(query: str) -> dict:
    """
    Searches Wikipedia and returns entries matching the query.

    This function is a langchain tool that performs an asynchronous Wikipedia search.
    It creates a WikipediaSearchInput object from the query string and calls the
    search_wikipedia function. The asynchronous call is handled by the run_async_in_thread
    decorator, allowing it to work within the synchronous context of langchain tools.

    Args:
        query (str): The search string to look up on Wikipedia.

    Returns:
        dict: A dictionary containing the search results. The structure depends
              on the implementation of the search_wikipedia function, and
              includes keys like 'summary', 'content', 'article_url', and 'image_url'.

    Raises:
        Exception: If there's an error during the Wikipedia search process.
    """
    try:
        # Create the search input
        search_input = WikipediaSearchInput(search_string=query)

        # Call the async search_wikipedia function
        result = await search_wikipedia(search_input)
        return result["summary"]
    except Exception as e:
        log.error(f"Failed to search Wikipedia: {str(e)}")
        return {"error": f"Failed to search Wikipedia: {str(e)}"}
