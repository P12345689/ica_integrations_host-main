# -*- coding: utf-8 -*-
"""
db2_integration tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..db2_integration_router import generate_timestamp


@tool
def get_db2_integration_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current db2_integration in the specified format.

    Args:
        format (str, optional): The format string for the db2_integration. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted db2_integration.

    Example:
        >>> result = get_db2_integration_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_db2_integration_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)

@tool
def get_db2_integration_info() -> str:
    """
    Tool for getting information about the db2_integration integration.

    Returns:
        str: Information about the db2_integration integration.

    Example:
        >>> info = get_db2_integration_info()
        >>> assert "db2_integration" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The db2_integration integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )

# You can add more tool functions as needed for your specific integration
