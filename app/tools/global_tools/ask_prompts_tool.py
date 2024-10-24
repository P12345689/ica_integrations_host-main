# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Prompt tool for retrieving and filtering prompts.

This module provides a tool that uses the prompt retrieval functionality from the main router.
"""

import json

from langchain.agents import tool

# Import the get_prompts function from the main router
from app.routes.ask_prompts.ask_prompts_router import get_prompts


@tool
def get_prompts_tool(input_str: str) -> str:
    """
    Tool for retrieving and filtering prompts based on various criteria.

    Args:
        input_str (str): A JSON string containing the search criteria.
            Possible keys:
            - tags (Optional[Union[str, List[str]]]): Tag or list of tags to filter prompts.
            - roles (Optional[Union[str, List[str]]]): Role or list of roles to filter prompts.
            - search_term (Optional[str]): Search term for prompt title or description.
            - visibility (Optional[str]): Visibility filter (e.g., 'TEAM', 'PUBLIC').
            - user_email (Optional[str]): Filter by user email.
            - prompt_id (Optional[str]): Specific prompt ID to retrieve.

    Returns:
        str: A formatted string containing information about the matching prompts.

    Example:
        >>> get_prompts_tool('{"tags": ["python"], "roles": "developer"}')
        'Matching prompts: ...'
    """
    try:
        input_data = json.loads(input_str)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    tags = input_data.get("tags")
    roles = input_data.get("roles")
    search_term = input_data.get("search_term")
    visibility = input_data.get("visibility")
    user_email = input_data.get("user_email")
    prompt_id = input_data.get("prompt_id")

    # Convert string to list for tags and roles if necessary
    if isinstance(tags, str):
        tags = [tags]
    if isinstance(roles, str):
        roles = [roles]

    prompts = get_prompts(tags, roles, search_term, visibility, user_email, prompt_id)

    if not prompts:
        return "No prompts found matching the specified criteria."

    result = "Matching prompts:\n\n"
    for prompt in prompts:
        result += f"Title: {prompt.promptTitle}\n"
        result += f"ID: {prompt.promptId}\n"
        result += f"Description: {prompt.description}\n"
        result += f"Tags: {', '.join(tag.name for tag in prompt.tags)}\n"
        result += f"Roles: {', '.join(role.name for role in prompt.roles)}\n"
        result += f"Visibility: {prompt.visibility}\n"
        result += f"Created By: {prompt.userEmail}\n\n"

    return result
