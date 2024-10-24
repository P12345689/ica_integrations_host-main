# -*- coding: utf-8 -*-
"""
model_router tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..model_router_router import generate_timestamp


@tool
def get_model_router_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current model_router in the specified format.

    Args:
        format (str, optional): The format string for the model_router. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted model_router.

    Example:
        >>> result = get_model_router_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_model_router_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)


@tool
def get_model_router_info() -> str:
    """
    Tool for getting information about the model_router integration.

    Returns:
        str: Information about the model_router integration.

    Example:
        >>> info = get_model_router_info()
        >>> assert "model_router" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The model_router integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )


# You can add more tool functions as needed for your specific integration
