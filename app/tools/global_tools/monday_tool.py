# -*- coding: utf-8 -*-
"""
Monday.com integration tool for use with LangChain.

This module provides tools that use the Monday.com API functionality from the main router.
"""

from typing import Any, Dict, Optional

from langchain.agents import tool

from app.routes.monday.monday_router import call_monday_api


@tool
async def monday_api_tool(query: str, variables: Optional[Dict[str, Any]] = None) -> str:
    """
    Tool for making Monday.com API calls.

    Args:
        query (str): The GraphQL query or mutation.
        variables (Optional[Dict[str, Any]]): Variables for the GraphQL query.

    Returns:
        str: The JSON response from the Monday.com API as a string.

    Example:
        >>> result = monday_api_tool("query { boards { id name } }")
        >>> isinstance(result, str)
        True
    """
    result = await call_monday_api(query, variables)
    return str(result)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
