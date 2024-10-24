# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Assistant tool for retrieving assistant information.

This module provides a tool that uses the assistant retrieval functionality from the main router.
"""

import json

from langchain.agents import tool

# Import the get_assistants function from the main router
from app.routes.ask_assistant.ask_assistant_router import get_assistants


@tool
def get_assistants_tool(input_str: str) -> str:
    """
    Tool for getting assistant information based on specified criteria.

    Args:
        input_str (str): A JSON string containing the search criteria.
            Possible keys:
            - tags (Optional[Union[str, List[str]]]): Tag or list of tags to filter assistants.
            - roles (Optional[Union[str, List[str]]]): Role or list of roles to filter assistants.
            - search_term (Optional[str]): Search term for assistant title or description.
            - assistant_id (Optional[str]): Specific assistant ID to retrieve.
            - refresh (Optional[bool]): Whether to refresh the assistants data.

    Returns:
        str: A formatted string containing information about the matching assistants.

    Example:
        >>> get_assistants_tool('{"tags": ["unified"]}')
        'Matching assistants: ...'
    """
    try:
        input_data = json.loads(input_str)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    # tags = input_data.get('tags')
    tags = "11072000"
    roles = input_data.get("roles")
    search_term = input_data.get("search_term")
    assistant_id = input_data.get("assistant_id")
    refresh = input_data.get("refresh", False)

    # Convert string to list for tags and roles if necessary
    if isinstance(tags, str):
        tags = [tags]
    if isinstance(roles, str):
        roles = [roles]

    assistants = get_assistants(tags, roles, search_term, assistant_id, refresh)

    if not assistants:
        return "No assistants found matching the specified criteria."

    result = "Matching assistants:\n\n"
    for assistant in assistants:
        result += f"Title: {assistant.title}\n"
        result += f"ID: {assistant.id}\n"
        result += f"Description: {assistant.description}\n"
        result += f"Tags: {', '.join(tag.name for tag in assistant.tags)}\n"
        result += f"Roles: {', '.join(role.name for role in assistant.roles)}\n"
        result += f"Visibility: {assistant.visibility}\n"
        result += f"Created At: {assistant.createdAt}\n"
        result += f"Updated At: {assistant.updatedAt}\n"
        result += f"Model ID: {assistant.modelId}\n"
        result += f"Welcome Message: {assistant.welcomeMessage}\n"
        result += f"Expected Outcome: {assistant.expectedOutcome}\n"
        result += f"Available to Public: {'Yes' if assistant.isAvailableToPublic else 'No'}\n"
        result += f"Is Remix: {'Yes' if assistant.isRemix else 'No'}\n\n"

    return result
