# -*- coding: utf-8 -*-
"""
mail_template_creation tool for retrieving the current time or generating timestamps.

This module provides a tool that wraps the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate_timestamp function from the main router
from ..mail_template_creation_router import generate_timestamp


@tool
def get_mail_template_creation_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Tool for getting the current mail_template_creation in the specified format.

    Args:
        format (str, optional): The format string for the mail_template_creation. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted mail_template_creation.

    Example:
        >>> result = get_mail_template_creation_tool()
        >>> import re
        >>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
        >>> custom_result = get_mail_template_creation_tool("%Y-%m-%d")
        >>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
    """
    return generate_timestamp(format)


@tool
def get_mail_template_creation_info() -> str:
    """
    Tool for getting information about the mail_template_creation integration.

    Returns:
        str: Information about the mail_template_creation integration.

    Example:
        >>> info = get_mail_template_creation_info()
        >>> assert "mail_template_creation" in info
        >>> assert "generate timestamps" in info
    """
    return (
        "The mail_template_creation integration provides functionality to generate timestamps "
        "and interact with time-related queries. It can format timestamps in various ways and "
        "provide information about dates and times."
    )


# You can add more tool functions as needed for your specific integration
