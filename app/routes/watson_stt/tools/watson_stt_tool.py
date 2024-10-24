# -*- coding: utf-8 -*-
"""
watson_stt tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..watson_stt_router import generate_timestamp


@tool
def get_watson_stt_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current watson_stt in the specified format.

    Args:
        format (str, optional): The format string for the watson_stt. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted watson_stt.

    Example:
        >>> result = get_watson_stt_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_watson_stt_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)


@tool
def get_watson_stt_info() -> str:
    """
    Tool for getting information about the watson_stt integration.

    Returns:
        str: Information about the watson_stt integration.

    Example:
        >>> info = get_watson_stt_info()
        >>> assert "watson_stt" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The watson_stt integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )


# You can add more tool functions as needed for your specific integration
