# -*- coding: utf-8 -*-
"""
batch_execution tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..batch_execution_router import generate_timestamp


@tool
def get_batch_execution_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current batch_execution in the specified format.

    Args:
        format (str, optional): The format string for the batch_execution. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted batch_execution.

    Example:
        >>> result = get_batch_execution_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_batch_execution_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)


@tool
def get_batch_execution_info() -> str:
    """
    Tool for getting information about the batch_execution integration.

    Returns:
        str: Information about the batch_execution integration.

    Example:
        >>> info = get_batch_execution_info()
        >>> assert "batch_execution" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The batch_execution integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )


# You can add more tool functions as needed for your specific integration
