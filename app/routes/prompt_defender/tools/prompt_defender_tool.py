# -*- coding: utf-8 -*-
"""
prompt_defender tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..prompt_defender_router import generate_timestamp


@tool
def get_prompt_defender_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current prompt_defender in the specified format.

    Args:
        format (str, optional): The format string for the prompt_defender. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted prompt_defender.

    Example:
        >>> result = get_prompt_defender_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_prompt_defender_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)


@tool
def get_prompt_defender_info() -> str:
    """
    Tool for getting information about the prompt_defender integration.

    Returns:
        str: Information about the prompt_defender integration.

    Example:
        >>> info = get_prompt_defender_info()
        >>> assert "prompt_defender" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The prompt_defender integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )


# You can add more tool functions as needed for your specific integration
