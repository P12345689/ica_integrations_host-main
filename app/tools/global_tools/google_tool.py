# -*- coding: utf-8 -*-
"""
Authors: Adrian Popa
Description: Google tool that returns snipet + URL

"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from langchain.agents import tool
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper

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
async def google_search(query: str) -> str:
    """
    Searches google and returns entries matching the query.

    Args:
        query (str): The search string to look up on Google.

    Returns:
        str: An string containing the search results. For each result it returns a snippet of the web page followed by page URL

    Raises:
        Exception: If there's an error during the Google search process.
    """
    try:
        # Create the search input
        search_input = GoogleSearchAPIWrapper()
        outputs = search_input.results(query, 5)
        result = ""
        for output in outputs:
            result = result + output["snippet"] + "(" + output["link"] + "). "

        return result
    except Exception as e:
        log.error(f"Failed to search Google: {str(e)}")
        return f"Failed to search Google: {str(e)}"


# Example usage
if __name__ == "__main__":
    response = google_search("What is London Bridge")
    print(response)
