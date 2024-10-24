# -*- coding: utf-8 -*-
"""
ms_teams tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..ms_teams_router import generate_timestamp


@tool
def get_ms_teams_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current ms_teams in the specified format.

    Args:
        format (str, optional): The format string for the ms_teams. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted ms_teams.

    Example:
        >>> result = get_ms_teams_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_ms_teams_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)


@tool
def get_ms_teams_info() -> str:
    """
    Tool for getting information about the ms_teams integration.

    Returns:
        str: Information about the ms_teams integration.

    Example:
        >>> info = get_ms_teams_info()
        >>> assert "ms_teams" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The ms_teams integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )


# You can add more tool functions as needed for your specific integration
