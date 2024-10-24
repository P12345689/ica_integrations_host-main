# -*- coding: utf-8 -*-
"""
{{cookiecutter.module_name}} tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..{{cookiecutter.module_name}}_router import generate_timestamp


@tool
def get_{{cookiecutter.module_name}}_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current {{cookiecutter.module_name}} in the specified format.

    Args:
        format (str, optional): The format string for the {{cookiecutter.module_name}}. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted {{cookiecutter.module_name}}.

    Example:
        >>> result = get_{{cookiecutter.module_name}}_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_{{cookiecutter.module_name}}_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)

@tool
def get_{{cookiecutter.module_name}}_info() -> str:
    """
    Tool for getting information about the {{cookiecutter.module_name}} integration.

    Returns:
        str: Information about the {{cookiecutter.module_name}} integration.

    Example:
        >>> info = get_{{cookiecutter.module_name}}_info()
        >>> assert "{{cookiecutter.module_name}}" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The {{cookiecutter.module_name}} integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )

# You can add more tool functions as needed for your specific integration
