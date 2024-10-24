# -*- coding: utf-8 -*-
"""
System time tool for retrieving the current time.

This module provides a tool that uses the time retrieval functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the get_system_time function from the main router
from app.routes.time.time_router import get_system_time


@tool
def get_system_time_tool(format: Optional[str] = "%Y-%m-%dT%H:%M:%S%Z") -> str:
    """
    Tool for getting the current system time in the specified format.

    Args:
        format (str, optional): The format string for the time. Defaults to "%Y-%m-%dT%H:%M:%S%Z".

    Returns:
        str: The formatted current time.
    """
    return get_system_time(format)
