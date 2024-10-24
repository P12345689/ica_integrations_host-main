# -*- coding: utf-8 -*-
"""
watson_discovery tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..watson_discovery_router import generate_timestamp


@tool
def get_watson_discovery_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current watson_discovery in the specified format.

    Args:
        format (str, optional): The format string for the watson_discovery. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted watson_discovery.

    Example:
        >>> result = get_watson_discovery_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_watson_discovery_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)


@tool
def get_watson_discovery_info() -> str:
    """
    Tool for getting information about the watson_discovery integration.

    Returns:
        str: Information about the watson_discovery integration.

    Example:
        >>> info = get_watson_discovery_info()
        >>> assert "watson_discovery" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The watson_discovery integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )


# You can add more tool functions as needed for your specific integration
